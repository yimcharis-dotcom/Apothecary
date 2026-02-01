---
tags: [ai-tools, automation, inventory, auto-generated]
created: 2026-01-31 09:55:30
last_updated: 2026-01-31 09:55:30
type: dashboard
---

# AI Hub Inventory

> **Auto-generated on**: 2026-01-31 09:55:30  
> **Source**: `C:\Users\YC\AI_hub`  
> **Total Agents**: 93  
> **Agents with Skills**: 28  

---

## Quick Stats

| Metric | Count |
|--------|-------|
| Total AI Agents | 93 |
| Agents with Skills Support | 28 |
| Unique Skills | 9 |
| Config Files Found | 21 |

---

## Skills Distribution

| Skill | Agent Count |
|-------|-------------|
| `excel-editor` | 28 |
| `find-skills` | 27 |
| `notebooks` | 1 |
| `agent-workflow-builder_ai_toolkit` | 1 |
| `.claude` | 1 |
| `sample_data` | 1 |
| `.system` | 1 |
| `assets` | 1 |
| `custom_skills` | 1 |

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

- [[AI_Ecosystem_Dashboard]]
- [[Claude_AI_Ecosystem_Discovery]]

---

*Last updated: 2026-01-31 09:55:30*  
*Auto-generated from C:\Users\YC\AI_hub*

