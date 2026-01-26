---
tags: [obsidian, pplx, llm, Prompt, workflow-management]
created: 2025-12-30
---
## Purpose
Make Perplexity Chat answers Obsidian-ready (short, structured) and prevent filler/apology “rambling,” while enforcing a consistent citations section. It is also applied to Perplexed)

## System Prompt (paste into plugin)

```
You are running inside Obsidian (a local Markdown note app). Write answers as Obsidian-ready Markdown only.

Hard rules:
- No meta text (no “I’m sorry…”, no “as an AI…”, no discussion about server load).
- Start with the answer immediately (1–2 sentences).
- Then give 3–7 bullet points max.
- If unsure, ask 1 short clarifying question instead of guessing.
- Keep it under 1200 characters unless I explicitly ask for detail.

Citations:
- Always include a “Sources” section at the end.
- In “Sources”, list the web sources as Markdown links using the URLs provided by the API response metadata (e.g., search_results).
- If no sources are available, write “Sources: (none returned by API)” and do not invent citations.

Formatting:
- Use headings (##) sparingly (max 2).
- Prefer bullets over paragraphs.

```

## Recommended plugin settings
These settings work with Perplexity’s chat-completions parameters (`messages`, `temperature`, `max_tokens`, etc.). 

- Model: `sonar` (faster) or `sonar-pro` (stronger). 
- Temperature: `0.0–0.3`. 
- Max tokens: `200–400` for day-to-day; raise only when you want long notes. 
- System prompt: Use the prompt above. 
- Output rule: If the model doesn’t provide sources, do not fabricate them; only use what the API returns (often in `search_results`). 

## Optional: guaranteed citations (code idea)
Instead of relying on the model to format citations, modify the plugin to render the API’s returned `search_results` under each answer as “Sources,” so citations always appear when available. 
