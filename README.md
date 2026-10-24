# Semt0's Blog

个人博客、课程笔记与技术实践：**[semt0.github.io](https://semt0.github.io/)**。

基于 Astro Theme Pure，使用 Markdown 写作，推送到 `main` 后由 GitHub Actions 自动构建并部署到 GitHub Pages。界面使用英语，个人介绍和中文笔记保留中文。

## 本地运行

需要 Node.js 24（最低 22.12）和 pnpm 10.30.3；内容检查另需 Python 3.9+，仅使用标准库。已经安装 pnpm 时无需重复安装。

```sh
git clone https://github.com/Semt0/Semt0.github.io.git
cd Semt0.github.io
npm install -g pnpm@10.30.3
pnpm install --frozen-lockfile
pnpm dev
```

默认地址为 `http://127.0.0.1:4322`，端口占用时以终端显示的地址为准。保存文件后页面自动刷新。开发模式可以查看草稿；生产构建会排除 `draft: true` 的文章。

要检查正式构建及全文搜索：

```sh
pnpm build
pnpm check:site
pnpm preview --host 127.0.0.1 --port 4322
```

全文搜索由构建时生成的 Pagefind 中文索引提供，新增内容后需要重新构建才能更新搜索结果。

## 写一篇新文章

```sh
pnpm new my-first-post --title "我的第一篇博客"
```

会生成 `src/content/blog/my-first-post.md`，默认是草稿。编辑文章简介与正文，发布前把 `draft` 改成 `false`：

```yaml
---
title: 我的第一篇博客
description: 用一句话说明这篇文章讲什么。
publishDate: '2026-10-24'
tags: [博客]
draft: false
language: 中文
---
```

正文从二级标题开始，不用重复文章标题，也不用手写目录。文件路径决定文章地址，例如上面的文章发布到 `/blog/my-first-post`。文件名建议使用小写英文和短横线，文章标题可以使用中文。

也可以直接新建 Markdown，至少填写 `title`、`description`、`publishDate`。`publishDate` 用于排序，不是自动定时发布；是否进入正式站点由 `draft` 决定。

`draft: true` 隐藏的是网站页面；如果将草稿提交到这个公开仓库，Markdown 源文件仍然公开。

## 写课程笔记

```sh
pnpm new ode/06 --title "第六章：课程笔记"
```

脚本会识别 `ode` 课程目录，自动填入 `数学`、`ode` 两个标签和下一章的 `order`。所有课程笔记统一使用“学科 + 课程”两个标签，映射见 [course-tags.json](src/data/course-tags.json)。

其他例子：

```sh
pnpm new rust/lifetimes --title "引用与生命周期"
pnpm new foundation-models/training-notes --title "训练实践笔记"
```

新增课程时，先在 `src/data/course-tags.json` 添加课程名称与两个标签，再显式指定课程：

```sh
pnpm new measure-theory/01 --title "第一章：测度" --course "测度论"
```

`order` 用于同一课程、同一天的章节排序；日期相同的章节按照章节号从大到小显示。Blog、标签页、归档、首页最新文章和 RSS 自动生成，不需要再运行旧版的索引生成器。

## 图片、公式与折叠证明

图片可以放在文章附近，使用相对路径，交给 Astro 构建处理：

```text
src/content/blog/
  my-first-post.md
  images/
    experiment.png
```

```markdown
![实验结果](./images/experiment.png)
```

公共图片或 PDF 放在 `public/`，引用时去掉 `public` 前缀：

```markdown
![结构示意](/images/my-post/diagram.webp)
[下载课件](/files/my-course/slides.pdf)
```

行内公式用 `$...$`，块级公式前后留空行：

```markdown
由 $f'(x)=0$ 可以得到驻点。

$$
f(x)=x^2+2x+1
$$
```

提示框和折叠证明使用以下写法：

```markdown
:::study-note[定理]{kind="abstract"}

这里写定理。

:::

:::study-proof[证明]{kind="note"}

这里写证明，支持公式、代码和列表。

:::
```

需要默认展开时，在属性中加 `open="true"`。详细格式、嵌套写法和表格公式见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 发布到线上

```sh
pnpm build
pnpm check:site
git add src public
git commit -m "Add a new post"
git push
```

配置或文档也改动时，一并加入提交。推送后到 [Actions](https://github.com/Semt0/Semt0.github.io/actions/workflows/pages.yml) 查看对应提交的部署结果；`build` 和 `deploy` 均成功才表示已经发布。无需手动提交 `dist/`。

## 站点维护

| 想修改的内容 | 位置 |
| --- | --- |
| 文章与课程笔记 | `src/content/blog/` |
| 标题、导航、作者、日期格式、评论设置 | `src/site.config.ts` |
| About 五行介绍和英文专业名称 | `src/data/profile.ts` |
| 课程的两个标签 | `src/data/course-tags.json` |
| 友链 | `src/data/links.json`；头像在 `public/links/` |
| GitHub 代表项目 | `src/data/projects.json` |
| GitHub 热力图 | `src/data/github-contributions.json` |
| 各栏目背景和渐隐强度 | `src/data/backgrounds.ts` |
| 首页布局 | `src/pages/index.astro`、`src/assets/styles/home.css` |
| 旧链接和旧章节书签 | `src/legacy-note-redirects.json`、`migration/legacy-heading-map.json` |
| GitHub Pages 部署 | `.github/workflows/pages.yml` |

热力图使用真实 GitHub 贡献记录的本地快照。需要刷新时运行 `python3 scripts/update-github.py`，然后重新构建、提交。普通构建不依赖 GitHub 数据接口。

评论沿用原 Waline 服务。已迁移文章通过 `commentPath` 关联历史讨论，Links 页继续使用原首页的 `/` 留言键。新文章默认允许评论，用 `comment: false` 可以关闭单篇评论；本地预览不初始化评论区。

## 迁移记录

旧 Zensical 站点在 `pre-astro-pure-2026-10-24` 标签中完整保留，Git 历史没有重写。此次迁入 97 篇内容，包括 84 篇课程笔记、4 篇博客和 9 篇手记。

- 原始 Markdown 快照、资源哈希和稳定地址映射保存在 `migration/`。
- 原文章地址及 2,899 个旧章节书签继续跳转到对应的新页面。
- 课件 PDF 保持原件；课件截图改为尺寸不变的无损 WebP。两个原来缺失的示意图已补绘并记录来源。
- 旧导入工具放在 `migration/tools/`，日常写作无需运行，也不依赖相邻的旧仓库或试版目录。

构建与检查范围见 [tests/README.md](tests/README.md)，迁移验收记录见 [migration/verification.md](migration/verification.md)。修改 Markdown 插件后，先运行 `pnpm exec astro sync --force` 清理内容渲染缓存，再构建。

主题来自 [Astro Theme Pure](https://github.com/cworld1/astro-theme-pure)，保留上游 Apache-2.0 许可证；课件和图片保留各自来源。
