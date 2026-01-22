---
date: 2025-12-25 22:45
type: experiment
project: ollama-models
status: active
tags:
  - ollama
  - cleanup
  - pkpm-setup
  - llm/models
---
# **Objective**: Reset models to phi3-local + minimal. Document for future automation.

## **Pre-Cleanup**: 
### Step 1  - make a list first , and then commend "Nuke all except phi3-local (your custom)" (why)

 **Why Kept phi3-local**:
 - Custom (Modelfile path: C:\Users\YC\Modelfile).
 - No hallucinations.
 - PKM-optimized.
---
## Objective
Reset models to a clean baseline (keep `phi3-local`) and document the process so it’s repeatable later.

---
## Pre-cleanup context

### Why keep `phi3-local`?
- Custom build (Modelfile path: `C:\Users\YC\Modelfile`)
- More reliable “I don’t know” behavior (lower hallucination risk)
- PKM-optimized (your preferred default)

### Reminder about logging
- Put **commands** in `powershell` code blocks.
- Put **terminal output** in `text` code blocks.
- Avoid pasting terminal output inside blockquotes (`> ...`) because it gets messy fast.

---
## Step 1 — Inventory (before cleanup)
### Command
```
### Output (before cleanup)

NAME                          ID              SIZE      MODIFIED
mistral:latest                6577803aa9a0    4.4 GB    16 minutes ago
mistral:7b-instruct           6577803aa9a0    4.4 GB    49 minutes ago
phi4-mini-reasoning:latest    3ca8c2865ce9    3.2 GB    2 hours ago
phi3-local:latest             d7299113caf4    2.2 GB    2 hours ago
phi3:mini                     4f2222927938    2.2 GB    2 hours ago
phi3:mini-128k                4f2222927938    2.2 GB    2 hours ago
phi3:latest                   4f2222927938    2.2 GB    3 hours ago
llama3:8b                     365c0bd3c000    4.7 GB    4 hours ago
llava-llama3:latest           44c161b1f465    5.5 GB    10 hours ago
```
### Notes
- `phi3:mini`, `phi3:mini-128k`, and `phi3:latest` share the same ID (`4f2222927938`) → effectively duplicate tags pointing to the same underlying model.
---
## Step 2 — Cleanup execution (remove everything except `phi3-local`)
### Command
```

ollama rm mistral mistral:7b-instruct phi4-mini-reasoning phi3:mini phi3:mini-128k phi3:latest llama3:8b llava-llama3

```
### Output
```

deleted 'mistral'
deleted 'mistral:7b-instruct'
deleted 'phi4-mini-reasoning'
deleted 'phi3:mini'
deleted 'phi3:mini-128k'
deleted 'phi3:latest'
deleted 'llama3:8b'
deleted 'llava-llama3'

```
### Verify
```

ollama list

```

```

NAME                 ID              SIZE      MODIFIED
phi3-local:latest    d7299113caf4    2.2 GB    3 hours ago

```
### Summary (after cleanup)
- Success: All stock models removed.
- Kept: `phi3-local:latest`
- Disk: Freed ~20 GB (approx.)
---
## Step 3 — Re-pull models (experiment mode: keep multiple)

### Re-pull plan:
Keep a small “learning set” for comparison:
- `mistral:latest` (planning / drafting)
- `llama3:8b` (code-ish help)
- `phi4-mini-reasoning:latest` (step-by-step reasoning tests)
- `llava-llama3:latest` (image / screenshot tests)
- One phi3 “daily driver” (choose either `phi3:mini` OR `phi3:mini-128k`)
### Post re-pull inventory (current state)
```
ollama list
```

```
NAME                          ID              SIZE      MODIFIED
phi3:mini-128k                4f2222927938    2.2 GB    11 minutes ago
llava-llama3:latest           44c161b1f465    5.5 GB    11 minutes ago
llama3:8b                     365c0bd3c000    4.7 GB    18 minutes ago
phi4-mini-reasoning:latest    3ca8c2865ce9    3.2 GB    21 minutes ago
mistral:latest                6577803aa9a0    4.4 GB    31 minutes ago
phi3-local:latest             d7299113caf4    2.2 GB    4 hours ago
```

### Small incident log (typo)
```
Typed: allama list
Result: 'allama' is not recognized...
Fix: use 'ollama list'
```

### Note: why `phi3:mini` was removed
```
ollama rm phi3:mini
```

```
deleted 'phi3:mini'   
```

Reason: it was redundant with `phi3:mini-128k` (same model ID previously), and keeping one tag with more context windex reduces confusion. [[The Model to Run for Local LLM 1]]

---

## Next steps (testing + documentation)

### 1) Create a “model inventory” note
- File: `2-Knowledge/Tools/Ollama/model-inventory.md`
- Paste the latest `ollama list` output
- Add 1-line “best use” per model
### 2) Run 1 standard PKM test prompt on each model
Pick one prompt and reuse it across models:
- “Turn this messy log into a clean checklist + next steps.”
- “Create an Obsidian template for an experiment log.”
- “Write a Dataview query for notes created today.”
### 3) Save outputs (raw)
For each model:
- Prompt used
- Full response
- 2 bullets: “good” / “bad”

---

## Quick test (optional)
```

ollama run phi3-local "Confirm: You are my safe PKM assistant."

```

ollama run phi4-mini-reasoning "Make a 5-bullet recap of what I learned tonight setting up Ollama + Obsidian logging."v

```
ollama run phi3-local "In this chat, PKM means Personal Knowledge Management in Obsidian. Compare Mistral vs my local model named phi3-local for: summarizing notes, creating templates, tagging, and weekly review checklists. If you are unsure, ask 1 clarification question."
```

