# Beiyuanji Hugo Migration

## Project Overview

Beiyuanji (北辕记) is a Chinese-language intellectual blog migrated from Jekyll to Hugo.

- **Authoritative plan**: `workplan.md`
- **Site URL**: `https://lithiumcr.github.io/`
- **Old local repo**: `/Users/administrator/work/Lithiumcr.github.io/`
- **New local repo**: `/Users/administrator/work/beiyuanji-hugo/`
- **Current posture**: Phase 2 core, Phase 3, Phase 4, Phase 5 JSON search/RSS, Phase 6 structure/visual system, and Phase 7 core are implemented locally. Remote/deployed search/RSS acceptance remains pending.
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

- Section directory names are singular and lowercase: `essay/`, `dialogue/`, `archive/`, `note/`, `series/`.
- Only expose populated sections in primary navigation and homepage cards. At present, `dialogue/`, `note/`, and `series/` are model placeholders and should remain hidden until real entries exist.
- Visible topics are durable problem domains, not old Jekyll source directories: `行旅与自省`, `技艺与现代性`, `文艺与审美`, `社会与制度`, `学术与思想`.
- Old Jekyll categories should remain as URL history in `aliases`, not as new taxonomy drivers.
- Content filenames use hyphens.
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
