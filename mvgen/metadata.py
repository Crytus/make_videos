"""生成時の設定の記録（動画と同名の .json）と、設定変更の検出。"""

from __future__ import annotations

import datetime
import functools
import hashlib
import json
from pathlib import Path

from .config import Config
from .plan import ClipSettings, Job, is_generated

# 生成状態
MISSING = "missing"   # 未生成
OK = "ok"             # 記録と現在の設定が一致
STALE = "stale"       # 記録と現在の設定が食い違う（プロンプトや画像が変わった）
UNKNOWN = "unknown"   # 動画はあるが記録が無い（このツール以前に作ったもの等）


@functools.lru_cache(maxsize=256)
def _sha256_cached(path: str, mtime: float, size: int) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def file_sha256(path: Path) -> str:
    st = path.stat()
    return _sha256_cached(str(path), st.st_mtime, st.st_size)


def effective_steps(clip: ClipSettings, cfg: Config) -> int | None:
    """実際に使われるステップ数。r2v で未指定ならテンプレートの値（None）。"""
    if clip.steps is not None:
        return int(clip.steps)
    if clip.mode == "i2v":
        return cfg.i2v["turbo_steps"] if clip.turbo else cfg.i2v["normal_steps"]
    return None


def generation_params(clip: ClipSettings, seed: int, cfg: Config) -> dict:
    """動画の見た目に影響する設定をまとめる。これが変わったら「要再生成」とみなす。"""
    params = {
        "mode": clip.mode,
        "prompt": clip.prompt,
        "duration": clip.duration,
        "seed": seed,
        "megapixels": clip.megapixels,
        "steps": effective_steps(clip, cfg),
        "images": [{"name": n, "sha256": file_sha256(cfg.image_dir / n)} for n in clip.images],
    }
    if clip.mode == "i2v":
        keys = ["unet_name", "clip_name", "video_vae", "audio_vae", "sampler", "scheduler"]
        params["turbo"] = clip.turbo
        params["models"] = {k: cfg.i2v[k] for k in keys}
        if clip.turbo:
            params["models"]["turbo_lora"] = cfg.i2v["turbo_lora"]
    else:
        params["models"] = {"template_sha256": file_sha256(cfg.r2v_template)}
    return params


def read_meta(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def write_meta(job: Job, params: dict, **extra) -> None:
    data = {
        "id": job.clip.id,
        "name": job.clip.name,
        "take": job.take,
        "file": job.dest.name,
        "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
        **extra,
        "params": params,
    }
    tmp = job.meta_path.with_name(job.meta_path.name + ".part")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(job.meta_path)


# 変更点の表示名
_KEY_LABELS = {"prompt": "プロンプト", "duration": "尺", "seed": "seed", "mode": "モード",
               "megapixels": "解像度", "steps": "ステップ数", "images": "画像",
               "turbo": "turbo", "models": "モデル"}


def changed_keys(old: dict, new: dict) -> list[str]:
    """記録された設定と現在の設定で異なる項目名を返す。"""
    keys = sorted(set(old) | set(new), key=lambda k: list(_KEY_LABELS).index(k)
                  if k in _KEY_LABELS else 99)
    return [_KEY_LABELS.get(k, k) for k in keys if old.get(k) != new.get(k)]


def video_state(video: Path, params: dict) -> tuple[str, list[str]]:
    """動画の生成状態と、STALE の場合は変わった項目を返す。"""
    if not is_generated(video):
        return MISSING, []
    meta = read_meta(video.with_suffix(".json"))
    if not meta or "params" not in meta:
        return UNKNOWN, []
    diff = changed_keys(meta["params"], params)
    return (STALE, diff) if diff else (OK, [])


def job_state(job: Job, cfg: Config) -> tuple[str, list[str], dict]:
    params = generation_params(job.clip, job.seed, cfg)
    state, diff = video_state(job.dest, params)
    return state, diff, params
