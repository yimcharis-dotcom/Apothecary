# Session Analysis Guide

This reference provides the detailed procedure for analyzing a conversation session and producing a skill from it.

## Analysis Procedure

### Step 1: Read the Full Session

Read the entire conversation from the beginning. Do not skim. You are looking for patterns that only emerge across the full arc — a correction in message 15 might reframe what happened in message 3.

### Step 2: Build the Event Timeline

Create a chronological list of significant events. An "event" is any of:

- User states or refines the goal
- Agent proposes an approach
- Agent executes a tool or produces output
- User accepts, rejects, or modifies output
- User corrects the agent's reasoning
- User shifts into teaching mode
- The goal or scope changes
- A dead end is reached and abandoned

For each event, note:
- What happened
- What the agent's reasoning was (stated or inferred)
- Whether the user accepted it
- If rejected, what the correction was

### Step 3: Identify the Stable Workflow

From the timeline, extract the sequence of steps that survived all iterations. This is the "final path" — the approach the session converged on. It may differ significantly from the initial approach.

Distinguish between:
- **Core steps**: present in every iteration, essential to the task
- **Conditional steps**: appeared only in certain branches or edge cases
- **Abandoned steps**: tried and discarded (these become anti-pattern candidates)

### Step 4: Classify Corrections

For each correction event, assign a severity:

| Severity | Criteria | Skill Encoding |
|----------|----------|----------------|
| Major | Multi-turn correction, teaching mode, fundamental error | Anti-pattern section with explanation |
| Medium | 2-3 turn correction, wrong approach but reasonable reasoning | Inline note on the relevant step |
| Minor | Single correction, preference/style | Reasoning log only |

### Step 5: Extract Implicit Knowledge

Some of the most valuable skill content is never explicitly stated in the session. Look for:

- **Unstated prerequisites**: things the user assumed the agent knew
- **Domain conventions**: naming patterns, file structures, coding styles used without explanation
- **Tool preferences**: when the user preferred one approach over an equally valid alternative
- **Quality standards**: what made the user accept output vs. request changes

These become background context or conventions sections in the skill.

## Skill Output Template

```markdown
---
name: [kebab-case-name]
description: "[What it does]. Use when [trigger phrases, file types, user language]. Also use when [adjacent triggers to prevent under-triggering]."
---

# [Skill Name]

[One paragraph: what this skill does and when to use it.]

## Workflow

1. **[Step]** → [Brief description]
2. **[Step]** → [Brief description]
...

## [Step 1 Detail]

[Imperative instructions. Be specific about tools, formats, parameters.]

[If a decision point exists:]
**If [condition]:** [approach A]
**If [other condition]:** [approach B]

## [Step 2 Detail]

[Continue for each step.]

## Worked Example

**Input:** [Actual input from session, simplified if needed]

**Process:** [Brief trace of what the agent should do]

**Output:** [Actual output from session]

[If a second example covers a different branch or edge case, include it.]

## Common Mistakes

[Only if major corrections occurred during the session.]

**Don't [wrong approach].**
[Why it fails — drawn from teaching-mode discussion or repeated corrections.]
Instead, [correct approach].

[Repeat for each major anti-pattern. Aim for 1-3 entries. If none warranted, omit this section entirely.]
```

## Reasoning Log Template

The reasoning log is a separate reference file that documents *why* the skill looks the way it does. It is not loaded into context during normal skill use — it exists for revision sessions and for the user's reference.

```markdown
# Reasoning Log: [Skill Name]

## Session Context
- **Date**: [date]
- **Task**: [what the user was trying to accomplish]
- **Iterations**: [how many major revision cycles occurred]
- **Teaching mode episodes**: [count]

## Instruction Provenance

### [Instruction / Step N]
**Source**: [Which session events informed this instruction]
**Reasoning**: [Why this instruction is structured this way]
**Alternatives considered**: [What was tried and abandoned, if applicable]

### [Instruction / Step N+1]
...

## Corrections Encoded

### [Anti-pattern 1]
**Session event**: [What happened — agent did X, user corrected to Y]
**Root cause**: [Why the agent made this mistake]
**Teaching exchange**: [Brief summary of the teaching-mode discussion, if applicable]
**Encoded as**: [How this appears in the skill — anti-pattern entry, inline note, etc.]

### [Anti-pattern 2]
...

## Decisions Made During Skill Drafting

### [Decision: e.g., "Omitted step Z from workflow"]
**Rationale**: [Why this was left out — e.g., only appeared in one iteration, user indicated it was a one-off]

### [Decision: e.g., "Used approach A over approach B"]
**Rationale**: [Why — e.g., user explicitly preferred A after testing both]

## Revision History

### v1 (initial draft)
[Summary of what was produced]

### v1.1 (revision after user feedback)
[What changed and why]

[Continue for each revision cycle]
```

## Handling Ambiguity

If the session is ambiguous about any of these elements, flag it during the presentation phase rather than guessing. Prefer under-specifying the skill (with a note about the gap) over encoding a guess.

Common ambiguities:
- The user solved a problem but the approach was ad-hoc — unclear if it should be generalized
- Multiple approaches were tried and the user didn't explicitly prefer one
- The session ended mid-iteration without clear convergence

For each ambiguity, present it to the user as: "I wasn't sure about [thing]. The session showed [evidence A] and [evidence B]. Which should the skill encode?"

## Multi-Session Skills

If the user invokes this skill referencing a previously generated skill, treat it as a revision pass rather than a fresh creation. The procedure is:

1. Load the existing skill and its reasoning log
2. Analyze only the new session (you already have the old one encoded)
3. Identify conflicts between the existing skill and new session behavior
4. Propose targeted edits: what to add, remove, or modify
5. Preserve the existing reasoning log and append new entries

Surgical revision is almost always better than rewriting. The existing skill represents validated knowledge — only override it with strong evidence from the new session.
