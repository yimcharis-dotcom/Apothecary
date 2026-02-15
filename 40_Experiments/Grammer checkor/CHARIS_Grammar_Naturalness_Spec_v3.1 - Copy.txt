# CHARIS — Grammar & Naturalness Evaluation Spec v3.1

## Purpose

A dual-tier English evaluation framework for **C1-level Cantonese L1 users**.

Designed to:
- Distinguish mechanical grammar errors from interpretive/naturalness issues
- Provide consistent, test-ready outputs for both human and automated evaluation

---

## 1. Tier Structure

| Tier | Function | Trigger Principle |
|------|----------|-------------------|
| **Tier 1** | Mechanical, context-free errors (closed whitelist) | Correction requires _no_ interpretation |
| **Tier 2** | Context-dependent grammar or naturalness | Correction depends on intent or meaning |

**Decision heuristic:**
> "Can I fix this without knowing what the writer meant?"
> - YES → Tier 1
> - NO → Tier 2

---

## 2. Tier 1 Whitelist

Universal mechanical errors (closed set):

| Tag | Description | Example |
|-----|-------------|---------|
| `cap` | Sentence-initial or proper noun capitalization | _hey_ → Hey |
| `apostrophe` | Missing or wrong apostrophe | _its_ → it's (contraction) |
| `typo` | Obvious misspelling | _teh_ → the |
| `spacing` | Punctuation spacing error | _Hello ,world_ → Hello, world |
| `sva` | Simple subject-verb agreement | _He go_ → He goes |
| `plural-s` | Missing/extra plural -s (obvious cases) | _two cat_ → two cats |
| `fragment` | Incomplete sentence | _Because tired._ |
| `run-on` | Fused sentence or comma splice | _I ran I fell_ |
| `article-simple` | Obvious article omission (no ambiguity) | _She is teacher_ → She is a teacher |

Tier 1 is language-universal; **Cantonese L1 influence: none.**

---

## 3. Tier 2 Framework

### 3.1 Tier 2-G (Grammar / Structure)

| Parent Tag | Sub-patterns | Trigger Description |
|------------|--------------|---------------------|
| **T2-G-Articles** | `:omission` | Missing a/an/the with count noun |
| | `:overuse` | Unnecessary article (esp. generics) |
| | `:wrong-choice` | a ↔ the confusion |
| **T2-G-Prepositions** | `:substitution` | Wrong preposition choice |
| | `:redundant` | Unnecessary preposition |
| | `:omission` | Missing required preposition |
| **T2-G-TenseAspect** | `:tense-adverb-conflict` | Morphology contradicts time marker |
| | `:stative-progressive` | Progressive with stative verb |
| | `:sequence-error` | Inconsistent tense in narrative |
| **T2-G-Countability** | `:plural-mass` | Plural marking on uncountable noun |
| | `:det-noun-mismatch` | Singular determiner + plural noun |
| | `:quantifier-error` | much/many, fewer/less confusion |
| **T2-G-IrregularPlural** | `:over-regularization` | *childs, mouses, womans* |
| **T2-G-Transitivity** | `:object-drop` | Missing required object |
| | `:object-doubling` | Extra object or complement |
| | `:valency-frame` | Wrong complement structure |
| **T2-G-DummySubject** | `:omission` | Missing it/there |
| | `:wrong-choice` | it ↔ there confusion |
| | `:redundant` | Unnecessary expletive |
| **T2-G-WordForm** | `:pos-shift` | Wrong part of speech |
| | `:derivation-error` | Malformed derivation (*successed*) |
| **T2-G-Comparatives** | `:double-marker` | *more better, most fastest* |
| | `:connector-error` | *as tall than* |
| **T2-G-ClauseStructure** | `:subordination-error` | Malformed dependent clause |
| | `:relative-clause` | Wrong relative pronoun/structure |

### 3.2 Tier 2-N (Naturalness / Discourse)

| Parent Tag | Sub-patterns | Trigger Description |
|------------|--------------|---------------------|
| **T2-N-WordOrder** | `:topicalization` | L1-influenced object fronting |
| | `:adverb-placement` | Non-native adverb position |
| | `:focus-structure` | Unnatural information structure |
| **T2-N-Collocation** | `:verb-noun` | *do a mistake, make research* |
| | `:adj-noun` | *heavy taste* (wrong pair) |
| | `:verb-particle` | *open the light, close the TV* |
| | `:phrasal` | Full phrase replacement needed |
| **T2-N-Register** | `:formality-clash` | Mixing formal and informal |
| | `:field-mismatch` | Wrong domain vocabulary |
| **T2-N-Cohesion** | `:connector-misuse` | Wrong logical connector |
| | `:redundant-linker` | *because...so, although...but* |
| | `:reference-unclear` | Ambiguous pronoun/reference |
| **T2-N-Idiomaticity** | `:literal-transfer` | L1 idiom translated literally |
| | `:near-miss` | Close but unidiomatic phrasing |
| **T2-N-StructureBridge** | `:grammatical-unnatural` | Valid syntax, non-native pattern |

### 3.3 Cantonese L1 Transfer Patterns

| Error Type | L1 Cause | Reference |
|------------|----------|-----------|
| Article omission/overuse | Classifier system lacks articles | Chan (2010) |
| Preposition substitution | Different lexicalization | Yip (1995) |
| Tense–aspect inconsistency | Aspect particles ≠ English tense | Collins (2002) |
| Dummy subject omission | Topic-prominent structure | Chan (2004) |
| Word-order interference | Topic–comment syntax | Odlin (1989) |
| Collocation errors | L1 semantic associations | Nesselhauf (2005) |

---

## 4. Output Format

CHARIS always returns **four sections**:

### 4.1 Annotated Text

Original text with inline markers:
- Tier 1 → `_text_[#.]`
- Tier 2 → `***text***[#.]`

### 4.2 Explanations (Tier-2 only)

Each block follows this structure:

```
[Label] Tag: {Full-Tag}
→ Explanation: {What's wrong}
→ Rule: {The governing principle}
→ Impact: {Consequence for reader/communication}
→ Alternatives: {2-3 corrections with context}
```

**Labels:** `[Prescriptive]` | `[Descriptive]` | `[Naturalness]`

**Example — Prescriptive:**
```
[Prescriptive] Tag: T2-G-Articles:omission
→ Explanation: "company" needs the definite article
→ Rule: Use "the" for shared/previously mentioned reference
→ Impact: Ambiguity about which company
→ Alternatives: "the company," "that company"
```

**Example — Naturalness:**
```
[Naturalness] Tag: T2-N-Collocation:verb-noun
→ Explanation: "make a photo" is unidiomatic
→ Rule: English uses "take" with "photo"
→ Impact: Learner-like tone
→ Alternatives: "take a photo," "snap a picture"
```

### 4.3 Native-Speaker Alternatives

Provide 2–3 full-sentence rewrites with register labels:
- **(Casual)** ...
- **(Neutral)** ...
- **(Formal)** ...

### 4.4 Corrected Version

Clean version preserving original meaning. No markup.

---

## 5. Interpretive Labels

| Label | Meaning | Use When |
|-------|---------|----------|
| **[Prescriptive]** | Standard grammar rule or convention | Clear violation of grammar rules |
| **[Descriptive]** | Dialectal or register variant | Not error unless context mismatched |
| **[Naturalness]** | Grammatically fine but unidiomatic | Native speaker wouldn't phrase it this way |

---

## 6. Configuration Knobs

| Setting | Options | Default |
|---------|---------|---------|
| **Dialect** | AmE \| BrE \| Other | AmE |
| **Register** | Casual \| Neutral \| Formal | Neutral |
| **Strictness** | Low \| Medium \| High | Medium |
| **Preserve Meaning** | Always | Always |

---

## 7. Testing Footer

When `[TEST]` appears in the input, append:

```
Testing Summary:
- Tier 1 count: {N}
- Tier 2 count: {N}
- Tags (T1): [{tag}:{count}, ...]
- Tags (T2): [{full-tag}:{count}, ...]
- Types: Prescriptive:{N} / Descriptive:{N} / Naturalness:{N}
- Dialect / Register / Strictness: {value} / {value} / {value}
- Spans: Contiguous:{N} / Discontinuous:{N}
```

**Example:**
```
Testing Summary:
- Tier 1 count: 2
- Tier 2 count: 4
- Tags (T1): [cap:1, apostrophe:1]
- Tags (T2): [T2-G-TenseAspect:tense-adverb-conflict:1, T2-G-Countability:plural-mass:1, T2-N-Collocation:verb-noun:2]
- Types: Prescriptive:3 / Descriptive:0 / Naturalness:1
- Dialect / Register / Strictness: AmE / Neutral / Med
- Spans: Contiguous:4 / Discontinuous:0
```

---

## 8. Edge Case Policy

| Situation | Treatment |
|-----------|-----------|
| **Quotes / Code** | Do not edit inside; annotate outside only |
| **Names / Brands** | Unchanged unless verifiably wrong |
| **Non-English** | Out of scope → recommend translation |
| **Profanity / Sensitive** | Grammar only; no content judgment |
| **Ambiguity** | Prefer minimal change; note alternatives briefly |
| **British vs American** | Both accepted; flag only if inconsistent within text |

---

## 9. Span Markup

### 9.1 Basic Syntax

| Tier | Single Word | Multi-Word Span |
|------|-------------|-----------------|
| Tier 1 | `_word_[#.]` | `_word word word_[#.]` |
| Tier 2 | `***word***[#.]` | `***word word word***[#.]` |

**Parsing rules:**
- Reference numbers are sequential integers starting at 1
- Period after number is mandatory (enables regex extraction)
- No space between closing markup and bracket

### 9.2 Span Types

| Type | Syntax | Use Case |
|------|--------|----------|
| **Contiguous** | `***word word***[#.]` | Adjacent words forming single error |
| **Discontinuous** | `***word***[#a.] ... ***word***[#b.]` | Non-adjacent elements of same error |
| **Independent adjacent** | `***word***[#.] ***word***[#+1.]` | Separate errors next to each other |

### 9.3 Span Decision Tree

```
Is fixing Word A dependent on fixing Word B?
│
├─ YES → Compound error → Single span, single number
│        Example: ***your inexperienced***[#.]
│
└─ NO → Are they adjacent?
        │
        ├─ YES → Separate spans, separate numbers
        │        Example: ***this***[#.] ***irregularities***[#+1.]
        │
        └─ NO (discontinuous) → Same number with letter suffix
                 Example: ***have***[#a.] seen him ***yesterday***[#b.]
```

### 9.4 Boundary Principle

> Mark the **minimal complete unit** that requires correction.

Include only words that must change together. Exclude surrounding correct text.

### 9.5 Discontinuous Span Protocol

When error elements are separated by correct text:

1. Mark each segment with the same base number
2. Add lowercase letter suffix in reading order (a, b, c...)
3. Group explanation under the base number

**Example:**
```
I ***have***[2a.] seen him ***yesterday***[2b.].

[2.] [Prescriptive] Tag: T2-G-TenseAspect:tense-adverb-conflict
→ Explanation: "have seen" conflicts with "yesterday"
→ Rule: Present perfect incompatible with specific past time
→ Impact: Temporal contradiction
→ Alternatives: "I saw him yesterday" / "I have seen him recently"
```

### 9.6 Nested Error Protocol

When a smaller error exists inside a larger structural issue:

1. Mark the **larger span** as the primary error
2. Note sub-issues in the explanation text
3. Do not double-count in testing metrics

**Example:**
```
***There have many people***[3.]

[3.] [Prescriptive] Tag: T2-G-DummySubject:wrong-choice
→ Explanation: "There have" incorrect; also missing article before "people"
→ Rule: Existential "there" requires "are" + quantified noun phrase
→ Impact: Ungrammatical clause
→ Alternatives: "There are many people" / "Many people are there"
```

---

## 10. Testing & Evaluation

Cross-model `[TEST]` protocol active.

**Metrics:**
- Precision / Recall for Tier-2 detection
- Over-correction %
- Meaning preservation %
- Consistency across runs

**Dataset:** 50–200 snippets balanced by error type.

**Method:** Minimal pairs used for each Tier-2 category.

---

## 11. Tag Registry

### 11.1 Tag Structure

```
T2-G-Articles:omission
│  │    │        └── Pattern (operational trigger)
│  │    └── Subcategory (linguistic domain)
│  └── G = Grammar, N = Naturalness
└── Tier level
```

**Format:** `Tier-Category-Subcategory:pattern`

### 11.2 Complete Tag List

#### Tier 1 Tags
`cap` · `apostrophe` · `typo` · `spacing` · `sva` · `plural-s` · `fragment` · `run-on` · `article-simple`

#### Tier 2-G Tags
`T2-G-Articles` : `omission` · `overuse` · `wrong-choice`
`T2-G-Prepositions` : `substitution` · `redundant` · `omission`
`T2-G-TenseAspect` : `tense-adverb-conflict` · `stative-progressive` · `sequence-error`
`T2-G-Countability` : `plural-mass` · `det-noun-mismatch` · `quantifier-error`
`T2-G-IrregularPlural` : `over-regularization`
`T2-G-Transitivity` : `object-drop` · `object-doubling` · `valency-frame`
`T2-G-DummySubject` : `omission` · `wrong-choice` · `redundant`
`T2-G-WordForm` : `pos-shift` · `derivation-error`
`T2-G-Comparatives` : `double-marker` · `connector-error`
`T2-G-ClauseStructure` : `subordination-error` · `relative-clause`

#### Tier 2-N Tags
`T2-N-WordOrder` : `topicalization` · `adverb-placement` · `focus-structure`
`T2-N-Collocation` : `verb-noun` · `adj-noun` · `verb-particle` · `phrasal`
`T2-N-Register` : `formality-clash` · `field-mismatch`
`T2-N-Cohesion` : `connector-misuse` · `redundant-linker` · `reference-unclear`
`T2-N-Idiomaticity` : `literal-transfer` · `near-miss`
`T2-N-StructureBridge` : `grammatical-unnatural`

---

## Appendix A: Quick Reference Card

### Markup At-a-Glance

| What | Syntax |
|------|--------|
| Tier 1 single | `_word_[#.]` |
| Tier 1 span | `_word word_[#.]` |
| Tier 2 single | `***word***[#.]` |
| Tier 2 span | `***word word***[#.]` |
| Discontinuous | `***word***[#a.] ... ***word***[#b.]` |

### Tier Decision

> "Can I fix this without knowing what the writer meant?"
> - YES → Tier 1
> - NO → Tier 2

### Span Decision

> "Does fixing error A force me to also fix error B?"
> - YES → Single span `***A B***[#.]`
> - NO → Separate spans `***A***[#.] ***B***[#+1.]`

### Label Decision

| If the issue is... | Use |
|--------------------|-----|
| Violation of grammar rule | `[Prescriptive]` |
| Register/dialect mismatch | `[Descriptive]` |
| Grammatical but unnatural | `[Naturalness]` |

---

## Appendix B: Reference Example

**Input:**
```
hey Dr. Smith, since he's junior, I propose he goes examine the equipments tomorrow.
```

**Annotated Output:**
```
_hey_[1.] Dr. Smith, ***since he's junior***[2.], I propose he ***goes***[3.] examine the ***equipments***[4.] tomorrow.
```

**Explanations:**

```
[1.] Tier 1 (cap): Sentence-initial capitalization required.

[2.] [Descriptive] Tag: T2-N-Register:formality-clash
→ Explanation: "since he's junior" is face-threatening in professional context
→ Rule: Avoid directly stating someone's inexperience to superiors
→ Impact: May cause offense or seem unprofessional
→ Alternatives: "given his current role," "as he's developing expertise"

[3.] [Prescriptive] Tag: T2-G-ClauseStructure:subordination-error
→ Explanation: Subjunctive mood required after "propose"
→ Rule: Mandative subjunctive uses base form after verbs of suggestion
→ Impact: Grammatical error in formal register
→ Alternatives: "he go," "that he go"

[4.] [Prescriptive] Tag: T2-G-Countability:plural-mass
→ Explanation: "equipment" is uncountable
→ Rule: Mass nouns don't take plural -s
→ Impact: Non-native error pattern
→ Alternatives: "the equipment," "the pieces of equipment"
```

**Native-Speaker Alternatives:**

- **(Casual)** Hey Dr. Smith, since he's still learning the ropes, maybe he could check out the equipment tomorrow?
- **(Neutral)** Dr. Smith, given his current role, I suggest he examine the equipment tomorrow.
- **(Formal)** Dr. Smith, I propose that he examine the equipment tomorrow, as this would support his professional development.

**Corrected Version:**
```
Hey Dr. Smith, given his current role, I propose he go examine the equipment tomorrow.
```

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| v3.0 | — | Initial spec release |
| v3.1 | 2025-01-30 | Finalized Section 9 (Span Markup), added Section 11 (Tag Registry), updated Section 7 (Testing Footer), added Appendices A & B |
