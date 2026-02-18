---
tags: [litellm, feature-plan, architecture, python, automation]
created: 2025-02-13
status: superseded
superseded-by: "[[PLAN_Discovery_TUI_Rewrite]]"
---

# Feature Plan: Multi-Provider Smart Discovery Orchestrator

## ⚠️ Session Status Update (2026-02-19) — Plan Superseded

This plan has been superseded by **[[PLAN_Discovery_TUI_Rewrite]]**.

Key changes in the new plan:
- `TARGETS`/`ROLES` replaced by `FAMILIES` dict — no static model slots
- All family-matched models loaded into config (not just one per slot)
- Parallel LLM calls per provider pick best model per family (replaces `score_model_id()`)
- `rich`+`questionary` TUI replaces headless execution
- `profile.yaml` persists selected launch model
- Safe per-provider config merge (existing entries preserved for skipped providers)

See `PLAN_Discovery_TUI_Rewrite.md` for implementation details.

---

## ✅ Session Status Update (2026-02-18) [[PLAN_Smart_Model_Discovery.md]]

### What is solved

- Secret externalization is active via `scr/setup-secretstore.ps1` + `scr/set-env.ps1`.
- Startup path hardening is in place (`scr/start-proxy.ps1` derives local paths and supports discovery mode switching).
- Multi-provider orchestrator exists and writes deterministic config with backup:
  - `scr/discovery-orchestrator.py`
  - `scr/providers/openrouter_provider.py`
  - `scr/providers/xai_provider.py`
  - `scr/providers/gemini_provider.py` (SDK-based)
  - `scr/providers/perplexity_provider.py`
- Responses API test path is implemented (`scr/test-claude-code.ps1` -> `/v1/responses`).
- Routing validated for OpenRouter-backed models via proxy (`claude`, `deepseek-v3-2`, `kimi-k2-5`).

### What was tried

- Proxy startup in DB mode (`--use_prisma_db_push`) with mixed Python runtimes.
- Authenticated and unauthenticated `/health` checks.
- Direct provider validation (OpenRouter, Perplexity, xAI, Gemini).
- Claude CLI print-mode tests with and without proxy env.
- Discovery dry-run and apply runs to refresh `config.yaml`.

### Root causes identified

1. **Runtime mismatch/DB coupling:** Python/Prisma compatibility issues caused unstable DB startup path.
2. **Auth confusion at health endpoint:** `/health` can return 401/403 if auth header missing.
3. **Upstream provider auth failures:** xAI and Gemini keys are blocked/leaked upstream (403).
4. **Shell/env scope drift:** Claude CLI only routes through proxy when `ANTHROPIC_BASE_URL` and auth token are loaded in the same shell.
5. **MCP schema interference:** some Claude CLI sessions fail with tool schema validation from loaded MCP config (not a LiteLLM routing failure).
6. **Path quoting/whitespace issues:** incorrect quoted paths in PowerShell caused script-not-found failures.

## 🎯 Objective

Create a discovery orchestrator that runs before LiteLLM startup, fetches model catalogs from multiple providers, applies a curated policy, and writes a safe deterministic `config.yaml`.

**Goal:** Keep config current without wildcard sprawl, while preserving predictable aliases and startup reliability.

## 🏗️ Architecture: The "Smart Orchestrator"

We are moving from a single discovery script to a provider-subagent architecture.

### New Startup Sequence

1. **User Runs:** `.\scr\start-proxy.ps1`
2. **Phase 1: Init**
    - Load secrets with `set-env.ps1`.
    - Resolve `config.yaml` path from repo root.
3. **Phase 2: Provider Subagents (parallel)**
    - OpenRouter model catalog subagent.
    - xAI model catalog subagent.
    - Gemini model catalog subagent.
    - Perplexity model catalog subagent.
4. **Phase 3: Normalizer + Curator**
    - Normalize provider responses to a shared schema.
    - Apply curated allowlist/family rules.
    - Build deterministic aliases (`default`, `claude`, `reasoning`, `cheap`, etc.).
5. **Phase 4: Config Writer**
    - Backup `config.yaml` to `config.yaml.bak`.
    - Overwrite `model_list` + `router_settings.model_group_alias`.
    - Preserve other config sections.
6. **Phase 5: Handoff**
    - Start proxy with updated config.
    - If discovery fails, continue with last known good config.

## 🧩 Components

### 1. Discovery Scripts

- `scr/discovery.py` (legacy single-source discovery)
- `scr/discovery-subagents.py` (current curated OpenRouter subagent flow)
- `scr/discovery-orchestrator.py` (planned multi-provider orchestrator)
- `scr/providers/*.py` (planned provider adapters)

### 2. Startup Wrapper

- `scr/start-proxy.ps1`
- Discovery remains **opt-in** via:
  - `LITELLM_ENABLE_DISCOVERY=1`
  - `LITELLM_DISCOVERY_MODE=subagents|orchestrator|legacy`

## 🔌 Integration with Existing Systems

| Feature | Component | Timing | Purpose |
| :--- | :--- | :--- | :--- |
| **Availability** | **Discovery Orchestrator** | **Startup** | Keeps curated model config up to date. |
| **Pricing** | **Existing Auto-Sync** | **Background** | Updates model pricing/cost map. |
| **Reliability** | **Config Backup + Fallback** | **Startup** | Prevents broken startup from discovery failures. |

## 🛠️ Implementation Steps

1. **Baseline (Done):**
    - Add `discovery-subagents.py`.
    - Add `run-subagent-discovery.ps1`.
    - Keep closed OpenRouter list as default config.
2. **Provider Adapters (Done, credential-dependent):**
    - Implemented xAI/Gemini/Perplexity/OpenRouter adapter modules.
    - Key-aware inclusion implemented (providers are skipped/logged when unavailable).
3. **Orchestrator (Done):**
    - Merges provider outputs.
    - Applies curated model policy and aliases.
    - Writes deterministic config with backup.
4. **Startup Integration (Done):**
    - Added `orchestrator` mode in `start-proxy.ps1`.
5. **Testing (In Progress):**
    - Dry-run and apply tests completed.
    - Responses alias checks completed for OpenRouter-backed routes.
    - Remaining: post-key-rotation tests for xAI/Gemini.

## 🔜 Next Actions

> **This plan is superseded.** See [[PLAN_Discovery_TUI_Rewrite]] for current next actions.

## ⚠️ Risks & Mitigations

- **Risk:** API outage or latency blocks startup.
  - *Mitigation:* Strict timeouts, fallback to previous config, and opt-in discovery.
- **Risk:** Config drift or corruption.
  - *Mitigation:* Backup file on each write and deterministic writer logic.
- **Risk:** Model explosion from provider catalogs.
  - *Mitigation:* Curated closed-list policy (no wildcard insertion).
- **Risk:** Missing keys cause partial updates.
  - *Mitigation:* Provider-level skip with explicit logs and non-fatal continuation.
