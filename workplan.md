# Workplan: Migrate beiyuanji from Jekyll to Hugo

> Source: Chapter 11 of new-site-rebuild-plan.md
> Last updated: 2026-06-05

---

## Current Audit Snapshot (2026-06-05)

- Hugo build passes locally with `hugo --gc --minify` on Hugo v0.160.1 from `/Users/administrator/work/Lithiumcr.github.io/` after the source cutover.
- Latest audited build output: 108 pages, 51 static files, 83 aliases.
- Migrated content present in repository: 55 essay files and 30 archive files, plus standalone pages (`search`, `subscribe`, `cite`). The placeholder `about` page has been removed. `dialogue`, `note`, and `series` currently contain only index placeholders and are hidden from primary navigation.
- Search now follows the old site's static `search.json` model: Hugo generates `/search.json` via `themes/beiyuanji/layouts/index.searchindex.json`, and `/search/` performs client-side title/body filtering.
- Deployment strategy is now **Plan B**: keep `/Users/administrator/work/Lithiumcr.github.io/.git`, use `master` as the default source branch, store Hugo source in the repository root, and let GitHub Actions build Hugo and deploy GitHub Pages artifacts.
- Cutover work is staged on `hugo-cutover-2026-06`; merging to `master` and verifying GitHub Pages Actions deployment remain release blockers.
- Visual direction is now explicitly aligned with `/Users/administrator/work/5hows-site` as a reference: borrow the modern product-like shell, homepage rhythm, design tokens, and card system while keeping this repository a fully custom Hugo theme and preserving CJK long-form reading quality.
- Homepage hero title uses a self-hosted Liu Jian Mao Cao / 刘建毛草 font subset (`static/fonts/liu-jian-mao-cao-hero-subset.ttf`) for the current title/axiom characters, avoiding a runtime Google Fonts dependency for the calligraphic display face.

---

## Old Site Metadata

| Item | Value |
|------|-------|
| Repo | https://github.com/Lithiumcr/Lithiumcr.github.io.git |
| Local path | `/Users/administrator/work/Lithiumcr.github.io/` |
| Stack | Jekyll + remote_theme (ngzhio/jekyll-theme-hamilton) |
| Site URL | https://lithiumcr.github.io |
| Post count | 81 posts across 7 category dirs |
| Archive tag | `jekyll-final-2026-06` (commit: 6fbf7a0); earlier archive tag `jekyll-final-2026-04` (commit: 09e45fb) |
| Archive branch | `archive/jekyll` |

### Core Pages

| Page | Source file | Old URL |
|------|-----------|---------|
| Home | index.html | / |
| Search | search.html | /search/ |
| Categories | categories.md | /categories/ |
| Years | years.md | /years/ |
| About | about.md | /about/ |
| Subscribe | subscribe.md | /subscribe/ |
| Friends | friends-apply.md | /friends-apply/ |
| Full blog | blog.html | /blog.html |
| 404 | 404.html | /404.html |

### Categories (7 dirs, 6 in _config.yml)

| Category | Post dir | Note |
|----------|----------|------|
| 司机行记 | _posts/司机行记/ | |
| 司机呓语 | _posts/司机呓语/ | Missing from _config.yml categories list |
| 搬运旧闻-学术杂谈 | _posts/搬运旧闻-学术杂谈/ | |
| 搬运旧闻-政治历史 | _posts/搬运旧闻-政治历史/ | |
| 搬运旧闻-经济金融 | _posts/搬运旧闻-经济金融/ | |
| 沙滩文学-拾遗 | _posts/沙滩文学-拾遗/ | |
| 游戏与怪谈 | _posts/游戏与怪谈/ | |

### Old URL Pattern (permalink)

Hamilton theme default: `/:categories/:year/:month/:day/:title/`

Example: `/司机行记/2025/03/15/some-title/`

> **Critical**: New site must preserve these URLs or set up systematic 301 redirects.

### Special Features

- Comments: utterances (repo: Lithiumcr/Lithiumcr.github.io, issue_term: pathname)
- Analytics: Google Analytics (G-0L0ZF5WQD7)
- Search: client-side search.json full index
- Feed: jekyll-feed plugin RSS
- Skin: time-based auto skin switching (Hamilton built-in)

---

## Phase 1: Archive Old Site

- [x] Tag old site code: `jekyll-final-2026-04` (commit 09e45fb)
- [x] Create archive branch: `archive/jekyll`
- [x] **Push tag and branch to remote** (manual)
  ```bash
  git -C /Users/administrator/work/Lithiumcr.github.io push origin jekyll-final-2026-04
  git -C /Users/administrator/work/Lithiumcr.github.io push origin archive/jekyll
  ```
- [x] **Save static build snapshot** (manual, contains CJK paths)
  ```bash
  cd /Users/administrator/work/Lithiumcr.github.io
  tar czf ../jekyll-site-snapshot-2026-04.tar.gz _site/
  shasum -a 256 /Users/administrator/work/jekyll-site-snapshot-2026-04.tar.gz 
  4ec75444bd700cd8f5cb6f08390a2926cde661d8729b0319c2367d2a7722c1b2 ß /Users/administrator/work/jekyll-site-snapshot-2026-04.tar.gz
  ```
- [x] Document old site URL structure and features (see tables above)

### Phase 1 Acceptance

- [x] Old site recoverable from source (archive/jekyll branch)
- [x] Old site recoverable from static snapshot
- [x] Tag and branch pushed to remote

---

## Phase 2: New Site Skeleton

- [x] Install Hugo (v0.160.1 via Homebrew)
- [x] Init Hugo project: `/Users/administrator/work/beiyuanji-hugo/`
- [x] Create custom theme (`hugo new theme beiyuanji`)
- [x] Configure hugo.toml (title, baseURL, language zh-CN, timezone Asia/Shanghai, theme beiyuanji, hasCJKLanguage)
- [x] Define base layout files
  - baseof.html (modern full-width site shell with fixed navigation and page-aware content containers)
  - home.html (curatorial landing page with hero, cards, topic entries, section entries, recent updates, and RSS CTA)
  - _default/list.html (section list)
  - _default/single.html (article with CJK reading style)
  - page.html (standalone pages like about)
  - partials: head, header, footer, menu
  - CSS combines a 5hows-inspired modern visual system for navigation/home/cards with serif CJK long-form article typography
- [x] Set up GitHub Actions CI/CD (push `master` -> build Hugo -> deploy GitHub Pages artifact)
- [x] Verify `hugo server --buildDrafts` runs locally
- [x] Init git repo

### Phase 2 Acceptance

- [x] Local Hugo build works (`hugo --gc --minify` verified on 2026-06-05 after source cutover)
- [x] Minimal navigation and reading style in place
- [x] GitHub Actions auto-builds on push to `master` after cutover merge
- [x] GitHub Pages deployment verified from remote

---

## Phase 3: Content Model

- [x] Define content types (Hugo sections)
  - content/essay/ (essays, reviews, long-form)
  - content/dialogue/ (conversations, interviews)
  - content/archive/ (reprints, curated materials)
  - content/note/ (short notes)
  - content/series/ (topic introductions, series entries)
  - Standalone pages (about, etc.) live in content/ root with `type = 'page'`
- [x] Design standard Front Matter template
  - Core fields: type, series, topics, summary, keywords
  - Optional fields: original_date, archive_role, ai_participation, people
- [x] Configure custom taxonomies in hugo.toml
  ```toml
  [taxonomies]
    topic = 'topics'
    series = 'series'
    person = 'people'
    keyword = 'keywords'
  ```
- [x] Create archetype templates (essay.md, dialogue.md, archive.md, note.md)
- [x] Build topic and series page templates (taxonomy.html, term.html, section.html)

### Phase 3 Acceptance

- One piece of content addressable by type, topic, and series simultaneously
- At least one topic page fully functional

---

## Phase 4: Content Migration

- [x] Build old-to-new content-type mapping (implemented in scripts/migrate.py) and replace mechanical old-category topics with a smaller editorial taxonomy.
  - Old Jekyll category directories are preserved in `aliases` for URL continuity, but no longer define the visible topic system.
  - New sections describe content form: `essay` for original writing, `archive` for reprints / curated materials.
  - New topics describe durable problem domains:
    - `行旅与自省`
    - `技艺与现代性`
    - `文艺与审美`
    - `社会与制度`
    - `学术与思想`
- [x] Define permalink strategy
  - Old URLs preserved via Front Matter `aliases` (83 alias redirects generated)
  - New canonical URLs: `/:section/:slug/`
- [x] Write batch migration script (Python): `scripts/migrate.py`
  - Jekyll YAML front matter -> Hugo TOML front matter
  - Category -> type + topic mapping
  - `absolute_url` filter -> direct paths
  - `post_url` tags -> Hugo relative links
  - Kramdown `{: .center}` cleanup
- [x] Fix image paths, internal links, footnotes, TOC globally
  - Images copied to `static/image/` (49 files)
  - Fixed absolute file-system paths in cross-references
  - Fixed missing `https://` in external links
  - List page summaries use `plainify` to strip images/HTML

### Phase 4 Principles

- Preserve old URLs or set up explicit redirects
- Do not rewrite original content text
- Structural reorganization before text polish

### Phase 4 Acceptance

- [x] Most old posts accessible on new site
- [x] Old link redirect strategy clear and documented
- [x] 83 old URLs generated as Hugo aliases in latest build
- [x] Images, footnotes, TOC, citations structurally migrated
- [ ] Sample-check high-value old URLs after deployment, including CJK paths

---

## Phase 5: Search & Subscription

- [x] Implement old-site-style static search: Hugo generates `/search.json`, and `/search/` filters title/body content client-side.
- [x] Configure Hugo RSS template (custom rss.xml, full content in `content:encoded`)
- [x] Rebuild standalone subscribe page (`/subscribe/`) with the old site's educational / lightly humorous RSS explanation
- [x] Add search page with instant JSON search (`/search/`)
- [x] RSS auto-discovery `<link>` in `<head>`
- [x] Verify local `public/search.json` generation and JSON validity

### Phase 5 Acceptance

- [x] Major articles are indexed in local `public/search.json` after Hugo build
- [x] RSS output generated locally (`public/index.xml` exists after Hugo build)
- [ ] RSS subscribable by mainstream readers after deployment

---

## Phase 6: Home & Topic Curation

- [x] Adopt a 5hows-site-inspired modern visual system as reference, not dependency
  - Borrow design tokens, fixed translucent navigation, wide homepage container, section rhythm, card grid, hover affordances, and CTA patterns
  - Keep this repository a custom Hugo theme; do not import Astro components, login logic, i18n routing, or API scripts from 5hows-site
  - Preserve 北辕记's serif CJK article reading experience instead of turning long-form pages into generic product documentation
- [x] Build home page blocks
  - Site introduction (one-sentence identity)
  - Topic entries (card grid with article counts)
  - Section entries for populated content forms (`essay` / `archive`); empty future sections (`dialogue`, `note`, `series`) remain available in the content model but are not exposed in primary navigation until they contain real entries
  - Featured works (ready; needs `featured = true` in front matter)
  - Recent updates (last 8 articles)
  - Subscribe entry (RSS link)
- [x] Differentiate visual style per section type
  - Home -> curatorial feel (section grid, topic cards)
  - Topic page -> research guide feel (accent left-border, larger title)
  - Article page -> publication page feel (larger title for essays)
  - Archive page -> library/archive feel (secondary left-border, "档案" prefix)
  - Body data-attributes (`data-section`, `data-kind`, `data-home`) for CSS targeting
- [x] Select 3 representative works for home featured section
  - `content/essay/工程师的自我修养.md`
  - `content/essay/年终总结，或北欧留学批判.md`
  - `content/essay/年终总结，或走出北欧后的自我批判.md`
- [ ] Write topic introductions and recommended reading order (owner decision)

### Phase 6 Acceptance

- [x] New visitors can understand site scope from home page structure
- [ ] Topic pages provide explicit introductions and recommended reading order
- [x] Returning readers can navigate by topic, section, and recent updates, not just timeline

---

## Phase 7: Citability & Long-term Maintenance

- [x] Implement stable paragraph anchors (Hugo render-heading hook, hover-reveal `#` links)
- [x] Create "Citation & Reprint Policy" page (`/cite/`)
- [x] Expose version field, last revision date, original writing date in article template
  - `original_date` field displayed when present
  - `.Lastmod` auto-detected and shown if different from publish date
  - Collapsible "引用本文" block at article footer with permalink
- [ ] Complete site archive statement and methodology notes (owner decision)

### Phase 7 Acceptance

- [x] Important articles have stable heading/paragraph anchors where headings exist
- [x] Article template exposes baseline citation metadata and permalink block
- [ ] Complete archive statement and methodology notes
- [ ] Verify citation block rendering on deployed pages

---

## Release Blockers Before First Public Cutover

- [x] Preserve old site recovery point with `jekyll-final-2026-06` on commit `6fbf7a0`
- [x] Keep `/Users/administrator/work/Lithiumcr.github.io/.git` and switch the working tree to Hugo source
- [x] Configure GitHub Actions workflow to build on pushes to `master`
- [x] Verify local Hugo build from `/Users/administrator/work/Lithiumcr.github.io/`
- [x] Commit and push `hugo-cutover-2026-06` for review / PR (`#3`)
- [x] Merge cutover branch into `master` (`d1b8bdc`)
- [x] Set GitHub Pages source to GitHub Actions (`build_type: workflow`)
- [x] Verify deployed `/search.json` and `/search/` client-side search endpoints respond
- [x] Smoke-test `/`, `/search/`, `/subscribe/`, `/cite/`, RSS, and representative article pages
- [x] Sample-check old Jekyll CJK URLs and confirm Hugo aliases respond online

---

## Theme Decision: Full Custom Build

Do NOT use predefined themes from https://themes.gohugo.io/. Reasons:

Reference policy: `/Users/administrator/work/5hows-site` may be used as a visual-system reference for layout rhythm, navigation, cards, tokens, and homepage information architecture. It must not become a code dependency or implementation base because it is an Astro project with unrelated auth/i18n/client logic.

1. **Theme sovereignty**: Old site pain point was "insufficient theme control". Custom ensures full code ownership.
2. **Unique content model**: Need "works gallery" and "curatorial polyphonic structure", not standard blog/docs.
3. **CJK typography**: Must achieve "publication-grade" typesetting. Foreign themes only reach "can display CJK".
4. **Progressive enhancement**: Keep minimal HTML/CSS skeleton, add lightweight JS only when needed.

---

## Progress Summary

| Phase | Status | Notes |
|-------|--------|-------|
| 1: Archive old site | Done | Tag, archive branch, static snapshot, and URL inventory documented |
| 2: New site skeleton | Done | Theme, layouts, config, local build, master-based Actions workflow, and GitHub Pages deployment are verified |
| 3: Content model | Done | Sections, taxonomies, archetypes, taxonomy templates complete |
| 4: Content migration | Substantially done | 83 aliases generated, 55 essays + 30 archives present; online CJK alias smoke test passed |
| 5: Search & subscription | Deployed and working | RSS and `/search.json` build locally and respond online; `/search/` is deployed |
| 6: Home & curation | Structure + visual refresh done | Home structure, 3 featured works, and 5hows-inspired modern visual system complete; topic introductions / reading order pending |
| 7: Citability | Core done | Anchors, citation block, policy page complete; archive statement and deeper deployed rendering review pending |
| Release readiness | First cutover complete | Hugo source is now on `master`, GitHub Pages uses Actions workflow deployment, and core online smoke tests passed |
