"""generate / status コマンドのテスト（ComfyUI はモックに差し替える）。"""

import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

from mvgen import cli
from mvgen.config import BUNDLED_R2V_TEMPLATE, Config
from mvgen.plan import resolve_clip
from tests.helpers import make_project, write_fake_meta


class FakeClient:
    """ComfyClient の代わり。download で中身 b"new-<seed>" の動画を書く。"""

    def __init__(self, server):
        self.queued = []
        self.uploaded = []
        self.fail_on = set()

    def check(self):
        pass

    def upload_image(self, path, subfolder):
        self.uploaded.append(path.name)
        return f"{subfolder}/{path.name}"

    def queue(self, wf):
        self.queued.append(wf)
        return f"pid{len(self.queued)}"

    def wait(self, prompt_id, poll=5, timeout=0):
        wf = self.queued[int(prompt_id[3:]) - 1]
        prefix = next(n["inputs"]["filename_prefix"] for n in wf.values()
                      if "filename_prefix" in n["inputs"])
        if any(prefix.endswith(s) for s in self.fail_on):
            raise RuntimeError("テスト用の失敗")
        return {"outputs": {"9": {"images": [{"filename": "x.mp4", "subfolder": "v", "type": "output"}]}}}

    def download(self, info, dest):
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(b"new")


class GenerateTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def project(self, config=None):
        self.cfg, self.movies = make_project(self.root, config)
        return self.cfg

    def run_cli(self, *argv, fail_on=()):
        client = FakeClient(None)
        client.fail_on = set(fail_on)
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.object(cli, "ComfyClient", return_value=client), \
                redirect_stdout(out), redirect_stderr(err):
            code = cli.main([*argv, "--config", str(self.root / "config.yaml")])
        self.out, self.err = out.getvalue(), err.getvalue()
        return code, client


class TestGenerate(GenerateTestCase):
    def test_generates_all_and_writes_meta(self):
        cfg = self.project()
        code, client = self.run_cli("--no-review")
        self.assertEqual(code, 0, self.err)
        self.assertEqual(len(client.queued), 3)
        meta = json.loads((cfg.out_dir / "s_01_a.json").read_text(encoding="utf-8"))
        self.assertEqual(meta["params"]["seed"], 1001)
        self.assertEqual(meta["params"]["megapixels"], 0.2)
        self.assertIn("elapsed_seconds", meta)

    def test_skips_existing(self):
        cfg = self.project()
        cfg.out_dir.mkdir()
        (cfg.out_dir / "s_01_a.mp4").write_bytes(b"old")
        code, client = self.run_cli("--ids", "01", "02", "--no-review")
        self.assertEqual(code, 0)
        self.assertEqual(client.uploaded, ["s_02_b.png"])
        self.assertEqual((cfg.out_dir / "s_01_a.mp4").read_bytes(), b"old")

    def test_force(self):
        cfg = self.project()
        cfg.out_dir.mkdir()
        (cfg.out_dir / "s_01_a.mp4").write_bytes(b"old")
        _, client = self.run_cli("--ids", "01", "--force", "--no-review")
        self.assertEqual(len(client.queued), 1)
        self.assertEqual((cfg.out_dir / "s_01_a.mp4").read_bytes(), b"new")

    def test_takes(self):
        cfg = self.project({"clips": {"02": {"takes": 3}}})
        _, client = self.run_cli("--no-review")
        names = sorted(p.name for p in cfg.out_dir.glob("*.mp4"))
        self.assertEqual(names, ["s_01_a.mp4", "s_02_b.mp4", "s_02_b_t2.mp4", "s_02_b_t3.mp4",
                                 "s_E1_c.mp4"])
        seeds = [wf["9"]["inputs"]["noise_seed"] for wf in client.queued]
        self.assertEqual(seeds, [1001, 1002, 1101, 2002, 3002])  # take1 を先に一巡

    def test_cli_takes_adds_only_new_takes(self):
        self.project()
        self.run_cli("--ids", "01", "--no-review")
        _, client = self.run_cli("--ids", "01", "--takes", "2", "--no-review")
        self.assertEqual(len(client.queued), 1)
        self.assertEqual(client.queued[0]["9"]["inputs"]["noise_seed"], 2001)

    def test_stale_detection_and_regeneration(self):
        cfg = self.project()
        self.run_cli("--ids", "01", "--no-review")
        # プロンプトを変更
        text = cfg.movies_path.read_text(encoding="utf-8").replace("prompt one", "prompt one v2")
        cfg.movies_path.write_text(text, encoding="utf-8")

        code, client = self.run_cli("--ids", "01", "--no-review")
        self.assertEqual(len(client.queued), 0)
        self.assertIn("s_01_a.mp4: プロンプトが変更", self.out)

        _, client = self.run_cli("--ids", "01", "--stale", "--no-review")
        self.assertEqual(len(client.queued), 1)
        self.assertEqual(client.queued[0]["8"]["inputs"]["prompt"], "prompt one v2")
        _, client = self.run_cli("--ids", "01", "--stale", "--no-review")
        self.assertEqual(len(client.queued), 0)  # 再生成後は最新

    def test_unknown_is_not_regenerated_by_stale(self):
        cfg = self.project()
        cfg.out_dir.mkdir()
        (cfg.out_dir / "s_01_a.mp4").write_bytes(b"old")  # 記録なし
        _, client = self.run_cli("--ids", "01", "--stale", "--no-review")
        self.assertEqual(len(client.queued), 0)

    def test_r2v_override(self):
        self.project({"clips": {"02": {"mode": "r2v", "ref-images": ["s_02_b.png", "s_01_a.png"]}}})
        _, client = self.run_cli("--ids", "02", "--no-review")
        wf = client.queued[0]
        self.assertEqual(wf["136"]["class_type"], "MiniMaxH3ReferenceToVideo")
        self.assertEqual(wf["188"]["inputs"]["image"], "make_videos/s_01_a.png")
        self.assertNotIn("189", wf)

    def test_failure_continues_and_returns_1(self):
        cfg = self.project()
        code, client = self.run_cli("--no-review", fail_on=["s_01_a"])
        self.assertEqual(code, 1)
        self.assertEqual(len(client.queued), 3)
        self.assertFalse((cfg.out_dir / "s_01_a.mp4").exists())
        self.assertIn("s_01_a.mp4", self.err)

    def test_dry_run_writes_workflows_without_queue(self):
        cfg = self.project()
        code, client = self.run_cli("--dry-run", "--ids", "01")
        self.assertEqual(code, 0)
        self.assertEqual(client.queued, [])
        wf = json.loads((cfg.out_dir / "workflows" / "s_01_a_i2v.json").read_text(encoding="utf-8"))
        self.assertEqual(wf["7"]["inputs"]["megapixels"], 0.2)

    def test_missing_image(self):
        cfg = self.project()
        (cfg.image_dir / "s_02_b.png").unlink()
        code, client = self.run_cli()
        self.assertEqual(code, 2)
        self.assertEqual(client.queued, [])

    def test_unknown_id(self):
        self.project()
        with self.assertRaises(SystemExit):
            self.run_cli("--ids", "99")

    def test_notify_called(self):
        self.project({"notify": {"toast": True, "webhook": "http://example.invalid/hook"}})
        with mock.patch("mvgen.notify.toast") as toast, mock.patch("mvgen.notify.webhook") as hook:
            self.run_cli("--ids", "01", "--no-review")
        toast.assert_called_once()
        hook.assert_called_once()
        self.assertIn("成功 1本", toast.call_args.args[1])

    def test_review_updated_after_generate(self):
        cfg = self.project()
        with mock.patch("mvgen.review.media.ffmpeg_available", return_value=False):
            self.run_cli("--ids", "01")
        self.assertTrue(cfg.review_path.is_file())


class TestInitAndConfig(GenerateTestCase):
    def test_init_creates_template(self):
        dest = self.root / "proj" / "config.yaml"
        with redirect_stdout(io.StringIO()):
            self.assertEqual(cli.main(["init", "--config", str(dest)]), 0)
        cfg = Config.load(dest)
        self.assertEqual(cfg.gen["megapixels"], 0.2)
        self.assertEqual(cfg.image_dir, dest.parent / "images")
        self.assertEqual(cfg.r2v_template, BUNDLED_R2V_TEMPLATE)
        self.assertTrue(cfg.r2v_template.is_file())
        # 既存ファイルは上書きしない
        with redirect_stderr(io.StringIO()):
            self.assertEqual(cli.main(["init", "--config", str(dest)]), 2)
        with redirect_stdout(io.StringIO()):
            self.assertEqual(cli.main(["init", "--config", str(dest), "--force"]), 0)

    def test_default_config_is_in_current_directory(self):
        self.project()
        cwd = os.getcwd()
        os.chdir(self.root)
        try:
            args = cli.parse_args(["status"])
        finally:
            os.chdir(cwd)
        self.assertEqual(args.config.resolve(), (self.root / "config.yaml").resolve())
        self.assertEqual(args.command, "status")

    def test_r2v_uses_bundled_template_by_default(self):
        self.project({"clips": {"01": {"mode": "r2v"}}})
        _, client = self.run_cli("--ids", "01", "--no-review")
        self.assertEqual(client.queued[0]["136"]["class_type"], "MiniMaxH3ReferenceToVideo")


class TestStatus(GenerateTestCase):
    def test_status(self):
        cfg = self.project({"clips": {"01": {"takes": 2}}})
        cfg.out_dir.mkdir()
        clip = resolve_clip(self.movies[0], cfg)
        video = cfg.out_dir / "s_01_a.mp4"
        video.write_bytes(b"x")
        write_fake_meta(cfg, clip, 1, video)
        (cfg.out_dir / "s_02_b.mp4").write_bytes(b"x")
        (cfg.out_dir / "selected.yaml").write_text('"01": s_01_a.mp4\n', encoding="utf-8")
        code, _ = self.run_cli("status")
        self.assertEqual(code, 0)
        self.assertIn("t1○★ t2-", self.out)
        self.assertIn("t1?", self.out)
        self.assertIn("最新 1 / 設定変更あり 0 / 記録なし 1 / 未生成 2 / 採用 1/3", self.out)


if __name__ == "__main__":
    unittest.main()
