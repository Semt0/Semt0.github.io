# 检查范围

```sh
pnpm build
pnpm check:site
git diff --check
```

`pnpm build` 执行 Astro 类型诊断并构建静态站点。`pnpm check:site` 对当前 Markdown（含新增文章）生成独立审计，再检查构建结果：文章与标签分页、草稿排除、公式、提示框与折叠状态、图片与本地链接、目录目标、旧链接与旧书签、RSS、搜索、栏目背景、友链、项目和贡献热力图。

检查无需相邻的旧博客、Fuwari 试版或忽略的原图缓存。原文快照与迁移资源哈希仍会验证；普通编辑不要求正文与迁移当天完全相同。需要重做迁移原样验收时可用 `python3 scripts/check-site.py --migration`。

前端改动还需在浏览器抽查桌面和手机、浅色和深色、长公式横向滚动、折叠证明、代码标签切换和中文搜索。评论后端、GitHub 热力图刷新和 CodeTime 属于外部服务，需要单独检查，构建成功不代表其随时在线。

部署通过后，以对应提交的 Actions `build` / `deploy` 成功和线上网址实际页面确认。历史迁移和浏览器验收记录保存在 `migration/verification.md`。
