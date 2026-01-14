# CHARIS Decision Checklist

This checklist captures every unresolved decision in your grammar checker. Answer each question to produce a finalized, implementation-ready spec.

---

## Section 1: Annotation Syntax

### 1.1 Number Format

**Question:** Should annotation numbers include a trailing period?

| Option | Example | Pros | Cons |
|--------|---------|------|------|
| **A: No period** | `[1]` `[2]` `[3]` | Cleaner visually | Your system prompt says period needed for parsing |
| **B: With period** | `[1.]` `[2.]` `[3.]` | Explicit sentence-final disambiguation | Slightly cluttered |

**Your current state:** System prompt uses `[#.]`, spec v 3.0 uses `[#]`

**Decision needed:** ☐ A / ☐ B

---

### 1.2 Tier 1 Markup Style

**Question:** What markdown format for Tier 1 errors?

| Option | Rendering | Example |
|--------|-----------|---------|
| **A: Single underscore** | _italics_ | `_hey_[1.]` |
| **B: Single asterisk** | *italics* | `*hey*[1.]` |

**Your current state:** All docs use underscore `_italics_`

**Decision needed:** ☐ A / ☐ B (or confirm A)

---

### 1.3 Tier 2 Markup Style

**Question:** What markdown format for Tier 2 errors?

| Option | Rendering | Example |
|--------|-----------|---------|
| **A: Triple asterisk** | ***bold italics*** | `***equipments***[2.]` |
| **B: Underscore + double asterisk** | _**bold italics**_ | `_**equipments**_[2.]` |
| **C: Double asterisk only** | **bold** | `**equipments**[2.]` |

**Your current state:** All docs use `***bold italics***`

**Decision needed:** ☐ A / ☐ B / ☐ C (or confirm A)

---

### 1.4 Annotation Placement

**Question:** Where does the annotation marker go relative to punctuation?

| Option | Example |
|--------|---------|
| **A: Before punctuation** | `the ***equipments***[2.], and...` |
| **B: After punctuation** | `the ***equipments,***[2.] and...` |
| **C: Punctuation outside markup** | `the ***equipments***[2.], and...` (same as A) |

**Decision needed:** ☐ A / ☐ B

---

## Section 2: Span Markup (Multi-Word Errors)

### 2.1 Span Syntax

**Question:** How do you mark errors spanning multiple words?

| Option | Example | Parsing Complexity |
|--------|---------|-------------------|
| **A: Wrap entire span** | `***your inexperienced***[2.]` | Low — clear boundaries |
| **B: Mark first + last** | `***your***...***inexperienced***[2.]` | Medium — needs pairing logic |
| **C: Bracket notation** | `***[your inexperienced]***[2.]` | Low — explicit grouping |
| **D: XML-style tags** | `<t2>your inexperienced</t2>[2.]` | High — but machine-parseable |

**Your current state:** Spec says "mark first and last word" (Option B) as interim, but no examples shown

**Decision needed:** ☐ A / ☐ B / ☐ C / ☐ D

---

### 2.2 Span Counting

**Question:** Does a multi-word span count as one error or multiple?

| Option | Behavior |
|--------|----------|
| **A: One error** | `***since he's junior***[2.]` = 1 T 2 instance |
| **B: Multiple errors** | Each word gets separate count |

**Your current state:** Edge Cases doc says "count as single Tier-2 instance"

**Decision needed:** ☐ A / ☐ B (or confirm A)

---

## Section 3: Tier 1 / Tier 2 Boundaries

### 3.1 Article Omission Classification

**Question:** When is missing article T 1 vs T 2?

| Option | Rule | Example |
|--------|------|---------|
| **A: Always T 1** | All article omissions are mechanical | "She is teacher" = T 1 |
| **B: Always T 2** | All article issues need interpretation | "She is teacher" = T 2 |
| **C: Context-dependent** | Simple omission = T 1; generic/transfer-related = T 2 | Need sub-rules |

**Your current state:** T 1 whitelist includes "Simple article omission" but T 2-G includes "Articles" — contradiction

**If Option C, specify the boundary rule:**

```
_______________________________________________
_______________________________________________
```

**Decision needed:** ☐ A / ☐ B / ☐ C

---

### 3.2 Subject-Verb Agreement Classification

**Question:** Is SVA always T 1?

| Option | Rule |
|--------|------|
| **A: Always T 1** | "He go" = T 1, no explanation needed |
| **B: Mostly T 1, some T 2** | Simple cases T 1; complex (e.g., collective nouns, existential there) = T 2 |

**Your current state:** T 1 whitelist includes "Subject-verb agreement" without qualification

**If Option B, specify exceptions:**

```
_______________________________________________
```

**Decision needed:** ☐ A / ☐ B

---

### 3.3 T 1 Promotion Rule

**Question:** Can a T 1 error be "promoted" to T 2?

| Option | Behavior |
|--------|----------|
| **A: No** | T 1 stays T 1 regardless of context |
| **B: Yes, with trigger** | If error may stem from L 1 transfer or semantic ambiguity, escalate |

**Your current state:** Not addressed in spec

**If Option B, what triggers promotion?**

```
_______________________________________________
```

**Decision needed:** ☐ A / ☐ B

---

## Section 4: Interpretive Labels

### 4.1 Collocation Label Assignment

**Question:** Are collocation errors [Prescriptive] or [Naturalness]?

| Option | Rule | Example |
|--------|------|---------|
| **A: Always Prescriptive** | Wrong collocation = grammar-level error | "make a photo" = [Prescriptive] |
| **B: Always Naturalness** | Collocations are about idiomaticity | "make a photo" = [Naturalness] |
| **C: Depends on severity** | Unacceptable pairing = Prescriptive; unusual but acceptable = Naturalness | Need sub-rules |

**Your current state:** System prompt says [Prescriptive], spec example shows [Naturalness]

**If Option C, specify the boundary:**

```
_______________________________________________
```

**Decision needed:** ☐ A / ☐ B / ☐ C

---

### 4.2 Register Mismatch Label

**Question:** What label for register/formality issues?

| Option | Label |
|--------|-------|
| **A: Descriptive** | Register is context-dependent, not "wrong" |
| **B: Naturalness** | Mismatch sounds unnatural |
| **C: Either, depending on severity** | Formal in casual = Descriptive; jarring clash = Naturalness |

**Your current state:** System prompt says [Descriptive], but T 2-N-Register exists under Naturalness track

**Decision needed:** ☐ A / ☐ B / ☐ C

---

### 4.3 Label Priority Conflicts

**Question:** When an error fits multiple labels, which wins?

**Your current system prompt priority:**
1. [Prescriptive] — grammar/collocation violations
2. [Descriptive] — register/tone/pragmatic when grammar correct
3. [Naturalness] — grammatically acceptable but non-native

**Is this priority correct?** ☐ Yes / ☐ No, revise to:

```
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________
```

---

## Section 5: Output Format

### 5.1 Section 2 vs Section 3 Distinction

**Question:** When do alternatives go in Section 2 (Explanations) vs Section 3 (Native-Speaker Alternatives)?

| Option | Rule |
|--------|------|
| **A: Section 2 = inline brief; Section 3 = full rewrites** | All T 2 errors get Section 2; only significant phrasing choices get Section 3 |
| **B: Section 2 = corrections; Section 3 = register variants** | Section 2 shows fix; Section 3 shows Casual/Neutral/Formal versions |
| **C: Merge them** | Combine into single "Alternatives" section |

**Your current state:** Both sections show alternatives, unclear when to use which

**Decision needed:** ☐ A / ☐ B / ☐ C

---

### 5.2 Section 3 Trigger

**Question:** When should Section 3 (Native-Speaker Alternatives) be provided?

| Option | Trigger |
|--------|---------|
| **A: Always** | Every response includes 2-3 rewrites |
| **B: Only for significant issues** | Skip for pure mechanical fixes |
| **C: Only when register varies** | Include only if Casual/Neutral/Formal differ meaningfully |

**Your current state:** Spec says "Provide 2-3 rewrites" without trigger condition

**Decision needed:** ☐ A / ☐ B / ☐ C

---

### 5.3 Explanation Block Format

**Question:** Confirm the exact format for Section 2 explanation blocks:

**Current template:**
```
[Label] Tag: T2-X-Category
→ Explanation: "quote" — what's wrong
→ Rule: principle
→ Impact: why it matters
→ Alternatives: 1-2 options
```

**Confirm or revise:**

☐ Confirmed as-is

☐ Revise to:
```
_______________________________________________
_______________________________________________
_______________________________________________
```

---

## Section 6: Edge Cases

### 6.1 Repeated Errors

**Question:** How to handle the same error appearing multiple times?

| Option | Behavior |
|--------|----------|
| **A: Annotate every instance** | Each occurrence gets its own `[#.]` |
| **B: Annotate first, note pattern** | First gets `[#.]`; subsequent marked but grouped in explanation |
| **C: Annotate first only** | Only first instance marked |

**Decision needed:** ☐ A / ☐ B / ☐ C

---

### 6.2 Adjacent Independent Errors

**Question:** When two errors are next to each other but unrelated, how to mark?

| Option | Example |
|--------|---------|
| **A: Separate markers** | `_hey_[1.] ***equipments***[2.]` |
| **B: Combined if touching** | `_hey_ ***equipments***[1-2.]` |

**Decision needed:** ☐ A / ☐ B (or confirm A)

---

### 6.3 Nested Errors

**Question:** When a T 1 error occurs inside a T 2 span, how to mark?

**Example:** "since your inexperienced" (T 1: your→you're, T 2: pragmatic/face-threatening)

| Option | Handling |
|--------|----------|
| **A: Mark T 2 only** | Higher tier takes precedence |
| **B: Mark both separately** | `since _your_[1.] ***inexperienced***[2.]` |
| **C: Mark T 2, note T 1 in explanation** | `***since your inexperienced***[2.]` with T 1 mentioned in Section 2 |

**Decision needed:** ☐ A / ☐ B / ☐ C

---

## Section 7: Configuration & Defaults

### 7.1 Default Strictness Behavior

**Question:** What does "Medium" strictness mean concretely?

| Setting | Behavior (define each) |
|---------|------------------------|
| **Low** | `_________________________________` |
| **Medium** | `_________________________________` |
| **High** | `_________________________________` |

---

### 7.2 Dialect Handling

**Question:** When input contains BrE in AmE mode (or vice versa), what happens?

| Option | Behavior |
|--------|----------|
| **A: Flag as error** | "colour" in AmE mode = T 1 or T 2 |
| **B: Note but don't correct** | Mention in output but don't mark |
| **C: Ignore dialect differences** | Accept both spellings regardless of setting |

**Decision needed:** ☐ A / ☐ B / ☐ C

---

## Section 8: Testing Protocol

### 8.1 [TEST] Footer Content

**Question:** Confirm what the `[TEST]` footer should include:

**Current list:**
- Tier 1 count: N
- Tier 2 count: N
- Tags (T 1): [tag: count,…]
- Tags (T 2): [tag: count,…]
- Types: Prescriptive / Descriptive / Naturalness breakdown
- Dialect / Register / Strictness settings

**Add anything?**

☐ Confirmed as-is

☐ Add:
```
_______________________________________________
```

---

## Summary: Quick Reference

After completing this checklist, fill in your decisions here:

| Decision | Your Choice |
|----------|-------------|
| 1.1 Number format | |
| 1.2 T 1 markup | |
| 1.3 T 2 markup | |
| 1.4 Annotation placement | |
| 2.1 Span syntax | |
| 2.2 Span counting | |
| 3.1 Article classification | |
| 3.2 SVA classification | |
| 3.3 T 1 promotion | |
| 4.1 Collocation label | |
| 4.2 Register label | |
| 4.3 Label priority | |
| 5.1 Section 2 vs 3 | |
| 5.2 Section 3 trigger | |
| 5.3 Explanation format | |
| 6.1 Repeated errors | |
| 6.2 Adjacent errors | |
| 6.3 Nested errors | |
| 7.1 Strictness definitions | |
| 7.2 Dialect handling | |
| 8.1 TEST footer | |

---

**Next step:** Go through each decision. I can help you think through any specific item if you're unsure — just tell me which numbers you want to discuss.