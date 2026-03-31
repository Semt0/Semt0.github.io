#!/usr/bin/env python3
"""从 lecture_2.pdf 导出指定页为 PNG，供 CS231n Lecture 2 笔记使用。"""
from pathlib import Path

import fitz

PDF_PATH = Path.home() / "Downloads" / "lecture_2.pdf"
OUT_DIR = Path(__file__).resolve().parent.parent / "docs" / "note" / "cs231n" / "pictures"

# 文件名 -> PDF 页码（0-based）
PAGE_MAP = {
    "01_semantic_gap.png": 7,              # Slide 8: semantic gap - cat pixel values
    "02_challenges.png": 8,                # Slide 9: viewpoint variation
    "03_data_driven.png": 18,              # Slide 19: data-driven approach
    "04_l1_distance.png": 22,              # Slide 23: L1 distance example
    "05_knn_decision_boundary.png": 29,    # Slide 30: KNN K=1,3,5
    "06_l1_vs_l2.png": 30,                 # Slide 31: L1 vs L2 distance shapes
    "07_hyperparameter_setting.png": 39,   # Slide 40: train/val/test split
    "08_cross_validation.png": 40,         # Slide 41: cross-validation folds
    "09_parametric_approach.png": 52,      # Slide 53: f(x,W) = Wx + b with dimensions
    "10_algebraic_example.png": 57,        # Slide 58: algebraic viewpoint example
    "11_visual_viewpoint.png": 59,         # Slide 60: learned weight templates
    "12_geometric_viewpoint.png": 60,      # Slide 61: geometric viewpoint
    "13_hard_cases.png": 61,               # Slide 62: hard cases for linear classifier
    "14_softmax_computation.png": 73,      # Slide 74: softmax full pipeline
    "15_svm_hinge_loss.png": 86,           # Slide 87: hinge loss shape
    "16_softmax_vs_svm.png": 98,           # Slide 99: softmax vs SVM side by side
}


def main():
    if not PDF_PATH.exists():
        print(f"未找到 PDF: {PDF_PATH}")
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(PDF_PATH)

    for name, page_no in PAGE_MAP.items():
        if page_no >= len(doc):
            print(f"跳过 {name}: 页码 {page_no} 超出范围 (共 {len(doc)} 页)")
            continue
        page = doc[page_no]
        mat = fitz.Matrix(2.0, 2.0)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        out_path = OUT_DIR / name
        pix.save(str(out_path))
        print(f"已导出: {out_path.name} (Slide {page_no + 1})")

    doc.close()
    print(f"\n共导出 {len(PAGE_MAP)} 张图到 {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
