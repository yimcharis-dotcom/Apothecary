---
Supported plugins: copilot
model: openai@sonar-pro
openaiUrl: https://api.perplexity.ai/v2
max_tokens: 400
temperature:
tag:
  - pplx
  - ai/api
updated: 2026-01-30T12:00:00+08:00
---

APIkey:
```
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
```

Copilot
$env:MCP_ROOT="C:\Users\YC\Documents\TestFolder"
$env:PPLX_API_KEY="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"
Node .\bridge. Js "What are the main tasks and deadlines in these files?"

LocalGPT

Perplexity chat: [[00_Reference/Tools setup/Perplexity Chat (Obsidian) – Stop rambling + citations]]

Perplxed: [[00_Reference/Tools setup/Perplexed Plugin Setup Guide]]

AI chat: go to main.js del openai /v1

AI chat as markdown

Auto classifier: [ PPLX]("C:\Vault\Apothecary\. Obsidian\New folder\auto classifer\main. Js")

## **Perplexity’s OpenAI Compatibility**

Perplexity is designed to be a "drop-in" replacement for OpenAI in most tools. To use it in a plugin or script that asks for an OpenAI-compatible endpoint, use these settings:

- **Base URL:** `https://api.perplexity.ai/v2`[](https://docs.perplexity.ai/guides/chat-completions-guide)​
- **Completions Path:** `/chat/completions`[](https://zuplo.com/learning-center/perplexity-api)​
- **Full Endpoint:** `https://api.perplexity.ai/v2/chat/completions`[]([[github/open-webui/open-webui]] [🔗](https://github.com/open-webui/open-webui)

## **Required Models**

When using this URL, you must also use Perplexity-specific model names instead of OpenAI's `gpt-4`. The current standard models are:

- `sonar`
- `sonar-pro`
- `sonar-reasoning` (or `sonar-reasoning-pro`)[](https://docs.perplexity.ai/api-reference/chat-completions-post)​

## **Key Comparison**

| Feature            | OpenAI Setting              | Perplexity Setting          |
| ------------------ | --------------------------- | --------------------------- |
| **Base URL**       | `https://api.openai.com/v1` | `https://api.perplexity.ai/v2` |
| **Model Example**  | `gpt-4o`                    | `sonar`                     |
| **API Key Format** | `sk-...`                    | `pplx-...`                  |

**Important Note:** Some plugins automatically append `/v1` to whatever base URL you provide. If your plugin fails with `https://api.perplexity.ai/v2`, try leaving it as is, or check if the plugin has a specific "Perplexity" preset that handles the URL structure for you.[]([[github/open-webui/open-webui]] [🔗](https://github.com/open-webui/open-webui)

## How to set ChatGPT MD to use PPLX

1. Paste your **Perplexity API key** into the plugin’s **OpenAI API Key** field (since the plugin will send it as a bearer token).​
2. Set the OpenAI-compatible endpoint to: `https://api.perplexity.ai/v2` (ChatGPT MD supports setting a custom OpenAI endpoint URL via an `openaiUrl` parameter / custom endpoint setting).
3. Change your model from `openai@gpt-…` to a Perplexity model name, e.g.:

   - `openai@sonar` (cheaper/faster)
   - `openai@sonar-pro` (stronger)
