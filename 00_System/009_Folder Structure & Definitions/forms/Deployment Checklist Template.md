---
Tags:
  - deployment/Deployment-checklist
  - Templates
  - Workflow-management
  - system-infrastructure
---

```
# Deployment Checklist - [Prompt Name]

## Pre-Deployment
- [ ] Frontmatter complete (category, model, version, tested-date)
- [ ] Purpose documented
- [ ] Variables/parameters documented
- [ ] Example usage included
- [ ] Test results attached (min. 5 test cases)
- [ ] Performance metrics logged (if applicable)
- [ ] Related prompts linked

## Deployment Actions
- [ ] Copy to `10_Prompt_library/[Category]/[Name].md`
- [ ] If System prompt: Copy to `00_System/[Subdirectory]/[Name].md`
- [ ] Update links in both files (canonical ↔ deployed)
- [ ] Add to Espanso config (if quick-access needed)
- [ ] Test deployed version in actual use case

## Post-Deployment
- [ ] Archive source experiment in `40_Experiments/_Archive/`
- [ ] Delete `30_Projects/[Project]/`
- [ ] Update changelog/wiki index

```