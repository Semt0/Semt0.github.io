from __future__ import annotations

import re
from pathlib import Path


REPO = Path("/Users/semt0/blog/Semt0.github.io")
ZEN = REPO / "docs" / "blog" / "音乐与数学期末复习.md"
TYP = REPO / "docs" / "blog" / "音乐与数学期末复习.typora.md"


def normalize_emphasis(text: str) -> str:
    text = re.sub(r"\*\*\*\$(.+?)\$\*\*\*", r"$\1$", text)
    text = re.sub(r"\*\*\$(.+?)\$\*\*", r"$\1$", text)

    for _ in range(2):
        text = re.sub(r"\*\*\*(.+?)\*\*\*", lambda m: f"***{m.group(1).strip()}***", text)
        text = re.sub(r"\*\*(.+?)\*\*", lambda m: f"**{m.group(1).strip()}**", text)

    text = re.sub(r"(?m)^(\s*[-]|\s*\d+\.)\*\*", lambda m: f"{m.group(1)} **", text)
    return text


def normalize_phrasing(text: str) -> str:
    text = text.replace("***对比***-", "***对比*** -")
    text = text.replace("$$p_0$", "$p_0$")
    text = text.replace("$L_p=20\\log_{10}\\frac{p}{p_0}。$p_0$", "$L_p=20\\log_{10}\\frac{p}{p_0}$。$p_0$")
    text = re.sub(
        r"(\\$L_p=20\\\\log_{10}\\\\frac\\{p\\}/\\{p_0\\}\\$)\\s*\\$p_0\\$",
        r"\\1。$p_0$",
        text,
    )
    return text


def main() -> None:
    for path in (ZEN, TYP):
        text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
        text = normalize_emphasis(text)
        text = normalize_phrasing(text)
        text = re.sub(r"\n{3,}", "\n\n", text).rstrip() + "\n"
        path.write_text(text, encoding="utf-8")
        print(f"updated {path.relative_to(REPO)}")


if __name__ == "__main__":
    main()
