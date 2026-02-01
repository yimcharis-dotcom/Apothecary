
# Claude AI Ecosystem Master List

**Last Updated:** 2026-01-31
**Format:** Canonical table structure (Provider → Product/Plan → Capability → Surface → Connected To → Presence → Auth → Status)

ho---

## Structure Rationale

This master list is a **dashboard inventory** of everything AI-related you have **installed or actively used on this laptop**, plus the **platforms/services those items connect to**. The canonical structure is 8 columns so every entry can be compared and filtered consistently:

| Column | Definition | Examples |
|--------|------------|----------|
| **Provider** | Vendor, org, or project behind the tool/service | Claude (Anthropic), OpenAI, Google, Ollama, Llama.cpp |
| **Product/Plan** | Specific app/tool/model or subscription tier | Claude Pro ($20/mo), Claude Code, OpenAI API, Ollama runtime, qwen2.5-coder |
| **Capability** | What it does (function) | Web Chat, IDE Integration, CLI, SDK, MCP Gateway, Local Model |
| **Surface** | Where/how you access it on this laptop | <https://claude.ai>, Cursor IDE, VS Code Extension, Terminal, Localhost |
| **Connected To** | Integration target(s) or downstream systems | Browser, LiteLLM proxy, Vault Bridge MCP, Obsidian vault, Continue |
| **Presence** | Where it primarily exists | Local, Web, Hybrid |
| **Auth** | How access is authenticated | OAuth, Email+Pass, API Key, Local |
| **Status** | Current state on this laptop | ✅ Active, ⚠️ Configured/Degraded, ⏸️ Paused |

### Key Design Decisions

1. **Inventory scope**: Includes **cloud platforms + local apps/extensions/runtimes/models** you have installed or actively used on this laptop.

2. **Row meaning**: Each row is a **single installed tool, model, or subscription plan** you can launch or call from this machine.

3. **Products vs Capabilities**: Claude Code, Codex, APIs, and local runtimes are **Products**. Capabilities describe what the product does (e.g., "IDE Integration", "CLI", "SDK").

4. **Surface vs Connected To**: **Surface** is the access channel (URL/app/CLI/extension). **Connected To** is what it integrates with (proxy, MCP, vault, runtime, or downstream service).

5. **Provider scope**: External vendors **and** local infrastructure projects can be Providers. This keeps the dashboard honest about what is actually installed.

6. **Presence is filterable**: Local = installed on this laptop, Web = account-only or browser-only, Hybrid = local client + cloud API.

7. **Auth/Status are operational**: These columns support auditing and troubleshooting, not taxonomy.

### Example Reading

```
| Provider | Product/Plan | Capability | Surface | Connected To | Presence | Auth | Status |
| Claude (Anthropic) | Claude Code | IDE Integration | Cursor IDE | Primary dev (17 processes) | Local | OAuth | ✅ |
```

Reads as: **Anthropic** offers **Claude Code** which provides **IDE Integration**, accessed via **Cursor IDE**, connected to your **primary dev environment (17 processes running)**, present **locally**, authenticated via **OAuth**, and currently **active**.

---

## Master Reference Table

| Provider | Product/Plan | Capability | Surface | Connected To | Presence | Auth | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Anthropic** | Claude Pro ($20/mo) | Interface (Browser) | <https://claude.ai> | Browser | Web | OAuth | ✅ |
| | Claude Code | Agent (Autonomous) | Terminal, Cursor, VS Code | Dev environment (17 procs) | Local | OAuth | ✅ |
| | Claude API | API (Model Provider) | anthropic-python, LiteLLM | Direct calls, Proxies | Hybrid | OAuth | ✅ |
| | Claude Desktop | MCP Gateway | Desktop App | Vault Bridge, Obsidian MCP | Local | OAuth | ✅ |
| | Claude Server Commander | CLI Utility | Terminal | MCP Server Management | Local | OAuth | ✅ |
| | OpenClaude | CLI Utility | Terminal | Alternative Interface | Local | OAuth | ✅ |
| **OpenAI** | ChatGPT Plus ($20/mo) | Interface (Browser) | <https://chatgpt.com> | Browser | Web | Email+Pass | ✅ |
| | Codex | CLI Utility | @openai/codex | Global npm tool | Local | Email+Pass | ✅ |
| | OpenAI API | API (Model Provider) | openai-python | Direct calls | Hybrid | Email+Pass | ✅ |
| **Cursor** | Cursor Pro ($20/mo) | IDE | Cursor IDE (v1.x) | Windows, Claude backend | Local | VS Code auth | ✅ |
| **VS Code** | VS Code (Free) | IDE | VS Code | | Local | | ✅ |
| **Codeium** | Windsurf IDE | IDE | Windsurf IDE | Flow backend (multi-provider) | Local | OAuth | ✅ |
| **Zed Industries** | Zed (Free) | IDE | Zed IDE | None (local editor) | Local | Local | ✅ |
| **BerriAI** | LiteLLM Proxy | API (Router/Proxy) | <http://localhost:8000> | Grok, Perplexity routing | Local | Local | ⚠️ |
| **Anomaly** | opencode-ai | CLI Utility | opencode-ai (npm global) | Model providers (varies) | Local | Local | ✅ |
| **Perplexity** | Perplexity Pro ($20/mo) | Interface (Search) | <https://perplexity.ai> | Browser | Web | OAuth | ✅ |
| | Perplexity App | Interface (Mobile/Desktop) | Native app | Cross-platform | Local | OAuth | ✅ |
| | Perplexity API | API (Search) | perplexity-sonar | LiteLLM proxy | Hybrid | OAuth | ✅ |
| **xAI** | Grok Premium ($25/mo) | Interface (Social) | <https://x.com/i/grok> | Browser/X.com | Web | X.com auth | ✅ |
| | Grok API | API (Model Provider) | grok models | LiteLLM proxy | Hybrid | X.com auth | ✅ |
| **Google** | Gemini (Free) | Interface (Browser) | <https://gemini.google.com> | Browser | Web | OAuth | ✅ |
| | Gemini CLI | CLI Utility | @google/gemini-cli | Global npm tool | Local | OAuth | ✅ |
| | Gemini Code Assist | IDE Extension | google.geminicodeassist | VS Code Extension | Local | OAuth | ✅ |
| | Antigravity | IDE | IDE | Google AI integration | Local | OAuth | ✅ |
| | Gemini API | API (Model Provider) | google-generativeai | Direct calls | Hybrid | OAuth | ✅ |
| | Google AI Studio | API Playground | <https://aistudio.google.com> | Browser | Web | OAuth | ✅ |
| | Google Cloud (Varies) | Infrastructure | <https://console.cloud.google.com> | Enterprise deployments | Web | API Keys | ✅ |
| | CloudCode | IDE Extension | VS Code | Cloud Platform Integration | Local | OAuth | ✅ |
| **Qwen** | Qwen (Free) | Interface (Browser) | <https://qwenlm.alibaba.com> | Browser | Web | Qwen OAuth | ✅ |
| | Qwen CLI | CLI Utility | @qwen-code/qwen-code | Global npm tool | Local | Qwen OAuth | ✅ |

| **Obsidian** | Obsidian (Free) | Knowledge Base | Desktop App | C:\Vault\Apothecary | Local | Local | ✅ |
| **Vault Bridge** | Vault Bridge MCP | MCP Server | MCP Server | LocalDocs RAG, Vault queries | Local | Local | ✅ |
| **OpenMCP** | OpenMCP Config | MCP Infrastructure | Local config | MCP connections | Local | Local | ✅ |
| **LocalDocs** | LocalDocs RAG | Knowledge / RAG | Local scripts | Vault Bridge MCP | Local | Local | ✅ |
| **Vault** | Apothecary Vault | Knowledge Base | C:\Vault\Apothecary | LocalDocs, Vault Bridge | Local | Local | ✅ |
| **Moonshot AI** | Kimi (Free) | Interface (Browser) | <https://kimi.moonshot.cn> | Browser | Web | Google OAuth | ✅ |
| **DeepSeek** | DeepSeek (Free) | Interface (Browser) | <https://chat.deepseek.com> | Browser | Web | Google OAuth | ✅ |
| **Meta** | Meta AI (Free) | Interface (Browser) | <https://www.meta.ai> | Browser | Web | Facebook auth | ✅ |
| **POE** | POE (Free) | Interface (Multi-Model) | <https://poe.com> | Browser/Mobile | Web | POE account | ✅ |
| **Brave** | Brave Search (Free) | API (Search) | <https://api.search.brave.com> | Moltbot gateway | Web | API Key | ✅ |
| **OpenRouter** | OpenRouter (Varies) | API (Aggregator) | <https://openrouter.ai> | Cost optimization | Web | API Key | ✅ |
| **Ollama** | Ollama (Free) | Inference Layer | <http://localhost:11434> | Multi-App (Continue, Obsidian, RAG) | Local | None | ✅ |
| **ggml.ai** | Llama.cpp (Free) | Inference Layer | Terminal | Alternative to Ollama | Local | None | ✅ |
| **AnythingLLM** | AnythingLLM (Free) | Knowledge / RAG | Desktop app | Local doc indexing | Local | Local | ✅ |
| **Kilo** | Kilo code | IDE Extension | VS Code | | Local | | ✅ |
| **Kombai** | Kombai | IDE Extension | VS Code | | Local | | ✅ |
| **Cline** | Cline | Agent (Autonomous) | VS Code | Multi-Provider API | Local | API Key | ✅ |
| **Roo** | Roo Code | Agent (Autonomous) | VS Code | Multi-Provider API | Local | API Key | ✅ |
| **ByteDance** | Trae / TraeCN | IDE | Trae IDE | Adaptive AI (CN/Global) | Local | OAuth | ✅ |
| **All-Hands-AI** | OpenHands | Agent Platform | Web UI (Local) | Multi-Provider API | Local | API Key | ✅ |
| **Aider** | Aider | Agent (Autonomous) | Terminal | Multi-Provider API | Local | API Key | ✅ |
| **Oven** | Bun | Infrastructure | Terminal | JS Toolkit | Local | None | ✅ |
| **Hugging Face** | HF Cache | Infrastructure | Local Directory | SDKs / Transformers | Local | API Key | ✅ |
| **Skills Hub** | Agent Fleet | Agent Swarm | Terminal | MoltBot, Junie, Qoder, Neovate, etc. | Local | OAuth | ✅ |
| **OpenMCP** | McpJam (Dev) | MCP Dev Tool | Terminal | MCP Server Testing | Local | | ✅ |

---

## Connection Map & Data Flows

### Primary Development Workflow

```
Claude (Anthropic)
├─ Cursor IDE (Primary environment, 17 processes)
│  └─ Claude backend for code generation
├─ VS Code Extensions
│  ├─ Claude Code extension
│  ├─ Continue (uses Ollama local models)
│  ├─ Codeium (free code completion)
│  └─ Gemini (Google code assistance)
└─ Claude Desktop App (MCP gateway)
   ├─ Vault Bridge MCP → queries Vault (C:\Vault\Apothecary)
   │  └─ Routed to: Grok or Perplexity (configurable default)
   └─ Obsidian MCP → queries Obsidian vault
```

### Knowledge Base Integration

```
Vault (C:\Vault\Apothecary)
├─ Indexed by: LocalDocs RAG (embeddings via nomic-embed-text)
├─ Queried via: Vault Bridge MCP
│  └─ Connected to: Claude Desktop → Claude, Grok, Perplexity
└─ Obsidian vault (parallel)
   └─ Connected via: Obsidian MCP
      └─ Accessible from: Claude Desktop
```

### Local LLM & Code Assistance

```
Ollama Runtime (http://localhost:11434)
├─ Models: llama3.1:8b, qwen2.5-coder:1.5b, nomic-embed-text
└─ Used by: Continue VS Code Extension
   ├─ Chat capability (llama3.1)
   ├─ Autocomplete capability (qwen-coder)
   └─ Embeddings (nomic-embed for RAG)
```

### Multi-Provider Routing

```
LiteLLM Proxy (http://localhost:8000)
├─ Grok: 10 variants (grok-4-1-fast, grok-code, grok-2-vision, etc.)
├─ Perplexity: 4 variants (sonar, sonar-pro, sonar-deep-research, sonar-reasoning)
└─ Used by: CLI tools, programmatic access, custom integrations
```

### Quick Provider Network

| From | To | Mechanism | Purpose |
|------|----|-----------|---------|
| Claude | Cursor IDE | Direct | Code generation (primary) |
| Claude | VS Code | Extension | IDE plugin |
| Claude | Vault Bridge MCP | MCP protocol | Knowledge base queries |
| Claude | Obsidian MCP | MCP protocol | Vault access |
| Grok | Vault Bridge MCP | Default provider | Knowledge base |
| Perplexity | Vault Bridge MCP | MCP integration | Web search in queries |
| Grok | LiteLLM | Proxy routing | Multi-model access |
| Perplexity | LiteLLM | Proxy routing | Multi-model access |
| Ollama | Continue extension | Local | Code completion + chat |
| Ollama | LocalDocs RAG | Embeddings | Vector indexing |
| Gemini | VS Code | Extension | Code assistance |
| Codeium | VS Code | Extension | Code completion |
| OpenRouter | CLI/API | Aggregator | Cost-optimized routing |
| AnythingLLM | LocalDocs | RAG | Document indexing |

---

## Summary & Inventory

### Subscriptions & Cost

| Provider | Plan | Cost | Status |
|----------|------|------|--------|
| Claude (Anthropic) | Pro | $20/mo | ✅ Active |
| ChatGPT (OpenAI) | Plus | $20/mo | ✅ Active |
| Cursor | Pro | $20/mo | ✅ Active |
| Perplexity | Pro | $20/mo | ✅ Active |
| Grok (xAI) | Premium | $25/mo | ✅ Active |
| **TOTAL PAID** | **5 subscriptions** | **$105/mo** | |

### Free Services

- **Chat Interfaces:** Gemini, Qwen, Kimi, DeepSeek, Meta AI, POE
- **Code Assistance:** Codeium, Monica (browser extension)
- **Knowledge:** Obsidian (local vault)
- **Local Inference:** Ollama, Llama.cpp
- **RAG/Search:** AnythingLLM, Brave Search, OpenRouter

### IDE Ecosystem

- **Primary:** Cursor (17 running processes, Claude backend)
- **VS Code:** Main editor with 49 extensions (9+ AI-related)
- **Dedicated Editors:** Gemini IDE, Qwen IDE, Codeium IDE
- **Continue Extension:** Local code assistance via Ollama

### Integration Infrastructure

- **MCPs Configured:** Vault Bridge (Grok/Perplexity routing), Obsidian, Perplexity, OP.GG
- **Local Runtimes:** Ollama (<http://localhost:11434>), Llama.cpp
- **Proxy Routers:** LiteLLM (multi-model), OpenRouter (cost optimization)

### CLI Tools

- Global npm: @google/gemini-cli, @qwen-code/qwen-code, openai-codex, and others
- Python: 113 packages (LiteLLM, MCP, SDKs, ML libraries)

### Total Ecosystem

| Metric | Count |
|--------|-------|
| Service Providers | 36 |
| Paid Subscriptions | 5 |
| Free Services | 11+ |
| VS Code Extensions (all) | 54 |
| AI-related Extensions | 9+ |
| MCP Servers | 4 |
| Global CLIs | 6+ |
| Python Packages | 113+ |

---

## Key Architecture Decisions

1. **Primary Dev Environment:** Cursor IDE with Claude backend
2. **Default Knowledge Base:** Vault Bridge MCP with Grok as default provider (fallback to Perplexity)
3. **Local Inference:** Ollama for private code completion and embeddings
4. **Web Search:** Perplexity integrated via MCP for real-time queries
5. **Code Assistance:** Continue extension for local + Cursor/VS Code for cloud

---

## Metadata

- **Format Version:** 5.0 (Presence-aware canonical structure)
- **Last Updated:** 2026-01-31
- **Structure:** Provider → Product/Plan → Capability → Surface + Connections + Presence
- **Scope:** External service providers only (excludes custom infrastructure implementation)
- **Completeness:** 100% (37 providers documented)
- **Next Phase:** Build web app dashboard to visualize connections and manage subscriptions
