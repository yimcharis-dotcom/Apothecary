---
tags: [litellm, feature-plan, architecture, python, automation]
created: 2025-02-13
status: in-progress
---

# Feature Plan: Multi-Provider Smart Discovery Orchestrator

## 🎯 Objective

Create a discovery orchestrator that runs before LiteLLM startup, fetches model catalogs from multiple providers, applies a curated policy, and writes a safe deterministic `config.yaml`.

**Goal:** Keep config current without wildcard sprawl, while preserving predictable aliases and startup reliability.

## 🏗️ Architecture: The "Smart Orchestrator"

We are moving from a single discovery script to a provider-subagent architecture.

### New Startup Sequence

1. **User Runs:** `.\scr\start-proxy.ps1`
2. **Phase 1: Init**
    * Load secrets with `set-env.ps1`.
    * Resolve `config.yaml` path from repo root.
3. **Phase 2: Provider Subagents (parallel)**
    * OpenRouter model catalog subagent.
    * xAI model catalog subagent.
    * Gemini model catalog subagent.
    * Perplexity model catalog subagent.
4. **Phase 3: Normalizer + Curator**
    * Normalize provider responses to a shared schema.
    * Apply curated allowlist/family rules.
    * Build deterministic aliases (`default`, `claude`, `reasoning`, `cheap`, etc.).
5. **Phase 4: Config Writer**
    * Backup `config.yaml` to `config.yaml.bak`.
    * Overwrite `model_list` + `router_settings.model_group_alias`.
    * Preserve other config sections.
6. **Phase 5: Handoff**
    * Start proxy with updated config.
    * If discovery fails, continue with last known good config.

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
    * Add `discovery-subagents.py`.
    * Add `run-subagent-discovery.ps1`.
    * Keep closed OpenRouter list as default config.
2. **Provider Adapters (Next):**
    * Implement xAI/Gemini/Perplexity adapter modules.
    * Add key-aware inclusion (skip provider if key missing).
3. **Orchestrator (Next):**
    * Merge adapter outputs.
    * Apply curated policy and aliases.
    * Write deterministic config with backup.
4. **Startup Integration (Next):**
    * Add `orchestrator` mode in `start-proxy.ps1`.
5. **Testing (Next):**
    * Dry-run and apply tests.
    * Health checks and sample calls by alias.

## ⚠️ Risks & Mitigations

* **Risk:** API outage or latency blocks startup.
  * *Mitigation:* Strict timeouts, fallback to previous config, and opt-in discovery.
* **Risk:** Config drift or corruption.
  * *Mitigation:* Backup file on each write and deterministic writer logic.
* **Risk:** Model explosion from provider catalogs.
  * *Mitigation:* Curated closed-list policy (no wildcard insertion).
* **Risk:** Missing keys cause partial updates.
  * *Mitigation:* Provider-level skip with explicit logs and non-fatal continuation.
