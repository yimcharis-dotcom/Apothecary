---
Created: 2026-01-13
updated: 2026-01-19T05:57:00
Tags:
  - Ai/mcp
  - perplexity
  - Grok
  - guide
  - Documentation
version: v1.0
---

**Current state** - pending adding indexing before searches: 20260119 5:57am

✅ **Semantic Search** - Finds files by meaning, not keywords  
✅ **Secure** - MCP enforces path boundaries, read-only by default  
✅ **Interactive** - Choose provider/model on the fly  
✅ **Production Ready** - Error handling, config files, logging  
✅ **Source Attribution** - Always know which files were used  
✅ **Multi-AI** - Grok, Perplexity, extensible to more

---

## 📁 **File Structure**

```
2010_vault-bridge/
├── 📄 Obsidian Vault Q&A Bridge - Complete Production Guide.md
├──  📄 Vault Bridge Script Index.md
├── 📄 @complete_bridge.Cjs.md
├── 📄 @config.json.md
├── 📄 @package.json.md
└── scr/
    ├── complete_bridge.Cjs        # Main script
    ├── config.json                # Configuration
    └── package.json               # Dependencies
```

---

## 🚀 **INSTALLATION (One-Time Setup)**

### **1. Install Dependencies:**

```bash
cd "C:\Users\YC\OneDrive\Desktop\MCPs\vault-bridge"
npm install @modelcontextprotocol/sdk
# Node 24+ has built-in fetch, no node-fetch needed
```

### **2. Set API Keys (PowerShell):**

```powershell
# Grok (X.AI)
$env:XAI_API_KEY="your-xai-api-key"

# Perplexity
$env:PPLX_API_KEY="your-perplexity-api-key"

# Optional: Save to profile (permanent)
notepad $PROFILE
# Add: $env:XAI_API_KEY="your-key"

Or set up in `config.json`
```

### **3. Create Optional Config [[@config.json]] :**

```json
{
  "vaultPath": "C:\\Vault\\Apothecary",
  "pythonExe": "C:\\Users\\YC\\OneDrive\\Desktop\\LocalDocs\\.venv\\Scripts\\python.exe",
  "pythonScript": "C:\\Users\\YC\\OneDrive\\Desktop\\LocalDocs\\rag_query_working.py",
  "pythonCwd": "C:\\Users\\YC\\OneDrive\\Desktop\\LocalDocs",
  "maxFiles": 5,
  "maxBytes": 200000,
  "defaultProvider": "grok",
  "temperature": 0.7,
  "xaiApiKey": "optional-alternative-to-env-var",
  "pplxApiKey": "optional-alternative-to-env-var"
}
```

---

## 💻 **USAGE COMMANDS**

### **📌 Basic Query:** #call

```bash
node complete_bridge.cjs "What are my TODOs?"
```

### **🔄 Interactive Mode (Select Provider/Model):**

```bash
node complete_bridge.cjs --interactive "What templates do I have?"
# Will show menu to choose Grok/Perplexity + model
```

### **🤖 With Specific Provider:**

```bash
# Grok with specific model
node complete_bridge.cjs --provider grok --model grok-4-1-fast-reasoning "Explain my MCP setup"

# Perplexity with Sonar Pro
node complete_bridge.cjs --provider pplx --model sonar-pro --temperature 0.9 "How is my vault organized?"
```

### **🔧 Advanced Options:**

```bash
# Custom vault, limit file reading
node complete_bridge.cjs --vault "C:\\MyVault" --max-files 3 --max-bytes 100000 "What's in here?"

# Verbose debugging
node complete_bridge.cjs --verbose "Debug search"
```

### **📋 List Available Models:**

```bash
# List all models
node complete_bridge.cjs --list-models

# List models for specific provider
node complete_bridge.cjs --list-models pplx
```

### **❓ Get Help:**

```bash
node complete_bridge.cjs --help
```

---

## 🛠️ **TROUBLESHOOTING**

### **1. "RAG failed" or Python errors:**

```bash
# Test Python directly
cd "C:\Users\YC\OneDrive\Desktop\LocalDocs"
.venv\Scripts\python.exe rag_query_working.py "test query"
```

### **2. "Missing API key":**

```powershell
# Verify env var is set
echo $env:XAI_API_KEY

# Set it if missing
$env:XAI_API_KEY="your-key"
```

### **3. "MCP server error":**

```bash
# Test MCP server directly
npx -y @modelcontextprotocol/server-filesystem "C:\Vault\Apothecary"
```

### **4. "Module not found" (FAISS):**

```bash
cd "C:\Users\YC\OneDrive\Desktop\LocalDocs"
.venv\Scripts\python.exe -m pip install faiss-cpu sentence-transformers
```

---

## 🔄 **WORKFLOW EXAMPLES**

### **Daily Review:**

```bash
# What should I work on today?
node complete_bridge.cjs "What are my active projects and their status?"

# What meetings do I have notes about?
node complete_bridge.cjs "Find all meeting notes from this week"

# What ideas have I captured?
node complete_bridge.cjs "Show me recent AI interaction notes"
```

### **Project Research:**

```bash
# Research MCP setup
node complete_bridge.cjs --provider pplx "What notes do I have about MCP architecture?"

# Find templates
node complete_bridge.cjs "List all template files in my vault"

# Knowledge queries
node complete_bridge.cjs "What have I learned about Python 3.14 compatibility?"
```

### **Vault Maintenance:**

```bash
# Find duplicates
node complete_bridge.cjs "Find duplicate or similar notes"

# TODO review
node complete_bridge.cjs "Find all unchecked checkboxes [ ] in my vault"

# Tag analysis
node complete_bridge.cjs "What tags do I use most frequently?"
```

---

## ⚙️ **CONFIGURATION OPTIONS**

| Option            | Default                      | Description                  |
| ----------------- | ---------------------------- | ---------------------------- |
| `vaultPath`       | `C:\Vault\Apothecary` | Path to your Obsidian vault  |
| `maxFiles`        | 5                            | Max files to read per query  |
| `maxBytes`        | 200000                       | Max characters to read total |
| `defaultProvider` | `grok`                       | Default AI provider          |
| `temperature`     | 0.7                          | Creativity (0.0-2.0)         |

**Edit in `config.json` or override with CLI flags.**

---

## 📊 **AVAILABLE MODELS**

### **Grok (X.AI):**

- `grok-4-1-fast-reasoning` 🚀 (recommended)
- `grok-4-1-fast-non-reasoning`
- `grok-4-fast-reasoning`
- `grok-4-fast-non-reasoning`
- `grok-4-0709`
- `grok-code-fast-1`
- `grok-3`
- `grok-3-mini`

### **Perplexity:**

- `sonar` (recommended)
- `sonar-pro`
- `sonar-deep-research`
- `sonar-reasoning-pro`

---

## 🔗 Related Systems

### RAG System

- **Location**: `C:\Users\YC\OneDrive\Desktop\LocalDocs\`
- **Python Script**: `rag_query_working.py`
- **Index**: `vault.index` (FAISS vector index)

## 💡 **PRO TIPS**

1. **Be specific** - "What are TODOs for MCP project?" vs "What are TODOs?"
2. **Use verbose mode** - `--verbose` to see what files are being read
3. **Limit scope** - Use `--max-files 3` for faster answers
4. **Try different models** - Some are better for reasoning, others for summarization
5. **Check sources** - Always review which files influenced the answer
6. **Keep RAG updated** - Apothecary index monthly or when vault changes significantly

---

## 🔮 **FUTURE ENHANCEMENTS**

```bash
# Planned features:
# 1. Auto-indexing (watch vault for changes)
# 2. Write operations (create/edit notes)
# 3. Obsidian-specific features (backlinks, graph)
# 4. TUI interface
# 5. Multi-vault support
```

---

## ⚡ **QUICK REFERENCE CARD**

```bash
# QUICK START
node complete_bridge.cjs "your question"

# INTERACTIVE (choose provider/model)
node complete_bridge.cjs -i "question"

# PERPLEXITY WITH SONAR PRO
node complete_bridge.cjs --provider pplx --model sonar-pro "question"

# VERBOSE DEBUGGING
node complete_bridge.cjs --verbose "question"

# LIST MODELS
node complete_bridge.cjs --list-models
```

```bash
# Basic queries
Node complete_bridge. Cjs "your question"
Node complete_bridge. Cjs --vault "C:\Vault\Apothecary" "question"

# Provider/model selection
Node complete_bridge. Cjs --provider grok "question"
Node complete_bridge. Cjs --provider pplx "question"
Node complete_bridge. Cjs --provider grok --model grok-3 "question"
Node complete_bridge. Cjs --provider pplx --model sonar-pro "question"

# Interactive mode
Node complete_bridge. Cjs --interactive "question"
Node complete_bridge. Cjs -i "question"

# Configuration
Node complete_bridge. Cjs --max-files 3 "question"
Node complete_bridge. Cjs --max-bytes 100000 "question"
Node complete_bridge. Cjs --temperature 0.9 "question"

# Information
Node complete_bridge. Cjs --list-models
Node complete_bridge. Cjs --list-models pplx
Node complete_bridge. Cjs --list-models grok
Node complete_bridge. Cjs --help

# Debugging
Node complete_bridge. Cjs --verbose "question"
---
```

## 🎯 \*\*

---

## 📞 **SUPPORT**

1. **Check Python works:** `python rag_query_working.py "test"`
2. **Check API key:** `echo $env:XAI_API_KEY`
3. **Check MCP:** `npx -y @modelcontextprotocol/server-filesystem "vault-path"`
4. **Enable verbose:** Add `--verbose` to see detailed logs

**Your vault now has Claude-like intelligence!** 🚀
