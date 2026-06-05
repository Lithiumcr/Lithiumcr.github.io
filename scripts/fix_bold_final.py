#!/usr/bin/env python3
"""
Final bold fix — operates on full body text, not line-by-line.
1. Revert all <strong>...</strong> to **...** (including cross-line)
2. Convert all **...** to <strong>...</strong> (including cross-line)
Skips code blocks.
"""

import re
from pathlib import Path

CONTENT_DIR = Path("/Users/administrator/work/beiyuanji-hugo/content")

# Match fenced code blocks to skip them
CODE_BLOCK = re.compile(r'```.*?```', re.DOTALL)


def fix_file(filepath: Path) -> int:
    text = filepath.read_text(encoding='utf-8')

    if text.startswith('+++'):
        parts = text.split('+++', 2)
        if len(parts) >= 3:
            front_matter = '+++' + parts[1] + '+++'
            body = parts[2]
        else:
            return 0
    else:
        return 0

    if '**' not in body and '<strong>' not in body:
        return 0

    # Extract and protect code blocks
    code_blocks = []
    def save_code(m):
        code_blocks.append(m.group(0))
        return f'\x00CODE{len(code_blocks)-1}\x00'

    body_safe = CODE_BLOCK.sub(save_code, body)

    # Step 1: Revert ALL <strong>...</strong> back to **...**
    body_safe = re.sub(r'<strong>(.*?)</strong>', r'**\1**', body_safe, flags=re.DOTALL)

    # Step 2: Convert ALL **...** to <strong>...</strong>
    count = 0
    def replace_bold(m):
        nonlocal count
        count += 1
        return f'<strong>{m.group(1)}</strong>'

    body_safe = re.sub(r'\*\*(?!\s)(.*?)(?<!\s)\*\*', replace_bold, body_safe, flags=re.DOTALL)

    # Restore code blocks
    def restore_code(m):
        idx = int(m.group(1))
        return code_blocks[idx]

    body_safe = re.sub(r'\x00CODE(\d+)\x00', restore_code, body_safe)

    if count > 0:
        filepath.write_text(front_matter + body_safe, encoding='utf-8')

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
