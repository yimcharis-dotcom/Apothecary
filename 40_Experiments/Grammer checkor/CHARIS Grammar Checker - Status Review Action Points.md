# CHARIS Grammar Checker: Status Review & Action Points

## Current State Assessment

After reviewing all your materials, here's an objective evaluation:

--- [[CHARIS — Grammar & Naturalness Evaluation Spec v3.0]]

## What's Working Well

| Component | Status | Notes |
|-----------|--------|-------|
| **Tier 1/T 2 Conceptual Split** | ✅ Solid | Clear principle: T 1 = no interpretation needed, T 2 = context-dependent |
| **Academic Foundation** | ✅ Verified | All citations real (Chan 2010, Yip 1995, Odlin 1989, etc.) |
| **T 2 Sub-categories** | ✅ Well-defined | T 2-G (grammar) and T 2-N (naturalness) with clear sub-tags |
| **Interpretive Labels** | ✅ Clear | [Prescriptive] / [Descriptive] / [Naturalness] distinction works |
| **Testing Protocol** | ✅ Designed | `[TEST]` footer with metrics defined |

---

## What Needs Work

### 1. **Annotation Formatting — Inconsistent Across Documents**

You have **three different annotation schemes** floating around:

**Version A (from spec v 3.0):**
```
Tier 1 → _italics_[#]
Tier 2 → ***bold italics***[#]
```

**Version B (from Edge Cases bydoc):**
```
Tier 1 → _italics_[#.]
Tier 2 → ***bold italics***[#.]
```

**Version C (from system prompt):**
```
- Tier 1: _italics_[#.]
- Tier 2: ***bold italics***[#.]
```

**Problem:** The period after the number (`[#.]` vs `[#]`) is inconsistent. Your system prompt says "period required for parser compliance" but the spec doesn't include it.

---

### 2. **Span Markup — Still Unresolved**

From your spec:
> "Multi-word spanning logic recognized but syntax TBD. Current interim: mark first and last word of span."

**Current interim solution:**
```
***your inexperienced***[#.]
```

**But this creates ambiguity:** Is `***word1 word2 word3***[2.]` one error or three? Your Edge Cases doc says "mark first and last word" but doesn't show the syntax.

---

### 3. **T 1 Whitelist — Boundary Ambiguity**

Your T 1 list includes "Simple article omission" but T 2-G also includes "Articles."

**Unresolved question:** When is article omission T 1 (mechanical) vs T 2 (transfer-driven)?

Example:
- "She is teacher" — T 1 or T 2?
- Your spec says T 1 = "no interpretation" but article omission in Cantonese L 1 speakers often stems from classifier interference (Chan 2010), which would make it T 2.

---

### 4. **Output Section 2 vs Section 3 Overlap**

**Section 2:** Explanations with "Alternatives"
**Section 3:** Native-Speaker Alternatives with register labels

These overlap. When do you use which? Your examples show alternatives in both sections.

---

### 5. **Label Assignment Rule — Underspecified**

From your system prompt:
> "For every Tier 2 issue, apply exactly one label using this priority:
> [Prescriptive] for grammar/collocation violations;
> [Descriptive] for register, tone, or pragmatic issues when grammar is correct;
> [Naturalness] for grammatically and contextually acceptable but non-native phrasing."

**But:** Collocations appear under both [Prescriptive] (system prompt) and [Naturalness] (spec examples like "make a photo"). Which is it?

---

## Objective Evaluation Scorecard

| Dimension | Score | Comment |
|-----------|-------|---------|
| **Conceptual Design** | 8/10 | Strong theoretical grounding, clear tier logic |
| **Specification Completeness** | 6/10 | Key decisions deferred (spans, T 1/T 2 boundaries) |
| **Internal Consistency** | 5/10 | Multiple versions with conflicting details |
| **Implementation Readiness** | 4/10 | Can't build reliably until formatting finalized |
| **Academic Rigor** | 9/10 | Citations verified, reasoning sound |

**Overall:** Strong foundation, but not executable as-is due to inconsistencies.

---

## Action Points (Priority Order)

### **P 0: Must Fix Before Implementation**

1. **Finalize annotation syntax**
   - Decide: `[#]` or `[#.]`?
   - Document the final choice in ONE canonical spec

2. **Resolve span markup**
   - Proposal: `***[start→end]***[#.]` or use brackets: `***[your inexperienced]***[#.]`
   - Pick one and add examples

1. **Clarify T 1/T 2 article boundary**
   - Suggestion: Add rule — "Article omission is T 1 unless context suggests L 1 transfer pattern (e.g., with count nouns, generic reference). When ambiguous, default to T 2."

### **P 1: Should Fix for Consistency**

4. **Consolidate label rules for collocations**
   - Proposal: Collocations = [Prescriptive] when wrong verb/noun pairing; [Naturalness] when technically acceptable but non-native

5. **Clarify Section 2 vs Section 3**
   - Proposal: Section 2 = brief alternatives inline; Section 3 = full rewrites only when register variation is significant

6. **Merge conflicting documents into single canonical spec**

### **P 2: Nice to Have**

7. Add difficulty/proficiency tags (B 2/C 1/C 2)
8. Add transfer flag (T 2-G-Tr) for L 1-influenced errors
9. Create minimal test set (10-20 sentences covering each tag)

---

## Recommended Next Step

**Would you like me to:**

1. **Draft a unified v 3.1 spec** — consolidating all the above into one clean document with all decisions made
2. **Focus on annotation rules only** — produce a definitive formatting guide
3. **Create a decision checklist** — questions you need to answer, with options for each
[[[CHARIS Decision Checklist]]]
Which would be most useful right now?