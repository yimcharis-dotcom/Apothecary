---
tags: [litellm, config, grok, pplx, ai/api, ai/tools, claude, claudeCode]
created: 2025-01-25
location: C:\Users\YC\LiteLLM\litellm-config\config.yaml
---

# LiteLLM config.yaml Reference


## Configuration Structure

```yaml
model_list:
  - model_name: <what-you-call-it>
    litellm_params:
      model: <provider>/<actual-model-name>
      baseUrl: 
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

**API Key:** Uses `XAI_API_KEY` from environment [[Grok API info]]

---

### 🔍 Perplexity Models (PPLX)

**Total Perplexity Models:** 4

- `perplexity-sonar` - Standard search-enhanced
- `perplexity-sonar-pro` - Pro version
- `perplexity-sonar-deep-research` - Deep research mode
- `perplexity-sonar-reasoning-pro` - Reasoning + search

**API Key:** Uses `PERPLEXITY_API_KEY` from environment [[PPLX API info]]

---

### Proxy Settings

```yaml
litellm_settings:
  master_key: "sk-litellm-master-key-12345"
  drop_params: true
  set_verbose: true
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

## How Models Map

```
Claude Code Request:
  "Use grok-code-fast-1"
       ↓
LiteLLM Proxy:
  Sees: model_name = "grok-code-fast-1"
  Maps to: xai/grok-code-fast-1
  Uses: XAI_API_KEY from environment
       ↓
X.AI API:
  Receives request with proper auth
  Returns response
       ↓
Claude Code:
  Receives response as if it was Anthropic
```

---

## Related Files
- [[set-env.ps1.md.ps1]] - API keys setup
- [[LiteLLM Proxy Installation]] - LiteLLM installation
- [[LiteLLM Proxy - Startup Guide]] - How to start the proxy
