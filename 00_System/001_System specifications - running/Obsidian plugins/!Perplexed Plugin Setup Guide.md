---
tags:
  - obsidian
  - pplx
  - Setup
  - plugin
created: 2025-12-30
status: working
---
## Installation

### 1. Download and install manually
The Perplexed plugin is not in the Community Plugins directory yet, so install manually:

1. Go to [[github/lossless-group/perplexed-plugin]] [🔗](https://github.com/lossless-group/perplexed-plugin)
2. Download the latest release ZIP
3. Extract to get `main.js`, `manifest.json`, `styles.css`
4. In your vault, navigate to `.obsidian/plugins/`
5. Create folder: `.obsidian/plugins/perplexed/`
6. Copy the three files into that folder
7. Restart Obsidian
8. Enable "Perplexed" in **Settings → Community Plugins**

## Configuration

### 2. Required settings
Go to **Settings → Community Plugins → Perplexed**:

#### Endpoint
```

[https://api.perplexity.ai/chat/completions](https://api.perplexity.ai/chat/completions)

```
⚠️ **Critical**: Must be the full path (not just `https://api.perplexity.ai`)
⚠️ **No trailing slash**

#### API Key
Get your key from: https://www.perplexity.ai/settings/api
- Requires payment info on file
- Paste the key into the "API Key" field

### 3. Request Body Template
Use this template for citations and clean responses:

```

{ "model": "sonar", "messages": [ { "role": "system", "content": "You are running inside Obsidian (a local Markdown note app). Write answers as Obsidian-ready Markdown only.\n\nHard rules:\n- No meta text (no \"I'm sorry…\", no \"as an AI…\", no discussion about server load).\n- Start with the answer immediately (1–2 sentences).\n- Then give 3–7 bullet points max.\n- If unsure, ask 1 short clarifying question instead of guessing.\n- Keep it under 1200 characters unless I explicitly ask for detail.\n\nCitations:\n- Always include a \"Sources\" section at the end.\n- In \"Sources\", list the web sources as Markdown links using the URLs provided by the API response metadata (e.g., search_results).\n- If no sources are available, write \"Sources: (none returned by API)\" and do not invent citations.\n\nFormatting:\n- Use headings (##) sparingly (max 2).\n- Prefer bullets over paragraphs." }, { "role": "user", "content": "What is the answer to this?" } ], "max_tokens": 1500, "temperature": 0.2, "top_p": 0.9, "return_citations": true, "stream": false }

```

**Template notes:**
- `sonar-pro`: Use `sonar` for faster/cheaper responses
- `max_tokens`: 1500 is balanced; raise for long reports, lower (500) for speed
- `return_citations: true`: Shows source URLs at bottom
- `stream: false`: Get full response at once (set `true` for live typing effect)
- system prompt [[00_Reference/Tools setup/Perplexity Chat (Obsidian) – Stop rambling + citations]]


## Usage

### Running queries
1. Open Command Palette (Ctrl/Cmd+P)
2. Type "Perplexed"
3. Select the query command
4. Enter your question
5. Response appears in current note with citations

### Best practices
- Use specific questions for better results
- Check citations for accuracy
- Lower `max_tokens` for faster daily use
- Use `sonar` model for simple queries, `sonar-pro` for research

## Model comparison

| Model | Speed | Quality | Cost | Use Case |
|-------|-------|---------|------|----------|
| `sonar` | Fast | Good | Low | Quick facts, simple Q&A |
| `sonar-pro` | Medium | Better | Medium | Research, detailed answers |
| `sonar-reasoning` | Slow | Best | High | Complex analysis, reports |

## Troubleshooting

### Common issues

**404 Error:**
- Check endpoint is exactly: `https://api.perplexity.ai/chat/completions`
- No trailing `/`
- Verify in `.obsidian/plugins/perplexed/data.json` if UI won't save

**Empty responses:**
- Check Developer Console (Ctrl/Cmd+Shift+I) for errors
- Verify API key is valid (test at Perplexity's API playground)
- Check rate limits if on free trial

**Connection refused:**
- Wrong endpoint (e.g., `localhost` or missing `https://`)
- VPN/firewall blocking `api.perplexity.ai`


## Related
- [[Perplexity Chat Plugin Setup]] – Alternative simple chat plugin
- [[Obsidian AI Workflows]] – Broader AI integration guide
```