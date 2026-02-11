---
created: 2026-01-28
updated: 2026-01-28
tags:
  - ai/tools
  - discovery
  - registry
status: draft
---

# AI Ecosystem Discovery (How We Know)

> This note documents exactly how we verify what is installed, subscribed, and authenticated.

## 1) Sources of Truth (Auto-Detectable)

- Windows installed apps (HKLM/HKCU Uninstall registry)
- Global npm packages
- Python packages
- VS Code extensions
- Running services/processes
- Known config files / env vars (auth evidence)

## 2) How I Would Check (Commands)

### Installed Apps
- HKLM: `Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* | Select-Object DisplayName, DisplayVersion`
- HKLM 32-bit: `Get-ItemProperty HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\* | Select-Object DisplayName, DisplayVersion`
- HKCU: `Get-ItemProperty HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* | Select-Object DisplayName, DisplayVersion`

### Global npm Packages
- `npm list -g --depth=0`

### Python Packages
- `pip list --format=columns`

### VS Code Extensions
- `code --list-extensions`

### Running Services/Processes
- `Get-Process | Where-Object { $_.ProcessName -match 'ollama|litellm|node|python|code' }`
- `tasklist | findstr /i "ollama litellm node python code"`

### Auth Evidence (Config/Env)
> Do NOT paste secrets. Only record paths or env var names.

Common env vars to check:
- OPENAI_API_KEY
- ANTHROPIC_API_KEY
- GOOGLE_API_KEY
- PPLX_API_KEY
- GROK_API_KEY
- OPENROUTER_API_KEY

Common config locations to inspect (paths only):
- `%USERPROFILE%\.config\` (many CLIs)
- `%APPDATA%\` and `%LOCALAPPDATA%\`
- `C:\Users\YC\LiteLLM\litellm-config\` (LiteLLM)
- `C:\Users\YC\MCPs\` (MCP servers)

## 3) Canonical Registry Fields (Per Tool)

- Name
- Type: Subscription / App / IDE / CLI / API / Extension
- Provider
- Status: Active / Inactive / Unknown
- Last Used
- Cost/Plan
- Auth Method: API key / OAuth / Cookie / Local / Unknown
- Auth Location: env var, config file path, keychain, browser session
- Connection: provider/endpoint/model
- Evidence: command output, registry entry, config path

## 4) Evidence Log (Append as you verify)

- Date:
- Tool:
- Evidence:
- Result:

## 5) Unknowns Queue

- [ ] Fill in auth method for tools with unknown linkage
- [ ] Confirm provider/endpoint for IDE extensions
- [ ] Confirm which CLIs are configured vs merely installed
