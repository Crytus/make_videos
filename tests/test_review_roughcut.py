"""レビューページ・選択の保存・ラフ版・通知のテスト。"""

import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest import mock

from mvgen import media, notify
from mvgen.plan import resolve_clip
from mvgen.review import build_review, make_handler
from mvgen.roughcut import build_filter, build_roughcut, plan_cues
from mvgen.selection import load_selection, save_selection
from tests.helpers import HAS_FFMPEG, make_project, make_video, write_fake_meta


class ProjectTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.cfg, self.movies = make_project(self.root)
        self.cfg.out_dir.mkdir()
        self.clips = [resolve_clip(m, self.cfg) for m in self.movies]

    def tearDown(self):
        self.tmp.cleanup()


class TestSelection(ProjectTestCase):
    def test_roundtrip_in_movie_order(self):
        path = self.cfg.selected_path
        save_selection(path, {"E-1": "c.mp4", "01": "a_t2.mp4"}, ["01", "02", "E-1"])
        text = path.read_text(encoding="utf-8")
        self.assertLess(text.index('"01"'), text.index('"E-1"'))
        self.assertEqual(load_selection(path), {"01": "a_t2.mp4", "E-1": "c.mp4"})

    def test_unquoted_ids(self):
        self.cfg.selected_path.write_text("1: a.mp4\nE-1: c.mp4\n", encoding="utf-8")
        self.assertEqual(load_selection(self.cfg.selected_path), {"01": "a.mp4", "E-1": "c.mp4"})


class TestReview(ProjectTestCase):
    def test_html_contents(self):
        out = self.cfg.out_dir
        (out / "s_01_a.mp4").write_bytes(b"x")
        (out / "s_01_a_t2.mp4").write_bytes(b"x")
        write_fake_meta(self.cfg, self.clips[0], 1, out / "s_01_a.mp4", elapsed_seconds=90)
        save_selection(self.cfg.selected_path, {"01": "s_01_a_t2.mp4"}, ["01"])
        with mock.patch.object(media, "ffmpeg_available", return_value=False):
            path = build_review(self.cfg, self.clips)
        html = path.read_text(encoding="utf-8")
        self.assertIn('src="s_01_a.mp4"', html)
        self.assertIn('src="../output/s_01_a.png"', html)     # 開始画像への相対パス
        self.assertIn('value="s_01_a_t2.mp4" checked', html)  # 選択済みのテイク
        self.assertIn("最新", html)
        self.assertIn("記録なし", html)                        # t2 は記録なし
        self.assertIn("未生成", html)                          # 02 と E-1
        self.assertIn("歌詞一", html)
        self.assertIn("prompt one", html)

    def test_html_escapes(self):
        movies = [dict(self.movies[0], prompt="<script>alert(1)</script>")]
        clips = [resolve_clip(movies[0], self.cfg)]
        with mock.patch.object(media, "ffmpeg_available", return_value=False):
            html = build_review(self.cfg, clips).read_text(encoding="utf-8")
        self.assertNotIn("<script>alert", html)

    @unittest.skipUnless(HAS_FFMPEG, "ffmpeg が必要")
    def test_frames_extracted(self):
        make_video(self.cfg.out_dir / "s_01_a.mp4", 2)
        html = build_review(self.cfg, self.clips).read_text(encoding="utf-8")
        for tag in ("first", "mid", "last"):
            self.assertTrue((self.cfg.frames_dir / f"s_01_a_{tag}.jpg").is_file())
            self.assertIn(f"review_frames/s_01_a_{tag}.jpg", html)


class TestReviewServer(ProjectTestCase):
    def setUp(self):
        super().setUp()
        (self.cfg.out_dir / "s_01_a_t2.mp4").write_bytes(b"x")
        with mock.patch.object(media, "ffmpeg_available", return_value=False):
            build_review(self.cfg, self.clips)
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0),
                                         make_handler(self.cfg, [c.id for c in self.clips]))
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()
        self.base = f"http://127.0.0.1:{self.httpd.server_address[1]}"

    def tearDown(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        super().tearDown()

    def post(self, data):
        req = urllib.request.Request(f"{self.base}/videos/api/selection",
                                     data=json.dumps(data).encode(),
                                     headers={"Content-Type": "application/json"})
        return urllib.request.urlopen(req, timeout=5)

    def test_serves_review_and_images(self):
        with urllib.request.urlopen(f"{self.base}/videos/review.html", timeout=5) as r:
            self.assertIn("クリップ確認", r.read().decode("utf-8"))
        with urllib.request.urlopen(f"{self.base}/output/s_01_a.png", timeout=5) as r:
            self.assertEqual(r.status, 200)

    def test_head_returns_last_modified_for_update_check(self):
        req = urllib.request.Request(f"{self.base}/videos/review.html", method="HEAD")
        with urllib.request.urlopen(req, timeout=5) as r:
            self.assertTrue(r.headers.get("Last-Modified"))
        html = self.cfg.review_path.read_text(encoding="utf-8")
        self.assertIn('id="updated"', html)
        self.assertIn("checkUpdate", html)

    def test_save_selection(self):
        with self.post({"01": "s_01_a_t2.mp4"}) as r:
            self.assertEqual(r.status, 200)
        self.assertEqual(load_selection(self.cfg.selected_path), {"01": "s_01_a_t2.mp4"})

    def test_rejects_invalid(self):
        for bad in ({"01": "../config_video.yaml"}, {"01": "nothing.mp4"}, {"99": "s_01_a_t2.mp4"}):
            with self.assertRaises(urllib.error.HTTPError) as cm:
                self.post(bad)
            self.assertEqual(cm.exception.code, 400)
        self.assertFalse(self.cfg.selected_path.exists())


class TestRoughcut(ProjectTestCase):
    def test_plan_cues_priority(self):
        out = self.cfg.out_dir
        for name in ("s_01_a.mp4", "s_01_a_t2.mp4", "s_02_b_t3.mp4"):
            (out / name).write_bytes(b"x")
        save_selection(self.cfg.selected_path, {"01": "s_01_a_t2.mp4"}, ["01"])
        cues = plan_cues(self.cfg, self.clips)
        self.assertEqual([c.source.name if c.source else None for c in cues],
                         ["s_01_a_t2.mp4", "s_02_b_t3.mp4", None])
        self.assertEqual([c.start for c in cues], [0, 2, 5])

    def test_filter_graph(self):
        out = self.cfg.out_dir
        (out / "s_01_a.mp4").write_bytes(b"x")
        cues = plan_cues(self.cfg, self.clips)
        graph, inputs = build_filter(cues, {out / "s_01_a.mp4": {"has_audio": False}}, 160, 96)
        self.assertEqual(inputs, [out / "s_01_a.mp4"])
        self.assertIn("trim=duration=2.0", graph)
        self.assertIn("color=c=black:s=160x96", graph)
        self.assertIn("concat=n=3:v=1:a=1", graph)
        graph, _ = build_filter(cues, {out / "s_01_a.mp4": {"has_audio": True}}, 160, 96,
                                with_audio=False)
        self.assertNotIn("[0:a]", graph)
        self.assertIn("concat=n=3:v=1:a=0[vout]", graph)

    @unittest.skipUnless(HAS_FFMPEG, "ffmpeg が必要")
    def test_build_roughcut(self):
        out = self.cfg.out_dir
        make_video(out / "s_01_a.mp4", 2.5)                 # 長い → 2秒に切る
        make_video(out / "s_02_b.mp4", 1.0, audio=False)    # 短い・音声なし → 3秒に延長
        output, cues = build_roughcut(self.cfg, self.clips)  # E-1 は未生成 → 黒
        info = media.probe(output)
        self.assertAlmostEqual(info["duration"], 7.0, delta=0.15)
        self.assertEqual((info["width"], info["height"]), (160, 90))
        self.assertTrue(info["has_audio"])
        self.assertFalse(list(out.glob("*.part*")))

    @unittest.skipUnless(HAS_FFMPEG, "ffmpeg が必要")
    def test_build_roughcut_with_song(self):
        out = self.cfg.out_dir
        make_video(out / "s_01_a.mp4", 2)
        song = self.root / "song.m4a"
        media.run_ffmpeg(["-f", "lavfi", "-i", "sine=frequency=220:duration=10", str(song)])
        output, _ = build_roughcut(self.cfg, self.clips, audio=song)
        info = media.probe(output)
        self.assertAlmostEqual(info["duration"], 7.0, delta=0.15)  # 音源が長くても映像の尺で切る
        self.assertTrue(info["has_audio"])


class TestNotify(unittest.TestCase):
    def test_webhook_payload(self):
        captured = {}

        class Res:
            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

        def fake_urlopen(req, timeout):
            captured["body"] = json.loads(req.data)
            return Res()

        with mock.patch("urllib.request.urlopen", fake_urlopen):
            notify.webhook("http://example.invalid", "完了")
        self.assertEqual(captured["body"], {"content": "完了", "text": "完了"})

    def test_failures_do_not_raise(self):
        with mock.patch.object(notify, "toast", side_effect=OSError("x")), \
                mock.patch.object(notify, "webhook", side_effect=OSError("y")), \
                mock.patch("sys.stderr"):
            notify.notify({"toast": True, "webhook": "http://example.invalid"}, "t", "m")

    def test_disabled(self):
        with mock.patch.object(notify, "toast") as t, mock.patch.object(notify, "webhook") as w:
            notify.notify({"toast": False, "webhook": None}, "t", "m")
        t.assert_not_called()
        w.assert_not_called()


if __name__ == "__main__":
    unittest.main()
