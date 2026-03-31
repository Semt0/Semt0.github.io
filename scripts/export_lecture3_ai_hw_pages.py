#!/usr/bin/env python3
"""从 Lecture3_2026_spring.pdf 导出指定页为 PNG，供数字逻辑与计算单元设计笔记使用。"""
from pathlib import Path

import fitz

PDF_PATH = Path.home() / "Downloads" / "Lecture3_2026_spring.pdf"
OUT_DIR = Path(__file__).resolve().parent.parent / "docs" / "note" / "ai硬件" / "pictures"

# 文件名 -> PDF 页码（0-based）
PAGE_MAP = {
    "lec3_05_pun_pdn.png": 4,          # PUN和PDN结构图
    "lec3_06_nand.png": 5,             # NAND门电路及真值表
    "lec3_07_complex_logic.png": 6,    # 复杂静态逻辑电路 F=D+(A(B+C))
    "lec3_08_adder_truth.png": 7,      # 1-bit全加器真值表和公式
    "lec3_09_adder_circuit.png": 8,    # 1-bit全加器晶体管电路
    "lec3_11_inverter_delay.png": 10,  # 反相器延迟
    "lec3_12_rc_delay.png": 11,        # 一阶RC延迟分析
    "lec3_13_inverter_rc.png": 12,     # 反相器RC延迟
    "lec3_15_input_pattern.png": 14,   # 输入Pattern对延迟的影响
    "lec3_16_transistor_order.png": 15, # Transistor Ordering
    "lec3_17_elmore.png": 16,          # Elmore Delay模型
    "lec3_18_sizing.png": 17,          # Transistor Sizing
    "lec3_19_power.png": 18,           # 逻辑电路功耗
    "lec3_20_power_detail.png": 19,    # 功耗充放电详细
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
