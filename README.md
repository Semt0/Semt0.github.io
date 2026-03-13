# Semt0's Blog

个人博客与学习笔记站点，基于 **Zensical（Material for MkDocs）** 搭建，用来记录技术文章、数学笔记（如 ODE）、以及日常随笔。

站点在线地址：`https://semt0.github.io/`

---

## 特性

- **静态站点**：基于 Zensical / MkDocs Material 构建，部署在 GitHub Pages，加载速度快。
- **深度定制主页**：
  - 左侧自我介绍 + 右侧头像布局
  - 下方四个内容栏目（博客、笔记、Tech Stack、链接）
  - 单词级的淡入动画、滚动淡入栏目动画
  - 全局花瓣飘落 + 夜间模式下星空背景
- **中英混合内容支持**：默认语言为中文，也支持英文内容和搜索。
- **数学公式渲染**：使用 KaTeX + `pymdownx.arithmatex`。
- **良好的暗色模式**：
  - 深灰偏黑背景
  - 白色高对比文字
  - 针对正文、导航、目录的统一配色调整
- **博客功能**：带有时间、阅读时间、分页等基础博客能力。

---

## 技术栈

- **静态站点生成**：Zensical（基于 MkDocs）
- **主题**：Material for MkDocs（`scheme = "default" / "slate"`）
- **标记语言**：Markdown（扩展：pymdownx 系列）
- **样式**：自定义 CSS（`docs/stylesheets/extra.css`）
- **脚本**：
  - `docs/javascripts/katex.js`：KaTeX SPA 渲染
  - `docs/javascripts/home-animation.js`：主页栏目滚动动画
  - `docs/javascripts/home-intro-words.js`：主页标题逐词淡入动画
  - `docs/javascripts/sakura-init.js`：花瓣飘落效果

---

## 目录结构（简要）

```text
.
├── docs/
│   ├── index.md                 # 主页
│   ├── blog/
│   ├── note/
│   ├── stylesheets/
│   │   └── extra.css            # 自定义样式（主页 + 夜间模式 + 樱花 + 星空）
│   └── javascripts/
│       ├── katex.js
│       ├── home-animation.js
│       ├── home-intro-words.js
│       └── sakura-init.js
├── zensical.toml                # Zensical 主配置（导航、主题、插件等）
└── README.md