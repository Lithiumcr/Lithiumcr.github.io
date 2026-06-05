#!/usr/bin/env python3
"""
Fix Goldmark CJK bold rendering issue — comprehensive version.

Replace ALL **text** patterns with <strong>text</strong> in markdown body,
since Goldmark has multiple edge cases with CJK characters after closing **.
Hugo's unsafe=true allows raw HTML.
"""

import re
from pathlib import Path

CONTENT_DIR = Path("/Users/administrator/work/beiyuanji-hugo/content")

# Match **text** but NOT inside code blocks or already-converted <strong>
# Non-greedy match; text must not contain newline-newline (paragraph break)
BOLD_PATTERN = re.compile(r'\*\*(?!\s)(.+?)(?<!\s)\*\*')


def fix_file(filepath: Path) -> int:
    """Fix bold rendering in a single file. Returns number of replacements."""
    text = filepath.read_text(encoding='utf-8')

    # Split front matter and body
    if text.startswith('+++'):
        parts = text.split('+++', 2)
        if len(parts) >= 3:
            front_matter = '+++' + parts[1] + '+++'
            body = parts[2]
        else:
            return 0
    else:
        return 0

    # Skip if no ** in body at all
    if '**' not in body:
        return 0

    # Process line by line to avoid touching code blocks
    lines = body.split('\n')
    in_code_block = False
    count = 0
    new_lines = []

    for line in lines:
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            new_lines.append(line)
            continue

        if in_code_block:
            new_lines.append(line)
            continue

        # Replace **text** with <strong>text</strong>
        def replace_bold(match):
            nonlocal count
            inner = match.group(1)
            # Don't replace if inner text already contains <strong>
            if '<strong>' in inner:
                return match.group(0)
            count += 1
            return f'<strong>{inner}</strong>'

        new_line = BOLD_PATTERN.sub(replace_bold, line)
        new_lines.append(new_line)

    if count > 0:
        new_body = '\n'.join(new_lines)
        filepath.write_text(front_matter + new_body, encoding='utf-8')

    return count


def main():
    total_files = 0
    total_fixes = 0

    for md_file in sorted(CONTENT_DIR.rglob('*.md')):
        fixes = fix_file(md_file)
        if fixes > 0:
            total_files += 1
            total_fixes += fixes
            print(f"  Fixed {fixes} in {md_file.name}")

    print(f"\nTotal: {total_fixes} fixes in {total_files} files")


if __name__ == '__main__':
    main()
