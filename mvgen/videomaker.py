"""videomaker（https://github.com/Crytus/videomaker）でクリップをつなぐためのシナリオ YAML を書き出す。

使う動画は roughcut と同じ規則（selected.yaml の採用テイク → take1 → 残りのテイク）で選ぶ。
H3 は 17k+5 フレームに切り上げて少し長く生成するため、各シーンに movies.yaml の尺を
duration として書き、videomaker 側で尺どおりに切らせる。未生成のクリップは開始画像を静止画で入れる。
"""

from __future__ import annotations

import copy
import os
import re
from pathlib import Path

import yaml

from .config import Config
from .plan import ClipSettings
from .roughcut import Cue, plan_cues

HEADER = ("# make_videos videomaker で生成（直接編集しても次回の生成で上書きされます。"
          "共通設定は config_video.yaml の videomaker 節へ）\n")

# 「（イントロ／歌唱なし）」「(間奏)」のように全体が括弧書きの歌詞は字幕にしない
_NOTE_RE = re.compile(r"^\s*[（(][^（）()]*[）)]\s*$")


def _rel(target: Path, start: Path) -> str:
    try:
        return Path(os.path.relpath(target, start)).as_posix()
    except ValueError:  # Windows でドライブが違う場合は絶対パス
        return Path(target).resolve().as_posix()


def subtitle_text(lyrics) -> str:
    """movies.yaml の lyrics を字幕の文字列にする（括弧書きの注記は空にする）。"""
    text = str(lyrics or "").strip()
    return "" if _NOTE_RE.match(text) else text


def _number(value: float):
    return int(value) if float(value).is_integer() else value


def _relocate(value, cfg: Config, out_dir: Path):
    """config_video.yaml 基準で実在するパスなら、シナリオファイル基準の相対パスに直す。
    実在しなければそのまま（videomaker の assets/ 以下の検索に任せる）。"""
    if not isinstance(value, str) or not value:
        return value
    path = cfg.path(value)
    return _rel(path, out_dir) if path.is_file() else value


def build_video_section(cfg: Config, out_dir: Path) -> dict:
    vm = cfg.data["videomaker"]
    video = copy.deepcopy(vm.get("video") or {})
    if not video.get("bgm") and cfg.roughcut_audio is not None:
        video["bgm"] = _rel(cfg.roughcut_audio, out_dir)
    elif video.get("bgm"):
        video["bgm"] = _relocate(video["bgm"], cfg, out_dir)
    if isinstance(video.get("subtitle"), dict) and video["subtitle"].get("font"):
        video["subtitle"]["font"] = _relocate(video["subtitle"]["font"], cfg, out_dir)
    return video


def build_scenes(cfg: Config, cues: list[Cue], out_dir: Path) -> list[dict]:
    mode = cfg.data["videomaker"]["subtitle"]
    scenes = []
    for cue in cues:
        clip = cue.clip
        scene: dict = {"id": clip.id}
        if cue.source is not None:
            scene["video"] = _rel(cue.source, out_dir)
        else:
            # 未生成は開始画像の静止画で尺を埋める
            scene["image"] = _rel(cfg.image_dir / clip.images[0], out_dir)
        scene["duration"] = _number(clip.duration)
        scene["subtitle"] = subtitle_text(clip.movie.get("lyrics")) if mode == "lyrics" else ""
        scenes.append(scene)
    return scenes


class _Dumper(yaml.SafeDumper):
    def increase_indent(self, flow=False, indentless=False):
        # scenes: の下のリストも字下げする（videomaker のサンプルと同じ書式）
        return super().increase_indent(flow, False)


def _str_representer(dumper, data: str):
    # 複数行の字幕は | のブロック形式で書く
    style = "|" if "\n" in data else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=style)


_Dumper.add_representer(str, _str_representer)


def render_scenario(cfg: Config, clips: list[ClipSettings], output: Path) -> tuple[str, list[Cue]]:
    out_dir = output.resolve().parent
    cues = plan_cues(cfg, clips)
    data = {"video": build_video_section(cfg, out_dir),
            "scenes": build_scenes(cfg, cues, out_dir)}
    options = cfg.data["videomaker"].get("options") or {}
    if options:
        data["options"] = copy.deepcopy(options)
    text = yaml.dump(data, Dumper=_Dumper, allow_unicode=True, sort_keys=False,
                     default_flow_style=False, width=1000)
    return HEADER + text, cues


def build_videomaker(cfg: Config, clips: list[ClipSettings], output: Path | None = None
                     ) -> tuple[Path, list[Cue]]:
    output = output or cfg.videomaker_output
    text, cues = render_scenario(cfg, clips, output)
    output.parent.mkdir(parents=True, exist_ok=True)
    tmp = output.with_name(output.name + ".part")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(output)
    return output, cues
