---
tags:
  - litellm
  - testing
created: 2025-01-25
---

# LiteLLM Proxy - Testing & Verification

## Pre-Flight Checklist

Before starting the proxy, verify:

```powershell
# ✅ 1. LiteLLM is installed
where.exe litellm
# Expected: C:\Program Files\Python314\Scripts\litellm.exe

# ✅ 2. Config file exists
Test-Path C:\Vault\Apothecary\LLMLite\config.yaml
# Expected: True

# ✅ 3. Env script exists
Test-Path C:\Vault\Apothecary\LLMLite\set-env.ps1
# Expected: True
```

---

## Test 1: Start the Proxy

### Method 1: Using the Startup Script

```powershell
C:\Vault\Apothecary\LLMLite\start-proxy.ps1
```

### Method 2: Manual Start

```powershell
# Load environment
. C:\Vault\Apothecary\LLMLite\set-env.ps1

# Start proxy
litellm --config C:\Vault\Apothecary\LLMLite\config.yaml
```

---

## Expected Output

```
LiteLLM: Proxy Server Started on http://0.0.0.0:4000
ℹ️ Ollama not running on your system
ℹ️ Ollama not running on your system
╭──────────────────────────────────────────────────────────────────────────╮
│ LiteLLM Proxy: Test your local proxy (with REST API):                   │
│                                                                           │
│ curl --location 'http://0.0.0.0:4000/chat/completions' \                │
│ --header 'Content-Type: application/json' \                             │
│ --data ' {                                                               │
│      "model": "gpt-3.5-turbo",                                          │
│      "messages": [                                                       │
│        {                                                                 │
│          "role": "user",                                                 │
│          "content": "what llm are you"                                   │
│        }                                                                 │
│      ]                                                                   │
│    }                                                                     │
│ '                                                                        │
╰──────────────────────────────────────────────────────────────────────────╯

INFO:     Started server process [XXXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:4000 (Press CTRL+C to quit)
```

**✅ Success Indicators:**
- "Proxy Server Started on http://0.0.0.0:4000"
- "Application startup complete"
- No error messages

**⚠️ Warning (OK to ignore):**
- "Ollama not running" - Normal if you don't have Ollama

---

## Test 2: Health Check

**In a NEW PowerShell window:**

```powershell
curl http://localhost:4000/health
```

**Expected response:**
```json
{"status":"healthy"}
```

---

## Test 3: List Models

```powershell
curl http://localhost:4000/v1/models
```

**Expected response:**
```json
{
  "data": [
    {"id": "grok-4-1-fast-reasoning", ...},
    {"id": "grok-code-fast-1", ...},
    {"id": "perplexity-sonar-pro", ...},
    ...
  ]
}
```

**✅ Success:** You should see all 14 models listed!

---

## Test 4: Simple Chat Request

### Test with Grok (Fast)

```powershell
curl http://localhost:4000/v1/chat/completions `
  -H "Content-Type: application/json" `
  -H "Authorization: Bearer sk-litellm-master-key-12345" `
  -d '{
    "model": "grok-code-fast-1",
    "messages": [{"role": "user", "content": "Say hello in one word"}]
  }'
```

**Expected response:**
```json
{
  "id": "chatcmpl-...",
  "choices": [{
    "message": {
      "role": "assistant",
      "content": "Hello!"
    }
  }],
  "model": "grok-code-fast-1",
  ...
}
```

---

### Test with Perplexity

```powershell
curl http://localhost:4000/v1/chat/completions `
  -H "Content-Type: application/json" `
  -H "Authorization: Bearer sk-litellm-master-key-12345" `
  -d '{
    "model": "perplexity-sonar",
    "messages": [{"role": "user", "content": "What is 2+2?"}]
  }'
```

---

## Test 5: Claude Code Integration

### Step 1: Verify Environment Variables

```powershell
# Should point to proxy:
$env:ANTHROPIC_BASE_URL
# Expected: http://127.0.0.1:4000

# Should be proxy master key:
$env:ANTHROPIC_AUTH_TOKEN
# Expected: sk-litellm-master-key-12345
```

**If empty:**
```powershell
. C:\Vault\Apothecary\LLMLite\set-env.ps1
```

---

### Step 2: Test with Claude Code CLI

```bash
# Simple test:
claude --model grok-code-fast-1 "Write hello world in Python"
```

**Expected:**
- Claude Code sends request to proxy
- Proxy routes to Grok
- Response appears in terminal

---

### Step 3: Verbose Test (See Full Flow)

**In proxy terminal**, you should see:
```
POST /v1/chat/completions
Model: grok-code-fast-1
Provider: xai
Response time: 1.23s
```

---

## Troubleshooting Failed Tests

### Test 1 Failed: Proxy Won't Start

**Error:** `litellm: command not found`
```powershell
pip install 'litellm[proxy]'
```

**Error:** `ModuleNotFoundError: No module named 'litellm'`
```powershell
# Check Python path:
python --version
where.exe python

# Reinstall:
pip uninstall litellm
pip install 'litellm[proxy]'
```

---

### Test 2 Failed: Health Check Error

**Error:** `Connection refused`
```
Proxy is not running! Go back to Test 1.
```

**Error:** `Timeout`
```powershell
# Check firewall:
# Windows Defender Firewall might be blocking port 4000
# Add exception for Python or LiteLLM
```

---

### Test 3 Failed: No Models Listed

**Error:** Empty model list
```yaml
# Check config.yaml has model_list section
# Restart proxy after any config changes
```

---

### Test 4 Failed: Chat Request Error

**Error:** `401 Unauthorized - Invalid API Key`
```powershell
# Check API keys are set:
$env:XAI_API_KEY
$env:PERPLEXITY_API_KEY

# If empty:
. C:\Vault\Apothecary\LLMLite\set-env.ps1

# Restart proxy
```

**Error:** `500 Internal Server Error`
```
Check proxy logs in the terminal for details.
Common causes:
- Invalid API key for provider
- Provider API is down
- Model name mismatch
```

**Error:** `404 Model Not Found`
```
Model name doesn't match config.yaml
Check: curl http://localhost:4000/v1/models
```

---

### Test 5 Failed: Claude Code Can't Connect

**Error:** Claude Code times out
```powershell
# 1. Check proxy is running:
curl http://localhost:4000/health

# 2. Check environment variables:
$env:ANTHROPIC_BASE_URL  # Should be: http://127.0.0.1:4000
$env:ANTHROPIC_AUTH_TOKEN  # Should be: sk-litellm-master-key-12345

# 3. Reload if empty:
. C:\Vault\Apothecary\LLMLite\set-env.ps1
```

**Error:** "Invalid model"
```bash
# Use exact model name from config.yaml
# ✅ Correct: grok-code-fast-1
# ❌ Wrong: grok-code
```

---

## Success Criteria

**All systems GO when:**

✅ Test 1: Proxy starts without errors  
✅ Test 2: Health check returns `{"status":"healthy"}`  
✅ Test 3: Model list shows all 14 models  
✅ Test 4: Chat requests work for both Grok and Perplexity  
✅ Test 5: Claude Code can access models through proxy  

---

## Performance Benchmarks

**Expected response times:**

| Model | Typical Latency |
|-------|----------------|
| grok-code-fast-1 | 0.5-2s |
| grok-4-1-fast-non-reasoning | 0.5-2s |
| grok-4-1-fast-reasoning | 2-5s |
| perplexity-sonar | 1-3s |
| perplexity-sonar-pro | 2-4s |

**If much slower:**
- Check internet connection
- Try different model
- Check provider status pages

---

## Next Steps After Successful Tests

✅ **All tests passed?**
→ You're ready to use the proxy!

📚 **Learn more:**
- [[model-comparison]] - Which model for what task
- [[advanced-config]] - Add more providers
- [[monitoring]] - Track usage and costs

🎉 **Start using:**
```bash
claude --model grok-code-fast-1 "Your task here"
```

---

## Related Documentation
- [[10_Prompt library/20_AI tools/202_GatewayProxy/2020_LiteLLM_ClaudeCode/v0/LiteLLM Proxy - Startup Guide]] - Quick start instructions
- [[10_Prompt library/20_AI tools/202_GatewayProxy/2020_LiteLLM_ClaudeCode/v0/LiteLLM config.yaml Reference]] - Config file details
- [[set-env-reference]] - Environment variables
