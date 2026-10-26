"""生成記録・設定変更の検出・残り時間の見積もりのテスト。"""

import json
import tempfile
import unittest
from pathlib import Path

from mvgen.metadata import (MISSING, OK, STALE, UNKNOWN, changed_keys, effective_steps,
                            generation_params, video_state)
from mvgen.plan import resolve_clip
from mvgen.progress import Eta, fmt_duration, fmt_eta
from tests.helpers import make_project, write_fake_meta


class TestMetadata(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.cfg, self.movies = make_project(self.root)
        self.cfg.out_dir.mkdir()
        self.video = self.cfg.out_dir / "s_01_a.mp4"

    def tearDown(self):
        self.tmp.cleanup()

    def clip(self, cfg=None, movie=None, **cli):
        return resolve_clip(movie or self.movies[0], cfg or self.cfg, cli)

    def state(self, clip):
        return video_state(self.video, generation_params(clip, clip.seed, self.cfg))

    def test_missing_unknown_ok(self):
        self.assertEqual(self.state(self.clip()), (MISSING, []))
        self.video.write_bytes(b"x")
        self.assertEqual(self.state(self.clip()), (UNKNOWN, []))
        meta = write_fake_meta(self.cfg, self.clip(), 1, self.video, elapsed_seconds=10)
        self.assertEqual(self.state(self.clip()), (OK, []))
        self.assertEqual(meta["take"], 1)
        self.assertEqual(meta["params"]["images"][0]["name"], "s_01_a.png")

    def test_prompt_change_is_stale(self):
        self.video.write_bytes(b"x")
        write_fake_meta(self.cfg, self.clip(), 1, self.video)
        movie = dict(self.movies[0], prompt="changed prompt")
        self.assertEqual(self.state(self.clip(movie=movie)), (STALE, ["プロンプト"]))

    def test_image_content_change_is_stale(self):
        self.video.write_bytes(b"x")
        write_fake_meta(self.cfg, self.clip(), 1, self.video)
        (self.cfg.image_dir / "s_01_a.png").write_bytes(b"regenerated image")
        self.assertEqual(self.state(self.clip()), (STALE, ["画像"]))

    def test_settings_change_is_stale(self):
        self.video.write_bytes(b"x")
        write_fake_meta(self.cfg, self.clip(), 1, self.video)
        state, diff = self.state(self.clip(megapixels=0.4, turbo=False))
        self.assertEqual(state, STALE)
        self.assertEqual(diff, ["解像度", "ステップ数", "turbo", "モデル"])

    def test_effective_steps(self):
        self.assertEqual(effective_steps(self.clip(), self.cfg), 8)
        self.assertEqual(effective_steps(self.clip(turbo=False), self.cfg), 20)
        self.assertEqual(effective_steps(self.clip(steps=5), self.cfg), 5)
        self.assertIsNone(effective_steps(self.clip(mode="r2v"), self.cfg))

    def test_changed_keys(self):
        self.assertEqual(changed_keys({"a": 1, "seed": 1}, {"a": 1, "seed": 2}), ["seed"])
        self.assertEqual(changed_keys({}, {}), [])


class TestEta(unittest.TestCase):
    def test_uses_history_then_run(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d)
            meta = {"elapsed_seconds": 120, "params": {"mode": "i2v", "megapixels": 0.2,
                                                       "steps": 8, "duration": 6}}
            (out / "a.json").write_text(json.dumps(meta), encoding="utf-8")
            eta = Eta.from_dir(out)
            key = ("i2v", 0.2, 8)
            self.assertAlmostEqual(eta.rate(key), 20.0)           # 過去の記録: 120秒 / 6秒
            self.assertAlmostEqual(eta.remaining([(key, 6), (key, 3)]), 180.0)
            eta.add(key, 300, 10)                                  # 今回の実績を優先
            self.assertAlmostEqual(eta.rate(key), 30.0)
            self.assertAlmostEqual(eta.rate(("r2v", 0.2, None)), 30.0)  # 記録が無い設定は全体平均

    def test_unknown(self):
        eta = Eta()
        self.assertIsNone(eta.remaining([(("i2v", 0.2, 8), 6)]))
        self.assertEqual(fmt_eta(None, 3), "残り 3本")

    def test_format(self):
        self.assertEqual(fmt_duration(45), "45秒")
        self.assertEqual(fmt_duration(600), "10分")
        self.assertEqual(fmt_duration(6000), "1時間40分")
        self.assertIn("約10分", fmt_eta(600, 2))


if __name__ == "__main__":
    unittest.main()
