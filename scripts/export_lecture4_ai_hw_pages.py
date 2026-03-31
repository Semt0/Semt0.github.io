#!/usr/bin/env python3
"""从 Lecture3_2026_spring (1).pdf (第四讲) 导出指定页为 PNG，供复杂计算单元与指令集笔记使用。"""
from pathlib import Path

import fitz

PDF_PATH = Path.home() / "Downloads" / "Lecture3_2026_spring (1).pdf"
OUT_DIR = Path(__file__).resolve().parent.parent / "docs" / "note" / "ai硬件" / "pictures"

# 文件名 -> PDF 页码（0-based）
PAGE_MAP = {
    "lec4_12_adder_circuit.png": 11,        # 1-bit加法器晶体管电路
    "lec4_13_ripple_carry.png": 12,          # Ripple Carry加法器
    "lec4_14_pgk.png": 13,                   # PGK加法器方法
    "lec4_15_carry_ripple_pg.png": 14,       # Carry-Ripple using P and G
    "lec4_16_pg_cells.png": 15,              # PG生成逻辑和Carry Ripple PG图
    "lec4_17_pg_tree.png": 16,               # 复杂PG树加法器 Kogge-Stone
    "lec4_18_pg_variants.png": 17,           # Brent-Kung, Sklansky, Han-Carlson
    "lec4_19_mult_basic.png": 18,            # 乘法器基本原理
    "lec4_20_mult_dot.png": 19,              # 乘法器dot diagram
    "lec4_21_mult_array.png": 20,            # 阵列乘法器 CSA/CPA
    "lec4_22_radix_encoding.png": 21,        # Radix编码
    "lec4_25_booth.png": 24,                 # 布斯编码表
    "lec4_26_booth_example1.png": 25,        # 布斯编码例1
    "lec4_27_booth_example2.png": 26,        # 布斯编码例2
    "lec4_28_barrel_shifter.png": 27,        # Barrel Shifter
    "lec4_29_conv_intro.png": 28,            # 卷积介绍
    "lec4_30_winograd_1d.png": 29,           # 1D Winograd
    "lec4_31_winograd_matrix.png": 30,       # Winograd矩阵形式
    "lec4_32_winograd_complexity.png": 31,   # Winograd复杂度分析
    "lec4_33_winograd_steps.png": 32,        # Winograd 4步
    "lec4_34_winograd_2d.png": 33,           # 2D Winograd
    "lec4_35_winograd_2d_detail.png": 34,    # 2D Winograd详细
    "lec4_36_winograd_nvdla.png": 35,        # NVDLA Winograd
    "lec4_37_cordic_rotation.png": 36,       # CORDIC旋转原理
    "lec4_38_cordic_pseudo.png": 37,         # CORDIC伪旋转
    "lec4_39_cordic_angles.png": 38,         # CORDIC角度选择
    "lec4_40_cordic_table.png": 39,          # CORDIC迭代表
    "lec4_41_cordic_iter.png": 40,           # CORDIC迭代公式
    "lec4_42_cordic_scaling.png": 41,        # CORDIC Scaling Factor
    "lec4_43_cordic_hw.png": 42,             # CORDIC硬件架构
    "lec4_45_fsm.png": 44,                   # 状态机结构
    "lec4_48_fsm_traffic.png": 47,           # 红绿灯状态转换表和电路
    "lec4_49_fsm_circuit.png": 48,           # 红绿灯电路实现
    "lec4_51_timing_why.png": 50,            # 为什么需要时钟
    "lec4_52_timing_setup.png": 51,          # Setup/Hold Time
    "lec4_53_timing_metrics.png": 52,        # Timing Metrics
    "lec4_54_timing_skew.png": 53,           # Clock Skew/Jitter
    "lec4_56_isa_layers.png": 55,            # ISA层次图
    "lec4_58_cisc_risc.png": 57,             # CISC vs RISC
    "lec4_61_von_neumann.png": 60,           # 冯诺依曼架构
    "lec4_62_processor.png": 61,             # 处理器结构
    "lec4_65_register_no.png": 64,           # 无寄存器9次访存
    "lec4_66_register_yes.png": 65,          # 有寄存器3次访存
    "lec4_68_isa_flow.png": 67,              # 指令集操作流程
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
