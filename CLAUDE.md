# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Personal blog and learning notes site (https://semt0.github.io/) built with **Zensical** (a Material for MkDocs fork). Content is bilingual (Chinese/English) with mathematical notation support via KaTeX.

## Build & Development

```bash
# Install dependencies (uses uv for Python package management)
uv sync

# Local development server
zensical serve

# Production build
zensical build --clean
```

**Python 3.13** required (see `.python-version`). The `zensical` package is the dev dependency that provides the build toolchain.

## Deployment

GitHub Actions (`.github/workflows/docs.yml`) auto-deploys on push to `main`/`master`. The workflow runs `zensical build --clean` and publishes the `site/` directory to GitHub Pages.

## Architecture

- **`zensical.toml`** — Main site configuration (theme, plugins, navigation, extensions, CSS/JS includes). This is the equivalent of `mkdocs.yml` for Zensical.
- **`docs/`** — All source content and assets
  - `index.md` — Homepage (custom HTML layout, not standard Markdown)
  - `blog/` — Blog posts with `.authors.yml`
  - `note/` — Learning notes organized by subject
  - `friends.md` — Friend links page
  - `stylesheets/extra.css` — All custom CSS (~1070 lines): homepage layout, sakura petals, dark mode starfield, animations, responsive design, Waline comments
  - `javascripts/` — Custom JS modules:
    - `sakura-init.js` — 3D petal falling animation (3-layer depth, performance-adaptive)
    - `home-animation.js` — Scroll-triggered section fade-ins, avatar preloading
    - `home-intro-words.js` — Word-by-word text reveal animation
    - `katex.js` — KaTeX math rendering integration
    - `waline-init.js` — Waline v3 comment system (server: Vercel-hosted)
- **`site/`** — Generated output (committed to repo, also built in CI)
- **`scripts/`** — Python utilities for extracting PDF lecture slides to PNG (uses PyMuPDF)

## Key Patterns

- All custom JS integrates with Zensical's SPA navigation via `document$` (RxJS observable) to reinitialize on page transitions.
- Animations respect `prefers-reduced-motion` and detect low-performance devices (coarse pointer, CPU cores ≤ 4).
- Dark mode (`[data-md-color-scheme="slate"]`) uses CSS variables extensively and adds a radial-gradient starfield background.
- The homepage (`docs/index.md`) uses raw HTML with CSS classes defined in `extra.css` — it is not standard Markdown content.
- When editing `docs/` files, the corresponding `site/` files are generated output and should be rebuilt, not manually edited.

## Note-Writing Conventions

When creating or editing learning notes under `docs/note/`, follow these rules:

- **Math formulas**: Use `$...$` for inline math, `$$...$$` for block-level formulas.
- **Block formula spacing**: Block-level formulas (`$$...$$`) must have a blank line before and after them.
- **Bold text spacing**: Bold text (`**text**`) must have a space before and after the whole bold span from surrounding non-bold text (e.g., `我是 **秦始皇** 吗`).
- **Bold next to Chinese / Latin**: After `**...**`, if the sentence continues (e.g. 约、同、时), insert a **space** between the closing `**` and that character (`**模型** 约`, not `**模型**约`). Same before opening `**` when it follows a word: `FP32 **模型**`, not `FP32**模型**`.
- **Bold and inline math (KaTeX)**: Do **not** wrap `$...$` inside `**...**`. Use `$x$` for formulas and `**词**` for emphasis separately.
- **Many bold fragments**: Avoid many adjacent `**...**` in one long sentence; prefer commas or fewer emphasized spans for reliable rendering in Zensical/Material.
- **List spacing**: The first bullet point of a list must have a blank line separating it from the preceding text.
- **Images**: Store images in a `pictures/` folder under the current note directory. Use the format: `![alt text](pictures/filename.png){ width="550" }`.
- **Frontmatter**: Each note should have YAML frontmatter with at least a `date` field.
- **List numbering**: Do not mix bullet markers with numbers inside list items. Use either `- item` or `1. item`, never `- (1) item`.
- **Markdown syntax**: Follow Zensical (Material for MkDocs fork) conventions. Refer to the official MkDocs Material documentation for details.
- **Navigation**: After creating a new note, add its path to `zensical.toml` under the correct subject in `nav`.

## Note Template & Admonition Style

When writing learning notes (especially math/CS theory), use the following structure and admonition patterns:

```markdown
---
date: YYYY-MM-DD
---

# Title

简短概述本章内容。

---

## 目录

- Topic 1
- Topic 2

---

## 1 Section Title

### 1.1 Subsection

正文内容...

!!! abstract "定义 X（Name）"
    定义的正式内容，使用 block formula：

    $$
    formula
    $$

直观理解或补充说明放在 admonition 外面。

!!! abstract "定理 X / 引理 X（Name）"
    定理的正式陈述。

    $$
    formula
    $$

??? note "证明"
    证明过程（可折叠）。最后用 $\square$ 结尾。

!!! tip "提示标题"
    重要的直觉或记忆技巧。

!!! warning "注意标题"
    容易出错的地方。

!!! info "信息标题"
    补充性说明。

!!! note "假设 X"
    定理所需的假设条件。

---

## N 总结

总结表格或核心公式。
```

### Admonition usage rules

- **Definitions**: `!!! abstract "定义 X（Name）"` — always visible
- **Theorems / Lemmas / Corollaries**: `!!! abstract "定理 X / 引理 X / 推论 X（Name）"` — always visible
- **Proofs**: `??? note "证明"` — collapsible (closed by default), end with `$\square$`
- **Assumptions**: `!!! note "假设 X"` — always visible
- **Tips / Intuition**: `!!! tip` — always visible
- **Warnings**: `!!! warning` — always visible
- **Supplementary info**: `!!! info` — always visible
- **Examples**: `???+ example "例X：..."` — collapsible (open by default)
- Admonition body is indented by **4 spaces**. Block formulas inside admonitions also need blank lines before and after `$$`.
