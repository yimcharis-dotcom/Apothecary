---
tags:
  - templates
  - system-infrastructure
  - workflow-management
  - prompt
---

```
---
type: prompt
category: grammar | accounting | ai-dev | system
model: gpt-4 | claude | both
status: production | testing | deprecated
version: 1.0
created: 2026-01-04
last-tested: 2026-01-04
deployed-to: [[00_System/Copilot_Prompts/Summarize]] | none
tags: [domain-tags]
---
# [Prompt Name]

## Purpose
One-sentence description of what this solves.

## Prompt
[Exact prompt text - copy-paste ready]

## Variables
- `{variable1}`: Description
- `{variable2}`: Description

## Example Usage
**Input:**
[Example input]


**Output:**
[Expected output]

## Parameters (if API use)
- Temperature: 0.7
- Max tokens: 1500
- Top-p: 0.9

## Quality Metrics
- Success rate: 85% (17/20 test cases)
- Avg. quality score: 8.2/10
- Last tested: 2026-01-04

## Iteration History
- v1.0 (2026-01-04): Initial production version
- v0.9 (2025-12-28): Beta - fixed edge case with nested lists

## Related
- [[Grammar_Checker_v2]] (older version)
- [[Tone_Adjuster]] (complementary)
- Experiment: [[40_Experiments/_Archive/Grammar_Checker/]]

## Deployment Notes
> **If deployed to System:** This prompt is also in `00_System/`. 
> To update: Edit here → copy to System → update plugin settings.

```