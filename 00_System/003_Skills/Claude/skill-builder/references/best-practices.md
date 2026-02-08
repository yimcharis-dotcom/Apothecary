# Best Practices for Claude Skills

This reference provides detailed guidance on creating effective, maintainable skills.

## Table of Contents

1. [Writing Concise Instructions](#writing-concise-instructions)
2. [Description Field Optimization](#description-field-optimization)
3. [Structuring Complex Workflows](#structuring-complex-workflows)
4. [Balancing Flexibility and Consistency](#balancing-flexibility-and-consistency)
5. [Common Patterns](#common-patterns)
6. [Anti-Patterns to Avoid](#anti-patterns-to-avoid)

---

## Writing Concise Instructions

The context window is a shared resource. Every token in your skill competes with conversation history, other skills, and the user's actual request. Write with economy.

### The Core Principle

**Default assumption: Claude is already very intelligent.** Only add context Claude doesn't already have. For each piece of information, ask: "Does Claude really need this explanation?" and "Does this justify its token cost?"

### Techniques for Conciseness

**Use examples instead of explanations:**

Instead of this (verbose):
```markdown
When creating a commit message, you should follow the conventional commits
specification. This means starting with a type like 'feat' for features or
'fix' for bug fixes, followed by an optional scope in parentheses, then a
colon and space, then the description. The description should be in
imperative mood and not end with a period.
```

Write this (concise with example):
```markdown
Format: `type(scope): description`

Example:
```
feat(auth): add OAuth2 support for Google login
```
```

**Prefer tables for structured information:**

Instead of paragraphs listing options, use a table:

| Type | Use for | Example |
|------|---------|---------|
| feat | New features | `feat(api): add user endpoints` |
| fix | Bug fixes | `fix(auth): handle expired tokens` |
| docs | Documentation | `docs: update API reference` |

**Use imperative mood:**

Instead of "The script will process the file", write "Process the file with..."

Instead of "This section describes how to...", just describe how to do it.

---

## Description Field Optimization

The description is the most critical part of your skill—it determines when Claude uses it.

### Structure

A good description has two parts:
1. **What it does** (functionality)
2. **When to use it** (triggers)

### Formula

```
[Action verb + domain/capability]. Use when [specific triggers, file types, user phrases, or scenarios].
```

### Examples

**Weak description:**
```
Helps with documents.
```

**Strong description:**
```
Create, edit, and analyze Microsoft Word documents (.docx files) with support for tracked changes, comments, and formatting. Use when the user asks to: create new documents, modify existing DOCX files, work with tracked changes or comments, extract text from Word documents, or convert documents to other formats.
```

**Weak description:**
```
A skill for working with data.
```

**Strong description:**
```
Analyze tabular data from CSV and Excel files to extract insights, compute statistics, and detect anomalies. Use when the user asks to: analyze data files, create data summaries, compute statistics, find patterns or outliers, or generate analytical reports.
```

### Keywords to Include

Include words users might actually say:
- File format names: "CSV", "Excel", "PDF", "DOCX"
- Action verbs: "create", "edit", "analyze", "convert", "extract"
- Domain terms: "report", "chart", "table", "form"
- User phrases: "help me with", "I need to", "can you"

---

## Structuring Complex Workflows

Complex skills need clear structure to guide Claude through multi-step processes.

### Use Numbered Workflows

For sequential processes, use numbered steps:

```markdown
## Workflow

1. **Load** → Read the input file and validate format
2. **Process** → Apply the requested transformation
3. **Validate** → Check output meets requirements
4. **Save** → Write to output location

## Step 1: Load

[Detailed instructions]

## Step 2: Process

[Detailed instructions]
```

### Use Decision Trees

For branching logic, make decisions explicit:

```markdown
## Choosing the Right Approach

**Is the user creating new content or editing existing?**
- Creating new → Go to [Creation Workflow](#creation-workflow)
- Editing existing → Go to [Editing Workflow](#editing-workflow)

**For editing, does the file have tracked changes?**
- Yes → Use the tracked changes approach in Step 3a
- No → Use the direct editing approach in Step 3b
```

### Use Checklists for Verification

```markdown
## Before Delivering Output

Verify:
- [ ] File format matches user's request
- [ ] All requested changes are applied
- [ ] No unintended modifications
- [ ] Output file is accessible
```

---

## Balancing Flexibility and Consistency

Different tasks need different levels of constraint. Match the constraint level to the task's fragility.

### High Flexibility (Guidelines)

Use when multiple approaches are valid and context determines the best choice.

```markdown
## Formatting Reports

Adapt the report structure based on content:
- For quantitative analysis, lead with numbers and charts
- For narrative content, use prose with embedded data
- When comparing options, use tables
```

### Medium Flexibility (Patterns with Options)

Use when a preferred approach exists but some variation is acceptable.

```markdown
## Creating Charts

Default approach: Use matplotlib for static charts.

Consider alternatives when:
- Interactive features needed → Use plotly
- Web embedding required → Use Chart.js
- High performance with large data → Use datashader
```

### Low Flexibility (Strict Scripts)

Use when operations are fragile and must be done exactly right.

```markdown
## Rotating PDF Pages

Always use the provided script—do not write custom rotation code:

```bash
python scripts/rotate_pdf.py input.pdf output.pdf --degrees 90
```

The script handles edge cases that custom code often misses.
```

---

## Common Patterns

### Pattern 1: Progressive Detail

Put essential information first, details in references:

```markdown
# SKILL.md

## Quick Start
[Minimal example to get started]

## Common Tasks
[Brief coverage of frequent uses]

## Advanced Features
See [references/advanced.md](references/advanced.md) for:
- Complex configurations
- Edge case handling
- Performance optimization
```

### Pattern 2: Input/Output Examples

Show what goes in and what comes out:

```markdown
## Date Formatting

**Input:** "2024-01-15"
**Output:** "January 15, 2024"

**Input:** "15/01/2024" (European format)
**Output:** "January 15, 2024"
```

### Pattern 3: Error Recovery

Guide Claude through common failure modes:

```markdown
## Troubleshooting

**If the file won't open:**
1. Check file extension matches actual format
2. Try alternative library: `from pypdf import PdfReader`
3. If corrupted, inform user and offer partial recovery

**If encoding errors occur:**
1. Try explicit encoding: `encoding='utf-8'`
2. Fallback: `encoding='latin-1'`
3. Last resort: `errors='ignore'`
```

### Pattern 4: Template with Customization Points

```markdown
## Report Template

```
# [TITLE]

## Executive Summary
[2-3 sentences summarizing key findings]

## Analysis
[Main content - adapt length to complexity]

## Recommendations
[Actionable next steps]

## Appendix (if needed)
[Supporting data, methodology notes]
```

Customize section depth based on report complexity.
```

---

## Anti-Patterns to Avoid

### Anti-Pattern 1: Explaining What Claude Already Knows

**Don't do this:**
```markdown
## Python Lists
Python lists are ordered collections that can hold multiple items...
[300 words explaining basic Python]
```

**Do this instead:**
Just use lists in your examples—Claude knows Python.

### Anti-Pattern 2: Duplicating Information

**Don't do this:**
```markdown
# SKILL.md
The API uses OAuth2 authentication with bearer tokens...

# references/api.md
Authentication uses OAuth2 with bearer tokens...
```

**Do this instead:**
Put detailed information in one place (references) and link to it.

### Anti-Pattern 3: Vague Descriptions

**Don't do this:**
```yaml
description: A useful skill for various tasks
```

**Do this instead:**
```yaml
description: Convert between image formats (PNG, JPEG, WebP, GIF). Use when the user asks to convert images, change image format, or save images as different types.
```

### Anti-Pattern 4: Over-Engineering Simple Tasks

**Don't do this:**
Create a complex skill with multiple scripts for tasks Claude can do directly.

**Do this instead:**
Only create skills for truly repetitive, error-prone, or domain-specific tasks.

### Anti-Pattern 5: Ignoring Real Usage

**Don't do this:**
Design a skill based on what you imagine users might want.

**Do this instead:**
Start with concrete examples of actual requests the skill should handle.

---

## Maintenance Guidelines

### When to Update a Skill

Update when you notice:
- Claude consistently misinterprets instructions
- Users frequently need the same clarification
- New use cases emerge that the skill should handle
- Better approaches become available

### Update Process

1. Identify the specific issue
2. Make minimal changes to address it
3. Test with the original problematic cases
4. Verify existing functionality still works

### Version Notes

Keep a brief mental model of changes (don't create CHANGELOG files):
- If making breaking changes, test thoroughly
- If adding features, ensure they don't bloat the skill unnecessarily
- If fixing bugs, verify the fix doesn't introduce new issues
