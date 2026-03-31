#!/usr/bin/env python3
"""导出 Lecture04(解线性方程组的直接法) 关键页面到笔记图片目录。"""
from pathlib import Path

import fitz

PDF_PATH = Path.home() / "Downloads" / "计算方法_00330050_Lecture04_解线性方程组的直接法.pdf"
OUT_DIR = Path(__file__).resolve().parent.parent / "docs" / "note" / "计算方法" / "pictures"

# 文件名 -> PDF 0-based 页码
PAGE_MAP = {
    "lecture04_01_cover.png": 0,
    "lecture04_02_ill_conditioned_example.png": 6,
    "lecture04_03_vector_norms.png": 11,
    "lecture04_04_matrix_norms.png": 16,
    "lecture04_05_error_analysis.png": 22,
    "lecture04_06_condition_number.png": 25,
    "lecture04_07_cond_estimation.png": 32,
    "lecture04_08_cond_distance.png": 36,
    "lecture04_09_overdetermined.png": 39,
    "lecture04_10_least_squares_objective.png": 41,
    "lecture04_11_normal_equation.png": 42,
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
