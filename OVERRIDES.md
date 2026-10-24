# 主题维护

站点基于 Astro Theme Pure 4.1.6 / astro-pure 1.4.9，实际依赖以 `pnpm-lock.yaml` 为准，上游 Apache-2.0 许可证保留在 LICENSE。

自定义页面、布局与样式位于 `src/`。`packages/pure/` 保留上游主题源码供参考，运行时使用锁定的 `astro-pure` npm 包；不要直接修改 `node_modules/`。

- `ContentPreview.astro`：文章卡片和精简标签。
- `BlogPost.astro`、`ContentLayout.astro`：文章、目录和移动端侧栏。
- `StudyTabs.astro`：渐进增强的代码标签页；无 JavaScript 时内容仍可读。
- `remark-study-blocks.ts`：定义、提示与折叠证明。
- `rehype-auto-link-headings.ts`：标题锚点，以及去除数学目录文字的重复表现。
- `legacy-redirects.ts`：静态旧地址跳转，保留查询参数与章节书签；脚本数据按 ASCII 转义，页面声明 UTF-8。
- `search-language.ts`：为主要为中文的语料保留 Pagefind 中文分词。
- `components/waline/`：本地打包客户端，保留原评论路径，按需初始化与清理。

栏目背景通过 `src/data/backgrounds.ts` 配置，使用构建生成的 WebP 和 CSS 渐隐。PKU 校徽保持原 SVG，来源记录见 `migration/pku-asset.json`。

升级主题前提交当前改动，按上游说明比较必要差异，再运行构建和内容检查。检查迁入长文中的公式、折叠证明、图片、代码标签，以及旧章节书签。修改 Markdown 插件后先清理 Astro 内容缓存。
