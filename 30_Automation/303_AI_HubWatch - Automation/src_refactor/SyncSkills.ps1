# SyncSkills.ps1
# Symlink skills from source agent to all others
# v2: Uses symlinks instead of copies + supports deletion
# v3: + Shared config + Skill validation + Portable paths
# v4: + Agent validation + Security checks
# v5: + Uses shared functions from AIToolsConfig.ps1

param(
    [Parameter(Mandatory=$false)]
    [string]$SourceAgent = "Claude_User_Dot",

    [Parameter(Mandatory=$false)]
    [string]$SkillName = "*",  # Default: all skills

    [Parameter(Mandatory=$false)]
    [switch]$Delete,  # Remove symlinks instead of creating

    [Parameter(Mandatory=$false)]
    [switch]$SkipValidation,  # Skip skill file validation

    [Parameter(Mandatory=$false)]
    [switch]$SkipSecurity,  # Skip security checks (dangerous file detection)

    [Parameter(Mandatory=$false)]
    [switch]$SkipAgentValidation  # Skip agent identity validation
)

# Load shared config (provides Test-IsValidSkill, Test-SkillSecurity, Test-IsValidAgent, $DangerousExtensions)
$configPath = Join-Path $PSScriptRoot "AIToolsConfig.ps1"
$configLoaded = $false
if (Test-Path $configPath) {
    . $configPath
    $configLoaded = $true
}

$HubDir = if ($script:HubDir) { $script:HubDir } elseif ($env:AI_HUB_PATH) { $env:AI_HUB_PATH } else { "$env:USERPROFILE\AI_hub" }

# Use shared dangerous extensions or fallback
$dangerousExts = if ($script:DangerousExtensions) { $script:DangerousExtensions } else {
    @(".exe", ".msi", ".bat", ".cmd", ".com", ".vbs", ".ps1", ".dll", ".scr")
}

# Wrapper functions that use shared config or fallback to local implementation
function Test-ValidSkillWrapper {
    param([string]$SkillPath)
    if ($configLoaded -and (Get-Command Test-IsValidSkill -ErrorAction SilentlyContinue)) {
        return Test-IsValidSkill -SkillPath $SkillPath
    }
    # Fallback
    $signatures = @("skill.json", "package.json", "index.js", "index.ts", "main.py", "__init__.py", "skill.yaml", "skill.yml")
    foreach ($sig in $signatures) {
        if (Test-Path (Join-Path $SkillPath $sig)) { return $true }
    }
    $items = Get-ChildItem -Path $SkillPath -ErrorAction SilentlyContinue
    return $items.Count -gt 0
}

function Test-SkillSecurityWrapper {
    param([string]$SkillPath)
    if ($configLoaded -and (Get-Command Test-SkillSecurity -ErrorAction SilentlyContinue)) {
        return Test-SkillSecurity -SkillPath $SkillPath
    }
    # Fallback
    $dangerous = Get-ChildItem -Path $SkillPath -Recurse -File -ErrorAction SilentlyContinue |
        Where-Object { $dangerousExts -contains $_.Extension.ToLower() }
    return @{
        IsSafe = ($dangerous.Count -eq 0)
        DangerousFiles = $dangerous
        Warnings = @()
    }
}

function Test-ValidAgentWrapper {
    param([string]$AgentPath)
    if ($configLoaded -and (Get-Command Test-IsValidAgent -ErrorAction SilentlyContinue)) {
        $result = Test-IsValidAgent -AgentPath $AgentPath
        return $result.IsValid
    }
    # Fallback - check for config files or name pattern
    $configSignatures = @("settings.json", "config.json", "claude_desktop_config.json", "extensions.json", "hosts.json", "keymap.json", "state.vscdb")
    foreach ($sig in $configSignatures) {
        if (Test-Path (Join-Path $AgentPath $sig)) { return $true }
    }
    $folderName = Split-Path $AgentPath -Leaf
    $aiPatterns = @("claude", "cursor", "zed", "ollama", "copilot", "cody", "continue", "anthropic", "code", "vscode")
    foreach ($pattern in $aiPatterns) {
        if ($folderName -like "*$pattern*") { return $true }
    }
    return $false
}

# Get source skills directory
$sourcePath = Join-Path $HubDir $SourceAgent
$sourceSkillsDir = Join-Path $sourcePath "skills"

if (-not (Test-Path $sourceSkillsDir)) {
    Write-Host "ERROR: $SourceAgent has no skills directory!" -ForegroundColor Red
    exit 1
}

# Find all agents with skills directories
$allPotentialAgents = Get-ChildItem -Path $HubDir -Directory | Where-Object {
    $skillsPath = Join-Path $_.FullName "skills"
    ($_.Name -ne $SourceAgent) -and (Test-Path $skillsPath)
}

# Validate agents (unless -SkipAgentValidation)
$targetAgents = @()
$invalidAgents = @()

foreach ($agent in $allPotentialAgents) {
    if ($SkipAgentValidation -or (Test-ValidAgentWrapper -AgentPath $agent.FullName)) {
        $targetAgents += $agent
    } else {
        $invalidAgents += $agent
    }
}

if ($invalidAgents.Count -gt 0) {
    Write-Host "`nSkipped non-AI agents: $($invalidAgents.Name -join ', ')" -ForegroundColor DarkYellow
}

if ($Delete) {
    # ============================================================
    # DELETE MODE - Remove symlinks for specified skill
    # ============================================================
    Write-Host "`n=== Removing skill symlinks: $SkillName ===" -ForegroundColor Red

    $removedCount = 0

    foreach ($agent in $targetAgents) {
        $targetSkillsDir = Join-Path $agent.FullName "skills"
        $targetPath = Join-Path $targetSkillsDir $SkillName

        if (Test-Path $targetPath) {
            # Check if it's a symlink
            $item = Get-Item $targetPath -Force
            if ($item.Attributes -match "ReparsePoint") {
                cmd /c rmdir "$targetPath" 2>&1 | Out-Null
                Write-Host "  - $($agent.Name): removed symlink" -ForegroundColor Yellow
                $removedCount++
            } else {
                Write-Host "  - $($agent.Name): not a symlink, skipped" -ForegroundColor DarkGray
            }
        }
    }

    Write-Host "`nRemoved $removedCount symlinks" -ForegroundColor Red

} else {
    # ============================================================
    # ADD MODE - Create symlinks for skills
    # ============================================================

    # Get skills to sync
    $skillsToCopy = Get-ChildItem -Path $sourceSkillsDir -Directory -Filter $SkillName

    if ($skillsToCopy.Count -eq 0) {
        Write-Host "No skills matching '$SkillName' found in $SourceAgent" -ForegroundColor Yellow
        exit 0
    }

    # Validate skills before syncing (unless -SkipValidation)
    $validSkills = @()
    $invalidSkills = @()
    $unsafeSkills = @()

    foreach ($skill in $skillsToCopy) {
        # Check validity (uses shared Test-IsValidSkill or fallback)
        $isValid = $SkipValidation -or (Test-ValidSkillWrapper -SkillPath $skill.FullName)

        if (-not $isValid) {
            $invalidSkills += $skill
            continue
        }

        # Security check (uses shared Test-SkillSecurity or fallback)
        if (-not $SkipSecurity) {
            $secCheck = Test-SkillSecurityWrapper -SkillPath $skill.FullName
            if (-not $secCheck.IsSafe) {
                $unsafeSkills += @{ Skill = $skill; Files = $secCheck.DangerousFiles }
                continue
            }
        }

        $validSkills += $skill
    }

    Write-Host "`n=== Syncing from $SourceAgent (symlinks) ===" -ForegroundColor Cyan
    Write-Host "Valid skills: $($validSkills.Name -join ', ')" -ForegroundColor White
    if ($invalidSkills.Count -gt 0) {
        Write-Host "Invalid (skipped): $($invalidSkills.Name -join ', ')" -ForegroundColor DarkYellow
    }
    if ($unsafeSkills.Count -gt 0) {
        Write-Host "UNSAFE (blocked): $($unsafeSkills.Skill.Name -join ', ')" -ForegroundColor Red
        foreach ($unsafe in $unsafeSkills) {
            Write-Host "  $($unsafe.Skill.Name) contains:" -ForegroundColor Red
            foreach ($df in $unsafe.Files) {
                Write-Host "    - $($df.Name)" -ForegroundColor DarkRed
            }
        }
    }

    if ($validSkills.Count -eq 0) {
        Write-Host "No valid skills to sync" -ForegroundColor Yellow
        exit 0
    }

    $linkedCount = 0
    $skippedCount = 0

    foreach ($agent in $targetAgents) {
        $targetSkillsDir = Join-Path $agent.FullName "skills"

        Write-Host "`n$($agent.Name):" -ForegroundColor Green

        foreach ($skill in $validSkills) {
            $targetPath = Join-Path $targetSkillsDir $skill.Name

            if (Test-Path $targetPath) {
                Write-Host "  - $($skill.Name) [already exists]" -ForegroundColor DarkGray
                $skippedCount++
            } else {
                # Create symlink (directory symlink)
                $result = cmd /c mklink /D "$targetPath" "$($skill.FullName)" 2>&1

                if ($LASTEXITCODE -eq 0) {
                    Write-Host "  + $($skill.Name) [symlinked]" -ForegroundColor Green
                    $linkedCount++
                } else {
                    Write-Host "  ! $($skill.Name) [failed: $result]" -ForegroundColor Red
                }
            }
        }
    }

    Write-Host "`n=== Summary ===" -ForegroundColor Cyan
    Write-Host "Symlinked: $linkedCount | Skipped: $skippedCount | Invalid: $($invalidSkills.Count) | Unsafe: $($unsafeSkills.Count)" -ForegroundColor White
    if ($invalidAgents.Count -gt 0) {
        Write-Host "Non-AI agents skipped: $($invalidAgents.Count)" -ForegroundColor DarkGray
    }
}

# Usage examples
Write-Host "`nUsage:" -ForegroundColor DarkGray
Write-Host "  .\SyncSkills.ps1                           # Symlink all valid skills" -ForegroundColor DarkGray
Write-Host "  .\SyncSkills.ps1 -SkillName 'my-skill'     # Symlink one skill" -ForegroundColor DarkGray
Write-Host "  .\SyncSkills.ps1 -SkillName 'old' -Delete  # Remove symlinks" -ForegroundColor DarkGray
Write-Host "  .\SyncSkills.ps1 -SkipValidation           # Skip skill file validation" -ForegroundColor DarkGray
Write-Host "  .\SyncSkills.ps1 -SkipSecurity             # Skip dangerous file check" -ForegroundColor DarkGray
Write-Host "  .\SyncSkills.ps1 -SkipAgentValidation      # Sync to ALL folders with skills/" -ForegroundColor DarkGray
