---
tags: [litellm, grok, pplx, ai/api, config, claude, claudeCode, agent, openrouter]
created: 2025-01-25
updated: 2026-02-12
---

# LiteLLM Proxy - Startup Guide

## Quick Start (3 Steps)

### 1. Start the Proxy

We have a unified startup script that loads keys and starts the server.

```powershell
# In PowerShell:
C:\Users\YC\LiteLLM\litellm-config\start-proxy.ps1
```

**You should see:**

```
LiteLLM: Proxy Server Started on http://0.0.0.0:4000
Available models: grok-4-1-fast-reasoning, perplexity-sonar-pro, chatgpt-4o, ...
```

**Proxy is now running at:** `http://localhost:4000`

---

### 2. Test It's Working

**In another PowerShell window:**

```powershell
# List available models:
curl http://localhost:4000/v1/models

# Test a simple request (Grok):
curl http://localhost:4000/v1/chat/completions `
  -H "Content-Type: application/json" `
  -H "Authorization: Bearer sk-litellm-master-key-12345" `
  -d '{
    "model": "grok-code-fast-1",
    "messages": [{"role": "user", "content": "Say hello!"}]
  }'
```

---

### 3. Using with Claude Code / Agents

**Environment Variables (Recommended)**

In your terminal (PowerShell):

```powershell
# Point Anthropic SDKs to your local proxy
$env:ANTHROPIC_BASE_URL = "http://127.0.0.1:4000"
$env:ANTHROPIC_AUTH_TOKEN = "sk-litellm-master-key-12345"
```

**Test in Claude Code:**

```bash
# Now use any model defined in your config:
claude --model grok-code-fast-1 "Write hello world in Python"
claude --model perplexity-sonar-deep-research "Research quantum computing"
```

---

## Available Models

Once proxy is running, you can use these models:

### Grok Models (xAI)

```bash
grok-4-1-fast-reasoning          # Latest with reasoning
grok-4-1-fast-non-reasoning      # Latest without reasoning
grok-code-fast-1                 # 🌟 BEST FOR CODING
grok-3-beta                      # Beta version
grok-2-image-1212                # Image generation
```

### Perplexity Models (Search)

```bash
perplexity-sonar-pro             # Pro version (Smart search)
perplexity-sonar-deep-research   # Deep research (Long queries)
perplexity-sonar-reasoning-pro   # Reasoning + search
```

### ChatGPT Models (Subscription/OAuth)

**Note:** Requires browser authentication on first use. See [Troubleshooting](#troubleshooting).

**Update (Feb 2026):** GPT-4o/4.1 series retiring Feb 13, 2026. Defaulting to GPT-5.2.

```bash
chatgpt-5-2-instant              # New Flagship (2026)
chatgpt-5-2-thinking             # New Reasoning Model (2026)
chatgpt-4o                       # Retiring soon
chatgpt-o1                       # o1-preview via subscription
```

### Gemini Models (Google)

```bash
gemini-3                         # New 2026 Flagship
gemini-3-flash                   # New Default Fast Model
gemini-2.0-flash                 # Deprecated (Ends Mar 2026)
gemini-1.5-pro                   # Large context window
```

### OpenRouter / Anthropic Models

```bash
openrouter-claude-opus-4-6       # Claude Opus 4.6 (New Feb 2026)
openrouter-claude-haiku-4-5      # Claude Haiku 4.5 (Fast)
openrouter-deepseek-chimera      # DeepSeek Chimera (Free/Experimental)
openrouter-claude-3-7-sonnet     # Claude 3.7 via OpenRouter
openrouter-deepseek-r1           # DeepSeek R1 via OpenRouter
```

---

## Agent Skills

We have installed **Agent Skills** to help build autonomous agents.

**Location:** `C:\Users\YC\.agents\skills`

### Installed Skills

1. **`create-agent`**: Blueprints for building modular AI agents with OpenRouter.
2. **`openrouter-typescript-sdk`**: TypeScript SDK for OpenRouter.

**How to use:**
These are reference skills for Trae/Claude to understand how to build agents. You can ask Trae:
> "Build a new agent using the create-agent skill"

---

## Troubleshooting

### ChatGPT Authentication ("Unusual UI")

When using `chatgpt-4o` or `chatgpt-o1`, you may see a "Sign in" prompt in the terminal.

1. **Terminal Message:**

    ```
    Sign in with ChatGPT using device code:
    1) Visit https://device.auth0.com/oauth2/device/verify
    2) Enter code: ABCD-1234
    ```

2. **Action:** Open the URL, enter the code, and click "Authorize".
3. **UI:** The page is a simple Auth0 page, not the main ChatGPT chat interface. This is normal.

### Database / Cost Tracking

* **Status:** **Disabled**
* **Reason:** SQLite compatibility issues with LiteLLM on Windows.
* **Impact:** The `/spend` endpoints and budget tracking are currently unavailable. The proxy functionality for routing requests works perfectly.

### Logs

**Enable Verbose Logging:**
Set in `config.yaml`:

```yaml
litellm_settings:
  set_verbose: true
```
