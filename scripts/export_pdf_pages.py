#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import fitz


def parse_page_spec(raw: str) -> tuple[int, str]:
    if ":" not in raw:
        raise argparse.ArgumentTypeError(
            f"无效的 --page 参数 `{raw}`，格式应为 `<页码>:<文件名.png>`"
        )

    page_text, filename = raw.split(":", 1)
    page_text = page_text.strip()
    filename = filename.strip()

    if not page_text.isdigit():
        raise argparse.ArgumentTypeError(
            f"无效页码 `{page_text}`，必须是正整数"
        )
    if not filename:
        raise argparse.ArgumentTypeError("输出文件名不能为空")
    if Path(filename).suffix.lower() != ".png":
        raise argparse.ArgumentTypeError("输出文件名必须以 .png 结尾")

    return int(page_text), filename


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="从 PDF 导出指定页面为高分辨率 PNG，写入笔记的 pictures 目录。"
    )
    parser.add_argument(
        "pdf",
        type=Path,
        help="PDF 文件路径，可使用绝对路径或相对仓库根目录的路径",
    )
    parser.add_argument(
        "out_dir",
        type=Path,
        help="输出目录，通常为 docs/note/<subject>/pictures",
    )
    parser.add_argument(
        "--page",
        dest="pages",
        action="append",
        required=True,
        type=parse_page_spec,
        help="导出规则，格式 `<页码>:<文件名.png>`；默认按 1-based 页码解释，可重复传入",
    )
    parser.add_argument(
        "--base",
        type=int,
        choices=(0, 1),
        default=1,
        help="输入页码的基准，默认 1；如需传 0-based 页码可设为 0",
    )
    parser.add_argument(
        "--zoom",
        type=float,
        default=6.0,
        help="导出倍率，默认 6.0；若原 PDF 质量差可尝试 8.0",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="允许覆盖已存在的同名文件",
    )
    return parser


def resolve_path(path: Path, repo_root: Path) -> Path:
    if path.is_absolute():
        return path
    return (repo_root / path).resolve()


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    pdf_path = resolve_path(args.pdf.expanduser(), repo_root)
    out_dir = resolve_path(args.out_dir.expanduser(), repo_root)

    if not pdf_path.exists():
        raise SystemExit(f"未找到 PDF: {pdf_path}")

    out_dir.mkdir(parents=True, exist_ok=True)
    matrix = fitz.Matrix(args.zoom, args.zoom)

    with fitz.open(pdf_path) as doc:
        total_pages = len(doc)
        for raw_page_no, filename in args.pages:
            page_index = raw_page_no if args.base == 0 else raw_page_no - 1
            if page_index < 0 or page_index >= total_pages:
                raise SystemExit(
                    f"页码超出范围: 输入={raw_page_no}, base={args.base}, PDF 总页数={total_pages}"
                )

            out_path = out_dir / filename
            if out_path.exists() and not args.overwrite:
                raise SystemExit(
                    f"目标文件已存在: {out_path}，如需覆盖请加 `--overwrite`"
                )

            pix = doc[page_index].get_pixmap(matrix=matrix, alpha=False)
            pix.save(out_path)
            print(
                f"exported page {raw_page_no} (index {page_index}) -> {out_path.relative_to(repo_root)}"
            )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
