# 算法笔记写作计划

## 目标
按照 CLAUDE.md 笔记书写规范，基于 PDF 课件完成 4 篇算法笔记写作。

## 交付物
1. `docs/note/algorithm/问题复杂度.md` — 基于 11/12/13-问题复杂度.pdf
2. `docs/note/algorithm/NP 完全.md` — 基于 14/15-NP完全.pdf
3. `docs/note/algorithm/近似算法.md` — 基于 16/17-近似算法.pdf
4. `docs/note/algorithm/随机算法.md` — 基于 18/19-随机算法.pdf

## 规范要点（来自 CLAUDE.md）

### 文件结构
- YAML frontmatter: `title`, `date`
- 以 `## 1 Section Title` 开始，**不要手动目录**
- 图片存 `pictures/` 子目录，引用格式 `![描述](pictures/filename.png){ width="800" }`

### Admonition 规范
- 定义: `!!! abstract "定义 X（Name）"`
- 定理/引理: `!!! abstract "定理 X / 引理 X（Name）"`
- 证明: `??? note "证明"`（可折叠，结尾 `$$\square$$`）
- 提示: `!!! tip`
- 警告: `!!! warning`
- 信息: `!!! info`
- 假设: `!!! note "假设 X"`
- 例子: `???+ example "例X：..."`（默认展开）

### 格式规范
- 行内数学: `$...$`
- 块级数学: `$$...$$`，**前后必须有空行**
- **粗体前后必须有空格**: `我是 **秦始皇** 吗`
- **不要**把 `$...$` 包在 `**...**` 内
- 列表前**必须有空行**（包括 admonition 内的列表）
- 算法伪代码用 LaTeX `aligned` 环境，不用 admonition 包裹

### 图片导出
使用 `scripts/export_pdf_pages.py` 从 PDF 导出关键页面：
```bash
uv run python scripts/export_pdf_pages.py \
  "<pdf_path>" \
  "docs/note/algorithm/pictures" \
  --page <页码>:<filename>.png \
  --overwrite
```
参数: `zoom=6.0`, `alpha=False`

### 伪代码格式
```markdown
### 算法 X.X（算法名称）

$$
\begin{aligned}
& \textbf{算法: } \text{AlgorithmName} \\
& \textbf{输入: } ... \\
& \textbf{输出: } ... \\
& 1. \quad ... \\
& 2. \quad \textbf{while } ... \textbf{ do} \\
& ... \\
& 6. \quad \textbf{return } x
\end{aligned}
$$
```

## Stage 1 — 并行写作（4个Agent同时工作）

每个Agent负责一篇笔记：
- **Agent 1**: 问题复杂度.md（3个PDF）
- **Agent 2**: NP 完全.md（2个PDF）
- **Agent 3**: 近似算法.md（2个PDF）
- **Agent 4**: 随机算法.md（2个PDF）

每个Agent任务：
1. 读取对应PDF课件，提取文本内容
2. 识别关键图表/示意图页面，用 export_pdf_pages.py 导出为 PNG
3. 按照笔记模板和admonition规范撰写完整笔记
4. 保存到 `docs/note/algorithm/<文件名>.md`

## Stage 2 — 验证与集成
1. 检查所有笔记 frontmatter、格式、图片引用
2. 更新 `zensical.toml` 导航
3. 运行更新脚本
