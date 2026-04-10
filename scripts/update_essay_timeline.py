#!/usr/bin/env python3
"""
自动更新 essay 首页的时间线布局。

扫描 docs/essay/ 目录下的手记文件（通常为 YYYY-MM-DD.md），按 frontmatter 的 date
字段排序（若缺失则回退使用文件名日期），生成时间线 HTML 并更新 docs/essay/index.md。
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date as date_cls
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS = REPO_ROOT / "docs"
ESSAY_ROOT = DOCS / "essay"
ESSAY_INDEX = ESSAY_ROOT / "index.md"

MARKER_BEGIN = "<!-- timeline:auto-begin -->"
MARKER_END = "<!-- timeline:auto-end -->"


@dataclass(frozen=True, order=True)
class TimelineEntry:
    sort_date: date_cls
    mtime: float
    rel_from_docs: Path
    title: str


def parse_frontmatter(raw: str) -> dict[str, str]:
    raw = raw.lstrip("\ufeff").strip()
    if not raw.startswith("---"):
        return {}
    m = re.match(r"^---\s*\n([\s\S]*?)\n---\s*(\n|$)", raw)
    if not m:
        m = re.match(r"^---\s*[\r\n]+([\s\S]*?)[\r\n]+---\s*([\r\n]|$)", raw)
        if not m:
            return {}
    block = m.group(1)
    data: dict[str, str] = {}
    for line in block.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, rest = line.partition(":")
        key = key.strip()
        val = rest.strip()
        if val.startswith('"') and val.endswith('"'):
            val = val[1:-1]
        elif val.startswith("'") and val.endswith("'"):
            val = val[1:-1]
        if key in ("title", "date"):
            data[key] = val
    return data


def parse_date_str(ds: str) -> date_cls | None:
    ds = ds.strip()
    if not ds:
        return None
    try:
        y, m, d = (int(x) for x in ds.split("-")[:3])
        return date_cls(y, m, d)
    except (ValueError, TypeError):
        return None


def href_for_timeline(rel_from_docs: Path) -> str:
    no_md = rel_from_docs.with_suffix("")
    parts = no_md.parts
    if len(parts) >= 2 and parts[0] == "essay":
        return "/".join(parts[1:]) + "/"
    return str(no_md) + "/"


def extract_first_heading_title(raw: str) -> str | None:
    in_code = False
    for line in raw.splitlines():
        s = line.rstrip()
        if s.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = re.match(r"^\s*#{1,6}\s+(.*)\s*$", s)
        if not m:
            continue
        title = m.group(1).strip()
        if title:
            return title
    return None



def collect_entries() -> list[TimelineEntry]:
    out: list[TimelineEntry] = []

    for path in sorted(ESSAY_ROOT.rglob("*.md")):
        if path.name == "index.md":
            continue

        rel_docs = path.relative_to(DOCS)
        text = path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)

        dt = parse_date_str(fm.get("date", ""))
        if dt is None:
            dt = parse_date_str(path.stem)
        if dt is None:
            continue

        title = (fm.get("title", "") or "").strip()
        if not title:
            title = extract_first_heading_title(text) or path.stem
        mtime = path.stat().st_mtime

        out.append(
            TimelineEntry(
                sort_date=dt,
                mtime=mtime,
                rel_from_docs=rel_docs,
                title=title,
            )
        )

    return out


def _esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def build_timeline_html(entries: list[TimelineEntry]) -> str:
    lines: list[str] = []
    lines.append('<div class="timeline">')

    for e in entries:
        href = href_for_timeline(e.rel_from_docs)
        dstr = e.sort_date.isoformat()

        lines.append('  <div class="timeline-item">')
        lines.append(f'    <div class="timeline-date">{dstr}</div>')
        lines.append('    <div class="timeline-content">')
        lines.append(f'      <a href="{href}">{_esc(e.title)}</a>')
        lines.append("    </div>")
        lines.append("  </div>")

    lines.append("</div>")
    return "\n".join(lines)


def inject(content: str, block: str) -> str:
    pattern = re.compile(
        re.escape(MARKER_BEGIN) + r"[\s\S]*?" + re.escape(MARKER_END),
        re.MULTILINE,
    )
    if not pattern.search(content):
        raise SystemExit(f"未找到 {MARKER_BEGIN} … {MARKER_END}，请先加入占位标记。")
    replacement = f"{MARKER_BEGIN}\n{block}\n{MARKER_END}"
    return pattern.sub(replacement, content, count=1)


def main() -> None:
    entries = collect_entries()
    entries.sort(key=lambda e: (e.sort_date, e.mtime, str(e.rel_from_docs)), reverse=True)
    if not entries:
        print(f"警告：{ESSAY_ROOT} 下未找到可用条目")
        return

    html = build_timeline_html(entries)
    text = ESSAY_INDEX.read_text(encoding="utf-8")
    new_text = inject(text, html)
    ESSAY_INDEX.write_text(new_text, encoding="utf-8", newline="\n")
    print(f"已更新 {ESSAY_INDEX.relative_to(REPO_ROOT)}（{len(entries)} 条）")


if __name__ == "__main__":
    main()
