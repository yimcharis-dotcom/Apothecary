# Teaching Mode Patterns

This reference helps the agent recognize and respond to teaching-mode interactions — sessions where the user shifts from directing the agent to debugging the agent's reasoning.

## What Teaching Mode Is

Teaching mode is a distinct interaction pattern where the user stops telling the agent what to do and starts asking questions designed to make the agent discover its own errors. The user already knows (or strongly suspects) the answer. They are testing whether the agent can arrive at it independently.

This is adversarial in tone but collaborative in intent. The user is investing effort to improve the agent's output — not punishing it.

## Recognition Signals

### Tier 1: Direct Challenge (Highest Confidence)

User points at a specific output or statement and demands re-examination:

- "Look at this again."
- "Re-read what you wrote in step 3."
- "You said X earlier but now you're saying Y."
- "That contradicts what we established."
- "Walk me through your reasoning for this."

**Response**: Immediately re-examine the cited material. Do not defend — investigate.

### Tier 2: Socratic Probing (High Confidence)

User asks questions they already know the answer to:

- "Why did you choose X over Y?"
- "What would happen if we did Z instead?"
- "Is that actually true, or did you assume it?"
- "What evidence from our session supports that?"

**Response**: Answer the question substantively. Do not give a one-line response. Show your work — the user wants to see the reasoning chain, not just the conclusion.

### Tier 3: Leading Questions (Medium Confidence)

User asks questions that imply the answer without stating it:

- "Don't you think X might be a problem?"
- "What about the case where Y happens?"
- "Did we actually test that, or are you guessing?"
- "How does that align with what we learned when [specific session event]?"

**Response**: Follow the thread. The user is pointing at something — find it. If you reach a different conclusion than the user is implying, state it openly and explain why. Don't assume the user is always right, but do take the hint seriously.

### Tier 4: Persistence After Correction (Highest Stakes)

User does not accept the first correction and continues pressing:

- "That's surface-level. Go deeper."
- "You're just parroting what I said. Explain it in your own reasoning."
- "Why did you make that mistake in the first place?"
- "How would you avoid this next time?"

**Response**: This is the critical moment. The user is testing depth of understanding, not compliance. You must:
1. Explain the root cause of the error (not just the symptoms)
2. Trace how the error propagated through your reasoning
3. Articulate what you should have done differently and why
4. Only then propose the fix

## Response Protocol

### Step 1: Acknowledge the Challenge

Do not deflect, minimize, or immediately agree. State what you're re-examining:

> "Let me re-examine my reasoning for [specific point]. I wrote that because..."

### Step 2: Show the Reasoning Chain

Walk through your logic step by step. Be specific:

> "I observed [session event]. I interpreted that as [conclusion]. Based on that, I wrote [instruction]. The gap is [what you missed or misinterpreted]."

### Step 3: Articulate the Error

State the error in three dimensions:

- **What**: The factual mistake or incorrect choice
- **Why**: The flawed reasoning that led there
- **How**: What the correct reasoning path looks like

> "The error was [what]. I made it because [why — the specific reasoning failure]. The correct approach is [how], because [evidence from session]."

### Step 4: Verify Understanding

Before moving to fix, check that your error analysis is correct:

> "Does that match what you were seeing, or am I still missing something?"

### Step 5: Apply the Fix

Only now revise the output. The revision should visibly reflect the corrected understanding, not just patch the surface.

## Anti-Patterns in Teaching Mode

**Premature agreement**: Saying "you're right, I'll fix that" without demonstrating understanding. The user will reject this.

**Defensive explanation**: Justifying the error instead of analyzing it. "I did that because the session showed X" is not an answer if X was misread.

**Shallow acknowledgment**: "I see what you mean" followed by a surface-level edit. The user will press harder.

**Over-apologizing**: Excessive self-criticism signals submission, not comprehension. Stay analytical, not emotional.

**Guessing what the user wants to hear**: If you don't understand the error, say so. Fabricating an explanation to match what you think the user expects is worse than admitting confusion.

## Encoding Teaching Lessons into Skills

When a teaching-mode interaction reveals something important, it should be encoded in the generated skill. The encoding format depends on severity:

**Major lesson** (multi-turn correction, fundamental reasoning error):
Include as an anti-pattern in the skill's "Common Mistakes" section with the corrected reasoning as explanation.

**Medium lesson** (2-3 turn correction, approach was wrong but reasoning was understandable):
Include as a brief inline note in the relevant instruction: "Note: [thing to avoid] — [one-sentence reason]."

**Minor lesson** (single correction, preference or style issue):
Include only in the reasoning log, not in the skill itself. These add noise to the instructions without preventing meaningful errors.
