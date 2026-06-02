from __future__ import annotations

import re
from pathlib import Path


REPO = Path("/Users/semt0/blog/Semt0.github.io")
ZEN_PATH = REPO / "docs" / "blog" / "音乐与数学期末复习.md"
TYPORA_PATH = REPO / "docs" / "blog" / "音乐与数学期末复习.typora.md"


def normalize_emphasis(text: str) -> str:
    text = re.sub(
        r"\*\*\*(.*?)\*\*\*",
        lambda m: f"***{m.group(1).strip()}***",
        text,
    )
    text = re.sub(
        r"\*\*(.*?)\*\*",
        lambda m: f"**{m.group(1).strip()}**",
        text,
    )

    # Add a space before/after emphasis when directly glued to text.
    token = r"(\*\*\*[^*\n]+\*\*\*|\*\*[^*\n]+\*\*)"
    text = re.sub(rf"([\u4e00-\u9fffA-Za-z0-9]){token}", r"\1 \2", text)
    text = re.sub(rf"{token}([\u4e00-\u9fffA-Za-z0-9])", r"\1 \2", text)
    text = re.sub(r"(?m)^(\s*[-]|\s*\d+\.)\*\*", r"\1 **", text)
    text = re.sub(r"(?m)^(>\s*[-]?)\*\*", r"\1 **", text)
    return text


def normalize_emphasis_v2(text: str) -> str:
    def strip_triple(s: str) -> str:
        return re.sub(r"\*\*\*(.+?)\*\*\*", lambda m: f"***{m.group(1).strip()}***", s)

    def strip_double(s: str) -> str:
        return re.sub(r"\*\*(.+?)\*\*", lambda m: f"**{m.group(1).strip()}**", s)

    for _ in range(2):
        text = strip_triple(text)
        text = strip_double(text)

    token = r"(\*\*\*[^*\n]+\*\*\*|\*\*[^*\n]+\*\*)"
    text = re.sub(rf"([\u4e00-\u9fffA-Za-z0-9]){token}", r"\1 \2", text)
    text = re.sub(rf"{token}([\u4e00-\u9fffA-Za-z0-9])", r"\1 \2", text)
    text = re.sub(r"(?m)^(\s*[-]|\s*\d+\.)\*\*", r"\1 **", text)
    text = re.sub(r"(?m)^(>\s*[-]?)\*\*", r"\1 **", text)
    return text


def normalize_inline_formulas(text: str) -> str:
    text = re.sub(r"^(\s*\d+\.\s+)\*\*\$(.+?)\$\*\*\s*$", r"\1$\2$", text, flags=re.M)
    text = re.sub(r"^(\s*\d+\.\s+)\$\$(.+?)\$\$\s*$", r"\1$\2$", text, flags=re.M)
    text = re.sub(r"^\s*\*\*\$(.+?)\$\*\*\s*$", r"$\1$", text, flags=re.M)
    text = re.sub(r"\*\*\$(.+?)\$\*\*", r"$\1$", text)
    text = re.sub(
        r"(\$L_p=20\\log_{10}\\frac\{p\}\{p_0\}\$)\s*\$p_0\$",
        r"\1。$p_0$",
        text,
    )
    return text


def split_merged_structure(text: str) -> str:
    replacements = {
        "**考试重点!!!** 1. **律学（temperament）** 要解决的问题：":
            "**考试重点!!!**\n\n1. **律学（temperament）** 要解决的问题：",
        "**群中的字**- 设":
            "**群中的字**\n\n- 设",
        "***音级 $\\rightarrow$ 音类 $\\rightarrow$ 音类集合 $\\rightarrow$ 集合类*** 11. 全音程和弦：":
            "***音级 $\\rightarrow$ 音类 $\\rightarrow$ 音类集合 $\\rightarrow$ 集合类***\n\n11. 全音程和弦：",
        "**集合类 3-11（大、小三和弦对应的pc集的集合类）上的变换** **25春考了很多！！！**1. **平行变换 $P$**:":
            "**集合类 3-11（大、小三和弦对应的pc集的集合类）上的变换**\n\n**25春考了很多！！！**\n\n1. **平行变换 $P$**:",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r"(\*\*[^*\n]+\*\*)\s*-\s*", r"\1\n\n- ", text)
    text = re.sub(r"(\*\*[^*\n]+\*\*)\s+(\d+\.\s)", r"\1\n\n\2", text)
    text = re.sub(r"([。！？：:）)])\s*(\d+\.\s)", r"\1\n\n\2", text)
    text = re.sub(r"([。！？：:）)])\s*(-\s)", r"\1\n\n\2", text)
    return text


def ensure_admonition_spacing(lines: list[str]) -> list[str]:
    out: list[str] = []
    for i, line in enumerate(lines):
        if re.match(r"^(!!!|\?\?\?) ", line):
            if out and out[-1].strip():
                out.append("")
            out.append(line)
            next_line = lines[i + 1] if i + 1 < len(lines) else ""
            if next_line.startswith("    ") and next_line.strip():
                out.append("")
            continue
        out.append(line)
    return out


def split_image_paragraphs(lines: list[str], keep_attrs: bool) -> list[str]:
    image_re = re.compile(r"!\[[^\]]*\]\([^)]+\)(?:\{ width=\"[^\"]+\" \})?")
    out: list[str] = []

    for line in lines:
        m = image_re.search(line)
        if not m:
            out.append(line)
            continue

        line_indent = re.match(r"^\s*", line).group(0)
        body = line[len(line_indent):]
        body_indent = line_indent
        list_match = re.match(r"^(\d+\.\s+|-\s+)", body)
        if list_match:
            body_indent = line_indent + " " * len(list_match.group(1))

        matches = list(image_re.finditer(body))
        if not matches:
            out.append(line)
            continue

        prefix = body[: matches[0].start()].rstrip()
        suffix = body[matches[-1].end() :].strip()
        images = [m.group(0) for m in matches]
        if not keep_attrs:
            images = [re.sub(r"\{ width=\"[^\"]+\" \}", "", img) for img in images]

        if prefix:
            out.append(line_indent + prefix)
            out.append("")

        for idx, image in enumerate(images):
            out.append(body_indent + image)
            if idx != len(images) - 1:
                out.append("")

        if suffix:
            out.append("")
            out.append(body_indent + suffix)
        elif prefix:
            out.append("")

    # Remove duplicate blank lines.
    compact: list[str] = []
    for line in out:
        if line == "" and compact and compact[-1] == "":
            continue
        compact.append(line)
    return compact


def join_number_only_image_items(text: str, keep_attrs: bool) -> str:
    image = r"!\[[^\]]*\]\([^)]+\)"
    if keep_attrs:
        image += r"(?:\{ width=\"[^\"]+\" \})?"

    pattern = re.compile(
        rf"(?m)^(\s*\d+\.)\s*$\n\n^\s*({image})\s*$"
    )
    return pattern.sub(r"\1 \2", text)


def normalize_outside_block_indentation(text: str) -> str:
    lines = text.split("\n")
    out: list[str] = []
    in_fence = False
    in_admon = False

    for raw in lines:
        line = raw

        if line.startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue

        if in_fence:
            out.append(line)
            continue

        if re.match(r"^(!!!|\?\?\?) ", line):
            in_admon = True
            out.append(line)
            continue

        if in_admon:
            if line == "" or line.startswith("    "):
                out.append(line)
                continue
            in_admon = False

        stripped = line.lstrip()
        if stripped.startswith("![") or re.match(r"^(?:-|\d+\.)\s+", stripped) or stripped.startswith("|"):
            out.append(stripped)
            continue

        if re.match(r"^\s{4,}\S", line) and not stripped.startswith(">"):
            out.append(stripped)
            continue

        out.append(line)

    return "\n".join(out)


def ensure_blank_lines_around_blocks(text: str) -> str:
    lines = text.split("\n")
    out: list[str] = []
    in_fence = False
    in_admon = False

    list_re = re.compile(r"^(?:-|\d+\.)\s+")

    for idx, line in enumerate(lines):
        if line.startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue

        if in_fence:
            out.append(line)
            continue

        if re.match(r"^(!!!|\?\?\?) ", line):
            in_admon = True
            if out and out[-1].strip():
                out.append("")
            out.append(line)
            continue

        if in_admon:
            if line == "" or line.startswith("    "):
                if re.match(r"^\s{4,}(?:-|\d+\.)\s+", line):
                    if out and out[-1].strip() and out[-1].strip() != ">":
                        out.append("")
                out.append(line)
                continue
            in_admon = False

        if list_re.match(line):
            if out and out[-1].strip():
                out.append("")
            out.append(line)
            continue

        if line.strip() == "$$":
            if out and out[-1].strip() and out[-1].strip() != "$$":
                out.append("")
            out.append(line)
            nxt = lines[idx + 1] if idx + 1 < len(lines) else ""
            if nxt.strip() and nxt.strip() != "$$":
                out.append("")
            continue

        out.append(line)

    compact: list[str] = []
    for l in out:
        if l == "" and compact and compact[-1] == "":
            continue
        compact.append(l)
    return "\n".join(compact)


def fix_local_phrasing(text: str) -> str:
    replacements = {
        "音乐会音高 ：A4, 440Hz": "音乐会音高：A4，440 Hz",
        "选B": "选 B",
        "主调：出现最多的,例：": "主调：出现最多的。例：",
        "联觉,想象,通感,移情": "联觉、想象、通感、移情",
        "由（盛宗亮）作曲。": "由盛宗亮作曲。",
        "纯律由（扎利诺）发明。": "纯律由扎利诺提出。",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r"答案是 D[。．]*", "答案是 D。", text)
    text = re.sub(r"答案是 x/2[。．]*", "答案是 $x/2$。", text)
    text = re.sub(r"选 B[。．]{2,}", "选 B。", text)
    text = re.sub(r"(?m)^(\s*-\s*)\*\*", r"\1**", text)
    text = re.sub(r"(?m)^(\s*\d+\.\s*)\*\*", r"\1**", text)
    return text


def polish_for_zensical(text: str) -> str:
    text = text.replace("\r\n", "\n")
    text = normalize_outside_block_indentation(text)
    text = normalize_emphasis_v2(text)
    text = normalize_inline_formulas(text)
    text = fix_local_phrasing(text)
    text = split_merged_structure(text)

    lines = text.split("\n")
    lines = ensure_admonition_spacing(lines)
    lines = split_image_paragraphs(lines, keep_attrs=True)
    text = "\n".join(lines)
    text = join_number_only_image_items(text, keep_attrs=True)
    text = ensure_blank_lines_around_blocks(text)
    return text.rstrip() + "\n"


def convert_admonitions_for_typora(lines: list[str]) -> list[str]:
    out: list[str] = []
    i = 0
    header_re = re.compile(r'^(!!!|\?\?\?)\s+\w+\s+"([^"]+)"\s*$')
    while i < len(lines):
        line = lines[i]
        m = header_re.match(line)
        if not m:
            out.append(line)
            i += 1
            continue

        title = m.group(2).strip()
        out.append(f"> **{title}**")
        i += 1
        while i < len(lines):
            cur = lines[i]
            if cur.startswith("    "):
                body = cur[4:]
                if body.strip():
                    out.append(f"> {body}")
                else:
                    out.append(">")
                i += 1
                continue
            if cur == "":
                out.append(">")
                i += 1
                continue
            break
        if out and out[-1] == ">":
            out.pop()
        out.append("")
    return out


def polish_for_typora(text: str) -> str:
    lines = text.split("\n")
    lines = convert_admonitions_for_typora(lines)
    lines = split_image_paragraphs(lines, keep_attrs=False)
    text = "\n".join(lines)
    text = join_number_only_image_items(text, keep_attrs=False)
    text = re.sub(r"\{ width=\"[^\"]+\" \}", "", text)
    return text.rstrip() + "\n"


def main() -> None:
    original = ZEN_PATH.read_text(encoding="utf-8")
    zensical = polish_for_zensical(original)
    ZEN_PATH.write_text(zensical, encoding="utf-8")
    TYPORA_PATH.write_text(polish_for_typora(zensical), encoding="utf-8")


if __name__ == "__main__":
    main()
