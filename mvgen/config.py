"""設定ファイル（config.yaml）の読み込み。

パスの基準:
  movies / image_dir / out_dir / r2v.template / roughcut.audio / clips.*.prompt_file
      → config.yaml のあるディレクトリ基準
  review.file / review.selected / roughcut.output
      → out_dir 基準
"""

from __future__ import annotations

import copy
import sys
from pathlib import Path

import yaml

# パッケージに同梱したテンプレート
TEMPLATE_DIR = Path(__file__).resolve().parent / "templates"
BUNDLED_R2V_TEMPLATE = TEMPLATE_DIR / "minimaxh3_r2v.json"
CONFIG_TEMPLATE = TEMPLATE_DIR / "config.yaml"

DEFAULTS: dict = {
    "server": "http://127.0.0.1:8188",
    "movies": "movies.yaml",
    "image_dir": "images",
    "out_dir": "videos",
    "comfy": {
        "upload_subfolder": "make_videos",       # 画像のアップロード先（ComfyUI の input/ 配下）
        "filename_prefix": "video/make_videos",  # ComfyUI 側の保存先（output/ 配下）
        "timeout_minutes": 180,
        "poll_seconds": 5,
    },
    "generation": {
        "mode": "i2v",
        "megapixels": 0.2,
        "steps": None,       # None ならモードの既定（i2v: turbo 8 / 通常 20、r2v: テンプレートの値）
        "turbo": True,       # i2v のみ
        "seed_base": 1000,
        "takes": 1,
    },
    "i2v": {
        "unet_name": "minimax_h3_fl2va_pruned_int8_convrot.safetensors",
        "clip_name": "qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors",
        "video_vae": "minimax_h3_video_vae_int8_convrot.safetensors",
        "audio_vae": "minimax_h3_audio_vae_fp32.safetensors",
        "turbo_lora": "minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors",
        "turbo_steps": 8,
        "normal_steps": 20,
        "sampler": "res_multistep",
        "scheduler": "simple",
    },
    "r2v": {
        "template": None,         # None なら同梱のテンプレート（mvgen/templates）
    },
    "review": {
        "auto": "each",           # review.html の自動更新: each=1本ごと / end=最後に1回 / off=しない
        "file": "review.html",
        "selected": "selected.yaml",
        "port": 8765,
    },
    "roughcut": {
        "output": "roughcut.mp4",
        "audio": None,            # 楽曲の音源。None なら生成された音声をつなぐ
    },
    "notify": {
        "toast": True,            # Windows のトースト通知
        "webhook": None,          # Discord / Slack 互換の Webhook URL
    },
    "clips": {},
}

# clips.<id> に書けるキー
CLIP_KEYS = {"mode", "ref-images", "prompt", "prompt_file", "seed", "steps",
             "megapixels", "turbo", "takes"}
MODES = ("i2v", "r2v")
REVIEW_AUTO = ("each", "end", "off")


def deep_merge(base: dict, override: dict) -> dict:
    """辞書を再帰的にマージした新しい辞書を返す。"""
    result = copy.deepcopy(base)
    for key, value in (override or {}).items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def normalize_clip_id(key) -> str:
    """YAML でクォートし忘れた id（01 → 1）を "01" に戻す。"""
    if isinstance(key, int):
        return f"{key:02d}"
    return str(key)


class Config:
    def __init__(self, data: dict, base_dir: Path):
        self.data = data
        self.base_dir = base_dir
        self.clips = {normalize_clip_id(k): (v or {}) for k, v in (data.get("clips") or {}).items()}
        self._validate()

    @classmethod
    def load(cls, path: Path | None) -> "Config":
        """config.yaml を読み込む。ファイルが無ければ既定値で動く。"""
        if path is not None and path.is_file():
            with open(path, encoding="utf-8") as f:
                user = yaml.safe_load(f) or {}
            unknown = set(user) - set(DEFAULTS)
            if unknown:
                print(f"警告: {path.name} の不明なキーを無視します: {sorted(unknown)}", file=sys.stderr)
            return cls(deep_merge(DEFAULTS, user), path.resolve().parent)
        base = path.resolve().parent if path is not None else Path.cwd()
        return cls(copy.deepcopy(DEFAULTS), base)

    def _validate(self):
        # 旧形式（true / false）も受け付ける
        auto = self.data["review"]["auto"]
        if auto is True:
            self.data["review"]["auto"] = "each"
        elif auto is False or auto is None:
            self.data["review"]["auto"] = "off"
        if self.data["review"]["auto"] not in REVIEW_AUTO:
            raise ValueError(f"review.auto は {REVIEW_AUTO} のいずれか: {auto}")
        if self.gen["mode"] not in MODES:
            raise ValueError(f"generation.mode は {MODES} のいずれか: {self.gen['mode']}")
        for cid, over in self.clips.items():
            unknown = set(over) - CLIP_KEYS
            if unknown:
                raise ValueError(f"clips.{cid} の不明なキー: {sorted(unknown)}（使えるキー: {sorted(CLIP_KEYS)}）")
            if "mode" in over and over["mode"] not in MODES:
                raise ValueError(f"clips.{cid}.mode は {MODES} のいずれか")
            if "prompt" in over and "prompt_file" in over:
                raise ValueError(f"clips.{cid}: prompt と prompt_file は同時に指定できません")

    def path(self, value, base: Path | None = None) -> Path | None:
        if value in (None, ""):
            return None
        p = Path(value)
        return p if p.is_absolute() else (base or self.base_dir) / p

    # --- よく使う値 ---
    @property
    def server(self) -> str:
        return self.data["server"]

    @property
    def gen(self) -> dict:
        return self.data["generation"]

    @property
    def comfy(self) -> dict:
        return self.data["comfy"]

    @property
    def i2v(self) -> dict:
        return self.data["i2v"]

    @property
    def review_auto(self) -> str:
        return self.data["review"]["auto"]

    @property
    def notify(self) -> dict:
        return self.data["notify"]

    @property
    def movies_path(self) -> Path:
        return self.path(self.data["movies"])

    @property
    def image_dir(self) -> Path:
        return self.path(self.data["image_dir"])

    @property
    def out_dir(self) -> Path:
        return self.path(self.data["out_dir"])

    @property
    def r2v_template(self) -> Path:
        return self.path(self.data["r2v"]["template"]) or BUNDLED_R2V_TEMPLATE

    @property
    def review_path(self) -> Path:
        return self.path(self.data["review"]["file"], self.out_dir)

    @property
    def selected_path(self) -> Path:
        return self.path(self.data["review"]["selected"], self.out_dir)

    @property
    def frames_dir(self) -> Path:
        return self.out_dir / "review_frames"

    @property
    def roughcut_output(self) -> Path:
        return self.path(self.data["roughcut"]["output"], self.out_dir)

    @property
    def roughcut_audio(self) -> Path | None:
        return self.path(self.data["roughcut"]["audio"])
