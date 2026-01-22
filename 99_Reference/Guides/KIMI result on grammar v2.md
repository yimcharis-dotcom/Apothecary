
Below is a **zero-coding, zero-infrastructure** path that takes you from “nothing” to “I have a grammar checker running inside Obsidian, powered by either (a) Perplexity Labs (PPLX) or (b) a ChatGPT / GPT project, and I know exactly how to judge the quality of the AI suggestions.”  
Every click, every setting, every sanity-check is spelled out.  
Skip nothing—do it in order.

---

## 0. Pick your weapon (30 s)

| Option | What it is | Privacy | Cost | When to choose |
|---|---|---|---|---|
| **Harper** | Pure-offline grammar engine inside Obsidian | 100 % local | Free | You want zero setup and zero data leaves your laptop. |
| **LanguageTool** cloud | Community plug-in, calls LT servers | Text leaves vault | Free tier 20 k chars / req | Fastest cloud path, no credit card. |
| **PPLX Labs (pplx-api)** | Open-source LLM endpoint (Sonar, Llama-3.1, etc.) | Text leaves vault | Free tier 7 $ credit / month | You want LLM-level rewrites, not just “red underline”. |
| **ChatGPT “project”** | GPT-4o-mini or GPT-4 inside a custom GPT | Text leaves vault | Pay-as-you-go | You already have OpenAI credits and want a custom prompt. |

Pick **ONE** now; you can swap later without losing notes.  
The rest of the guide is forked so you can’t get lost.

---

## 1. One-time Obsidian prep (2 min)

1. Install Obsidian desktop (≥ v1.6).  
2. Create a new vault called `GrammarLab`.  
3. Settings → Community plug-ins → Turn off “Safe mode”.  
4. Create three permanent notes you will reuse for testing:  
   - `01-draft-raw` – paste any ugly paragraph here.  
   - `02-ai-suggestion` – empty, will hold the AI rewrite.  
   - `03-evaluation-log` – you will jot down “good / bad / why” for every run.

---

## 2-A. Harper route (offline, 90 s)

1. Settings → Community plug-ins → Browse → search **“Harper”** → Install → Enable.  
2. That’s it. Harper immediately underlines errors inside any note.  
3. **Evaluation protocol**  
   - Right-click an underline → look at the card.  
   - In `03-evaluation-log` write:  
     ```
     2025-12-22 09:14
     Original: "Each of the students have a book."
     Harper: "Each of the students has a book."
     Verdict: ACCEPT. Subject-verb agreement fix is correct.
     ```
   - Keep a running tally: **Accept / Reject / False-positive**.  
   - After 20 sentences you’ll have a % acceptance rate—your first quality metric.

---

## 2-B. LanguageTool cloud route (3 min)

1. Same plug-in browser → search **“LanguageTool Integration”** → Install → Enable.  
2. Settings → LanguageTool Integration:  
   - Endpoint: `Standard` (default)  
   - API key: leave empty (free tier)  
   - Auto-check ON.  
3. A small “Aa” icon appears in the status bar.  
4. **Evaluation protocol** identical to Harper, but LT also gives “punctuation” and “style” hints.  
5. Optional privacy upgrade (later): run LT locally in Docker (`docker run -p 8010:8010 erikvl87/languagetool`) and change endpoint to `http://localhost:8010` .

---

## 2-C. PPLX Labs route (LLM-powered, 10 min)

### 2-C-1 Get your key

1. Go to [https://labs.perplexity.ai](https://labs.perplexity.ai) → sign in with GitHub → Generate API key → copy it.

### 2-C-2 Create a “grammar GPT” inside Obsidian (no code)

We will piggy-back on the free “Text Generator” community plug-in that can call ANY Open-AI-compatible endpoint.

1. Plug-in browser → search **“Text Generator”** → Install → Enable.  
2. Settings → Text Generator → Add new provider:  
   - Name: `PPLX-Sonar`  
   - Base URL: `https://api.perplexity.ai`  
   - Model: `sonar` (cheapest, good at grammar)  
   - Bearer token: paste your PPLX key.  
3. Still in settings → Templates → Add template:  
   - Title: `GrammarFix`  
   - Prompt:
     ```
     You are an expert copy-editor.  
     Rewrite the following text so it is grammatically correct and stylistically clear.  
     Output ONLY the rewritten text, no explanations.  
     ```
   - Insert cursor variable: `{{selection}}`  
   - Output: `replace` (or `append to note` if you prefer).  
4. Hot-key: bind `Ctrl+Shift+G` to template `GrammarFix`.  

### 2-C-3 First run

1. In note `01-draft-raw` paste:  
   “The data are insufficient to makes a conclusion.”  
2. Select the sentence → press `Ctrl+Shift+G`.  
3. Within 2 s the sentence is replaced with:  
   “The data are insufficient to draw a conclusion.”  

### 2-C-4 Evaluation pipeline (this is the critical part)

1. Immediately copy the rewritten text into `02-ai-suggestion`.  
2. Manually compare the two versions side-by-side.  
3. In `03-evaluation-log` fill five fields for every run:  
   - **ID** (time stamp)  
   - **Original**  
   - **AI rewrite**  
   - **Error types fixed** (subject-verb, article, punctuation, etc.)  
   - **Verdict** (Accept / Reject / Partial)  
   - **Notes** (e.g., “changed meaning slightly – ‘draw’ vs ‘make’”)  
4. After 30 samples compute:  
   - **Precision** = Accepted rewrites / Total rewrites  
   - **Recall** = Errors you agree existed / Total errors you spotted manually  
   - **Meaning drift** = # of times the LLM changed your intended meaning  
5. Keep a running markdown table in `03-evaluation-log`; it becomes your “quality dashboard”.  

### 2-C-5 Iterating the prompt (no coding)

If precision < 85 % or meaning drift > 5 %, tweak the prompt:  
- Add “Do NOT change technical terms.”  
- Add “Use Oxford comma.”  
- Add “Keep sentence length similar.”  
Each change becomes a new template (`GrammarFix-v2`, etc.) and you rerun the same 30 samples to see if metrics improve—classic A/B testing without code.

---

## 2-D. ChatGPT “project” route (identical to 2-C, but OpenAI)

1. Open [https://chatgpt.com](https://chatgpt.com) → “Create a project” → name it `Obsidian-Grammar`.  
2. In the project instructions paste the same prompt as in 2-C-2.  
3. Settings → Custom GPT → enable “Code Interpreter” if you want readability stats.  
4. Use the **“Text Generator”** plug-in exactly as in 2-C, but base URL:  
   `https://api.openai.com/v1`  
   Model: `gpt-4o-mini` (cheap) or `gpt-4o` (best).  
5. Evaluation protocol stays identical; you can even paste the `03-evaluation-log` table into the GPT project and ask it to compute precision/recall for you.

---

## 3. Daily workflow (30 s per note)

1. Write freely in any note—ignore errors while in flow.  
2. When ready, either:  
   - Harper/LT: click the status-bar icon → accept/reject pop-ups.  
   - PPLX/ChatGPT: select paragraph → `Ctrl+Shift+G` → glance at rewrite → accept (`Enter`) or undo (`Ctrl+Z`).  
3. Log the verdict in `03-evaluation-log` (one line is enough).  
4. End of week: open `03-evaluation-log`, add a ## Weekly summary heading, count Accept vs Reject, decide whether to tweak prompt or switch provider.

---

## 4. Advanced guardrails (optional, still no code)

- **“Freeze” technical terms**: maintain a note `terms-to-protect` and add to prompt: “Never change the following terms: {{terms-to-protect}}”.  
- **Readability target**: append to prompt “Flesch score ≥ 60.” (GPT-4 can calculate it).  
- **Multi-language**: create separate templates `GrammarFix-ES`, `GrammarFix-FR` and change the model instruction language accordingly.  
- **Batch mode**: select multiple paragraphs → Text Generator will process each block and return them in sequence; log aggregate metrics.

---

## 5. Completion checklist

- [ ] Grammar checker installed and hot-keyed.  
- [ ] 30-sentence evaluation log filled (baseline metrics).  
- [ ] Precision ≥ 85 % or you know why it isn’t.  
- [ ] Meaning-drift events ≤ 5 %.  
- [ ] Weekly review habit scheduled (calendar reminder).  

The moment you can tick all five boxes, your “grammar checker” is **production-ready** inside Obsidian—no further coding required. When you **do** learn to code later, you can replace Text-Generator with your own plug-in or move the same API calls to PPLX-Space or a GitHub Action, but the evaluation discipline above stays identical.

Happy writing!