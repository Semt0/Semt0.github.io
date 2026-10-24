# 日常工具

- `pnpm new <slug> --title "标题"`：创建草稿，可自动识别已有课程目录，`--course` 可显式指定课程。
- `pnpm check:site`：审核当前文章并检查正式构建；新增内容与正常编辑都受支持。
- `python3 scripts/update-github.py`：手动刷新公开贡献日历快照。

原 Zensical 导入、原图转码和旧标题映射工具在 `migration/tools/`，它们属于一次性迁移流程，日常写作不需要运行。不要用导入工具覆盖手工编辑后的文章。
