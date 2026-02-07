---
created: 2026-01-28
updated: 2026-02-01T00:00:00
tags:
  - ai/tools
  - dashboard
  - registry
status: active
---

# AI Ecosystem Dashboard

At-a-glance view of: subscriptions, installed tools, APIs, and auth/connection status.

- Map (project context): `Apothecary/90_Inbox/AI_Ecosystem_Map.md`
- Discovery (how we verify): `Apothecary/AI_Ecosystem_Discovery.md`

## ✅ KPIs (Verified 2026-01-28)

| KPI | Value | Notes |
| --- | ---: | --- |
| Service Providers | 37 | Unique vendors/projects (de-duplicated) |
| Paid subscriptions | 5 | Anthropic, OpenAI, Cursor, Perplexity, xAI |
| Installed apps | 28+ | User-scope apps + Agents + Skill Tools |
| Editors/IDEs | 10 | Standalone IDEs and Extensions |
| Global CLIs (npm) | 8+ | gemini-cli, codex, qwen-code, opencode-ai, aider, bun, etc. |
| VS Code extensions | 54? | `code --list-extensions` (Recent: Cline, Roo, CloudCode, Kilo, Kombai) |
| Python packages | 113 | `pip list` |
| Local AI runtime | Ollama installed | Not running; endpoint would be `http://localhost:11434` |
| Auth status coverage | Incomplete | Most auth/connection rows still Unknown (needs config/env verification) |

## 💳 Paid Subscriptions (Manual List)

> Fill these in from receipts/billing pages. This is the only reliable way.

| Service | Plan | $/mo | Status | Evidence |
| --- | --- | ---: | --- | --- |
| ChatGPT | ChatGPT Plus | $20 | ✅ Active | Master List |
| Claude | Claude Pro | $20 | ✅ Active | Master List |
| Perplexity | Perplexity Pro | $20 | ✅ Active | Master List |
| Cursor | Cursor Pro | $20 | ✅ Active | Master List |
| xAI (Grok) | Grok Premium | $25 | ✅ Active | Master List |

## 🖥️ Installed Apps (Verified)

| App | Version | Role | Status |
| --- | --- | --- | --- |
| Ollama | 0.15.0 | Local models runtime | Installed (not running) |
| Cursor |  | IDE | Installed |
| VS Code | 1.108.2 (User) | IDE | Installed |
| Windsurf | 1.13.13 | IDE | Installed |
| Zed | 0.220.6 | IDE | Installed |
| Perplexity | 1.5.0 | App | Installed |
| Antigravity | 1.15.8 | App | Installed |
| OP.GG | 2.0.11 | App | Installed |
| Lenovo AI Now | 1.3.3.912 | Utility | Installed |
| Kilo code | | IDE Extension | Installed |
| Kombai | | IDE Extension | Installed |
| Claude Code (Ext) |  | Agent (Autonomous) | Installed |
| OpenHands |  | Agent Platform | Installed |
| Aider |  | Agent (Autonomous) | Installed |
| Bun |  | Runtime | Installed |
| HF Cache |  | Cache/Hub | Installed |
| Skills Hub Fleet |  | Agent Fleet | Consolidated skills framework |

## 🧰 Dev Tools (Verified)

| Tool | Version |
| --- | --- |
| Node.js | 25.3.0 |
| npm | 11.6.2 |
| pnpm | 10.28.1 |
| Python | 3.14.2 (+ 3.12 installed) |
| Git | 2.52.0.windows.1 |
| PowerShell | 7.5.4 |

## 🧩 CLIs (Global npm, Verified)

| CLI | Version | Likely Provider |
| --- | --- | --- |
| @google/gemini-cli | 0.25.2 | Google |
| @openai/codex | 0.89.0 | OpenAI |
| @qwen-code/qwen-code | 0.8.1 | Qwen |
| opencode-ai | 1.1.36 | Anomaly |
| wrangler | 4.60.0 | Cloudflare |
| pnpm | 10.28.1 | Local tooling |

## 🧩 VS Code (Verified)

| Item | Value |
| --- | ---: |
| Extensions installed | 49 |
| AI-related extensions (examples) | anthropic.claude-code, continue.continue, github.copilot, google.geminicodeassist, openai.chatgpt, qwenlm.qwen-code-vscode-ide-companion |

## 🧪 Python (Verified)

| Item | Value |
| --- | ---: |
| Packages installed | 113 |
| Key AI packages (examples) | litellm 1.81.1, mcp 1.26.0, openai 2.15.0, huggingface_hub 1.3.3 |

## 🌐 API Providers (Auth + Endpoint)

> This is the "who you can call" list. Most rows are Unknown until we verify config/env.

| Provider | Base URL / Endpoint | Auth Method | Auth Location | Status |
| --- | --- | --- | --- | --- |
| Ollama | `http://localhost:11434` | Local | Local service | Verified installed (not running) |
| OpenAI |  | Email+Pass | Master List | Not verified |
| Anthropic |  | OAuth | Master List | Not verified |
| Google AI / Gemini |  | OAuth | Master List | Not verified |
| Perplexity |  | OAuth | Master List | Not verified |
| xAI (Grok) |  | X.com auth | Master List | Not verified |
| OpenRouter |  | API Key | Master List | Not verified |
| DeepSeek |  | Google OAuth | Master List | Not verified |

## 🔐 Auth + Connections (To Be Filled)

> This is the core of your goal: tool -> auth -> provider/endpoint. We fill this by checking config/env (without copying secrets).

| Tool | Auth Method | Auth Location | Connection | Status |
| --- | --- | --- | --- | --- |
| codex CLI | Unknown | Unknown | OpenAI | Not verified |
| gemini-cli | Unknown | Unknown | Google | Not verified |
| qwen-code | Unknown | Unknown | Qwen | Not verified |
| claude-code (VS Code) | Unknown | Unknown | Anthropic | Not verified |
| continue (VS Code) | Unknown | Unknown | Provider? | Not verified |
| Ollama | Local | Local service | localhost:11434 | Verified installed |

## 🔌 Connections Map (Tool -> Provider)

> Wiring diagram. This should match the table above once verified.

| Tool | Talks To | How |
| --- | --- | --- |
| codex CLI | OpenAI | API (key or OAuth) |
| gemini-cli | Google | API (key or OAuth) |
| qwen-code | Qwen | API (key or OAuth) |
| claude-code (VS Code) | Anthropic (or proxy) | API (key or OAuth) |
| continue (VS Code) | Unknown (could be local Ollama or remote) | Config-driven |
| wrangler | Cloudflare | OAuth / API token |

## ❓ Unknowns Queue (Next Verifications)

- [ ] Fill in Auth Method/Auth Location for codex CLI (OpenAI)
- [ ] Fill in Auth Method/Auth Location for gemini-cli (Google)
- [ ] Fill in Auth Method/Auth Location for qwen-code
- [ ] Confirm what Continue is configured to use (Ollama? OpenAI-compatible? LiteLLM?)
- [ ] Confirm whether LiteLLM proxy is present and where its config lives

## ⚠️ Corrections vs Earlier Report

- Python packages count is **113** (not 142)
- VS Code extensions count is **49** (not 47)
- Editors/IDEs count is **4** (not 3)
- `sqlalchemy` and `psycopg2` are **not installed**

## 🔗 Sources

- Map: `C:\Vault\Apothecary\90_Inbox\AI_Ecosystem_Map.md`
- Discovery: `C:\Vault\Apothecary\AI_Ecosystem_Discovery.md`
- Registry: `C:\Vault\Apothecary\90_Inbox\Registry`
