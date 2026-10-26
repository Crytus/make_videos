"""設定の読み込み・クリップ設定の解決・ジョブ組み立てのテスト。"""

import tempfile
import unittest
from pathlib import Path

from mvgen.config import Config
from mvgen.movies import frame_length, load_movies
from mvgen.plan import build_jobs, list_takes, resolve_clip, take_path, take_seed
from tests.helpers import REPO, make_project


class TestConfig(unittest.TestCase):
    def test_repo_config_loads(self):
        cfg = Config.load(REPO / "config.yaml")
        self.assertEqual(cfg.gen["megapixels"], 0.2)
        self.assertEqual(cfg.gen["mode"], "i2v")
        self.assertEqual(cfg.out_dir, REPO / "videos")
        self.assertEqual(cfg.selected_path, REPO / "videos" / "selected.yaml")
        for m in load_movies(cfg.movies_path):
            resolve_clip(m, cfg)  # 全クリップで設定が解決できる

    def test_missing_file_uses_defaults(self):
        with tempfile.TemporaryDirectory() as d:
            cfg = Config.load(Path(d) / "none.yaml")
            self.assertEqual(cfg.gen["megapixels"], 0.2)
            self.assertEqual(cfg.out_dir, Path(d) / "videos")

    def test_partial_override_keeps_other_defaults(self):
        with tempfile.TemporaryDirectory() as d:
            cfg, _ = make_project(Path(d), {"generation": {"takes": 2}})
            self.assertEqual(cfg.gen["takes"], 2)
            self.assertEqual(cfg.gen["megapixels"], 0.2)

    def test_unquoted_clip_id_is_normalized(self):
        with tempfile.TemporaryDirectory() as d:
            cfg, _ = make_project(Path(d), {"clips": {1: {"takes": 2}}})
            self.assertIn("01", cfg.clips)

    def test_invalid_clip_key(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                make_project(Path(d), {"clips": {"01": {"take": 2}}})

    def test_invalid_mode(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                make_project(Path(d), {"generation": {"mode": "t2v"}})


class TestResolveClip(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_defaults(self):
        cfg, movies = make_project(self.root)
        c = resolve_clip(movies[0], cfg)
        self.assertEqual((c.mode, c.megapixels, c.turbo, c.takes), ("i2v", 0.2, True, 1))
        self.assertEqual(c.seed, 1001)
        self.assertEqual(c.prompt, "prompt one")
        self.assertEqual(resolve_clip(movies[2], cfg).seed, 1101)  # E-1

    def test_priority_cli_over_clip_over_generation(self):
        cfg, movies = make_project(self.root, {
            "generation": {"megapixels": 0.3, "takes": 2},
            "clips": {"01": {"megapixels": 0.5, "takes": 3}}})
        self.assertEqual(resolve_clip(movies[1], cfg).megapixels, 0.3)
        c = resolve_clip(movies[0], cfg)
        self.assertEqual((c.megapixels, c.takes), (0.5, 3))
        self.assertEqual(c.overridden, ["megapixels", "takes"])
        c = resolve_clip(movies[0], cfg, {"megapixels": 0.9, "takes": None})
        self.assertEqual((c.megapixels, c.takes), (0.9, 3))

    def test_r2v_override_with_images_and_prompt_file(self):
        (self.root / "prompts").mkdir()
        (self.root / "prompts" / "01.txt").write_text("subject_definitions: ...\n", encoding="utf-8")
        cfg, movies = make_project(self.root, {"clips": {"01": {
            "mode": "r2v", "ref-images": ["s_01_a.png", "s_02_b.png"],
            "prompt_file": "prompts/01.txt", "seed": 42}}})
        c = resolve_clip(movies[0], cfg)
        self.assertEqual(c.mode, "r2v")
        self.assertEqual(c.images, ["s_01_a.png", "s_02_b.png"])
        self.assertEqual(c.prompt, "subject_definitions: ...")
        self.assertEqual(c.seed, 42)

    def test_i2v_uses_only_first_image(self):
        cfg, movies = make_project(self.root, {"clips": {"01": {"ref-images": ["a.png", "b.png"]}}})
        self.assertEqual(resolve_clip(movies[0], cfg).images, ["a.png"])

    def test_cli_seed(self):
        cfg, movies = make_project(self.root, {"clips": {"01": {"seed": 42}}})
        self.assertEqual(resolve_clip(movies[0], cfg, {"seed": 7}).seed, 7)
        self.assertEqual(resolve_clip(movies[1], cfg, {"seed_base": 5000}).seed, 5002)


class TestJobs(unittest.TestCase):
    def test_take_path_and_seed(self):
        out = Path("v")
        self.assertEqual(take_path(out, "s_01", 1), out / "s_01.mp4")
        self.assertEqual(take_path(out, "s_01", 3), out / "s_01_t3.mp4")
        self.assertEqual(take_seed(1001, 1), 1001)
        self.assertEqual(take_seed(1001, 3), 3001)

    def test_jobs_ordered_by_take_then_clip(self):
        with tempfile.TemporaryDirectory() as d:
            cfg, movies = make_project(Path(d), {"clips": {"02": {"takes": 3}, "01": {"takes": 2}}})
            clips = [resolve_clip(m, cfg) for m in movies]
            jobs = build_jobs(clips, cfg.out_dir)
            self.assertEqual([(j.clip.id, j.take) for j in jobs],
                             [("01", 1), ("02", 1), ("E-1", 1), ("01", 2), ("02", 2), ("02", 3)])
            self.assertEqual(len({j.seed for j in jobs}), len(jobs))

    def test_list_takes(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d)
            for name in ("s_01.mp4", "s_01_t2.mp4", "s_01_t10.mp4", "s_011.mp4", "s_01_t2.json"):
                (out / name).write_bytes(b"x")
            (out / "s_01_t3.mp4").write_bytes(b"")  # 空ファイルは未生成
            self.assertEqual(list(list_takes(out, "s_01")), [1, 2, 10])

    def test_frame_length(self):
        for sec in (4, 6, 7, 8, 10, 15):
            n = frame_length(sec)
            self.assertEqual(n % 17, 5)
            self.assertTrue(0 <= n - sec * 24 < 17)


if __name__ == "__main__":
    unittest.main()
