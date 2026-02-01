# AI Hub - Centralized AI Agent Management

**Simple automation for managing 50+ AI agents in one workspace**
## What This Is
Instead of a complex dashboard, this is a collection of **simple PowerShell scripts** that leverage your symlinked AI_hub directory to make config and skills management easier.
## Quick Start
```powershell
# Interactive menu (easiest)
.\Hub.ps1

# Or run specific commands
.\Hub.ps1 skills   # Show what skills are installed where
.\Hub.ps1 agents   # List all agents by category
.\Hub.ps1 sync     # Copy skills from Claude to all other agents
.\Hub.ps1 code     # Open Hub in VSCode
```

## Scripts Included

### 🎯 Hub.ps1 (Master Control)
Main menu system that ties everything together. Run this first.

```powershell
.\Hub.ps1           # Interactive menu
.\Hub.ps1 skills    # Quick skills inventory
.\Hub.ps1 configs   # Quick config inventory
```

### 📊 ShowSkills.ps1
See which skills are installed in which agents.

```powershell
.\ShowSkills.ps1
```

Output:
```
Claude_User_Dot:
  - excel-editor
  - find-skills

Cursor_User_Dot:
  - excel-editor
  - find-skills

=== Skills Distribution ===
excel-editor (2 agents):
  Claude_User_Dot, Cursor_User_Dot
```

### 🔄 SyncSkills.ps1
Copy skills from one agent to all others (works through symlinks).

```powershell
# Copy all skills from Claude to everyone
.\SyncSkills.ps1

# Copy from a different agent
.\SyncSkills.ps1 -SourceAgent "Cursor_User_Dot"

# Copy only specific skill
.\SyncSkills.ps1 -SkillName "excel-editor"
```

### ⚙️ ShowConfigs.ps1
Find all config files across agents.

```powershell
.\ShowConfigs.ps1
```

### 📝 ExportToObsidian.ps1
Auto-generate a live inventory note in your Obsidian vault. Creates a markdown file with stats, skills distribution, and management commands.

```powershell
.\ExportToObsidian.ps1
# Creates: C:\Vault\Apothecary\20_AI tools\AI_Hub_Inventory_AUTO.md
```

The generated note includes:
- Quick stats (agent count, skills, configs)
- Skills distribution table
- Management command reference
- Auto-updates timestamp
- Obsidian frontmatter tags

### 🔍 WatchHub.ps1 (v2)
Auto-discovers new AI tools across **three layers**:
- **Layer 1**: User home and AppData settings folder.
- **Layer 2**: System programs, custom project roots (`GitHubRepo`), and drive roots.
- **Layer 3**: Binary signature detection (detects AI tools even if folder names are generic).

```powershell
.\WatchHub.ps1  # Tracks _User_Dot, _AppData, _System, and _Root suffixes
```

## Common Workflows

### Install a new skill to all agents
```powershell
# Using Skills CLI (recommended)
npx skills add vercel-labs/agent-skills --all --global --yes

# Or via Hub menu
.\Hub.ps1
# Select option 5
```

### Keep skills updated
```powershell
npx skills update --yes

# Or via Hub menu
.\Hub.ps1
# Select option 6
```

### Sync skills from your main agent
```powershell
.\SyncSkills.ps1 -SourceAgent "Claude_User_Dot"
```

### Find what configs need updating
```powershell
.\ShowConfigs.ps1
# Then manually edit configs in VSCode workspace
```

## VSCode Workspace Setup

Your AI_hub is perfect for a VSCode workspace:

1. Open Hub: `.\Hub.ps1 code` or `code C:\Users\YC\AI_hub`
2. In VSCode: File → Save Workspace As → `AI_Hub.code-workspace`
3. Now you can:
   - Search across all agent configs at once (Ctrl+Shift+F)
   - Edit multiple agent configs side-by-side
   - Use Git to track config changes
   - Quickly navigate between agents
## File Structure
```text
AI_hub/
├── Hub.ps1                 # Master control script
├── ShowSkills.ps1          # Skills inventory
├── SyncSkills.ps1          # Skills sync tool
├── ShowConfigs.ps1         # Config inventory
├── WatchHub.ps1            # Auto-discovery (existing)
├── GEMINI.md               # Documentation (existing)
├── README.md               # This file
└── [50+ symlinked agent directories]
```

## Why This Works Better Than a Dashboard

- **No complex UI** to maintain
- **Works with VSCode** (your IDE) instead of separate tool
- **Scripts are simple** - easy to modify/extend
- **Leverages existing symlinks** - no database needed
- **Fast** - just PowerShell and file operations
- **Reliable** - symlinks keep everything in sync

## Next Steps

1. Run `.\Hub.ps1` to see the menu
2. Try `.\ShowSkills.ps1` to see current skills
3. Install a skill globally: `npx skills add vercel-labs/agent-skills --all --global -y`
4. Sync it: `.\SyncSkills.ps1`
5. Open in VSCode: `.\Hub.ps1 code`

## Tips

- Keep WatchHub.ps1 running in background to auto-discover new tools
- Use `npx skills` for installing, use `SyncSkills.ps1` for copying between agents
- The symlinks mean changes in AI_hub affect the real config directories
- Commit your scripts to Git for version control
- Add more patterns to WatchHub.ps1 as you discover new AI tool types
---
**Simple automation > Complex dashboards**
