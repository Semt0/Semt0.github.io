# Semt0's Blog

个人博客与学习笔记站点，基于 **Zensical**（Material for MkDocs 风格）搭建，用来整理技术文章、课程笔记、数学推导、日常手记与一些长期学习材料。

在线地址：<https://semt0.github.io/>

## 内容

- **博客**：较完整的主题文章、课程复盘与阶段性整理。
- **笔记**：复变函数、常微分方程、数理方程、计算方法、CVDL、CS231n、Foundation Models、算法、并行程序设计、AI 硬件、Rust 等学习笔记。
- **手记**：更轻量的日常记录、想法片段与短篇整理。
- **友链**：个人链接页。

## 特性

- **静态站点**：由 Zensical / MkDocs Material 工具链构建，部署到 GitHub Pages。
- **自定义主页**：个人介绍、头像、内容入口、Recent 列表、滚动淡入与逐词淡入动画。
- **数学公式**：通过 KaTeX 与 `pymdownx.arithmatex` 渲染行内和块级公式。
- **暗色模式**：跟随系统主题，针对正文、导航、目录、背景与评论区做了额外适配。
- **动效细节**：樱花飘落、光标樱花、夜间星空背景，并兼顾低性能设备和 `prefers-reduced-motion`。
- **评论系统**：集成 Waline v3。
- **自动维护脚本**：自动更新主页 Recent、博客/笔记时间线、手记时间线与导航。

## 技术栈

- **站点生成**：Zensical
- **主题系统**：Material for MkDocs 风格主题与自定义 `overrides`
- **内容格式**：Markdown + pymdownx 扩展
- **数学渲染**：KaTeX
- **样式**：`docs/stylesheets/extra.css`
- **脚本**：`docs/javascripts/`
- **包管理**：`uv`
- **运行环境**：Python 3.13+

## 本地开发

安装依赖：

```bash
uv sync
```

启动本地预览：

```bash
uv run zensical serve
```

构建站点：

```bash
uv run zensical build --clean
```

常规更新流程：

```bash
bash update.sh
uv run zensical build --clean
```

## 维护脚本

- `update.sh`：依次更新主页 Recent、手记时间线、博客/笔记时间线与导航。
- `scripts/update_home_recent.py`：按笔记 frontmatter 的 `date` 字段更新主页 Recent 列表。
- `scripts/update_timeline.py`：扫描博客和笔记目录，生成时间线布局。
- `scripts/update_essay_timeline.py`：扫描手记目录，生成手记时间线。
- `scripts/update_nav_blog.py`：根据博客文件更新 `zensical.toml` 中的博客导航。
- `scripts/update_nav_notes.py`：根据笔记文件更新 `zensical.toml` 中的笔记导航。
- `scripts/update_note_counts.py`：更新笔记首页的栏目数量统计。
- `scripts/compress_images.py`：批量压缩图片资源。
- `scripts/export_pdf_pages.py`：将 PDF 页面导出为图片，方便整理课程材料。

## 目录结构

```text
.
├── docs/
│   ├── index.md                 # 主页
│   ├── blog/                    # 博客文章
│   ├── note/                    # 学习笔记
│   ├── essay/                   # 手记
│   ├── friends.md               # 友链
│   ├── images/                  # 站点图片资源
│   ├── stylesheets/
│   │   └── extra.css            # 自定义样式
│   └── javascripts/             # KaTeX、主页动画、樱花、Waline 等脚本
├── overrides/                   # 主题模板覆盖
├── scripts/                     # 内容维护与资源处理脚本
├── site/                        # 构建产物
├── tests/                       # 项目规则测试
├── pyproject.toml               # Python 项目与依赖配置
├── uv.lock                      # uv 锁文件
├── zensical.toml                # 站点主配置
├── update.sh                    # 常用维护入口
└── README.md
```

## 写作约定

- 笔记文件放在 `docs/note/` 对应学科目录下，并在 frontmatter 中写入 `title` 与 `date`。
- 博客文章放在 `docs/blog/`，手记放在 `docs/essay/`。
- 新增内容后运行 `bash update.sh`，让首页、时间线与导航保持同步。
- `site/` 是构建产物，常规内容修改应优先编辑 `docs/`、`scripts/` 与配置文件。
- 数学公式使用 `$...$` 与 `$$...$$`；块级公式前后保留空行，以保证 KaTeX 渲染稳定。

## 部署

GitHub Actions 会在推送到 `main` 或 `master` 后构建并部署到 GitHub Pages。工作流位于 `.github/workflows/docs.yml`，主要步骤是安装 Zensical、运行内容更新脚本、执行 `zensical build --clean`，并发布 `site/` 目录。
