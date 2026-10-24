# Pure 本地试用验收 · 2026-10-24

验收范围为与 Fuwari 样站相同的 10 篇文章：7 篇课程笔记、3 篇博客／手记。

- 上游模板提交：`4ecd4762e1e750daf7a51978092d7cea8e14c0d6`。
- `pnpm build` 通过；Astro 检查 130 个文件，0 错误、0 警告、0 提示。构建工具另有上游 Markdown 插件接口弃用提醒，当前仍可正常构建。
- 构建为静态站点，包含 25 个 HTML 文件；其中包含模板原有 `DocsContents` 部分页面。
- 10 份原文与快照 SHA-256 一致；导入正文与 Fuwari 样站的规范化 Markdown 保持一致。
- 49 份原始图片／PDF 哈希一致，本地图片与页面链接均有对应构建产物。
- 1,289 处数学表达式数量逐篇与 Fuwari 样站一致；构建 HTML 中未发现 KaTeX 错误。数学内容未重新审校。
- 9 个折叠证明／例题框保留，默认开闭状态与原稿一致；浏览器实际展开首个证明成功（打开数量从 1 变为 2）。
- 课程目录显示常微分方程 5 章与基础模型 2 篇，顺序正确；手机菜单可进入课程页。
- 中文搜索：实际在手机视图输入“梯度”，得到 Gradient Descent 与常微分方程第二章；点击后进入对应正文。
- 文档在桌面 1440×960 下显示课程目录、正文、文章目录三栏；中文长章节名已约束宽度，目录右边缘与正文之间有 24px 间隔。
- 首页在桌面 1280×900、手机 390×844 下检查；正文在手机 390×844 下检查，未造成整页横向溢出，长公式在自身容器内滚动。
- 深色阅读实际检查前景与背景，并恢复跟随系统。首页头像与 CodeTime 在本次浏览器中加载成功。
- 原博客工作区仍然干净；没有部署、提交或推送。

截图：`home-desktop.png`、`home-mobile.png`、`reading-desktop.png`、`proof-mobile.png`、`toc-mobile.png`、`reading-dark-mobile.png`。

未覆盖：完整历史内容迁移、旧 URL 重定向、正式评论接入、所有浏览器兼容性和长期维护。CodeTime 与图片放大库使用远端资源，其可用性取决于网络。

## Arthals 课程标签卡片调整

- 参考 `https://arthals.ink/tags/具身智能导论` 的公开页面结构，沿用同款 Pure 详细文章卡片：单列宽卡片、日期、标题与箭头、摘要、阅读时间、语言和标签按钮。
- `/docs` 汇总 7 篇笔记；`/tags/常微分方程` 聚合 5 篇、`/tags/基础模型` 聚合 2 篇。所有主题标签同时覆盖博客与课程笔记。
- 按发布日期倒序显示，同日同课程笔记按章节倒序显示。首页课程入口、正文返回链接和文档侧栏的课程名均连接到对应课程标签页。
- 构建检查 132 个文件，0 错误、0 警告、0 提示，共 40 个 HTML 页面。内容完整性检查继续通过：49 份资源、9 个折叠框、1,289 处公式与原样站一致。
- 新增渲染检查：每篇笔记在总列表中恰好出现一次，课程分组数量与目标链接正确，同日章节顺序正确。
- 实际浏览器检查 1280×900 与 390×844：桌面卡片 16px 圆角、20px 内边距，列表间距 12px；手机标签换行，整页无横向溢出。
- 实际测试：课程卡片 → 数学标签筛选 → 返回课程 → 笔记正文 → 返回所属课程 → 全部课程笔记 → 基础模型分类。
- 本轮截图：`course-cards-desktop.png`、`course-cards-mobile.png`。参考记录见 `card-reference.json`。

## 统一 Blog 与英文主页

- 10 篇文章已统一进入 `src/content/blog/`，课程通过标签组织；Blog 分页、Tags、Archives、RSS 与首页 Posts 均覆盖同一集合。
- 界面、主页介绍、日期格式和 About 文案改为英文；原文章标题、正文与课程标签保留原文。Blog 两页分别显示 8 篇、2 篇，无遗漏或重复。
- 旧 `/docs` 及 7 个笔记地址跳转到新 Blog 地址；旧笔记 RSS 地址继续提供统一 RSS。实际浏览器检查 Gradient Descent 的旧地址成功进入新正文，356 处公式、9 个折叠框均存在，未出现 KaTeX 错误。
- PKU 教育卡片加入本地校徽背景，来源与原文件哈希见 `pku-asset.json`；实际浏览器确认图片加载，浅色和深色下文字可读。
- 主页重新组织个人介绍、About、Education、最近 6 篇 Posts 和 Tags；1280×1000 桌面、390×844 手机检查通过，整页无横向溢出。主题已恢复跟随系统。
- 英文 HTML 默认搜索分词曾使“梯度”少返回一篇笔记；已单独保留中文内容分词。实际在英文搜索界面输入“梯度”，可找到 Gradient Descent 与常微分方程第二章，结果地址均为新 Blog 地址。
- 最终构建及内容检查通过，47 个 HTML 文件（包含旧地址跳转），10 份原文与规范化正文哈希保持一致，49 份原始资源、9 个折叠框、1,289 处公式均通过核对。RSS 可解析且包含全部 10 篇。
- 本轮截图：`home-english-desktop.png`、`home-english-mobile.png`、`home-english-dark.png`。

## Arthals 主页、Projects 与 GitHub 热力图

- 主页参考 `https://arthals.ink/` 的居中个人信息、左侧栏目名称和右侧内容布局。顺序为 About、Posts、Education、Projects、GitHub。教育卡片按用户截图改为灰底、细边框、圆角、大校徽裁切背景；保留 Semt0 自己的教育信息。
- 导航中 Projects 替代 Tags，主页独立标签分组移除。Blog 内的标签筛选与旧标签地址继续可用。
- 读取 GitHub 公开置顶仓库及各仓库 README，展示 Personal Blog、Self-Study、User-Space Network Stack、Language Models from Scratch。两个 fork 均链接其上游；网络实验简介仅描述已完成的 Ethernet 部分。
- GitHub 贡献数据来自公开端点 `https://github.com/users/Semt0/contributions`，本次记录覆盖 2025-10-19 至 2026-10-24，共 371 个连续日期、253 次贡献。每日计数与颜色等级保存在本地，页面显示更新时间；不依赖远端热力图图片。刷新入口为 `python3 scripts/update-github.py`。
- 构建检查 133 个文件，0 错误、0 警告、0 提示。48 个 HTML 文件；原有 10 篇文章、49 份资源、9 个折叠框、1,289 处公式及 RSS、重定向、搜索检查继续通过。新增检查核对项目链接、fork 来源及实际渲染的全部每日贡献计数。
- 浏览器检查 1280×1000 桌面、390×844 手机：主页无整页横向溢出，手机项目卡片为单列、热力图在自身容器内滚动；真实校徽成功加载。手机菜单可进入 Projects，显示全部四个项目。浅色与深色主页及深色手机 Projects 已检查，未捕获浏览器错误。
- 热力图刷新入口已实际联网运行成功；手机键盘右方向键使热力图容器横向滚动，整页宽度未变化。桌面 Projects 页面亦检查通过，主题已恢复跟随系统。
- 本轮截图：`home-arthals-desktop.png`、`home-arthals-mobile.png`、`home-arthals-dark.png`、`projects-dark-mobile.png`、`projects-desktop.png`。保持本地预览，未部署、提交或推送；原博客工作区仍干净。

## 主页渐变背景

- 增加淡紫、雾蓝、浅粉和薄荷色的柔和背景，头像渐变描边、名字渐变与淡网格；卡片使用半透明底色和轻阴影。背景由 CSS 绘制，不新增图片、远端请求或动画。
- 浅色与深色分别配置调色变量，装饰通过主页 body 类限制作用范围。高对比度模式提供纯色标题回退；原有内容、教育卡片和布局保留。
- 构建检查与内容检查通过。1280×1000 桌面、390×844 手机的浅色和深色实际检查通过，手机没有整页横向溢出。
- 截图：`home-gradient-desktop.png`、`home-gradient-mobile.png`、`home-gradient-dark.png`、`home-gradient-dark-mobile.png`。

## 中文简介、专业名称与蓝色淡出背景

- 主页 About 与独立 About 页共用一段中文介绍，文案集中在 `src/data/profile.ts`；独立页改为简洁的“关于我”，移除空目录侧栏。
- 专业名称改为 `Theoretical and Applied Mechanics (Engineering and Scientific Computing) + Computer Science and Technology`，两个专业在教育卡片内分行显示。
- CodeTime 已移至 GitHub、Email 下方，位于 About 上方；浏览器确认徽章实际加载，顺序正确且仅出现一次。
- 复用 Fuwari 试版生成的蓝白厚涂图，原始图像未改动，来源与哈希见 `home-background-provenance.json`。Astro 输出 1600px、约 197 KiB 的 WebP；背景在顶部以低透明度显示，向下淡出，浅深色分别调整透明度；其余渐变、名字与头像描边统一为蓝色系。
- 构建及完整性检查通过：10 篇文章、49 份原始资源、9 个折叠框、1,289 处公式，项目、热力图、RSS、重定向和搜索均正常。背景资源路径存在。
- 1280×1000 桌面、390×844 手机的浅色与深色实际检查通过，无整页横向溢出；专业名称完整显示。导航进入独立 About 页，确认只有一段中文正文。预览服务已恢复为本地 4322 端口，主题恢复跟随系统。
- 截图：`home-blue-fade-desktop.png`、`home-blue-fade-mobile.png`、`home-blue-fade-dark.png`、`home-blue-fade-dark-mobile.png`。

## 栏目独立背景与 Links

- 主页保留原蓝白厚涂图；Blog、Projects、Archives、About、Links 各加入一张不同的新背景，分别为海浪、几何层叠、远山、云层和交汇水纹。五张图由内置 imagegen 生成，原图、准确提示词、来源与哈希见 `section-backgrounds.json`。构建后的 WebP 分别约 146、138、121、99、124 KiB。
- 背景选择集中在 `src/data/backgrounds.ts`，渐隐与浅深色样式集中在 `src/assets/styles/backgrounds.css`，由基础布局统一加载。Blog 分页、标签筛选、搜索和文章正文继承 Blog 的背景。
- 新增 `/links` 及 Links 导航。原博客两位友链按原名称、介绍、网址迁入，头像本地保存；卡片数据在 `src/data/links.json`。页面提供交换友链的邮件入口。原 `/` 评论键仅记录为迁移元数据，评论服务仍关闭。
- 构建检查 136 个文件，0 错误、0 警告、0 提示。49 个 HTML 页面；全部原有文章、公式、资源、折叠框、RSS、搜索、重定向、项目与贡献图检查继续通过。新增检查核对六个主栏目图片各不相同、优化资源存在、子页面继承正确、友链和导航完整。
- 浏览器实际点击 Links 导航成功，两张本地头像均加载为 112px。1280×900 检查所有主栏目背景地址正确；390×844 检查手机菜单、友链单列、浅深色文字和背景；768px 检查新增导航及 Blog 排版，均无整页横向溢出。
- 手机深色下抽查 Gradient Descent，背景继承正确，356 处公式、0 个 KaTeX 错误，无整页横向溢出。主题恢复跟随系统。
- 截图：`links-background-desktop.png`、`links-background-mobile.png`、`links-background-dark-mobile.png`、`blog-background-dark-desktop.png`。

## About 五行排版

- 按用户最新文案显示五个独立段落，保留 Minecraft、Genshin Impact (逃) 与艾尔登法环：黑夜君临的写法；“欢迎 connect！”前增加间距，connect 连接现有邮箱。
- 主页与独立 About 页复用同一组件和文案。桌面、390px 手机实际检查：文字完整、段落顺序一致、自然折行，无整页横向溢出。构建、完整性检查与差异格式检查通过。
- 截图：`about-lines-desktop.png`、`about-lines-mobile.png`。预览服务以独立进程恢复，页面可访问。

## Full original-blog migration — 2026-10-24

Scope: all 97 article Markdown files in the original blog's `docs/note/`, `docs/blog/`, and `docs/essay/`; 84 course notes across 13 course groups, 4 blog posts, 9 journal entries. Generated landing pages are replaced by Blog, course tags, and Archives. This does not import other local/private study vaults or deploy the site.

The repeatable importer reads the original Git commit and records original text hashes, normalized body hashes, source paths, original comment paths, stable English routes, and asset hashes. Markdown snapshots remain byte-for-byte copies. `migration/content-map.json` freezes routes independently of future navigation order. Locally edited imported articles are protected on subsequent imports unless `--force` is explicitly supplied.

Compatibility includes MkDocs callouts and default-open/collapsed proofs, nested containers, 19 tab panels with keyboard-accessible progressive enhancement, inline highlights, original TeX, fenced code, internal article links, local images, and PDF attachments. Original article URLs and earlier Pure `/docs` trial URLs redirect to the canonical Blog routes. Static redirects preserve query strings and map all 2,899 original section bookmarks to existing canonical heading IDs. The mappings were matched by heading text and order against the original built site, with zero unmatched headings; they are stored in `migration/legacy-heading-map.json`. Existing comment paths remain in metadata; comments stay disabled in the local preview.

The original Git tree lacked `complex_plane.svg` and `connected_domain.svg`. Two new explanatory SVG diagrams fill those references, with provenance in `migration/repaired-diagrams.json`; they are not claimed as recovered originals.

All referenced source resources are checked against their source Git blob IDs and SHA-256 records. PNGs are converted to lossless WebP with original dimensions retained. Original PNGs are kept in the ignored `migration/asset-cache/`; their immutable upstream commit and hashes permit restoration. PDFs are copied unchanged. Optimization metadata and output hashes are in `migration/optimized-assets.json`.

`node scripts/audit-markdown.mjs` records independent Markdown AST formula/container/code counts. `scripts/check-preview.py` checks complete source coverage, source/body/asset integrity, rendered formula counts and KaTeX errors, proof states, callout and panel counts, fenced-code preservation (ignoring blank-line/trailing whitespace), every tag across pagination, Blog and archive membership, RSS destinations, redirects, search, and prior homepage features. The original ten-article trial remains a rendering baseline where a Fuwari build exists.

RSS contains all article titles, dates, descriptions, categories, and canonical links. It uses summaries to keep an archive of long mathematical notes practical for feed readers.

The full migration also normalizes 550 legacy TeX delimiter pairs, protects 12 table formulas from Markdown pipe splitting, and fixes 7 empty ordered-list items whose indented images/text otherwise became code in CommonMark. Original TeX meanings and snapshots remain preserved. A 97-page original-rendering baseline prevents a migrated article from silently rendering fewer formulas than the original blog. Every referenced article image is counted against the rendered HTML. Math labels in the article TOC are extracted once instead of repeating KaTeX accessibility/visual representations.

### Final migration verification

- 97 articles; 1,077 original resources; 1,059 rendered image references; 1,070 callouts including 215 disclosures; 19 tab panels; 14,634 rendered formulas; zero KaTeX render errors.
- 108 legacy route mappings and 2,899 old heading bookmarks, with no unmatched original headings. Redirect HTML declares UTF-8 and escapes JavaScript data to preserve Chinese section IDs across browser encodings.
- Complete paginated Blog, all course/topic tag pages, archives, summary RSS, and Chinese Pagefind index checked against the migration manifest. Every local HTML link and heading target checked.
- Original blog worktree remains clean. Migration is local only; comments are disabled and the production blog is unchanged.
- Browser: Blog shows 97 posts; the 13 numerical-methods notes span two course pages; LU has 266 rendered formulas and 7 working tab groups. Switching Python → C++ selects the correct visible panel. The TOC displays each mathematical label once.
- Browser search for `伪共享` returns the newly imported OpenMP memory-model note.
- At 390px, complex-analysis note width is exactly 390px; both replacement SVG diagrams fit the content, and a default-open example collapses correctly.
- Browser navigated an original LU section URL with `?from=migration-check#31-lu`, preserved the query, and reached the canonical algorithm 3.1 heading.
- Five sampled original PNG/WebP pairs have identical decoded RGBA pixels. PNG input/output dimensions are unchanged for every optimized image.
- Screenshots: `import-blog-desktop.png`, `import-search-desktop.png`, `import-proof-mobile.png`, `import-bookmark-desktop.png`.

Final build: Astro diagnostics checked 142 files with 0 errors, 0 warnings, 0 hints. Full migration checker passed across 367 built HTML files; `git diff --check` passed.

## Simplified course tags — 2026-10-24

All 84 course notes now use exactly two tags: subject and course. ODE uses `[数学, ode]`; other math courses use `数学` plus their short course label, and computing courses use `计算机` plus the course label. Policy is centralized in `src/data/course-tags.json` and shared with the importer. Article bodies and source snapshots are unchanged. Visible site tags decreased from 133 to 22; retired tag URLs and their former pagination redirect to the appropriate course or subject. Build and the full migration checker passed. Browser confirmed all five ODE cards show only 数学 and ode.

## Production migration to Semt0/Semt0.github.io — 2026-10-24

The formal repository now contains the approved Pure site. The original Zensical commit is retained by `pre-astro-pure-2026-10-24`; history is preserved without a force push. Production URLs use https://semt0.github.io/. The Pages workflow installs pinned pnpm dependencies with Node 24, builds the static site, runs standalone content checks, and deploys only successful builds.

Dependencies were installed independently in the formal checkout. Build and content checks no longer require an adjacent old repository, Fuwari build, or ignored PNG cache. The original 97 article bodies and immutable snapshots remain unchanged; original resources, 14,634 formulas, disclosures, links and bookmarks still validate. Normal edits and new posts are permitted by the daily checker; `--migration` enables strict original-body auditing.

The existing Waline backend returned HTTP 200 / errno 0. Production comments and view counts use each original `commentPath`; Links retains `/` as the original homepage guestbook. The client is bundled locally, initializes lazily, and is disposed on disconnect. No test comments were posted.

The new-post command was exercised for existing courses and new course folders: it creates a protected draft, assigns the two configured tags, increments chapter order, and refuses to overwrite an existing file. Browser preview showed the Draft label and correct tags. A production build with two temporary drafts excluded both from routes and RSS; checks counted 97 published posts and two unpublished drafts. Temporary files were removed before release.

README, CONTRIBUTING, theme-maintenance and project conventions now document the new workflow. Obsolete Zensical build scripts and Python CI were replaced. One-time migration tools are isolated under migration/tools/.
