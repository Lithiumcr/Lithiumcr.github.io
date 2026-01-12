# GEMINI.md - Lithiumcr.github.io

## Project Overview

This is a **Jekyll-based personal blog/website** hosted on GitHub Pages. The site is titled "北辕记" (Northern Journey Notes) and serves as a personal blog featuring various categories of content including travel notes, game reviews, economic/financial commentary, political/historical analysis, academic discussions, and literary works.

**Key Technologies:**
- **Jekyll** - Static site generator
- **Hamilton Theme** - Remote theme from ngzhio/jekyll-theme-hamilton
- **GitHub Pages** - Hosting platform
- **Markdown** - Content format

## Project Structure

```
├── _config.yml          # Jekyll configuration
├── Gemfile              # Ruby gem dependencies
├── index.html           # Homepage
├── _posts/              # Blog posts organized by category
│   ├── 司机行记/        # Travel notes
│   ├── 游戏与怪谈/      # Games and strange tales
│   ├── 搬运旧闻-经济金融/ # Economic/financial content
│   ├── 搬运旧闻-政治历史/ # Political/historical content
│   ├── 搬运旧闻-学术杂谈/ # Academic discussions
│   ├── 沙滩文学-拾遗/   # Literary works
│   └── 司机呓语/        # Miscellaneous thoughts
├── _layouts/            # HTML templates
├── _includes/           # Reusable HTML components
├── _data/               # Site data (navigation, social links)
├── category/            # Generated category pages
├── image/               # Image assets
├── assets/css/          # Custom CSS
└── scripts/             # Utility scripts
```

## Building and Running

### Local Development
```bash
# Start Jekyll development server
./scripts/server

# Or directly with bundle
bundle exec jekyll serve --trace
```

### Building for Production
```bash
# Build the site
bundle exec jekyll build

# Build with future posts
bundle exec jekyll build --future
```

### Category Page Generation
```bash
# Generate category pages (run when adding new categories)
python generate_category_pages.py
```

## Content Management

### Adding New Posts
1. Create markdown files in `_posts/` with proper naming convention: `YYYY-MM-DD-title.md`
2. Include front matter with required metadata:
```yaml
---
layout: post
title: "Post Title"
category: 司机行记
author: 北辕司机
toc: true  # Optional: enable table of contents
---
```

### Categories
The site supports the following categories defined in `_config.yml`:
- 司机行记 (Travel notes)
- 游戏与怪谈 (Games and strange tales)
- 搬运旧闻-经济金融 (Economic/financial content)
- 搬运旧闻-政治历史 (Political/historical content)
- 搬运旧闻-学术杂谈 (Academic discussions)
- 沙滩文学-拾遗 (Literary works)

### Navigation
Site navigation is configured in `_data/navigation.yml` and includes:
- About page
- Years archive
- Categories
- Tags
- FAQ and Docs

## Development Conventions

### Content Style
- Posts are written in Chinese (Simplified)
- Use Markdown for content formatting
- Include images in the `image/` directory
- Posts should have meaningful front matter with proper categorization

### Theme Customization
- The site uses the Hamilton theme via remote_theme
- Custom CSS can be added to `assets/css/`
- Layout overrides go in `_layouts/`
- Component overrides go in `_includes/`

### Deployment
- The site is automatically deployed to GitHub Pages
- Push changes to the main branch to trigger deployment
- No additional build steps required for GitHub Pages

## Key Files for Development

- `_config.yml` - Main configuration file
- `Gemfile` - Ruby dependencies
- `generate_category_pages.py` - Script for generating category pages
- `scripts/server` - Development server script
- `_layouts/home.html` - Homepage layout
- `_data/navigation.yml` - Navigation structure

## Recent Changes

### Search Functionality (Jan 2026)
- Enhanced search with XSS protection and improved snippet highlighting in `search.html`.
- Addressed limitations regarding Unicode case folding, HTML special characters in queries, and URL safety.
- *Note: Future improvements could include stricter URL validation and indexing for performance.*

### Content Updates
- Debugging and fixes for post: `2026-01-06-年终总结，或走出北欧后的自我批判.md`.

## TODO Items

- [ ] Add custom CSS styling if needed
- [x] Configure RSS feed if not already present
- [ ] Set up proper SEO meta tags
- [x] Add search functionality
- [ ] Implement comment system (Disqus is commented out in config)

This GEMINI.md file provides the essential context for working with this Jekyll-based personal blog project.