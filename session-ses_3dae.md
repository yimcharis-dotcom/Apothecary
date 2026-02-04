---
words:
  2026-02-04: 3306
---
# Read-Only Plan: AI HubWatch Automation Refactor Discussion

**Session ID:** ses_3dae10a02ffefr7KBTH6OFdbg3
**Created:** 04/02/2026, 04:08:31
**Updated:** 04/02/2026, 04:43:03

---

## User

C:\Vault\Apothecary\30_Automation\303_AI_HubWatch - Automation\src_refactor read this first

---

## Assistant (Plan · kimi-k2.5-free · 2.9s)

**Tool: read**



---

## Assistant (Plan · kimi-k2.5-free · 2.5s)

**Tool: glob**



---

## Assistant (Plan · kimi-k2.5-free · 2.0s)

**Tool: read**



---

## Assistant (Plan · kimi-k2.5-free · 4.2s)

 I've read your session planning document. I can see you're working on refactoring the AI Hub scripts with concerns about:

1. **Detection issues** - Folders like `C:\Users\YC\Perplexity` not being identified correctly
2. **Deletion tracking** - Deletions not being detected
3. **Scope creep** - You want to track more than just configs (plans, transcripts, etc.)
4. **Exclusions** - GitHubRepo being monitored when it shouldn't be

Let me read the key files to understand the current architecture before we discuss the plan:

**Tool: read**

**Tool: read**

**Tool: read**

**Tool: read**

---

## Assistant (Plan · kimi-k2.5-free · 7.8s)

 I now understand the architecture. Here's what I found:

## Issues Identified

1. **"Perplexity" not detected** - It's not in the `StrictKeywords` list in `AIToolsConfig.ps1:111-116`

2. **Deletion detection exists** - WatchHub_Realtime.ps1:405-509 has deletion logic, but may have issues

3. **GitHubRepo monitoring** - It's explicitly included in `WatchHub_Realtime.ps1:74-78` with `Category: Projects_GitHubRepo`

4. **Scope expansion** - Currently only tracking configs via `AIToolDefinitions` structure

## Key Questions Before I Draft the Plan:

1. **Perplexity** - Should I add "perplexity" to the AI tools list? What config files does it use?

2. **Deletion issues** - Are you seeing folders being deleted but junctions remaining in AI_hub? Or logs not being created?

3. **Exclusions** - Should GitHubRepo be completely excluded, or moved to an optional/explicit opt-in category?

4. **Scope expansion** - What specific file types beyond configs should be tracked? (e.g., `.md` plans, `.txt` transcripts, `.json` settings?)

---

## User

lol sorry i was going to say read"THESE". understand the project first

---

## Assistant (Plan · kimi-k2.5-free · 10.9s)

 Let me read all the relevant project files to fully understand the architecture.

**Tool: read**

**Tool: read**

**Tool: read**

**Tool: read**

**Tool: read**

**Tool: read**

**Tool: read**

**Tool: read**

---

## Assistant (Plan · kimi-k2.5-free · 72.0s)

  Now I have a complete understanding of the project. Here's my analysis:

## Current Architecture Summary

**Core System:**
- **AIToolsConfig.ps1** (525 lines) - "Brain" - Single source of truth for AI tool definitions, keywords, categories, validation
- **WatchHub_Realtime.ps1** (808 lines) - "Watcher" - 7 FileSystemWatchers with debouncing, mutex locking, config validation
- **SyncSkills.ps1** (252 lines) - "Hands" - Skill synchronization via symlinks
- **Hub.ps1** (233 lines) - "Control Center" - Interactive menu + CLI dispatcher

**Key Features:**
- Real-time monitoring: UserHome, AppData (Roaming/Local), Programs, GitHubRepo, RootDot
- Auto-linking AI tools to `AI_hub` junctions
- Skills auto-sync across all agents
- Concurrency protection (mutex + debouncing)
- Obsidian inventory export

## Issues You Mentioned

1. **Perplexity not detected** - It's not in `StrictKeywords` (AIToolsConfig.ps1:111-116)
2. **Deletion detection** - Logic exists (WatchHub_Realtime.ps1:405-509) but may have issues
3. **GitHubRepo monitoring** - Explicitly enabled (WatchHub_Realtime.ps1:74-78)
4. **Scope expansion** - Currently only tracking configs

## Questions to Refine the Plan

1. **Perplexity**: Add "perplexity" keyword + what config files should it look for?

2. **Deletion issues**: What's the actual behavior you're seeing? (junctions not being removed when folders are deleted?)

3. **GitHubRepo**: Should it be completely removed from monitoring, or moved to an optional category?

4. **Scope expansion**: What file types beyond configs? (`.md` plans, `.txt` transcripts, `.pdf` docs?) And should these be tracked in a different way than the junction-based approach?

---

## User

tell me what i wanna do from the scripts and note

---

## Assistant (Plan · kimi-k2.5-free · 14.6s)
 Based on your planning document and the code I've reviewed, here's what you want to accomplish:

## 1. Fix AI Tool Detection
**Problem:** Perplexity folders (`C:\Users\YC\Perplexity`, `C:\Users\YC\Perplexity - Copy`) aren't being recognized as AI tools.

**Root cause:** Looking at `AIToolsConfig.ps1:111-116`, "perplexity" isn't in the `$script:StrictKeywords` list. The detection logic only matches folders against the strict keywords (claude, cursor, ollama, mcp, etc.).

## 2. Fix Deletion Detection
**Problem:** When folders are deleted from the system, WatchHub isn't detecting/cleaning up the junctions in `AI_hub`.

**Current state:** The deletion logic exists in `WatchHub_Realtime.ps1:405-509`, but it may not be working correctly. The FileSystemWatcher's Deleted event fires when the folder is removed from the filesystem, but the junction in `AI_hub` might not be getting cleaned up.

## 3. Expand Scope Beyond Configs
**Problem:** You want to track more than just config files—specifically "plans, transcripts, and other information" you'd likely want to reference later.

**Current limitation:** The system is designed around junction-based linking of *folders* containing configs. You're asking whether to expand this to track individual files (docs, transcripts, plans) or create a different tracking mechanism for informational content.

## 4. Refine Exclusions
**Problem:** `C:\Users\YC\GitHubRepo` is being monitored but shouldn't be (it's being categorized as `Projects_GitHubRepo`).

**Current state:** It's explicitly included in the monitor paths at `WatchHub_Realtime.ps1:74-78`.

## 5. Organizational Decision
**Question:** Should the refactored scripts move out of `src_refactor` to the main folder?

**Current state:** There's a `src/` folder (original) and `src_refactor/` folder (new versions). The refactored versions have the "Brain" (`AIToolsConfig.ps1`) vs "Hands" (`SyncSkills.ps1`) separation.

## 6. Quiet Mode Toggle
**Question:** Should the main menu have a "Quiet Mode" toggle to reduce console output?

---

**Is this correct? Any clarifications before I draft the implementation plan?**

---

## User

what does this workflow do?

---

## Assistant (Plan · kimi-k2.5-free · 27.4s)

 ## AI HubWatch Workflow Overview

This is a **real-time monitoring system** that automatically tracks AI tool installations and synchronizes skills across all your AI agents.

### The Three-Layer Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 1: Auto-Start                                         │
│  Task Scheduler → Launches on login, hidden, auto-restarts  │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│  Layer 2: Error Handler                                      │
│  WatchHub_Wrapper.ps1 → 5x retry logic, popups on errors    │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│  Layer 3: Core Monitor                                       │
│  WatchHub_Realtime.ps1 → 7 FileSystemWatchers               │
└─────────────────────────────────────────────────────────────┘
```

### What It Actually Does

**1. Watches 7 Locations Simultaneously:**
- User home dotfiles (`C:\Users\YC\.claude`, `.cursor`, etc.)
- AppData Roaming & Local
- Local\Programs
- GitHubRepo folder
- Root dotfiles on C:\

**2. When a New AI Tool is Installed:**
```
New folder "perplexity" created in AppData
         ↓
FileSystemWatcher detects it
         ↓
Matches AI keyword list? → YES
         ↓
Checks for config files to validate it's real
         ↓
Creates junction: AI_hub\perplexity_AppData_Local → original folder
         ↓
Logs to _Change_log\perplexity_AppData_Local_add.txt
         ↓
Updates Obsidian inventory
```

**3. When a Skill is Added to Claude:**
```
npx skills add my-skill → creates folder in .claude\skills\
         ↓
Skills FileSystemWatcher detects it
         ↓
Calls SyncSkills.ps1
         ↓
Creates symlinks from Claude\skills\my-skill to ALL other agents
         ↓
Now all your AI tools have the same skill
```

**4. Key Design Decisions:**
- **Junctions** (`/J`) for AI tool directories (link whole folders)
- **Symlinks** (`/D`) for skills (link individual skill folders)
- **Mutex locking** prevents concurrent operations from conflicting
- **Debouncing** (2s window) prevents duplicate events
- **Single source of truth**: `AIToolsConfig.ps1` defines all AI tool keywords, config files, categories

### The Problem You're Solving

You're essentially creating a **unified hub** where all your AI tool configurations live, so you can:
1. See all AI tools in one place (`AI_hub\`)
2. Install a skill once, use it everywhere
3. Track what changed when you install new tools
4. Export inventory to Obsidian for documentation

**Does this match your understanding? What aspects need clarification before we plan the fixes?**

---

## User

yes 90% its good enough. so the refactor planning sessions notes is just what i saw during testing walkthrough. i dont think the detection logic is reliable the to cover all future downloads. what do you think? maybe we shouldnt rely on scripts?

---

## Assistant (Plan · kimi-k2.5-free · 23.3s)

  You're raising a critical architectural question. The keyword + config-file validation approach is indeed brittle—every new AI tool requires manual updates to `AIToolsConfig.ps1`.

**The Core Problem:** Detection by *naming* is inherently fragile. Perplexity wasn't detected because "perplexity" wasn't in the keywords list. Tomorrow's AI tool won't be detected either.

**Alternative Approaches:**

**Option 1: Pattern-Based Heuristics** (Smarter detection)
- Instead of tool names, detect *behavior patterns*:
  - Folders containing `models/`, `config/`, `.env` files
  - Presence of model files (`.gguf`, `.onnx`, `.pt`, `.safetensors`)
  - Executable patterns (`*-server.exe`, `*-agent.exe`)
- **Pros:** Adapts to new tools automatically
- **Cons:** More false positives, complex to implement

**Option 2: Registry + Process Monitoring** (Installation-aware)
- Hook into Windows software installation events
- Monitor process creation for AI-related binaries
- **Pros:** Catches actual installs reliably
- **Cons:** Misses portable/zip tools, requires deeper system integration

**Option 3: Hybrid Manual/Auto** (Pragmatic)
- Keep auto-detection for *known* tools (cursor, claude, etc.)
- Add "Watch this folder" manual mode for unknown tools
- CLI command: `.\Hub.ps1 watch-folder "C:\Users\YC\Perplexity"`
- **Pros:** Reliable, explicit, user-controlled
- **Cons:** Less "magic," requires user action

**Option 4: Simplify Scope** (Radical)
- Stop trying to auto-detect *everything*
- Focus only on high-value locations: `~/.claude`, `~/.cursor`, etc.
- Everything else = manual junction creation
- **Pros:** Simple, predictable, zero false positives
- **Cons:** Loses the "discover new tools" feature

**My Recommendation:** **Option 3 (Hybrid)** + simplify the keywords list to *only* well-known, stable tools (claude, cursor, ollama, etc.). Don't try to catch everything—make manual linking easy and discoverable.

**Your thoughts:**
- Do you want to keep the "auto-discovery" feature at all?
- Is the tradeoff (brittle detection vs. manual work) worth it?
- Should we pivot to a different platform (Python, Go) or stick with PowerShell?

---

## User

i dont want to miss any one of them. can we somehow add ai agent in?

---

## Assistant (Plan · kimi-k2.5-free · 81.6s)

 You're right to be concerned—keyword lists are inherently incomplete. Let me explore what "AI agent detection" could actually mean and present some robust options.

**Tool: task**

---

## Assistant (Plan · kimi-k2.5-free · 13.5s)

  Perfect research. Based on this, here's my recommendation for catching **100% of AI tools without brittle keyword lists:**

## The Solution: Heuristic + Interactive Detection

Instead of trying to name every tool, we detect by **what the tool IS** (model files, config patterns, folder structures) + **learn from you** when uncertain.

### Core Detection Engine

**Multi-Factor Scoring** (replaces keyword list):
```powershell
$aiScore = 0

# HIGH confidence indicators (+25-40 points)
Contains *.gguf, *.safetensors, *.onnx files    → LLM runtime
Contains "skills/" folder with .json files      → Agent with capabilities
Contains models/ folder with >100MB files       → Local LLM

# MEDIUM confidence (+10-20 points)
settings.json with "mcpServers", "apiKey"       → API-based tool
.env with OPENAI_, ANTHROPIC_, OLLAMA_          → AI service client
Subfolders: prompts/, embeddings/, checkpoints/  → AI workflow

# LOW confidence (+5-10 points)
*.exe with "ai", "llm", "agent" in name         → Possible AI tool
```

### The "AI Agent" Pattern Specifically

You asked about detecting "AI agents" - these have unique fingerprints:
```powershell
# Agent-specific patterns
"autonomous": true in config                   → Autonomous agent
Contains "tools/" or "capabilities/" folder    → Tool-using agent
Has planning/execution loops in code            → Agent framework
Multi-step workflow configs                     → Agent behavior
```

### Interactive Learning Loop

**The key innovation:** When score is 30-70 (uncertain), **ask you**:
```
[AI HubWatch] New tool detected: C:\Users\YC\Perplexity
           Confidence: 45% (has settings.json, web content patterns)
           
Is this an AI tool?
[Y] Yes - Always track tools like this
[N] No - Ignore this path
[S] Show me what's inside first
```

Your answers train the system:
- **"Yes"** → Add folder pattern to whitelist
- **"No"** → Add to blacklist
- **"Always track .json configs in AppData"** → Rule learning

### Package Manager Integration (Backup Layer)

Also watch:
- `winget list` every 60s (catches managed installs)
- `choco list` for chocolatey apps
- npm global packages with AI keywords

This catches tools **before** they create folders.

## Implementation Plan

**Phase 1: Heuristic Engine** (replaces keyword list)
- Scan new folders for model files, config patterns
- Score-based detection (>70 = auto-link, 30-70 = ask, <30 = ignore)

**Phase 2: Interactive Mode**
- Windows notifications for uncertain detections
- Store user preferences in `~\.aihubwatch\learned.json`

**Phase 3: Package Manager Hooks**
- Parse `winget list --json` periodically
- Pre-link known AI packages before they run

**Questions:**

1. **Interactive vs Silent?** Do you want popups asking "Is this an AI tool?" or should it log to a file for batch review?

2. **Auto-link threshold?** At what confidence should it auto-create junctions vs ask you? (I suggest 75%)

3. **Package managers?** Do you use winget, choco, scoop, or manual installs mostly?

4. **"AI Agent" priority?** Should we specifically detect "autonomous agent" patterns (planning loops, tool use, multi-step) differently from simple "AI chat tools"?

This approach means **you never update keyword lists again**—the system learns what you consider "AI tools" by your answers.

---

## User

just let agents call tools for websearch i dont think they would miss anything i they can google? this is what i think

---

## Assistant (Plan · kimi-k2.5-free · 8.3s)

  You're raising a fundamental architectural question: **Is proactive detection even necessary if agents can just search the web?**

## The Trade-Off

**Current Approach (Proactive Detection):**
- Pros: Instant junctions when tools install, automatic skill sync, unified hub view
- Cons: Complex detection logic, maintenance burden, false positives/negatives

**Your Alternative (Reactive/Web Search):**
- Pros: Simpler code, no detection logic to maintain, agents find info on-demand
- Cons: Requires agents to have web access, slower (search latency), no unified filesystem view

## Questions to Clarify Your Vision:

1. **The Hub Purpose**: Is the `AI_hub` folder meant to be:
   - A **convenience** (easy access to all configs in one place)?
   - A **requirement** (agents MUST use it to find tools)?
   - A **documentation** source (just for your reference)?

2. **Agent Autonomy**: If an agent encounters "Perplexity" and doesn't recognize it, should it:
   - Search web → "Perplexity is an AI search tool" → done?
   - Or need the junction in `AI_hub` to know it exists?

3. **Scope Reduction**: Are you saying:
   - Kill the auto-detection entirely?
   - Keep manual junction creation only?
   - Or reduce to a minimal "known tools" list (claude/cursor/ollama only)?

4. **What Problem Are We Solving?**
   - Finding configs quickly? → Manual links work
   - Syncing skills? → That still needs the junction structure
   - Discovering new tools? → Web search handles this
   - Documentation? → Could be simplified

**My take**: If agents have reliable web access, detection becomes **nice-to-have, not need-to-have**. The core value might just be the **skill sync** (symlinks), not the discovery.

**What's your instinct here?**
- Simplify to manual-only?
- Keep minimal auto-detection for major tools?
- Or something else?

---

## User

1. basically there wouldnt be new folders for what i have installed. there is no point to tract them for new folders. 2. new downloads still passe through keyword check first, if no keywords then pass to agent? 

---

## Assistant (Plan · kimi-k2.5-free)

---

## User

why detection becomes nice to have? we are not droping it. tell me the reason why you are honing on these issues? if AI hub serves no purpose anymore then we dont use it?? we are in plan mode. it is kinda strange. you dont sound like you are asking these question for my vision, you are thinking at operational level?

---

## Assistant (Plan · kimi-k2.5-free · 14.4s)

  You're absolutely right - I was overthinking operational details instead of planning your vision. Let me refocus.

## Your Vision (Corrected Understanding)

**The Core Workflow:**
```
New folder detected → Keyword check → Match? → Auto-link (existing)
                              ↓ No match
                    Pass to agent/web search → "Is this an AI tool?"
                              ↓ Yes
                         Create junction + log
                              ↓ No
                         Skip silently
```

**Key Points:**
1. **Existing tools covered** - You already have junctions for your 50+ agents
2. **Future detection enhanced** - Unknown tools get verified via web search, not just skipped
3. **AI Hub stays** - It's the central hub for skill sync, not going anywhere
4. **Detection improved** - Two-tier: fast keyword match + agent verification for unknowns

## The Planning Questions I Should Ask:

1. **Web Search Integration**: Should WatchHub call an external AI service (Claude API, etc.) or should it spawn a subprocess that does the search?

2. **Rate Limiting**: If 10 folders appear simultaneously, do we batch them for web search or queue them?

3. **Offline Mode**: What happens when there's no internet? Skip unknowns or cache them for later?

4. **Verification Prompt**: Should WatchHub wait for agent confirmation (blocking) or queue it (async)?

5. **Learning**: Once agent identifies "Perplexity" as AI tool, add it to local keyword cache so next time it's instant?

**Does this capture what you want? What details am I missing for the implementation plan?**

---

