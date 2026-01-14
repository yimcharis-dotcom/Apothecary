## 🧩 Assurance: Grammar Checking Integrity

Your concern is correct — we must not let expanded naturalness checks blur grammatical accuracy.  
Here’s how the new structure preserves both functions:

| Mechanism                        | Protection                                                                                                                                    |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **Tier 2-G remains intact**      | Core grammar checks (articles, prepositions, tense/aspect, etc.) are untouched and remain the primary source for grammatical error detection. |
| **Tier 2-N uses dual-role tags** | Tags like `T2-N-StructureBridge` or `T2-N-Cohesion` handle grammar-linked naturalness without re-labeling them as pure naturalness errors.    |
| **Severity differentiation**     | Grammar-critical = Tier 2-G; stylistically or rhythmically awkward = Tier 2-N (marked lower severity in testing).                             |
| **Independent scoring**          | `[TEST]` footer keeps separate counts for T2-G and T2-N tags, so grammar precision metrics are not diluted.                                   |
🔹 Tier 2-N Refinement Plan (v2.1)

| Sub-Track                                     | Function                                                                                                                                  | Scope                 | Diagnostic Basis                                   |
| --------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | --------------------- | -------------------------------------------------- |
| **T2-N-WordOrder**                            | Ensures syntactic flow natural to L1 English users                                                                                        | Grammar + rhythm      | Checks adverb placement, topicalization, inversion |
| **T2-N-Collocation**                          | Validates native verb–noun / adj–noun combinations                                                                                        | Naturalness           | Collocation lists, idiom norms                     |
| **T2-N-Register**                             | Ensures vocabulary–tone match                                                                                                             | Naturalness           | Formality and tone cues                            |
| **T2-N-Cohesion**                             | Monitors discourse connectors, redundancy                                                                                                 | Grammar + Naturalness | Conjunction and reference patterns                 |
| **T2-N-Idiomaticity**                         | Detects literal or L1-transfer renderings                                                                                                 | Naturalness           | Canonical expression sets                          |
| **T2-N-StructureBridge** _(new bridging tag)_ | Handles cases that are **grammatically** permissible but **structurally** non-native (e.g., dummy subject misuse, missing complementizer) | Grammar + Naturalness | Syntax templates from Tier 2-G overlap             |
🔹 Behavioral Adjustments

|Component|Old Behavior|New Behavior|
|---|---|---|
|**Tier 2-N Activation**|Triggered only when phrasing obviously unidiomatic|Runs for _every_ sentence; passes if native-like|
|**Tier 2-N Tagging**|Optional descriptive tag|Mandatory tag header using `[Pvd vN] Tag:`|
|**Testing Footer**|Counted tags inferred heuristically|Tag counts parsed explicitly from header|
|**Cross-Model Scripts**|Parsed by label text|Anchored via `[Pvd vN]` token for deterministic parsing|