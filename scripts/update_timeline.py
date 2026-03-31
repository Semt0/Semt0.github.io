#!/usr/bin/env python3
"""
自动更新 blog 和 note 首页的时间线布局。
扫描 docs/blog/ 和 docs/note/ 目录，按 frontmatter 的 date 字段排序，
生成时间线 HTML 并更新对应的 index.md 文件。
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date as date_cls
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS = REPO_ROOT / "docs"
BLOG_ROOT = DOCS / "blog"
NOTE_ROOT = DOCS / "note"

BLOG_INDEX = BLOG_ROOT / "index.md"
NOTE_INDEX = NOTE_ROOT / "index.md"

BLOG_MARKER_BEGIN = "<!-- timeline:auto-begin -->"
BLOG_MARKER_END = "<!-- timeline:auto-end -->"
NOTE_MARKER_BEGIN = "<!-- timeline:auto-begin -->"
NOTE_MARKER_END = "<!-- timeline:auto-end -->"


@dataclass(frozen=True, order=True)
class TimelineEntry:
    sort_date: date_cls
    mtime: float
    rel_from_docs: Path  # e.g. blog/2026-03-19.md or note/复变函数/xxx.md
    title: str
    category: Optional[str]  # 分类名（博客为 None）


def parse_frontmatter(raw: str) -> dict[str, str]:
    """解析简单 YAML frontmatter（仅收集 title / date 等单行键）。"""
    if not raw.startswith("---"):
        return {}
    m = re.match(r"^---\s*\r?\n([\s\S]*?)\r?\n---\s*\r?\n", raw)
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


def category_from_rel(rel: Path, root_name: str) -> Optional[str]:
    """从相对路径提取分类名。"""
    parts = rel.parts
    if len(parts) >= 2 and parts[0] == root_name:
        # 对于 note/复变函数/xxx.md，返回 "复变函数"
        # 对于 note/CVDL/ml_intro/xxx.md，返回 "CVDL"
        return parts[1]
    return None


def href_for_timeline(rel_from_docs: Path, is_blog: bool) -> str:
    """
    生成时间线中使用的链接。
    - 博客：相对于 blog/index.md，链接应为文章目录名（如 2026-03-19/）
    - 笔记：相对于 note/index.md，链接应为分类/文章目录名（如 复变函数/拉普拉斯变换/）
    """
    no_md = rel_from_docs.with_suffix("")
    parts = no_md.parts

    if is_blog:
        # blog/2026-03-19.md -> 2026-03-19/
        if len(parts) >= 2 and parts[0] == "blog":
            return parts[1] + "/"
    else:
        # note/复变函数/拉普拉斯变换.md -> 复变函数/拉普拉斯变换/
        if len(parts) >= 2 and parts[0] == "note":
            return "/".join(parts[1:]) + "/"

    return str(no_md) + "/"


def collect_entries(root: Path, root_name: str, is_blog: bool) -> list[TimelineEntry]:
    """收集指定目录下的所有笔记/博客条目。"""
    out: list[TimelineEntry] = []

    for path in sorted(root.rglob("*.md")):
        if path.name == "index.md":
            continue

        rel_docs = path.relative_to(DOCS)
        text = path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)

        ds = fm.get("date", "").strip()
        if not ds:
            continue

        try:
            y, m, d = (int(x) for x in ds.split("-")[:3])
            dt = date_cls(y, m, d)
        except (ValueError, TypeError):
            continue

        title = fm.get("title", "").strip() or path.stem
        cat = None if is_blog else category_from_rel(rel_docs, root_name)
        mtime = path.stat().st_mtime

        out.append(
            TimelineEntry(
                sort_date=dt,
                mtime=mtime,
                rel_from_docs=rel_docs,
                title=title,
                category=cat,
            )
        )

    return out


def build_timeline_html(entries: list[TimelineEntry], is_blog: bool) -> str:
    """构建时间线 HTML。"""
    lines: list[str] = []
    lines.append('<div class="timeline">')

    for e in entries:
        href = href_for_timeline(e.rel_from_docs, is_blog)
        dstr = e.sort_date.isoformat()

        lines.append('  <div class="timeline-item">')
        lines.append(f'    <div class="timeline-date">{dstr}</div>')
        lines.append('    <div class="timeline-content">')

        if is_blog:
            lines.append(f'      <a href="{href}">{_esc(e.title)}</a>')
        else:
            lines.append(f'      <a href="{href}">{_esc(e.title)}</a>')
            if e.category:
                lines.append(f'      <span class="timeline-category">{_esc(e.category)}</span>')

        lines.append('    </div>')
        lines.append('  </div>')

    lines.append('</div>')
    return "\n".join(lines)


def _esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def inject(content: str, block: str, marker_begin: str, marker_end: str) -> str:
    """将生成的 HTML 注入到标记之间。"""
    pattern = re.compile(
        re.escape(marker_begin) + r"[\s\S]*?" + re.escape(marker_end),
        re.MULTILINE,
    )
    if not pattern.search(content):
        raise SystemExit(
            f"未找到 {marker_begin} … {marker_end}，请先加入占位标记。"
        )
    replacement = f"{marker_begin}\n{block}\n{marker_end}"
    return pattern.sub(replacement, content, count=1)


def update_timeline(index_path: Path, root: Path, root_name: str, is_blog: bool) -> None:
    """更新时间线。"""
    if is_blog:
        marker_begin = BLOG_MARKER_BEGIN
        marker_end = BLOG_MARKER_END
    else:
        marker_begin = NOTE_MARKER_BEGIN
        marker_end = NOTE_MARKER_END

    entries = collect_entries(root, root_name, is_blog)
    # 按日期降序排列（最新的在前）
    entries.sort(key=lambda e: (e.sort_date, e.mtime, str(e.rel_from_docs)), reverse=True)

    if not entries:
        print(f"警告：{root} 下未找到带 date 的文件")
        return

    html = build_timeline_html(entries, is_blog)
    text = index_path.read_text(encoding="utf-8")
    new_text = inject(text, html, marker_begin, marker_end)
    index_path.write_text(new_text, encoding="utf-8", newline="\n")
    print(f"已更新 {index_path.relative_to(REPO_ROOT)}（{len(entries)} 条）")


def main() -> None:
    """主函数。"""
    print("更新博客时间线...")
    update_timeline(BLOG_INDEX, BLOG_ROOT, "blog", is_blog=True)

    print("更新笔记时间线...")
    update_timeline(NOTE_INDEX, NOTE_ROOT, "note", is_blog=False)

    print("\n时间线更新完成！")


if __name__ == "__main__":
    main()
