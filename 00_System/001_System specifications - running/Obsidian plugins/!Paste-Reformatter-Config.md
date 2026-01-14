---
type: plugin configuation
created: 2026-01-04
plugin: Paste Reformatter
tags:
  - workflow
  - citation-cleaning
  - plugin/settings
---


# Paste Reformatter Configuration

## Citation Removal Patterns


**Markdown transformations:**
1. **Pattern:** `<span style="display:none">(?:\[\^[\w_]+\])+</span>|\[\^[\w_]+\]:\s*[^\n]+|(?:\[\^[\w_]+\])+`
2. **Replace:** *(empty)*
3. **Purpose:** Remove Perplexity footnote citations


## Why this works
- Catches hidden spans
- Catches footnote definitions
- Catches inline citations
- One pattern for all formats


