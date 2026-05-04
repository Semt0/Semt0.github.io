#!/usr/bin/env python3

from __future__ import annotations

from datetime import date as date_cls
from pathlib import Path
import re
import tomllib


REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS = REPO_ROOT / "docs"
BLOG_ROOT = DOCS / "blog"
CONFIG_PATH = REPO_ROOT / "zensical.toml"


def find_nav_block(text: str) -> tuple[int, int]:
    key = "nav"
    i = text.find(key)
    if i < 0:
        raise SystemExit("未找到 nav 配置块")

    eq = text.find("=", i)
    if eq < 0:
        raise SystemExit("未找到 nav 的 '='")

    j = eq + 1
    while j < len(text) and text[j].isspace():
        j += 1
    if j >= len(text) or text[j] != "[":
        raise SystemExit("nav 不是以 '[' 开始的数组")

    start = i
    k = j
    depth = 0
    in_str = False
    escape = False
    while k < len(text):
        ch = text[k]
        if in_str:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_str = False
        else:
            if ch == '"':
                in_str = True
            elif ch == "[":
                depth += 1
            elif ch == "]":
                depth -= 1
                if depth == 0:
                    end = k + 1
                    return start, end
        k += 1

    raise SystemExit("未能匹配 nav 数组的闭合 ']'")


def esc_string(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def render_items(items: list[object], item_indent: str) -> list[str]:
    lines: list[str] = []
    for it in items:
        if isinstance(it, str):
            lines.append(f"{item_indent}{esc_string(it)},")
            continue
        if not isinstance(it, dict) or len(it) != 1:
            raise SystemExit("nav 中存在不受支持的条目类型")
        k, v = next(iter(it.items()))
        if isinstance(v, str):
            lines.append(f'{item_indent}{{{esc_string(k)} = {esc_string(v)}}},')
            continue
        if not isinstance(v, list):
            raise SystemExit("nav dict 的值类型不受支持")

        lines.append(f'{item_indent}{{{esc_string(k)} = [')
        sub_item_indent = item_indent + "    "
        lines.extend(render_items(v, item_indent=sub_item_indent))
        lines.append(f"{item_indent}]}},")
    return lines


def render_nav(nav: list[object]) -> str:
    lines: list[str] = ["nav = ["]
    lines.extend(render_items(nav, item_indent="   "))
    lines.append("]")
    return "\n".join(lines)


def parse_frontmatter(raw: str) -> dict[str, str]:
    raw = raw.lstrip("\ufeff").strip()
    if not raw.startswith("---"):
        return {}
    m = re.match(r"^---\s*\n([\s\S]*?)\n---\s*(\n|$)", raw)
    if not m:
        m = re.match(r"^---\s*[\r\n]+([\s\S]*?)[\r\n]+---\s*([\r\n]|$)", raw)
        if not m:
            return {}
    block = m.group(1)
    data: dict[str, str] = {}
    for line in block.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, rest = line.partition(":")
        key = key.strip()
        val = rest.strip().strip('"').strip("'")
        if key in ("title", "date"):
            data[key] = val
    return data


def collect_blog_paths() -> list[str]:
    dated: list[tuple[date_cls, float, str]] = []
    undated: list[str] = []

    for p in sorted(BLOG_ROOT.rglob("*.md")):
        if p.name == "index.md":
            continue

        rel = p.relative_to(DOCS).as_posix()
        fm = parse_frontmatter(p.read_text(encoding="utf-8"))
        ds = fm.get("date", "").strip()
        if not ds:
            undated.append(rel)
            continue

        try:
            y, m, d = (int(x) for x in ds.split("-")[:3])
            dt = date_cls(y, m, d)
        except (ValueError, TypeError):
            undated.append(rel)
            continue

        dated.append((dt, p.stat().st_mtime, rel))

    dated.sort(key=lambda x: (x[0], x[1], x[2]), reverse=True)
    undated.sort()
    return [x[2] for x in dated] + undated


def update_nav_blog(nav: list[object]) -> bool:
    blog_entry: dict[str, object] | None = None
    for it in nav:
        if isinstance(it, dict) and "博客" in it:
            blog_entry = it
            break
    if blog_entry is None:
        raise SystemExit("nav 中未找到 '博客' 配置块")

    blog_list = blog_entry["博客"]
    if not isinstance(blog_list, list):
        raise SystemExit("'博客' 不是列表")

    existing: set[str] = set()
    for it in blog_list:
        if isinstance(it, str):
            existing.add(it)

    missing = [rel for rel in collect_blog_paths() if rel not in existing]
    if not missing:
        return False

    insert_pos = 0
    for i, it in enumerate(blog_list):
        if isinstance(it, str) and it == "blog/index.md":
            insert_pos = i + 1
            break

    for rel in missing:
        blog_list.insert(insert_pos, rel)
        insert_pos += 1

    return True


def main() -> None:
    raw = CONFIG_PATH.read_text(encoding="utf-8")
    start, end = find_nav_block(raw)
    nav_block = raw[start:end]

    data = tomllib.loads(nav_block)
    nav = data.get("nav")
    if not isinstance(nav, list):
        raise SystemExit("nav 解析失败：不是列表")

    changed = update_nav_blog(nav)
    if not changed:
        print("zensical.toml blog nav 无需更新")
        return

    new_nav_block = render_nav(nav)
    new_raw = raw[:start] + new_nav_block + raw[end:]
    CONFIG_PATH.write_text(new_raw, encoding="utf-8", newline="\n")
    print("已更新 zensical.toml（新增 blog 条目已写入 nav）")


if __name__ == "__main__":
    main()

