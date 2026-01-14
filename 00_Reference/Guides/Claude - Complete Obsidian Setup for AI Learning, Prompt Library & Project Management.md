# Complete Obsidian Setup for AI Learning, Prompt Library & Project Management

This is an exhaustive, actionable workflow to build your personal AI knowledge system.

---

## Phase 1: Initial Obsidian Setup

### 1.1 Install & Configure Base System

**Step 1:** Download Obsidian from obsidian.md and install it.

**Step 2:** Create a new vault named something like `AI-Brain` or `AI-PKM` in a cloud-synced folder (Dropbox, OneDrive, or Google Drive) for backup.

**Step 3:** Enable these core Community Plugins (Settings → Community Plugins → Browse):

|Plugin|Purpose|
|---|---|
|**Templater**|Create prompt templates, note templates|
|**Dataview**|Query and display your prompts/notes dynamically|
|**QuickAdd**|Rapid capture of prompts, ideas, iterations|
|**Kanban**|Track project progress (your GPT projects)|
|**Excalidraw**|Visual diagrams for system specs|
|**Omnisearch**|Better search across vault|
|**Tag Wrangler**|Manage tags efficiently|

**Step 4:** Set hotkeys (Settings → Hotkeys):

- `Ctrl+N` → New note
- `Ctrl+Shift+P` → QuickAdd menu (for fast prompt capture)
- `Ctrl+O` → Quick switcher

---

## Phase 2: Folder Structure

Create this exact structure:

```gcode
📁 AI-Brain/
├── 📁 00-Inbox/                    # Quick capture, unsorted
├── 📁 01-Projects/
│   ├── 📁 System-Spec-Generator/
│   ├── 📁 Grammar-Checker/
│   └── 📁 Custom-GPT-Projects/
├── 📁 02-Prompt-Library/
│   ├── 📁 System-Prompts/
│   ├── 📁 Task-Prompts/
│   ├── 📁 Chain-Prompts/
│   └── 📁 Templates/
├── 📁 03-AI-Concepts/
│   ├── 📁 LLM-Fundamentals/
│   ├── 📁 Prompt-Engineering/
│   └── 📁 Tools-APIs/
├── 📁 04-Iterations/               # Version history of prompts
├── 📁 05-Reviews/                  # AI output analysis
├── 📁 06-Resources/
│   └── 📁 Clipped-Articles/
└── 📁 Templates/                   # Note templates
```

---

## Phase 3: Note Templates (Create in `/Templates/`)

### 3.1 Prompt Template

Create file: `Templates/T-Prompt.md`

markdown

```markdown
---
type: prompt
category: {{category}}
model: {{model}}
version: 1.0
status: draft/testing/production
created: {{date}}
tags: [prompt, {{tags}}]
---

## Purpose
{{What does this prompt do?}}

## System Prompt
```

{{system prompt here}}

```clean

## User Prompt Template
```

{{user prompt here}}

handlebars

```handlebars

## Variables
- `{{variable1}}`: description
- `{{variable2}}`: description

## Example Input
{{example}}

## Example Output
{{example output}}

## Iteration Notes
- v1.0: Initial version

## Related
- [[related prompt]]
```

---

### 3.2 Iteration Log Template

Create file: `Templates/T-Iteration.md`

markdown

```markdown
---
type: iteration
parent-prompt: [[{{prompt name}}]]
version: {{version}}
date: {{date}}
tags: [iteration]
---

## Change Made
{{What did you change?}}

## Reason for Change
{{Why?}}

## Before
```

{{old prompt section}}

```clean

## After
```

{{new prompt section}}

gherkin

```gherkin

## Test Results
| Input | Expected | Actual | Pass/Fail |
|-------|----------|--------|-----------|
| | | | |

## Observations
{{What did you learn?}}

## Next Steps
- [ ] {{next action}}
```

---

### 3.3 AI Output Review Template

Create file: `Templates/T-Review.md`

markdown

```markdown
---
type: review
prompt-used: [[{{prompt}}]]
model: {{model}}
date: {{date}}
rating: /5
tags: [review]
---

## Task Given
{{what you asked}}

## Output Received
{{paste AI output or summary}}

## Evaluation Criteria

### Accuracy (1-5): 
- Factual errors: 
- Hallucinations: 

### Completeness (1-5):
- Missing elements:
- Extra/unnecessary:

### Format/Style (1-5):
- Followed instructions:
- Tone appropriate:

### Usefulness (1-5):
- Directly usable:
- Needs editing:

## What Worked Well
- 

## What Failed
- 

## Prompt Improvements Needed
- [ ] {{improvement}}

## Patterns Noticed
{{recurring issues or strengths}}
```

---

### 3.4 Project Note Template

Create file: `Templates/T-Project.md`

markdown

```markdown
---
type: project
status: active/paused/complete
started: {{date}}
tags: [project]
---

## Objective
{{What are you building?}}

## Success Criteria
- [ ] {{criterion 1}}
- [ ] {{criterion 2}}

## Components
- [[Component 1]]
- [[Component 2]]

## Prompts Used
- [[prompt 1]]
- [[prompt 2]]

## Progress Log
### {{date}}
- {{update}}

## Blockers
- 

## Resources
- [[resource]]
```

---

## Phase 4: What to Capture (Be Exhaustive)

### 4.1 During Prompt Iteration, Capture:

|What|Why|How|
|---|---|---|
|**Every version of the prompt**|Track what works|Use iteration template|
|**The exact input you tested**|Reproduce results|Copy-paste in note|
|**Full AI output**|Analyze patterns|Screenshot or paste|
|**What went wrong**|Avoid repeating mistakes|Bullet points|
|**What worked unexpectedly**|Discover techniques|Tag with `#insight`|
|**Time taken**|Measure efficiency|Note timestamp|
|**Model used + settings**|Temperature, etc. matters|Metadata field|
|**Edge cases tested**|Know prompt limits|Create test table|

### 4.2 For Your Specific Projects, Capture:

**System Spec Generator:**

- Input examples (different project types)
- Output format requirements
- Edge cases (vague inputs, complex systems)
- Validation rules you discover

**Grammar Checker:**

- Types of errors it catches/misses
- False positives (correct text marked wrong)
- Style preferences (formal vs casual)
- Language-specific issues

**Custom GPT Projects:**

- Persona definitions that work
- Instruction patterns that get followed
- Guardrails that work/fail
- User feedback

---

## Phase 5: Quick Access System (PowerToys vs Espanso)

### 5.1 PowerToys (Recommended for Windows)

**Setup PowerToys Run:**

1. Install PowerToys from Microsoft Store
2. Enable "PowerToys Run" (Alt+Space by default)
3. Install the **"Everything"** plugin for instant file search

**For Obsidian integration:**

- Use `Alt+Space` → type note name → opens directly
- Limitation: Can search files but won't search inside note content

### 5.2 Espanso (Better for Text Expansion)

**When to use Espanso:**

- You want to type `:systemprompt` and have it expand to your full prompt
- You need snippets available OUTSIDE Obsidian (in ChatGPT, API playgrounds)

**Setup:**

yaml

```yaml
# In espanso config (default.yml)
matches:
  - trigger: ":grammarcheck"
    replace: "You are a grammar expert. Review the following text..."
    
  - trigger: ":specgen"
    replace: "Generate a system specification for: "
```

### 5.3 Recommended Hybrid Setup

|Tool|Use For|
|---|---|
|**Obsidian QuickAdd**|Fast capture INTO vault|
|**PowerToys Run**|Fast search/open files|
|**Espanso**|Paste prompts OUTSIDE Obsidian|
|**Obsidian Omnisearch**|Deep search inside vault|

**Workflow:**

1. Store master prompts in Obsidian
2. Export working prompts to Espanso for quick typing
3. Use PowerToys to jump to any note instantly

---

## Phase 6: How to Get Prompts (Sources)

### 6.1 Prompt Sources

|Source|URL|What to Get|
|---|---|---|
|**Awesome ChatGPT Prompts**|github.com/f/awesome-chatgpt-prompts|Starter templates|
|**FlowGPT**|flowgpt.com|Community prompts|
|**PromptBase**|promptbase.com|Paid professional prompts|
|**r/PromptEngineering**|reddit.com/r/PromptEngineering|Discussions, techniques|
|**Anthropic Cookbook**|github.com/anthropics/anthropic-cookbook|Best practices|
|**OpenAI Cookbook**|github.com/openai/openai-cookbook|Patterns|
|**Learn Prompting**|learnprompting.org|Structured learning|

### 6.2 When You Find a Prompt

**Capture Workflow:**

1. `Ctrl+Shift+P` → QuickAdd → "New Prompt"
2. Paste prompt into template
3. Add source link
4. Tag: `#imported` `#untested`
5. Schedule testing

---

## Phase 7: Daily/Weekly Workflows

### 7.1 Daily Workflow (15 min)

vhdl

```vhdl
Morning (5 min):
1. Check 00-Inbox → Process or file notes
2. Review today's project priorities

During Work:
3. Use QuickAdd to capture every prompt iteration
4. Tag outputs: #worked #failed #partial

End of Day (10 min):
5. File inbox items
6. Update project progress note
7. Note 1 key learning in daily note
```

### 7.2 Weekly Review Workflow (30 min)

sql_more

```sql_more
1. Review all #failed tags → What patterns?
2. Review all #worked tags → What made them work?
3. Promote tested prompts: #draft → #production
4. Update Espanso with new production prompts
5. Archive old iterations (move to 04-Iterations)
6. Update project Kanban boards
7. Identify 1 skill gap → add to learning queue
```

---

## Phase 8: Dataview Queries (Put in Dashboard Note)

Create `Dashboard.md` in root:

markdown

````markdown
# 🧠 AI Brain Dashboard

## 📥 Inbox (Process These)
```dataview
TABLE file.ctime as "Added"
FROM "00-Inbox"
SORT file.ctime DESC
````

## 🔥 Production Prompts

dataview

```text
TABLE category, model, version
FROM "02-Prompt-Library"
WHERE status = "production"
SORT file.mtime DESC
```

## 🧪 Prompts Needing Testing

dataview

```text
LIST
FROM #untested
```

## 📊 Recent Iterations

dataview

```text
TABLE parent-prompt, version, date
FROM "04-Iterations"
SORT date DESC
LIMIT 10
```

## ❌ Failed Attempts (Learn From These)

dataview

```text
LIST
FROM #failed
SORT file.mtime DESC
LIMIT 5
```

yaml

````yaml

---

## Phase 9: Review AI Work Systematically

### 9.1 Evaluation Checklist (Use Every Time)

```markdown
□ Did it follow the format I specified?
□ Did it include all required sections?
□ Are there factual errors I can verify?
□ Did it make up information (hallucination)?
□ Is the tone/style what I wanted?
□ Would I use this output as-is?
□ What's the ONE thing to improve in the prompt?
````

### 9.2 Create Rubrics for Repeated Tasks

For **System Spec Generator**, create a note with:

markdown

```markdown
# System Spec Rubric

| Criterion | Weight | 1 (Poor) | 3 (OK) | 5 (Excellent) |
|-----------|--------|----------|--------|---------------|
| Completeness | 25% | Missing sections | Most present | All sections |
| Clarity | 25% | Vague | Understandable | Crystal clear |
| Technical accuracy | 25% | Errors | Minor issues | Accurate |
| Format | 25% | Messy | Readable | Perfect |
```

---

## Phase 10: Additional Notes to Keep

### 10.1 Meta-Learning Notes

- **Model comparison notes:** "Claude vs GPT for grammar = ..."
- **Token/cost tracking:** What prompts cost more?
- **Failure patterns:** "When I say X, it always does Y wrong"
- **Workarounds discovered:** "Adding 'step by step' fixes..."

### 10.2 Reference Notes

- API documentation snippets
- Pricing/limits for different models
- Your custom GPT configuration backups
- Prompt engineering principles (summarized)

### 10.3 Decision Logs

- Why you chose certain approaches
- Trade-offs you made
- Things you tried and abandoned (and why)

---

## Quick Start Checklist

markdown

```markdown
□ Install Obsidian + enable plugins
□ Create folder structure
□ Copy templates to Templates folder
□ Set up QuickAdd for fast capture
□ Install PowerToys, configure Run
□ Create Dashboard.md with Dataview
□ Bookmark 3 prompt sources
□ Create first project note (System Spec Generator)
□ Capture first 5 prompts
□ Do first weekly review after 7 days
```

---

This system scales from a few prompts to hundreds. Start simple, add complexity as needed. The key is **consistent capture** - every iteration, every failure, every insight gets logged.