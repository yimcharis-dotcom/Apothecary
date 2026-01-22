#pplx #guide
# Personal Wiki + AI Workflow: Comprehensive Step-by-Step Guide

[[_Originals/Guides/PPLX - personal-wiki-ai-workflow]]
## Table of Contents
1. [Vault Architecture (Folder Structure)](#vault-architecture)
2. [Note Template System](#note-templates)
3. [Workflow: Iterative Prompt Development](#workflow-iterative)
4. [How to Capture & Review AI Work](#capture-review)
5. [Organization & Tagging](#organization)
6. [Quick Retrieval & Reuse (Espanso vs PowerToys)](#quick-retrieval)
7. [Personal Wiki Index & Discovery](#wiki-index)
8. [End-to-End Example: Grammar Checker Project](#example-grammar-checker)

---

## 1. Vault Architecture (Folder Structure)

**Create this folder structure in Obsidian:**

```
your-vault/
├── 00-system/                    # System-wide configs, MOC (Maps of Content)
│   ├── Home.md                   # Central dashboard
│   ├── Vault-Changelog.md        # Track changes to vault structure
│   └── Naming-Conventions.md     # Rules for file naming, tagging
│
├── 10-prompts/                   # All reusable prompts organized by type
│   ├── 10-prompts-ai-learn/      # Learning AI: tutorials, concept explanations
│   │   ├── Explain-Concept.md
│   │   └── Compare-Methods.md
│   ├── 10-prompts-system-specs/  # System spec generators
│   │   ├── Spec-Template-Generator.md
│   │   └── API-Schema-Builder.md
│   ├── 10-prompts-grammar/       # Grammar/naturalness checking
│   │   ├── Grammar-Checker-Main.md
│   │   └── Grammar-Checker-Reference.md
│   ├── 10-prompts-writing/       # Writing assistance
│   │   ├── Email-Tone-Adjuster.md
│   │   └── Technical-Writer.md
│   └── 10-prompts-reasoning/     # Problem-solving, reasoning
│       ├── Root-Cause-Analysis.md
│       └── Decompose-Problem.md
│
├── 20-research/                  # Research notes, papers, findings
│   ├── 20-research-ai/
│   │   ├── LLM-Architecture-Notes.md
│   │   ├── Prompt-Engineering-Techniques.md
│   │   └── Evaluation-Methods.md
│   └── 20-research-tools/
│       ├── Obsidian-Plugins-Comparison.md
│       └── Espanso-vs-PowerToys.md
│
├── 30-projects/                  # Active projects
│   ├── 30-proj-grammar-checker/
│   │   ├── Spec.md               # System specification
│   │   ├── Test-Cases.md         # Test inputs and expected outputs
│   │   ├── Iterations/
│   │   │   ├── v1-initial.md
│   │   │   ├── v2-tier-fix.md
│   │   │   └── v3-final.md
│   │   └── Results/
│   │       ├── GPT-Results.md
│   │       └── Claude-Results.md
│   ├── 30-proj-system-spec-gen/
│   │   ├── Spec.md
│   │   └── Iterations/
│   └── 30-proj-custom-gpt/
│       ├── Spec.md
│       └── Training-Data/
│
├── 40-experiments/               # Scratch work, half-done tests
│   ├── 40-exp-prompt-variants.md
│   ├── 40-exp-eval-framework.md
│   └── 40-exp-notation-tests.md
│
├── 50-archive/                   # Deprecated, superseded versions
│   └── old-grammar-v1.md
│
├── Templates/                    # Obsidian template files (Templater plugin)
│   ├── Prompt-Template.md
│   ├── Project-Template.md
│   ├── Test-Case-Template.md
│   └── Iteration-Log-Template.md
│
└── Assets/                       # Images, diagrams, reference files
    └── workflow-diagram.png
```

**Rationale:**
- **00-system** = Vault governance, MOC (Map of Contents), entry points
- **10-prompts** = Immediately reusable, sortable by domain
- **20-research** = Knowledge you're building from (reference layer)
- **30-projects** = Active work with versioning and results
- **40-experiments** = WIP, no cleanup needed yet
- **50-archive** = Searchable but out of mind
- **Templates** = Standardized structure for new notes
- **Assets** = Media, external reference files

---
#templates 
## 2. Note Template System

Use **Templater** plugin to auto-generate these on creation.

### **Template 1: Prompt Note**
File: `Templates/Prompt-Template.md`

```markdown
---
type: prompt
domain: [ai-learn | system-spec | grammar | writing | reasoning]
purpose: [one-line description of what this prompt does]
model: [gpt-4 | claude-3.5 | both]
status: [draft | tested | production | archived]
version: 1.0
created: 2026-01-22
last-tested: 
tags: [tag1, tag2]
---

## Purpose
[Why does this prompt exist? What problem does it solve?]

## Constraints & Rules
- [Hard rule 1]
- [Hard rule 2]
- [Soft guideline 1]

## Prompt (Copy Below)
```
[ACTUAL PROMPT TEXT HERE]
```

## Example Input & Output
**Input:**
```
[Example input text]
```

**Output:**
```
[Expected output]
```

## Usage Notes
- Best for: [Context where this works well]
- Watch out for: [Common failure modes]
- Cost estimate: [API cost per use]

## Changelog
- **v1.0** (DATE): Initial version, tested on GPT-4
- **v1.1** (DATE): Added clarification to Constraints section

## See Also
- [[Related-Prompt]]
- [[Project-That-Uses-This]]
```

### **Template 2: Project Spec Note**
File: `Templates/Project-Template.md`

```markdown
---
type: project
name: [Project Name]
status: [ideation | in-progress | testing | shipped | paused]
priority: [high | medium | low]
created: 2026-01-22
deadline: 
owner: 
tags: [project, domain-tag]
---

## Goal
[What are you building? Why?]

## Core Requirements
1. [Requirement 1]
2. [Requirement 2]
3. [Requirement 3]

## Success Criteria
- [ ] [Measurable goal 1]
- [ ] [Measurable goal 2]
- [ ] [Measurable goal 3]

## System Prompts Used
- [[Prompt-Name-1]]
- [[Prompt-Name-2]]

## Test Cases
| Input | Expected Output | Status |
|-------|-----------------|--------|
| [Test 1 input] | [Test 1 expected] | ✅ Pass |
| [Test 2 input] | [Test 2 expected] | ❌ Fail |

## Iteration Log
- **v0.1** (DATE): Initial spec draft
- **v0.2** (DATE): Added test cases, identified issue #3
- **v1.0** (DATE): First passing version

## Known Issues & Next Steps
- [ ] Issue 1: [Description]
- [ ] Issue 2: [Description]

## Results
- See [[Grammar-Checker-Results]] for test outputs
- See [[Grammar-Checker-v2-Iteration]] for refinements

## Related Files
- [[Main-Prompt]]
- [[Test-Cases]]
- [[Results]]
```
#Iteratation 
### **Template 3: Iteration Log Note**
File: `Templates/Iteration-Log-Template.md`

```markdown
---
type: iteration-log
project: [[Project-Name]]
version: 1.1
date: 2026-01-22
status: [in-progress | complete | failed]
tags: [iteration, project-name]
---

## What Changed This Iteration?
- [Change 1: Context about what was wrong, how you fixed it]
- [Change 2: ...]

## What Was Tested?
- Test case: [Name]
- Model: [GPT-4 | Claude | Both]
- Result: [Pass/Fail] 
- [Explain the result]

## Key Findings
- **Success:** [What worked well]
- **Failure:** [What broke or didn't work]
- **Root Cause:** [Why did it fail? Hypothesis]

## Next Iteration Plan
- [What to try next]
- [How success will look]

## Relevant Outputs
- [[Link-to-GPT-Run-Output]]
- [[Link-to-Claude-Run-Output]]
```

---

## 3. Workflow: Iterative Prompt Development

### **Phase 1: Capture & Design (DAY 1)**

1. **Create a new Project note** using `Project-Template.md`
   - Fill in Goal, Requirements, Success Criteria
   - Save as `30-projects/30-proj-[name]/Spec.md`

2. **Create Prompt note(s)** using `Prompt-Template.md`
   - Save as `10-prompts-[domain]/[prompt-name].md`
   - Link from project spec

3. **Create Test Cases note**
   - Save as `30-projects/30-proj-[name]/Test-Cases.md`
   - List 3-5 simple test cases with expected output
   - Format: markdown table or bullet list

4. **Initial Run:** Paste prompt + first test case into GPT/Claude
   - Copy the FULL output (don't summarize)
   - Save raw output as `30-projects/30-proj-[name]/Results/GPT-v0.1-Raw.md`

**What to capture in notes:**
- Problem statement (1-2 sentences)
- Assumptions you made
- Success definition (measurable)
- Test cases (exact input, expected output)
- Links to related prompts/research

---

### **Phase 2: Review AI's Work (AFTER FIRST RUN)**

Create an "Evaluation Note" to systematically review output.

**Template:**
```markdown
---
type: evaluation
project: [[Project-Name]]
iteration: v0.1
model: GPT-4
date: 2026-01-22
---

## Output Quality Scorecard

| Criterion | Pass? | Evidence | Fix Priority |
|-----------|-------|----------|--------------|
| Format compliance | ❌ | Section numbers wrong | High |
| Completeness | ✅ | All 4 sections present | — |
| Accuracy | ⚠️ | 3 of 5 test cases correct | High |
| Clarity | ✅ | Explanations clear | — |

## Specific Failures
1. **Test Case 1:** Expected "X", got "Y" → Root cause: [Explain]
2. **Test Case 2:** ...

## Instruction Ambiguities Found
- [What did the model misunderstand?]
- [What was unclear in the prompt?]

## Proposed Fixes
- Change 1: [Exact text change and why]
- Change 2: ...

## Confidence in Fix
[Will this actually solve the problem? Why or why not?]

## Next Action
- Apply fixes to prompt
- Re-test on same test cases
```

**Review checklist (always use this):**
- ✅ Does output match format requirement?
- ✅ Does it pass all test cases?
- ✅ Are there false positives (things it shouldn't flag)?
- ✅ Are there false negatives (things it missed)?
- ✅ Is the explanation clear enough for a user?
- ✅ Did it misunderstand any part of the prompt?

---

### **Phase 3: Iterate (DAYS 2-N)**

1. **Apply ONE small fix** (not multiple at once)
   - Update Prompt note with new version
   - Increment version number (1.0 → 1.1)
   - Document what changed in Changelog

2. **Re-test on the SAME test cases**
   - Run the updated prompt on all previous test cases
   - Save output as `v0.2-Raw.md`

3. **Create Iteration Log note**
   - Link to both v0.1 and v0.2 outputs
   - Explain: Did the fix work? Any new problems?

4. **Compare outputs side-by-side**
   - Use a markdown table if possible
   - Highlight what changed
   - Note if new errors appeared

5. **Repeat until passing**
   - Each iteration should only change 1-2 things
   - Keep a changelog
   - Don't skip testing

**Notes to keep during iteration:**
- Before/after outputs (save as markdown)
- What you think the root cause is (hypothesis)
- Why your fix should work (reasoning)
- Side effects of your fix (did it break something else?)

---

## 4. How to Capture & Review AI Work

### **Capturing Outputs (What to Save)**

**Always save:**
1. **Raw output** – Copy-paste verbatim from GPT/Claude
   - Format: `GPT-v1.0-Raw.md` or `Claude-v1.1-Raw.md`
   - Keep the full text, no edits

2. **Evaluation note** – Your critique of the output
   - Format: `Eval-v1.0.md`
   - Answer: "Does this work? Why/why not?"

3. **Test results** – For each test case, did it pass?
   - Format: table or structured list
   - Include: input, expected, actual, status

**Optional but useful:**
- Tokenizer visualization (if format is the issue)
- Cost breakdown (tokens × price)
- Performance metrics (latency, accuracy %)

### **Review Checklist (Use Every Time)**

```markdown
## AI Work Review Checklist

- [ ] Output is well-formed (no truncation, syntax errors)
- [ ] Format matches specification exactly
- [ ] All test cases produce correct output
- [ ] No hallucinations or false positives
- [ ] Explanations are accurate and useful
- [ ] Instructions were followed (no skipped sections)
- [ ] Output is reproducible (run 2x, same result?)

## If Something Failed
- [ ] Identify EXACTLY which instruction was misunderstood
- [ ] Determine if it's a prompt issue or model limitation
- [ ] Write down the root cause hypothesis
- [ ] Plan a specific, minimal fix
```

---

## 5. Organization & Tagging

### **Tagging Strategy**

Use consistent tags in frontmatter:

```yaml
tags: [type/prompt, domain/grammar, status/tested, model/gpt-4, urgency/high]
```

**Tag categories:**
- `type/[prompt|project|research|experiment]`
- `domain/[ai-learn|grammar|system-spec|writing|reasoning]`
- `status/[draft|tested|production|archived]`
- `model/[gpt-4|claude|both]`
- `urgency/[high|medium|low]`

### **Dataview Queries to Build Dashboards**

**Example 1: All Active Prompts by Domain**
```dataview
table domain, model, status, last-tested
from #type/prompt
where status != "archived"
group by domain
sort status desc
```

**Example 2: Project Status Overview**
```dataview
table status, priority, deadline
from #type/project
where status != "shipped"
sort priority desc
```

**Example 3: Recently Tested Prompts**
```dataview
table last-tested, domain, model
from #type/prompt
sort last-tested desc
limit 10
```

Add these to `00-system/Home.md` for quick overview.

---

## 6. Quick Retrieval & Reuse: Espanso vs PowerToys

### **Option A: Espanso (Recommended for prompts)**

**Why Espanso:**
- ✅ Free, lightweight, cross-platform (Windows, Mac, Linux)
- ✅ Fast expansion (type shortcut → full prompt)
- ✅ Works in any app (browsers, VS Code, ChatGPT UI)
- ✅ Easy to organize (YAML config, categorized)

**Setup (Windows):**

1. **Install Espanso:** https://espanso.org/install/
2. **Edit config file** (usually `%APPDATA%/espanso/match/base.yml`):

```yaml
matches:
  # Grammar Checker
  - trigger: grammachecker
    replace: |
      You are a system that checks English for grammar and naturalness...
      [FULL PROMPT HERE]
    label: Grammar Checker v1.0

  - trigger: grammaspec
    replace: |
      [MD REFERENCE CONTENT]
    label: Grammar Checker - MD Reference

  # System Spec Generator
  - trigger: specgen
    replace: |
      You are a system specification generator...
      [FULL PROMPT]

  # Learning AI
  - trigger: explainai
    replace: |
      Explain this AI concept clearly with examples...
      [PROMPT]

  # Variation: Use snippets from Obsidian
  - trigger: grammav2
    replace: |
      {{now}}
      Prompt version: 2.0
      Status: TESTED
      [INSERT PROMPT CONTENT]
```

**Workflow:**
1. Refine prompt in Obsidian
2. Copy final version
3. Paste into Espanso config
4. Reload Espanso
5. Type `:grammachecker` in ChatGPT → instant prompt

**Best practice:** Only add prompts to Espanso after they're **tested and stable**. Keep drafts in Obsidian only.

---

### **Option B: PowerToys Run (Windows-specific)**

**Why PowerToys:**
- ✅ Built into Windows
- ✅ Fast search + action launcher
- ✅ Can call scripts, open files quickly

**Why NOT for prompts:**
- ❌ More complex setup for text expansion
- ❌ Requires creating plugins or PowerShell scripts
- ❌ Slower for large text blocks
- ❌ Better for file/app launching than text expansion

**Verdict:** Use **PowerToys** for launching Obsidian, VS Code, or quick file access. Use **Espanso** for prompt expansion.

---

### **Hybrid Workflow (Recommended)**

```
Workflow: Research in Obsidian → Test in GPT → Review & Refine → Add to Espanso

Day 1: Draft prompt in Obsidian (10-prompts/grammar/)
       ↓
Day 2: Test on 5 test cases in ChatGPT
       ↓
Day 3: Review results, identify issues
       ↓
Day 4: Fix prompt, retest
       ↓
Day 5: PASSING → Copy to Espanso config
       ↓
Now:   :grammachecker + Enter = instant prompt in any app
```

---

## 7. Personal Wiki Index & Discovery

### **Create a Home Dashboard**
File: `00-system/Home.md`

```markdown
# Personal Wiki Home

## Quick Navigation

### 📚 Prompts by Domain
- [[10-prompts-ai-learn]] – Understanding AI concepts
- [[10-prompts-system-specs]] – Building system specs
- [[10-prompts-grammar]] – Grammar & naturalness
- [[10-prompts-writing]] – Writing assistance
- [[10-prompts-reasoning]] – Problem solving

### 🔧 Active Projects
```dataview
table status, priority, created
from #type/project
where status != "shipped"
sort priority desc
```

### 🧪 Recent Iterations
```dataview
table project, version, date, status
from #type/iteration-log
sort date desc
limit 5
```

### 📖 Latest Research
```dataview
table from, date
from #type/research
sort date desc
limit 5
```

### 📊 Vault Stats
- Total prompts: [will auto-update with Dataview]
- Active projects: [count]
- Tested & stable: [count]

---

## Search & Retrieval Tips

1. **Quick search:** Obsidian Cmd+P → "Open Quick Switcher"
   - Type "grammar" → all grammar-related notes

2. **Backlinks:** Click any [[note-name]] to see what links to it
   - Useful for seeing which projects use a prompt

3. **Graph view:** Cmd+Shift+G to see knowledge graph
   - Clusters of related notes = your wiki structure

4. **Dataview:** Build custom dashboards (see examples above)
   - Filters by tag, status, domain
   - Updates automatically
```

### **Create MOC (Map of Contents) Notes**

A MOC is a note that links together related notes.

**Example MOC:** `20-research/AI-Learning-MOC.md`

```markdown
# AI Learning Map of Contents

## Foundational Concepts
- [[LLM-Architecture]]
- [[Tokenization]]
- [[Attention-Mechanism]]

## Practical Skills
- [[Prompt-Engineering-Techniques]]
- [[Few-Shot-Learning]]
- [[Chain-of-Thought]]

## Projects Using This Knowledge
- [[30-proj-grammar-checker]] – Applied naturalness evaluation
- [[30-proj-custom-gpt]] – Prompt design

## Related Prompts
- [[Explain-Concept-Prompt]]
- [[Reasoning-Prompt]]
```

Link from `Home.md` to all MOCs for easy navigation.

---

## 8. End-to-End Example: Grammar Checker Project

### **Day 1: Capture**

**File 1:** `30-projects/30-proj-grammar-checker/Spec.md`
```markdown
---
type: project
name: Grammar Checker (C1 Level)
status: in-progress
created: 2025-12-21
---

## Goal
Build a system that evaluates English text for grammar and naturalness
errors at C1 level (advanced non-native speakers).

## Success Criteria
- [ ] Passes 5 test cases from business email domain
- [ ] Passes 5 test cases from technical forum domain
- [ ] Differentiates between Prescriptive/Descriptive errors
- [ ] Produces explanations for all Tier 2 errors
- [ ] Works consistently on GPT-4 and Claude 3.5

## Test Cases
| Domain | Input | Expected | Status |
|--------|-------|----------|--------|
| Business | "Hey Dr. Smith..." | 3 Tier 2 errors | ⏳ Testing |
| Forum | "So I've been..." | 4 Tier 2 errors | ⏳ Testing |

## System Prompts
- [[Grammar-Checker-Main-Instruction]]
- [[Grammar-Checker-MD-Reference]]
```

**File 2:** `10-prompts-grammar/Grammar-Checker-Main.md`
```markdown
---
type: prompt
domain: grammar
purpose: C1-level grammar and naturalness evaluation
model: both
status: draft
version: 0.1
---

## Prompt
You are a system that evaluates English text...
[FULL PROMPT TEXT]

## Test Cases
[From project spec]
```

**File 3:** `30-projects/30-proj-grammar-checker/Test-Cases.md`
```markdown
# Test Cases for Grammar Checker

## Test 1: Business Email
**Input:**
```
Hey Dr. Smith, I wanted to reach out regarding...
```

**Expected Output:**
- Section 1: Tier 1 errors (typos, obvious fixes)
- Section 2: Tier 2 errors (complex issues)
- Section 3: Explanations for Tier 2
- Section 4: Native alternatives
```

---

### **Day 2: First Run & Capture**

**File 4:** `30-projects/30-proj-grammar-checker/Results/GPT-v0.1-Raw.md`
```markdown
# GPT-4 Output - v0.1

[PASTE FULL OUTPUT FROM CHATGPT HERE - NO EDITS]
```

**File 5:** `30-projects/30-proj-grammar-checker/Results/Eval-v0.1.md`
```markdown
---
type: evaluation
project: [[Grammar-Checker]]
iteration: v0.1
model: GPT-4
---

## Scorecard
| Criterion | Result | Evidence |
|-----------|--------|----------|
| Format | ❌ FAIL | Section 1 markup missing |
| Completeness | ✅ PASS | All 4 sections present |
| Accuracy | ⚠️ PARTIAL | Test 1 OK, Test 2 wrong |

## Root Causes Found
1. **Markup issue:** Prompt said use *italics* for Tier 1, but output has no italics
   - Hypothesis: Model ignored formatting instruction
   - Fix: Add "You MUST use *asterisks*" more explicitly

2. **Label ambiguity:** Some errors got both Prescriptive AND Descriptive
   - Hypothesis: Instructions didn't make labels mutually exclusive
   - Fix: Add priority rule (if grammar is wrong → Prescriptive, else Descriptive)

## Next Action
- Apply 2 fixes to main prompt
- Re-test on same 2 test cases
```

---

### **Day 3: First Iteration**

**File 6:** `30-projects/30-proj-grammar-checker/Iterations/v0.2-Changes.md`
```markdown
---
type: iteration-log
project: [[Grammar-Checker]]
version: 0.2
date: 2025-12-22
---

## Changes Made

### Change 1: Explicit Markup Rule
**Old:** "Mark Tier 1 errors with italics."
**New:** "Mark Tier 1 errors with *asterisks on both sides* like this: *error*."

Reason: Model may have missed the markup instruction. Being more explicit helps.

### Change 2: Label Priority Rule
**Added new paragraph:**
```
Label each Tier 2 error with EXACTLY ONE label:
- Use Prescriptive if there is a grammar, collocation, or mood error
- Use Descriptive if grammar is correct but register/tone is wrong
- Use Naturalness if sentence is correct but sounds non-native
Choose the FIRST matching rule only. Do not use multiple labels.
```

Reason: GPT output had "Prescriptive/Descriptive" for some errors, showing ambiguity.

## Testing
**Re-ran on Test 1 (Business Email):**
- Markup now present? ✅ YES
- Labels mutually exclusive? ✅ YES
- Accuracy improved? ⚠️ Partial (1 new error introduced)

**New Issue Found:**
- Missing explanation for one Tier 2 error (section 3 incomplete)
- This is a new regression – change 1 or 2 broke something

## Next Iteration
- Review which change caused regression
- Likely: Change 2 made label rule too strict
- Try: Relax naturalness definition slightly
```

**File 7:** `30-projects/30-proj-grammar-checker/Results/GPT-v0.2-Raw.md`
```markdown
[PASTE FULL v0.2 OUTPUT HERE]
```

---

### **Day 4: Analyze Regression, Plan v0.3**

**File 8:** `30-projects/30-proj-grammar-checker/Iterations/v0.2-Analysis.md`
```markdown
---
type: evaluation
project: [[Grammar-Checker]]
iteration: v0.2
issue: regression-in-section-3
---

## What Broke
**Error #4 in Test 1:**
- Expected explanation: "This sounds non-native because..."
- Got: (no explanation in Section 3)

## Why
- Error #4 is labeled "Naturalness"
- Change 2 added: "Choose the FIRST matching rule only"
- Error #4 ALSO matches "Descriptive" rule (unclear grammar)
- Model chose "Descriptive" first, skipped "Naturalness"
- But explanation shouldn't disappear either way

## Root Cause
The "first rule wins" logic is too aggressive. The rule should be:
- "If multiple rules match, choose the MOST SPECIFIC one"
- Prescriptive > Descriptive > Naturalness (by specificity)

## Proposed Fix for v0.3
Replace Change 2 with:
```
When labeling, if multiple categories apply:
1. Prescriptive always takes precedence (grammar is fundamental)
2. If no grammar error, then Descriptive (context matters)
3. If only stylistic/non-native feeling, then Naturalness
Use exactly ONE label per error. No "/" combinations.
```

## Confidence
High – this is a clear precedence rule, not ambiguous like v0.2.
```

---

### **Day 5: Execute v0.3 & Validate**

**File 9:** Updated `10-prompts-grammar/Grammar-Checker-Main.md`
```markdown
---
version: 0.3
last-tested: 2025-12-22
status: tested
---

[UPDATED PROMPT WITH FIX]
```

**File 10:** `30-projects/30-proj-grammar-checker/Results/GPT-v0.3-Raw.md`
```markdown
[PASTE v0.3 OUTPUT]
```

**File 11:** `30-projects/30-proj-grammar-checker/Iterations/v0.3-Complete.md`
```markdown
---
type: iteration-log
version: 0.3
status: complete
---

## Result: ✅ ALL TESTS PASS

### Test 1 (Business Email)
- Format: ✅ All markup correct
- Completeness: ✅ All 4 sections, all errors explained
- Accuracy: ✅ 3/3 Tier 2 errors correct labels
- Naturalness: ✅ Good explanations

### Test 2 (Forum Post)
- Format: ✅ Correct
- Completeness: ✅ Complete
- Accuracy: ✅ 4/4 errors correct
- Naturalness: ✅ Clear explanations

## Iteration Complete
- 3 versions tested (v0.1, v0.2, v0.3)
- Root causes systematically fixed
- All test cases passing
- Ready for production

## Next: Add to Espanso
```

---

### **Day 6: Finalize & Deploy**

**File 12:** Updated project spec status
```markdown
---
status: shipped
---

## Results
- ✅ 10 test cases passing
- ✅ Tested on GPT-4 and Claude 3.5
- ✅ Ready for production

## Deployment
- Added to Espanso: `:grammachecker`
- Added to prompt library: [[10-prompts-grammar/Grammar-Checker-Production]]
- Archive old versions: [[50-archive/grammar-checker-v0.1]]
```

**Final:** Update `00-system/Home.md` to reflect project completion
```markdown
### 🎉 Shipped Projects
- Grammar Checker (v1.0) – C1-level evaluation ✅
```

---

## Summary: The Complete Workflow

| Phase | Action | File Type | Tool |
|-------|--------|-----------|------|
| **Design** | Write spec & test cases | `.md` in 30-projects | Obsidian |
| **Initial Run** | Paste prompt + test case into AI | Raw output `.md` | ChatGPT/Claude |
| **Capture** | Save raw AI output | `Results/[Model]-vX-Raw.md` | Obsidian |
| **Review** | Evaluate output, find failures | `Eval-vX.md` | Obsidian (template) |
| **Fix** | Update prompt based on findings | Update `10-prompts/` | Obsidian |
| **Re-test** | Run updated prompt on same tests | New raw output | ChatGPT/Claude |
| **Iterate** | Log changes & findings | `Iterations/vX.md` | Obsidian (template) |
| **Validate** | Confirm all tests pass | Final eval | Obsidian |
| **Deploy** | Add to Espanso, archive old | Update Espanso config | Espanso/Obsidian |

---

## Key Principles to Remember

1. **One change per iteration** – Don't change 5 things at once
2. **Always retest** – Run updated prompt on all previous test cases
3. **Save everything** – Raw output, evaluations, reasoning
4. **Tag & link** – Use `[[links]]` and frontmatter tags
5. **MOCs & dashboards** – Build navigation that grows with your vault
6. **Version your work** – v0.1, v0.2, v1.0 tells the story
7. **Only add to Espanso when STABLE** – Don't expand half-finished prompts
8. **Review systematically** – Use the checklist every time
9. **Archive old versions** – Keep them searchable but out of sight
10. **Build in public** – Your wiki should tell a clear narrative of what you learned

---

## Resources & Next Steps

- **Obsidian docs:** https://help.obsidian.md/
- **Templater plugin:** https://silentvoid13.github.io/Templater/
- **Dataview plugin:** https://blacksmithgu.github.io/obsidian-dataview/
- **Espanso docs:** https://espanso.org/docs/
- **Your grammar checker files:** Cross-link to them as you build

Start with ONE project (e.g., grammar checker), follow this workflow end-to-end, then replicate for system spec generator and custom GPT. You'll develop a muscle memory for the pattern.
