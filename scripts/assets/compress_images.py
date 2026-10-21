from __future__ import annotations

import argparse
import os
import tempfile
from pathlib import Path

from PIL import Image


def iter_images(root: Path) -> list[Path]:
    exts = {".png", ".jpg", ".jpeg", ".webp"}
    out: list[Path] = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() in exts:
            out.append(p)
    return sorted(out)


def _alpha_is_opaque(img: Image.Image) -> bool:
    if img.mode == "RGBA":
        lo, hi = img.getchannel("A").getextrema()
        return lo == 255 and hi == 255
    if img.mode == "LA":
        lo, hi = img.getchannel("A").getextrema()
        return lo == 255 and hi == 255
    return True


def _save_png(img: Image.Image, out_path: Path) -> None:
    img.save(out_path, format="PNG", optimize=True, compress_level=9)


def _save_jpeg(img: Image.Image, out_path: Path, quality: int) -> None:
    img.save(out_path, format="JPEG", quality=quality, optimize=True, progressive=True)


def _save_webp(img: Image.Image, out_path: Path, quality: int) -> None:
    img.save(out_path, format="WEBP", quality=quality, method=6)


def compress_one(
    path: Path,
    max_bytes: int,
    max_width: int,
    min_width: int,
    min_quality: int,
) -> tuple[bool, int, int]:
    before = path.stat().st_size
    if before <= max_bytes:
        return False, before, before

    with Image.open(path) as img0:
        img = img0.copy()

    if img.mode in ("RGBA", "LA") and _alpha_is_opaque(img):
        img = img.convert("RGB")

    ext = path.suffix.lower()

    def write_tmp(save_fn) -> int:
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            tmp_path = Path(tmp.name)
        try:
            save_fn(tmp_path)
            size = tmp_path.stat().st_size
            os.replace(tmp_path, path)
            return size
        finally:
            if tmp_path.exists():
                tmp_path.unlink(missing_ok=True)

    def resize_to(width: int) -> Image.Image:
        if img.width <= width:
            return img
        h = int(round(img.height * (width / img.width)))
        return img.resize((width, h), Image.Resampling.LANCZOS)

    widths: list[int] = []
    w = min(img.width, max_width)
    while w >= min_width:
        widths.append(w)
        w = int(w * 0.85)
        if w == widths[-1]:
            break

    if ext in (".jpg", ".jpeg"):
        qualities = list(range(90, min_quality - 1, -5))
        for width in widths:
            img_r = resize_to(width)
            for q in qualities:
                after = write_tmp(lambda p: _save_jpeg(img_r, p, q))
                if after <= max_bytes:
                    return True, before, after
        return True, before, path.stat().st_size

    if ext == ".webp":
        qualities = list(range(85, min_quality - 1, -5))
        for width in widths:
            img_r = resize_to(width)
            for q in qualities:
                after = write_tmp(lambda p: _save_webp(img_r, p, q))
                if after <= max_bytes:
                    return True, before, after
        return True, before, path.stat().st_size

    for width in widths:
        img_r = resize_to(width)
        after = write_tmp(lambda p: _save_png(img_r, p))
        if after <= max_bytes:
            return True, before, after

        if img_r.mode == "RGB":
            for colors in (256, 128, 64):
                img_q = img_r.convert("P", palette=Image.Palette.ADAPTIVE, colors=colors)
                after2 = write_tmp(lambda p: _save_png(img_q, p))
                if after2 <= max_bytes:
                    return True, before, after2

    return True, before, path.stat().st_size


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", type=str)
    parser.add_argument("--max-bytes", type=int, default=1_000_000)
    parser.add_argument("--max-width", type=int, default=1600)
    parser.add_argument("--min-width", type=int, default=900)
    parser.add_argument("--min-quality", type=int, default=50)
    args = parser.parse_args()

    root = Path(args.dir).expanduser().resolve()
    paths = iter_images(root)
    changed = 0
    still_over = 0
    total_before = 0
    total_after = 0

    for p in paths:
        before = p.stat().st_size
        total_before += before
        did, b, a = compress_one(
            p,
            max_bytes=args.max_bytes,
            max_width=args.max_width,
            min_width=args.min_width,
            min_quality=args.min_quality,
        )
        total_after += a
        if did:
            changed += 1
        if p.stat().st_size > args.max_bytes:
            still_over += 1

    print(f"dir={root}")
    print(f"images={len(paths)} changed={changed} still_over={still_over}")
    print(f"bytes_before={total_before} bytes_after={total_after}")


if __name__ == "__main__":
    main()

