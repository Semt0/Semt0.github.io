#!/usr/bin/env python3
"""Regenerate timelines and missing navigation entries in one pass."""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date, datetime
from html import escape
import json
from pathlib import Path
import re
import tomllib
from urllib.parse import quote

import yaml

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = ("blog", "note", "essay")


@dataclass(frozen=True)
class Entry:
    path: Path  # relative to docs; never use checkout mtime as publication date
    title: str
    date: date | None

    @property
    def section(self) -> str:
        return self.path.parts[0]

    @property
    def category(self) -> str:
        return self.path.parts[1] if self.section == "note" and len(self.path.parts) > 2 else ""

    def href(self, *, relative: bool = False) -> str:
        path = Path(*self.path.parts[1:]) if relative else self.path
        return quote(path.with_suffix("").as_posix(), safe="/") + "/"


def frontmatter(text: str) -> dict:
    match = re.match(r"\A---[ \t]*\n(.*?)\n---[ \t]*(?:\n|$)", text.lstrip("\ufeff"), re.S)
    if not match:
        return {}
    data = yaml.safe_load(match[1]) or {}
    if not isinstance(data, dict):
        raise ValueError("Frontmatter must be a YAML mapping")
    return {str(key).lower(): value for key, value in data.items()}


def parse_date(value: object) -> date | None:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value))
    except ValueError:
        return None


def first_heading(text: str) -> str | None:
    fence = None
    for line in text.splitlines():
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            token = marker[1]
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            continue
        heading = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
        if fence is None and heading:
            return heading[1]
    return None


def collect(docs: Path) -> list[Entry]:
    entries = []
    for section in SECTIONS:
        for path in sorted((docs / section).rglob("*.md")):
            if path.name in {"index.md", "README.md"}:
                continue
            text = path.read_text(encoding="utf-8-sig")
            try:
                meta = frontmatter(text)
            except (yaml.YAMLError, ValueError) as error:
                raise ValueError(f"{path}: {error}") from error
            published = parse_date(meta.get("date", meta.get("data")))
            fallback = first_heading(text) if section == "essay" else None
            if section == "essay" and published is None:
                published = parse_date(path.stem)
            title = str(meta.get("title") or fallback or path.stem).strip()
            entries.append(Entry(path.relative_to(docs), title, published))
    return sorted(entries, key=lambda e: (e.date or date.min, e.path.as_posix()), reverse=True)


def replace_block(text: str, name: str, body: str) -> str:
    begin, end = f"<!-- {name}:auto-begin -->", f"<!-- {name}:auto-end -->"
    if text.count(begin) != 1 or text.count(end) != 1 or text.index(begin) >= text.index(end):
        raise ValueError(f"Expected exactly one ordered {name} marker pair")
    start, stop = text.index(begin), text.index(end) + len(end)
    return text[:start] + f"{begin}\n{body}\n{end}" + text[stop:]


def timeline_html(entries: list[Entry]) -> str:
    lines = ['<div class="timeline">']
    for entry in entries:
        stamp = (f'<time class="timeline-date" datetime="{entry.date}">{entry.date}</time>'
                 if entry.date else '<span class="timeline-date">未标日期</span>')
        lines.extend(['  <div class="timeline-item">', f'    {stamp}',
                      '    <div class="timeline-content">',
                      f'      <a href="{entry.href(relative=True)}">{escape(entry.title)}</a>'])
        if entry.category:
            lines.append(f'      <span class="timeline-category">{escape(entry.category)}</span>')
        lines.extend(['    </div>', '  </div>'])
    return "\n".join([*lines, '</div>'])


def nav_paths(value: object) -> set[str]:
    if isinstance(value, str):
        return {value}
    children = value.values() if isinstance(value, dict) else value
    return set().union(*(nav_paths(child) for child in children))


def extend_nav(nav: list, entries: list[Entry]) -> None:
    """Preserve curated order/labels; infer category identity from its paths."""
    for section, label in (("blog", "博客"), ("note", "笔记")):
        items = next(item[label] for item in nav if isinstance(item, dict) and label in item)
        known = nav_paths(items)
        groups = {}
        if section == "note":
            for item in items:
                if isinstance(item, dict):
                    for title, children in item.items():
                        for path in nav_paths(children):
                            parts = Path(path).parts
                            if len(parts) > 2 and parts[0] == "note":
                                groups[parts[1]] = children
                        groups.setdefault(title, children)
        missing = [e for e in entries if e.section == section and e.path.as_posix() not in known]
        if section == "blog":
            position = items.index("blog/index.md") + 1 if "blog/index.md" in items else 0
            items[position:position] = [e.path.as_posix() for e in missing]
        else:
            for entry in sorted(missing, key=lambda e: e.path.as_posix()):
                if not entry.category:
                    items.append(entry.path.as_posix())
                    continue
                if entry.category not in groups:
                    groups[entry.category] = []
                    items.append({entry.category: groups[entry.category]})
                groups[entry.category].append(entry.path.as_posix())


def render_nav(value: object, depth: int = 0) -> str:
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, dict):
        return "{" + ", ".join(f"{render_nav(k)} = {render_nav(v, depth)}" for k, v in value.items()) + "}"
    indent = "    " * (depth + 1)
    return "[\n" + "\n".join(f"{indent}{render_nav(item, depth + 1)}," for item in value) + "\n" + "    " * depth + "]"


def outputs(root: Path) -> dict[Path, str]:
    docs = root / "docs"
    entries = collect(docs)
    result = {}
    for section in SECTIONS:
        index = docs / section / "index.md"
        result[index] = replace_block(index.read_text(), "timeline", timeline_html([e for e in entries if e.section == section]))
    config = root / "zensical.toml"
    text = config.read_text()
    nav = tomllib.loads(text)["project"]["nav"]
    extend_nav(nav, entries)
    # Explicit markers avoid implementing a second TOML parser to find the array.
    begin, end = "# nav:auto-begin", "# nav:auto-end"
    if text.count(begin) != 1 or text.count(end) != 1 or text.index(begin) >= text.index(end):
        raise ValueError("Expected exactly one ordered navigation marker pair")
    start, stop = text.index(begin), text.index(end) + len(end)
    result[config] = text[:start] + f"{begin}\nnav = {render_nav(nav)}\n{end}" + text[stop:]
    tomllib.loads(result[config])  # validate before writing any outputs
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Report stale generated files without writing")
    args = parser.parse_args()
    changed = {p: text for p, text in outputs(ROOT).items() if p.read_text() != text}
    for path, text in changed.items():
        print(f'{"Stale" if args.check else "Updated"}: {path.relative_to(ROOT)}')
        if not args.check:
            path.write_text(text, encoding="utf-8")
    return int(args.check and bool(changed))


if __name__ == "__main__":
    raise SystemExit(main())
