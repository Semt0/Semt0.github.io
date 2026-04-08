import importlib.util
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
ENGINE_PATH = ROOT / ".trae" / "rules" / "rule_engine.py"
SPEC = importlib.util.spec_from_file_location("rule_engine", ENGINE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC is not None and SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)
choose_image_width = MODULE.choose_image_width
evaluate_request = MODULE.evaluate_request
resolve_conflict = MODULE.resolve_conflict


class TestRulePriority(unittest.TestCase):
    def test_conflict_prefers_blog_project_mdc(self) -> None:
        a = "/Users/semt0/blog/Semt0.github.io/CLAUDE.md"
        b = "/Users/semt0/blog/Semt0.github.io/.cursor/rules/blog-project.mdc"
        self.assertEqual(resolve_conflict(a, b), b)


class TestRuleTrigger(unittest.TestCase):
    def test_block_formula_rule_triggered(self) -> None:
        text = "请把行间公式统一改成 $$...$$ 并检查渲染"
        self.assertIn("R-P1-07", evaluate_request(text))

    def test_aligned_pseudocode_rule_triggered(self) -> None:
        text = "把算法伪代码改成 aligned 环境"
        self.assertIn("R-P1-09", evaluate_request(text))

    def test_no_manual_toc_rule_triggered(self) -> None:
        text = "在笔记里新增 ## 目录 章节"
        self.assertIn("R-P2-02", evaluate_request(text))


class TestRuleExecution(unittest.TestCase):
    def test_image_width_resolution(self) -> None:
        self.assertEqual(choose_image_width([800, 550]), 550)

    def test_image_width_default(self) -> None:
        self.assertEqual(choose_image_width([]), 550)


if __name__ == "__main__":
    unittest.main()
