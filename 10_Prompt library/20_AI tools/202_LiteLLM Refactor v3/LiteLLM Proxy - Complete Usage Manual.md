---
tags: [litellm, guide, usage, proxy, management, troubleshooting]
created: 2025-02-12
---

# LiteLLM Proxy - Complete Usage Manual

This manual provides a complete guide for managing, using, and troubleshooting your LiteLLM proxy. It covers daily operations, model selection, integration patterns, and production workflows.

## 📖 Quick Reference Card

### 🚀 Starting & Stopping
- **Start Proxy:** `.\scr\start-proxy.ps1` (or `litellm --config config.yaml`)
- **Stop Proxy:** `Ctrl+C` in terminal, or `Stop-Process -Name litellm -Force`
- **Health Check:** `curl http://localhost:4000/health` (should return `{"status":"healthy"}`)

### 🔍 Monitoring & Logs
- **View Spend:** `.\scr\view-spend.ps1`
- **Daily Activity:** `.\scr\view-daily-activity.ps1`
- **User Spend:** `.\scr\view-user-spend.ps1 -UserId <username>`
- **Live Logs:** `Get-Content "C:\Users\YC\LiteLLM\logs\proxy.log" -Tail 50 -Wait`

### 🔄 Model Sync & Updates
- **Check Status:** `.\scr\check-sync-status.ps1`
- **Force Sync:** `.\scr\sync-models.ps1`
- **Enable Auto-Sync:** `.\scr\enable-auto-sync.ps1`

---

## 🗓️ Daily Operations Guide

### Starting Your Day
1.  Open a PowerShell terminal as Administrator (recommended).
2.  Navigate to the project root: `cd "C:\Vault\Apothecary\10_Prompt library\20_AI tools\202_LiteLLM Refactor v3"`
3.  Run the startup script: `.\scr\start-proxy.ps1`
4.  Verify the proxy is running: The terminal should show "Proxy Server Started on http://0.0.0.0:4000".

### Switching Between Models
- **No Restart Needed:** You can switch models in your client application (e.g., Claude Code, Cursor) simply by changing the model name (e.g., from `grok-code-fast-1` to `claude-3.5-sonnet`).
- **Config Changes:** If you *edit* `config.yaml` to add/remove models or change aliases, you **must restart** the proxy for changes to take effect.

### Monitoring Usage
- Run `.\scr\view-daily-activity.ps1` periodically to check spend and token usage.
- Use the detailed flag for granular data: `.\scr\view-daily-activity.ps1 -Detailed`.

### End-of-Day Procedures
- **Optional:** Stop the proxy to save resources if not running as a background service.
- **Review Spend:** Check total daily spend to ensure budget compliance.

---

## 🤖 Model Selection Guide

Use this matrix to choose the right model for your task:

| Use Case | Recommended Model | Alternative | Why? |
| :--- | :--- | :--- | :--- |
| **Coding** | `grok-code-fast-1` | `deepseek-chat` | Optimized for code generation, fast inference. |
| **Reasoning** | `claude-opus-4` | `grok-4-1-fast-reasoning` | High complexity handling, superior logic. |
| **Research** | `perplexity-sonar-deep-research` | `perplexity-sonar-pro` | Real-time web search integration, citation support. |
| **Speed/Chat** | `claude-3.5-haiku` | `grok-4-1-fast-non-reasoning` | Extremely fast response times, low cost. |
| **General** | `claude-3.5-sonnet` | `gpt-4o` | Best balance of performance, cost, and speed. |
| **Multilingual**| `qwen-2.5-72b` | `gpt-4o` | Excellent performance across diverse languages. |

---

## 🔗 Integration Patterns

### PowerShell Scripts
```powershell
$headers = @{ "Authorization" = "Bearer sk-litellm-master-key-12345" }
$body = @{
    model = "grok-code-fast-1"
    messages = @(@{ role = "user"; content = "Hello world" })
}
Invoke-RestMethod -Uri "http://localhost:4000/v1/chat/completions" -Method Post -Headers $headers -Body ($body | ConvertTo-Json)
```

### Python (OpenAI SDK)
```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-litellm-master-key-12345",
    base_url="http://localhost:4000"
)

response = client.chat.completions.create(
    model="claude-3.5-sonnet",
    messages=[{"role": "user", "content": "Hello world"}]
)
print(response.choices[0].message.content)
```

### curl Command
```bash
curl http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-litellm-master-key-12345" \
  -d '{
    "model": "grok-code-fast-1",
    "messages": [{"role": "user", "content": "Hello world"}]
  }'
```

### Claude Code CLI
```bash
# Set environment variables (PowerShell):
$env:ANTHROPIC_BASE_URL="http://127.0.0.1:4000"
$env:ANTHROPIC_AUTH_TOKEN="sk-litellm-master-key-12345"

# Run command:
claude --model claude-3.5-sonnet "Refactor this file"
```

---

## 🏭 Production Deployment Guide

### Monitoring Setup
- **Uptime:** Use a service monitor (e.g., Uptime Kuma) to ping `/health` every minute.
- **Alerts:** Configure Slack/Email alerts in `config.yaml` for budget thresholds.

### Backup Procedures
- **Configuration:** Regularly backup `config.yaml` and `set-env.ps1`.
- **Database:** Backup `litellm.db` (SQLite) daily if maintaining critical spend logs.

### Scaling Considerations
- **Load Balancing:** Add multiple API keys for the same model in `config.yaml` to distribute load.
- **Redis:** Enable Redis caching in `general_settings` for high-traffic environments.

### Security Best Practices
- **Master Key:** Rotate `LITELLM_MASTER_KEY` periodically.
- **Network:** Restrict access to port 4000 using firewall rules (allow only localhost or trusted IPs).
- **HTTPS:** Set up an Nginx reverse proxy with SSL for remote access.

---

## 🛠️ Troubleshooting Manual

### Common Issues & Fixes

**Issue:** "Model not found" error
- **Fix:** Check `config.yaml` for typo in `model_name`. Verify alias exists if using one. Restart proxy.

**Issue:** 401 Unauthorized
- **Fix:** Verify `Authorization: Bearer <key>` matches `LITELLM_MASTER_KEY` in `set-env.ps1`.

**Issue:** 500 Internal Server Error (Provider Error)
- **Fix:** Check specific provider API key in `set-env.ps1`. Check provider status page. Check proxy logs for detailed error message.

**Issue:** Cost tracking showing $0.00
- **Fix:** Ensure `track_cost: true` is in `config.yaml`. Verify model is supported in cost map (`.\scr\check-sync-status.ps1`).

---

## ⚡ Performance Optimization

- **Caching:** Enable simple caching in `config.yaml` to serve repeated requests instantly.
- **Streaming:** Use `stream=True` in client requests for lower perceived latency.
- **Fast Models:** Use `haiku` or `flash` variants for non-complex tasks.
