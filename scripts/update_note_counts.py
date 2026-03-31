#!/usr/bin/env python3
"""
自动更新 note 首页的栏目卡片数量统计。
扫描 docs/note/ 下的子目录，统计每个目录中的 Markdown 文件数量，
并更新 docs/note/index.md 中的卡片显示。
"""

import re
from pathlib import Path


def count_md_files(directory: Path) -> int:
    """统计目录中的 Markdown 文件数量（不包括 index.md）。"""
    return len(list(directory.glob("*.md")))


def get_note_categories(note_dir: Path) -> dict[str, int]:
    """
    获取所有笔记分类及其文章数量。
    遍历 docs/note/ 下的子目录，统计每个目录中的 .md 文件数量。
    """
    categories = {}

    for subdir in note_dir.iterdir():
        if subdir.is_dir() and not subdir.name.startswith("."):
            # 递归统计所有 .md 文件
            md_count = len(list(subdir.rglob("*.md")))
            if md_count > 0:
                categories[subdir.name] = md_count

    return categories


def update_index_md(index_path: Path, categories: dict[str, int]) -> bool:
    """
    更新 index.md 文件中的数量显示。
    使用正则表达式替换 <span class="nav-card__count">X 篇内容</span> 中的数字。
    """
    content = index_path.read_text(encoding="utf-8")
    original_content = content

    # 定义目录名到标题的映射（用于匹配卡片）
    dir_to_title = {
        "复变函数": "复变函数",
        "ODE": "常微分方程",
        "计算方法": "计算方法",
        "OJ复习": "OJ复习",
        "Introduction to Foundation Models": "Introduction to Foundation Models",
        "CVDL": "CVDL",
        "cs231n": "CS231n",
        "ai硬件": "AI硬件",
        "Rust程序设计": "Rust程序设计",
        "algorithm": "算法设计与分析",
    }

    # 为每个已知分类更新数量
    for dir_name, title in dir_to_title.items():
        if dir_name in categories:
            count = categories[dir_name]
            # 匹配对应标题的卡片，然后替换其数量
            # 模式：匹配 <a href="..."> 中包含特定标题的卡片
            pattern = rf'(<a href="[^"]*{re.escape(dir_name)}[^"]*" class="nav-card">\s*<span class="nav-card__title">{re.escape(title)}</span>\s*<span class="nav-card__count">)\d+( 篇内容</span>)'
            replacement = rf'\g<1>{count}\g<2>'
            content = re.sub(pattern, replacement, content)

    if content != original_content:
        index_path.write_text(content, encoding="utf-8")
        return True
    return False


def main():
    """主函数。"""
    repo_root = Path(__file__).parent.parent
    note_dir = repo_root / "docs" / "note"
    index_path = note_dir / "index.md"

    if not index_path.exists():
        print(f"Error: {index_path} not found")
        return 1

    # 获取各分类的文章数量
    categories = get_note_categories(note_dir)

    print("笔记分类统计：")
    for name, count in sorted(categories.items()):
        print(f"  {name}: {count} 篇")

    # 更新 index.md
    if update_index_md(index_path, categories):
        print(f"\n已更新 {index_path}")
    else:
        print(f"\n无需更新 {index_path}")

    return 0


if __name__ == "__main__":
    exit(main())
