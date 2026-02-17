---
tags: [litellm, feature-plan, architecture, python, automation]
created: 2025-02-13
status: planned
---

# Feature Plan: Smart Model Discovery System

## 🎯 Objective

Create a "Realtime Discovery Node" that runs before the LiteLLM proxy starts. It uses Provider SDKs to fetch *currently available* models and updates `config.yaml` dynamically.

**Goal:** Ensure dropdown lists in client tools (Claude Code, Cursor) always show the latest models without manual config editing.

## 🏗️ Architecture: The "Smart Orchestrator"

We will enhance the startup flow to include an intelligent pre-flight check.

### New Startup Sequence

1. **User Runs:** `.\scr\start-proxy.ps1`
2. **Phase 1: UI & Init (Python + Rich)**
    * Launch TUI with progress spinner.
    * Load API keys from `set-env.ps1`.
3. **Phase 2: The Fetcher (Parallel Workers)**
    * **Worker A (OpenRouter):** Queries `openrouter.ai/api/v1/models`.
        * *Filter:* **Strict.** Only keep models where `manufacturer == 'Anthropic'`. (Solves "Cooldown Fallback").
    * **Worker B (Native Providers):**
        * Checks xAI for latest `grok-*`.
        * Checks Gemini for `gemini-2.0-*`.
4. **Phase 3: The Configbuilder**
    * Reads existing `config.yaml`.
    * **Section A (Manual):** Preserves custom aliases and specific user settings.
    * **Section B (Dynamic):** Overwrites the "Auto-Discovered" section with the new list.
    * *Auto-Alias:* Creates friendly aliases (e.g., `claude-fallback` -> `openrouter/anthropic/claude-3.5-sonnet`).
5. **Phase 4: Handoff**
    * Python script exits.
    * PowerShell starts `litellm` with the fresh config.

## 🧩 Components

### 1. `scr/discovery.py` (The Brain)

* **Language:** Python 3.14
* **Libraries:** `rich` (UI), `requests` (API), `pyyaml` (Config)
* **Logic:**
  * `fetch_openrouter_anthropic()`: Get fallback models.
  * `fetch_native_providers()`: Get Grok/Gemini models.
  * `update_config()`: Safe injection into YAML.

### 2. `scr/start-proxy.ps1` (The Wrapper)

* **Enhanced Logic:**
  * Check for `discovery.py`.
  * Run Python script.
  * If success -> Start Proxy.
  * If fail -> Warn user -> Start Proxy with old config (Fallback).

## 🔌 Integration with Existing Systems

| Feature | Component | Timing | Purpose |
| :--- | :--- | :--- | :--- |
| **Availability** | **New Discovery Node** | **Startup** | Updates `config.yaml` so models appear in lists. |
| **Pricing** | **Existing Auto-Sync** | **Background** | Updates internal memory for cost tracking. |

## 🛠️ Implementation Steps

1. **Dependencies:** Install `rich`, `requests`, `pyyaml`.
2. **Scripting:** Build `discovery.py` with OpenRouter fetching first.
3. **Orchestration:** Modify `start-proxy.ps1` to chain the scripts.
4. **Testing:** Verify `config.yaml` updates correctly without breaking comments/structure.

## ⚠️ Risks & Mitigations

* **Risk:** API failure slows down startup.
  * *Mitigation:* Set strict timeouts (e.g., 2s) on fetch requests. Proceed if timeout.
* **Risk:** `config.yaml` corruption.
  * *Mitigation:* Create `config.yaml.bak` before every write.
