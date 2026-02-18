---
tags: [litellm, setup, ai/tools, pplx, grok, claude, claudeCode]
created: 2025-02-12
status: enhanced
github: https://github.com/BerriAI/litellm
Docs: https://docs.litellm.ai/docs
---

# LiteLLM Proxy Installation (Enhanced v3)

This guide covers the installation and setup of the enhanced LiteLLM Proxy v3, including advanced cost tracking, auto-sync features, and production-ready configuration.

## 📦 1. Core Installation

### Prerequisites
- **Python:** 3.10 or higher (3.14 recommended)
- **PowerShell:** 5.1 or 7+ (Admin rights recommended)

### Installation Command
Run as **Administrator** in PowerShell:
```powershell
pip install 'litellm[proxy]'
```

**Verify Installation:**
```powershell
litellm --version
# Expected: 1.x.x
```

## 📂 2. Directory Setup

The enhanced v3 refactor is self-contained. Ensure your directory looks like this:

```
C:\Vault\Apothecary\10_Prompt library\20_AI tools\202_LiteLLM Refactor v3\
├── config.yaml                    # ✅ MAIN CONFIGURATION
├── AGENTS.md                      # Development guidelines
├── LiteLLM Proxy - Startup Guide.md
├── LiteLLM Cost Tracking Guide.md # ✨ NEW
├── LiteLLM Auto-Sync Models Guide.md # ✨ NEW
├── LiteLLM Proxy - Complete Usage Manual.md # ✨ NEW
└── scr/                           # Automation scripts
    ├── start-proxy.ps1            # 🚀 Startup
    ├── set-env.ps1                # 🔑 API Keys
    ├── sync-models.ps1            # 🔄 Model Updates
    ├── check-sync-status.ps1      # 📊 Monitoring
    ├── view-daily-activity.ps1    # 📈 Analytics
    └── view-user-spend.ps1        # 👤 User Tracking
```

## 🔑 3. Configuration & Secrets

### Set API Keys
Edit `scr/set-env.ps1` to add your provider keys:

```powershell
# Edit this file with your actual keys
notepad scr/set-env.ps1
```

**Required Keys:**
- `LITELLM_MASTER_KEY` (Your proxy admin password)
- `OPENROUTER_API_KEY` (For broad model access)
- `ANTHROPIC_API_KEY` (For Claude models)
- `XAI_API_KEY` (For Grok models)
- `PERPLEXITY_API_KEY` (For Sonar models)
- `GEMINI_API_KEY` (For Google models)

### Initialize Environment
Run this once per session to load keys:
```powershell
. .\scr\set-env.ps1
```

## 🚀 4. Starting the Proxy

Use the enhanced startup script which handles environment loading and logging:

```powershell
.\scr\start-proxy.ps1
```

**Success Output:**
```
🚀 Starting LiteLLM Proxy...
📍 Config: ...\config.yaml
🌐 Proxy URL: http://127.0.0.1:4000
```

## 🧪 5. Verification

### Health Check
```powershell
curl http://localhost:4000/health
# Response: {"status":"healthy"}
```

### Test Model Access
```powershell
.\scr\test-claude-code.ps1
```

## 🛠️ Installation Troubleshooting

**Issue:** `litellm: command not found`
- **Fix:** Ensure Python is in your PATH. Try reinstalling: `pip install --force-reinstall 'litellm[proxy]'`

**Issue:** Scripts don't run (Permission Denied)
- **Fix:** Allow script execution: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

## 🔄 6. Auto-Sync Setup (Optional but Recommended)

Enable automatic model pricing updates:

```powershell
.\scr\enable-auto-sync.ps1 -Hours 6
```

## 📚 Next Steps

- **Daily Usage:** See [[LiteLLM Proxy - Complete Usage Manual]]
- **Cost Management:** See [[10_Prompt library/20_AI tools/202_GatewayProxy/2020_LiteLLM_ClaudeCode/v0_refactor_1b/202_LiteLLM Refactor v3/LiteLLM Cost Tracking Guide]]
- **Model Updates:** See [[10_Prompt library/20_AI tools/202_GatewayProxy/2020_LiteLLM_ClaudeCode/v0_refactor_1b/202_LiteLLM Refactor v3/LiteLLM Auto-Sync Models Guide]]
- **Official Docs:** See [[10_Prompt library/20_AI tools/202_GatewayProxy/2020_LiteLLM_ClaudeCode/v0_refactor_1b/202_LiteLLM Refactor v3/LiteLLM Official Documentation References]]
