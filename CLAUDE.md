# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Personal blog and learning notes site (https://semt0.github.io/) built with **Zensical** (a Material for MkDocs fork). Content is bilingual (Chinese/English) with mathematical notation support via KaTeX.

## Build & Development

```bash
# Install dependencies (uses uv for Python package management)
uv sync

# Local development server
zensical serve

# Production build
zensical build --clean
```

**Python 3.13** required (see `.python-version`). The `zensical` package is the dev dependency that provides the build toolchain.

## Deployment

GitHub Actions (`.github/workflows/docs.yml`) auto-deploys on push to `main`/`master`. The workflow runs `zensical build --clean` and publishes the `site/` directory to GitHub Pages.

## Architecture

- **`zensical.toml`** — Main site configuration (theme, plugins, navigation, extensions, CSS/JS includes). This is the equivalent of `mkdocs.yml` for Zensical.
- **`docs/`** — All source content and assets
  - `index.md` — Homepage (custom HTML layout, not standard Markdown)
  - `blog/` — Blog posts with `.authors.yml`
  - `note/` — Learning notes organized by subject
  - `friends.md` — Friend links page
  - `stylesheets/extra.css` — All custom CSS (~1070 lines): homepage layout, sakura petals, dark mode starfield, animations, responsive design, Waline comments
  - `javascripts/` — Custom JS modules:
    - `sakura-init.js` — 3D petal falling animation (3-layer depth, performance-adaptive)
    - `home-animation.js` — Scroll-triggered section fade-ins, avatar preloading
    - `home-intro-words.js` — Word-by-word text reveal animation
    - `katex.js` — KaTeX math rendering integration
    - `waline-init.js` — Waline v3 comment system (server: Vercel-hosted)
- **`site/`** — Generated output (committed to repo, also built in CI)
- **`scripts/`** — Python utilities for extracting PDF lecture slides to PNG (uses PyMuPDF)

## Key Patterns

- All custom JS integrates with Zensical's SPA navigation via `document$` (RxJS observable) to reinitialize on page transitions.
- Animations respect `prefers-reduced-motion` and detect low-performance devices (coarse pointer, CPU cores ≤ 4).
- Dark mode (`[data-md-color-scheme="slate"]`) uses CSS variables extensively and adds a radial-gradient starfield background.
- The homepage (`docs/index.md`) uses raw HTML with CSS classes defined in `extra.css` — it is not standard Markdown content.
- When editing `docs/` files, the corresponding `site/` files are generated output and should be rebuilt, not manually edited.
