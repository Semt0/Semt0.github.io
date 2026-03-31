#!/usr/bin/env python3
"""导出 Rust程序设计 第03章(所有权与所有权转移) 关键页面到笔记图片目录。"""
from pathlib import Path

import fitz

PDF_PATH = Path.home() / "Downloads" / "第03章 - 所有权与所有权转移.pdf"
OUT_DIR = Path(__file__).resolve().parent.parent / "docs" / "note" / "Rust程序设计" / "pictures"

# 文件名 -> PDF 0-based 页码
PAGE_MAP = {
    "ch03_01_cpp_string_memory.png": 3,
    "ch03_02_rust_string_memory.png": 6,
    "ch03_03_vec_string_memory.png": 8,
    "ch03_04_python_shared_ref.png": 14,
    "ch03_05_cpp_deep_copy.png": 17,
    "ch03_06_rust_move.png": 21,
    "ch03_07_comparison_table.png": 24,
    "ch03_08_rc_ref_count.png": 48,
    "ch03_09_rc_drop.png": 51,
}


def main() -> int:
    if not PDF_PATH.exists():
        print(f"未找到 PDF: {PDF_PATH}")
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(PDF_PATH)

    for name, page_index in PAGE_MAP.items():
        if page_index < 0 or page_index >= len(doc):
            print(f"跳过 {name}: 页码超出范围")
            continue
        page = doc[page_index]
        pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0), alpha=False)
        out_path = OUT_DIR / name
        pix.save(str(out_path))
        print(f"已导出: {name} (Slide {page_index + 1})")

    doc.close()
    print(f"\n完成：共导出 {len(PAGE_MAP)} 张图片到 {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
