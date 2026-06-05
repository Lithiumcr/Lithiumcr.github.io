# CLAUDE.md

This file provides working guidance to Claude Code when operating in this repository.

## Project Overview

Beiyuanji (北辕记) is a Chinese-language intellectual blog migrated from Jekyll to Hugo.

- **Primary plan source**: `workplan.md` (last updated 2026-06-05)
- **Current implementation status**: the first Hugo cutover is complete. `master` contains Hugo source, GitHub Pages uses the Actions workflow deployment path, and deployed smoke tests for home, search, RSS, subscribe, cite, representative article pages, and a CJK legacy alias have passed.
- **Site URL**: `https://lithiumcr.github.io/`
- **Repository**: `/Users/administrator/work/Lithiumcr.github.io/`
- **Source archive / staging reference**: `/Users/administrator/work/beiyuanji-hugo/`
- **Scale**: 83 legacy URL aliases preserved; latest audited Hugo build renders 118 pages and 51 static files after restoring legacy physical content directories
- **Migrated content present**: 55 essays and 30 archives stored under the old Jekyll source directories, plus standalone pages (`search`, `subscribe`, `cite`); empty placeholder sections (`dialogue`, `note`, `series`) have been removed
- **Display typography**: homepage hero title uses a self-hosted Liu Jian Mao Cao / 刘建毛草 subset font at `static/fonts/liu-jian-mao-cao-hero-subset.ttf`; update the subset if the title/axiom text introduces new Chinese characters.

If this file conflicts with `workplan.md`, treat `workplan.md` as the authoritative source.

## Non-Negotiable Project Decisions

### 1. Build a custom Hugo theme

Do **not** adopt a predefined theme from `https://themes.gohugo.io/` as the site foundation.

Reasons:

- **Theme sovereignty**: the old site already suffered from insufficient theme control
- **Content model fit**: this project is not a standard chronological blog or docs site
- **CJK typography**: the site needs publication-grade Chinese reading experience
- **Full ownership**: future iteration should not depend on external theme architecture

A third-party theme may be inspected for reference, but should not become the implementation base. `/Users/administrator/work/5hows-site` is an approved visual reference for the modern shell, design tokens, cards, section rhythm, and homepage information architecture; borrow the design thinking, not its Astro components, auth/i18n code, or runtime dependencies.

### 2. Preserve old URLs

Old Jekyll URLs follow:

`/:categories/:year/:month/:day/:title/`

Example:

`/司机行记/2025/03/15/some-title/`

The new Hugo site must preserve these URLs where possible, or provide explicit redirects through Hugo permalink strategy and front matter `aliases`.

### 3. Do not modify old-site content semantics during migration

During migration, prioritize:

- structural conversion
- metadata normalization
- link and asset repair
- URL continuity

Do **not** rewrite article meaning or polish prose unless the user explicitly asks.

## Current Repository Reality

This repository is an operational Hugo site rather than a bare skeleton.

Current known state:

- `hugo.toml` is configured for `zh-CN`, `Asia/Shanghai`, custom taxonomies, RSS outputs, and theme `beiyuanji`
- `themes/beiyuanji/` contains the active layouts, partials, and styles
- `content/` stores migrated articles under legacy physical directories while front matter `type` controls logical sections (`essay` / `archive`); standalone pages remain at the content root
- `scripts/migrate.py` exists for Jekyll -> Hugo migration
- `themes/beiyuanji/layouts/index.searchindex.json` generates `/search.json` for client-side search
- there is no automated test suite

Only describe features as complete when they are verifiable in the repository or build output.

## Phase Execution Rules

## Current Phase Posture

Implemented / verified work:

- **Phase 2**: new site skeleton, local build, GitHub Actions workflow, and deployed GitHub Pages are verified
- **Phase 3**: content model
- **Phase 4**: content migration, including 83 online legacy aliases with a sampled CJK alias check
- **Phase 5 deployed**: `/search.json`, `/search/`, and RSS respond online
- **Phase 6 core**: home structure, 3 featured works, and 5hows-inspired modern visual system are in place
- **Phase 7 core**: stable paragraph anchors, `/cite/` policy page, article-footer citation block, `original_date` / `Lastmod` exposure

Outstanding work (default next priorities):

- **Phase 6 editorial** — topic introductions and recommended reading order (owner decision)
- **Phase 7 editorial** — full archive statement and methodology notes (owner decision)
- **Deeper post-cutover QA** — broader sample checks for article rendering, aliases, RSS readers, and citation blocks beyond the initial smoke test

Audit caveat:

- **Phase 1 archive** is complete with `jekyll-final-2026-06` on commit `6fbf7a0` and the older `jekyll-final-2026-04` archive retained

Unless the user explicitly asks for regression fixes or rework, prefer advancing the outstanding items above rather than redoing accepted Phase 2-5 tasks or rebuilding the Phase 6/7 work that is already landed.

## Release Status After First Public Cutover

The first Hugo cutover is complete. Per `workplan.md`, the completed release facts are:

- Old site recovery is preserved by `jekyll-final-2026-06` on commit `6fbf7a0`
- `master` contains the Hugo source tree in `/Users/administrator/work/Lithiumcr.github.io/`
- GitHub Pages build type is `workflow`
- `.github/workflows/hugo.yml` builds Hugo on pushes to `master`; PRs to `master` run build verification but skip deploy
- PR `#3` was merged into `master` as `d1b8bdc`
- Deployed smoke tests passed for `/`, `/search/`, `/search.json`, `/index.xml`, `/subscribe/`, `/cite/`, a representative article page, and a sampled old CJK alias

Treat any regression in build, deployment, search/RSS, or URL preservation as release-blocking.

## Implemented Content Model

The content model defined in `workplan.md` is already present.

Logical content sections:

- `essay`: original writing, identified by `type = "essay"`
- `archive`: curated/reposted material, identified by `type = "archive"`
- standalone pages in `content/` root

Physical article directories follow the old Jekyll source categories for human maintainability:

- `司机呓语/`
- `司机行记/`
- `沙滩文学-拾遗/`
- `游戏与怪谈/`
- `搬运旧闻-学术杂谈/`
- `搬运旧闻-政治历史/`
- `搬运旧闻-经济金融/`

Taxonomies:

```toml
[taxonomies]
  topic = "topics"
  series = "series"
  person = "people"
  keyword = "keywords"
```

Do not invent additional core content types unless the user requests them.

## Completed Migration and Feature Baseline

Already implemented in repository:

- batch migration from old Jekyll posts via `scripts/migrate.py` (85 migrated articles currently present as 55 essays + 30 archives)
- old URL preservation through front matter `aliases` (83 aliases generated in latest build)
- search UI with old-site-style static `/search.json` index and client-side title/body filtering
- RSS / subscription pages and templates (custom `rss.xml`, full content in `content:encoded`, `/subscribe/` page)
- Home page with 5hows-inspired modern visual system: hero, topic cards, section entries, 3 featured works, recent updates, RSS CTA
- Per-section visual differentiation via `data-section` / `data-kind` / `data-home` body attributes
- Citability layer: render-heading-hook anchors, `/cite/` policy page, article-footer citation block, `original_date` and `Lastmod` exposure
- GitHub Actions deployment from `master` to GitHub Pages artifact hosting

Still pending as default roadmap work:

- topic introductions and recommended reading order on topic pages
- complete site archive statement and methodology notes
- deeper post-cutover verification across more old aliases, RSS readers, and citation block renderings

Do not reopen completed phases without a concrete bug, regression, or explicit user request.

## Classification Reference

The visible classification system is intentionally smaller than the old Jekyll category tree.

- **Sections describe content form**: `essay` for original writing; `archive` for reprints, curated materials, interviews, and historical records.
- **Empty future sections should not be kept as blank content directories**: create `dialogue` or `note` content only when real entries exist.
- **Old Jekyll directories are physical storage aids**, not taxonomy drivers; article listing, search, styling, and canonical URLs should rely on front matter `type` and `url`.
- **Topics describe durable problem domains**, not old source directories:
  - `行旅与自省`
  - `技艺与现代性`
  - `文艺与审美`
  - `社会与制度`
  - `学术与思想`
- **Old Jekyll categories are URL history only**: preserve them in `aliases`, but do not use them to drive new taxonomy decisions.

If the user wants finer reclassification for specific pieces, treat that as post-migration editorial work.

## Build Commands

```bash
hugo server --buildDrafts
hugo --gc --minify
hugo new essay/my-post.md
hugo config
```

Hugo `v0.160.1 (extended+withdeploy)` is installed via Homebrew.

## Verification Rules

There is no automated test suite. Before considering a change complete, verify at least:

1. **Configuration resolves**: `hugo config`
2. **Production build succeeds**: `hugo --gc --minify`
3. **Local dev server starts**: `hugo server --buildDrafts`
4. **Affected page types render** in local preview

Add task-specific verification when relevant:

- search changes: verify `public/search.json` is generated and `/search/` can fetch it
- RSS / subscription changes: verify `public/index.xml` and relevant section feeds
- URL preservation changes: verify affected front matter `aliases`

If a task changes layout or navigation, verify the relevant rendered pages instead of only editing templates.

## Working Conventions

- Physical article directories preserve old Jekyll categories for maintainability; do not infer logical site sections from directory names
- `type` controls logical section behavior; `url` preserves canonical URLs when files move
- Front matter uses **TOML** unless the user explicitly changes the convention
- Keep HTML/CSS minimal and semantic
- Prefer progressive enhancement; add JS only when it solves a real need
- Use the 5hows-inspired modern visual system for navigation, homepage, cards, section rhythm, CTAs, and metadata hierarchy
- Keep article bodies optimized for Chinese long-form reading with serif typography, generous line-height, and restrained publication-like styling

## Files That Matter Most

- `workplan.md`: authoritative migration phases, tasks, and acceptance criteria
- `hugo.toml`: Hugo configuration
- `themes/beiyuanji/`: active theme implementation
- `themes/beiyuanji/layouts/index.searchindex.json`: Hugo-generated `/search.json` index for client-side search
- `content/`: Hugo content tree
- `scripts/migrate.py`: migration baseline and old-to-new mapping logic
- `.github/workflows/hugo.yml`: GitHub Pages build/deploy flow

## Execution Guardrails for Future Claude Instances

- Always check `workplan.md` before making structural decisions
- Treat the old Jekyll repo as a migration reference and archive source, not the primary implementation workspace
- Prefer incremental, phase-aligned changes over broad speculative scaffolding
- Do not claim CI/CD, theme files, taxonomies, migration scripts, search, or RSS features exist unless they are actually present
- Do not switch to a predefined Hugo theme to save time
- Do not break URL preservation requirements for convenience
- When uncertain, choose the smaller reversible change that advances the roadmap without regressing accepted Phase 2-5 work or the already-landed Phase 6/7 core
- Do not claim deployment, remote push, or deployed search/RSS features as verified until the corresponding Release Blocker is actually closed
