"""movies.yaml の読み込みとクリップ単位の基本計算。"""

from __future__ import annotations

from pathlib import Path

import yaml

FPS = 24


def load_movies(path: Path) -> list[dict]:
    """movies.yaml を読み込み、必須キーを検証して返す。"""
    with open(path, encoding="utf-8") as f:
        movies = yaml.safe_load(f)
    if not isinstance(movies, list):
        raise ValueError(f"{path}: トップレベルがリストではありません")
    for m in movies:
        for key in ("id", "duration", "ref-image1", "prompt"):
            if key not in m or m[key] in (None, ""):
                raise ValueError(f"{path}: id={m.get('id')} に {key} がありません")
        m["id"] = str(m["id"])
    return movies


def ref_images(movie: dict) -> list[str]:
    """空でない ref-image1..3 を順に返す。"""
    return [movie[k] for k in ("ref-image1", "ref-image2", "ref-image3") if movie.get(k)]


def frame_length(seconds: float) -> int:
    """秒数を H3 のフレーム数（24fps・17k+5 の格子に切り上げ）に変換する。
    ワークフロー内の ComfyMathExpression と同じ式。"""
    n = max(5, round(seconds * FPS))
    return n + (5 - n % 17) % 17


def output_stem(movie: dict) -> str:
    """出力ファイル名の幹。開始画像名に合わせる（例: hope_01_path_before_dawn）。"""
    return Path(movie["ref-image1"]).stem


def default_seed(movie: dict, base: int) -> int:
    """クリップごとに再現可能な seed を決める（id の数字部分 + base）。"""
    digits = "".join(c for c in movie["id"] if c.isdigit())
    offset = int(digits) if digits else 0
    if not movie["id"][:1].isdigit():
        offset += 100  # E-1 などは 01 と重ならないようにずらす
    return base + offset
