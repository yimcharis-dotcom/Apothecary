---
name: session-to-skill
description: "Extract a reusable Claude skill from the current conversation session. Use when the user says 'turn this into a skill', 'make a skill from this', 'capture this as a skill', 'skillify this', or otherwise asks to crystallize the work done in the current session into a repeatable skill. Also triggers when the user says 'create a skill for this task' after demonstrating a workflow through iteration. This skill observes the conversation history, extracts the emergent workflow, captures the agent's reasoning and corrections, and produces a skill that encodes both the correct path and the lessons learned getting there."
---

# Session to Skill

Extract a reusable skill from a working session by analyzing what happened, what went wrong, what the user corrected, and what the final working approach looks like.

This is not a prescriptive skill-builder. It is a retrospective distillation engine. The session already happened — your job is to observe it, understand it, and compress it into something another agent can follow without repeating the same mistakes.

## Mental Model

Think of yourself as a postmortem analyst who also writes the manual. You are examining a completed (or in-progress) collaboration between a user and an agent. That collaboration contains:

- **The task**: what the user wanted accomplished
- **The path**: the sequence of attempts, tools, and outputs
- **The corrections**: where the user redirected, refined, or challenged the agent
- **The reasoning**: why the agent made certain choices (and why some were wrong)
- **The teaching moments**: where the user forced the agent to re-examine its own logic

Your output is a skill that encodes the *correct* workflow while carrying forward the *lessons* from the incorrect attempts.

## Activation

This skill activates on demand when the user explicitly requests it. Do not self-activate or suggest skill extraction unprompted.

When triggered, your first move is always to analyze the conversation history before asking questions. Extract as much as you can from what already exists — the user has already done the work and shouldn't have to re-explain it.

## Workflow

```
ANALYZE → EXTRACT → DRAFT → PRESENT → REVISE → PACKAGE
```

### Phase 1: Analyze the Session

Read the full conversation. Build a mental map of what happened by identifying these elements:

**The task arc**: What did the user ask for? How did the goal evolve? Did the scope narrow or expand as the session progressed? Trace the goal from first mention to final form.

**The tool chain**: What tools, libraries, APIs, file formats, or external systems were involved? Note the order they were used and any that were abandoned.

**The iteration pattern**: Where did the agent get it right on the first try? Where did it take multiple attempts? For each multi-attempt sequence, identify what changed between attempts and why.

**Correction events**: Identify every point where the user redirected the agent. Classify each correction:
- **Factual correction**: agent had wrong information
- **Approach correction**: agent used wrong method/tool
- **Scope correction**: agent over- or under-delivered
- **Logic correction**: agent's reasoning was flawed
- **Quality correction**: output was technically correct but not what the user wanted

**Teaching mode sequences**: Detect when the user shifted from directing to teaching. Signals include:
- User asks "why did you do X?" (forcing re-examination)
- User points at specific output and says "look at this again"
- User asks leading questions that imply the answer without stating it
- User identifies contradictions in the agent's reasoning and presses until the agent articulates the error
- User does not accept surface-level acknowledgment — demands the agent explain what went wrong, why, and how to avoid it

See [references/teaching-mode-patterns.md](references/teaching-mode-patterns.md) for detailed recognition patterns and response protocols.

### Phase 2: Extract the Workflow

From your analysis, distill the *correct* workflow — not the chronological sequence of what happened, but the cleaned-up path that a future agent should follow.

**Separate signal from noise.** The session may contain dead ends, tangents, debugging detours, and exploratory attempts. The skill should encode the destination, not the wandering.

**Identify decision points.** Where did the workflow branch based on input characteristics, user preferences, or environmental conditions? These become conditional logic in the skill.

**Map inputs to outputs.** For each major step, define what goes in and what comes out. Be concrete — use actual examples from the session.

**Extract the anti-patterns.** Review your correction events from Phase 1. For each *major* correction (not minor course adjustments), formulate a "do not" instruction. Only include anti-patterns where:
- The mistake is non-obvious (an agent would plausibly repeat it)
- The correction required significant back-and-forth to resolve
- The user explicitly articulated why the approach was wrong

Minor corrections (formatting tweaks, small scope adjustments) do not warrant anti-pattern entries.

### Phase 3: Draft the Skill

Produce the skill using standard structure. Read [references/session-analysis-guide.md](references/session-analysis-guide.md) for the full template and output format.

The skill must contain:

**Frontmatter**: name, description with trigger phrases. Make the description slightly "pushy" to combat under-triggering — include synonyms and adjacent phrasings.

**Core instructions**: The cleaned-up workflow in imperative form. Each step should be actionable. Use numbered steps for sequential processes, decision trees for branching logic.

**Worked examples from the session**: Include 1–2 concrete input/output pairs drawn directly from the session. These serve double duty — they show the expected behavior AND they demonstrate the reasoning that was validated through iteration.

**Anti-pattern section** (when warranted): A short section titled "Common Mistakes" or "What Not To Do" that encodes the major lessons from corrections. Format as:

```markdown
## Common Mistakes

**Don't [description of wrong approach].**
This fails because [reason extracted from teaching-mode discussion].
Instead, [correct approach].
```

**Reasoning log reference**: Produce a separate `references/reasoning-log.md` that captures the full analytical trace — why each instruction exists, which session moments informed it, and what the agent learned from corrections. This is not included in the skill's main body (to keep token cost down) but exists for future revision sessions.

### Phase 4: Present and Explain

Show the user the drafted skill. Accompany it with a brief summary of your analysis:

- What you identified as the core workflow
- Which corrections you encoded as anti-patterns
- What you chose to leave out and why
- Any ambiguities or gaps you noticed

Do not present the reasoning log unless the user asks for it. The skill itself should be self-contained and readable.

### Phase 5: Revise

The skill draft is not final. Expect the user to iterate. Three revision triggers to watch for:

**On-demand revision**: User directly says to change something. Straightforward — apply the edit.

**Friction-signal revision**: During review, the user repeatedly questions the same section or asks you to re-read parts of the conversation. This signals the skill doesn't accurately capture what happened. Go back to Phase 1 for that specific section, re-analyze, and redraft.

**Teaching-mode revision**: The user shifts into Socratic correction — asking you *why* you wrote a particular instruction, pointing out contradictions between your skill and what actually happened in the session, or pressing you to re-examine your own reasoning about the skill's structure.

When teaching mode activates during revision:

1. **Do not deflect.** Do not say "you're right, I'll fix that." The user is asking you to understand *why* you were wrong.
2. **Walk back through your reasoning.** Trace the chain: "I wrote instruction X because I observed Y in the session, which I interpreted as Z. But you're pointing out that Z was actually [corrected interpretation]."
3. **Articulate the error.** State clearly what you got wrong: the what (factual), the why (reasoning), and the how (what you should have done instead).
4. **Only then revise.** Update the skill based on the corrected understanding.
5. **Update the reasoning log.** Add the correction to the reasoning log as a lesson learned.

This is the most critical interaction pattern this skill handles. The user uses adversarial debugging of your reasoning chain to ensure the skill is accurate. They will not accept surface-level compliance — they need evidence that you understood the error before they trust the revision.

### Phase 6: Package

Once the user approves, finalize the skill:

1. Ensure SKILL.md frontmatter is valid YAML
2. Verify all referenced files exist
3. Place anti-patterns derived from teaching sessions as inline examples in the skill
4. Finalize the reasoning log with all revision history
5. Run the validation script if available:
   ```bash
   python /mnt/skills/user/skill-builder/scripts/validate_skill.py /path/to/skill
   ```
6. Copy to output location

## Revision Protocol for Future Sessions

If the user invokes this skill on a *subsequent* session working with a *previously generated* skill, treat it as a revision pass:

1. Read the existing skill and its reasoning log
2. Analyze the new session for friction points, corrections, and new patterns
3. Identify what the existing skill got wrong or missed
4. Propose targeted revisions (additions, removals, modifications)
5. Update the reasoning log with the new session's lessons

Never rewrite from scratch unless the workflow fundamentally changed. Prefer surgical edits that preserve what already works.

## Quality Criteria

Before presenting a skill, verify:

- Every instruction traces back to something that happened in the session (no invented steps)
- Anti-patterns trace back to actual corrections (no hypothetical warnings)
- Examples are drawn from real session data (no synthetic examples)
- The reasoning log explains *why* each instruction exists
- The skill is under 500 lines (move detail to references if needed)
- The description includes specific trigger phrases the user would actually say
