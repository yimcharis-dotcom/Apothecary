---
name: litellm-claude-proxy-routing
description: Use when Claude Code should route through a local LiteLLM proxy and requests fail with 401, 502, connection refused, health-check confusion, or model-alias mismatch.
---

# LiteLLM Claude Proxy Routing

## Purpose

Use this workflow to verify and stabilize Claude Code -> LiteLLM -> provider routing with minimal guesswork.

## Quick Flow

1. Load env in the same shell that will run Claude:
   - `.\scr\set-env.ps1`
2. Start proxy:
   - `.\scr\start-proxy.ps1`
3. Verify routed call (authoritative check):
   - `.\scr\test-claude-code.ps1 -Model claude -Prompt "Reply with exactly: OK"`

Do not treat `/health` alone as success/failure; `/v1/responses` success is the routing truth.

## Triage Checklist

1. **Connection refused**
   - Proxy not running in this shell/context.
   - Restart proxy and test again.
2. **401/403**
   - Missing/invalid `LITELLM_MASTER_KEY` in current shell.
   - Confirm `set-env.ps1` ran successfully.
3. **502 from provider**
   - Upstream provider auth/key issue; test provider directly.
4. **Model invalid**
   - Alias not present in `config.yaml`.
   - Run orchestrator/subagent discovery and recheck alias map.
5. **Claude CLI schema/tool errors**
   - Separate from proxy routing.
   - Isolate with strict empty MCP config for debugging.

## Known Good Commands

```powershell
.\scr\set-env.ps1
$env:PYTHONUTF8="1"
$env:PYTHONIOENCODING="utf-8"
.\scr\start-proxy.ps1
```

```powershell
.\scr\set-env.ps1
claude -p --model claude "Reply with exactly: OK"
```

## Common Root Causes

- Shell env not shared between proxy and Claude process.
- API keys present but blocked upstream (xAI/Gemini leak blocks).
- DB/Prisma runtime mismatch causing unstable startup when DB mode is enabled.
- PowerShell path quoting issues in long absolute paths.
