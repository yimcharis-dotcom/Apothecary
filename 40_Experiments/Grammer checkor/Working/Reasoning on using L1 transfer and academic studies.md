# Errors of ESL combined research studies, prior agent kinda tested it, its not reliable apparently, what is your rational?

## That’s a good question. When combining ESL error studies, several methodological inconsistencies make the results unreliable if used without filtering.
### Main reasons

1. **Heterogeneous corpora.** Studies differ in learners’ L1s, proficiency levels, and elicitation tasks. Error frequencies or categories often reflect sampling rather than linguistic reality.
    
2. **Non-standard annotation.** Each project defines “error” differently—some include stylistic issues, others exclude borderline forms. Aggregating them mixes incompatible criteria.
    
3. **Uneven inter-rater reliability.** Annotators’ judgments vary widely, especially on article use, prepositions, and collocation. Combined datasets amplify this variance.
    
4. **Different theoretical bases.** Some analyses are contrastive (L1-transfer focused), others SLA-based (developmental). When merged, their categories overlap or conflict.
    
### Practical rationale

	When building a system like Charis, exhaustive but noisy lists are less useful than _stable, interpretable clusters_. We use the literature to confirm known transfer zones, then filter by:

- consistency across at least two Cantonese-L1 or East-Asian L1 studies,
    
- clarity of linguistic rule or pedagogical value,
    
- frequency at C1 level (not only beginner interference).
    
# yeah sure, but do we know this linguistic reality would be proritised by ai across models? like T1 the terms of error types that are considered, AI friendy/parsable most of time are not the precise linguistic terminologies. If ai doesnt like seeing the technical terms, why do we expect that ai would respect this linguistic reality. if it makes sense

## The gap you’re describing is real. Current language models and NLP pipelines are not aligned with linguistic taxonomy—they learn operational rather than theoretical distinctions.

### How AI prioritizes “linguistic reality”

	Models prioritize **statistical regularity and contextual predictability**, not explicit grammar theory. They internalize probabilistic mappings between forms and meanings rather than rule-based categories like “transitivity” or “countability.” As a result, linguistic “truth” (e.g., article omission being tied to countability) only appears indirectly through frequency and co-occurrence patterns.

### Why that matters for Charis

	To build Tier 2 categories that both humans and AI can use:

	- You need **linguistic precision** for interpretability and explanation.
	    
	- You also need **AI-operational phrasing**—labels and features that align with model-visible cues (e.g., “missing determiner before singular count noun” instead of “article omission from countable context”).
	    
	
	So, the compromise is to design _dual-layer labels_:
	
	- **Human-facing label:** linguistically precise (“article omission: countability interference”).
	    
	- **Model-facing descriptor:** surface-parseable form (“Ø before singular countable noun”).
	    
	
	