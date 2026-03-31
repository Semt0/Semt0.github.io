#!/usr/bin/env python3
"""
根据笔记 frontmatter 的 date 字段，自动更新主页 Recent 区块（docs/index.md）。

默认取最新 5 篇；跳过 docs/note/index.md；无 date 的笔记不参与排序（可改为用文件mtime，当前跳过）。
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import date as date_cls
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS = REPO_ROOT / "docs"
INDEX_MD = DOCS / "index.md"
NOTE_ROOT = DOCS / "note"

MARKER_BEGIN = "<!-- home-recent:auto-begin -->"
MARKER_END = "<!-- home-recent:auto-end -->"


@dataclass(frozen=True, order=True)
class NoteEntry:
    sort_date: date_cls
    mtime: float  # 同日时优先最近修改
    rel_from_docs: Path  # e.g. note/foo/bar.md
    title: str
    category: str  # 分科目录名，用于 resume-card-sub


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


def category_from_rel(rel: Path) -> str:
    parts = rel.parts
    if len(parts) >= 3 and parts[0] == "note":
        return parts[1]
    return ""


def href_from_rel(rel: Path) -> str:
    """与现有主页一致：相对站点根的路径 + 尾部斜杠，段内保留空格。"""
    no_md = rel.with_suffix("")
    return str(no_md).replace("\\", "/") + "/"


def collect_notes() -> list[NoteEntry]:
    out: list[NoteEntry] = []
    for path in sorted(NOTE_ROOT.rglob("*.md")):
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
        cat = category_from_rel(rel_docs)
        mtime = path.stat().st_mtime
        out.append(
            NoteEntry(
                sort_date=dt,
                mtime=mtime,
                rel_from_docs=rel_docs,
                title=title,
                category=cat,
            )
        )
    return out


def build_cards_html(entries: list[NoteEntry]) -> str:
    lines: list[str] = []
    for e in entries:
        href = href_from_rel(e.rel_from_docs)
        dstr = e.sort_date.isoformat()
        sub = e.category or "笔记"
        lines.append(f'          <a class="resume-card" href="{href}">')
        lines.append('            <div class="resume-card-body">')
        lines.append(f'              <h3 class="resume-card-title">{_esc(e.title)}</h3>')
        lines.append(f'              <p class="resume-card-sub">{_esc(sub)}</p>')
        lines.append(f'              <span class="resume-card-date">{dstr}</span>')
        lines.append("            </div>")
        lines.append("          </a>")
    return "\n".join(lines)


def _esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def inject(content: str, block: str) -> str:
    pattern = re.compile(
        re.escape(MARKER_BEGIN) + r"[\s\S]*?" + re.escape(MARKER_END),
        re.MULTILINE,
    )
    if not pattern.search(content):
        raise SystemExit(
            f"在 {INDEX_MD} 中未找到 {MARKER_BEGIN} … {MARKER_END}，请先加入占位标记。"
        )
    replacement = f"{MARKER_BEGIN}\n{block}\n{MARKER_END}"
    return pattern.sub(replacement, content, count=1)


def main() -> None:
    ap = argparse.ArgumentParser(description="更新主页 Recent 区块")
    ap.add_argument(
        "--count",
        type=int,
        default=5,
        help="展示条数（默认 5）",
    )
    args = ap.parse_args()

    notes = collect_notes()
    notes.sort(key=lambda e: (e.sort_date, e.mtime, str(e.rel_from_docs)), reverse=True)
    top = notes[: args.count]

    if not top:
        raise SystemExit("未找到带 date 的笔记，无法生成 Recent。")

    html = build_cards_html(top)
    text = INDEX_MD.read_text(encoding="utf-8")
    new_text = inject(text, html)
    INDEX_MD.write_text(new_text, encoding="utf-8", newline="\n")
    print(f"已更新 {INDEX_MD.relative_to(REPO_ROOT)}（{len(top)} 条 Recent）")


if __name__ == "__main__":
    main()
