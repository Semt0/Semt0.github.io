# 主题与前端维护

站点布局沿用 Zensical，只覆盖资源引入和评论挂载。构建与发布见 [README](README.md)。

## 模板边界

| 文件 | 职责 |
|---|---|
| `overrides/main.html` | 继承 `base.html`，覆盖 `extrahead` 区块 |
| `overrides/partials/extrahead.html` | 字体、KaTeX 样式和自动渲染依赖 |
| `overrides/partials/comments.html` | 唯一的 Waline 挂载点，读取页面评论开关和稳定路径键 |

不要复制整份 `partials/content.html` 来插入评论。此说明放在仓库根目录；不要在 `overrides/` 内放 Markdown 文档，Zensical 0.0.23 会将其当成内容处理，可能覆盖首页。

## 全站样式

`zensical.toml` 按以下顺序加载样式：Waline 上游 CSS → `theme.css` → `home.css` → `components.css` → `comments.css`。保留该顺序，使站点覆盖在上游样式之后生效。

- `theme.css` 是设计变量的唯一入口：`--site-*` 定义纸色、文字、强调色、表面色、边框与语义提示色，并映射到 Zensical 的变量。浅色与 `slate` 深色都需维护。
- 搜索弹窗和移动端抽屉使用继承的 `--color-*`、`--md-text-font-family` 等变量。RGB 通道变量使用空格分隔的数值，不能直接替换成十六进制颜色。不要另行注入搜索组件的 Shadow DOM 样式。
- `home.css` 只负责主页布局与动画；`components.css` 负责时间线和友链等公共组件；`comments.css` 将同一组主题变量映射到 Waline。
- 宽表格和长公式在各自区域横向滚动；不让正文撑宽整个手机页面。装饰动画遵守 `prefers-reduced-motion`，内容默认可见。

## 头像与外部资源

首页头像来源是 `docs/index.md` 中的 GitHub 图片地址，头像下方名称也是该页的正文。CodeTime 为远端动态图片，账户与徽章地址在同一文件中设置，不能将当前时长写成固定文本。

浏览器图标和导航标志由 `zensical.toml` 的 `favicon` / `logo` 共用 `docs/images/avatar-icon.svg`。SVG 内嵌原始 `logo-emilia.jpg`，用 `viewBox="300 150 480 480"` 聚焦脸部，输出为 64 × 64 的方形图标。原图保留；更新 JPEG 后需同步替换 SVG 内嵌图像，调整视口时还应检查 16 / 32 像素下的识别度。修改文件名后同步更新两个配置项，避免继续命中旧图标缓存。

字体和 KaTeX 仍从外部服务加载；本地托管 Waline 不代表整个站点离线可用。KaTeX 的 CSS、主脚本和自动渲染脚本使用相同精确版本，更新时同步校验 SRI。正文渲染入口是 `docs/javascripts/katex.js`，限制在 `.md-content__inner` 内并跳过 `.katex-ignore`、已渲染公式。

## Waline 评论

客户端 JS / CSS 存放于 `docs/vendor/waline/`，保留上游许可证，版本、来源与 SHA-256 记录在 `PROVENANCE.txt`。升级时一并替换客户端文件、更新校验记录并运行 Node 回归测试。

`docs/javascripts/waline-init.js` 中的 `serverURL` 指定评论后端；仅托管客户端不会替代后端服务。模板通过 URL 过滤器提供本地模块地址，初始化脚本按需动态导入、复用模块加载结果，并在 Zensical `document$` 切页时销毁旧实例。异步加载完成后会核对页面标识，避免把评论挂到已经离开的页面。

`comments: false` 不生成挂载点。`comment_path` 可覆盖默认 `window.location.pathname`：首页关闭评论，友链使用 `/` 继承原首页留言；其他文章保持原 URL 键。不要通过统一截断或解码路径改变已有评论归属。

排查时分别确认挂载点、本地客户端响应和后端请求。模块加载失败会显示刷新提示；线上后端可用性需通过浏览器验证，单元测试不会连接后端。完整验收清单见 [tests/README.md](tests/README.md#浏览器验收)。
