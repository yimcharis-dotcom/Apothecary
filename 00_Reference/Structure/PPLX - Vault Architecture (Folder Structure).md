---

## 1. Vault Architecture (Folder Structure)

**Create this folder structure in Obsidian:**

```
your-vault/
├── 00-system/                    # System-wide configs, MOC (Maps of Content)
│   ├── Home.md                   # Central dashboard
│   ├── Vault-Changelog.md        # Track changes to vault structure
│   └── Naming-Conventions.md     # Rules for file naming, tagging
│
├── 10-prompts/                   # All reusable prompts organized by type
│   ├── 10-prompts-ai-learn/      # Learning AI: tutorials, concept explanations
│   │   ├── Explain-Concept.md
│   │   └── Compare-Methods.md
│   ├── 10-prompts-system-specs/  # System spec generators
│   │   ├── Spec-Template-Generator.md
│   │   └── API-Schema-Builder.md
│   ├── 10-prompts-grammar/       # Grammar/naturalness checking
│   │   ├── Grammar-Checker-Main.md
│   │   └── Grammar-Checker-Reference.md
│   ├── 10-prompts-writing/       # Writing assistance
│   │   ├── Email-Tone-Adjuster.md
│   │   └── Technical-Writer.md
│   └── 10-prompts-reasoning/     # Problem-solving, reasoning
│       ├── Root-Cause-Analysis.md
│       └── Decompose-Problem.md
│
├── 20-research/                  # Research notes, papers, findings
│   ├── 20-research-ai/
│   │   ├── LLM-Architecture-Notes.md
│   │   ├── Prompt-Engineering-Techniques.md
│   │   └── Evaluation-Methods.md
│   └── 20-research-tools/
│       ├── Obsidian-Plugins-Comparison.md
│       └── Espanso-vs-PowerToys.md
│
├── 30-projects/                  # Active projects
│   ├── 30-proj-grammar-checker/
│   │   ├── Spec.md               # System specification
│   │   ├── Test-Cases.md         # Test inputs and expected outputs
│   │   ├── Iterations/
│   │   │   ├── v1-initial.md
│   │   │   ├── v2-tier-fix.md
│   │   │   └── v3-final.md
│   │   └── Results/
│   │       ├── GPT-Results.md
│   │       └── Claude-Results.md
│   ├── 30-proj-system-spec-gen/
│   │   ├── Spec.md
│   │   └── Iterations/
│   └── 30-proj-custom-gpt/
│       ├── Spec.md
│       └── Training-Data/
│
├── 40-experiments/               # Scratch work, half-done tests
│   ├── 40-exp-prompt-variants.md
│   ├── 40-exp-eval-framework.md
│   └── 40-exp-notation-tests.md
│
├── 50-archive/                   # Deprecated, superseded versions
│   └── old-grammar-v1.md
│
├── Templates/                    # Obsidian template files (Templater plugin)
│   ├── Prompt-Template.md
│   ├── Project-Template.md
│   ├── Test-Case-Template.md
│   └── Iteration-Log-Template.md
│
└── Assets/                       # Images, diagrams, reference files
    └── workflow-diagram.png
```

**Rationale:**

- **00-system** = Vault governance, MOC (Map of Contents), entry points
- **10-prompts** = Immediately reusable, sortable by domain
- **20-research** = Knowledge you're building from (reference layer)
- **30-projects** = Active work with versioning and results
- **40-experiments** = WIP, no cleanup needed yet
- **50-archive** = Searchable but out of mind
- **Templates** = Standardized structure for new notes
- **Assets** = Media, external reference files