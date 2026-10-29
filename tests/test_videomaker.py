"""videomaker 用シナリオ YAML の書き出しのテスト。"""

import io
import json
import tempfile
import threading
import unittest
import urllib.request
from contextlib import redirect_stderr, redirect_stdout
from http.server import ThreadingHTTPServer
from pathlib import Path

import yaml

from mvgen import cli
from mvgen.plan import resolve_clip
from mvgen.review import make_handler
from mvgen.selection import save_selection
from mvgen.videomaker import build_videomaker, subtitle_text
from tests.helpers import make_project


class VideomakerTestCase(unittest.TestCase):
    config: dict | None = None

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.cfg, self.movies = make_project(self.root, self.config)
        self.cfg.out_dir.mkdir()
        self.clips = [resolve_clip(m, self.cfg) for m in self.movies]

    def tearDown(self):
        self.tmp.cleanup()

    def load(self, path=None):
        return yaml.safe_load((path or self.cfg.videomaker_output).read_text(encoding="utf-8"))


class TestSubtitleText(unittest.TestCase):
    def test_notes_are_blank(self):
        for note in ("（イントロ／歌唱なし）", "(間奏)", " （アウトロ） ", "", None):
            self.assertEqual(subtitle_text(note), "")

    def test_lyrics_kept(self):
        self.assertEqual(subtitle_text("新しい朝が"), "新しい朝が")
        self.assertEqual(subtitle_text("一行目\n二行目\n"), "一行目\n二行目")
        self.assertEqual(subtitle_text("（かっこ）で始まる歌詞"), "（かっこ）で始まる歌詞")


class TestBuildVideomaker(VideomakerTestCase):
    def test_scenes(self):
        out = self.cfg.out_dir
        for name in ("s_01_a.mp4", "s_01_a_t2.mp4", "s_02_b_t3.mp4"):
            (out / name).write_bytes(b"x")
        save_selection(self.cfg.selected_path, {"01": "s_01_a_t2.mp4"}, ["01"])
        path, _ = build_videomaker(self.cfg, self.clips)
        self.assertEqual(path, out / "videomaker.yaml")
        data = self.load()
        self.assertEqual(data["video"], {"width": 1920, "height": 1080, "fps": 30,
                                         "bgm_volume": 1.0, "bgm_loop": False})
        self.assertEqual(data["scenes"], [
            {"id": "01", "video": "s_01_a_t2.mp4", "duration": 2, "subtitle": "歌詞一"},  # 採用テイク
            {"id": "02", "video": "s_02_b_t3.mp4", "duration": 3, "subtitle": "歌詞二"},  # 残りのテイク
            {"id": "E-1", "image": "../output/s_E1_c.png", "duration": 2, "subtitle": ""},  # 未生成は開始画像
        ])
        self.assertNotIn("options", data)
        self.assertFalse(list(out.glob("*.part")))

    def test_subtitle_none(self):
        self.cfg.data["videomaker"]["subtitle"] = "none"
        build_videomaker(self.cfg, self.clips)
        self.assertEqual({s["subtitle"] for s in self.load()["scenes"]}, {""})

    def test_multiline_lyrics_block_style(self):
        movies = [dict(self.movies[0], lyrics="一行目\n二行目", duration=2.5)]
        build_videomaker(self.cfg, [resolve_clip(movies[0], self.cfg)])
        text = self.cfg.videomaker_output.read_text(encoding="utf-8")
        self.assertIn("subtitle: |-\n      一行目\n      二行目", text)
        self.assertEqual(self.load()["scenes"][0]["duration"], 2.5)

    def test_output_option(self):
        dest = self.root / "scenario" / "mv.yaml"
        (self.cfg.out_dir / "s_01_a.mp4").write_bytes(b"x")
        build_videomaker(self.cfg, self.clips, output=dest)
        self.assertEqual(self.load(dest)["scenes"][0]["video"], "../videos/s_01_a.mp4")


class TestVideoSection(VideomakerTestCase):
    config = {
        "roughcut": {"audio": "song.wav"},
        "videomaker": {
            "video": {"fps": 25, "voice": "narrator_female",
                      "subtitle": {"font": "fonts/a.ttc", "position": "bottom"}},
            "options": {"no_voice": True},
        },
    }

    def test_merge_and_paths(self):
        (self.root / "song.wav").write_bytes(b"x")
        (self.root / "fonts").mkdir()
        (self.root / "fonts" / "a.ttc").write_bytes(b"x")
        build_videomaker(self.cfg, self.clips)
        data = self.load()
        video = data["video"]
        self.assertEqual((video["width"], video["fps"], video["voice"]), (1920, 25, "narrator_female"))
        self.assertEqual(video["bgm"], "../song.wav")                # roughcut.audio を流用
        self.assertEqual(video["subtitle"]["font"], "../fonts/a.ttc")  # 実在すれば YAML 基準に直す
        self.assertEqual(data["options"], {"no_voice": True})

    def test_missing_paths_left_as_is(self):
        self.cfg.data["videomaker"]["video"]["bgm"] = "assets/sounds/x.wav"
        self.cfg.data["videomaker"]["video"]["subtitle"]["font"] = "msgothic.ttc"
        build_videomaker(self.cfg, self.clips)
        video = self.load()["video"]
        self.assertEqual(video["bgm"], "assets/sounds/x.wav")  # videomaker の assets/ 検索に任せる
        self.assertEqual(video["subtitle"]["font"], "msgothic.ttc")

    def test_invalid_subtitle_mode(self):
        from mvgen.config import Config, deep_merge
        with self.assertRaises(ValueError):
            Config(deep_merge(self.cfg.data, {"videomaker": {"subtitle": "x"}}), self.root)


class TestCliAndServer(VideomakerTestCase):
    def test_cli(self):
        (self.cfg.out_dir / "s_01_a.mp4").write_bytes(b"x")
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = cli.main(["videomaker", "--config", str(self.root / "config_video.yaml")])
        self.assertEqual(code, 0)
        self.assertIn("（7秒）", out.getvalue())
        self.assertIn("02 E-1", err.getvalue())  # 未生成の一覧
        self.assertEqual(len(self.load()["scenes"]), 3)

    def test_server_writes_scenario_on_save(self):
        (self.cfg.out_dir / "s_01_a_t2.mp4").write_bytes(b"x")
        handler = make_handler(self.cfg, [c.id for c in self.clips],
                               on_save=lambda: build_videomaker(self.cfg, self.clips)[0])
        httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        try:
            req = urllib.request.Request(
                f"http://127.0.0.1:{httpd.server_address[1]}/videos/api/selection",
                data=json.dumps({"01": "s_01_a_t2.mp4"}).encode(),
                headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=5) as r:
                self.assertEqual(r.read().decode("utf-8"), "selected.yaml と videomaker.yaml")
        finally:
            httpd.shutdown()
            httpd.server_close()
        self.assertEqual(self.load()["scenes"][0]["video"], "s_01_a_t2.mp4")


if __name__ == "__main__":
    unittest.main()
