"""確認用の一覧ページ（review.html）の生成と、選択を保存するローカルサーバー。"""

from __future__ import annotations

import datetime
import html
import json
import os
import sys
import threading
import webbrowser
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from . import media
from .config import Config
from .metadata import MISSING, OK, STALE, UNKNOWN, generation_params, read_meta, video_state
from .plan import ClipSettings, list_takes, take_seed
from .selection import load_selection, save_selection


def _rel(target: Path, start: Path) -> str:
    return Path(os.path.relpath(target, start)).as_posix()


def _frames(video: Path, cfg: Config) -> list[Path]:
    """最初・中間・最後のコマを書き出す（動画より新しいキャッシュがあれば再利用）。"""
    if not media.ffmpeg_available():
        return []
    outs = [cfg.frames_dir / f"{video.stem}_{tag}.jpg" for tag in ("first", "mid", "last")]
    mtime = video.stat().st_mtime
    if all(p.is_file() and p.stat().st_mtime >= mtime for p in outs):
        return outs
    try:
        duration = media.probe(video)["duration"]
        media.extract_frame(video, outs[0], at=0)
        media.extract_frame(video, outs[1], at=duration / 2)
        media.extract_frame(video, outs[2], from_end=True)
    except Exception as e:
        print(f"コマの書き出しに失敗しました ({video.name}): {e}", file=sys.stderr)
        return []
    return outs


def _take_info(clip: ClipSettings, take: int, video: Path, cfg: Config) -> dict:
    meta = read_meta(video.with_suffix(".json")) or {}
    try:
        state, diff = video_state(video, generation_params(clip, take_seed(clip.seed, take), cfg))
    except FileNotFoundError:
        state, diff = UNKNOWN, []
    return {
        "take": take,
        "file": video.name,
        "video": _rel(video, cfg.out_dir),
        "frames": [_rel(p, cfg.out_dir) for p in _frames(video, cfg)],
        "state": state,
        "diff": diff,
        "seed": meta.get("params", {}).get("seed"),
        "mode": meta.get("params", {}).get("mode"),
        "megapixels": meta.get("params", {}).get("megapixels"),
        "elapsed": meta.get("elapsed_seconds"),
    }


_STATE_BADGE = {
    OK: ("ok", "最新"),
    STALE: ("stale", "設定変更あり"),
    UNKNOWN: ("unknown", "記録なし"),
    MISSING: ("unknown", "未生成"),
}

_CSS = """
body{font-family:"Segoe UI","Yu Gothic UI",sans-serif;margin:0;background:#f4f4f2;color:#222}
header{position:sticky;top:0;z-index:2;background:#1b2a4a;color:#fff;padding:10px 20px;display:flex;gap:16px;align-items:center;flex-wrap:wrap}
header h1{font-size:18px;margin:0}
header button{font-size:14px;padding:6px 14px;border:0;border-radius:4px;background:#e8b96a;color:#1b2a4a;font-weight:bold;cursor:pointer}
#updated{display:none;background:#3a8a5c;color:#fff;padding:4px 10px;border-radius:4px;font-size:13px}
#updated button{background:#fff;color:#3a8a5c;padding:2px 10px;margin-left:6px}
header label{font-size:13px}
#msg{font-size:13px}
main{padding:12px 20px}
section.clip{background:#fff;border-radius:6px;margin:0 0 14px;padding:12px 14px;box-shadow:0 1px 2px #0002}
section.clip.done{border-left:6px solid #3a8a5c}
section.clip:not(.done){border-left:6px solid #ccc}
.head{display:flex;gap:12px;align-items:baseline;flex-wrap:wrap}
.head h2{font-size:16px;margin:0}
.meta{color:#666;font-size:13px}
.lyrics{font-size:14px;color:#1b2a4a}
.row{display:flex;gap:12px;margin-top:8px;align-items:flex-start;overflow-x:auto}
.start{flex:0 0 200px;font-size:12px;color:#666}
.start img{width:200px;border-radius:4px;display:block}
.take{flex:0 0 340px;border:2px solid #ddd;border-radius:6px;padding:6px}
.take.selected{border-color:#e8b96a;background:#fffaf0}
.take video{width:100%;border-radius:4px;background:#000}
.frames{display:flex;gap:2px;margin-top:4px}
.frames img{width:33%;border-radius:2px}
.take .info{font-size:12px;color:#555;margin-top:4px;display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.badge{font-size:11px;padding:1px 6px;border-radius:8px;color:#fff}
.badge.ok{background:#3a8a5c}.badge.stale{background:#c0603a}.badge.unknown{background:#888}
.none{font-size:13px;color:#888;padding:8px}
details{font-size:12px;color:#444;margin-top:6px}
details pre{white-space:pre-wrap;background:#f6f6f6;padding:8px;border-radius:4px}
body.only-open section.clip.done{display:none}
"""

_JS = """
const IDS = %(ids)s;
function selection(){
  const sel = {};
  document.querySelectorAll('input[type=radio]:checked').forEach(r => { if (r.value) sel[r.dataset.clip] = r.value; });
  return sel;
}
function toYaml(sel){
  let s = '# 採用テイク（make_videos.py review で選択）。id: 動画ファイル名\\n';
  for (const id of IDS) if (sel[id]) s += '"' + id + '": ' + sel[id] + '\\n';
  return s;
}
function refresh(){
  const sel = selection();
  document.querySelectorAll('section.clip').forEach(sec => {
    sec.classList.toggle('done', !!sel[sec.dataset.clip]);
    sec.querySelectorAll('.take').forEach(t => t.classList.toggle('selected', sel[sec.dataset.clip] === t.dataset.file));
  });
  document.getElementById('count').textContent = Object.keys(sel).length + ' / ' + IDS.length + ' 選択済み';
}
function msg(text){ document.getElementById('msg').textContent = text; }
async function save(){
  const sel = selection();
  try {
    const r = await fetch('api/selection', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(sel)});
    if (!r.ok) throw new Error(await r.text());
    msg('selected.yaml に保存しました（' + new Date().toLocaleTimeString() + '）');
  } catch (e) {
    const a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([toYaml(sel)], {type:'text/yaml'}));
    a.download = 'selected.yaml';
    a.click();
    msg('サーバー未起動のため selected.yaml をダウンロードしました。%(out_dir)s に置いてください');
  }
}
// --serve で開いている間、review.html が作り直されたら知らせる（未保存の選択を消さないよう自動では再読み込みしない）
let pageStamp = null;
async function checkUpdate(){
  try {
    const r = await fetch(location.pathname, {method:'HEAD', cache:'no-store'});
    const stamp = r.headers.get('Last-Modified');
    if (pageStamp === null) pageStamp = stamp;
    else if (stamp && stamp !== pageStamp) document.getElementById('updated').style.display = 'inline-block';
  } catch (e) { /* ファイルを直接開いている場合は何もしない */ }
}
if (location.protocol.startsWith('http')) { checkUpdate(); setInterval(checkUpdate, 15000); }
document.addEventListener('change', e => { if (e.target.type === 'radio') refresh(); });
document.getElementById('onlyOpen').addEventListener('change', e => document.body.classList.toggle('only-open', e.target.checked));
refresh();
"""


def render_review(cfg: Config, clips: list[ClipSettings]) -> str:
    selection = load_selection(cfg.selected_path)
    esc = html.escape
    sections = []
    total = sum(c.duration for c in clips)
    for clip in clips:
        takes = [_take_info(clip, t, p, cfg) for t, p in list_takes(cfg.out_dir, clip.stem).items()]
        chosen = selection.get(clip.id, "")
        start_img = cfg.image_dir / clip.images[0]
        cards = []
        for t in takes:
            cls, text = _STATE_BADGE[t["state"]]
            diff = f"（{'・'.join(t['diff'])}）" if t["diff"] else ""
            frames = "".join(f'<img src="{esc(f)}" loading="lazy" alt="">' for f in t["frames"])
            extra = []
            if t["seed"] is not None:
                extra.append(f"seed {t['seed']}")
            if t["mode"]:
                extra.append(f"{t['mode']} {t['megapixels']}MP")
            if t["elapsed"]:
                extra.append(f"{t['elapsed'] / 60:.1f}分")
            cards.append(f"""
      <div class="take" data-file="{esc(t['file'])}">
        <video src="{esc(t['video'])}" controls preload="metadata"></video>
        <div class="frames">{frames}</div>
        <div class="info">
          <label><input type="radio" name="clip-{esc(clip.id)}" data-clip="{esc(clip.id)}" value="{esc(t['file'])}"{' checked' if chosen == t['file'] else ''}> <b>take{t['take']}</b></label>
          <span class="badge {cls}" title="{esc(diff)}">{text}{esc(diff)}</span>
          <span>{esc(' / '.join(extra))}</span>
        </div>
      </div>""")
        if not takes:
            cards.append('<div class="none">未生成</div>')
        unselected = f'<label class="meta"><input type="radio" name="clip-{esc(clip.id)}" data-clip="{esc(clip.id)}" value=""{"" if chosen else " checked"}> 未選択</label>'
        sections.append(f"""
  <section class="clip" data-clip="{esc(clip.id)}">
    <div class="head">
      <h2>{esc(clip.id)} {esc(clip.name)}</h2>
      <span class="meta">{clip.duration:g}秒 / {clip.mode} / {len(takes)}テイク</span>
      <span class="lyrics">{esc(str(clip.movie.get('lyrics', '')))}</span>
      {unselected}
    </div>
    <div class="row">
      <div class="start"><img src="{esc(_rel(start_img, cfg.out_dir))}" loading="lazy" alt="">開始画像 {esc(clip.images[0])}</div>{''.join(cards)}
    </div>
    <details><summary>プロンプト</summary><pre>{esc(clip.prompt)}</pre></details>
  </section>""")

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    js = _JS % {"ids": json.dumps([c.id for c in clips]), "out_dir": cfg.out_dir.name + "/"}
    return f"""<!DOCTYPE html>
<html lang="ja"><head><meta charset="utf-8"><title>レビュー — {esc(cfg.movies_path.name)}</title>
<style>{_CSS}</style></head>
<body>
<header>
  <h1>クリップ確認</h1>
  <span id="count"></span>
  <span class="meta" style="color:#ccd">{len(clips)}クリップ / 計{total:g}秒 / {now} 更新</span>
  <label><input type="checkbox" id="onlyOpen"> 未選択のみ表示</label>
  <button onclick="save()">選択を保存</button>
  <span id="msg"></span>
  <span id="updated">新しいクリップがあります（未保存の選択は先に保存してください）<button onclick="location.reload()">再読み込み</button></span>
</header>
<main>{''.join(sections)}
</main>
<script>{js}</script>
</body></html>
"""


def build_review(cfg: Config, clips: list[ClipSettings]) -> Path:
    cfg.out_dir.mkdir(parents=True, exist_ok=True)
    path = cfg.review_path
    tmp = path.with_name(path.name + ".part")
    tmp.write_text(render_review(cfg, clips), encoding="utf-8")
    tmp.replace(path)
    return path


def serve_root(cfg: Config) -> Path:
    """動画と開始画像の両方を配信できる共通の親ディレクトリ。"""
    return Path(os.path.commonpath([cfg.out_dir.resolve(), cfg.image_dir.resolve()]))


def make_handler(cfg: Config, clip_ids: list[str]):
    """review.html の配信と、選択の保存（POST …/api/selection）を受け持つハンドラ。"""
    root = serve_root(cfg)

    class Handler(SimpleHTTPRequestHandler):
        def do_POST(self):
            if not self.path.split("?")[0].endswith("/api/selection"):
                self.send_error(404)
                return
            try:
                length = int(self.headers.get("Content-Length", 0))
                data = json.loads(self.rfile.read(length) or b"{}")
                if not isinstance(data, dict):
                    raise ValueError("JSON オブジェクトではありません")
                selection = {}
                for cid, name in data.items():
                    if cid not in clip_ids:
                        raise ValueError(f"不明な id: {cid}")
                    # ファイル名のみ許可（ディレクトリ指定は拒否）し、実在を確認する
                    if not isinstance(name, str) or Path(name).name != name or \
                            not (cfg.out_dir / name).is_file():
                        raise ValueError(f"動画が見つかりません: {name}")
                    selection[cid] = name
                save_selection(cfg.selected_path, selection, clip_ids)
            except (ValueError, json.JSONDecodeError) as e:
                self.send_response(400)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write(str(e).encode("utf-8"))
                return
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"ok")

        def log_message(self, fmt, *args):  # アクセスログは出さない
            pass

    return partial(Handler, directory=str(root))


def serve(cfg: Config, clip_ids: list[str], port: int, open_browser: bool = True) -> None:
    """ローカルサーバーを起動し、ブラウザから選択を selected.yaml に直接保存できるようにする。"""
    httpd = ThreadingHTTPServer(("127.0.0.1", port), make_handler(cfg, clip_ids))
    rel = _rel(cfg.review_path.resolve(), serve_root(cfg))
    url = f"http://127.0.0.1:{httpd.server_address[1]}/{rel}"
    print(f"レビューページ: {url}\n（Ctrl+C で終了）")
    if open_browser:
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
