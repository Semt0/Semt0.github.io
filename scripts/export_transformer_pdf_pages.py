#!/usr/bin/env python3
"""从 04_transformer.pdf 导出指定页为 PNG，供 Transformer 笔记使用。"""
from pathlib import Path

import fitz

# PDF 路径（请按实际位置修改）
PDF_PATH = Path.home() / "Downloads" / "04_transformer.pdf"
# 输出目录（相对项目根目录下的笔记 pictures）
OUT_DIR = Path(__file__).resolve().parent.parent / "docs" / "note" / "LLM" / "pictures"

# 文件名 -> PDF 页码（0-based，与课件 “Slide N” 对应为 page N-1）
PAGE_MAP = {
    "01_seq2seq_encoder_decoder.png": 6,   # Slide 7: Training NMT
    "02_rnn_bottleneck.png": 10,             # Slide 11: bottleneck
    "03_attention_weighted_avg.png": 15,    # Slide 16: weighted averaging
    "04_seq2seq_attention.png": 19,         # Slide 20: seq2seq with attention
    "05_self_attention_example.png": 34,     # Slide 35: self-attention example
    "06_self_attention_matrix.png": 37,     # Slide 38: matrix representation
    "07_position_embedding.png": 46,        # Slide 47: position embedding
    "08_multi_head_attention.png": 55,       # Slide 56: multi-head
    "09_residual_connection.png": 59,       # Slide 60: residual
    "10_transformer_encoder.png": 62,       # Slide 63: encoder
    "11_transformer_decoder.png": 61,       # Slide 62: decoder
    "12_cross_attention.png": 65,            # Slide 66: cross attention
    "13_transformer_full.png": 63,          # Slide 64: full transformer
    "14_quadratic_complexity.png": 69,       # Slide 70: quadratic
}


def main():
    if not PDF_PATH.exists():
        print(f"未找到 PDF: {PDF_PATH}")
        print("请将 04_transformer.pdf 放在 Downloads 目录，或修改本脚本中的 PDF_PATH")
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(PDF_PATH)

    for name, page_no in PAGE_MAP.items():
        if page_no >= len(doc):
            print(f"跳过 {name}: 页码 {page_no} 超出范围 (共 {len(doc)} 页)")
            continue
        page = doc[page_no]
        # 2x 缩放以提高清晰度
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
