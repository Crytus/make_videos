"""採用テイクの一覧（selected.yaml）の読み書き。

形式: {クリップ id: 動画ファイル名}
  "01": hope_01_path_before_dawn.mp4
  "04": hope_04_light_in_hands_t2.mp4
"""

from __future__ import annotations

from pathlib import Path

import yaml

from .config import normalize_clip_id

HEADER = "# 採用テイク（make_videos.py review で選択）。id: 動画ファイル名\n"


def load_selection(path: Path) -> dict[str, str]:
    if not path.is_file():
        return {}
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return {normalize_clip_id(k): str(v) for k, v in data.items() if v}


def save_selection(path: Path, selection: dict[str, str], order: list[str]) -> None:
    """movies.yaml の並び順で書き出す。"""
    lines = [HEADER]
    for cid in order:
        if selection.get(cid):
            lines.append(f"\"{cid}\": {selection[cid]}\n")
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".part")
    tmp.write_text("".join(lines), encoding="utf-8")
    tmp.replace(path)
