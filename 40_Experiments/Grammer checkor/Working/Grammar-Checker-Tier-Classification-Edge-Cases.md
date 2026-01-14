# Grammar Checker: Tier Classification & Edge Cases

## What Qualifies as an Error?

**Mark these:**
- Grammar violations: wrong tense, missing articles, subject-verb disagreement
- Unnatural collocations: "do a mistake", "make research"
- Unclear constructions: ambiguous references, confusing structure
- Register mismatches: "hey" in formal audit, slang in professional docs
- Pragmatic risks: face-threatening language, inappropriate tone
- Naturalness issues: grammatically correct but unnatural to native speakers

**Don't mark these:**
- Standard British or American usage (both accepted)
  - Collective nouns: "team is/are", "data is/are"
  - Spelling: "colour/color", "organise/organize"
- Correct grammar: "boss's", "I'm", "team's"
- Stylistic choices: active vs passive (unless clarity suffers)

---

## Prescriptive vs Descriptive vs Naturalness

**[Prescriptive]**: Grammar or collocation violation

**[Descriptive]**: Register, tone, or pragmatic issue

**[Naturalness]**: Grammatically correct but unnatural to native speakers

---

## Tier Classification

**Tier 1** (_italics_[#.]) = Self-evident fix, no explanation
- Typos, missing apostrophes, sentence-initial caps
- Simple SVA (you just missed the plural)

**Tier 2** (***bold italics***[#.]) = Needs explanation
- Grammar: tense/aspect, mood errors, articles
- Collocations: "make research" vs "conduct research"
- Semantic issues: "Fascism" vs "fascism", "Internet" vs "internet"
- Register clashes, face-threatening phrases, pragmatic risks
- Naturalness: grammatically correct but unnatural constructions

---

## Edge Cases

### Error Span Boundaries

Mark the complete unit that needs correction:

**Wrong:** since ***your***[#.] inexperienced  
**Correct:** since ***your inexperienced***[#.] (pragmatic + grammar)

**Wrong:** on ***this***[#.] irregularities  
**Correct:** on ***this irregularities***[#.] (determiner-noun agreement)

### Adjacent vs Compound Errors

Mark separately when each error needs independent correction.

Mark as compound when corrections are interdependent—fixing one requires fixing the other.

---

## Reference Test Sentence

hey Dr. Smith, since he's junior, I propose he goes examine the equipments tomorrow.

**Annotated:**

_hey_[1.] Dr. Smith, ***since he's junior***[2.], I propose he ***goes***[3.] examine the ***equipments***[4.] tomorrow.

**Breakdown:**
- [1.] Tier 1: mechanical cap
- [2.] Tier 2 [Descriptive]: face-threatening
- [3.] Tier 2 [Prescriptive]: subjunctive mood
- [4.] Tier 2 [Prescriptive]: mass noun error
