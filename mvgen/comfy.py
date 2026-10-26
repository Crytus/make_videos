"""ComfyUI の HTTP API クライアント。"""

from __future__ import annotations

import json
import mimetypes
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

VIDEO_SUFFIXES = (".mp4", ".webm", ".mov", ".mkv")


class ComfyClient:
    def __init__(self, server: str):
        self.base = server.rstrip("/")
        self.client_id = str(uuid.uuid4())

    def _request(self, path: str, data: bytes | None = None,
                 headers: dict | None = None) -> bytes:
        req = urllib.request.Request(self.base + path, data=data, headers=headers or {})
        with urllib.request.urlopen(req, timeout=60) as res:
            return res.read()

    def get_json(self, path: str):
        return json.loads(self._request(path))

    def check(self) -> None:
        """サーバーに接続できるか確認する。"""
        try:
            self.get_json("/system_stats")
        except (urllib.error.URLError, OSError) as e:
            raise ConnectionError(f"ComfyUI ({self.base}) に接続できません: {e}") from e

    def upload_image(self, path: Path, subfolder: str) -> str:
        """画像を ComfyUI の input にアップロードし、LoadImage に渡す名前を返す。"""
        boundary = uuid.uuid4().hex
        ctype = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        parts = []
        for name, value in (("overwrite", "true"), ("type", "input"), ("subfolder", subfolder)):
            parts.append(f"--{boundary}\r\nContent-Disposition: form-data; "
                         f"name=\"{name}\"\r\n\r\n{value}\r\n".encode())
        parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"image\"; "
                     f"filename=\"{path.name}\"\r\nContent-Type: {ctype}\r\n\r\n".encode())
        parts.append(path.read_bytes())
        parts.append(f"\r\n--{boundary}--\r\n".encode())
        res = json.loads(self._request(
            "/upload/image", b"".join(parts),
            {"Content-Type": f"multipart/form-data; boundary={boundary}"}))
        return f"{res['subfolder']}/{res['name']}" if res.get("subfolder") else res["name"]

    def queue(self, workflow: dict) -> str:
        body = json.dumps({"prompt": workflow, "client_id": self.client_id}).encode()
        try:
            res = json.loads(self._request("/prompt", body, {"Content-Type": "application/json"}))
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")
            raise RuntimeError(f"キュー投入に失敗しました ({e.code}): {detail}") from e
        return res["prompt_id"]

    def wait(self, prompt_id: str, poll: float = 5.0, timeout: float = 3 * 3600) -> dict:
        """実行完了まで待ち、history のエントリを返す。"""
        start = time.time()
        while time.time() - start < timeout:
            hist = self.get_json(f"/history/{prompt_id}")
            if prompt_id in hist:
                entry = hist[prompt_id]
                status = entry.get("status", {})
                if status.get("status_str") == "error":
                    msgs = [m for m in status.get("messages", []) if m[0] == "execution_error"]
                    raise RuntimeError(f"実行エラー: {json.dumps(msgs, ensure_ascii=False)[:2000]}")
                if status.get("completed", True):
                    return entry
            time.sleep(poll)
        raise TimeoutError(f"{prompt_id} がタイムアウトしました")

    def download(self, file_info: dict, dest: Path) -> None:
        query = urllib.parse.urlencode({k: file_info.get(k, "") for k in ("filename", "subfolder", "type")})
        dest.parent.mkdir(parents=True, exist_ok=True)
        # 途中で止まっても壊れたファイルが「生成済み」と誤認されないよう、一時ファイル経由で保存する
        tmp = dest.with_name(dest.name + ".part")
        req = urllib.request.Request(f"{self.base}/view?{query}")
        with urllib.request.urlopen(req, timeout=600) as res, open(tmp, "wb") as f:
            while chunk := res.read(1 << 20):
                f.write(chunk)
        tmp.replace(dest)


def find_video_outputs(entry: dict) -> list[dict]:
    """history のエントリから保存された動画ファイル情報を取り出す。"""
    videos = []
    for node_out in entry.get("outputs", {}).values():
        for key in ("videos", "gifs", "images"):
            for item in node_out.get(key, []) or []:
                if isinstance(item, dict) and item.get("type") == "output" and \
                        Path(item.get("filename", "")).suffix.lower() in VIDEO_SUFFIXES:
                    videos.append(item)
    return videos
