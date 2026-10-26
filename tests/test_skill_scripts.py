"""skills/music-video-production/scripts のテスト（リポジトリ直下のサンプルデータを使う）。"""

import importlib.util
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests.helpers import REPO

SCRIPTS = REPO / "skills" / "music-video-production" / "scripts"


def run(script, *args):
    return subprocess.run([sys.executable, str(SCRIPTS / script), *map(str, args)],
                          capture_output=True, text=True, encoding="utf-8")


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@unittest.skipUnless((REPO / "movies.md").is_file(), "サンプルデータが必要")
class TestSampleProject(unittest.TestCase):
    def test_check_assets_passes_with_auto_detected_refs(self):
        res = run("check_mv_assets.py", REPO, "--prefix", "hope_", "--song-seconds", "176")
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
        self.assertIn("refs=7", res.stdout)

    def test_gen_movies_table_reproduces_movies_yaml(self):
        with tempfile.TemporaryDirectory() as d:
            shutil.copy(REPO / "movies.md", d)
            res = run("gen_movies_table.py", d)
            self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
            self.assertEqual((Path(d) / "movies.yaml").read_bytes(), (REPO / "movies.yaml").read_bytes())


class TestFindRefsCsv(unittest.TestCase):
    def setUp(self):
        self.mod = load("check_mv_assets")
        self.tmp = tempfile.TemporaryDirectory()
        self.base = self.tmp.name

    def tearDown(self):
        self.tmp.cleanup()

    def touch(self, name):
        (Path(self.base) / name).write_text("", encoding="utf-8")

    def test_none(self):
        self.assertIsNone(self.mod.find_refs_csv(self.base, None, None))

    def test_prefix_and_single_and_explicit(self):
        self.touch("ab_refs.csv")
        self.assertTrue(self.mod.find_refs_csv(self.base, None, None).endswith("ab_refs.csv"))
        self.touch("xy_refs.csv")
        self.assertTrue(self.mod.find_refs_csv(self.base, "xy_", None).endswith("xy_refs.csv"))
        self.assertTrue(self.mod.find_refs_csv(self.base, None, "ab_refs.csv").endswith("ab_refs.csv"))
        with self.assertRaises(SystemExit):  # 候補が複数で決められない
            self.mod.find_refs_csv(self.base, None, None)


if __name__ == "__main__":
    unittest.main()
