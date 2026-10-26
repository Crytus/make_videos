"""残り時間の見積もり。

過去の生成記録（.json の elapsed_seconds）と今回の実績から、
「動画1秒あたりの生成時間」を設定（モード・解像度・ステップ数）ごとに求めて使う。
"""

from __future__ import annotations

import datetime
from pathlib import Path

from .metadata import read_meta

Key = tuple  # (mode, megapixels, steps)


def rate_key(params: dict) -> Key:
    return (params.get("mode"), params.get("megapixels"), params.get("steps"))


class Eta:
    def __init__(self, history: dict[Key, list[float]] | None = None):
        # key → [生成時間の合計, 動画秒数の合計]
        self.history = history or {}
        self.run: dict[Key, list[float]] = {}

    @classmethod
    def from_dir(cls, out_dir: Path) -> "Eta":
        history: dict[Key, list[float]] = {}
        if out_dir.is_dir():
            for p in out_dir.glob("*.json"):
                meta = read_meta(p)
                if not meta or not meta.get("elapsed_seconds") or "params" not in meta:
                    continue
                acc = history.setdefault(rate_key(meta["params"]), [0.0, 0.0])
                acc[0] += meta["elapsed_seconds"]
                acc[1] += meta["params"].get("duration") or 0
        return cls(history)

    def add(self, key: Key, elapsed: float, duration: float) -> None:
        acc = self.run.setdefault(key, [0.0, 0.0])
        acc[0] += elapsed
        acc[1] += duration

    def rate(self, key: Key) -> float | None:
        """動画1秒あたりの生成秒数。今回の実績 → 過去の記録 → 今回の全体平均の順に使う。"""
        for table in (self.run, self.history):
            acc = table.get(key)
            if acc and acc[1] > 0:
                return acc[0] / acc[1]
        total = [sum(v[0] for v in self.run.values()), sum(v[1] for v in self.run.values())]
        return total[0] / total[1] if total[1] > 0 else None

    def remaining(self, items: list[tuple[Key, float]]) -> float | None:
        """残りジョブ [(key, 動画秒数)] の所要時間。見積もれなければ None。"""
        total = 0.0
        for key, duration in items:
            r = self.rate(key)
            if r is None:
                return None
            total += r * duration
        return total


def fmt_duration(sec: float) -> str:
    sec = int(round(sec))
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}時間{m}分"
    if m:
        return f"{m}分"
    return f"{s}秒"


def fmt_eta(remaining: float | None, count: int) -> str:
    if count == 0:
        return "残りなし"
    if remaining is None:
        return f"残り {count}本"
    end = datetime.datetime.now() + datetime.timedelta(seconds=remaining)
    return f"残り {count}本・約{fmt_duration(remaining)}（{end:%H:%M} 頃終了）"
