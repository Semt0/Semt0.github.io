# Semt0's Blog

个人博客与学习笔记：[semt0.github.io](https://semt0.github.io/)。基于 Zensical，支持中文排版、KaTeX、浅色/深色主题和 Waline 评论。

## 开发与构建

需要 Python 3.13+ 和 uv；前端回归测试需要 Node.js 22+。

```bash
uv sync --frozen
bash update.sh
uv run zensical serve
```

发布前使用与 CI 相同的检查：

```bash
bash update.sh --check
uv run python -m unittest discover -s tests -p 'test_*.py'
node --experimental-vm-modules --test tests/*.test.mjs
uv run zensical build --clean
uv run python scripts/check_site.py
```

`update.sh` 统一生成三个板块的时间线和缺失导航条目。`--check` 只检查是否过期，不修改文件。新增或修改元数据后先运行 `bash update.sh`；预览服务器不会自动运行生成器。

## 目录

```text
docs/                       文章、页面和静态资源
  blog/                     博客
  note/                     按科目组织的学习笔记
  essay/                    手记
  javascripts/              仅保留公式与评论初始化
  stylesheets/              theme / home / components / comments
overrides/                  资源引入与评论模板
scripts/
  update_site.py            内容索引与导航生成器
  check_site.py             构建产物检查
  assets/                   PDF、图片、速查表工具
  figures/                  各文章的插图生成源码
tests/                      独立运行的 Python / Node 回归测试
zensical.toml               站点配置与导航
site/                       构建产物，不提交、不手动编辑
```

## 写作

在对应板块新增 Markdown 文件，建议包含 `title` 和 `date: YYYY-MM-DD`。写作模板、公式和图片规范见 [CONTRIBUTING.md](CONTRIBUTING.md)。

- `zensical.toml` 保留人工安排的科目名称和顺序；生成器只补充缺失文章。新科目默认使用目录名，可手动修改显示名称。
- 时间线按日期、路径稳定排序，不依赖本机文件时间。无日期条目放在末尾并标注“未标日期”。
- 文章路径决定 URL 和 Waline 评论归属。重命名需要单独处理链接与评论迁移。
- `comments: false` 可关闭单页评论；评论容器由模板统一插入。
- 首页不加载评论；友链页用 `comment_path: /` 继续展示原首页留言。其他文章默认按原始 URL 关联评论，迁移页面时可用此字段保留讨论。

## 前端维护

样式按职责分为四个文件。全站纸白/深色、玫瑰色强调、边框与语义提示颜色统一定义在 `theme.css` 的 `--site-*` 变量中；`home.css` 只负责首页布局，列表、友链、正文及评论复用同一组变量。装饰动画仅使用 CSS，尊重系统“减少动态效果”偏好；正文和链接不依赖动画或 JavaScript 才显示。Zensical 负责导航、搜索、主题切换等基础交互。

Waline 客户端固定版本随站点托管，避免运行时 CDN 故障。更新时同时替换 JS / CSS，并核对 `docs/vendor/waline/PROVENANCE.txt` 中的来源、版本和校验值。模板说明见 [OVERRIDES.md](OVERRIDES.md)。

## 可选资源工具

普通构建只安装站点运行包，不需要绘图和 PDF 依赖。制作课件资源时：

```bash
uv sync --group assets
uv run --group assets python scripts/assets/export_pdf_pages.py source.pdf output/ --page 3:figure.png
```

工具说明见 [scripts/README.md](scripts/README.md)。科学插图生成源码保留在 `scripts/figures/`，不参与站点部署。

## 部署

推送到 `main` / `master` 后，GitHub Actions 使用 `uv.lock` 安装依赖，通过测试和构建检查后部署 GitHub Pages。PR 仅运行构建检查，不部署。
