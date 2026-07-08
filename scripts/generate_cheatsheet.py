#!/usr/bin/env python3
"""
Generate a dense A4 4-column cheatsheet PDF using Pandoc + XeLaTeX.

The layout follows the Cheatsheet-Template style:
  https://github.com/zhuozhiyongde/Cheatsheet-Template

Usage:
    python scripts/generate_cheatsheet.py <input.json> <output.pdf>
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = SCRIPT_DIR / "cheatsheet_template"


def parse_data(raw: dict) -> list[dict]:
    """Normalize the JSON data structure."""
    sections: list[dict] = []
    for sec in raw.get("sections", []):
        subsections: list[dict] = []
        for sub in sec.get("subsections", []):
            items = sub.get("items", [])
            if isinstance(items, str):
                items = [items]
            subsections.append({"title": sub.get("title", ""), "items": items})
        sections.append({"title": sec.get("title", ""), "subsections": subsections})
    return sections


def format_item(item: str) -> str:
    """
    Convert a raw item into the 'bold phrase + description' style.

    Rules:
    - If the item contains ':' or '：', bold the part before the separator.
    - Otherwise bold the whole item so the term/concept stands out.
    """
    item = item.strip()
    if not item:
        return ""

    # Prefer full-width colon first, then half-width colon.
    for sep in ("：", ":"):
        if sep in item:
            phrase, _, rest = item.partition(sep)
            phrase = phrase.strip()
            rest = rest.strip()
            if phrase and rest:
                return f"**{phrase}**{sep} {rest}"
            break

    return f"**{item}**"


def json_to_markdown(data: dict) -> str:
    """Convert cheatsheet JSON to Markdown suitable for the LaTeX template."""
    sections = parse_data(data)
    lines: list[str] = []

    for sec in sections:
        if sec["title"]:
            lines.append(f"# {sec['title']}")
            lines.append("")

        for sub in sec["subsections"]:
            if sub["title"]:
                lines.append(f"## {sub['title']}")
                lines.append("")

            for item in sub["items"]:
                if isinstance(item, str):
                    for line in item.splitlines():
                        formatted = format_item(line)
                        if formatted:
                            lines.append(formatted)
                            lines.append("")
                else:
                    formatted = format_item(str(item))
                    if formatted:
                        lines.append(formatted)
                        lines.append("")

            lines.append("")

    return "\n".join(lines)


def generate_pdf(input_path: Path, output_path: Path) -> None:
    raw = json.loads(input_path.read_text(encoding="utf-8"))
    title = raw.get("title", "Cheatsheet")
    md_content = json_to_markdown(raw)

    if not shutil.which("pandoc"):
        raise RuntimeError("pandoc is not installed or not in PATH")
    if not shutil.which("xelatex"):
        raise RuntimeError("xelatex is not installed or not in PATH")

    with tempfile.TemporaryDirectory(prefix="cheatsheet_") as tmpdir:
        tmp = Path(tmpdir)
        md_file = tmp / "cheatsheet.md"
        tex_file = tmp / "cheatsheet.tex"
        md_file.write_text(md_content, encoding="utf-8")

        # Prepare a temporary before-body snippet with the title substituted.
        before_body_src = (TEMPLATE_DIR / "before_body.tex").read_text(encoding="utf-8")
        before_body_file = tmp / "before_body.tex"
        before_body_file.write_text(before_body_src.replace("$title$", title), encoding="utf-8")

        # Markdown -> LaTeX via Pandoc, injecting the template snippets.
        subprocess.run(
            [
                "pandoc",
                str(md_file),
                "--from",
                "markdown-raw_tex",
                "-o",
                str(tex_file),
                "--variable=documentclass:extarticle",
                "--variable=classoption:8pt",
                "-H",
                str(TEMPLATE_DIR / "preamble.tex"),
                "-B",
                str(before_body_file),
                "-A",
                str(TEMPLATE_DIR / "after_body.tex"),
            ],
            check=True,
        )

        # LaTeX -> PDF (run twice for stable references).
        for _ in range(2):
            subprocess.run(
                [
                    "xelatex",
                    "-interaction=nonstopmode",
                    "-output-directory",
                    str(tmpdir),
                    str(tex_file),
                ],
                check=True,
                capture_output=True,
            )

        generated_pdf = tmp / "cheatsheet.pdf"
        if not generated_pdf.exists():
            raise RuntimeError("xelatex did not produce a PDF file")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(generated_pdf), str(output_path))

    print(f"Wrote cheatsheet to {output_path}")


def main() -> None:
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <input.json> <output.pdf>")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    generate_pdf(input_path, output_path)


if __name__ == "__main__":
    main()
