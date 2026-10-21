# 维护工具

所有命令从仓库根目录执行。

- `update_site.py`：一次扫描文章，统一解析 YAML、生成时间线、补齐导航；`--check` 检查生成内容是否过期。
- `check_site.py`：构建后核对文章路由、单页评论开关、唯一评论容器、脚本/样式资源和索引链接。

`assets/` 中的工具按需运行，使用 `uv run --group assets python scripts/assets/<脚本>.py`：

| 脚本 | 用途 |
|---|---|
| `export_pdf_pages.py` | 从 PDF 导出 PNG；`--page 页码:文件名`，默认 1-based，支持 `--zoom`、`--overwrite` |
| `check_pages.py` | 查看 PDF 页数 |
| `extract_pdf_text.py` | 提取 PDF 文本 |
| `compress_images.py` | 压缩图片 |
| `generate_cheatsheet.py` | JSON → 四栏速查表，额外需要 Pandoc 和 XeLaTeX |

`figures/` 保留复变函数、数值计算、视觉识别和具身智能文章的插图生成源码。两个 recognition 脚本输出不同的教学图，均保留。它们使用相对仓库根目录的输出路径，运行前确保相应 `pictures/` 目录存在。

已合并原来的 6 个 `update_*` 入口；`update.sh` 是统一入口。已删除无对应页面的卡片计数逻辑、依赖未入库 Agent 索引的检查、重复 PDF 导出器及已完成的一次性文章修补脚本。
