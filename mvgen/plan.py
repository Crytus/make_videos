"""クリップごとの設定の解決と、生成ジョブ（クリップ × テイク）の組み立て。

設定の優先順位: コマンドライン > config.yaml の clips.<id> > config.yaml の generation > 既定値
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from .config import Config
from .movies import default_seed, output_stem, ref_images

# テイク k の seed は take1 の seed + (k-1) * TAKE_SEED_STRIDE
TAKE_SEED_STRIDE = 1000


@dataclass
class ClipSettings:
    movie: dict
    mode: str
    images: list[str]
    prompt: str
    seed: int          # take1 の seed
    megapixels: float
    steps: int | None
    turbo: bool
    takes: int
    overridden: list[str] = field(default_factory=list)  # clips.<id> で上書きされたキー

    @property
    def id(self) -> str:
        return self.movie["id"]

    @property
    def name(self) -> str:
        return self.movie.get("name", "")

    @property
    def duration(self) -> float:
        return float(self.movie["duration"])

    @property
    def stem(self) -> str:
        return output_stem(self.movie)


@dataclass
class Job:
    clip: ClipSettings
    take: int
    seed: int
    dest: Path

    @property
    def meta_path(self) -> Path:
        return self.dest.with_suffix(".json")

    @property
    def label(self) -> str:
        return f"{self.clip.id} {self.clip.name} take{self.take}"


def resolve_clip(movie: dict, cfg: Config, cli: dict | None = None) -> ClipSettings:
    """1クリップ分の生成設定を決める。cli は値が None でないものだけ優先される。"""
    cli = {k: v for k, v in (cli or {}).items() if v is not None}
    over = cfg.clips.get(movie["id"], {})
    gen = cfg.gen

    def pick(key, over_key=None):
        if key in cli:
            return cli[key]
        if (over_key or key) in over:
            return over[over_key or key]
        return gen[key]

    mode = pick("mode")
    images = list(over.get("ref-images") or ref_images(movie))
    if not images:
        raise ValueError(f"id={movie['id']}: 参照画像がありません")
    if mode == "i2v":
        images = images[:1]  # i2v は開始フレーム1枚のみ

    if "prompt_file" in over:
        prompt = cfg.path(over["prompt_file"]).read_text(encoding="utf-8").strip()
    else:
        prompt = over.get("prompt") or movie["prompt"]

    if "seed" in cli:
        seed = cli["seed"]
    elif "seed" in over:
        seed = over["seed"]
    else:
        seed = default_seed(movie, cli.get("seed_base", gen["seed_base"]))

    takes = int(pick("takes"))
    if takes < 1:
        raise ValueError(f"id={movie['id']}: takes は 1 以上")

    return ClipSettings(movie=movie, mode=mode, images=images, prompt=prompt, seed=int(seed),
                        megapixels=float(pick("megapixels")), steps=pick("steps"),
                        turbo=bool(pick("turbo")), takes=takes, overridden=sorted(over))


def take_path(out_dir: Path, stem: str, take: int) -> Path:
    """テイクの保存先。take1 は従来どおり <stem>.mp4、2本目以降は <stem>_t2.mp4 …"""
    return out_dir / (f"{stem}.mp4" if take == 1 else f"{stem}_t{take}.mp4")


def take_seed(seed: int, take: int) -> int:
    return seed + (take - 1) * TAKE_SEED_STRIDE


def list_takes(out_dir: Path, stem: str) -> dict[int, Path]:
    """ディスク上にある生成済みテイクを {テイク番号: パス} で返す。"""
    pattern = re.compile(rf"^{re.escape(stem)}(?:_t(\d+))?\.mp4$")
    found = {}
    if out_dir.is_dir():
        for p in out_dir.iterdir():
            m = pattern.match(p.name)
            if m and is_generated(p):
                found[int(m.group(1) or 1)] = p
    return dict(sorted(found.items()))


def is_generated(dest: Path) -> bool:
    """生成済みの動画があるか（空ファイルは未生成扱い）。"""
    return dest.is_file() and dest.stat().st_size > 0


def build_jobs(clips: list[ClipSettings], out_dir: Path) -> list[Job]:
    """全ジョブを「テイク番号 → クリップ順」に並べる。
    先に全クリップの take1 が揃うので、途中で止めても一通り確認できる。"""
    jobs = []
    for take in range(1, max((c.takes for c in clips), default=0) + 1):
        for clip in clips:
            if take <= clip.takes:
                jobs.append(Job(clip, take, take_seed(clip.seed, take),
                                take_path(out_dir, clip.stem, take)))
    return jobs
