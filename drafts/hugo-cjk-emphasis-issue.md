## Issue: Support goldmark-cjk-friendly extension for CJK emphasis parsing

**Repo:** https://github.com/gohugoio/hugo/issues/new

**Title:** Support goldmark-cjk-friendly extension for CJK emphasis parsing

---

### Summary

Hugo's built-in Goldmark renderer fails to parse `**bold**` emphasis when the closing `**` is immediately followed by a CJK character (Chinese/Japanese/Korean) without a space. This is a known limitation of the CommonMark spec's emphasis-detection algorithm, which assumes word boundaries exist around emphasis delimiters.

### Reproduction

Given this Markdown input:

```markdown
**这是加粗文字。**后面紧跟中文。
```

**Expected HTML:**
```html
<p><strong>这是加粗文字。</strong>后面紧跟中文。</p>
```

**Actual HTML (Hugo 0.160.1):**
```html
<p>**这是加粗文字。**后面紧跟中文。</p>
```

The `**` markers are output as literal asterisks instead of being converted to `<strong>`.

### Patterns that fail

| Pattern | Result |
|---|---|
| `**加粗。**紧跟中文` | ❌ Raw `**` |
| `**加粗**，后面有标点` | ✅ Works (Chinese comma acts as delimiter) |
| `中文**加粗**中文` | ✅ Works (mid-paragraph) |
| `**"引号内容"**紧跟` | ❌ Raw `**` |

The common factor: closing `**` immediately followed by a CJK ideograph (U+4E00–U+9FFF) without intervening punctuation or space.

### Additional context

With `hasCJKLanguage = true` and:

```toml
[markup.goldmark.extensions.cjk]
  enable = true
  eastAsianLineBreaks = true
  escapedSpace = true
```

The issue persists. The existing CJK extension only handles line breaks, not emphasis delimiter recognition.

### Proposed solution

The [`goldmark-cjk-friendly`](https://github.com/tats-u/goldmark-cjk-friendly) extension by @tats-u solves exactly this problem at the Goldmark parser level. It modifies emphasis delimiter detection to account for CJK character boundaries, making `**...**` work naturally in Chinese/Japanese/Korean text.

This extension is:
- MIT-licensed (same as Goldmark)
- A direct Goldmark plugin (`goldmark.WithExtensions(...)`)
- Part of a broader [CommonMark CJK-friendly specification effort](https://github.com/tats-u/markdown-cjk-friendly)
- Available as a stable v2 release

#### Suggested integration

Add a new configuration option under the existing CJK section:

```toml
[markup.goldmark.extensions.cjk]
  enable = true
  friendlyEmphasis = true   # NEW: use goldmark-cjk-friendly for emphasis parsing
```

Or, since `enable = true` already implies CJK support is desired, `friendlyEmphasis` could default to `true` when `enable = true`.

### Impact

This affects any Hugo site with CJK content that uses standard Markdown `**bold**` syntax. The current workaround is to replace all `**...**` with raw `<strong>...</strong>` HTML tags, which:
- Degrades Markdown readability
- Requires post-processing scripts during content migration
- Creates maintenance burden for future content authors

A native fix would benefit the entire CJK Hugo community.

### Environment

- Hugo: v0.160.1 extended (darwin/arm64, Homebrew)
- OS: macOS
- Content: ~80 Chinese-language articles, ~4000 affected emphasis instances

---

### 提交方式

```bash
gh auth login
gh issue create --repo gohugoio/hugo \
  --title "Support goldmark-cjk-friendly extension for CJK emphasis parsing" \
  --body-file /Users/administrator/work/beiyuanji-hugo/drafts/hugo-cjk-emphasis-issue.md
```

（提交时用 `--body-file` 指向本文件，去掉开头的标题和末尾的"提交方式"段落即可）
