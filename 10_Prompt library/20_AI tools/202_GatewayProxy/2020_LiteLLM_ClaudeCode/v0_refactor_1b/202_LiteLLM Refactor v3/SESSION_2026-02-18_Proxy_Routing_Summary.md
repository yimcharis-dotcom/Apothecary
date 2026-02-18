---
tags: [session-log, litellm, proxy, claude-code, routing, troubleshooting]
created: 2026-02-18
status: active
---

# Session Summary: LiteLLM Proxy Routing Stabilization

## Objective

Stabilize Claude Code -> LiteLLM proxy routing, migrate test flow to Responses API, externalize secrets, and validate multi-provider discovery behavior.

## What We Changed

1. Secret and env flow:
   - Added/used `scr/setup-secretstore.ps1`.
   - Updated `scr/set-env.ps1` to load required and optional secrets from SecretStore.
   - Set Claude routing env in script (`ANTHROPIC_BASE_URL`, `ANTHROPIC_AUTH_TOKEN`).

2. Startup flow:
   - Updated `scr/start-proxy.ps1` for local path resolution and discovery mode switching.
   - Added default DB-off behavior for local stability unless explicitly enabled.
   - Added runtime guidance around Python 3.12 LiteLLM executable path.

3. Discovery flow:
   - Added orchestrated discovery path:
     - `scr/discovery-orchestrator.py`
     - `scr/providers/openrouter_provider.py`
     - `scr/providers/xai_provider.py`
     - `scr/providers/gemini_provider.py`
     - `scr/providers/perplexity_provider.py`
   - Added launcher scripts:
     - `scr/run-orchestrator-discovery.ps1`
     - `scr/run-subagent-discovery.ps1`

4. API test flow:
   - Updated `scr/test-claude-code.ps1` to use `/v1/responses`.
   - Added authenticated health check behavior with fallback to responses test.

5. Config curation:
   - Kept a closed curated model list.
   - Added/validated aliases (`default`, `claude`, `claude-strong`, `reasoning`, `cheap`, `kimi`, `glm`).

## What We Solved

1. End-to-end routing works through proxy for OpenRouter-backed models:
   - `claude`
   - `deepseek-v3-2`
   - `kimi-k2-5`
2. Direct provider checks confirmed:
   - OpenRouter: pass
   - Perplexity: pass
3. Claude CLI can route through proxy when env is loaded in the same shell.

## What We Tried

1. DB-enabled startup and Prisma migration paths.
2. Multiple health-check styles (with and without auth).
3. Direct `/v1/responses` smoke tests with model aliases.
4. Claude CLI print-mode tests for routed and non-routed scenarios.
5. Discovery dry-run and apply flows.

## Root Causes Identified

1. Python/runtime + Prisma/DB mismatch caused unstable DB startup paths.
2. Health endpoint auth mismatch (missing Bearer key) produced 401/403 noise.
3. Upstream key state:
   - xAI key blocked (leak response)
   - Gemini key blocked/reported leaked
4. Shell-scope env drift:
   - routing fails when Claude is launched from a shell that did not run `set-env.ps1`.
5. MCP schema issue in Claude CLI environment can throw tool schema 400 errors unrelated to proxy routing.
6. PowerShell path quoting/line-break issues caused script not found failures.

## Current Known-Good Runbook

1. Terminal A:
   - `.\scr\set-env.ps1`
   - `$env:PYTHONUTF8="1"`
   - `$env:PYTHONIOENCODING="utf-8"`
   - `.\scr\start-proxy.ps1`

2. Terminal B:
   - `.\scr\set-env.ps1`
   - `claude -p --model claude "Reply with exactly: OK"`
   - or `.\scr\test-claude-code.ps1 -Model claude -Prompt "Reply with exactly: OK"`

## Remaining Gaps

1. Rotate and replace xAI and Gemini keys.
2. Add a one-command launcher for Claude-through-proxy.
3. Add startup diagnostics helper (capture logs + endpoint probe summary).
4. Optional: re-enable DB mode after locking runtime compatibility.
