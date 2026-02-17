---
tags: [agent-guidelines, development, automation, powershell]
created: 2025-02-12
---

# Agent Guidelines for LiteLLM Refactor

This repository contains a PowerShell-based LiteLLM proxy management system. Follow these guidelines for all development and maintenance tasks.

## 🛠️ Build & Test Commands

### Proxy Management

- **Start Proxy:** `.\scr\start-proxy.ps1`
- **Stop Proxy:** `Stop-Process -Name litellm -Force`
- **Health Check:** `curl http://localhost:4000/health`

### Testing

- **Run All Tests:** `.\scr\test-claude-code.ps1`
- **Test Specific Model:**

  ```powershell
  curl http://localhost:4000/v1/chat/completions `
    -H "Authorization: Bearer sk-litellm-master-key-12345" `
    -d '{ "model": "grok-code-fast-1", "messages": [{"role": "user", "content": "Hello"}] }'
  ```

- **Verify Cost Tracking:** `.\scr\view-spend.ps1`

### Auto-Sync & Maintenance

- **Manual Sync:** `.\scr\sync-models.ps1`
- **Check Status:** `.\scr\check-sync-status.ps1`

## 📝 Code Style Guidelines

### PowerShell Scripts (`.ps1`)

- **Naming:** Kebab-case (e.g., `view-daily-activity.ps1`)
- **Parameters:** Always use `param()` block at the top
- **Output:** Use `Write-Host` with `-ForegroundColor` for status updates
- **Error Handling:** Use `try { ... } catch { ... }` blocks for external calls
- **Paths:** Use `$PSScriptRoot` or relative paths; avoid hardcoded absolute paths where possible

### Configuration (`config.yaml`)

- **Structure:** Follow LiteLLM schema strictly
- **Model Naming:** Use provider prefix (e.g., `openrouter/`, `xai/`) in `litellm_params`
- **Aliases:** Define friendly names in `router_settings.model_group_alias`
- **Secrets:** Use `os.environ/VARIABLE_NAME` for API keys

### Documentation (`.md`)

- **Frontmatter:** Include `tags` and `created` date
- **Links:** Use Obsidian-style links `[[Page Name]]` where appropriate
- **Snippets:** Use code blocks with language specifiers (e.g., `powershell`, `yaml`)

## 📂 Repository Structure

```
/
├── config.yaml                    # Main proxy configuration
├── AGENTS.md                      # This file
├── *.md                           # Documentation guides
└── scr/                           # PowerShell scripts
    ├── start-*.ps1                # Startup scripts
    ├── view-*.ps1                 # Monitoring scripts
    ├── sync-*.ps1                 # Maintenance scripts
    └── set-env.ps1                # Environment configuration
```

## 🚀 Development Workflow

1. **Modify Config:** Edit `config.yaml` to add models or change settings
2. **Restart Proxy:** Changes require a restart (`Ctrl+C` then `.\scr\start-proxy.ps1`)
3. **Verify:** Run `.\scr\test-claude-code.ps1` to ensure connectivity
4. **Document:** Update relevant `.md` files if functionality changes

## ⚠️ Critical Rules

- **Never commit API keys:** Use `set-env.ps1` for local secrets
- **Always verify config syntax:** Invalid YAML prevents startup
- **Check proxy health:** Before running complex tests, ensure `/health` returns 200 OK

## Completed

- [x] **Smart Model Discovery:**
  - Implemented `scr/discovery.py` to fetch Anthropic models from OpenRouter.
  - Integrated into `scr/start-proxy.ps1`.
  - Updated `PLAN_Smart_Model_Discovery.md`.
- [x] **ChatGPT Subscription Support:**
  - Configured `config.yaml` with `chatgpt/gpt-5.2` (responses mode).
  - Updated `scr/set-env.ps1` documentation.
- [x] **MCP Server:**
  - Installed `upstash/context7-mcp`.
- [x] **Model Cleanup:**
  - Removed unstable/preview models (Gemini 2.x).
  - Updated OpenRouter aliases to stable versions (`claude-3-5-sonnet`).

## Coming up

- [ ] 1. API Modernization
  - [ ] Check how we call the API now. If still using `completion`, update codes to `response` style (LiteLLM native).
- [ ] 2. Stability: Fix Database
  - [ ] Fix database issues to ensure reliable cost tracking.
- [ ] 3. Integration: Seamless "Claude Code" Launch
  - [ ] Wrap env and launch claude code: Create a wrapper script.
  - [ ] config.json should point to claude code one (Clarify config integration).
- [ ] 4. UX: TUI & Interactive Features
  - [ ] Add TUI to select models (using `rich` library).
  - [ ] Add switch models mid session.
