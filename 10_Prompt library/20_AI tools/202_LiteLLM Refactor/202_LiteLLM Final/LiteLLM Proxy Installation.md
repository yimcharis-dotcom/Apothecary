---
tags: [litellm, setup, ai/tools, pplx, grok, claude, claudeCode]
created: 2025-01-25
updated: 2026-02-12
status: completed
github: https://github.com/BerriAI/litellm
Docs: https://docs.litellm.ai/docs
---

# LiteLLM Proxy Installation Log

## Installation Details

### Method: pip (User)
**Date:** 2026-02-12
**Version:** 1.81.10
**Python:** 3.14 (User install)
**Environment:** PowerShell 7+ on Windows 11

### Installation Command
```powershell
# Run in PowerShell
pip install --user litellm --upgrade --force-reinstall
```

### Installed Location
```
C:\Users\YC\AppData\Roaming\Python\Python314\Scripts\litellm.exe
```

## Configuration Files Location

**Config Directory:** `C:\Users\YC\LiteLLM\litellm-config`

Files created/updated:
- `config.yaml` - LiteLLM proxy configuration (Models, Master Key) [[config.yaml]]
- `set-env.ps1` - Environment variables for API keys (Secure storage) [[30_Automation/20_AI tools/202_LiteLLM/set-env.ps1|set-env]]
- `start-proxy.ps1` - One-click startup script [[30_Automation/20_AI tools/202_LiteLLM/start-proxy.ps1|start-proxy]]

## Database Status
**Status:** Disabled
**Reason:** The default Prisma SQLite client is incompatible with the Windows Python environment in this specific setup.
**Workaround:** Cost tracking features are disabled (`database_url` commented out in `config.yaml`). The proxy functions normally for routing requests.

## Next Steps
[[LiteLLM Proxy - Startup Guide]]
