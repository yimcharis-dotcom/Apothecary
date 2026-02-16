---
tags: [litellm, grok, pplx, ai/api, config, claude, claudeCode]
created: 2025-01-25
---

## Quick Start (3 Steps)

### 1. Set Environment Variables

```powershell
# In PowerShell:
. C:\Users\YC\LiteLLM\litellm-config\set-env.ps1
```

---

### 2. Start the Proxy

```powershell
litellm --config C:\Users\YC\LiteLLM\litellm-config\config.yaml
```

```powershell
cd C:\Users\YC\LiteLLM\litellm-config
litellm --config .\config.yaml --port 4000
```

**You should see:**

```
LiteLLM: Proxy Server Started on http://0.0.0.0:4000
Available models: grok-4-1-fast-reasoning, grok-code-fast-1, ...
```

**Proxy is now running at:** `http://localhost:4000`

---

### 3. Test It's Working

**In another PowerShell window:**

```powershell
# List available models:
curl http://localhost:4000/v1/models

# Test a simple request:
curl http://localhost:4000/v1/chat/completions `
  -H "Content-Type: application/json" `
  -H "Authorization: Bearer sk-litellm-master-key-12345" `
  -d '{
    "model": "grok-code-fast-1",
    "messages": [{"role": "user", "content": "Say hello!"}]
  }'
```

---

## Using with Claude Code

Environment Variables (Recommended)

- [Claude Non-Anthropic Models](https://docs.litellm.ai/docs/tutorials/claude_non_anthropic_models)  
 In PowerShell:

```powershell

. C:\Users\YC\LiteLLM\litellm-config\set-env.ps1
```

Or,

```powershell
$env:XAI_API_KEY = "xai-ap3FR5Oo56oqBOAapUvEmH6XUKwL3bBysMNu5POmqRvkZedTDMMGdUs2KelXRQT43TD0nxRnZeaxRDMk"
$env:PERPLEXITY_API_KEY = "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"

# Claude Code -> LiteLLM proxy
$env:ANTHROPIC_BASE_URL = "http://127.0.0.1:4000"
$env:ANTHROPIC_AUTH_TOKEN = "sk-litellm-master-key-12345"
```

**Test in Claude Code:**

```bash
# In Claude Code terminal:
export ANTHROPIC_BASE_URL=http://127.0.0.1:4000
export ANTHROPIC_AUTH_TOKEN=sk-litellm-master-key-12345

# Now use any model:
claude --model grok-code-fast-1 "Write hello world in Python"
```

---

## Startup Script (One-Command Launch)

**Create:** `C:\Users\YC\LiteLLM\litellm-config\set-env.ps1`

```powershell
# Load environment variables
. C:\Users\YC\LiteLLM\litellm-config\set-env.ps1

# Start proxy
Write-Host "`n🚀 Starting LiteLLM Proxy...`n" -ForegroundColor Green
litellm --config C:\Users\YC\LiteLLM\litellm-config\config.yaml
```

**Usage:**

```powershell
# Just run:
C:\Users\YC\LiteLLM\litellm-config\start-proxy.ps1
```

---

## Available Models

Once proxy is running, you can use these models:

### Grok Models

```bash
grok-4-1-fast-reasoning          # Latest with reasoning
grok-4-1-fast-non-reasoning      # Latest without reasoning
grok-4-fast-reasoning            # Previous gen with reasoning
grok-4-fast-non-reasoning        # Previous gen without reasoning
grok-4-07-09                     # Stable release
grok-code-fast-1                 # 🌟 BEST FOR CODING
grok-3-beta                      # Beta version
grok-3-mini-beta                 # Smaller beta
grok-2-image-1212                # Image generation
grok-2-vision-1212               # Image analysis
```

### Perplexity Models

```bash
perplexity-sonar                 # Standard
perplexity-sonar-pro             # Pro version
perplexity-sonar-deep-research   # Deep research
perplexity-sonar-reasoning-pro   # Reasoning + search
```

## Recommended Models by Task

### For Coding

```bash
claude --model grok-code-fast-1 "Your coding task"
```

### For Reasoning/Analysis

```bash
claude --model grok-4-1-fast-reasoning "Complex problem"
```

### For Research

```bash
claude --model perplexity-sonar-deep-research "Research topic"
```

### For Speed

```bash
claude --model grok-4-1-fast-non-reasoning "Quick task"
```

---

## Logs & Debugging

### Enable Verbose Logging

**Already enabled in your config!**

```yaml
litellm_settings:
  set_verbose: true
```

**You'll see:**

- Every request received
- Which provider it routes to
- Response times
- Any errors

---

### Check Logs

**Proxy logs to console** - just watch the terminal where you started it.

**Save logs to file:**

```powershell
litellm --config C:\Users\YC\LiteLLM\litellm-config\config.yaml > proxy-log.txt 2>&1
```

---

## Stopping the Proxy

**In the proxy terminal:**

```
Press Ctrl+C
```

**Or from another terminal:**

```powershell
# Find the process:
Get-Process | Where-Object {$_.ProcessName -eq "litellm"}

# Kill it:
Stop-Process -Name litellm -Force
```

---
