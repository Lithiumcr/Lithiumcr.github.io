# Repository Guidelines

## Project Structure & Module Organization

This is the Hugo source for the Chinese-language Beiyuanji (北辕记) site. Site configuration lives in `hugo.toml`. Write pages and articles in `content/`; existing article directories retain legacy Chinese category names for URL and editorial continuity. Logical behavior is set in TOML front matter (`type = 'essay'` or `type = 'archive'`), not inferred from the directory.

The custom theme is `themes/beiyuanji/`: layouts are in `layouts/`, CSS and JavaScript in `assets/`, and theme-static files in `static/`. Put site-wide images and fonts in `static/`; friend-link data is in `data/friends.yml`. `archetypes/` contains content templates, and `scripts/` holds one-off migration/maintenance utilities. Do not hand-edit generated `public/` or `resources/_gen/` output.

## Build, Test, and Development Commands

- `hugo config` — validate and inspect resolved configuration.
- `hugo server --buildDrafts` — run a local preview, including draft content.
- `hugo --gc --minify` — create the production build in `public/`; run this before submitting changes.
- `hugo new essay/my-post.md` — create a new essay from Hugo’s archetype.

The GitHub Actions workflow runs the production build on pull requests to `master` and deploys pushes to `master` to GitHub Pages.

## Coding Style & Naming Conventions

Use TOML front matter delimited by `+++`. Preserve stable `url` values and legacy `aliases` when moving or editing migrated content; URL compatibility is release-critical. Use semantic, minimal HTML and restrained CSS in `themes/beiyuanji/`; match the existing two-space indentation in TOML and templates/CSS. Prefer progressive enhancement and add JavaScript only when necessary. Do not rewrite published prose or change its classification without an explicit request.

## Testing & Verification

There is no automated test suite. For every change, run `hugo config` and `hugo --gc --minify`, then inspect the affected page locally. Also verify generated `public/search.json` for search work, `public/index.xml` for RSS work, and the applicable front-matter aliases for URL changes.

## Commits & Pull Requests

Recent commits use concise, imperative Conventional Commit-style subjects, such as `feat: add logo`, `fix: refine friend card layout`, and `chore: remove dead refs`. Keep each commit focused. PRs should explain the user-visible change, list verification commands, link relevant issues, and include screenshots for layout or typography changes. Flag any URL, RSS, search, or deployment impact explicitly.
