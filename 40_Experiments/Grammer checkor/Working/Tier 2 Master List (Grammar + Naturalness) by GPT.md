
# Tier 2 Master List (Grammar + Naturalness)

 Tier 2 Master List
 Version: 2025-12-20
 Source scope: Cantonese L1 ESL (with comparative ESL cross-validation)
 Author: Charis project
### Grammar (Tier 2-G)

- **Article and countability errors** — Chan, A. Y. W. (2010). _“Advanced Cantonese ESL learners’ use of English articles.”_ _Second Language Research_, 26(2).
    
- **Preposition substitution and transitivity** — Yip, V. (1995). _Interlanguage and Learnability: From Chinese to English._
    
- **Tense–aspect inconsistency** — Collins, L. (2002). _“The role of L1 influence in the acquisition of temporal morphology.”_ _Language Learning_, 52(1).
    
- **Dummy subject omission** — Chan, A. Y. W. (2004). _“Syntactic transfer: Cantonese and English structures.”_ _International Review of Applied Linguistics_, 42(2).
    
- **Word-form and comparative errors** — Dulay & Burt (1974). _“Natural sequences in child second language acquisition.”_ _Language Learning_, 24(1).* (Foundational morphological framework.)
    

---

## Tier 2-G (Grammar)

| Linguistic label                | Operational tag                                                  | Linguistic reasoning                                                                    | Operational logic / core trigger                                                                     | Representative minimal pairs (3 per category)                                                                                                                                                                       | Reference / source                            |
| ------------------------------- | ---------------------------------------------------------------- | --------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------- |
| Article omission / overuse      | `Ø+singular-count-noun`, `the+generic-noun`                      | Cantonese classifier system lacks articles; omission / overuse with generics frequent.  | Detect noun phrases missing or redundantly using *a/an/the* by checking countability + definiteness. | *She is teacher.* → *She is a teacher.* / *I closed door.* → *I closed the door.* / *The life is hard.* → *Life is hard.*                                                                                           | Chan (2010) *Second Language Research* 26(2)  |
| Preposition substitution        | `wrong-prep+verb`, `redundant-prep`                              | Prepositions lexicalized differently in Cantonese; transfer yields wrong / extra items. | Compare verb–preposition pairs to licensed corpus frames; flag unlisted / redundant pairs.           | *He discussed about the issue.* → *He discussed the issue.* / *Different with others.* → *Different from others.* / *Enter to the room.* → *Enter the room.*                                                        | Yip (1995) *Interlanguage and Learnability*   |
| Tense–aspect inconsistency      | `verb-form<>temporal-cue`, `progressive+stative`                 | Aspect particles in Cantonese ≠ English tense; temporal mismatches typical.             | Match verb morphology to temporal adverbials; flag conflicts or progressive on statives.             | *I have seen him yesterday.* → *I saw him yesterday.* / *I am knowing the answer.* → *I know the answer.* / *When I arrived, he leaves already.* → *When I arrived, he had left already.*                           | Collins (2002) *Language Learning* 52(1)      |
| Countability confusion          | `plural+uncount-noun`, `sing-det+plural-noun`, `much+count-noun` | Classifier–noun mapping causes pluralization / quantifier errors.                       | Cross-check determiner + number features against noun’s lexical countability class.                  | *The equipments are broken.* → *The equipment is broken.* / *He gave me a good advice.* → *He gave me good advice.* / *He gave me an advice.* → *He gave me a piece of advice.*                                     | Chan (2010); Yip (1995)                       |
| Irregular plural error          | `noun-pl-form-error`                                             | Over-regularization of low-frequency irregular forms.                                   | Flag plural morphemes not in irregular lexicon (*childs, foots*).                                    | *Three childs are playing.* → *Three children are playing.* / *Many womans attended.* → *Many women attended.* / *Several mouses in the lab.* → *Several mice in the lab.*                                          | Dulay & Burt (1974) *Language Learning* 24(1) |
| Transitivity error              | `verb-arg-mismatch`                                              | Broader verb valency in Cantonese → object drop / doubling.                             | Compare complement pattern to verb valency database; flag missing / extra object.                    | *He explained me the problem.* → *He explained the problem to me.* / *She suggested to go home.* → *She suggested going home.* / *He recommended me to take the course.* → *He recommended that I take the course.* | Yip (1995)                                    |
| Dummy-subject omission / misuse | `Ø+it/there-subj`, `unneeded-dummy`                              | Topic-prominent L1 omits expletives or adds them unnecessarily.                         | Identify clauses needing *it/there* (existential, weather); flag omission / redundant insert.        | *Is raining outside.* → *It is raining outside.* / *Is a problem with the file.* → *There is a problem with the file.* / *There have many people.* → *There are many people.*                                       | Chan (2004) *IRAL* 42(2)                      |
| Word-form error                 | `POS-shift`, `deriv-morph-error`                                 | Incorrect derivation / part-of-speech assignment from morphological over-extension.     | Detect lexical forms incompatible with syntactic role or unattested derivation.                      | *She made a decide.* → *She made a decision.* / *He successed in the exam.* → *He succeeded in the exam.* / *It was a beautyful day.* → *It was a beautiful day.*                                                   | Dulay & Burt (1974)                           |
| Comparative error               | `double-marker`, `comp-connector-error`                          | Analytic comparison in Cantonese → redundant or ill-formed comparatives.                | Identify double markers (*more better*) or wrong connectors (*as tall than*).                        | *This one is more better.* → *This one is better.* / *She is taller than me is.* → *She is taller than I am.* / *He is as tall than his brother.* → *He is as tall as his brother.*                                 | Yip (1995)                                    |

## Tier 2-N (Naturalness)

| Linguistic label | Operational tag | Linguistic reasoning | Operational logic / core trigger | Representative minimal pairs (3 per category) | Reference / source |
|------------------|-----------------|----------------------|----------------------------------|------------------------------------------------|--------------------|
| Word-order interference | `non-canonical-order`, `adv-precedes-mainverb` | Topic–comment syntax in Cantonese causes fronting / adverb misplacement. | Parse dependency order; flag topicalized objects or pre-verbal adverbs without focus motivation. | *I very like it.* → *I like it very much.* / *Yesterday I very tired.* → *I was very tired yesterday.* / *This book I read yesterday.* → *I read this book yesterday.* | Odlin (1989) *Language Transfer* |
| Collocation error | `verb-noun-mismatch`, `adj-noun-mismatch`, `phrasal-replacement` | Lexical choice reflects L1 semantic association rather than native frequency. | Compute collocation association score (MI / LLR) vs native corpus; flag low-probability pairs. | *Do a mistake.* → *Make a mistake.* / *Heavy taste.* → *Strong taste.* / *Open the light.* → *Turn on the light.* | Nesselhauf (2005) *Collocations in a Learner Corpus* |
| Register mismatch | `inconsistent-register` | Cantonese pragmatic range differs; formal / informal mixing common. | Compare lexical items’ register vectors; flag large stylistic distance within context. | *Hey professor, I wanna ask you something.* → *Dear Professor, I would like to ask you something.* / *The results were kinda disappointing.* → *The results were somewhat disappointing.* / *We would be most obliged if you could hang out tonight.* → *We’d love to see you tonight.* | Gilquin & Granger (2011) *IJCL* 16(3) |
| Cohesion / coherence issue | `connector-misuse`, `redundant-linker` | Literal transfer creates redundant or contradictory linkers (*because so*). | Detect connector sequence violating logical templates; flag redundant or conflicting linkers. | *Because he was late, so we left.* → *Because he was late, we left.* / *Although it was raining, but we went out.* → *Although it was raining, we went out.* / *In the other side, the results were better.* → *On the other hand, the results were better.* | Hyland (2004) *Disciplinary Discourses* |

### Naturalness (Tier 2-N)

- **Word-order interference** — Odlin, T. (1989). _Language Transfer: Cross-Linguistic Influence in Language Learning._
    
- **Collocation error** — Nesselhauf, N. (2005). _Collocations in a Learner Corpus._
    
- **Register mismatch** — Gilquin, G., & Granger, S. (2011). _“From EFL to ESL: The acquisition of native-like collocational competence.”_ _International Journal of Corpus Linguistics_, 16(3).
    
- **Cohesion/coherence issues** — Hyland, K. (2004). _Disciplinary Discourses: Social Interactions in Academic Writing._
    

---

I can now compile these into a **full table** with four columns (Category | Reasoning | Operational logic | Reference) so you can track the link between Charis’s rules and external work.  
Would you like me to generate that table next?