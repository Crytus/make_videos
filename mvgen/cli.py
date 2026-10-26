"""コマンドライン。

  python make_videos.py [generate] [オプション]   動画を生成（既定のコマンド）
  python make_videos.py status                     生成状況を一覧表示
  python make_videos.py review [--serve]           確認用の review.html を作る
  python make_videos.py roughcut                   全クリップをつないだラフ版を作る
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

from . import notify as notifier
from .comfy import ComfyClient, find_video_outputs
from .config import MODES, Config
from .metadata import (MISSING, OK, STALE, UNKNOWN, effective_steps, generation_params, job_state,
                       video_state, write_meta)
from .movies import frame_length, load_movies
from .plan import ClipSettings, Job, build_jobs, list_takes, resolve_clip, take_seed
from .progress import Eta, fmt_duration, fmt_eta, rate_key
from .review import build_review, serve
from .roughcut import build_roughcut, format_cues
from .selection import load_selection
from .workflow import build_i2v_workflow, build_r2v_workflow

COMMANDS = ("generate", "status", "review", "roughcut")
DEFAULT_CONFIG = Path(__file__).resolve().parent.parent / "config.yaml"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    argv = list(sys.argv[1:] if argv is None else argv)
    # コマンド省略時は generate（従来の使い方との互換）
    command = argv.pop(0) if argv and argv[0] in COMMANDS else "generate"

    p = argparse.ArgumentParser(prog=f"make_videos.py {command}",
                                description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="設定ファイル（既定: config.yaml）")
    if command in ("generate", "status"):
        p.add_argument("--ids", nargs="*", help="対象クリップの id（省略時は全件）")
    if command == "generate":
        p.add_argument("--server", help="ComfyUI の URL")
        p.add_argument("--mode", choices=MODES)
        p.add_argument("--megapixels", type=float, help="解像度（16:9、0.2 = 608x352）")
        p.add_argument("--steps", type=int, help="サンプリングステップ数")
        p.add_argument("--turbo", action=argparse.BooleanOptionalAction, default=None,
                       help="i2v で turbo LoRA を使う / 使わない（--no-turbo）")
        p.add_argument("--seed", type=int, help="take1 の seed（全クリップ共通）")
        p.add_argument("--seed-base", type=int, help="自動 seed の基準値")
        p.add_argument("--takes", type=int, help="1クリップあたりのテイク数")
        p.add_argument("--force", action="store_true", help="生成済みの動画があっても再生成する")
        p.add_argument("--stale", action="store_true",
                       help="設定（プロンプト・画像など）が変わったテイクを再生成する")
        p.add_argument("--dry-run", action="store_true",
                       help="キュー投入せず、ワークフロー JSON を <out_dir>/workflows に書き出す")
        p.add_argument("--no-review", action="store_true", help="終了後に review.html を更新しない")
        p.add_argument("--no-notify", action="store_true", help="終了時の通知をしない")
    if command == "review":
        p.add_argument("--serve", action="store_true",
                       help="ローカルサーバーを起動し、ブラウザから選択を直接保存できるようにする")
        p.add_argument("--port", type=int, help="--serve のポート")
        p.add_argument("--no-open", action="store_true", help="ブラウザを自動で開かない")
    if command == "roughcut":
        p.add_argument("--audio", type=Path, help="重ねる音源（歌）。省略時は config の roughcut.audio")
        p.add_argument("--output", type=Path, help="出力ファイル")
    args = p.parse_args(argv)
    args.command = command
    return args


def _cli_overrides(args) -> dict:
    return {"mode": args.mode, "megapixels": args.megapixels, "steps": args.steps,
            "turbo": args.turbo, "seed": args.seed, "seed_base": args.seed_base,
            "takes": args.takes}


def _select_movies(movies: list[dict], ids: list[str] | None) -> list[dict]:
    if not ids:
        return movies
    unknown = set(ids) - {m["id"] for m in movies}
    if unknown:
        raise SystemExit(f"movies.yaml に無い id: {sorted(unknown)}")
    return [m for m in movies if m["id"] in set(ids)]


def _build_workflow(job: Job, image_names: list[str], cfg: Config, template: dict | None) -> dict:
    clip = job.clip
    prefix = f"{cfg.comfy['filename_prefix']}/{job.dest.stem}"
    if clip.mode == "i2v":
        return build_i2v_workflow(prompt=clip.prompt, duration=clip.duration,
                                  image_name=image_names[0], seed=job.seed,
                                  megapixels=clip.megapixels, turbo=clip.turbo,
                                  steps=effective_steps(clip, cfg), models=cfg.i2v,
                                  filename_prefix=prefix)
    return build_r2v_workflow(template, prompt=clip.prompt, duration=clip.duration,
                              image_names=image_names, seed=job.seed,
                              megapixels=clip.megapixels, steps=clip.steps, filename_prefix=prefix)


def _all_clips(cfg: Config, movies: list[dict]) -> list[ClipSettings]:
    return [resolve_clip(m, cfg) for m in movies]


def _update_review(cfg: Config, movies: list[dict]) -> None:
    try:
        path = build_review(cfg, _all_clips(cfg, movies))
        print(f"レビューページを更新しました: {path}")
    except Exception as e:
        print(f"レビューページの更新に失敗しました: {e}", file=sys.stderr)


# ---------------------------------------------------------------------------
# generate
# ---------------------------------------------------------------------------

def cmd_generate(args, cfg: Config, movies: list[dict]) -> int:
    targets = _select_movies(movies, args.ids)
    clips = [resolve_clip(m, cfg, _cli_overrides(args)) for m in targets]

    missing = sorted({str(cfg.image_dir / n) for c in clips for n in c.images
                      if not (cfg.image_dir / n).is_file()})
    if missing:
        print("画像が見つかりません:\n  " + "\n  ".join(missing), file=sys.stderr)
        return 2

    # ジョブごとに「生成する / スキップ」を決める
    run, skipped, stale_kept = [], 0, []
    for job in build_jobs(clips, cfg.out_dir):
        state, diff, params = job_state(job, cfg)
        if args.force or state == MISSING or (state == STALE and args.stale):
            run.append((job, params, state, diff))
        elif state == STALE:
            stale_kept.append((job, diff))
        else:
            skipped += 1

    regen = [(j, d) for j, _, s, d in run if s != MISSING]
    print(f"生成 {len(run)}本（うち再生成 {len(regen)}本） / 生成済みのためスキップ {skipped + len(stale_kept)}本")
    for job, diff in regen:
        print(f"  再生成: {job.dest.name}" + (f"（{'・'.join(diff)}が変更）" if diff else ""))
    if stale_kept:
        print(f"設定が変わったテイクが {len(stale_kept)}本あります（--stale で再生成）:")
        for job, diff in stale_kept:
            print(f"  {job.dest.name}: {'・'.join(diff)}が変更")

    if args.dry_run:
        return _dry_run(run, cfg)
    if not run:
        print("生成するクリップはありません")
        return 0

    client = ComfyClient(args.server or cfg.server)
    try:
        client.check()
    except ConnectionError as e:
        print(e, file=sys.stderr)
        return 2
    template = None
    if any(j.clip.mode == "r2v" for j, *_ in run):
        template = json.loads(cfg.r2v_template.read_text(encoding="utf-8"))

    cfg.out_dir.mkdir(parents=True, exist_ok=True)
    eta = Eta.from_dir(cfg.out_dir)
    print(fmt_eta(eta.remaining([(rate_key(p), j.clip.duration) for j, p, *_ in run]), len(run)))

    failures, t_start = [], time.time()
    for n, (job, params, _, _) in enumerate(run, 1):
        label = f"[{n}/{len(run)}] {job.label}"
        try:
            names = [client.upload_image(cfg.image_dir / img, cfg.comfy["upload_subfolder"])
                     for img in job.clip.images]
            wf = _build_workflow(job, names, cfg, template)
            t0 = time.time()
            prompt_id = client.queue(wf)
            print(f"{label}: 生成中 (seed={job.seed}, {job.clip.mode}, {job.clip.megapixels}MP)", flush=True)
            entry = client.wait(prompt_id, poll=cfg.comfy["poll_seconds"],
                                timeout=cfg.comfy["timeout_minutes"] * 60)
            videos = find_video_outputs(entry)
            if not videos:
                raise RuntimeError("出力に動画ファイルが見つかりません")
            client.download(videos[0], job.dest)
            elapsed = time.time() - t0
            write_meta(job, params, elapsed_seconds=round(elapsed, 1), prompt_id=prompt_id,
                       comfy_file=videos[0].get("filename"))
            eta.add(rate_key(params), elapsed, job.clip.duration)
            print(f"{label}: 完了 {job.dest.name}（{fmt_duration(elapsed)}）", flush=True)
        except Exception as e:  # 1本の失敗で全体を止めない
            print(f"{label}: 失敗 - {e}", file=sys.stderr, flush=True)
            failures.append(job.dest.name)
        rest = run[n:]
        if rest:
            print("  " + fmt_eta(eta.remaining([(rate_key(p), j.clip.duration) for j, p, *_ in rest]),
                                 len(rest)), flush=True)

    done = len(run) - len(failures)
    summary = f"成功 {done}本 / 失敗 {len(failures)}本（{fmt_duration(time.time() - t_start)}）"
    print(summary)
    if failures:
        print("失敗: " + " ".join(failures), file=sys.stderr)
    if cfg.data["review"]["auto"] and not args.no_review:
        _update_review(cfg, movies)
    if not args.no_notify:
        notifier.notify(cfg.notify, "動画生成が終わりました" if not failures else "動画生成が終わりました（失敗あり）",
                        summary)
    return 1 if failures else 0


def _dry_run(run, cfg: Config) -> int:
    template = None
    if any(j.clip.mode == "r2v" for j, *_ in run):
        template = json.loads(cfg.r2v_template.read_text(encoding="utf-8"))
    out = cfg.out_dir / "workflows"
    out.mkdir(parents=True, exist_ok=True)
    sub = cfg.comfy["upload_subfolder"]
    for job, *_ in run:
        wf = _build_workflow(job, [f"{sub}/{n}" for n in job.clip.images], cfg, template)
        path = out / f"{job.dest.stem}_{job.clip.mode}.json"
        path.write_text(json.dumps(wf, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  {path.name}（{job.clip.duration:g}秒 = {frame_length(job.clip.duration)}フレーム, "
              f"seed={job.seed}）")
    print(f"ワークフローを {out} に書き出しました（キュー投入はしていません）")
    return 0


# ---------------------------------------------------------------------------
# status / review / roughcut
# ---------------------------------------------------------------------------

_STATE_MARK = {OK: "○", STALE: "△", UNKNOWN: "?", MISSING: "-"}


def cmd_status(args, cfg: Config, movies: list[dict]) -> int:
    clips = _all_clips(cfg, _select_movies(movies, args.ids))
    selection = load_selection(cfg.selected_path)
    counts = {OK: 0, STALE: 0, UNKNOWN: 0, MISSING: 0}
    print("○=最新 △=設定変更あり ?=記録なし -=未生成  ★=採用テイク\n")
    for clip in clips:
        on_disk = list_takes(cfg.out_dir, clip.stem)
        marks, notes = [], []
        for take in sorted(set(range(1, clip.takes + 1)) | set(on_disk)):
            video = on_disk.get(take) or cfg.out_dir / "_missing_"
            try:
                state, diff = video_state(video, generation_params(clip, take_seed(clip.seed, take), cfg))
            except FileNotFoundError:
                state, diff = UNKNOWN, []
            counts[state] += 1
            star = "★" if on_disk.get(take) and selection.get(clip.id) == on_disk[take].name else ""
            marks.append(f"t{take}{_STATE_MARK[state]}{star}")
            if diff:
                notes.append(f"t{take}: {'・'.join(diff)}")
        extra = f"  [{clip.mode}" + (f", 上書き: {','.join(clip.overridden)}" if clip.overridden else "") + "]"
        print(f"{clip.id:>3} {clip.name}  {' '.join(marks)}{extra}" + (f"  変更: {'; '.join(notes)}" if notes else ""))
    print(f"\n最新 {counts[OK]} / 設定変更あり {counts[STALE]} / 記録なし {counts[UNKNOWN]} / "
          f"未生成 {counts[MISSING]} / 採用 {len(selection)}/{len(clips)}")
    return 0


def cmd_review(args, cfg: Config, movies: list[dict]) -> int:
    clips = _all_clips(cfg, movies)
    path = build_review(cfg, clips)
    print(f"レビューページを作成しました: {path}")
    if args.serve:
        serve(cfg, [c.id for c in clips], args.port or cfg.data["review"]["port"],
              open_browser=not args.no_open)
    return 0


def cmd_roughcut(args, cfg: Config, movies: list[dict]) -> int:
    clips = _all_clips(cfg, movies)
    try:
        output, cues = build_roughcut(cfg, clips, output=args.output, audio=args.audio)
    except (RuntimeError, FileNotFoundError) as e:
        print(e, file=sys.stderr)
        return 2
    print(format_cues(cues))
    print(f"\nラフ版を作成しました: {output}（{sum(c.clip.duration for c in clips):g}秒）")
    return 0


def main(argv: list[str] | None = None) -> int:
    if not sys.stdout.isatty() and not os.environ.get("PYTHONIOENCODING"):
        # パイプ出力（Git Bash 等）でも日本語が化けないよう UTF-8 にする
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except Exception:
            pass
    args = parse_args(argv)
    try:
        cfg = Config.load(args.config)
        movies = load_movies(cfg.movies_path)
    except (ValueError, FileNotFoundError) as e:
        print(f"設定エラー: {e}", file=sys.stderr)
        return 2
    handler = {"generate": cmd_generate, "status": cmd_status,
               "review": cmd_review, "roughcut": cmd_roughcut}[args.command]
    try:
        return handler(args, cfg, movies)
    except ValueError as e:
        print(f"設定エラー: {e}", file=sys.stderr)
        return 2
