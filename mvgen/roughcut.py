"""全クリップを movies.yaml の尺どおりに切りそろえてつないだラフ版を作る。"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

from . import media
from .config import Config
from .movies import FPS
from .plan import ClipSettings, list_takes
from .selection import load_selection


@dataclass
class Cue:
    clip: ClipSettings
    start: float
    source: Path | None   # None は未生成（黒画面で埋める）
    note: str


def plan_cues(cfg: Config, clips: list[ClipSettings]) -> list[Cue]:
    """各クリップに使う動画を決める。selected.yaml の選択 → take1 → 最小番号のテイクの順。"""
    selection = load_selection(cfg.selected_path)
    cues, t = [], 0.0
    for clip in clips:
        takes = list_takes(cfg.out_dir, clip.stem)
        chosen = selection.get(clip.id)
        if chosen and (cfg.out_dir / chosen).is_file():
            src, note = cfg.out_dir / chosen, "採用"
        else:
            if chosen:
                print(f"警告: {clip.id} の採用テイク {chosen} が見つかりません", file=sys.stderr)
            src = takes.get(1) or next(iter(takes.values()), None)
            note = "未選択" if src else "未生成（黒）"
        cues.append(Cue(clip, t, src, note))
        t += clip.duration
    return cues


def _timecode(sec: float) -> str:
    return f"{int(sec // 60)}:{sec % 60:05.2f}"


def build_filter(cues: list[Cue], infos: dict[Path, dict], width: int, height: int,
                 with_audio: bool = True) -> tuple[str, list[Path]]:
    """ffmpeg の filter_complex と入力ファイルの並びを作る。
    with_audio=False（歌の音源を別に重ねる場合）はクリップの音声をつながない。"""
    inputs: list[Path] = []
    chains, pairs = [], []
    for i, cue in enumerate(cues):
        d = cue.clip.duration
        v, a = f"v{i}", f"a{i}"
        if cue.source is None:
            chains.append(f"color=c=black:s={width}x{height}:r={FPS}:d={d},format=yuv420p,setsar=1[{v}]")
            if with_audio:
                chains.append(f"anullsrc=r=48000:cl=stereo,atrim=duration={d}[{a}]")
        else:
            idx = len(inputs)
            inputs.append(cue.source)
            # 足りない場合は最後のコマで延長し、尺ちょうどで切る
            chains.append(
                f"[{idx}:v]fps={FPS},scale={width}:{height}:force_original_aspect_ratio=decrease,"
                f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1,"
                f"tpad=stop_mode=clone:stop_duration={d},trim=duration={d},setpts=PTS-STARTPTS,"
                f"format=yuv420p[{v}]")
            if with_audio and infos[cue.source]["has_audio"]:
                chains.append(f"[{idx}:a]aresample=48000,aformat=channel_layouts=stereo,apad,"
                              f"atrim=duration={d},asetpts=PTS-STARTPTS[{a}]")
            elif with_audio:
                chains.append(f"anullsrc=r=48000:cl=stereo,atrim=duration={d}[{a}]")
        pairs.append(f"[{v}][{a}]" if with_audio else f"[{v}]")
    if with_audio:
        chains.append(f"{''.join(pairs)}concat=n={len(cues)}:v=1:a=1[vout][aout]")
    else:
        chains.append(f"{''.join(pairs)}concat=n={len(cues)}:v=1:a=0[vout]")
    return ";".join(chains), inputs


def build_roughcut(cfg: Config, clips: list[ClipSettings], output: Path | None = None,
                   audio: Path | None = None) -> tuple[Path, list[Cue]]:
    if not media.ffmpeg_available():
        raise RuntimeError("ffmpeg / ffprobe が見つかりません（PATH を確認してください）")
    output = output or cfg.roughcut_output
    audio = audio or cfg.roughcut_audio
    if audio is not None and not audio.is_file():
        raise FileNotFoundError(f"音源が見つかりません: {audio}")

    cues = plan_cues(cfg, clips)
    sources = [c.source for c in cues if c.source]
    if not sources:
        raise RuntimeError("生成済みのクリップが1本もありません")
    infos = {p: media.probe(p) for p in set(sources)}
    first = infos[sources[0]]
    width, height = first["width"], first["height"]

    graph, inputs = build_filter(cues, infos, width, height, with_audio=audio is None)
    total = sum(c.clip.duration for c in cues)
    args = []
    for p in inputs:
        args += ["-i", str(p)]
    if audio is not None:
        args += ["-i", str(audio)]
    args += ["-filter_complex", graph, "-map", "[vout]"]
    args += ["-map", f"{len(inputs)}:a"] if audio is not None else ["-map", "[aout]"]
    args += ["-t", f"{total}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
             "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart"]

    output.parent.mkdir(parents=True, exist_ok=True)
    tmp = output.with_name(output.stem + ".part" + output.suffix)
    media.run_ffmpeg([*args, str(tmp)])
    tmp.replace(output)
    return output, cues


def format_cues(cues: list[Cue]) -> str:
    lines = []
    for c in cues:
        src = c.source.name if c.source else "-"
        lines.append(f"{_timecode(c.start):>8}  {c.clip.id:>3} {c.clip.name}  {src}（{c.note}）")
    return "\n".join(lines)
