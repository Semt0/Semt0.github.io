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

# 更新主页 Recent 列表（按笔记 frontmatter 的 date，默认最新 5 篇）
uv run python scripts/update_home_recent.py

# 更新笔记首页的栏目卡片数量统计
uv run python scripts/update_note_counts.py

# 更新 blog 和 note 首页的时间线布局
uv run python scripts/update_timeline.py

# Production build（自动执行所有更新脚本）
uv run python scripts/update_home_recent.py
uv run python scripts/update_note_counts.py
uv run python scripts/update_timeline.py
zensical build --clean
```

**Python 3.13** required (see `.python-version`). The `zensical` package is the dev dependency that provides the build toolchain.

## Deployment

GitHub Actions (`.github/workflows/docs.yml`) auto-deploys on push to `main`/`master`. The workflow runs `scripts/update_home_recent.py`, `scripts/update_note_counts.py`, and `scripts/update_timeline.py` then `zensical build --clean`, and publishes the `site/` directory to GitHub Pages.

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
- **`scripts/`** —
  - `update_home_recent.py` — 按笔记 frontmatter 的 `date` 更新主页 Recent 列表
  - `update_note_counts.py` — 扫描笔记目录，自动更新 note 首页的栏目卡片数量统计
  - `update_timeline.py` — 扫描 blog 和 note 目录，按日期排序更新时间线布局
  - `export_pdf_pages.py` — 通用 PDF 页面导出脚本（PyMuPDF，高分辨率导出到 `pictures/`）
  - `compress_images.py` — 批量压缩笔记图片，控制单图体积
- **Source PDFs** — 笔记对应的 PDF 源文件存放在 `/Users/semt0/Downloads` 目录下

## Key Patterns

- All custom JS integrates with Zensical's SPA navigation via `document$` (RxJS observable) to reinitialize on page transitions.
- Animations respect `prefers-reduced-motion` and detect low-performance devices (coarse pointer, CPU cores ≤ 4).
- Dark mode (`[data-md-color-scheme="slate"]`) uses CSS variables extensively and adds a radial-gradient starfield background.
- The homepage (`docs/index.md`) uses raw HTML with CSS classes defined in `extra.css` — it is not standard Markdown content.
- When editing `docs/` files, the corresponding `site/` files are generated output and should be rebuilt, not manually edited.

## Note-Writing Conventions

When creating or editing learning notes under `docs/note/`, follow these rules:

- **Images are required**: 笔记默认必须包含必要的插图。可以：
  - 从 PDF 源文件截取关键图表/示意图
  - 使用 matplotlib 绘制算法流程图、几何示意图、收敛曲线等
  - 所有图片存放在 `pictures/` 子目录中
  - 引用格式：`![描述](pictures/filename.png){ width="800" }`
  
- **Math formulas**: Use `$...$` for inline math, `$$...$$` for block-level formulas.

- **Block formula spacing**: Block-level formulas (`$$...$$`) must have a blank line before and after them.

- **Bold text spacing**: Bold text (`**text**`) must have a space before and after the whole bold span from surrounding non-bold text (e.g., `我是 **秦始皇** 吗` not `我是**秦始皇**吗`).

- **Bold and inline math (KaTeX)**: Do **not** wrap `$...$` inside `**...**`. Use `$x$` for formulas and `**词**` for emphasis separately.

- **Many bold fragments**: Avoid many adjacent `**...**` in one long sentence; prefer commas or fewer emphasized spans for reliable rendering in Zensical/Material.

- **List spacing**:
  
  - **列表前必须有空行**：当使用 `-` 创建无序列表时，必须在列表前插入一个完整的空行（即两个连续的换行符），确保列表与上文内容之间有明显视觉分隔。
  - 正确示例：
    ```markdown
    下面是理由：
    
    - 第一点
    - 第二点
    ```
  - 错误示例（禁止出现）：
    ```markdown
    下面是理由：
    - 第一点
    - 第二点
    ```
  - 此规则适用于所有层级的无序列表，包括 admonition 内和 admonition 外的列表。
  - **Admonition 内列表前必须有空行**：在 `!!!` 或 `???` admonition 中，标题行、段落文本、或 `:` 结尾的句子与列表的第一个条目之间必须有空行
  - 正确示例：
    ```markdown
    !!! abstract "定义 X（Name）"
        定义的正式内容：
    
        - 第一个列表项
        - 第二个列表项
    ```
  - 错误示例（以下情况均违反规则）：
    ```markdown
    !!! warning "标题后直接跟列表"
        - 列表项 1  ← 标题后直接跟列表，错误
        - 列表项 2
    
    !!! abstract "定义 X（Name）"
        段落文本后直接跟列表：
        - 列表项 1  ← 冒号后直接跟列表，错误
        - 列表项 2
    ```
  
- **Images**: Store images in a `pictures/` folder under the current note directory. Use the format: `![alt text](pictures/filename.png){ width="600" }`.

- **Frontmatter**: Each note should have YAML frontmatter with at least a `date` field.

- **List numbering**: Do not mix bullet markers with numbers inside list items. Use either `- item` or `1. item`, never `- (1) item`.

- **Markdown syntax**: Follow Zensical (Material for MkDocs fork) conventions. Refer to the official MkDocs Material documentation for details.

- **Navigation**: After creating a new note, add its path to `zensical.toml` under the correct subject in `nav`.

- **Algorithms/Pseudocode**: All algorithms must be written in LaTeX format using the `aligned` environment, not Markdown lists. See template in "Note Template & Admonition Style" section.

## Note Template & Admonition Style

When writing learning notes (especially math/CS theory), use the following structure and admonition patterns:

!!! warning "重要：笔记不需要手动目录"
    **不要在笔记开头添加 `## 目录` 章节**。Zensical 会自动生成右侧目录导航。
    
    直接以 `## 1 Section Title` 开始正文即可。

```markdown
---
title: 本章标题。
date: YYYY-MM-DD
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
- **Algorithms**: **不要**使用 `!!! abstract` 包裹伪代码块。直接使用 `##` 小标题 + LaTeX `aligned` 环境
- Admonition body is indented by **4 spaces**. Block formulas inside admonitions also need blank lines before and after `$$`.

### Pseudocode Format

All algorithms must use LaTeX `aligned` environment. Use `###` subheading for algorithm title, not admonition:

```markdown
### 算法 X.X（算法名称）

$$
\begin{aligned}
& \textbf{算法: } \text{AlgorithmName} \\
& \textbf{输入: } A \in \mathbb{R}^{n \times n}, \quad x^{(0)} \in \mathbb{R}^n, \quad b \in \mathbb{R}^n, \quad N, \quad \varepsilon \\
& \textbf{输出: } x \approx A^{-1}b \\
& 1. \quad k \leftarrow 0 \\
& 2. \quad \textbf{while } k < N \textbf{ do} \\
& 3. \quad \quad \text{// 循环体} \\
& 4. \quad \quad k \leftarrow k + 1 \\
& 5. \quad \textbf{end while} \\
& 6. \quad \textbf{return } x
\end{aligned}
$$
```

**Key formatting rules:**
- Use `\begin{aligned}` environment with `&` for alignment
- Line numbers: `1. \quad`, `2. \quad`, etc.
- Keywords: `\textbf{while}`, `\textbf{do}`, `\textbf{end while}`, `\textbf{if}`, `\textbf{then}`, `\textbf{end if}`, `\textbf{for}`, `\textbf{end for}`, `\textbf{return}`
- Assignment: `\leftarrow`
- Comments: `\text{// comment}`
- Input/Output labels: `\textbf{输入: }`, `\textbf{输出: }`

## Image Generation Workflow

When creating learning notes that need illustrations (e.g., algorithm flowcharts, convergence plots, geometric diagrams), follow this workflow:

### 1. Setup

Ensure `numpy` and `matplotlib` are installed (if not, add them via `uv add numpy matplotlib`).

### 2. Create Generation Script

Create a Python script in `scripts/` directory (e.g., `generate_<topic>_plots.py`) using this template:

```python
import numpy as np
import matplotlib.pyplot as plt

# Use DejaVu Sans for better compatibility
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

def plot_example():
    fig, ax = plt.subplots(figsize=(9, 6))
    # ... plotting code ...
    plt.tight_layout()
    plt.savefig('docs/note/<subject>/pictures/filename.png',
                dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()

if __name__ == '__main__':
    plot_example()
```

### 3. Important Guidelines

- **Font**: Use only **English labels** in plots (matplotlib has limited CJK font support in this environment)
- **Resolution**: Use `dpi=150` for clear web display
- **Background**: Set `facecolor='white'` for consistent appearance
- **Format**: Save as PNG
- **Location**: Store in `docs/note/<subject>/pictures/`
- **Width**: Reference images with `{ width="800" }` for consistent sizing

### 3.1 PDF 页面导出清晰度（必须遵守）

当需要从 PDF 课件/讲义中截取页面作为笔记插图时，统一使用仓库内的通用脚本 `scripts/export_pdf_pages.py`，默认高分辨率参数固定为：

- `zoom = 6.0`
- `alpha = False`

导出的 PNG 必须写入当前笔记目录的 `pictures/` 下，优先覆盖同名文件以保持 Markdown 引用不变。

```bash
uv run python scripts/export_pdf_pages.py \
  "docs/note/<subject>/slides/<file>.pdf" \
  "docs/note/<subject>/pictures" \
  --page 3:figure_03.png \
  --page 7:figure_07.png \
  --page 12:figure_12.png \
  --overwrite
```

参数约定：

- `--page <页码>:<文件名.png>` 可重复传入，默认按 **1-based** 页码解释
- 如需传入 **0-based** 页码，追加 `--base 0`
- 如果个别页面仍显得偏糊（例如原 PDF 本身是低分辨率位图），再将 `--zoom` 提升到 `8.0`
- 覆盖已有图片时必须显式加 `--overwrite`

### 4. Run Script

```bash
uv run python scripts/generate_<topic>_plots.py
```

或导出 PDF 页面：

```bash
uv run python scripts/export_pdf_pages.py \
  "docs/note/<subject>/slides/<file>.pdf" \
  "docs/note/<subject>/pictures" \
  --page 3:figure_03.png \
  --overwrite
```

### 5. Insert into Note

Add image reference in the Markdown:

```markdown
![Description](pictures/filename.png){ width="750" }
```

### Example Reference

See `scripts/generate_iterative_method_plots.py` for a complete example covering:
- Flowcharts (iteration process)
- Comparison diagrams (Jacobi vs Gauss-Seidel)
- Convergence plots (SOR omega effect)
- Geometric visualizations (A-conjugate directions, steepest descent paths)
