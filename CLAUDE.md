# 项目约定

构建、目录结构和命令以 [README.md](README.md) 为准；写作模板见 [CONTRIBUTING.md](CONTRIBUTING.md)。

- 保留文章路径与内容；路径同时决定站点 URL 和评论归属。
- 不手动编辑 `site/` 或 `<!-- ...:auto-begin -->` / `auto-end` 内的生成内容，运行 `bash update.sh`。
- 导航保留人工顺序和科目显示名称；生成器只补充缺失条目。
- 自定义脚本须支持 Zensical 的 `document$` 切页事件和普通页面加载；异步初始化不得挂载到过期页面。
- 内容默认可见，动画只做渐进增强，遵守 `prefers-reduced-motion`。
- 全站视觉变量集中在 `theme.css`，页面布局复用 `--site-*`；同时检查浅色、深色与移动端。外部服务是否可用需单独验证。
- 仅覆盖必要主题局部模板，避免复制主题正文模板。`overrides/` 内不放 Markdown，维护说明写在根目录 `OVERRIDES.md`。
- 首页关闭评论，友链保留 `comment_path: /`；不要改变文章原有评论路径键。Waline 升级时同步客户端、许可证与来源校验记录。
- 首页保留 CodeTime 动态徽章与 Semt0 名称；导航标志和 favicon 共用本地 `avatar-icon.svg`。
- 构建依赖属于默认环境；PDF、绘图工具依赖属于 `assets` 组。
- 完成改动后运行 README 中与改动相关的测试和构建检查；前端改动按 `tests/README.md` 做浏览器验收。结构或工作流改变时同步维护相关文档。
