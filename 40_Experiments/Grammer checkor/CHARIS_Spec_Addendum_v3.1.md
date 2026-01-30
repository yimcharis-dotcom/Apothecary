# CHARIS — Spec Addendum v3.1

**Additions to Grammar & Naturalness Evaluation Spec v3.0**

---

## Section 9: Span Markup (Finalized)

*Replaces the "Pending Item" placeholder in v3.0*

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

### 9.3 Boundary Principle

> Mark the **minimal complete unit** that requires correction.

Include only words that must change together. Exclude surrounding correct text.

### 9.4 Span Decision Tree

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

### 9.5 Discontinuous Span Protocol

When error elements are separated by correct text:

1. Mark each segment with the same base number
2. Add lowercase letter suffix in reading order (a, b, c...)
3. Group explanation under the base number

**Example:**

```markdown
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

```markdown
***There have many people***[3.]

[3.] [Prescriptive] Tag: T2-G-DummySubject:wrong-choice
→ Explanation: "There have" incorrect; also missing article before "people"
→ Rule: Existential "there" requires "are" + quantified noun phrase
→ Impact: Ungrammatical clause
→ Alternatives: "There are many people" / "Many people are there"
```

### 9.7 Full Annotated Example

**Input:**
```
hey Dr. Smith, since he's junior, I propose he goes examine the equipments yesterday.
```

**Annotated Output:**
```markdown
_hey_[1.] Dr. Smith, ***since he's junior***[2.], I propose he ***goes***[3.] examine the ***equipments***[4.] ***yesterday***[5.].
```

**With discontinuous tense error variant:**
```markdown
_hey_[1.] Dr. Smith, I ***have***[2a.] seen him ***yesterday***[2b.], and the ***equipments***[3.] are broken.
```

---

## Section 11: Tag Registry

*New section — standardizes tag naming across all CHARIS components*

### 11.1 Tag Structure

```
T2-G-Articles:omission
│  │    │        └── Pattern (operational trigger)
│  │    └── Subcategory (linguistic domain)
│  └── G = Grammar, N = Naturalness
└── Tier level
```

**Format:** `Tier-Category-Subcategory:pattern`

- Tier 1 tags use simple labels: `cap`, `apostrophe`, `typo`, `spacing`, `sva`, `fragment`, `run-on`
- Tier 2 tags use the hierarchical format above

### 11.2 Tier 1 Tags (Closed Set)

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

### 11.3 Tier 2-G Tags (Grammar)

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

### 11.4 Tier 2-N Tags (Naturalness)

| Parent Tag | Sub-patterns | Trigger Description |
|------------|--------------|---------------------|
| **T2-N-WordOrder** | `:topicalization` | L1-influenced object fronting |
| | `:adverb-placement` | Non-native adverb position |
| | `:focus-structure` | Unnatural information structure |
| **T2-N-Collocation** | `:verb-noun` | *do a mistake, make research* |
| | `:adj-noun` | *heavy taste, strong wind* (wrong pair) |
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

### 11.5 Migration Table

*Maps old operational tags from Master List to new standardized tags*

| Old Operational Tag | New Standardized Tag |
|---------------------|---------------------|
| `Ø+singular-count-noun` | `T2-G-Articles:omission` |
| `the+generic-noun` | `T2-G-Articles:overuse` |
| `wrong-prep+verb` | `T2-G-Prepositions:substitution` |
| `redundant-prep` | `T2-G-Prepositions:redundant` |
| `verb-form<>temporal-cue` | `T2-G-TenseAspect:tense-adverb-conflict` |
| `progressive+stative` | `T2-G-TenseAspect:stative-progressive` |
| `plural+uncount-noun` | `T2-G-Countability:plural-mass` |
| `sing-det+plural-noun` | `T2-G-Countability:det-noun-mismatch` |
| `much+count-noun` | `T2-G-Countability:quantifier-error` |
| `noun-pl-form-error` | `T2-G-IrregularPlural:over-regularization` |
| `verb-arg-mismatch` | `T2-G-Transitivity:valency-frame` |
| `Ø+it/there-subj` | `T2-G-DummySubject:omission` |
| `unneeded-dummy` | `T2-G-DummySubject:redundant` |
| `POS-shift` | `T2-G-WordForm:pos-shift` |
| `deriv-morph-error` | `T2-G-WordForm:derivation-error` |
| `double-marker` | `T2-G-Comparatives:double-marker` |
| `comp-connector-error` | `T2-G-Comparatives:connector-error` |
| `non-canonical-order` | `T2-N-WordOrder:topicalization` |
| `adv-precedes-mainverb` | `T2-N-WordOrder:adverb-placement` |
| `verb-noun-mismatch` | `T2-N-Collocation:verb-noun` |
| `adj-noun-mismatch` | `T2-N-Collocation:adj-noun` |
| `phrasal-replacement` | `T2-N-Collocation:phrasal` |
| `inconsistent-register` | `T2-N-Register:formality-clash` |
| `connector-misuse` | `T2-N-Cohesion:connector-misuse` |
| `redundant-linker` | `T2-N-Cohesion:redundant-linker` |

### 11.6 Explanation Block Format (Updated)

Each Tier-2 explanation must follow this structure:

```markdown
[Label] Tag: {Full-Tag}
→ Explanation: {What's wrong}
→ Rule: {The governing principle}
→ Impact: {Consequence for reader/communication}
→ Alternatives: {2-3 corrections with context}
```

**Labels:** `[Prescriptive]` | `[Descriptive]` | `[Naturalness]`

**Example:**

```markdown
[Prescriptive] Tag: T2-G-TenseAspect:tense-adverb-conflict
→ Explanation: "have seen" conflicts with "yesterday"
→ Rule: Present perfect requires non-specific or present-relevant time
→ Impact: Temporal contradiction; confuses timeline
→ Alternatives: "I saw him yesterday" / "I have seen him before"
```

---

## Section 7: Testing Footer (Updated)

*Replaces Section 7 in v3.0 to reflect new tag format*

When `[TEST]` appears in the input, append:

```markdown
Testing Summary:
- Tier 1 count: {N}
- Tier 2 count: {N}
- Tags (T1): [{tag}:{count}, ...]
- Tags (T2): [{full-tag}:{count}, ...]
- Types: Prescriptive:{N} / Descriptive:{N} / Naturalness:{N}
- Dialect / Register / Strictness: {AmE|BrE|Other} / {Casual|Neutral|Formal} / {Low|Med|High}
- Spans: Contiguous:{N} / Discontinuous:{N}
```

**Example:**

```markdown
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

## Appendix A: Quick Reference Card

### Markup At-a-Glance

| What | Syntax |
|------|--------|
| Tier 1 single | `_word_[#.]` |
| Tier 1 span | `_word word_[#.]` |
| Tier 2 single | `***word***[#.]` |
| Tier 2 span | `***word word***[#.]` |
| Discontinuous | `***word***[#a.] ... ***word***[#b.]` |

### Tag Format

```
T2-{G|N}-{Subcategory}:{pattern}
```

### Decision: Tier 1 or Tier 2?

> **Tier 1:** "Can I fix this without knowing what the writer meant?"
> - YES → Tier 1
> - NO → Tier 2

### Decision: Compound or Separate?

> **Compound:** "Does fixing error A force me to also fix error B?"
> - YES → Single span `***A B***[#.]`
> - NO → Separate spans `***A***[#.] ***B***[#+1.]`

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| v3.0 | — | Initial spec release |
| v3.1 | 2025-01-30 | Added Section 9 (Span Markup), Section 11 (Tag Registry), updated Section 7 (Testing Footer) |
