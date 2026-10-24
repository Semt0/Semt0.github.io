# 原站迁移工具

日常写作见根目录 README，这些工具不参与构建或 GitHub Actions。

原站提交与内容快照、资源哈希在 `migration/report.json`；旧版标签为 `pre-astro-pure-2026-10-24`。需要重新研究迁移过程时，可另外检出旧版，向 `import-preview.py` 显式提供 `--source /path/to/old-blog`。脚本不能把当前新站当成旧来源。

`optimize-assets.mjs` 对迁移资源进行无损转码，原 PNG 缓存在被忽略的 `migration/asset-cache/`。正式站点只需要已提交的 WebP 和 PDF，不需要这个缓存。

`update-legacy-headings.mjs /path/to/old/site` 对比旧站已构建 HTML，重新生成旧章节书签映射并刷新当前 `dist/` 中的跳转文件。已有的 2,899 个映射已经随源码提交，普通新增文章不需要重跑。

工具需要原环境的相关 Python 依赖（例如 PyYAML）与本项目 Node 依赖。上游试版锁文件、迁移原文和当时的验收记录保留作为历史依据。
