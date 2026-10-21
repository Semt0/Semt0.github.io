# 维护工具

所有示例从仓库根目录执行。普通站点维护使用默认依赖；PDF、图片和绘图工具使用可选 `assets` 依赖组。

## 内容与构建

```bash
bash update.sh                 # 更新索引与缺失导航
bash update.sh --check         # 只检查，过期则非零退出
uv run zensical build --clean
uv run python scripts/check_site.py
```

`update.sh` 转发参数给 `update_site.py`。生成器扫描 `docs/blog/`、`docs/note/`、`docs/essay/` 的 Markdown，跳过 `index.md` 和 `README.md`，写入三个索引的 `timeline:auto-begin` / `timeline:auto-end` 区域及 `zensical.toml` 的 `nav:auto-begin` / `nav:auto-end` 区域。

标题优先取 YAML `title`，手记还可回退到正文首个标题，最后使用文件名。日期优先取 `date`，兼容旧字段 `data`；手记无有效日期时尝试从文件名解析。排序使用日期与路径的降序，不读取文件修改时间。无日期文章显示“未标日期”。

导航只补齐博客、笔记的缺失条目，保留人工分组、名称和顺序；手记仍通过时间线访问。删除或移动文章后需手动清理旧导航项。标记缺失、重复或顺序错误时生成器会报错，不应通过删除标记绕过检查。

`check_site.py` 在构建完成后检查页面路由、评论开关与归属、首页结构、时间线数量、本地脚本／样式及入口页链接。详细覆盖边界见 [tests/README.md](../tests/README.md)。

## 可选资源工具

```bash
uv sync --frozen --group assets
```

| 脚本 | 调用方式与用途 |
|---|---|
| `assets/export_pdf_pages.py` | `source.pdf output/ --page 3:figure.png`，导出指定页为 PNG |
| `assets/check_pages.py` | `source.pdf`，查看 PDF 页数 |
| `assets/extract_pdf_text.py` | `source.pdf output/`，按页提取文本至 `page_001.txt` 等文件，不做 OCR |
| `assets/compress_images.py` | `pictures/`，递归压缩目录中的图片，原地更新文件 |
| `assets/generate_cheatsheet.py` | `input.json output.pdf`，生成四栏速查表，额外需要 Pandoc 和 XeLaTeX |

表中的参数须放在 `uv run --group assets python scripts/<脚本>` 后面，例如：

```bash
uv run --group assets python scripts/assets/export_pdf_pages.py \
  docs/note/subject/slides/source.pdf docs/note/subject/pictures \
  --page 3:figure_03.png --page 7:figure_07.png
```

PDF 导出默认按 1-based 页码解释，`--base 0` 可改用 0-based；`--zoom` 默认 6.0，输出不带透明通道。已有同名图片需显式加 `--overwrite` 才会覆盖。图片压缩默认目标为 1,000,000 字节、最大宽度 1600 像素；结果仍可能超出大小目标，应查看脚本汇总和实际画质。

`figures/` 保留复变函数、数值计算、视觉识别和具身智能文章的插图生成源码。两个 recognition 脚本输出不同的教学图，均保留。执行前查看脚本输出路径，确保对应 `pictures/` 目录存在，再使用 `uv run --group assets python scripts/figures/<脚本>.py`。这些工具不参与站点 CI 构建。
