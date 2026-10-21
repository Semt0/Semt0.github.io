# 主题覆盖

- `main.html`：通过 `extrahead` 区块引入资源；其余布局沿用 Zensical。
- `partials/extrahead.html`：字体和 KaTeX。带 SRI 的资源必须固定精确版本，文件更新后同步校验值。
- `partials/comments.html`：唯一的 Waline 挂载点，遵守 `comments: false`，预先设置 `katex-ignore` 避免数学自动扫描干扰评论。

Waline JS / CSS 固定版本存放在 `docs/vendor/waline/`，来源及校验值见 `PROVENANCE.txt`。样式由站点配置引入，评论模板通过 URL 过滤器生成模块路径，兼容子路径部署。Waline ESM 由 `docs/javascripts/waline-init.js` 按需加载，不再额外作为普通 script 引入。不要覆盖整份 `partials/content.html` 来插入评论。

此说明放在仓库根目录；不要在 `overrides/` 内放 Markdown 文档，Zensical 0.0.23 会将其当成内容处理，可能覆盖首页。
