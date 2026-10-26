"""ワークフロー組み立てのテスト。"""

import json
import unittest

from mvgen.config import DEFAULTS
from mvgen.movies import frame_length
from mvgen.workflow import build_i2v_workflow, build_r2v_workflow
from tests.helpers import REPO


def assert_links_valid(tc, wf):
    """全リンクが存在するノードを指していることを確認する。"""
    for node_id, node in wf.items():
        for key, val in node["inputs"].items():
            if isinstance(val, list) and len(val) == 2 and isinstance(val[1], int):
                tc.assertIn(val[0], wf, f"{node_id}.{key} が存在しないノード {val[0]} を参照")


def i2v(**kw):
    args = dict(prompt="P", duration=8, image_name="hope/x.png", seed=5, megapixels=0.2,
                turbo=True, steps=8, models=DEFAULTS["i2v"], filename_prefix="video/x")
    args.update(kw)
    return build_i2v_workflow(**args)


class TestI2V(unittest.TestCase):
    def test_turbo(self):
        wf = i2v()
        assert_links_valid(self, wf)
        self.assertEqual(wf["8"]["inputs"]["length"], frame_length(8))
        self.assertEqual(wf["7"]["inputs"]["megapixels"], 0.2)
        self.assertEqual(wf["6"]["inputs"]["image"], "hope/x.png")
        self.assertEqual(wf["11"]["inputs"]["model"], ["2", 0])
        self.assertEqual(wf["9"]["inputs"]["noise_seed"], 5)

    def test_no_turbo(self):
        wf = i2v(turbo=False, steps=20)
        assert_links_valid(self, wf)
        self.assertNotIn("2", wf)
        self.assertEqual(wf["11"]["inputs"]["steps"], 20)
        self.assertEqual(wf["12"]["inputs"]["model"], ["1", 0])


class TestR2V(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.template = json.loads((REPO / "minimaxh3_r2v.json").read_text(encoding="utf-8"))

    def build(self, images, **kw):
        args = dict(prompt="P", duration=6, image_names=images, seed=7, megapixels=0.2,
                    steps=None, filename_prefix="video/a")
        args.update(kw)
        return build_r2v_workflow(self.template, **args)

    def test_single_image_removes_unused_loaders(self):
        wf = self.build(["hope/a.png"])
        assert_links_valid(self, wf)
        self.assertNotIn("188", wf)
        self.assertNotIn("189", wf)
        self.assertNotIn("ref_images.ref_image_1", wf["136"]["inputs"])
        self.assertEqual(wf["132"]["inputs"]["value"], 6.0)
        self.assertEqual(wf["138"]["inputs"]["value"], "P")
        self.assertEqual(wf["161"]["inputs"]["seed"], 7)
        self.assertEqual(wf["161"]["inputs"]["steps"], self.template["161"]["inputs"]["steps"])
        self.assertEqual(wf["115"]["inputs"]["megapixels"], 0.2)
        self.assertIn("188", self.template)  # テンプレート自体は変更しない

    def test_three_images_and_steps(self):
        wf = self.build(["a", "b", "c"], steps=4)
        assert_links_valid(self, wf)
        self.assertEqual(wf["189"]["inputs"]["image"], "c")
        self.assertEqual(wf["161"]["inputs"]["steps"], 4)

    def test_too_many_images(self):
        with self.assertRaises(ValueError):
            self.build(list("abcd"))

    def test_template_without_expected_nodes(self):
        with self.assertRaises(ValueError):
            build_r2v_workflow({}, prompt="P", duration=6, image_names=["a"], seed=1,
                               megapixels=0.2, steps=None, filename_prefix="p")


if __name__ == "__main__":
    unittest.main()
