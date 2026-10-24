# 内容写作

本地运行和发布见 [README](README.md)。全部内容放在 `src/content/blog/`，新增文章后自动生成列表、标签、归档和 RSS，不需要手动维护导航或运行旧生成器。

## 文章模板

推荐使用 `pnpm new <slug> --title "标题"`，也可以直接新建文件：

```yaml
---
title: 文章标题
description: 用一两句话概括内容，不超过 160 个字符。
publishDate: '2026-10-24'
tags: [博客]
draft: true
language: 中文
# updatedDate: '2026-10-25'
# comment: false
---
```

标题不超过 60 个字符。开发服务器显示草稿，正式构建排除草稿；准备发布时设置 `draft: false`。修改已有文章可设置 `updatedDate`，RSS 仍以首次发布时间为准。

不要在正文重复一级标题，也不要手写目录。正文用 `##`、`###` 组织章节，目录会自动生成。

## 课程笔记

```sh
pnpm new ode/06 --title "第六章：课程笔记"
```

课程文件夹仅帮助保持路径清晰，页面仍属于统一的 Blog。标签保留两个，例如 `[数学, ode]`、`[数学, 复变函数]`、`[计算机, rust]`。课程映射集中在 `src/data/course-tags.json`。

脚本可以通过 `--course` 接受完整课程名称或短标签；新课程先加入映射，再用 `--course` 指定。自动生成的 `order` 可以调整，用来确定同日章节的顺序。

保留资料来源，区分课件或教材的内容与自己补充的理解；适当提供图示、推导与例题。参考资料放在正文中，方便读者直接看到。

## 数学公式

行内用 `$...$`，块级用独占一行的 `$$`，前后留空行。

````markdown
由 $a^2+b^2=c^2$ 可得：

$$
f(x)=\int_0^x t^2\,\mathrm{d}t.
$$
````

Markdown 表格里的公式不要直接写 `|`，使用 `\lvert x\rvert`、`\lVert x\rVert` 等 TeX 命令，避免被识别为分栏符。不要把公式包在粗体标记中。

## 提示框与证明

```markdown
:::study-note[定义]{kind="abstract"}

这里是定义。

:::

:::study-proof[证明]{kind="note" open="true"}

这里是默认展开的证明。

:::
```

省略 `open="true"` 时默认折叠。常用 `kind` 为 `abstract`、`note`、`tip`、`info`、`warning` 和 `example`。

嵌套时，外层使用更多冒号，例如外层 `::::study-note`、内层 `:::study-proof`，各自用相同数量的冒号结束。代码示例需要按语言分组时，连续使用 `:::study-tab[Python]`、`:::study-tab[C++]`，会自动生成可键盘切换的标签页。

代码块写明语言，例如 `python`、`cpp`、`rust`、`cuda`。列表前留空行；不要在空列表项后隔着空行放缩进图片，这容易被 CommonMark 当成代码。

## 插图与附件

文章附近的图片使用相对路径，例如 `![说明](./images/figure.png)`。Astro 会处理这些图片。也可以将资源放在 `public/images/<文章名>/` 或 `public/files/<课程>/`，通过 `/images/...`、`/files/...` 引用。

使用明确的替代文本。公共资源地址不包含 `public` 前缀，也不要使用旧版 `{ width="800" }` 属性语法。需要精确宽度时使用普通 HTML `<img src="/images/example.webp" alt="说明" width="800">`。

## 已有链接与评论

文章文件路径决定 URL。不要直接改名已经发布的文章；确需移动时，在 `src/legacy-note-redirects.json` 中保留旧地址，并检查历史章节书签。

迁入文章的 `sourcePath`、`commentPath` 用于来源追踪和历史评论关联，编辑正文时保留这些字段。新文章无需手动填写。Links 留言区的 `/` 是原首页留言键，普通文章不要复用。

## 提交前

```sh
pnpm build
pnpm check:site
git diff --check
```

本地检查正文、目录、公式、图片和手机排版。使用 `pnpm dev` 查看草稿，使用构建后的预览验证搜索。确认要发布的文章已经设置 `draft: false`，再提交并推送。
