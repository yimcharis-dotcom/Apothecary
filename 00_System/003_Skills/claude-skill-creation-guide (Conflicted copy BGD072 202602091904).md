# Complete Guide to Creating and Implementing Claude Skills

## What Are Claude Skills?

Claude skills are modular, self-contained packages that extend Claude's capabilities by providing specialized knowledge, workflows, and tools. Think of them as "onboarding guides" for specific domains or tasks—they transform Claude from a general-purpose assistant into a specialized agent equipped with procedural knowledge that no language model can fully possess on its own.

Skills are particularly valuable when you need Claude to handle domain-specific tasks consistently, follow multi-step procedures reliably, or work with specific file formats and APIs. Rather than explaining the same process repeatedly in each conversation, you encode that knowledge once in a skill, and Claude can reference it whenever needed.

---

## Step 1: Understanding What Makes a Good Skill

Before you create a skill, you need to understand what kinds of information belong in a skill versus what Claude already knows.

### When to Create a Skill

A skill is appropriate when:

- **Repetitive workflows exist**: You find yourself explaining the same multi-step process repeatedly to Claude, such as "when creating a report, always start with X, then do Y, then finish with Z."

- **Domain-specific knowledge is required**: Your task requires company-specific schemas, internal APIs, brand guidelines, or proprietary processes that Claude couldn't know from its general training.

- **Tool integrations need standardization**: You need Claude to work with specific file formats (like DOCX, PDF, PPTX) in a consistent way, using specific libraries and approaches.

- **Bundled resources would help**: Scripts, templates, or reference documentation would make Claude's work more efficient and reliable.

### When NOT to Create a Skill

Avoid creating skills for:

- **General knowledge Claude already has**: Claude doesn't need a skill to explain Python syntax or write basic code—it already knows this.

- **One-off tasks**: If you'll only do something once, just explain it in the conversation rather than building a skill.

- **Simple preferences**: A single instruction like "always respond in Spanish" doesn't need a full skill—you can just tell Claude directly.

---

## Step 2: Gather Concrete Examples

The most important preparation step is collecting concrete examples of how the skill will be used. This grounds your skill design in reality rather than abstract theory.

Ask yourself these questions:

1. **What specific requests will trigger this skill?** Write down 3-5 example user requests word-for-word. For example, if you're building an image-editor skill:
   - "Remove the background from this photo"
   - "Rotate this image 90 degrees clockwise"
   - "Convert this PNG to JPEG"

2. **What should the output look like?** For each example request, describe or show what the ideal output would be.

3. **What steps does Claude need to follow?** Walk through the process manually and note each decision point and action.

4. **What could go wrong?** Identify common errors or edge cases that the skill should handle.

This exercise reveals the actual scope of your skill and prevents feature creep or missing requirements.

---

## Step 3: Plan Your Skill's Contents

Based on your concrete examples, identify what reusable resources would help Claude execute these tasks repeatedly.

### Three Types of Bundled Resources

**1. Scripts (`scripts/` directory)**

Executable code that performs specific operations deterministically. Include a script when:

- The same code would be rewritten each time
- Deterministic reliability is critical
- The operation is error-prone and benefits from tested code

Examples: `rotate_pdf.py`, `extract_text.py`, `convert_image.py`

**2. References (`references/` directory)**

Documentation that Claude should read while working. Include references when:

- Detailed information is too long for the main SKILL.md
- Information is only needed for specific use cases
- External schemas, APIs, or specifications need to be documented

Examples: `api_reference.md`, `database_schema.md`, `brand_guidelines.md`

**3. Assets (`assets/` directory)**

Files that become part of Claude's output (not read into context). Include assets when:

- Templates need to be filled in or copied
- Images, fonts, or other binary files are needed
- Boilerplate code or project structures should be reused

Examples: `template.pptx`, `logo.png`, `hello-world/` (starter project)

### Resource Planning Worksheet

For each of your example use cases, answer:

| Example Request | Scripts Needed? | References Needed? | Assets Needed? |
|----------------|-----------------|-------------------|----------------|
| "Rotate PDF 90°" | rotate_pdf.py | None | None |
| "Create report from template" | None | report_guidelines.md | template.docx |
| "Build a landing page" | None | design_system.md | starter-template/ |

---

## Step 4: Understand Skill Architecture

Every skill follows a specific structure. Understanding this architecture helps you organize your content effectively.

### Required Structure

```
skill-name/
├── SKILL.md          (required - the main skill file)
├── scripts/          (optional - executable code)
├── references/       (optional - documentation)
└── assets/           (optional - templates and resources)
```

### The SKILL.md File

This is the heart of your skill. It has two parts:

**Part 1: YAML Frontmatter (Required)**

```yaml
---
name: your-skill-name
description: A complete description of what the skill does and WHEN to use it. Include specific triggers, file types, or scenarios.
---
```

The `description` field is crucial because it's how Claude decides whether to use your skill. Be specific about triggers:

- ❌ Bad: "Helps with documents"
- ✅ Good: "Creates, edits, and analyzes Microsoft Word documents (.docx files). Use when: creating new documents, modifying existing content, working with tracked changes, adding comments, or extracting text from DOCX files."

**Part 2: Markdown Body (Required)**

The instructions Claude follows when using the skill. This is only loaded after Claude decides to use the skill, so don't put "when to use" information here—it belongs in the description.

### Progressive Disclosure Principle

Skills use a three-level loading system to manage context efficiently:

1. **Level 1 - Metadata**: The `name` and `description` are always in context (~100 tokens). This is how Claude decides whether to read the full skill.

2. **Level 2 - SKILL.md Body**: Loaded when the skill triggers. Keep this under 500 lines to minimize context usage.

3. **Level 3 - Bundled Resources**: Only loaded when Claude determines they're needed. This allows unlimited detailed content without bloating every request.

---

## Step 5: Initialize Your Skill

With your planning complete, it's time to create the skill structure. Use the initialization script for a clean starting point.

### Using the Init Script

```bash
python /mnt/skills/examples/skill-creator/scripts/init_skill.py your-skill-name --path /home/claude/skills
```

This creates:

```
your-skill-name/
├── SKILL.md              (template with TODOs)
├── scripts/
│   └── example.py        (placeholder script)
├── references/
│   └── api_reference.md  (placeholder reference)
└── assets/
    └── example_asset.txt (placeholder asset)
```

### Naming Conventions

- Use **kebab-case** for skill names: `my-awesome-skill`, not `myAwesomeSkill`
- Keep names under 64 characters
- Use descriptive names that hint at functionality: `pdf-form-filler`, `brand-style-guide`, `api-integration-helper`

---

## Step 6: Write Your SKILL.md

Now fill in the SKILL.md template with your actual content. This is where most of the work happens.

### Writing the Frontmatter

```yaml
---
name: image-processor
description: Process and manipulate images including format conversion, resizing, rotation, cropping, and filters. Use when the user asks to: convert between image formats (PNG, JPEG, WebP, etc.), resize or scale images, rotate or flip images, crop images, apply filters or adjustments, remove backgrounds, or perform any image editing task.
---
```

### Choosing a Structure for the Body

Select a structure based on your skill's nature:

**Workflow-Based** (for sequential processes):
```markdown
# Image Processor

## Overview
Process images through a consistent workflow.

## Workflow
1. Load the image
2. Determine the operation type
3. Execute the operation
4. Save the output

## Operations

### Rotation
[details]

### Resizing
[details]
```

**Task-Based** (for tool collections):
```markdown
# Image Processor

## Quick Start
Basic image operations require the Pillow library...

## Format Conversion
[details]

## Resizing
[details]

## Rotation
[details]
```

**Reference-Based** (for standards/guidelines):
```markdown
# Brand Guidelines

## Overview
Standards for all brand communications.

## Colors
[specifications]

## Typography
[specifications]

## Logo Usage
[specifications]
```

### Writing Effective Instructions

Remember: you're writing for another instance of Claude. Include:

1. **What Claude doesn't know**: Proprietary information, specific approaches, your preferences
2. **Decision guidance**: How to choose between options
3. **Examples**: Concrete input/output pairs are more effective than abstract explanations
4. **Error handling**: What to do when things go wrong

Avoid:
1. **Explaining basics**: Claude knows how to write Python or format JSON
2. **Excessive explanation**: Be concise—every token costs context space
3. **Redundancy**: Information should live in one place only

### Referencing Bundled Resources

When your skill has scripts, references, or assets, tell Claude when to use them:

```markdown
## Rotating PDFs

To rotate a PDF, use the provided script:

```bash
python scripts/rotate_pdf.py input.pdf output.pdf --degrees 90
```

For complex rotations affecting only certain pages, see [references/advanced_rotation.md](references/advanced_rotation.md).
```

---

## Step 7: Create Your Bundled Resources

### Writing Scripts

Scripts should be self-contained and well-documented:

```python
#!/usr/bin/env python3
"""
Rotate a PDF by specified degrees.

Usage:
    python rotate_pdf.py input.pdf output.pdf --degrees 90

Arguments:
    input.pdf   - Path to the input PDF file
    output.pdf  - Path for the rotated output
    --degrees   - Rotation angle (90, 180, or 270)
"""

import argparse
from pypdf import PdfReader, PdfWriter

def rotate_pdf(input_path, output_path, degrees):
    """Rotate all pages in a PDF by the specified degrees."""
    reader = PdfReader(input_path)
    writer = PdfWriter()
    
    for page in reader.pages:
        page.rotate(degrees)
        writer.add_page(page)
    
    with open(output_path, 'wb') as f:
        writer.write(f)
    
    print(f"✅ Rotated {input_path} by {degrees}° → {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rotate PDF pages")
    parser.add_argument("input", help="Input PDF file")
    parser.add_argument("output", help="Output PDF file")
    parser.add_argument("--degrees", type=int, default=90, 
                        choices=[90, 180, 270], help="Rotation degrees")
    
    args = parser.parse_args()
    rotate_pdf(args.input, args.output, args.degrees)
```

**Important**: Always test your scripts before including them. Run them with various inputs to ensure they work correctly.

### Writing Reference Documents

Keep references focused and well-structured:

```markdown
# API Reference

## Authentication

All API calls require a Bearer token in the Authorization header.

## Endpoints

### GET /users/{id}

Retrieve user information.

**Parameters:**
- `id` (required): User ID

**Response:**
```json
{
  "id": "123",
  "name": "Jane Doe",
  "email": "jane@example.com"
}
```

### POST /users

Create a new user.

[etc.]
```

For long references (>100 lines), include a table of contents at the top.

### Organizing Assets

Assets are files Claude uses in output—not reads into context:

```
assets/
├── templates/
│   ├── report_template.docx
│   └── presentation_template.pptx
├── images/
│   ├── logo.png
│   └── icons/
└── boilerplate/
    └── react-starter/
        ├── package.json
        ├── src/
        └── public/
```

Reference assets in SKILL.md by their paths:

```markdown
## Creating Reports

Start by copying the template:
```bash
cp assets/templates/report_template.docx output/my_report.docx
```
```

---

## Step 8: Validate Your Skill

Before packaging, validate that your skill meets all requirements.

### Manual Validation Checklist

- [ ] SKILL.md exists and has valid YAML frontmatter
- [ ] `name` and `description` fields are present and non-empty
- [ ] Description clearly explains WHEN to use the skill
- [ ] Body is under 500 lines
- [ ] All referenced files actually exist
- [ ] Scripts are executable and tested
- [ ] No duplicate information between SKILL.md and references
- [ ] No unnecessary files (README.md, CHANGELOG.md, etc.)

### Using the Validation Script

```bash
python /mnt/skills/examples/skill-creator/scripts/quick_validate.py /path/to/your-skill
```

This checks:
- YAML frontmatter format
- Required fields
- Naming conventions
- File organization

---

## Step 9: Package Your Skill

Once validated, package your skill for distribution.

```bash
python /mnt/skills/examples/skill-creator/scripts/package_skill.py /path/to/your-skill ./output
```

This creates `your-skill.skill`—a zip file containing your entire skill directory. This file can be:

- Shared with others
- Uploaded to Claude's skill repository
- Version controlled
- Backed up

---

## Step 10: Test and Iterate

The real test is using your skill in practice. After deployment:

1. **Use the skill on real tasks** - Try various requests that should trigger it
2. **Notice struggles** - Where does Claude get confused or produce suboptimal output?
3. **Identify improvements** - What additional guidance, examples, or resources would help?
4. **Update and retest** - Make changes and verify they improve behavior

Common iteration patterns:

- **Adding examples** when Claude misinterprets the desired output format
- **Adding decision trees** when Claude chooses wrong approaches
- **Adding scripts** when Claude keeps rewriting the same code with bugs
- **Splitting references** when context gets too long

---

## Complete Example: Building a "Data Analyzer" Skill

Let's walk through creating a complete skill from scratch.

### Step 1: Gather Examples

User requests this skill should handle:
- "Analyze this CSV and give me insights"
- "Create a summary report of this data"
- "What are the key statistics in this dataset?"
- "Find anomalies in this data"

### Step 2: Plan Resources

| Request | Scripts | References | Assets |
|---------|---------|------------|--------|
| Analyze CSV | analyze_csv.py | analysis_guidelines.md | None |
| Summary report | None | report_format.md | report_template.md |
| Statistics | statistics.py | None | None |
| Find anomalies | anomaly_detection.py | None | None |

### Step 3: Create Structure

```
data-analyzer/
├── SKILL.md
├── scripts/
│   ├── analyze_csv.py
│   ├── statistics.py
│   └── anomaly_detection.py
├── references/
│   ├── analysis_guidelines.md
│   └── report_format.md
└── assets/
    └── report_template.md
```

### Step 4: Write SKILL.md

```markdown
---
name: data-analyzer
description: Analyze tabular data (CSV, Excel) to extract insights, statistics, and anomalies. Use when the user asks to: analyze data files, create data summaries, compute statistics, find patterns or anomalies, or generate reports from datasets.
---

# Data Analyzer

## Overview

Analyze tabular datasets to extract meaningful insights using consistent, reproducible methods.

## Workflow

1. **Load data**: Read the file and assess its structure
2. **Profile**: Understand columns, types, and basic statistics
3. **Analyze**: Apply appropriate analysis based on the request
4. **Report**: Present findings in a clear, actionable format

## Quick Analysis

For fast insights, use the analysis script:

```bash
python scripts/analyze_csv.py data.csv
```

This outputs basic statistics and identifies potential issues.

## Statistical Analysis

For comprehensive statistics:

```bash
python scripts/statistics.py data.csv --output stats.json
```

## Anomaly Detection

To find outliers and anomalies:

```bash
python scripts/anomaly_detection.py data.csv --threshold 2.5
```

## Report Generation

Follow the format in [references/report_format.md](references/report_format.md) when creating analysis reports. Use the template in [assets/report_template.md](assets/report_template.md) as a starting point.

## Guidelines

See [references/analysis_guidelines.md](references/analysis_guidelines.md) for best practices on:
- Handling missing data
- Choosing appropriate statistics
- Interpreting results
- Presenting findings
```

### Step 5: Package and Test

```bash
python /mnt/skills/examples/skill-creator/scripts/package_skill.py data-analyzer ./dist
```

---

## Best Practices Summary

1. **Be concise**: Every token costs context space. Only include what Claude doesn't already know.

2. **Write clear triggers**: The `description` field determines when your skill activates—make it specific.

3. **Use progressive disclosure**: Keep SKILL.md lean; put details in references.

4. **Test your scripts**: Never include untested code.

5. **Provide examples**: Input/output pairs are more effective than abstract explanations.

6. **Iterate based on use**: Real-world usage reveals gaps that planning misses.

7. **Avoid duplication**: Information should live in one place only.

8. **Match freedom to fragility**: Use strict scripts for error-prone operations; use flexible guidance for creative tasks.

---

## Troubleshooting Common Issues

**Skill doesn't trigger**: Check that your `description` includes the specific scenarios and keywords users might use.

**Claude ignores instructions**: Make instructions imperative ("Do X") rather than descriptive ("This skill does X").

**Context too long**: Move detailed content from SKILL.md to reference files.

**Scripts fail**: Test scripts independently with various inputs before including them.

**Inconsistent output**: Add examples showing exact expected output format.

---

This guide covers everything you need to create effective Claude skills. Start simple, test thoroughly, and iterate based on real usage.
