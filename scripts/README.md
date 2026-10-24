# 日常工具

- `./write` / `pnpm write`：交互新建草稿；也可用 `--type`、`--course`、`--tags` 等参数，自动归档、打开 Typora 和浏览器实时预览。原 `pnpm new` 兼容。
- `pnpm write --list` / `--help`：查看类型、课程、标签和完整参数。
- 新课程用 `--course 测度论 --subject 数学 --folder measure-theory` 自动登记，不需要事先改 JSON；普通文章的新标签直接传入。
- `pnpm live [ode/05]`：启动或复用实时开发预览；`--stop` 只停止由写作脚本启动的服务。
- `pnpm test:writing`：测试归档、标签、课程登记、文件冲突与路径保护，不启动桌面应用。
- `pnpm check:site`：审核当前文章并检查正式构建；新增内容与正常编辑都受支持。
- `python3 scripts/update-github.py`：手动刷新公开贡献日历快照。

原 Zensical 导入、原图转码和旧标题映射工具在 `migration/tools/`，它们属于一次性迁移流程，日常写作不需要运行。不要用导入工具覆盖手工编辑后的文章。
