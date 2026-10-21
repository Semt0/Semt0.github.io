# 项目约定

构建、目录结构和命令以 [README.md](README.md) 为准；写作模板见 [CONTRIBUTING.md](CONTRIBUTING.md)。

- 保留文章路径与内容；路径同时决定站点 URL 和评论归属。
- 不手动编辑 `site/` 或 `<!-- ...:auto-begin -->` / `auto-end` 内的生成内容，运行 `bash update.sh`。
- 导航保留人工顺序和科目显示名称；生成器只补充缺失条目。
- 自定义脚本须支持 Zensical 的 `document$` 切页事件和普通页面加载；异步初始化不得挂载到过期页面。
- 内容默认可见，动画只做渐进增强，遵守 `prefers-reduced-motion`。
- 仅覆盖必要主题局部模板，避免复制主题正文模板。
- 构建依赖属于默认环境；PDF、绘图工具依赖属于 `assets` 组。
- 完成改动后运行 README 中与改动相关的测试和构建检查。
