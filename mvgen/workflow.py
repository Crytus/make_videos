"""ComfyUI に投入するワークフロー（API 形式）の組み立て。"""

from __future__ import annotations

import copy

from .movies import FPS, frame_length

# minimaxh3_r2v.json 内のノード ID
R2V_NODE = {
    "save": "92",
    "resolution": "115",
    "duration": "132",
    "r2v": "136",
    "prompt": "138",
    "sampler": "161",
    "images": ["187", "188", "189"],
}


def build_i2v_workflow(*, prompt: str, duration: float, image_name: str, seed: int,
                       megapixels: float, turbo: bool, steps: int, models: dict,
                       filename_prefix: str) -> dict:
    """公式テンプレート video_minimax_h3_i2v と同等のグラフを組み立てる。"""
    model_ref = ["2", 0] if turbo else ["1", 0]
    wf: dict = {
        "1": {"class_type": "UNETLoader",
              "inputs": {"unet_name": models["unet_name"], "weight_dtype": "default"}},
        "3": {"class_type": "CLIPLoader",
              "inputs": {"clip_name": models["clip_name"], "type": "minimax", "device": "default"}},
        "4": {"class_type": "VAELoader", "inputs": {"vae_name": models["video_vae"]}},
        "5": {"class_type": "VAELoader", "inputs": {"vae_name": models["audio_vae"]}},
        "6": {"class_type": "LoadImage", "inputs": {"image": image_name}},
        "7": {"class_type": "ResolutionSelector",
              "inputs": {"aspect_ratio": "16:9 (Widescreen)", "megapixels": megapixels,
                         "multiple": 32}},
        "8": {"class_type": "MiniMaxH3ImageToVideo",
              "inputs": {"clip": ["3", 0], "vae": ["4", 0], "prompt": prompt,
                         "width": ["7", 0], "height": ["7", 1],
                         "length": frame_length(duration), "first_frame": ["6", 0]}},
        "9": {"class_type": "RandomNoise", "inputs": {"noise_seed": seed}},
        "10": {"class_type": "KSamplerSelect", "inputs": {"sampler_name": models["sampler"]}},
        "11": {"class_type": "BasicScheduler",
               "inputs": {"model": model_ref, "scheduler": models["scheduler"],
                          "steps": steps, "denoise": 1.0}},
        "12": {"class_type": "BasicGuider",
               "inputs": {"model": model_ref, "conditioning": ["8", 0]}},
        "13": {"class_type": "SamplerCustomAdvanced",
               "inputs": {"noise": ["9", 0], "guider": ["12", 0], "sampler": ["10", 0],
                          "sigmas": ["11", 0], "latent_image": ["8", 1]}},
        "14": {"class_type": "VAEDecode", "inputs": {"samples": ["13", 0], "vae": ["4", 0]}},
        "15": {"class_type": "VAEDecodeAudio", "inputs": {"samples": ["13", 0], "vae": ["5", 0]}},
        "16": {"class_type": "CreateVideo",
               "inputs": {"images": ["14", 0], "audio": ["15", 0], "fps": FPS}},
        "17": {"class_type": "SaveVideo",
               "inputs": {"video": ["16", 0], "filename_prefix": filename_prefix,
                          "format": "auto", "codec": "auto"}},
    }
    if turbo:
        wf["2"] = {"class_type": "LoraLoaderModelOnly",
                   "inputs": {"model": ["1", 0], "lora_name": models["turbo_lora"],
                              "strength_model": 1.0}}
    return wf


def build_r2v_workflow(template: dict, *, prompt: str, duration: float, image_names: list[str],
                       seed: int, megapixels: float, steps: int | None,
                       filename_prefix: str) -> dict:
    """minimaxh3_r2v.json を書き換えて R2V のワークフローを作る。"""
    wf = copy.deepcopy(template)
    n = R2V_NODE
    missing = [nid for nid in (n["save"], n["resolution"], n["duration"], n["r2v"],
                               n["prompt"], n["sampler"]) if nid not in wf]
    if missing:
        raise ValueError(f"r2v テンプレートにノード {missing} がありません（R2V_NODE を更新してください）")
    if not 1 <= len(image_names) <= len(n["images"]):
        raise ValueError(f"r2v の参照画像は 1〜{len(n['images'])} 枚です（{len(image_names)} 枚）")

    wf[n["prompt"]]["inputs"]["value"] = prompt
    wf[n["duration"]]["inputs"]["value"] = float(duration)
    wf[n["sampler"]]["inputs"]["seed"] = seed
    if steps is not None:
        wf[n["sampler"]]["inputs"]["steps"] = steps
    wf[n["resolution"]]["inputs"]["megapixels"] = megapixels
    wf[n["save"]]["inputs"]["filename_prefix"] = filename_prefix

    # 参照画像: 使う分だけ LoadImage を残し、余りはノードごと削除する
    r2v_inputs = wf[n["r2v"]]["inputs"]
    for i, node_id in enumerate(n["images"]):
        key = f"ref_images.ref_image_{i}"
        if i < len(image_names):
            wf[node_id]["inputs"]["image"] = image_names[i]
            r2v_inputs[key] = [node_id, 0]
        else:
            wf.pop(node_id, None)
            r2v_inputs.pop(key, None)
    return wf
