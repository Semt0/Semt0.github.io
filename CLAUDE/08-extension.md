# 扩展指南

← [返回 CLAUDE.md 入口](../CLAUDE.md)

本节说明新增内容时如何维护索引文件与 `CLAUDE.md`。

## 10.1 新增一个科目

1. 创建 `docs/note/<subject>/` 目录。
2. 创建 `.claude/indexes/docs/note/<subject>/README.md`（按目录 README 模板填写）。
3. 在 `.claude/indexes/docs/note/README.md` 中加入该科目链接。
4. 在根 `README.md` 的科目索引表中加入一行。
5. 在 `zensical.toml` 的 `nav` 中添加科目导航。
6. 运行 `bash update.sh`。

## 10.2 新增一篇笔记

1. 在对应科目目录下创建 `.md` 文件。
2. frontmatter 至少包含 `title` 与 `date`，推荐补充 `summary`、`key_points`、`sources`。
3. 如笔记开启新章节 / 新主题，更新 `.claude/indexes/docs/note/<subject>/README.md` 的内容清单。
4. 将文件路径加入 `zensical.toml` 对应科目的 `nav`。
5. 运行 `bash update.sh`。

## 10.3 新增一篇博客 / 手记

1. 在 `docs/blog/` 或 `docs/essay/` 创建文件。
2. 更新对应目录的 Agent 索引 `.claude/indexes/docs/<dir>/README.md`（必要时）。
3. 运行 `bash update.sh`。

## 10.4 新增一个脚本

1. 放入 `scripts/`。
2. 在 `scripts/README.md` 中登记脚本名、用途、触发方式。
3. 如脚本需要在 CI 中运行，更新 `.github/workflows/docs.yml`。
4. 如脚本影响构建流程，更新 `CLAUDE.md` 第 5 节“内容更新工作流”。
5. 运行 `bash update.sh`。

## 10.5 当索引文件超过 300 行

**注意：此阈值只针对索引文件（`CLAUDE.md`、`README.md`、各科 `README.md` 等），笔记正文没有行数限制。**

当某个索引文件超过 300 行时，按以下方式树形分解：

1. 创建与文件名同名的子目录（去掉 `.md`）：
   - `CLAUDE.md` → `CLAUDE/`
   - `README.md` → `README/`
   - `.claude/indexes/docs/note/计算方法/README.md` → `.claude/indexes/docs/note/计算方法/README/`
2. 将章节拆分为编号文件，例如：
   - `CLAUDE/01-overview.md`
   - `CLAUDE/02-rules.md`
   - `CLAUDE/03-templates.md`
3. 原文件瘦身为入口，只保留标题、一句话摘要和目录链接。
4. 子文件之间保留“← 返回入口”和“→ 下一节”链接。
5. 更新上层索引中的链接。

## 10.6 笔记正文是否需要拆分

**不需要。** 笔记正文没有行数限制，本次也不会自动拆分任何现有笔记。如果未来某篇笔记作者自己觉得过长、希望拆分，可参照以下自愿规范：

- 按章节拆分为 `01-xxx.md`、`02-xxx.md` 等。
- 原文件保留为入口，链接到各章节。
- 更新 `zensical.toml` 导航和科目 `README.md`。

这不是强制要求。

## 10.7 不索引的内容

以下目录/文件属于原始素材或构建产物，不在其中维护知识索引：

- `site/`：构建产物。
- `docs/note/*/slides/*_extracted.txt`：PDF 讲稿 OCR 文本，原始素材。
- `docs/*/pictures/`、`docs/images/`：图片资源，只放极简说明或不放索引。

---

→ [返回 CLAUDE.md 入口](../CLAUDE.md)
