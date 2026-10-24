# 项目约定

这是 Astro Theme Pure 博客，正式网址为 https://semt0.github.io/。构建、写作和发布以 README.md 与 CONTRIBUTING.md 为准。

- 所有文章放在 `src/content/blog/`，用 `publishDate` 排序。课程笔记统一使用 `src/data/course-tags.json` 中的两个标签。
- 写作入口为 `./write` / `pnpm write`。内容类型、默认目录和课程目录在 `src/data/writing.json`，新课程由脚本自动登记；新标签不需要白名单。改动写作工具后运行 `pnpm test:writing`，自动化单元测试不得打开真实应用或改动已有笔记。
- 保留已发布文章的地址。移动文章时维护 `src/legacy-note-redirects.json` 和旧章节书签映射；保留迁入文章的 `sourcePath`、`commentPath`。
- 本地开发可看草稿，生产构建排除 `draft: true`。不得把草稿写入正式列表、RSS 或搜索索引。
- `migration/originals/` 与来源哈希是不可变快照；正常写作只改 `src/content/blog/`。日常检查应允许新增文章及编辑旧文，不能要求相邻试版、旧仓库或未提交的资源缓存。
- 公式用 `$` / `$$`，提示框用 study-note，折叠证明用 study-proof；保留默认展开状态。表格公式避免未转义竖线。
- About 保持中文五行，界面与专业名称使用英语；首页保留 CodeTime、PKU 教育卡片、GitHub 项目与贡献热力图。
- 图片、背景和标识保留来源记录。原课件截图是无损 WebP，PDF 为原件。
- Waline 沿用原服务，迁入文章使用原评论路径，Links 留言键为 `/`；本地不初始化评论组件，销毁离开页面的实例。
- `dist/`、`.astro/`、`node_modules/` 是生成内容，不提交。不要恢复旧 Zensical 生成器或旧 CI。
- 修改代码后运行 `pnpm build`、`pnpm check:site`、`git diff --check`。修改 Markdown 插件后先 `pnpm exec astro sync --force`。前端改动检查桌面、手机及深浅主题。
- 部署使用 `.github/workflows/pages.yml`；推送后以对应提交的 GitHub Actions 成功及线上页面验证确认发布。
