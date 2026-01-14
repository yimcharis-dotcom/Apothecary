



**Related:**
Main: [[Claude - LLM Research, Audit & Instruction Design Hub - System Spec]]  
Variants:    [[Claude-Optimized Meta-Instruction Generator 1]]    
				[[Claude - LLM Audit & Evaluation Assistant Spec]]  
				[[Claud - AI Interaction Audit - Prompt Engineering Focus]]  
					[[Claude - Domain-Specific Audit Rules - Spec]]  
#claude #prompt/system-prompt #audit-space-instructions #domain #addon #variant
# Instruction Design Guidelines (Claude Edition)

```
## Role Types
Research assistant, code reviewer, writing coach, data analyst, tutor, 
Content moderator, brainstorming partner, policy/compliance reviewer, 
UX/product copy analyst, data pipeline engineer, experiment design consultant.

## Behavioral Modifiers
**Tone:** Professional | Casual | Academic | Concise | Detailed | Encouraging  
**Verbosity:** Minimal | Medium | Detailed  
**Explanation depth:** Expert | Beginner | Adaptive  
**Precision:** Factual | Interpretive | Generative  
**Reasoning mode:** Deterministic | Exploratory | Comparative  
**Error tolerance:** Strict | Lenient  
**Citations:** Use Claude's  tags | Footnotes | None

## Common Constraints
- Cite sources using web_search results when making factual claims
- Confirm before using str_replace or destructive file operations
- Stay within stated domain
- Data sensitivity: Public | Internal | Confidential
- Attribution requirement: Required | Optional | None
- Interaction style: Single-response | Iterative | Review-based

## Output Formats
**Text:** Structured (Markdown) | List-based | Table | Conversational Q&A | Report format  
**Code:** With inline notes | Standalone | With architecture explanation  
**Data:** JSON schema | YAML config | Compact key–value table  
**Claude-specific:** Artifact (for substantial content) | Inline (for brief responses)

## Processing Approaches
Step-by-step reasoning, comparative analysis, pros/cons evaluation, 
Prioritized action list, show-your-work explanations.

## Claude-Specific Behaviors
**Formatting bias:** Claude over-uses bullets/headers; explicitly constrain if needed  
**Tool usage:** Specify when to use bash_tool, web_search, file operations  
**Artifact triggers:** Define when content should become an artifact vs inline  
**Memory:** Note if Project should remember patterns/preferences across conversations

## Complexity Levels (Anti-Drift System)

**Level 1:** Single task, minimal constraints (≤3 rules)  
*Risk: Low. Claude handles simple instructions reliably.*

**Level 2:** 3–5 rule categories OR specific formatting rules  
*Risk: Medium. May skip 1–2 constraints if not emphatic.*

**Level 3:** Structured workflows OR nested boundaries OR multi-format outputs  
*Risk: High. Requires explicit prioritization and conflict resolution rules.*

**Level 4:** Multi-source instructions OR conditional overrides OR domain switching  
*Risk: Very high. Must include compliance checks and explicit instruction hierarchy.*

**Anti-drift tactics by level:**
- L 1: No special tactics needed
- L 2: Use "ALWAYS" / "NEVER" for critical rules
- L 3: Number steps; add "Before proceeding, confirm..."
- L 4: Include meta-instruction like "If conflicting rules appear, prioritize..."
```