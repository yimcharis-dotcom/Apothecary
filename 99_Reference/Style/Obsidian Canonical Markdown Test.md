---
title: Obsidian Canonical Markdown Test
type: test
tags:
  - formatting
  - obsidian

---
# CB4C48>
# Headings (H1–H6)

# H1 — Heading
## H2 — Heading
### H3 — Heading
#### H4 — Heading
##### H5 — Heading
###### H6 — Heading

# Emphasis & Text Styles

This is **bold** text.  
This is *italic* text.  
This is ***bold italic*** text.  
This is `inline code`.  
~~Strikethrough~~.  
==Highlight==.

# Paragraphs and Line Breaks

This is a paragraph.  
Two spaces at end of line create a line break.  
This is still the same paragraph.

# Quotes and Nested Quotes

> This is a blockquote.
>
> > This is a nested blockquote.

# Callouts (Obsidian)

> [!info] This is an info callout.  
> It supports **formatting**, , ==highlight==, and embeds. :contentReference{index=1}

> [!tip] This is a tip callout.

> [!warning] This is a warning callout.

> [!danger] This is a danger callout.

# Lists

## Unordered
- Item one
- Item two
  - Nested item
- Item three

## Ordered
1. First
2. Second
3. Third

## Task List
- [ ] Incomplete task
- [x] Complete task

# Tables

| Header A | Header B | Header C |
|----------|----------|----------|
| Text     | **Bold** | *Italic* |
| `Code`   | ==Highlight== | ~~Strike~~

# Code Blocks

```markdown
# Markdown block
	- List inside code
- **Bold that stays literal**
```

// JavaScript sample
function test(value) {
    return value ? "Yes" : "No";
}
# Wiki Links and Embeds (Obsidian)

Internal link:   
Internal link alias: 
Embed (if file exists): !

# Horizontal Rules

---

---

---

# Comments (Obsidian)

Text before comment. %%This part is a comment and will not render in preview.%% Text after.

# Footnotes

Here is a reference1.

# Escaping Characters

Escaped star: *Not italic*  
Escaped hash: # Not a heading

# End of Test Page

**What this covers**

This file tests all major elements that Obsidian supports including:

- Standard Markdown: headings, lists, tables, code blocks, quotes.  
- Obsidian-specific extensions: callouts, wiki links, embeds, task list states, highlight syntax. :contentReference{index=2}

**Notes**

- Obsidian supports both **CommonMark and GitHub-flavored Markdown** plus its own extensions. :contentReference{index=3}  
- Some elements (e.g., comments enclosed in `%%`) behave differently between editing and preview modes. :contentReference{index=4}

You can paste this into a new `.md` file in your vault and toggle different themes to evaluate typography, spacing, colors, and component rendering. If you want a **variant that includes plugin-specific features such as Mermaid, Dataview, or Tasks advanced queries**, tell me and I can generate that next.
::contentReference{index=5}