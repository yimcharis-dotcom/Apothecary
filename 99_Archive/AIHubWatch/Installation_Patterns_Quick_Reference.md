# Windows Installation Patterns - Quick Reference

## Where Programs Install (By Installer Type)

```
┌─────────────────────────────────────────────────────────────────────┐
│ MSI Installer (.msi)                                                │
├─────────────────────────────────────────────────────────────────────┤
│ Program:  C:\Program Files\[AppName]                                │
│ Config:   C:\ProgramData\[AppName]                                  │
│           %APPDATA%\[AppName]                                       │
│ Admin:    ✅ Required                                               │
│ Examples: Microsoft Office, Adobe products, enterprise software     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ EXE Installer (setup.exe)                                           │
├─────────────────────────────────────────────────────────────────────┤
│ Program:  %LOCALAPPDATA%\Programs\[AppName]  (user install)         │
│           C:\Program Files\[AppName]          (system install)      │
│ Config:   %APPDATA%\[AppName]                                       │
│           %LOCALAPPDATA%\[AppName]                                  │
│ Admin:    ❌ Usually not required                                   │
│ Examples: VSCode, Cursor, Discord, Slack                            │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ Microsoft Store Apps                                                │
├─────────────────────────────────────────────────────────────────────┤
│ Program:  C:\Program Files\WindowsApps\[PackageFullName]           │
│ Config:   %LOCALAPPDATA%\Packages\[PackageFullName]                │
│ Admin:    ❌ Not required                                           │
│ Note:     WindowsApps folder is hidden/protected                    │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ Portable Apps (.zip, .7z)                                           │
├─────────────────────────────────────────────────────────────────────┤
│ Program:  [Anywhere you extract]                                    │
│ Config:   Same folder as .exe OR                                    │
│           %APPDATA%\[AppName]                                       │
│ Admin:    ❌ Not required                                           │
│ Examples: Notepad++, 7-Zip portable, many dev tools                │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ Chocolatey (choco install)                                          │
├─────────────────────────────────────────────────────────────────────┤
│ Program:  C:\ProgramData\chocolatey\lib\[package]                  │
│ Binary:   C:\ProgramData\chocolatey\bin                            │
│ Config:   C:\ProgramData\chocolatey\config                         │
│ Admin:    ✅ Required                                               │
│ Note:     System-wide installation                                 │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ Scoop (scoop install)                                               │
├─────────────────────────────────────────────────────────────────────┤
│ Program:  %USERPROFILE%\scoop\apps\[package]\current               │
│ Persist:  %USERPROFILE%\scoop\persist\[package]                    │
│ Global:   C:\ProgramData\scoop (if installed with -g)              │
│ Admin:    ❌ Not required (unless -g flag)                          │
│ Note:     User-scoped, portable-style apps                         │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ NPM Global (npm install -g)                                         │
├─────────────────────────────────────────────────────────────────────┤
│ Modules:  %APPDATA%\npm\node_modules\[package]                     │
│ Binary:   %APPDATA%\npm                                             │
│ Config:   %USERPROFILE%\.npmrc                                      │
│ Cache:    %APPDATA%\npm-cache                                       │
│ Admin:    ❌ Not required                                           │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ Python pip (pip install)                                            │
├─────────────────────────────────────────────────────────────────────┤
│ Packages: [PythonInstall]\Lib\site-packages                        │
│ Scripts:  [PythonInstall]\Scripts                                  │
│ Config:   %APPDATA%\Python                                          │
│           %USERPROFILE%\.config\pip                                 │
│ Admin:    ❌ Not required (user install)                            │
└─────────────────────────────────────────────────────────────────────┘
```

## AI Tool Specific Patterns

```
┌─────────────────────────────────────────────────────────────────────┐
│ Claude Desktop (Anthropic)                                          │
├─────────────────────────────────────────────────────────────────────┤
│ %LOCALAPPDATA%\Anthropic\Claude    → Program files                 │
│ %APPDATA%\.claude                  → Config/skills                  │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ Cursor                                                              │
├─────────────────────────────────────────────────────────────────────┤
│ %LOCALAPPDATA%\Programs\cursor     → Program files                 │
│ %APPDATA%\Cursor                   → Settings/extensions            │
│ %USERPROFILE%\.cursor              → User config                    │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ Windsurf                                                            │
├─────────────────────────────────────────────────────────────────────┤
│ %LOCALAPPDATA%\Programs\windsurf   → Program files                 │
│ %APPDATA%\Windsurf                 → Settings/extensions            │
│ %USERPROFILE%\.windsurf            → User config                    │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ VS Code                                                             │
├─────────────────────────────────────────────────────────────────────┤
│ %LOCALAPPDATA%\Programs\Microsoft VS Code → Program                │
│ %APPDATA%\Code                             → Settings/extensions    │
│ %USERPROFILE%\.vscode                      → User extensions        │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ Ollama                                                              │
├─────────────────────────────────────────────────────────────────────┤
│ C:\Program Files\Ollama            → Program files                  │
│ %USERPROFILE%\.ollama              → Models/config                  │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ Zed                                                                 │
├─────────────────────────────────────────────────────────────────────┤
│ %LOCALAPPDATA%\Zed                 → Program files                  │
│ %APPDATA%\Zed                      → Settings/extensions            │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ Obsidian                                                            │
├─────────────────────────────────────────────────────────────────────┤
│ %APPDATA%\obsidian                 → Settings/plugins               │
│ [User chosen location]             → Vaults                         │
└─────────────────────────────────────────────────────────────────────┘
```

## Path Variables Expansion

```
%USERPROFILE%              → C:\Users\YC
%APPDATA%                  → C:\Users\YC\AppData\Roaming
%LOCALAPPDATA%             → C:\Users\YC\AppData\Local
%PROGRAMFILES%             → C:\Program Files
%PROGRAMFILES(X86)%        → C:\Program Files (x86)
%PROGRAMDATA%              → C:\ProgramData
%TEMP% or %TMP%            → C:\Users\YC\AppData\Local\Temp
%WINDIR%                   → C:\Windows
%SYSTEMROOT%               → C:\Windows
%PUBLIC%                   → C:\Users\Public
```

## Common Config File Locations

```
Global/System:
  C:\ProgramData\[AppName]
  C:\Windows\System32\config

User-Specific:
  %APPDATA%\[AppName]              → Roaming profile
  %LOCALAPPDATA%\[AppName]         → Local only
  %USERPROFILE%\.[appname]         → Dotfile config
  %USERPROFILE%\.config\[appname]  → XDG-style config
```

## Installation Detection Checklist

**Before Installing:**
```
□ Note the installer type (.msi, .exe, .zip, Store, etc.)
□ Run: .\TrackInstallation.ps1 -Mode before
□ Check if installer offers "Choose location" option
```

**During Installation:**
```
□ Watch for "Installing to: C:\..." messages
□ Note any "This will install to..." notifications
□ Check if admin elevation prompt appears
```

**After Installing:**
```
□ Run: .\TrackInstallation.ps1 -Mode after
□ Check Program Files folders
□ Check AppData folders
□ Check home directory for dotfiles
□ Search Windows Start Menu for shortcut (right-click → Properties shows path)
```

## Quick Commands

**Find installed programs:**
```powershell
# List Program Files
Get-ChildItem "C:\Program Files"
Get-ChildItem "C:\Program Files (x86)"

# List AppData Programs
Get-ChildItem "$env:LOCALAPPDATA\Programs"

# List dotfiles in home
Get-ChildItem $env:USERPROFILE -Force | Where-Object Name -like ".*"

# Find by name
Get-ChildItem C:\ -Recurse -Directory -Filter "*claude*" -ErrorAction SilentlyContinue
```

**Check install location from shortcut:**
```powershell
$shortcut = (New-Object -ComObject WScript.Shell).CreateShortcut("$env:APPDATA\Microsoft\Windows\Start Menu\Programs\AppName.lnk")
$shortcut.TargetPath
```

**Registry lookups:**
```powershell
# Installed programs
Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*

# User installed programs
Get-ItemProperty HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*
```

## Signs of Installation Location

**Admin required → System-wide:**
- Likely: `C:\Program Files`
- Config: `C:\ProgramData` or `%APPDATA%`

**No admin → User-scoped:**
- Likely: `%LOCALAPPDATA%\Programs`
- Config: `%APPDATA%` or home directory

**Installer shows custom path:**
- You choose the location
- Config might still go to standard paths

**Portable (no installer):**
- Runs from extracted folder
- May create config in `%APPDATA%` or same folder

---

## Pro Tips

**Want control over install location?**
1. Look for "Custom" or "Advanced" install option
2. Avoid "Express" or "Quick" install
3. Some installers let you change path mid-install

**Can't find where program installed?**
```powershell
# Search recent files
Get-ChildItem C:\ -Recurse -Directory | 
  Where-Object CreationTime -gt (Get-Date).AddHours(-1) |
  Sort-Object CreationTime -Descending

# Process Monitor from Sysinternals
# Download: https://learn.microsoft.com/en-us/sysinternals/downloads/procmon
```

**Make portable apps easier:**
Consider using:
- **Scoop** for developer tools
- **Chocolatey** for system tools
- Both keep everything organized in known locations

---

*Print this and keep it handy!*
*Last updated: 2026-01-31*
