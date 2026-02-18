---
tags: [secretstore, powershell, litellm, setup, runbook]
created: 2026-02-18
status: active
---

# SecretStore Setup and Usage

This note is the quick runbook for storing and loading LiteLLM secrets with PowerShell SecretStore.

## 1) First-time setup

Run once:

```powershell
& "C:\Vault\Apothecary\10_Prompt library\20_AI tools\202_GatewayProxy\2020_LiteLLM_ClaudeCode\v0_refactor_1b\202_LiteLLM Refactor v3 Gemini\scr\setup-secretstore.ps1"
```

What it does:

1. Installs `Microsoft.PowerShell.SecretManagement` and `Microsoft.PowerShell.SecretStore` (CurrentUser).
2. Registers vault `LiteLLM`.
3. Prompts for secret values and saves them.

Secrets prompted by script:

- `LITELLM_MASTER_KEY` (required)
- `OPENROUTER_API_KEY` (optional but needed for OpenRouter routes)
- `PERPLEXITY_API_KEY` (optional)
- `XAI_API_KEY` (optional)
- `GEMINI_API_KEY` (optional)

## 2) Add or update a single secret

```powershell
Set-Secret -Vault LiteLLM -Name OPENROUTER_API_KEY -Secret "your_key_here"
```

Required key example:

```powershell
Set-Secret -Vault LiteLLM -Name LITELLM_MASTER_KEY -Secret "sk-litellm-master-key-xxxxx"
```

## 3) Load secrets into current shell

Run this in every new terminal session before proxy/Claude commands:

```powershell
& "C:\Vault\Apothecary\10_Prompt library\20_AI tools\202_GatewayProxy\2020_LiteLLM_ClaudeCode\v0_refactor_1b\202_LiteLLM Refactor v3 Gemini\scr\set-env.ps1"
```

`set-env.ps1` sets:

- `LITELLM_MASTER_KEY`
- provider keys if present
- `ANTHROPIC_BASE_URL=http://127.0.0.1:4000`
- `ANTHROPIC_AUTH_TOKEN=$env:LITELLM_MASTER_KEY`
- `ANTHROPIC_API_KEY=$env:LITELLM_MASTER_KEY`

## 4) Verify (safe check, no full key print)

```powershell
$names = "LITELLM_MASTER_KEY","OPENROUTER_API_KEY","PERPLEXITY_API_KEY","XAI_API_KEY","GEMINI_API_KEY"
$names | ForEach-Object {
  $v = [Environment]::GetEnvironmentVariable($_, "Process")
  [pscustomobject]@{
    Name   = $_
    Loaded = -not [string]::IsNullOrWhiteSpace($v)
    Length = if ($v) { $v.Length } else { 0 }
  }
} | Format-Table -AutoSize
```

## 5) Normal daily flow

Terminal A:

```powershell
& "C:\Vault\Apothecary\10_Prompt library\20_AI tools\202_GatewayProxy\2020_LiteLLM_ClaudeCode\v0_refactor_1b\202_LiteLLM Refactor v3 Gemini\scr\set-env.ps1"
$env:PYTHONUTF8="1"
$env:PYTHONIOENCODING="utf-8"
& "C:\Vault\Apothecary\10_Prompt library\20_AI tools\202_GatewayProxy\2020_LiteLLM_ClaudeCode\v0_refactor_1b\202_LiteLLM Refactor v3 Gemini\scr\start-proxy.ps1"
```

Terminal B:

```powershell
& "C:\Vault\Apothecary\10_Prompt library\20_AI tools\202_GatewayProxy\2020_LiteLLM_ClaudeCode\v0_refactor_1b\202_LiteLLM Refactor v3 Gemini\scr\set-env.ps1"
claude -p --model claude "Reply with exactly: OK"
```

## 6) Troubleshooting

### Error: `Get-Secret command not found`

```powershell
Install-Module Microsoft.PowerShell.SecretManagement -Scope CurrentUser -Force
Install-Module Microsoft.PowerShell.SecretStore -Scope CurrentUser -Force
```

### Error: `Secret vault 'LiteLLM' not found`

Run setup again:

```powershell
& "C:\Vault\Apothecary\10_Prompt library\20_AI tools\202_GatewayProxy\2020_LiteLLM_ClaudeCode\v0_refactor_1b\202_LiteLLM Refactor v3 Gemini\scr\setup-secretstore.ps1"
```

### Error: `Missing required secret: LITELLM_MASTER_KEY`

```powershell
Set-Secret -Vault LiteLLM -Name LITELLM_MASTER_KEY -Secret "sk-litellm-master-key-xxxxx"
```

### Error: path not recognized

- Always use `& "full path with spaces.ps1"` (quotes required for these folders).
- Do not split the path across lines.

### It works in one terminal but not another

- Env vars are shell-local.
- Run `set-env.ps1` in every terminal where you run `claude` or test scripts.
