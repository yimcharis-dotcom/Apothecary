
---

#workflow-management #system-infrastructure   #setup 
##  **Folder Structure & Definitions** v2026-01-04
``` markdown
Vault Root/
├── `__Templates/`              `[Plugin Dependency - Templates]`
├── `__obsidian-scripts/`     `[Plugin Dependency - Automation]`
├── `00_Reference/`            `[External Knowledge - Read-Only Source]`
├── `00_System/`                 `[Infrastructure - Read-Only Deploy Target]`
├── `10_Prompt_library/`    `[Finalized Tools - Production Ready]`
├── `30_Projects/00_______``[Active Iteration - Fluid Workspace]`
├── `40_Experiments/`        `[Early Development - Testing Ground]`
├── `90_Inbox/`
└── `99_Archive/`
```
|Folder|Purpose|Edit Policy|Lifespan of Contents|
|---|---|---|---|
|`__Templates/`|Files that Templater/Templates plugin reads to create new notes|Edit in place when template itself needs updating|Permanent (until template deprecated)|
|`__obsidian-scripts/`|`.js`, `.py`, automation scripts that plugins execute|Edit in place (use version control)|Permanent (versioned)|
|`00_System/`|**Infrastructure only:** Prompts pasted into plugin settings, Space instructions, vault governance rules|**NEVER edit directly** - Copy to Projects, revise, redeploy|Permanent (with archive)|
|`10_Prompt_library/`|Tested, documented, production-ready prompts for daily work|Edit via Projects workflow|Permanent (with deprecation)|
| `30_Projects/` /`00______`|Active refinement workspace - **always in motion**|Edit freely - temporary staging|0-14 days (then promote or archive)|
|`40_Experiments/`|Early-stage testing, wild ideas, multi-iteration development|Edit freely - messy lab|0-60 days (then promote or archive)|
| `Reference/` |Downloaded guides, PDFs, external documentation|Read-only (annotate via linked notes)|Permanent|

## 🔄 **The Four-Stage Pipeline**

## Stage 1: EXPERIMENT (40_Experiments/)

**When to use:**

- New prompt idea that needs multiple iterations
    
- Learning a new technique (e.g., few-shot prompting)
    
- Testing whether an approach even works
    
- Capturing AI interactions for analysis
  
- **Promotion Trigger:**  
When all checkboxes in `promotion-criteria` are checked → Move to Stage 2.  
  
**Structure:**
```
40_Experiments/
├── Grammar_Checker/
│   ├── index.md                    [Project metadata + status]
│   ├── test_cases.md               [Input/output pairs]
│   ├── iteration_log.md            [What changed, why, results]
│   ├── v1_simple.md                [First attempt]
│   ├── v2_with_examples.md         [Improvement]
│   └── prompts/                    [Versions being tested]
├── Annual_Report_Typeset_Checker/
└── HKICPA_Download_Automation/
```
[[index.md Template]]

## Stage 2: ITERATE (30_Projects/)

**When to use:**

- Experiment passed basic tests, now needs final polish
    
- Updating an existing deployed prompt (copied from System)
    
- Preparing for production deployment
    
**Structure:**

```
30_Projects/
├── Grammar_Checker_v2/          [Temporary - delete after promotion]
│   ├── prompt.md                [Working draft]
│   ├── test_results.md          [Final validation]
│   └── deployment_checklist.md  [Pre-flight checks]
└── [Usually empty or 1-3 active projects max]

```
**Key Principle:** This is a **hot workspace**, not storage. Files should flow through in <14 days.

**Workflow:**

1. **Import:** Copy from `40_Experiments/[Project]/prompts/vX.md` OR copy from `00_System/` (if updating deployed)
    
2. **Refine:** Make final adjustments, run comprehensive tests
    
3. **Validate:** Check against deployment checklist
    
4. **Export:** Promote to `10_Prompt_library/` (and `00_System/` if infrastructure)
    
5. **Cleanup:** Delete project folder from `30_Projects/`
    

[[Deployment Checklist Template]]


## Stage 3: LIBRARY (10_Prompt_library/)

**When to use:**

- Prompt has passed all tests and is ready for daily use
    
- Canonical "source of truth" for production prompts
    

**Structure:**

```
10_Prompt_library/
├── _Index.md                      [Master list + Dataview dashboard]
├── Accounting/
│   ├── IFRS_Explainer.md
│   └── Audit_Checklist_Generator.md
├── AI_Development/
│   ├── Code_Reviewer.md
│   └── System_Spec_Generator.md
├── Grammar/
│   ├── Grammar_Checker_v3.md
│   └── Tone_Adjuster.md
├── System_Infrastructure/         [For prompts used in both Library & System]
│   └── Summarize_Text.md
└── _Deprecated/
    └── Old_Grammar_v1.md

```

[[Standard Prompt File Template]]

## Stage 4: SYSTEM (00_System/)

**When to use:**

- Prompt is pasted into plugin settings (Copilot, Templater, etc.)
    
- Instruction text for this AI Space
    
- Vault governance rules (Style Guide, Naming Conventions)
    

**Structure:**

```
00_System/
├── _Index.md                           [System overview + last update log]
├── Specs/
│   ├── Space_Instruction_PKM.md        [Deployed in this Space]
│   ├── Space_Instruction_Coding.md     [For coding assistant Space]
│   └── Vault_Style_Guide.md            [Grammar/formatting rules]
├── Plugin_Configs/
│   ├── Copilot_System_Prompt.md        [Pasted in Copilot settings]
│   ├── Templater_Scripts_Ref.md        [Documentation of scripts]
│   └── QuickAdd_Captures.md            [Capture workflow configs]
├── Prompts/                             [Infrastructure prompts]
│   └── Summarize_Text.md               [Deployed copy - links to Library]
├── Governance/
│   ├── Naming_Conventions.md
│   ├── Tagging_Rules.md
│   └── Response_Contract.md
└── _Archive/
    └── 2025-12/
        └── Space_Instruction_v1.md
```

[[System File Template (Deployed Copy)]]


## 🔗 **Linking Strategy for Dual-Use Prompts**

**The Solution:** Canonical version in Library, linked copy in System.

## Implementation

[[In Library (Canonical)]]
[[In System (Deployed Copy)]]

## 📂 **Other Critical Folders**

## Reference/

**Purpose:** External knowledge you consume but don't create.

**Structure:**
```
Reference/
├── Guides/
│   ├── Obsidian_Setup/
│   │   └── Perplexed_Plugin_Setup_Guide.md
│   ├── Prompt_Engineering/
│   └── PKM_Methods/
├── Standards/
│   ├── IFRS_17_Summary.pdf
│   └── GAAP_Updates_2025.pdf
├── Tools/
│   └── Espanso_Cheatsheet.md
└── _Extracted/                     [Temporary - prompts pulled from guides]
    └── Guide_Prompt_Samples/

```

**Rule:** If you extract a prompt/template from a guide:

1. Save extracted piece in `Reference/_Extracted/[Source]/`
    
2. Copy to `40_Experiments/` to test
    
3. After extraction, original guide can stay in `Reference/` or be deleted
## __Templates/

**Purpose:** Files that Templater/Templates plugin inserts into new notes.

**Structure:**

```
__Templates/
├── daily-note.md
├── project-start.md
├── prompt-library-entry.md
├── experiment-index.md
├── review-template.md
└── _scripts/                       [Templater .js scripts]
    ├── daily-note-auto.js
    └── project-generator.js
```

**Update Policy:** Edit in place (these are tools, not content).

**Link to System:** Add documentation in `00_System/Plugin_Configs/Templater_Templates_Ref.md`.