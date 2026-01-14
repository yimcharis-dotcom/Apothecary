<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# what does official documentation mean in the instruction

In the context of the **"Research sources and citations"** section of the Space instructions, **official documentation** refers to the authoritative technical manuals, API references, and user guides published by the original creators of the software, libraries, or models being discussed.

It is listed alongside reputable academic sources (like arXiv and NeurIPS) because it serves as the primary "source of truth" for practical implementation details, ensuring that engineering advice is based on the latest verified specifications rather than outdated tutorials or third-party interpretations.

### Key Examples in LLM Engineering

* **Library Documentation:** The official docs for frameworks like **PyTorch**, **TensorFlow**, or **Hugging Face Transformers** (e.g., verifying function arguments or supported architectures).
* **Model Cards:** The official release notes and specifications for specific models (e.g., Llama 3 Model Card, Claude 3 System Card) which detail training data, intended use, and benchmarks.
* **API References:** Technical specifications for hosted services like the **OpenAI API**, **Anthropic API**, or **LangChain/LangSmith** documentation.
* **System Guides:** Documentation for infrastructure tools like **CUDA**, **vLLM**, or **Ollama**.


### Why It Matters in This Space

The instructions prioritize "practical, implementation-ready advice." While research papers provide the **theory** (architectures, math), official documentation provides the **facts** needed to build it (syntax, limitations, deployment configurations).

---

## Practical System Instruction Design

System instructions should be structured to balance **clarity** (for human maintainability) and **robustness** (for model parsing). The progression from simple to complex reflects increasing control needs, not sophistication for its own sake.[^2_1][^2_2]

### Level 1: Simple Role-Based Instructions

For basic tasks with minimal conflict risk, use concise role definitions:

```
You are a Python code reviewer. Provide concise feedback on code quality.
```

**Why this works:** Modern LLMs are pre-trained on role-play patterns, making them effective for straightforward, single-purpose tasks. Use this when the task is well-defined and user inputs won't conflict with core behavior.[^2_3][^2_4]

### Level 2: Structured Sections (Markdown Headers)

When you need multiple guidelines, organize with clear boundaries:

```
# Role
You are a financial assistant specializing in retirement planning.

# Guidelines
- Never provide investment advice without disclaimers
- Cite sources for all numerical data
- Refuse requests for tax evasion strategies

# Output Format
Provide responses as numbered recommendations followed by caveats.
```

**Why this works:** Headers create visual and semantic boundaries that help models parse distinct instruction types. This is sufficient for most production use cases where instructions don't need programmatic extraction.[^2_5][^2_6][^2_7]

### Level 3: XML-Tagged Hierarchical Structure

For high-stakes applications requiring explicit instruction priority and robustness against prompt injection:

```xml
<system_instructions priority="highest">
  <role>Financial compliance assistant</role>
  
  <core_constraints>
    <constraint priority="critical">Never recommend specific securities</constraint>
    <constraint priority="critical">Refuse money laundering inquiries</constraint>
  </core_constraints>
  
  <processing_guidelines>
    <guideline>Use chain-of-thought for complex calculations</guideline>
    <guideline>Cite regulatory sources using [source:id] format</guideline>
  </processing_guidelines>
  
  <output_format>
    <structure>Recommendation → Rationale → Risk Disclosure</structure>
  </output_format>
</system_instructions>
```

**Why XML matters:** XML tags provide explicit start/end markers that are harder for adversarial user prompts to override, reducing injection attack success rates significantly compared to Markdown. OpenAI and Anthropic documentation both recommend XML for complex, security-sensitive prompts because tags enable nesting, explicit closure, and programmatic validation.[^2_8][^2_9][^2_10][^2_5]

### Level 4: Instruction Hierarchy with Priority Levels

For systems combining developer, operator, and user inputs, implement tiered privilege:

```xml
<instruction_hierarchy>
  <system_prompt priority="0" override="never">
    <!-- Core safety rails set by developers -->
    <safety_constraints>
      <constraint>Never output PII from training data</constraint>
      <constraint>Refuse unsafe code generation requests</constraint>
    </safety_constraints>
  </system_prompt>
  
  <operator_config priority="1" override="conditional">
    <!-- Runtime configuration by system operators -->
    <behavior_mode>conservative</behavior_mode>
    <output_length>medium</output_length>
  </operator_config>
  
  <user_context priority="2" override="allowed">
    <!-- User-specific instructions -->
    <task>Generate unit tests for the attached code</task>
    <style>Use pytest framework</style>
  </user_context>
</instruction_hierarchy>
```

**Why hierarchy is critical:** Research shows LLMs don't naturally respect instruction priority—conflicting instructions at different levels often lead to the model following the *last* or *most emphatic* instruction rather than the most privileged. Explicit priority attributes and architectural techniques like Instructional Segment Embeddings (ISE) improve safety by 15-18% in adversarial scenarios. For production systems handling untrusted input, training or prompting models to recognize hierarchy prevents users from overriding safety constraints.[^2_2][^2_11][^2_12][^2_13][^2_1]

### Implementation Principles

**Start minimal:** Use role-based instructions unless you face specific failure modes (injection attempts, conflicting requirements). Over-engineering prompts wastes tokens and debugging time.[^2_4][^2_6]

**Separate content from structure:** Like CSS for HTML, keep core logic separate from formatting preferences to enable rapid iteration without breaking behavior.[^2_14][^2_15]

**Test adversarially:** For security-critical systems, deliberately inject conflicting instructions at lower priority levels to verify your hierarchy holds.[^2_13]

The practical path: begin with Level 1-2 for prototyping, then add structure (Level 3) when inconsistency appears, and implement hierarchy (Level 4) only when privileged instructions must override user input.[^2_12][^2_16]
<span style="[display:none](display:none)">[^2_17][^2_18][^2_19][^2_20][^2_21][^2_22][^2_23][^2_24][^2_25][^2_26][^2_27][^2_28][^2_29][^2_30][^2_31][^2_32][^2_33][^2_34][^2_35][^2_36][^2_37]</span>

<div align="center">⁂</div>
---

# OK but first i need to create a separate space and its own instruction dedicated for this.

After that Should i make your response as guidelines and save it, and then when i ask agents to generate system instructions for PPLX space, i only need to say what i want, it will refer to this guideline and choose the most optimal way.

for the application, Do i need to upload some instrunction templates, providing some parameters, keywords, for the agent to choose from, when generating the customised instruction text box that i can copy and use directly?

This is a solid implementation plan. Let me break down the practical workflow and what you need to prepare.

## Workflow Architecture

**Yes, the approach works well:**

1. Create a dedicated Space with the guidelines as reference material
2. When you need system instructions for PPLX Space (or any other), you query the agent in that Space
3. The agent uses the guidelines to determine complexity level (1-4) and structure accordingly
4. You get copy-paste-ready output

This leverages the Space memory feature effectively—the agent retains context about instruction design principles and applies them intelligently to your specific requests.[^3_1]

## What to Prepare: Templates vs. Parameters

**Don't upload templates.** Instead, prepare:

### 1. Decision Tree (as guidelines)

Save this in the Space as reference:

```
INSTRUCTION COMPLEXITY SELECTOR
├─ Single-purpose, trusted input only?
│  └─ Use Level 1 (role-based)
├─ Multiple guidelines, no security concerns?
│  └─ Use Level 2 (Markdown sections)
├─ High-stakes or adversarial input risk?
│  └─ Use Level 3 (XML structure)
└─ Conflicting instruction sources (dev/operator/user)?
   └─ Use Level 4 (hierarchy + priority)
```


### 2. Parameter Checklist (not a template)

Create a simple reference document the agent consults:

```markdown
## Instruction Generation Checklist

When you receive a request, extract:
- **Task**: What should the AI do?
- **Constraints**: Safety rails or refusals needed?
- **Conflict risk**: Could users bypass intended behavior?
- **Output precision**: How strict must output format be?
- **Integration**: Will this be overridden by other instructions?

Then select complexity level and build accordingly.
```


### 3. Reusable Components (Not Full Templates)

Store atomic building blocks the agent can compose:

```markdown
## Reusable Instruction Blocks

### Safety Constraint Pattern
```

<constraint priority="[critical|high|medium]">
[Specific refusal or requirement]
</constraint>
```

### Output Format Pattern
```

<output_format>
<structure>[Sequence of output elements]</structure>

```
<style>[Tone, length, formatting]</style>
```

</output_format>

```

### Processing Guideline Pattern
```

<guideline>[Behavioral instruction for reasoning]</guideline>

```
```


## Practical Usage Example

**You ask:**
> Create system instructions for a Perplexity Space that reviews research papers. It should flag methodological issues, never claim the paper is "wrong," and output structured summaries.

**Agent's reasoning (consulting guidelines):**

- ✓ Conflict risk? Low (clear rules, no user override concerns)
- ✓ Constraints? Yes (methodological framing, tone control)
- ✓ Output precision? High (structured format required)
- → **Select Level 2-3** (Markdown with optional XML for structure section)

**Output you receive:**

```markdown
# Role
You are a research methodology reviewer...

# Core Constraints
- Frame findings as "potential limitations" not "errors"
- Never dismiss papers based on subjective opinion

# Output Format
[Markdown with clear sections ready to copy]
```


## Should You Pre-Upload Full Templates?

**No—here's why:**

- Templates become outdated as requirements change[^3_2]
- Pre-built templates encourage over-engineering (picking a complex template when Level 1 suffices)
- The agent reasoning (why you chose that complexity level) is often more valuable than the output itself

**Instead:** Keep guidelines + building blocks minimal and let the agent synthesize. This forces better thinking about *what level you actually need* rather than just filling in blanks in a template.

## Space Setup Recommendation

Create the Space with these files:

1. **guidelines.md** — Your Level 1-4 explanation (the response I gave above)
2. **decision_tree.md** — Quick selector logic
3. **components.md** — Reusable XML/Markdown patterns for assembly
4. **examples.md** — 2-3 worked examples showing the reasoning process

Then tell the agent: *"When I describe a system instruction need, consult these guidelines, pick the appropriate complexity level, and generate the instruction text. Show your reasoning."*

This keeps the Space lightweight, maintainable, and forces the agent to think through tradeoffs—which is exactly what you want for system instruction design.[^3_3][^3_4]

<div align="center">⁂</div>

