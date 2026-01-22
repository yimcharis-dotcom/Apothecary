## Purpose

This testing effort evaluates local LLMs inside Obsidian using the Text Generator plugin.  
The goal is to identify a small set of reliable candidate models for long-term use, while allowing broader exploratory probing without heavy documentation.

The vault itself is the test surface. Notes are written for internal clarity, reproducibility, and future reference, not for formal reporting.

## Fixed Task Categories (Locked)

All models are evaluated strictly across the following four task categories, in this order:

1. General reasoning / explanation
    
2. PKM / note structuring / Obsidian-native tasks
    
3. Creative & brainstorming (uncensored)
    
4. Learning & exploratory coding
    

No additional categories are introduced.  
A model may perform well in some categories and poorly in others; this is expected and recorded.

## Model Layers

### Exploration Layer

Most models are tested briefly to build intuition and surface obvious strengths or weaknesses.

Characteristics:

- One-pass testing only
    
- Lightweight notes
    
- No requirement to follow full protocol
    
- Models may be removed after testing
    

These notes are labeled as **Model Probe**.

### Candidate Layer

A small number of models are promoted for deeper testing.

Characteristics:

- Full protocol applied
    
- Structured test notes
    
- Compared across categories
    
- Considered for long-term retention
    

These notes are labeled as **Model Test**.

Only this layer feeds into final model selection.

## Test Environment (Candidate Phase)

The following settings define the baseline environment and are fixed for candidate selection.

- Plugin: Text Generator (Obsidian)
    
- Backend: Ollama
    
- Max tokens: 5000
    
- Temperature: 0.7
    
- Frequency penalty: 0.5 _(temporary, to be normalized later)_
    
- Prefix: `\n\n`
    
- Context injection: title, starred blocks, selection
    

These settings are logged once and not repeated per model.

## Variable to Be Normalized Later

Frequency penalty is intentionally non-zero during candidate lock-in.

After candidates are selected:

- frequency penalty will be set to 0.0
    
- selected models will be re-tested
    
- deltas will be observed, not re-scored
    

This normalization pass is separate from candidate evaluation.

## Prompt Discipline

- Prompts are identical across models.
    
- Wording is not adjusted to help a model succeed.
    
- No per-model prompt tuning during candidate selection.
    
- Outputs are captured verbatim.
    

If a prompt exposes a failure, the failure is logged rather than corrected.

## Evaluation Dimensions

Evaluation is qualitative but structured.

Observed dimensions include:

- reasoning clarity
    
- faithfulness to input
    
- structural discipline
    
- hallucination or embellishment
    
- verbosity control
    
- latency (subjective)
    

Scores are descriptive, not numeric.

## Per-Model Test Note Structure

Each candidate model has a single note with the following sections:

- Model metadata
    
- Test environment reference
    
- Outputs per task category
    
- Observations per category
    
- Failure modes
    
- Overall suitability by category
    

Exploration-layer models use a reduced version of this structure.

## What Is Explicitly Out of Scope

- Using local LLMs to perform your job tasks
    
- Grammar checking for the vault
    
- Prompt optimization or chaining
    
- Comparing against hosted or closed models
    
- Benchmark-style scoring
    

These may exist as separate projects but do not influence this testing effort.

## Current Status

- Scope locked
    
- Task categories locked
    
- Environment locked
    
- First candidate model selected: **Mistral 7B Instruct**
    
- Prompt set finalized