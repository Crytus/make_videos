"""ffmpeg / ffprobe の呼び出し。"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


def ffmpeg_available() -> bool:
    return shutil.which("ffmpeg") is not None and shutil.which("ffprobe") is not None


def probe(path: Path) -> dict:
    """動画の長さ・解像度・音声の有無を返す。"""
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "format=duration:stream=codec_type,width,height", "-of", "json", str(path)],
        capture_output=True, text=True, check=True).stdout
    data = json.loads(out)
    video = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), {})
    return {
        "duration": float(data.get("format", {}).get("duration", 0) or 0),
        "width": video.get("width"),
        "height": video.get("height"),
        "has_audio": any(s.get("codec_type") == "audio" for s in data.get("streams", [])),
    }


def run_ffmpeg(args: list[str]) -> None:
    res = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *args],
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    if res.returncode != 0:
        raise RuntimeError(f"ffmpeg が失敗しました: {res.stderr.strip()[-2000:]}")


def extract_frame(video: Path, dest: Path, *, at: float | None = None,
                  from_end: bool = False, width: int = 320) -> None:
    """動画から1コマを JPEG で書き出す。from_end=True なら最後のコマ。"""
    dest.parent.mkdir(parents=True, exist_ok=True)
    seek = ["-sseof", "-0.1"] if from_end else ["-ss", f"{at or 0:.3f}"]
    run_ffmpeg([*seek, "-i", str(video), "-frames:v", "1", "-vf", f"scale={width}:-2",
                "-q:v", "4", str(dest)])
