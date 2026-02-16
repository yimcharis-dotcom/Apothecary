---
tags: [litellm, config, grok, pplx, ai/api, ai/tools, claude, claudeCode, chatgpt, gemini, openrouter]
created: 2025-01-25
updated: 2026-02-12
location: C:\Users\YC\LiteLLM\litellm-config\config.yaml
---

# LiteLLM config.yaml Reference


## Configuration Structure

```yaml
model_list:
  - model_name: <what-you-call-it>
    litellm_params:
      model: <provider>/<actual-model-name>
      api_key: os.environ/API_KEY_NAME

litellm_settings:
  master_key: "sk-litellm-master-key-12345"
  drop_params: true
  set_verbose: true
```
Check Docs for specific providers: [liteLLM Docs for providers](https://docs.litellm.ai/docs/providers)


## Current Models

### 🤖 Grok Models (X.AI) 

#### Reasoning Models
- `grok-4-1-fast-reasoning` - Latest, fast with reasoning
- `grok-4-fast-reasoning` - Previous gen, fast with reasoning

#### Non-Reasoning Models
- `grok-4-1-fast-non-reasoning` - Latest, fast without reasoning
- `grok-4-fast-non-reasoning` - Previous gen, fast without reasoning

#### Stable Version
- `grok-4-07-09` - Stable release from July 9, 2024

#### Specialized Models
- `grok-code-fast-1` - **Optimized for coding** ⭐
- `grok-3-beta` - Beta version
- `grok-3-mini-beta` - Smaller beta version

#### Vision/Image Models
- `grok-2-image-1212` - Can generate images
- `grok-2-vision-1212` - Can read/analyze images

**API Key:** Uses `XAI_API_KEY` from environment

---

### 🔍 Perplexity Models (PPLX)

- `perplexity-sonar` - Standard search-enhanced
- `perplexity-sonar-pro` - Pro version
- `perplexity-sonar-deep-research` - Deep research mode
- `perplexity-sonar-reasoning-pro` - Reasoning + search

**API Key:** Uses `PERPLEXITY_API_KEY` from environment

---

### 💬 ChatGPT Models (Subscription/OAuth)

- `chatgpt-4o` - GPT-4o via Plus subscription
- `chatgpt-o1` - o1-preview via subscription

**Auth:** Uses Browser OAuth (Device Flow). No API key needed, but requires manual login on first use.

---

### 💎 Gemini Models (Google)

- `gemini-2.0-flash` - Fast, multimodal
- `gemini-1.5-pro` - Large context window

**API Key:** Uses `GEMINI_API_KEY` from environment

---

### 🌐 OpenRouter Models

- `openrouter-claude-3-7-sonnet` - Claude 3.7
- `openrouter-deepseek-r1` - DeepSeek R1

**API Key:** Uses `OPENROUTER_API_KEY` from environment

---

### Proxy Settings

```yaml
litellm_settings:
  master_key: "sk-litellm-master-key-12345"
  drop_params: true
  set_verbose: true

# general_settings:
#   database_url: "os.environ/DATABASE_URL" # Disabled due to SQLite issues on Windows
#   store_model_in_db: true
```

#### What These Do:

**`master_key`:**
- Acts as the authentication token
- Used in `ANTHROPIC_AUTH_TOKEN` environment variable
- Claude Code uses this to authenticate with the proxy

**`drop_params: true`:**
- Removes unsupported parameters automatically
- Prevents errors when Claude Code sends Anthropic-specific params
- Makes proxy more flexible

**`set_verbose: true`:**
- Enables detailed logging
- Useful for debugging
- Shows what's happening in real-time

---

## Related Files
- [[set-env.ps1.md.ps1]] - API keys setup
- [[10_Prompt library/20_AI tools/202_GatewayProxy/2020_LiteLLM_ClaudeCode/v0/LiteLLM Proxy Installation]] - LiteLLM installation
- [[10_Prompt library/20_AI tools/202_GatewayProxy/2020_LiteLLM_ClaudeCode/v0/LiteLLM Proxy - Startup Guide]] - How to start the proxy
