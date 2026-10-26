"""テスト用の一時プロジェクトを作る。"""

import json
import shutil
import subprocess
from pathlib import Path

import yaml

from mvgen.config import Config
from mvgen.movies import load_movies

REPO = Path(__file__).resolve().parent.parent
HAS_FFMPEG = shutil.which("ffmpeg") is not None and shutil.which("ffprobe") is not None

MOVIES = [
    {"id": "01", "name": "一", "duration": 2, "ref-image1": "s_01_a.png", "ref-image2": "",
     "ref-image3": "", "prompt": "prompt one", "lyrics": "歌詞一"},
    {"id": "02", "name": "二", "duration": 3, "ref-image1": "s_02_b.png", "ref-image2": "",
     "ref-image3": "", "prompt": "prompt two", "lyrics": "歌詞二"},
    {"id": "E-1", "name": "終", "duration": 2, "ref-image1": "s_E1_c.png", "ref-image2": "",
     "ref-image3": "", "prompt": "prompt end", "lyrics": ""},
]


def make_project(root: Path, config: dict | None = None, movies=None):
    """config.yaml・movies.yaml・画像・r2v テンプレートを持つ一時プロジェクトを作る。"""
    movies = movies or MOVIES
    (root / "output").mkdir()
    for m in movies:
        for k in ("ref-image1", "ref-image2", "ref-image3"):
            if m.get(k):
                (root / "output" / m[k]).write_bytes(b"PNG-" + m[k].encode())
    (root / "movies.yaml").write_text(yaml.safe_dump(movies, allow_unicode=True), encoding="utf-8")
    cfg_data = {"image_dir": "output", "notify": {"toast": False}, **(config or {})}
    (root / "config.yaml").write_text(yaml.safe_dump(cfg_data, allow_unicode=True), encoding="utf-8")
    cfg = Config.load(root / "config.yaml")
    return cfg, load_movies(cfg.movies_path)


def make_video(path: Path, seconds: float = 2.0, audio: bool = True, size="160x90"):
    """ffmpeg のテストパターンで小さな動画を作る。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    args = ["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i",
            f"testsrc=size={size}:rate=24:duration={seconds}"]
    if audio:
        args += ["-f", "lavfi", "-i", f"sine=frequency=440:duration={seconds}"]
    args += ["-c:v", "libx264", "-pix_fmt", "yuv420p"]
    if audio:
        args += ["-c:a", "aac", "-shortest"]
    subprocess.run([*args, str(path)], check=True)


def write_fake_meta(cfg, clip, take, video: Path, **extra):
    """動画に対応する生成記録を、現在の設定どおりに書く。"""
    from mvgen.metadata import generation_params, write_meta
    from mvgen.plan import Job, take_seed
    job = Job(clip, take, take_seed(clip.seed, take), video)
    write_meta(job, generation_params(clip, job.seed, cfg), **extra)
    return json.loads(video.with_suffix(".json").read_text(encoding="utf-8"))
