# Beiyuanji Hugo Migration

## Project Overview

Beiyuanji (北辕记) is a Chinese-language intellectual blog migrated from Jekyll to Hugo.

- **Authoritative plan**: `workplan.md`
- **Site URL**: `https://lithiumcr.github.io/`
- **Repository**: `/Users/administrator/work/Lithiumcr.github.io/`
- **Source archive / staging reference**: `/Users/administrator/work/beiyuanji-hugo/`
- **Current posture**: the first Hugo cutover is complete. `master` contains Hugo source, GitHub Pages uses the Actions workflow deployment path, and deployed smoke tests for home, search, RSS, subscribe, cite, representative article pages, and a CJK legacy alias have passed.
- **Display typography**: homepage hero title uses a self-hosted Liu Jian Mao Cao / 刘建毛草 subset font at `static/fonts/liu-jian-mao-cao-hero-subset.ttf`; update the subset when title/axiom text introduces new Chinese characters.

If this file conflicts with `workplan.md`, follow `workplan.md`.

## Core Mandates

1. **Custom Theme**: Keep the custom Hugo theme. Do **not** adopt a predefined Hugo theme as the implementation base.
2. **Modern Visual Reference**: `/Users/administrator/work/5hows-site` is approved as a reference for modern design tokens, fixed translucent navigation, card systems, section rhythm, CTAs, and homepage information architecture. Borrow design thinking only; do not import Astro components, auth/i18n routing, API scripts, or runtime dependencies.
3. **CJK Long-form Reading**: Preserve 北辕记's serif, publication-like Chinese article reading experience. The homepage and navigation may be modern/product-like; article bodies should remain optimized for sustained Chinese reading.
4. **URL Preservation**: Old Jekyll URLs using `/:categories/:year/:month/:day/:title/` must remain available through aliases or redirects.
5. **Content Integrity**: Do not rewrite migrated article meaning or prose unless explicitly requested.

## Building and Running

```bash
hugo server --buildDrafts
hugo --gc --minify
hugo config
```

Hugo v0.160.1 extended is the expected local version.

## Verification Process

There is no automated test suite. Before considering a change complete, verify:

1. `hugo config` resolves without errors.
2. `hugo --gc --minify` succeeds.
3. Layout or navigation changes render correctly on affected page types.
4. Search changes are followed by `public/search.json` generation and a rendered `/search/` smoke test.
5. URL preservation changes are checked against representative aliases.

## Development Conventions

- Physical article storage follows the old Jekyll source directories for maintainability: `司机呓语/`, `司机行记/`, `沙滩文学-拾遗/`, `游戏与怪谈/`, `搬运旧闻-学术杂谈/`, `搬运旧闻-政治历史/`, `搬运旧闻-经济金融/`.
- Logical site sections are controlled by front matter `type`, not physical directory names: `type = 'essay'` for original writing and `type = 'archive'` for curated/reposted material.
- Canonical URLs for moved articles must stay fixed through front matter `url`; old Jekyll URLs remain preserved through `aliases`.
- Visible topics are durable problem domains, not old Jekyll source directories: `行旅与自省`, `技艺与现代性`, `文艺与审美`, `社会与制度`, `学术与思想`, `诗歌`.
- Content filenames may preserve readable Chinese titles when migrated from the old site.
- Front matter uses TOML unless explicitly changed.
- Keep HTML/CSS semantic and lightweight.
- Prefer progressive enhancement; add JavaScript only for concrete needs.
- Do not claim CI/CD, migration, search, RSS, or deployment status unless it is verifiable in the repository or build output.

## Key Files

- `workplan.md`: authoritative migration phases, design decisions, blockers, and acceptance criteria.
- `CLAUDE.md`: detailed working guidance for future agent sessions.
- `hugo.toml`: Hugo configuration, menus, taxonomies, and outputs.
- `themes/beiyuanji/`: active custom theme implementation.
- `themes/beiyuanji/layouts/index.searchindex.json`: Hugo-generated `/search.json` index for client-side search.
- `content/`: migrated content tree.
- `scripts/migrate.py`: Jekyll-to-Hugo migration baseline.
- `.github/workflows/hugo.yml`: GitHub Pages build/deploy flow.
