"""Behavior tests for deterministic content generation; no external services."""
from datetime import date
import os
from pathlib import Path
import tempfile
import tomllib
import unittest

from scripts.update_site import (Entry, collect, extend_nav, frontmatter, nav_paths,
                                 outputs, replace_block, render_nav, timeline_html)

ROOT = Path(__file__).resolve().parents[1]


class ContentTests(unittest.TestCase):
    def test_yaml_titles_dates_and_legacy_keys(self):
        meta = frontmatter('\ufeff---\nTitle: "A: B # C"\nDate: 2026-01-02\nsummary: |\n  title: not metadata\n---\nText')
        self.assertEqual(meta['title'], 'A: B # C')
        self.assertEqual(meta['date'], date(2026, 1, 2))

    def test_scan_is_independent_of_checkout_timestamps(self):
        with tempfile.TemporaryDirectory() as directory:
            docs = Path(directory)
            (docs / 'essay').mkdir()
            (docs / 'note' / 'Course').mkdir(parents=True)
            for name in ('a', 'b'):
                (docs / 'note' / 'Course' / f'{name}.md').write_text('---\ndate: 2026-01-02\n---\n')
            (docs / 'essay' / 'undated.md').write_text('```\n# Ignore\n```\n## Actual title')
            first = collect(docs)
            for path in docs.rglob('*.md'):
                os.utime(path, (1, 1))
            self.assertEqual(first, collect(docs))
            self.assertEqual(first[-1].title, 'Actual title')
            self.assertIsNone(first[-1].date)

    def test_links_and_titles_are_escaped_without_losing_nested_paths(self):
        entry = Entry(Path('blog/nested/A #&.md'), '<Title & "quote">', date(2026, 1, 2))
        html = timeline_html([entry])
        self.assertIn('href="nested/A%20%23%26/"', html)
        self.assertIn('&lt;Title &amp; &quot;quote&quot;&gt;', html)
        self.assertNotIn('<Title', html)

    def test_marker_replacement_is_literal_and_rejects_ambiguous_blocks(self):
        text = 'Before\n<!-- x:auto-begin -->\nOld\n<!-- x:auto-end -->\nAfter'
        result = replace_block(text, 'x', r'\1 literal')
        self.assertIn(r'\1 literal', result)
        self.assertTrue(result.endswith('After'))
        with self.assertRaises(ValueError):
            replace_block(text + text, 'x', 'new')

    def test_navigation_uses_directory_identity_not_display_name(self):
        nav = [{'博客': ['blog/index.md']}, {'笔记': ['note/index.md', {'常微分方程': ['note/ODE/first.md']}]}]
        entries = [Entry(Path('note/ODE/next.md'), 'next', None),
                   Entry(Path('note/New/one.md'), 'one', None)]
        extend_nav(nav, entries)
        extend_nav(nav, entries)
        groups = nav[1]['笔记']
        self.assertEqual(groups[1]['常微分方程'], ['note/ODE/first.md', 'note/ODE/next.md'])
        self.assertEqual(len(groups), 3)
        self.assertEqual(tomllib.loads('nav = ' + render_nav(nav))['nav'], nav)

    def test_repository_outputs_are_current_and_navigation_resolves(self):
        for path, generated in outputs(ROOT).items():
            self.assertEqual(path.read_text(), generated, f'Run update.sh: {path}')
        config = tomllib.loads((ROOT / 'zensical.toml').read_text())
        for path in nav_paths(config['project']['nav']):
            self.assertTrue((ROOT / 'docs' / path).is_file(), path)


if __name__ == '__main__':
    unittest.main()
