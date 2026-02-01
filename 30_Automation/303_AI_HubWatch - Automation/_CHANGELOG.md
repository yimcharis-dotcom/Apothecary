# AI HubWatch Scripts - Changelog

## 2026-02-01

### ✨ Initial Deployment

**Scripts deployed:**
- `!WatchHub_Realtime.ps1` v2.0
  - Real-time monitoring of AI tools installation
  - Deletion detection & cleanup
  - Skills auto-sync via symlinks
  - Individual logs in `_Change_log/` with `_add` / `_del` suffixes

- `!SyncSkills.ps1` v2.0
  - Changed from copy to symlink
  - Added `-Delete` flag for cleanup
  - Syncs from Claude_User_Dot to all agents

- `!TrackInstallation.ps1` v1.0
  - Before/after snapshot comparison
  - Installation prediction guide
  - Interactive menu

- `!Hub.ps1` v2.0
  - Menu option 9: WatchHub v2
  - Menu option 10: Track Installation
  - CLI commands: `watch`, `track`

- `!ExportToObsidian.ps1` v1.0
  - Generates AI_Hub_Inventory_AUTO.md
  - Stats: agents, skills, configs

### 📋 Workflow Established

```
AI Tool Installed
  ↓ WatchHub detects
  ↓ Creates junction
  ↓ Logs to _Change_log
  ↓ Updates Obsidian

Skill Installed to Claude
  ↓ WatchHub detects
  ↓ Triggers SyncSkills
  ↓ Symlinks to all agents
  ↓ Logs to _Change_log
  ↓ Updates Obsidian
```

### 🎯 Canonical Locations

- **Runtime:** `C:\Users\YC\AI_hub\`
- **Deployed:** `C:\Vault\Apothecary\30_Automation/303_AI_HubWatch - Automation\`
- **Logs:** `C:\Users\YC\AI_hub\_Change_log\`

---

## Template for Future Changes

```markdown
## YYYY-MM-DD

### 🔧 Changes

**!ScriptName.ps1** vX.Y
- Change description
- Bug fix description

### 🐛 Bug Fixes

- Fixed issue with...

### 📝 Notes

- Additional context
```
