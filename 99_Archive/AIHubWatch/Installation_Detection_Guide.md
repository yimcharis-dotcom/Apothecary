# Installation Location Detection Guide

## Quick Start

### 1. Real-Time Monitoring (Set and Forget)
```powershell
cd C:\Users\YC\AI_hub
.\WatchHub_Realtime.ps1
```
**Leave this running** - it auto-detects new AI tools instantly!

### 2. Track Specific Installation
```powershell
# BEFORE installing
.\TrackInstallation.ps1 -Mode before

# Install your program now...

# AFTER installing
.\TrackInstallation.ps1 -Mode after
```

---

## How to Know Where Programs Install

### Method 1: Check the Installer Type

| Installer Type | Where It Installs | Config Location | Needs Admin? |
|----------------|-------------------|-----------------|--------------|
| **MSI** (.msi) | `C:\Program Files` | `%APPDATA%` or `C:\ProgramData` | ✅ Yes |
| **EXE** (setup.exe) | `C:\Program Files` or `%LOCALAPPDATA%\Programs` | `%APPDATA%` or `%LOCALAPPDATA%` | ❌ Usually No |
| **Portable** (.zip) | Wherever you extract | Same folder or `%APPDATA%` | ❌ No |
| **Microsoft Store** | `C:\Program Files\WindowsApps` | `%LOCALAPPDATA%\Packages` | ❌ No |
| **Chocolatey** | `C:\ProgramData\chocolatey\lib` | `C:\ProgramData\chocolatey` | ✅ Yes |
| **Scoop** | `%USERPROFILE%\scoop\apps` | `%USERPROFILE%\scoop\persist` | ❌ No |
| **NPM** | `%APPDATA%\npm\node_modules` | `%USERPROFILE%\.npmrc` | ❌ No |
| **pip/Python** | `Python\Scripts` or `Lib\site-packages` | `%APPDATA%\Python` | ❌ No |

### Method 2: Read the Installer

**During installation**, most installers show you:
1. **"Choose Install Location"** screen → This is where the program goes
2. **Progress screen** often shows: "Installing to C:\..."
3. Check "Show Details" or "Advanced" options

**Signs you can control location:**
- ✅ "Choose installation directory" button
- ✅ "Custom installation" option
- ❌ "Express installation" usually = no choice

### Method 3: AI Tool Common Patterns

Most AI tools follow these patterns:

**CLI/Agent Tools:**
```
C:\Users\YC\.toolname          (config)
%APPDATA%\toolname             (settings)
%LOCALAPPDATA%\toolname        (cache)
```

**GUI Applications:**
```
%LOCALAPPDATA%\Programs\toolname    (program)
%APPDATA%\toolname                  (config)
```

**Examples:**
- Claude Desktop: `%LOCALAPPDATA%\Anthropic\Claude` + `%APPDATA%\.claude`
- Cursor: `%LOCALAPPDATA%\Programs\cursor` + `C:\Users\YC\.cursor`
- Ollama: `C:\Program Files\Ollama` + `C:\Users\YC\.ollama`
- Zed: `%LOCALAPPDATA%\Zed` + `%APPDATA%\Zed`

---

## Using TrackInstallation.ps1

### Interactive Menu Mode
```powershell
.\TrackInstallation.ps1
```

**Options:**
1. **Track installation** - Before/After comparison
2. **Show common locations** - Where AI tools typically install
3. **Predict installation** - Answer questions to predict location
4. **Installer guide** - Reference table

### Track a New Installation

**Step 1: Before snapshot**
```powershell
.\TrackInstallation.ps1 -Mode before
```

**Step 2: Install your program**
- Run the installer
- Complete installation
- Don't restart yet

**Step 3: After snapshot**
```powershell
.\TrackInstallation.ps1 -Mode after
```

**Output shows:**
- All new folders created
- Full paths
- Suggested junction commands
- Detection of AI-related keywords

**Example output:**
```
Found 2 new folders:

Location: C:\Users\YC\AppData\Local\Programs
  • NewAITool
    Path: C:\Users\YC\AppData\Local\Programs\NewAITool
    Created: 2026-01-31 10:30:15
    → Looks like an AI tool! Consider linking to AI_hub

Location: C:\Users\YC\AppData\Roaming
  • NewAITool
    Path: C:\Users\YC\AppData\Roaming\NewAITool
    Created: 2026-01-31 10:30:16

Suggested Junction Commands:
mklink /J "C:\Users\YC\AI_hub\NewAITool_AppData_Local" "C:\Users\YC\AppData\Local\Programs\NewAITool"
mklink /J "C:\Users\YC\AI_hub\NewAITool_AppData_Roaming" "C:\Users\YC\AppData\Roaming\NewAITool"
```

### Predict Before Installing

```powershell
.\TrackInstallation.ps1 -Mode predict
```

**Answer questions:**
- Installer type (MSI, EXE, ZIP, etc.)
- Package manager (if applicable)

**Get prediction:**
- Where program files will go
- Where configs will be stored
- Whether admin rights needed

---

## Using WatchHub_Realtime.ps1

### Basic Usage

**Start monitoring:**
```powershell
cd C:\Users\YC\AI_hub
.\WatchHub_Realtime.ps1
```

**What it monitors:**
- `C:\Users\YC` (dotfiles like `.claude`, `.cursor`)
- `%APPDATA%` (Roaming application data)
- `%LOCALAPPDATA%` (Local application data)
- `%LOCALAPPDATA%\Programs` (User-installed programs)
- `C:\GitHubRepo` (your projects)
- `C:\` (root dotfiles)

**What happens when new folder appears:**
1. **Instant detection** (milliseconds)
2. **AI keyword check** (claude, ollama, mcp, etc.)
3. **Auto-create junction** in AI_hub
4. **Update Obsidian** inventory
5. **Log to** `discovery.log`

### Verbose Mode

```powershell
.\WatchHub_Realtime.ps1 -Verbose
```

Shows all activity, even non-AI folders.

### Run at Startup

**Option A: Task Scheduler**
```powershell
$action = New-ScheduledTaskAction `
    -Execute "PowerShell.exe" `
    -Argument "-WindowStyle Hidden -File C:\Users\YC\AI_hub\WatchHub_Realtime.ps1"

$trigger = New-ScheduledTaskTrigger -AtLogon

Register-ScheduledTask `
    -TaskName "AI Hub Real-Time Monitor" `
    -Action $action `
    -Trigger $trigger `
    -RunLevel Highest
```

**Option B: Startup Folder**
1. Press `Win+R`, type `shell:startup`, press Enter
2. Create shortcut to `WatchHub_Realtime.ps1`
3. Edit shortcut properties:
   - Target: `powershell.exe -WindowStyle Hidden -File C:\Users\YC\AI_hub\WatchHub_Realtime.ps1`

---

## Monitoring Locations Reference

### Expanded Variables

| Variable | Actual Path |
|----------|-------------|
| `%USERPROFILE%` | `C:\Users\YC` |
| `%APPDATA%` | `C:\Users\YC\AppData\Roaming` |
| `%LOCALAPPDATA%` | `C:\Users\YC\AppData\Local` |
| `%PROGRAMFILES%` | `C:\Program Files` |
| `%PROGRAMFILES(X86)%` | `C:\Program Files (x86)` |
| `%PROGRAMDATA%` | `C:\ProgramData` |
| `%TEMP%` | `C:\Users\YC\AppData\Local\Temp` |

### AI Tool Patterns

**Config files (home directory):**
```
C:\Users\YC\.claude
C:\Users\YC\.cursor
C:\Users\YC\.ollama
C:\Users\YC\.config
C:\Users\YC\.anthropic
```

**Roaming data:**
```
C:\Users\YC\AppData\Roaming\Code
C:\Users\YC\AppData\Roaming\cursor
C:\Users\YC\AppData\Roaming\Zed
C:\Users\YC\AppData\Roaming\obsidian
```

**Local programs:**
```
C:\Users\YC\AppData\Local\Programs\cursor
C:\Users\YC\AppData\Local\Programs\windsurf
C:\Users\YC\AppData\Local\Programs\Microsoft VS Code
```

**Local data:**
```
C:\Users\YC\AppData\Local\Anthropic
C:\Users\YC\AppData\Local\Ollama
C:\Users\YC\AppData\Local\Claude
```

**System programs:**
```
C:\Program Files\Ollama
C:\Program Files\Python312
C:\Program Files\Git
```

---

## Troubleshooting

### "Nothing detected after installation"

**Possible reasons:**
1. Program installed to non-monitored location
2. Program modified existing folders instead of creating new ones
3. Program is portable (no installation needed)

**Solutions:**
- Check `C:\Program Files` manually
- Check installer's own log files
- Look in Windows Registry: `HKEY_LOCAL_MACHINE\SOFTWARE` or `HKEY_CURRENT_USER\SOFTWARE`
- Use Process Monitor (from Sysinternals) during installation

### "WatchHub not creating junctions"

**Check:**
1. Is the folder name matching AI keywords?
2. Run WatchHub with `-Verbose` flag
3. Check `C:\Users\YC\AI_hub\discovery.log`
4. Verify junction creation permission (should not need admin)

**Manual junction creation:**
```powershell
mklink /J "C:\Users\YC\AI_hub\ToolName_Category" "C:\Path\To\Tool"
```

### "Want to add custom keywords"

Edit `WatchHub_Realtime.ps1`, find:
```powershell
$aiKeywords = @(
    'claude', 'cursor', 'zed', 'ollama', ...
)
```

Add your keywords, restart the watcher.

---

## Integration with AI_hub

### Update Hub.ps1 Menu

Add to your `Hub.ps1`:

```powershell
# In the menu section
Write-Host "  [10] Start Real-Time Monitor" -ForegroundColor Cyan
Write-Host "  [11] Track Installation" -ForegroundColor Cyan

# In the switch statement
case "10":
    Start-Process powershell -ArgumentList "-NoExit", "-File", "$PSScriptRoot\WatchHub_Realtime.ps1"
    break

case "11":
    & "$PSScriptRoot\TrackInstallation.ps1"
    break
```

### Auto-Export to Obsidian

WatchHub already does this! Every new junction triggers:
```powershell
.\ExportToObsidian.ps1
```

Your `AI_Hub_Inventory_AUTO.md` stays up-to-date automatically.

---

## Best Practices

### Daily Workflow

**Morning:**
```powershell
# Start the real-time watcher
.\WatchHub_Realtime.ps1
```

**When installing new tool:**
- Just install normally
- Watcher auto-detects within seconds
- Check `.\Hub.ps1 agents` to verify

**Evening:**
- Check `discovery.log` for new tools
- Review Obsidian inventory
- Watcher keeps running overnight

### Weekly Maintenance

```powershell
# Check what's been discovered
Get-Content C:\Users\YC\AI_hub\discovery.log -Tail 50

# Verify all junctions are valid
Get-ChildItem C:\Users\YC\AI_hub | Where-Object { $_.Attributes -match "ReparsePoint" }

# Export fresh inventory
.\Hub.ps1 obsidian
```

---

## Advanced: Process Monitor Method

For the most detailed installation tracking:

1. **Download Process Monitor** (Sysinternals)
2. **Before installing:**
   - Start Process Monitor
   - Add filter: `Operation is CreateFile`
   - Add filter: `Path contains C:\`
3. **Install program**
4. **Stop capture**
5. **Search for:**
   - Program name
   - Common paths (`AppData`, `Program Files`)

Process Monitor shows **every** file/folder created.

---

## Summary

**For automatic detection:**
→ Use `WatchHub_Realtime.ps1` (always running)

**For manual tracking:**
→ Use `TrackInstallation.ps1` before/after

**To predict before installing:**
→ Use `TrackInstallation.ps1 -Mode predict`
→ Check installer type guide

**Integration:**
→ Both tools work with your AI_hub system
→ Auto-create junctions
→ Auto-update Obsidian

---

*Last updated: 2026-01-31*
