---
tags: [architecture, workflow, documentation, standard]
created: 2025-02-15
status: active
---

# Architecture & Workflow Standards

To prevent configuration drift and "missing file" confusion, we strictly enforce a separation between **Source Code** and **Runtime Artifacts**.

## 🏗️ System Layout

| Zone | Path | Purpose | Rules |
| :--- | :--- | :--- | :--- |
| **Vault (Source)** | `.../202_LiteLLM Refactor v3/` | The **Single Source of Truth**. | ✅ **EDIT HERE**<br>❌ NO RUNTIME DATA |
| **Runtime (Prod)** | `C:\Users\YC\LiteLLM\` | The **Active Engine**. | ❌ **DO NOT EDIT**<br>✅ Generates DB/Logs |

## 📂 File Locations

### 1. Configuration & Scripts (Source Controlled)
*Managed in Vault, deployed to Runtime.*
- `config.yaml` — written by `discovery-orchestrator.py`; do not hand-edit
- `profile.yaml` — persists the last user-selected launch model; source-controlled
- `scr/start-proxy.ps1`
- `scr/set-env.ps1`
- `scr/sync-models.ps1`
- `scr/discovery-orchestrator.py` — TUI discovery launcher; run before starting proxy to refresh model list
- `scr/providers/*.py` — provider catalog adapters (OpenRouter, xAI, Gemini, Perplexity)

### 2. Documentation (Vault Only)
*Never deployed to Runtime.*
- `Manual.md`
- `AGENTS.md`
- `ARCHITECTURE.md` (This file)

### 3. Runtime Artifacts (Generated on Start)
*Created by the application. Do not move or edit manually.*
- `litellm.db` (SQLite Database)
- `schema.prisma` (Database Schema)
- `logs/` (Application Logs)

## 🚀 Deployment Workflow

**Never edit files in `C:\Users\YC\LiteLLM` directly.**

1.  **Edit:** Modify `config.yaml` or scripts in the **Vault (`v3`)**.
2.  **Deploy:** Run the deployment script (Coming Soon) or copy manually:
    ```powershell
    Copy-Item "Vault\...\config.yaml" "C:\Users\YC\LiteLLM\litellm-config\"
    ```
3.  **Restart:** Restart the proxy service to apply changes.

## ⚠️ Critical Note on Database
The `litellm.db` and `schema.prisma` files are **stateful**. 
*   **DO NOT** overwrite them from the Vault (they don't exist there).
*   **DO NOT** delete them unless you want to wipe your cost history.
