# CLAUDE.md

> 本文件是 Claude Code 的项目级 instructions，也是项目的**顶层入口（讲规则）**。
> 
> 详细资源索引、科目目录、脚本说明见 [README.md](README.md)。

## 1 项目总览

Personal blog and learning notes site: https://semt0.github.io/

- **站点生成器**：Zensical（Material for MkDocs 分支）
- **内容**：博客、学习笔记、手记、复习题库、友链
- **语言**：中英双语，数学公式使用 KaTeX
- **Python**：3.13+，包管理使用 `uv`

## 2 快速入门

```bash
# 安装依赖
uv sync

# 本地预览
zensical serve

# 常规更新 + 构建
bash update.sh
uv run zensical build --clean
```

## 3 架构要点

| 路径 | 用途 |
|------|------|
| `zensical.toml` | 站点主配置（主题、导航、插件、CSS/JS） |
| `docs/index.md` | 主页（**原始 HTML**，不是标准 Markdown） |
| `docs/blog/` | 博客文章 |
| `docs/note/` | 学习笔记，按科目组织 |
| `docs/essay/` | 手记 |
| `docs/quiz/` | 复习题库（由 `scripts/update_quiz.py` 自动生成） |
| `docs/friends.md` | 友链 |
| `docs/stylesheets/extra.css` | 自定义样式 |
| `docs/javascripts/` | 自定义脚本 |
| `scripts/` | 内容维护与资源处理脚本 |
| `site/` | 构建产物（**不要手动编辑**） |

## 4 关键技术模式

- **SPA 导航**：所有自定义 JS 通过 `document$` 在页面切换后重新初始化。
- **深色模式**：通过 `[data-md-color-scheme="slate"]` 适配。
- **主页特殊**：`docs/index.md` 使用原始 HTML 和 `extra.css` 中的类，不是标准 Markdown。
- **图片位置**：笔记图片放在当前目录的 `pictures/` 下，引用格式 `![描述](pictures/filename.png){ width="800" }`。
- **自动生成文件**：`docs/quiz/`、`site/` 以及首页 Recent / 时间线 / 导航等由脚本生成，**不要手动编辑**。

## 5 内容更新工作流

修改内容后，先运行更新脚本再构建：

```bash
bash update.sh
uv run zensical build --clean
```

`update.sh` 会依次执行：

- `scripts/update_home_recent.py` — 更新主页 Recent
- `scripts/update_note_counts.py` — 更新笔记首页栏目统计
- `scripts/update_timeline.py` — 更新 blog/note 时间线
- `scripts/update_essay_timeline.py` — 更新手记时间线
- `scripts/update_nav_blog.py` — 更新博客导航
- `scripts/update_nav_notes.py` — 更新笔记导航
- `scripts/update_quiz.py` — 生成复习题库页面

各脚本的详细说明见 [README.md](README.md)。

## 6 笔记写作规则

当创建或编辑 `docs/note/` 下的学习笔记时，遵守以下规则：

- **图片是必需的**：笔记默认必须包含必要插图。来源可以是 PDF 截图、matplotlib 绘图等。图片放在 `pictures/` 子目录，引用格式 `![描述](pictures/filename.png){ width="800" }`。

- **数学公式**：行内用 `$...$`，块级用 `$$...$$`。

- **块级公式间距**：`$$...$$` 前后必须各有一个空行。

- **粗体间距**：`**text**` 与周围非粗体文字之间要留空格，例如 `我是 **秦始皇** 吗`，不要 `我是**秦始皇**吗`。

- **粗体与行内公式**：不要把 `$...$` 包在 `**...**` 里面。公式和强调分开写。

- **避免密集粗体**：一句话里不要连续很多 `**...**`，用逗号或减少强调片段。

- **列表前必须有空行**：使用 `-` 的无序列表前必须插入完整空行。这也适用于 admonition 内部的列表。

- **图片引用**：统一用 `![alt text](pictures/filename.png){ width="600" }`。

- **Frontmatter**：至少包含 `date`；推荐新增 `summary`、`key_points`、`sources`（见第 7 节模板）。

- **列表编号**：不要混用 `-` 和数字，也不要用 `- (1)` 这种形式。

- **导航**：新建笔记后，把路径加到 `zensical.toml` 对应科目的 `nav` 中。

- **算法/伪代码**：使用 LaTeX `aligned` 环境，不要用 Markdown 列表。详见第 7 节模板。

## 7 笔记模板与 Admonition 风格

!!! warning "重要：笔记不需要手动目录"
    **不要在笔记开头添加 `## 目录` 章节**。Zensical 会自动生成右侧目录导航。
    
    直接以 `## 1 Section Title` 开始正文即可。

```markdown
---
title: 本章标题
date: YYYY-MM-DD
summary: |
  用一两句话概括本章核心内容，用于索引和快速预览。
key_points:
  - 核心知识点 1
  - 核心知识点 2
  - 核心知识点 3
sources:
  - "课程/教材名称，章节"
  - "论文标题，作者，年份"
  - "在线资源 URL"
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

### Admonition 使用规则

- **Definitions**: `!!! abstract "定义 X（Name）"` — 始终可见
- **Theorems / Lemmas / Corollaries**: `!!! abstract "定理 X / 引理 X / 推论 X（Name）"` — 始终可见
- **Proofs**: `??? note "证明"` — 可折叠（默认收起），结尾用 `$&square;$`
- **Assumptions**: `!!! note "假设 X"` — 始终可见
- **Tips / Intuition**: `!!! tip` — 始终可见
- **Warnings**: `!!! warning` — 始终可见
- **Supplementary info**: `!!! info` — 始终可见
- **Examples**: `???+ example "例X：..."` — 可折叠（默认展开）
- **Algorithms**: **不要**使用 `!!! abstract` 包裹伪代码块。直接用 `##` 小标题 + LaTeX `aligned` 环境
- Admonition 正文缩进 **4 个空格**，内部的块级公式前后也要有空行

### 伪代码格式

所有算法使用 LaTeX `aligned` 环境，用 `###` 小标题作为算法标题：

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

**格式要点：**
- 环境：`\begin{aligned}`，用 `&` 对齐
- 行号：`1. \quad`, `2. \quad`, ...
- 关键字：`\textbf{while}`, `\textbf{do}`, `\textbf{end while}`, `\textbf{if}`, `\textbf{then}`, `\textbf{end if}`, `\textbf{for}`, `\textbf{end for}`, `\textbf{return}`
- 赋值：`\leftarrow`
- 注释：`\text{// comment}`
- 输入/输出标签：`\textbf{输入: }`, `\textbf{输出: }`

## 8 图片生成工作流

当笔记需要插图（流程图、收敛曲线、几何示意图等）时：

### 8.1 使用 matplotlib

确保已安装 `numpy` 和 `matplotlib`（否则 `uv add numpy matplotlib`）。在 `scripts/` 下创建 `generate_<topic>_plots.py`：

```python
import numpy as np
import matplotlib.pyplot as plt

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

**准则：**
- 图中标签用英文（matplotlib CJK 字体支持有限）
- 分辨率 `dpi=150`
- 背景 `facecolor='white'`
- 格式 PNG，存放到 `docs/note/<subject>/pictures/`
- 引用宽度 `{ width="800" }`

### 8.2 从 PDF 导出页面

从 PDF 课件截取页面时，统一使用 `scripts/export_pdf_pages.py`：

```bash
uv run python scripts/export_pdf_pages.py \
  "docs/note/<subject>/slides/<file>.pdf" \
  "docs/note/<subject>/pictures" \
  --page 3:figure_03.png \
  --page 7:figure_07.png \
  --page 12:figure_12.png \
  --overwrite
```

参数固定为 `zoom=6.0`、`alpha=False`。如仍模糊可提升到 `zoom=8.0`。页码默认 1-based，0-based 需加 `--base 0`。覆盖已有文件必须加 `--overwrite`。

## 9 边界与禁忌

- **不要手动编辑 `site/`**：它是构建产物。
- **不要给笔记加手动目录**：Zensical 自动生成右侧目录。
- **不要把所有信息塞进一个巨大文件**：项目文档已分层，`CLAUDE.md` 讲规则，`README.md` 讲索引，具体知识在 `docs/note/`。
- **不要混用列表标记**：同一列表内不要 `-` 和 `1.` 混用，也不要 `- (1)`。
- **自动生成页面不要手动改**：包括 `docs/quiz/*.md`、首页 Recent 区域、时间线等。

## 10 扩展与索引维护

新增内容、维护目录索引与树形分解的详细指南见 [CLAUDE/08-extension.md](CLAUDE/08-extension.md)。

