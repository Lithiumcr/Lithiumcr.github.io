#!/usr/bin/env python3
"""
Batch migration script: Jekyll posts -> Hugo content.
Converts front matter, remaps categories, fixes Jekyll-specific syntax.
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime

# === Configuration ===
OLD_SITE = Path("/Users/administrator/work/Lithiumcr.github.io")
NEW_SITE = Path("/Users/administrator/work/beiyuanji-hugo")
OLD_POSTS = OLD_SITE / "_posts"
OLD_IMAGES = OLD_SITE / "image"
NEW_CONTENT = NEW_SITE / "content"
NEW_STATIC = NEW_SITE / "static"

# Old category -> (new_type, initial_topic)
# Old categories are URL history only; visible topics should be reviewed after migration.
CATEGORY_MAP = {
    "司机行记": ("essay", "行旅与自省"),
    "司机呓语": ("essay", "行旅与自省"),
    "搬运旧闻-学术杂谈": ("archive", "学术与思想"),
    "搬运旧闻-政治历史": ("archive", "社会与制度"),
    "搬运旧闻-经济金融": ("archive", "社会与制度"),
    "沙滩文学-拾遗": ("essay", "文艺与审美"),
    "游戏与怪谈": ("essay", "文艺与审美"),
}


def parse_jekyll_front_matter(content: str):
    """Parse YAML front matter from Jekyll post. Returns (metadata_dict, body)."""
    if not content.startswith("---"):
        return {}, content

    end = content.find("---", 3)
    if end == -1:
        return {}, content

    yaml_str = content[3:end].strip()
    body = content[end + 3:].strip()

    # Simple YAML parser (fields are simple key: value)
    meta = {}
    for line in yaml_str.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if value.lower() == "true":
                value = True
            elif value.lower() == "false":
                value = False
            meta[key] = value

    return meta, body


def make_hugo_front_matter(meta: dict, date_str: str, old_category: str, old_filename: str) -> str:
    """Generate TOML front matter for Hugo."""
    title = meta.get("title", "Untitled")
    # Escape single quotes in title
    title_escaped = title.replace("'", "''")

    new_type, new_topic = CATEGORY_MAP.get(old_category, ("essay", "其他"))

    lines = [
        "+++",
        f"title = '{title_escaped}'",
        f"date = {date_str}",
        f"draft = false",
        f"type = '{new_type}'",
        f"topics = ['{new_topic}']",
        f"keywords = []",
    ]

    # Preserve old category as alias source for URL preservation
    # Old URL: /:category/:year/:month/:day/:title/
    slug = extract_slug_from_filename(old_filename)
    year, month, day = date_str.split("T")[0].split("-") if "T" in date_str else date_str.split("-")
    old_url = f"/{old_category}/{year}/{month}/{day}/{slug}/"
    lines.append(f"aliases = ['{old_url}']")

    lines.append("+++")
    return "\n".join(lines)


def extract_slug_from_filename(filename: str) -> str:
    """Extract slug from Jekyll filename like 2024-01-14-旅瑞鼠鼠.md"""
    # Remove date prefix and extension
    name = Path(filename).stem
    match = re.match(r"\d{4}-\d{2}-\d{2}-(.*)", name)
    if match:
        return match.group(1)
    return name


def extract_date_from_filename(filename: str) -> str:
    """Extract date string from Jekyll filename."""
    match = re.match(r"(\d{4}-\d{2}-\d{2})", filename)
    if match:
        return match.group(1)
    return "2020-01-01"


def fix_image_paths(body: str) -> str:
    """Convert Jekyll image syntax to Hugo static paths."""
    # {{ "/image/foo.jpg" | absolute_url }} -> /image/foo.jpg
    body = re.sub(
        r'\{\{\s*"(/image/[^"]+)"\s*\|\s*absolute_url\s*\}\}',
        r'\1',
        body
    )
    return body


def fix_post_url(body: str, all_posts_map: dict) -> str:
    """Convert {% post_url ... %} to Hugo relative links."""
    def replace_post_url(match):
        ref = match.group(1).strip()
        # ref is like: 2025-02-11-DeepSeek锐评《白色相簿2》女主
        if ref in all_posts_map:
            return all_posts_map[ref]
        # Fallback: try to construct path
        date_str = extract_date_from_filename(ref)
        slug = extract_slug_from_filename(ref)
        # We can't know the exact section, use a relative ref
        return f"/posts/{ref}/"

    body = re.sub(
        r'\{%\s*post_url\s+(.+?)\s*%\}',
        replace_post_url,
        body
    )
    return body


def fix_kramdown_attrs(body: str) -> str:
    """Remove Kramdown attribute lists like {: .center } since Hugo doesn't support them."""
    body = re.sub(r'\n\{:\s*[^}]+\}\s*', '\n', body)
    return body


def build_post_url_map(old_posts_dir: Path) -> dict:
    """Build a map from Jekyll post_url references to Hugo URLs."""
    url_map = {}
    for category_dir in old_posts_dir.iterdir():
        if not category_dir.is_dir():
            continue
        category = category_dir.name
        new_type, _ = CATEGORY_MAP.get(category, ("essay", "其他"))

        for post_file in category_dir.glob("*.md"):
            filename = post_file.name
            # Jekyll post_url uses filename without extension, sometimes with date
            ref_key = post_file.stem  # e.g. 2024-01-14-旅瑞鼠鼠
            slug = extract_slug_from_filename(filename)
            hugo_path = f"/{new_type}/{slug}/"
            url_map[ref_key] = hugo_path

    return url_map


def migrate_post(post_file: Path, category: str, post_url_map: dict) -> tuple:
    """Migrate a single post. Returns (output_path, content) or None on error."""
    filename = post_file.name
    date_str = extract_date_from_filename(filename)
    slug = extract_slug_from_filename(filename)

    # Validate date (handle invalid dates like 2020-04-31)
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        # Fix invalid date: use last valid day of month
        parts = date_str.split("-")
        date_str = f"{parts[0]}-{parts[1]}-28"

    raw = post_file.read_text(encoding="utf-8")
    meta, body = parse_jekyll_front_matter(raw)

    # Generate Hugo front matter
    front_matter = make_hugo_front_matter(meta, date_str, category, filename)

    # Fix body content
    body = fix_image_paths(body)
    body = fix_post_url(body, post_url_map)
    body = fix_kramdown_attrs(body)

    # Determine output path
    new_type, _ = CATEGORY_MAP.get(category, ("essay", "其他"))
    output_path = NEW_CONTENT / new_type / f"{slug}.md"

    content = f"{front_matter}\n\n{body}\n"
    return output_path, content


def migrate_images():
    """Copy images from old site to new static directory."""
    dest = NEW_STATIC / "image"
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(OLD_IMAGES, dest)
    print(f"  Copied {sum(1 for _ in dest.rglob('*') if _.is_file())} image files")


def main():
    print("=" * 60)
    print("Jekyll -> Hugo Migration")
    print("=" * 60)

    # Build cross-reference map
    print("\n[1/4] Building post cross-reference map...")
    post_url_map = build_post_url_map(OLD_POSTS)
    print(f"  Indexed {len(post_url_map)} posts")

    # Migrate posts
    print("\n[2/4] Migrating posts...")
    migrated = 0
    errors = []

    for category_dir in sorted(OLD_POSTS.iterdir()):
        if not category_dir.is_dir():
            continue
        category = category_dir.name
        posts = sorted(category_dir.glob("*.md"))
        print(f"  {category}: {len(posts)} posts")

        for post_file in posts:
            try:
                result = migrate_post(post_file, category, post_url_map)
                if result:
                    output_path, content = result
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    output_path.write_text(content, encoding="utf-8")
                    migrated += 1
            except Exception as e:
                errors.append((post_file.name, str(e)))

    print(f"\n  Total migrated: {migrated}")
    if errors:
        print(f"  Errors: {len(errors)}")
        for name, err in errors:
            print(f"    - {name}: {err}")

    # Migrate images
    print("\n[3/4] Migrating images...")
    migrate_images()

    # Remove test post (will be replaced by real content)
    print("\n[4/4] Cleanup...")
    test_post = NEW_CONTENT / "essay" / "test-post.md"
    if test_post.exists():
        test_post.unlink()
        print("  Removed test-post.md")

    print("\n" + "=" * 60)
    print("Migration complete!")
    print(f"  Posts: {migrated}")
    print(f"  Errors: {len(errors)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
