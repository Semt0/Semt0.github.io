# scripts

## 1 用途

内容维护、资源处理与项目自动化脚本。

## 2 内容清单

### 内容更新脚本（由 `update.sh` / CI 调用）

| 脚本 | 用途 | 输出 |
|------|------|------|
| `update.sh` | 依次调用所有内容更新脚本 | 多个生成文件 |
| `update_home_recent.py` | 按笔记 frontmatter `date` 更新主页 Recent | `docs/index.md` |
| `update_note_counts.py` | 更新笔记首页栏目卡片数量 | `docs/note/index.md` |
| `update_timeline.py` | 更新 blog/note 时间线 | `docs/blog/index.md`、`docs/note/index.md` |
| `update_essay_timeline.py` | 更新手记时间线 | `docs/essay/index.md` |
| `update_nav_blog.py` | 根据博客文件更新 `zensical.toml` 博客导航 | `zensical.toml` |
| `update_nav_notes.py` | 根据笔记文件更新 `zensical.toml` 笔记导航 | `zensical.toml` |
| `update_quiz.py` | 扫描 `quiz.yml` 生成分科目题库页 | `docs/quiz/*.md` |
| `check_indexes.py` | 检查目录索引 README 完整性与大小 | 终端报告 |

### 资源处理脚本（手动调用）

| 脚本 | 用途 |
|------|------|
| `check_pages.py` | 查看 PDF 总页数 |
| `compress_images.py` | 批量压缩图片 |
| `export_pdf_pages.py` | 高分辨率导出 PDF 页面为 PNG |
| `export_pdf_pages_simple.py` | PDF 页面导出简化版 |
| `extract_pdf_text.py` | 提取 PDF 文本 |
| `generate_cheatsheet.py` | 从 JSON 数据生成 A4 横向四栏速查表 PDF（Pandoc + XeLaTeX） |

### 绘图生成脚本

- `generate_conformal_mapping_plots.py`
- `generate_diffusion_policy_figures.py`
- `generate_dp_benchmarks.py`
- `generate_eigenvalue_plots.py`
- `generate_iterative_method_plots.py`
- `generate_recognition_plots.py`
- `generate_recognition_plots_v2.py`

### 其他辅助脚本

- `fix_music_math_format.py`
- `polish_music_math_note.py`

## 3 规则与约定

- 影响站点生成流程的脚本，需在 `update.sh` 和 `.github/workflows/docs.yml` 中同步登记。
- 生成性脚本的输出文件应声明为“不要手动编辑”。
- 新增脚本后，更新本 `README.md`。

### 依赖说明

- `generate_cheatsheet.py` 需要系统安装 `pandoc` 和 `xelatex`（TeX Live / MacTeX）。

## 4 上下层索引

- 上层：[../README.md](../README.md)、[../CLAUDE.md](../CLAUDE.md)
- 相关：[../.claude/indexes/docs/javascripts/README.md](../.claude/indexes/docs/javascripts/README.md)

## 5 扩展指南

新增脚本时参见 [扩展指南](../CLAUDE/08-extension.md) 中“新增一个脚本”。
