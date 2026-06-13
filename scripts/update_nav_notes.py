#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path
import tomllib


REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS = REPO_ROOT / "docs"
NOTE_ROOT = DOCS / "note"
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


def render_items(items: list[object], indent: str, item_indent: str) -> list[str]:
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
        lines.extend(render_items(v, indent="", item_indent=sub_item_indent))
        lines.append(f"{item_indent}]}},")
    return lines


def render_list(items: list[object], indent: str, item_indent: str) -> str:
    lines: list[str] = []
    lines.append("[")
    lines.extend(render_items(items, indent=indent, item_indent=item_indent))
    lines.append(f"{indent}]")
    return "\n".join(lines)


def render_nav(nav: list[object]) -> str:
    indent = ""
    top_item_indent = "   "
    rendered = render_list(nav, indent, top_item_indent)
    return "nav = " + rendered


def collect_note_paths() -> list[str]:
    out: list[str] = []
    for p in sorted(NOTE_ROOT.rglob("*.md")):
        if p.name in ("index.md", "README.md"):
            continue
        rel = p.relative_to(DOCS).as_posix()
        out.append(rel)
    return out


def update_nav_notes(nav: list[object]) -> bool:
    note_entry: dict[str, object] | None = None
    for it in nav:
        if isinstance(it, dict) and "笔记" in it:
            note_entry = it
            break
    if note_entry is None:
        raise SystemExit("nav 中未找到 '笔记' 配置块")

    note_list = note_entry["笔记"]
    if not isinstance(note_list, list):
        raise SystemExit("'笔记' 不是列表")

    existing: set[str] = set()
    for it in note_list:
        if isinstance(it, str):
            existing.add(it)
        elif isinstance(it, dict) and len(it) == 1:
            _, v = next(iter(it.items()))
            if isinstance(v, list):
                for s in v:
                    if isinstance(s, str):
                        existing.add(s)

    changed = False
    for rel in collect_note_paths():
        if rel in existing:
            continue
        parts = Path(rel).parts
        if len(parts) < 2 or parts[0] != "note":
            continue
        cat = parts[1]

        cat_dict: dict[str, object] | None = None
        for it in note_list:
            if isinstance(it, dict) and cat in it:
                cat_dict = it
                break

        if cat_dict is None:
            note_list.append({cat: [rel]})
            changed = True
            existing.add(rel)
            continue

        cat_list = cat_dict.get(cat)
        if not isinstance(cat_list, list):
            raise SystemExit(f"分类 {cat} 在 nav 中不是列表")
        cat_list.append(rel)
        changed = True
        existing.add(rel)

    return changed


def main() -> None:
    raw = CONFIG_PATH.read_text(encoding="utf-8")
    start, end = find_nav_block(raw)
    nav_block = raw[start:end]

    data = tomllib.loads(nav_block)
    nav = data.get("nav")
    if not isinstance(nav, list):
        raise SystemExit("nav 解析失败：不是列表")

    changed = update_nav_notes(nav)
    if not changed:
        print("zensical.toml nav 无需更新")
        return

    new_nav_block = render_nav(nav)
    new_raw = raw[:start] + new_nav_block + raw[end:]
    CONFIG_PATH.write_text(new_raw, encoding="utf-8", newline="\n")
    print("已更新 zensical.toml（新增 note 条目已写入 nav）")


if __name__ == "__main__":
    main()
