---
title: AI Usage Analysis – Perplexity CLI Branch
created: 2026-01-10
Tags:
  - ai/usage
  - Pipeline
  - Guide
  - PPLX
---
[[AI Usage Analysis Pipeline (Guide)]
This note documents an **optional branch** used only to confirm that
Perplexity supports message-level timestamps via the API.

---

## When to use this

- Short-term diagnostics
- Verifying limits and flow
- Not for long-term usage tracking

API billing applies.

---

## Environment setup (Windows)

```powershell
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1
pip install pplx-cli
```
## Authentication (non-interactive)
Do NOT use `perplexity setup`.  
```
setx PERPLEXITY_API_KEY "<API_KEY>"`
```
Restart PowerShell.  
Verify:
```
perplexity ask "ping"
```
## List conversations
```
perplexity history
```
---

## Export a conversation

```python
perplexity history perplexity export-chat 1 --format json --output test.json
```

---

## Confirmed JSON fields

- created_at
    
- messages[].timestamp
    

This proves timestamps exist internally.