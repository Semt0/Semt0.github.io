# Semt0's Blog

个人博客与学习笔记：[semt0.github.io](https://semt0.github.io/)。使用 Zensical 构建，文章以 Markdown 保存，GitHub Actions 自动部署到 GitHub Pages。

主页展示个人介绍、CodeTime、求学经历与内容入口；博客、笔记、手记各自提供时间线，友链页承载首页原有留言。全站共用纸白／深色主题、玫瑰色强调、中文字体和响应式布局，支持搜索、KaTeX 数学公式和 Waline 评论。

## 本地开发

需要 Python 3.13+、uv；运行前端回归测试还需要 Node.js 22+。以下命令从仓库根目录执行：

```bash
git clone https://github.com/Semt0/Semt0.github.io.git
cd Semt0.github.io
uv sync --frozen
bash update.sh
uv run zensical serve
```

预览地址以终端输出为准。使用完整检出可同时预览文章图片与 PDF；稀疏检出若排除了 `pictures/` 或 `slides/`，本地会缺少这些资源。

`bash update.sh` 统一更新三个板块的时间线，并补齐博客、笔记的导航。新增文章或修改元数据后先运行它；预览服务器不会自动执行生成器。`bash update.sh --check` 只检查是否过期，不写文件。

## 写作与页面配置

在 `docs/blog/`、`docs/note/<科目>/` 或 `docs/essay/` 新建 Markdown，填写 `title` 和 `date: YYYY-MM-DD`，运行生成器后检查导航和预览。详细模板、公式与插图规范见 [CONTRIBUTING.md](CONTRIBUTING.md)。

- 时间线按日期从新到旧排列，同日按路径稳定排序；无有效日期的文章排在末尾。
- 导航保留人工顺序和显示名称，只补充缺失文章。新科目默认使用目录名，之后可在 `zensical.toml` 调整名称和顺序；删除或移动文章时还需手动清理旧导航项。
- 文章路径决定 URL 和评论归属。迁移文章时需同时处理旧链接与评论键。
- `comments: false` 关闭单页评论。首页已关闭，友链页设置 `comment_path: /` 继续展示原首页留言；其他页面默认使用访问路径作为评论键。

## 维护入口

| 内容 | 文件 |
|---|---|
| 站点标题、导航、主题开关、资源顺序 | [zensical.toml](zensical.toml) |
| 首页介绍、头像、CodeTime、求学经历 | [docs/index.md](docs/index.md) |
| 友链与留言归属 | [docs/friends.md](docs/friends.md) |
| 全站颜色、字体、正文、导航和移动端规则 | [theme.css](docs/stylesheets/theme.css) |
| 首页布局与装饰动画 | [home.css](docs/stylesheets/home.css) |
| 时间线、友链与公共内容组件 | [components.css](docs/stylesheets/components.css) |
| 评论区主题 | [comments.css](docs/stylesheets/comments.css) |
| 模板、外部资源、图标和评论维护细节 | [OVERRIDES.md](OVERRIDES.md) |
| 索引与可选资源工具 | [scripts/README.md](scripts/README.md) |
| 自动检查与浏览器验收范围 | [tests/README.md](tests/README.md) |

首页头像使用 GitHub 头像，名称文字为 Semt0。CodeTime 使用远端动态徽章，不在仓库中维护时长数值。浏览器标签图标和导航标志使用本地 `docs/images/avatar-icon.svg`，以方形视口聚焦原画脸部；修改原始 JPEG 不会自动更新 SVG 内嵌图像。

## 项目结构

```text
docs/                       文章、页面和静态资源
  blog/                     博客
  note/                     按科目组织的学习笔记
  essay/                    手记
  images/                   站点图标等公共图片
  javascripts/              公式渲染与评论初始化
  stylesheets/              全站主题、首页、组件、评论样式
  vendor/waline/            固定版本客户端、许可证与校验记录
overrides/                  最小模板覆盖，不存放 Markdown 文档
scripts/
  update_site.py            时间线与导航生成器
  check_site.py             构建产物检查
  assets/                   PDF、图片、速查表工具
  figures/                  文章插图生成源码
tests/                      Python / Node 回归测试
uv.lock                     构建及可选工具依赖锁定
site/                       构建产物，不提交、不手动编辑
```

普通构建只安装站点依赖。需要 PDF 或绘图工具时使用 `uv sync --frozen --group assets`，执行脚本时同样指定 `uv run --group assets`，用法见工具说明。

## 检查与发布

提交前运行与 CI 对应的检查：

```bash
uv sync --frozen
bash update.sh --check
uv run python -m unittest discover -s tests -p 'test_*.py'
node --experimental-vm-modules --test tests/*.test.mjs
uv run zensical build --clean
uv run python scripts/check_site.py
git diff --check
```

修改前端后还需按 [浏览器验收清单](tests/README.md#浏览器验收) 检查桌面／手机、浅色／深色和页面切换。自动检查不验证线上评论后端、远端徽章或所有历史文章图片。

推送到 `main` / `master` 后，[Documentation 工作流](.github/workflows/docs.yml) 先安装锁定依赖、检查生成内容、运行测试并构建，再部署 Pages；PR 执行同样的构建检查但不部署。以 [Actions](https://github.com/Semt0/Semt0.github.io/actions) 对应提交的部署结果确认发布成功，构建失败时先查看失败步骤的日志。
