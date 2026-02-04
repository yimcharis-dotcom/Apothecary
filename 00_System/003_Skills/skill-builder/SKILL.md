---
name: skill-builder
description: "Create new Claude skills through guided conversation and automated scaffolding. Use when the user asks to create a skill, build a skill, make a new skill, design a skill, develop a skill, or wants to extend Claude's capabilities with custom workflows. Also triggers when user mentions 'skill' in the context of creating reusable Claude enhancements."
---

# Skill Builder

Create professional Claude skills through a guided, conversational workflow.

## Overview

This skill guides you through creating new Claude skills by gathering requirements, generating appropriate structure, and producing a distributable `.skill` package. The process ensures skills follow best practices and are immediately usable.

## Workflow

Creating a skill involves five phases:

1. **Discovery** → Understand what the skill should do through concrete examples
2. **Planning** → Identify scripts, references, and assets needed
3. **Generation** → Create the skill directory structure and files
4. **Refinement** → Review and improve the generated content
5. **Packaging** → Produce a distributable `.skill` file

## Phase 1: Discovery

Begin by understanding the skill's purpose through concrete examples.

### Essential Questions

Ask these questions (one or two at a time to avoid overwhelming the user):

**Scope questions:**
- "What specific task or domain should this skill help with?"
- "Can you give me 3-5 example requests that should trigger this skill?"
- "What would ideal outputs look like for each example?"

**Boundary questions:**
- "What should this skill NOT do? Are there related tasks it should leave to other skills?"
- "What errors or edge cases should it handle?"

**Resource questions:**
- "Do you have any existing scripts, templates, or documentation to include?"
- "Are there external APIs, file formats, or tools this skill needs to work with?"

### Discovery Completion Criteria

Proceed to Planning when you have:
- Clear understanding of 3+ concrete use cases
- Knowledge of required inputs and expected outputs
- List of any existing resources to incorporate

## Phase 2: Planning

Analyze each use case to determine required resources.

### Resource Analysis Template

For each use case, determine:

| Use Case | Scripts Needed | References Needed | Assets Needed |
|----------|---------------|-------------------|---------------|
| [Example 1] | [scripts that would be rewritten each time] | [documentation to reference] | [templates or files for output] |
| [Example 2] | ... | ... | ... |

### Resource Guidelines

**Include scripts when:**
- Same code would be rewritten repeatedly
- Deterministic reliability is critical
- Operations are error-prone

**Include references when:**
- Detailed information exceeds 50 lines
- Content is only needed for specific use cases
- External schemas or APIs need documentation

**Include assets when:**
- Templates should be copied or filled
- Images, fonts, or binary files are needed
- Boilerplate code should be reused

## Phase 3: Generation

Create the skill structure using the generation script.

### Generate the Skill

Run the generation script with planned resources:

```bash
python scripts/generate_skill.py \
  --name "skill-name" \
  --description "Complete description including when to use" \
  --output /home/claude/skills
```

The script creates the directory structure with:
- SKILL.md with frontmatter and structured sections
- Placeholder directories for scripts/, references/, assets/

### Customize Generated Content

After generation, implement the actual content:

1. **Write SKILL.md body** following these patterns:

   **For workflow-based skills:**
   ```markdown
   ## Workflow
   1. [First step]
   2. [Second step]
   ...
   
   ## [Step 1 Details]
   [Implementation guidance]
   ```

   **For task-based skills:**
   ```markdown
   ## Quick Start
   [Minimal example]
   
   ## [Task Category 1]
   [Details]
   
   ## [Task Category 2]
   [Details]
   ```

2. **Implement scripts** - Write tested, documented code
3. **Write references** - Create focused documentation
4. **Add assets** - Include templates and resources

### Writing Effective Descriptions

The description field is critical—it determines when the skill triggers.

**Structure:** [What it does] + [When to use it]

**Example:**
```
Analyze tabular data files to extract insights and statistics. Use when the user asks to: analyze CSV or Excel files, compute statistics, find data patterns, detect anomalies, or create data summary reports.
```

## Phase 4: Refinement

Review and improve the generated skill.

### Quality Checklist

Verify before packaging:

**Structure:**
- [ ] SKILL.md has valid YAML frontmatter
- [ ] `name` matches directory name (kebab-case)
- [ ] `description` includes specific triggers
- [ ] Body is under 500 lines

**Content:**
- [ ] Instructions use imperative form ("Do X" not "This does X")
- [ ] Examples show concrete input/output pairs
- [ ] References are linked from SKILL.md
- [ ] No duplicate information across files

**Resources:**
- [ ] All scripts are tested and working
- [ ] All referenced files exist
- [ ] No unnecessary files (README, CHANGELOG, etc.)

### Common Improvements

**If instructions are unclear:** Add step-by-step workflows with numbered steps.

**If output varies too much:** Add examples showing exact expected format.

**If context is too long:** Move detailed content to reference files.

**If decisions are inconsistent:** Add decision trees for choosing between approaches.

## Phase 5: Packaging

Create the distributable skill file.

### Validate First

```bash
python scripts/validate_skill.py /path/to/skill-name
```

Fix any reported issues before packaging.

### Create Package

```bash
python scripts/package_skill.py /path/to/skill-name --output /home/claude/output
```

This creates `skill-name.skill` ready for distribution.

## Best Practices Reference

See [references/best-practices.md](references/best-practices.md) for detailed guidance on:
- Writing concise, effective instructions
- Structuring complex workflows
- Balancing flexibility and consistency
- Common patterns and anti-patterns

## Example Skills

See [references/example-patterns.md](references/example-patterns.md) for annotated examples of:
- Workflow-based skills (PDF processing)
- Task-based skills (image manipulation)
- Reference-based skills (brand guidelines)
- Integration skills (API connectors)
