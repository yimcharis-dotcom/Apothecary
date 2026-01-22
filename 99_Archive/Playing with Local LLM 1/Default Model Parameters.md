

## Default Model Parameters (What They Mean for Testing)

**Max tokens (5000)**  
This is the upper bound on generated output, not input. For local CPU models, 5000 is high and may introduce latency or truncation artifacts near context limits. For baseline testing, this is acceptable but should be logged explicitly.

**Temperature (0.7)**  
This controls randomness. 0.7 is a balanced default and suitable for the first baseline run across all four task categories. We will not change this during candidate selection.

**Frequency penalty (0.5)**  
This discourages repetition. This is non-default behavior and materially affects PKM structuring and summarization. We must treat this as part of the test environment, not a neutral setting.

**Timeout (300000 ms)**  
Five minutes. This effectively disables timeout for CPU inference. Log this once at environment level; it does not vary by model.

**Prefix (`\n\n`)**  
This is prepended to every generation. It can subtly affect formatting-sensitive PKM tasks. We will keep it unchanged and note it once.

## Custom Instructions (Generation Prompt Wrapper)

The following wrapper is active and must be treated as part of _every_ test:

- `Title: {{title}}`
    
- `Starred Blocks: {{starredBlocks}}`
    
- `{{tg_selection}}`
    

This means:

- The model always receives document title and starred blocks when present.
    
- Selection-based prompts are contextual, not raw text.
    

This is important for PKM / Obsidian-native tasks and must be stated explicitly in the test protocol.

## Template Settings (`{{context}}`)

The same structure appears again under Template Settings. This confirms that:

- Context injection is consistent between ad-hoc generation and template-driven generation.
    
- There is no hidden divergence between “generate text” and “generate from template.”
    

This is good. It simplifies comparisons.

## ext Generator Options (Operational Scope)

The enabled toggles define **what actions we can test**, not model behavior itself.

Enabled:

- generate-text
    
- generate-text-with-metadata
    
- insert-generated-text-from-template
    
- create-generated-text-from-template
    
- search-results-batch-generate-from-template
    
- show-modal-from-template
    
- open-template-as-tool
    

Disabled:

- insert-text-from-template
    
- create-text-from-template
    

Implication:  
We can test **single-note**, **template-driven**, and **batch-generation** flows later without changing settings. For now, we stay on single-note generation.

## What We Will Lock for the Baseline

For the first candidate (Mistral 7B Instruct), we lock:

- Max tokens: 5000
    
- Temperature: 0.7
    
- Frequency penalty: 0.5
    
- Prefix: `\n\n`
    
- Context injection: title + starred blocks + selection
    

These become part of the **environment header** in the test log and will not be repeated per model.