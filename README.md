# Semt0's Blog

个人博客与学习笔记站点：<https://semt0.github.io/>

基于 **Zensical**（Material for MkDocs 分支）搭建，内容以中文为主，支持 KaTeX 数学公式与深色模式。

## 这里有什么

| 板块 | 路径 | 说明 |
|------|------|------|
| **博客** | `docs/blog/` | 主题文章、课程复盘、阶段性整理 |
| **笔记** | `docs/note/` | 按科目整理的学习笔记（数学、CS、AI、硬件等） |
| **手记** | `docs/essay/` | 更轻量的日常记录、想法片段 |
| **友链** | `docs/friends.md` | 个人链接页 |

## 科目索引（笔记）

| 科目 | 目录 | 主题 |
|------|------|------|
| **复变函数** | `note/复变函数/` | 复数与平面点集、解析函数、积分、级数、留数、保形变换、傅里叶/拉普拉斯变换 |
| **常微分方程** | `note/ODE/` | 初等积分法、线性方程组、常系数线性方程、一般理论、定性理论 |
| **数理方程** | `note/数理方程/` | 偏微分方程、分离变量法、特殊函数、积分变换、Green 函数 |
| **计算方法** | `note/计算方法/` | 误差分析、Gauss/LU 消去、迭代法、插值、函数逼近、数值微积分、QR/SVD、ODE 数值解 |
| **算法设计与分析** | `note/算法设计与分析/` | 动态规划、线性规划、网络流、问题复杂度、NP 完全、近似/随机算法 |
| **CVDL** | `note/CVDL/` | ML 入门、Recognition、Detection、3D Vision、Tracking、生成模型 |
| **Introduction to Foundation Models** | `note/Introduction to Foundation Models/` | Transformer、SGD 系列、FlashAttention、PEFT、LLM 推理、CoT、数据准备 |
| **CS231n** | `note/cs231n/` | 图像分类、正则化与优化 |
| **AI 硬件** | `note/ai硬件/` | 数字逻辑、计算单元、指令集、浮点运算 |
| **并行程序设计** | `note/并行程序设计/` | MPI、OpenMP、GPU 编程与内存模型 |
| **Rust 程序设计** | `note/Rust程序设计/` | 所有权、所有权转移 |
| **OJ 复习** | `note/OJ复习/` | 基础数据结构、图论、字符串算法 |

## 技术栈

- **站点生成**：Zensical
- **主题系统**：Material for MkDocs 风格 + 自定义 `overrides/`
- **数学渲染**：KaTeX + `pymdownx.arithmatex`
- **自定义样式**：`docs/stylesheets/extra.css`
- **自定义脚本**：`docs/javascripts/`（樱花、主页动画、Waline、KaTeX 等）
- **包管理**：`uv`
- **运行环境**：Python 3.13+

## 本地开发

```bash
# 安装依赖
uv sync

# 启动本地预览
uv run zensical serve

# 构建站点
bash update.sh
uv run zensical build --clean
```

## 维护脚本索引

| 脚本 | 用途 | 触发方式 |
|------|------|----------|
| `update.sh` | 依次执行所有内容更新脚本 | 手动 |
| `scripts/update_home_recent.py` | 按 frontmatter `date` 更新主页 Recent | `update.sh` / CI |
| `scripts/update_note_counts.py` | 更新笔记首页栏目卡片数量 | `update.sh` / CI |
| `scripts/update_timeline.py` | 生成 blog/note 时间线 | `update.sh` / CI |
| `scripts/update_essay_timeline.py` | 生成手记时间线 | `update.sh` / CI |
| `scripts/update_nav_blog.py` | 根据文件更新博客导航 | `update.sh` / CI |
| `scripts/update_nav_notes.py` | 根据文件更新笔记导航 | `update.sh` / CI |
| `scripts/check_pages.py` | 查看 PDF 总页数 | 手动 |
| `scripts/compress_images.py` | 批量压缩图片 | 手动 |
| `scripts/export_pdf_pages.py` | 高分辨率导出 PDF 页面为 PNG | 手动 |

其他脚本（绘图生成、PDF 文本提取等）见 `scripts/` 目录。

## 目录结构

```text
.
├── docs/
│   ├── index.md                 # 主页（原始 HTML）
│   ├── blog/                    # 博客文章
│   ├── note/                    # 学习笔记
│   ├── essay/                   # 手记
│   ├── friends.md               # 友链
│   ├── images/                  # 站点图片资源
│   ├── stylesheets/             # 自定义 CSS
│   └── javascripts/             # 自定义 JS
├── .claude/indexes/             # Agent 目录索引（不渲染到站点）
│   └── docs/.../README.md
├── overrides/                   # 主题模板覆盖
├── scripts/                     # 内容维护脚本
├── site/                        # 构建产物（不手动编辑）
├── tests/                       # 项目规则测试
├── pyproject.toml               # Python 配置
├── uv.lock                      # uv 锁文件
├── zensical.toml                # 站点主配置
└── README.md                    # 本文件：资源索引
```

## 部署

GitHub Actions（`.github/workflows/docs.yml`）在推送到 `main`/`master` 后自动构建并部署到 GitHub Pages。

## 写作约定

详细规则、笔记模板、admonition 风格、图片生成工作流见 **CLAUDE.md**。

笔记 frontmatter 推荐新增：

```yaml
---
title: 本章标题
date: YYYY-MM-DD
summary: |
  一句话概括本章核心内容。
key_points:
  - 核心知识点 1
  - 核心知识点 2
sources:
  - "课程/教材名称，章节"
---
```

## 目录索引维护

本项目采用**分层目录索引**：几乎每个内容目录都在 `.claude/indexes/` 下有对应的 `README.md`，说明该目录的用途、内容清单、规则和扩展方式。这些 `README.md` 仅作为 Agent / 仓库导航索引，**不会渲染到站点**；站点页面由各个 `index.md` 负责。

- **顶层规则入口**：[CLAUDE.md](CLAUDE.md)
- **根资源索引**：本文件
- **docs 层索引**：`.claude/indexes/docs/README.md`
- **笔记层索引**：`.claude/indexes/docs/note/README.md`
- **科目目录索引**：如 `.claude/indexes/docs/note/计算方法/README.md`
- **工程层索引**：[scripts/README.md](scripts/README.md)、[tests/README.md](tests/README.md)、[overrides/README.md](overrides/README.md)

当某个 `README.md` 或 `CLAUDE.md` 超过 300 行时，会按树形结构拆分到同名子目录中（如 `CLAUDE/`、`README/`）。笔记正文不受行数限制。

新增内容时如何维护索引，见 [扩展指南](CLAUDE/08-extension.md)。

可以使用验证脚本检查索引完整性：

```bash
uv run python scripts/check_indexes.py
```
