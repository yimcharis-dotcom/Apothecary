---
tags: [ai-tools, automation, inventory, auto-generated]
created: 2026-02-01 06:37:18
last_updated: 2026-02-01 06:37:18
type: dashboard
---

# AI Hub Inventory

> **Auto-generated on**: 2026-02-01 06:37:18  
> **Source**: `C:\Users\YC\AI_hub`  
> **Total Agents**: 146  
> **Agents with Skills**: 31  

---

## Quick Stats

| Metric | Count |
|--------|-------|
| Total AI Agents | 146 |
| Agents with Skills Support | 31 |
| Unique Skills | 9 |
| Config Files Found | 37 |

---

## Skills Distribution

| Skill | Agent Count |
|-------|-------------|
| `excel-editor` | 29 |
| `find-skills` | 28 |
| `custom_skills` | 2 |
| `assets` | 2 |
| `notebooks` | 2 |
| `.claude` | 2 |
| `sample_data` | 2 |
| `.system` | 1 |
| `agent-workflow-builder_ai_toolkit` | 1 |

---

## Management Commands

### View Inventory
```powershell
cd C:\Users\YC\AI_hub
.\ShowSkills.ps1        # File system view
npx skills list -g      # Skills CLI view
.\ShowConfigs.ps1       # Find all configs
```

### Install Skills
```powershell
# Install to all agents
npx skills add vercel-labs/agent-skills --all -g -y

# Update all skills
npx skills update -y
```

### Export to Obsidian
```powershell
# Regenerate this file
.\ExportToObsidian.ps1
```

---

## Related Notes

- [[99_Archive/ss/AI_Ecosystem_Dashboard]]
- [[Claude_AI_Ecosystem_Discovery]]

---

*Last updated: 2026-02-01 06:37:18*  
*Auto-generated from C:\Users\YC\AI_hub*

