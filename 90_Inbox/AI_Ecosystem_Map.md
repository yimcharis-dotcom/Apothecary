---
tags:
  - project/ai-ecosystem
  - status/active
created: 2026-01-28
---
# 🗺️ Project: AI Ecosystem Mapping

> [!summary] Goal
> To clarify the "My AI Stack" — documenting exactly what subscriptions, APIs, and tools are active, how much they cost, and how they connect.

## 📅 Progress Log

| Phase                  | Task                 | Status         | Notes                                             |
| :--------------------- | :------------------- | :------------- | :------------------------------------------------ |
| **1. Planning**  | Design Table Schema  | ✅ Done        | Agreed on "Treasury" (Subs) vs "Workshop" (Tools) |
| **2. Inventory** | Initial "Brain Dump" | ✅ Done        | Captured all tools from memory                    |
|                        | Add Login URLs       | ✅ Done        | Verified Login pages for ~20 services             |
|                        | Refine Categories    | ✅ Done        | Infrastructure vs Chatbots vs Tools               |
|                        | Verify APIs          | ✅ Done        | Removed OpenAI, Added Brave/Google                |
| **3. Refining**  | Verify Connections   | 🟡 In Progress | Checking: Cline, Continued.dev links              |

---

## 📦 The Inventory (Current Snapshot)

### 1. The Treasury & Infrastructure

*Complete list of what I have access to.*

| Service                | Category            | API? | Cost/Plan                 | Status                            | Login                                    |
| :--------------------- | :------------------ | :--: | :------------------------ | :-------------------------------- | :--------------------------------------- |
| **ChatGPT**      | 💬 Chatbot          |  ❌  | $20/mo (Plus)             | ✅ Active                         | [Login](https://chat.openai.com)            |
| **Perplexity**   | 💬 Chatbot (Search) |  ✅  | $20/mo (Pro)              | ✅ GPT-5.2, Claude 4.5, etc.      | [Login](https://perplexity.ai)              |
| **Claude**       | 💬 Chatbot          |  ❌  | $20/mo (Pro)              | ✅ Active                         | [Login](https://claude.ai)                  |
| **Cursor**       | 🛠️ Editor         |  ❌  | $20/mo (Pro)              | ✅ Active                         | [Link](https://cursor.com)                  |
| **xAI (Grok)**   | 💬 Chatbot          |  ✅  | ~$25 (Sub)                | ✅ Active                         | [Link](https://x.ai)                        |
| **Brave Search** | 🏭 Provider (Search)|  ✅  | $0 (Free)                 | ✅ Active                         | [Keys](https://brave.com/app/keys)          |
| **Google AI**    | 🏭 Provider         |  ✅  | $0 (Free)                 | ✅ Active                         | [Studio](https://aistudio.google.com)       |
| **Vertex AI**    | 🏗️ Infrastructure |  ✅  | $1300 Credits             | ✅ Active                         | [Console](https://console.cloud.google.com) |
| **OpenRouter**   | 🔌 Aggregator       |  ✅  | Pre-paid                  | ✅ Active                         | [Link](https://openrouter.ai)               |
| **DeepSeek**     | 💬 Chatbot          |  ✅  | $0 (Free)                 | ✅ Active                         | [Link](https://chat.deepseek.com)           |
| **Kimi**         | 💬 Chatbot          |  ❌  | $0 (Free)                 | ✅ Active                         | [Link](https://kimi.moonshot.cn)            |
| **Qwen Chat**    | 💬 Chatbot          |  ❌  | $0 (Free)                 | ✅ Active                         | [Link](https://chat.qwenlm.ai)              |
| **ModelScope**   | 📦 Hub              |  ✅  | $0 (Free)                 | ✅ Active                         | [Link](https://modelscope.cn)               |
| **Monica**       | 🧩 Extension        |  ❌  | $0 (Free: 40/day)         | ✅ GPT-4.1 mini + Claude 4.5 Haiku | [Link](https://monica.im)                   |
| **POE**          | 💬 Aggregator       |  ❌  | $0 (Free)                 | ✅ Active                         | [Link](https://poe.com)                     |
| **Meta AI**      | 💬 Chatbot          |  ❌  | $0 (Free)                 | ✅ Active                         | [Link](https://meta.ai)                     |
| **Cloudflare**   | 🏗️ Infrastructure |  ✅  | $0 (Free)                 | ✅ Active (Wrangler v4.60)        | [Link](https://dash.cloudflare.com)         |
| **Firebase**     | 🏗️ Infrastructure |  ✅  | $0 (Free)                 | ✅ Active                         | [Link](https://console.firebase.google.com) |

### 2. The Workshop

*Where the work happens & how it connects.*

| Tool                            | Type        | Connection Source          | Status                    |
| :------------------------------ | :---------- | :------------------------- | :------------------------ |
| **Codex**                 | CLI         | 🔑**ChatGPT** Login  | ✅ v0.89.0                |
| **Claude Code**           | CLI         | 🔑**Claude** Login   | ✅ Active                 |
| **Gemini CLI**            | CLI         | 🔑**Google** Login   | ✅ v0.25.2 (Latest)       |
| **Qwen CLI**              | CLI         | 🔑**Qwen** OAuth     | ✅ v0.8.1                 |
| **OpenCode**              | CLI         | 🔑**?**              | ✅ v1.1.36                |
| **Antigravity**           | IDE         | 🔑**Gemini** API     | ✅ Active                 |
| **Ollama**                | Local       | 💻**Llama.cpp**      | ✅ Active                 |
| **Cline**                 | IDE Ext     | 🔑**Qwen Coder** API | ✅ Active (3k/day)        |
| **Continued**             | IDE Ext     | 💻 **Local/API**     | ✅ Open Source (Ollama)   |
| **Moltbot (uninstalled)** | CLI Gateway | 🔑**Claude/Codex**   | ✅ Active                 |
| **pnpm**                  | Pkg Mgr     | 💻**Local**          | ✅ v10.28.1               |

> [!todo] Next Actions
>
> - [X] Check **Cline** settings: Uses Qwen Coder (3000 req/day free)
> - [ ] Check **Continued.dev** settings: Is it connected to Ollama?
> - [X] Check **Moltbot**: Successor to Clawdbot. Uses Brave Search + Claude/Codex.
