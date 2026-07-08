# overrides

## 1 用途

Zensical / Material for MkDocs 主题模板覆盖与扩展目录。

## 2 内容清单

| 文件 | 用途 |
|------|------|
| `main.html` | 扩展 `base.html` 的 `extrahead` 块，注入带 SRI 的外部 CDN 资源 |
| `partials/content.html` | 覆盖主题 `partials/content.html`，在页面内容后注入 Waline 评论区 |
| `partials/extrahead.html` | 集中加载 KaTeX、Waline、字体等外部资源，并配置 `integrity`/`crossorigin` |

## 3 规则与约定

- 覆盖文件需与主题原始模板路径对应。
- 修改前建议先复制主题原始模板，再在明确位置插入自定义内容，避免丢失主题升级带来的功能。
- 新增覆盖模板时，需在本文件和 [`OVERRIDES.md`](../OVERRIDES.md) 中同步说明用途。

## 5 扩展指南

新增覆盖模板时：
1. 在 `overrides/` 下保持与主题模板相对路径一致的文件路径。
2. 说明覆盖的原始模板版本与修改点。
3. 更新本文件和 [`OVERRIDES.md`](../OVERRIDES.md) 的内容清单。
