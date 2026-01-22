
-Below is the **“kitchen-sink” companion** to the grammar-checker recipe.  
I have broken it into two mega-sections:

**A. Practical tips & tricks for EVERY sub-step** of the four grammar routes (Harper, LanguageTool, PPLX, ChatGPT).  
**B. “I’m an audit/accounting professional who has never taken notes—how do I turn Obsidian into a personal wiki without drowning in clutter?”**

Print it, tick items off, copy-paste templates directly into Obsidian.

---

## A. Grammar checker – exhaustive field manual

### 0. Weapon-selection cheat-sheet (expanded)

| Route            | Hidden gotcha                                                                          | Pro hack                                                                                                      |          |
| ---------------- | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | -------- |
| **Harper**       | Only English, no style suggestions                                                     | Bind `Ctrl-Shift-H` to “Harper: show next issue” so you can review every underline without touching the mouse |          |
| **LanguageTool** | Free cloud server sometimes 503’s                                                      | Keep a second template that hits `http://localhost:8010` (docker) and switch in 5 s when cloud dies           |          |
| **PPLX**         | You pay per token, empty lines cost money                                              | Strip blank lines with a 1-line template pre-processor: `{{selection                                          | strip}}` |
| **ChatGPT**      | GPT-4o-mini is **twice** cheaper and **grammar-only** tasks score within 2 % of GPT-4o | Unless you need nuance, stay on mini for 90 % savings                                                         |          |

---

### 1. Obsidian prep – deep dive

- **Vault naming**: append the date (`GrammarLab-2025Q4`) so you can archive a whole quarter and start fresh without losing data.  
- **Core plug-ins to enable once and forget**:  
  – File Recovery (snapshots every 5 min)  
  – Word count (needed for token estimation)  
- **Folder layout that scales**:
  ```
  00-inbox/
  01-grammar/
    01-drafts/
    02-rewrites/
    03-logs/
  02-templates/
  03-scripts/   (empty for now, reserved)
  ```
- **Daily note automation** (built-in): Settings → Core → Daily notes → date format `YYYY-MM-DD ddd` → open command palette “Daily notes: open” every morning; write one line “Grammar runs today: ___” so you can correlate quality dips with sleepy days.

---

### 2-A. Harper – micro-tactics

- **Colour-blind friendly**: Harper uses red underline same as spell-check; change in Settings → Appearance → CSS → add snippet:
  ```css
  .harper-error {
    border-bottom: 2px dotted #00FF00;
  }
  ```
- **Keyboard macro (AutoHotKey or Karabiner)**: map `F6` to `Ctrl-Shift-H` → `Enter` → `Ctrl-→` (jump to next word) so you can accept/reject while keeping hands on arrow keys.  
- **False-positive whitelist**: Harper ships with `harper-obsidian.md` in `.obsidian/plugins/harper/`; append words like “EBITDA”, “SOX”, “ASC842” once and they disappear forever.  
- **Metrics shortcut**: at end of week, run command palette “Harper: count issues in current note” → jot number in `03-evaluation-log` → divide by word-count → “issues per 100 words” trending down = success.

---

### 2-B. LanguageTool – micro-tactics

- **Rule toggles** (web UI): visit `https://community.languagetool.org/rule/list` → disable “UPPERCASE_SENTENCE_START” if you often quote ISO codes like “ebitda” at line start.  
- **Picky vs standard mode**: add `&level=picky` to API call in Text-Generator template to catch passive voice and “really, very” fluff.  
- **Mother-tongue interference**: set `&motherTongue=zh` (or your L1) → LT will flag Chinese-style comma splices specifically.  
- **Docker health-check**: create note `LT-docker` with code block:
  ```bash
  docker run -d --rm -p 8010:8010 \
    --memory="1g" --cpus="0.5" \
    erikvl87/languagetool
  ```
  and a companion note `LT-check` containing `http://localhost:8010/v2/check?language=en-US&text=test` — click to verify local server is up before big batch jobs.

---

### 2-C. PPLX – micro-tactics

- **Token budget guardrail**: Sonar costs ~0.07 $ per 1 M input tokens. A 100-word paragraph ≈ 150 tokens → 4 000 fixes per dollar. Put a recurring calendar entry “PPLX credit 5 $” so you never hit zero unexpectedly.  
- **Streaming on/off**: Text-Generator has toggle “stream responses”; turn OFF if you want to log raw JSON for later debugging.  
- **Temperature**: set `0.15` in provider config—lower than default 0.2 to reduce creative “improvements” that change meaning.  
- **Post-processing hygiene**: add second template `GrammarFix-Clean` that strips markdown code fences the model sometimes hallucinates:
  ```
  Replace ``` with empty string.
  ```
  Chain the two templates with macro `Ctrl-Shift-Alt-G`.  
- **A/B prompt storage**: keep prompts in separate notes under `02-templates/prompts/` and paste into Text-Generator config instead of typing inside settings—faster rollback.

---

### 2-D. ChatGPT project – micro-tactics

- **Project-level instruction** (2000-char limit) – include **negative examples**:
  ```
  NEVER replace “ASC 842” with “ASC-842”.
  NEVER change currency codes (keep “USD”, not “$”).
  ```
- **Upload a “style bible” PDF** (max 512 MB) into the project — GPT can reference it during rewrite.  
- **Use “compare” button** inside ChatGPT web UI to visual-diff two rewrites—screenshot the delta and drag image into `03-evaluation-log` for future you.  
- **Cost cap**: OpenAI allows hard monthly limit—set to 10 $ so an infinite loop in a template cannot burn your card.  
- **Prompt versioning**: every time you change instructions, increment version in first line `# v3.2 2025-12-22` — makes correlation with evaluation log trivial.

---

### 3. Daily workflow – advanced

- **Command-palette only habit**: hide left ribbon (Settings → Appearance → Show ribbon OFF) to force yourself to use `Ctrl-P` “GrammarFix” → muscle memory in 3 days.  
- **Mobile fallback**: Obsidian mobile cannot load Text-Generator, but **LanguageTool official app** (iOS/Android) shares clipboard; write on phone → share → LT app → copy back → sync via Obsidian-git.  
- **Batch night**: Friday 4 pm, select all weekly meeting minutes → run template → log aggregate metrics → export CSV via “Obsidian Advanced Tables” → pivot in Excel to find which meeting type produces most grammar issues (usually “stand-up” because of fragmented speech).

---

### 4. Guardrails – deep dive

- **Meaning-drift detector**: append to prompt  
  “After rewrite, list every changed word as ‘OLD → NEW’.”  
  You get an instant diff; if list > 3 items for a 30-word sentence, reject.  
- **Flesch readability inside Obsidian**: install “Obsidian Reading Time” plug-in → enables `{{readability}}` placeholder; log the number before/after rewrite to ensure you are not oversimplifying technical prose.  
- **Protected-regex list**: maintain note `protect-patterns` with lines like  
  `\bQ\d{1,2}\b` (matches Q1, Q2…)  
  and inject into prompt: “Do not alter text matching these regexes: {{protect-patterns}}”  
- **Sentiment guard**: if your original text is negative (performance review warning), add to prompt “preserve negative tone” so the AI doesn’t accidentally soften language.

---

## B. Personal wiki for an audit/accounting professional who has never taken notes

### Mindset shift first

You are **not** “taking notes”, you are **building an external brain** that pays compound interest: every piece of data you capture today saves 5 min in a future audit or client call.  
Think in **three buckets**:

1. **Capture** – anything that sparks “huh, interesting” in 5 s or less.  
2. **Connect** – tag or link so you can surface it when you need it **without remembering the exact keyword**.  
3. **Create** – turn captured crumbs into deliverables (work-papers, client decks, career portfolio).

---

### 0. Folder design that mirrors your real life

```
00-inbox/               ← default dump
01-zettels/             ← permanent notes (one idea per file)
02-projects/
  2025Q4-ClientABC/
  2025Q4-IPO-Project/
03-areas/
  Audit
  Tax
  Accounting-Standards
  Tech-Tools
  Career
04-resources/
  Laws
  Checklists
  CPE-slides
05-archive/
templates/
scripts/
```

**Rule**: if something has a deadline → lives in `02-projects`; if it’s an ongoing responsibility (e.g., “monthly consolidation”) → `03-areas`.

---

### 1. When to jot – exhaustive trigger list

Copy this into a note `when-to-capture`; review it weekly until internalised.

| Scenario | What to capture | Template / tag |
|---|---|---|
| Client call ends | Decisions, open items, who owns what | `#meeting` `@owner` |
| Partner blurts obscure regulation | Exact wording + source PDF page | `#reg` |
| You google the same JE twice | Screenshot + JE template | `#recurring` |
| Staff asks you a question | Question + your answer → becomes future FAQ | `#faq` |
| CPE webinar | One golden sentence + timestamp | `#gold` |
| You make a mistake | What went wrong + preventive control | `#lesson` |
| Coffee chat | Colleague’s career path | `#network` |
| Random idea while driving | Voice memo → auto-transcribe → inbox | `#spark` |

**30-second rule**: if capture takes > 30 s, skip—you will resist next time.

---

### 2. How to jot – frictionless templates

Create note `T-meeting` in `templates/`:

```
---
date: {{date}} {{time}}
client: 
type: call / field / zoom
attendees:
tags: meeting, {{client}}
---

## Purpose

## Key points

## Decisions

## Open items | owner | due
- [ ]  |  | 

## Follow-up
```

**Hot-key**: `Ctrl-T` → select `T-meeting` → fill blanks.  
Same pattern for `T-je`, `T-faq`, `T-lesson`.

---

### 3. Linking – make it future-proof

- **Date format**: always `[[2025-12-22]]` inline—creates daily note automatically.  
- **MOC (Map of Content) notes**: maintain `MOC-Audit` and `MOC-Tax`—nothing else.  
  Every new permanent note must be linked from **at least one MOC within 24 h** or it rots.  
- **Index note per client**: `ClientABC-MOC` contains links to all work-papers + key regs + key people.  
- **Back-link pane** (built-in) → keep open on right; when you see empty “Unlinked mentions” convert to real link—5 s housekeeping.

---

### 4. Tag taxonomy – minimal viable

Three levels only:  
`#status-wip`, `#status-waiting`, `#status-done`  
`#type-faq`, `#type-checklist`, `#type-je`  
`#reg-ASC842`, `#reg-SOX`, `#reg-tax-163j`  
Avoid free-form tags—use search (`Ctrl-Shift-F`) for everything else.

---

### 5. Daily/weekly/monthly rituals

- **Morning (2 min)**: open daily note → copy yesterday’s open items → tag `#today`.  
- **End-of-day (2 min)**: scan inbox → move each note to correct folder → link to MOC → empty inbox to zero.  
- **Friday weekly review (30 min)**:  
  1. Search `tag:#lesson` created this week → distill into “top 3 lessons” → add to `Week-Review-2025W51`.  
  2. Search `tag:#waiting` → email people who owe you.  
  3. Update `MOC-Career` with any new achievements.  
- **Month-end (1 h)**: run “random note” (`Ctrl-O` → random) 20 times; if you encounter something outdated, update or archive—compounding knowledge hygiene.

---

### 6. Audit-specific workflows

- **Work-paper index**: every Excel file gets a markdown twin `WP-500-Accounts-Receivable.md` containing: purpose, source, conclusion, link to Excel (file:// absolute path or OneDrive share).  
- **Sampling documentation**: drag screenshot of sampling tool → Obsidian auto-pastes PNG → rename to `Sample-ClientABC-2025Q4.png` → embed in note.  
- **Issue log**: maintain `IssueLog-ClientABC` table:

  | Issue # | Description | Root cause | Impact | Status | Link |
  |---|---|---|---|---|---|
  | IC-25-001 | Revenue cut-off error | Sales clerk reversed date | 0.8 M | Open | [[2025-12-22-meeting]] |

- **CAAT/ACL scripts**: store `.acl` code block inside note; add tag `#script` so you can grep “which client did I use stratified sampling on?”

---

### 7. Accounting-standards knowledge base

- **One note per standard**: `ASC-842`, `IAS-12`, etc.  
- **Top of note**: copy exact paragraph from Codification → block-quote → below write “Plain English: …”  
- **Tag each paragraph with effective date**: `#eff-2025` so you can later search `tag:#eff-2027` to see what is coming.  
- **Cross-standard links**: `ASC-842` links to `TRG-842` (transition resource group) meeting summaries.

---

### 8. Career equity

- **Brag document**: note `Career-Wins` → every Friday add one bullet with metric: “Reduced reconciliation time 30 %” → link to evidence (Excel, email).  
- **Interview question bank**: tag `#interview`; when you hear a tricky question in a podcast, drop it in.  
- **CPE log**: template `T-CPE` contains date, hours, provider, summary → export to Excel at year-end for licence renewal.

---

### 9. Tool stack that plays nicely with Obsidian

- **Obsidian-git** plugin → auto-commit every hour → private GitHub repo = free backup + diff history.  
- **Obsidian-advanced-tables** → Excel-like navigation inside markdown tables.  
- **Obsidian-tasks** → any `- [ ]` with due date appears in a master task panel.  
- **Obsidian-canvas** → visual mind-map for complex audit scoping discussions.  
- **Zotero + mdnotes** → academic PDFs → drag citation into note → never lose source.  
- **Raycast (Mac) or PowerToys (Win)** → global hot-key to open Obsidian inbox even if app is closed.

---

### 10. Capture on the go (phone)

- **iOS Shortcuts**: “Add to Obsidian” shares any highlighted text → creates note `2025-12-22-094317.md` in `00-inbox/` → sync via Obsidian-Sync or git.  
- **Android**: same with “Obsidian URI” plugin → create widget on home screen.  
- **Voice**: use Otter.ai → export txt → drop into inbox → later distill to one-sentence gold nugget.

---

### 11. Anti-clutter rules

- **No PDF dumping**: extract **three sentences max** or highlight page range and link—storage is cheap, attention is not.  
- **No copy-paste without citation**: always add `> source: URL or “Partner John email 2025-12-22”` under quote—future you will trust it.  
- **Archive ruthlessly**: anything > 12 months old and no backlinks → move to `05-archive`; search still finds it, day-to-day list stays short.

---

### 12. 30-day onboarding plan

| Day | Task | Time |
|---|---|---|
| 1 | Install Obsidian, create vault, set daily note | 15 min |
| 2 | Build `T-meeting`, `T-je`, `T-lesson` | 20 min |
| 3–7 | Capture only, no linking, inbox allowed to bloat | 5 min/d |
| 8 | Create first MOC notes, link everything | 30 min |
| 9–14 | Add tags, clean inbox to zero every night | 5 min/d |
| 15 | Install git backup, push first time | 15 min |
| 16–21 | Use templates for real client work | — |
| 22 | Run first weekly review | 30 min |
| 23–30 | Add canvas, tasks, advanced tables as needed | — |
| 31 | Celebrate: you now have a **second brain** that pays rent. |

---

### 13. Quick-search cheat-sheet you can pin

- `path:02-projects tag:#waiting` → all open items across projects  
- `section:("## Key points") "revenue"` → revenue mentioned in meeting key points  
- `file:WP- tag:#ASC842` → all work-papers related to ASC 842  
- `section:("## Root cause") "cut-off"` → every cut-off error root cause you ever wrote

---

### 14. Exit ramp

When your vault > 2 000 notes and you crave automation, you already have:

- structured YAML front-matter → ready for Python parsing;  
- consistent tags → ready for graph analytics;  
- git history → ready for CI/CD (auto-pdf generation, anyone?).

Until then, **stay scrappy**—the best personal wiki is the one you actually use.

---

Copy any template block above straight into Obsidian, set your daily-capture hot-key, and start compounding knowledge today.