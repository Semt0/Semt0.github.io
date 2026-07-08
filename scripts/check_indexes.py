#!/usr/bin/env python3
"""
检查项目目录索引结构。

- 确认必须存在 README.md 的目录都有 README.md
- 检查 README.md 是否包含关键节标题
- 报告超过 300 行的索引文件
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Agent 索引根目录：README.md 不再放在 docs/ 下渲染，而是集中放在 .claude/indexes/
# 以保证站点构建时 index.md 作为人读页面，README.md 仅作为 Agent 索引。
INDEXES_ROOT = REPO_ROOT / ".claude" / "indexes"

# 必须存在 README.md 的目录（相对 INDEXES_ROOT）
REQUIRED_DOCS_INDEX_DIRS = [
    "docs",
    "docs/blog",
    "docs/essay",
    "docs/note",
    "docs/stylesheets",
    "docs/javascripts",
    "docs/images",
]

REQUIRED_DIRS = REQUIRED_DOCS_INDEX_DIRS + [
    "scripts",
    "tests",
]

# 需要检查行数是否超限的索引文件（相对仓库根目录）
INDEX_FILES = [
    "CLAUDE.md",
    "CLAUDE/08-extension.md",
    "README.md",
    ".claude/indexes/docs/README.md",
    ".claude/indexes/docs/blog/README.md",
    ".claude/indexes/docs/essay/README.md",
    ".claude/indexes/docs/note/README.md",
    ".claude/indexes/docs/stylesheets/README.md",
    ".claude/indexes/docs/javascripts/README.md",
    ".claude/indexes/docs/images/README.md",
    "scripts/README.md",
    "tests/README.md",
    "overrides/README.md",
]

# README.md 必须包含的关键节标题
REQUIRED_SECTIONS = [
    "## 1 用途",
    "## 2 内容清单",
    "## 3 规则与约定",
    "## 5 扩展指南",
]

LINE_LIMIT = 300


def collect_subject_readmes() -> list[str]:
    """自动收集 docs/note/<subject>/README.md（Agent 索引位置）。"""
    note_root = INDEXES_ROOT / "docs" / "note"
    paths: list[str] = []
    if note_root.exists():
        for d in sorted(note_root.iterdir()):
            if d.is_dir() and not d.name.startswith(".") and not d.name.startswith("_"):
                readme = d / "README.md"
                if readme.exists():
                    paths.append(str(readme.relative_to(REPO_ROOT)))
    return paths


def _readme_path(rel: str) -> Path:
    """返回某个 REQUIRED_DIR 对应的 README.md 路径。"""
    if rel.startswith("docs/") or rel == "docs":
        return INDEXES_ROOT / rel / "README.md"
    return REPO_ROOT / rel / "README.md"


def check_required_readmes() -> list[str]:
    """检查必须目录是否都有 README.md。"""
    errors: list[str] = []
    for rel in REQUIRED_DIRS:
        readme = _readme_path(rel)
        if not readme.exists():
            errors.append(f"缺失 README.md: {readme.relative_to(REPO_ROOT)}")
    return errors


def check_readme_sections() -> list[str]:
    """检查 README.md 是否包含关键节标题。"""
    errors: list[str] = []
    for rel in REQUIRED_DIRS:
        readme = _readme_path(rel)
        if not readme.exists():
            continue
        text = readme.read_text(encoding="utf-8")
        for section in REQUIRED_SECTIONS:
            if section not in text:
                errors.append(
                    f"{readme.relative_to(REPO_ROOT)} 缺少关键节：{section}"
                )
    return errors


def check_oversized_indexes(index_files: list[str]) -> list[str]:
    """检查索引文件是否超过行数限制。"""
    warnings: list[str] = []
    for rel in index_files:
        path = REPO_ROOT / rel
        if not path.exists():
            continue
        lines = path.read_text(encoding="utf-8").count("\n") + 1
        if lines > LINE_LIMIT:
            warnings.append(
                f"索引文件超过 {LINE_LIMIT} 行（{lines} 行）: {rel}"
                f" — 建议按树形分解约定拆分"
            )
    return warnings


def main() -> int:
    subject_readmes = collect_subject_readmes()
    all_index_files = sorted(set(INDEX_FILES + subject_readmes))

    errors = check_required_readmes()
    errors += check_readme_sections()
    warnings = check_oversized_indexes(all_index_files)

    print("=" * 60)
    print("目录索引结构检查")
    print("=" * 60)

    if errors:
        print("\n❌ 错误：")
        for e in errors:
            print(f"  - {e}")
    else:
        print("\n✅ 所有必须目录都存在 README.md，且包含关键节标题。")

    if warnings:
        print("\n⚠️  警告：")
        for w in warnings:
            print(f"  - {w}")
    else:
        print(f"\n✅ 所有索引文件均未超过 {LINE_LIMIT} 行。")

    print(f"\n共检查 {len(REQUIRED_DIRS)} 个必须目录、{len(all_index_files)} 个索引文件。")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
