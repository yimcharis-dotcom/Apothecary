# SyncSkills.ps1
# Symlink skills from source agent to all others
# v2: Uses symlinks instead of copies + supports deletion
# v3: + Shared config + Skill validation + Portable paths

param(
    [Parameter(Mandatory=$false)]
    [string]$SourceAgent = "Claude_User_Dot",

    [Parameter(Mandatory=$false)]
    [string]$SkillName = "*",  # Default: all skills

    [Parameter(Mandatory=$false)]
    [switch]$Delete,  # Remove symlinks instead of creating

    [Parameter(Mandatory=$false)]
    [switch]$SkipValidation  # Skip skill file validation
)

# Load shared config
$configPath = Join-Path $PSScriptRoot "AIToolsConfig.ps1"
if (Test-Path $configPath) {
    . $configPath
}

$HubDir = if ($script:HubDir) { $script:HubDir } elseif ($env:AI_HUB_PATH) { $env:AI_HUB_PATH } else { "$env:USERPROFILE\AI_hub" }

# Skill validation function
function Test-ValidSkill {
    param([string]$SkillPath)
    $signatures = @("skill.json", "package.json", "index.js", "index.ts", "main.py", "__init__.py", "skill.yaml", "skill.yml")
    foreach ($sig in $signatures) {
        if (Test-Path (Join-Path $SkillPath $sig)) { return $true }
    }
    # Fallback: check if folder has any content
    $items = Get-ChildItem -Path $SkillPath -ErrorAction SilentlyContinue
    return $items.Count -gt 0
}

# Get source skills directory
$sourcePath = Join-Path $HubDir $SourceAgent
$sourceSkillsDir = Join-Path $sourcePath "skills"

if (-not (Test-Path $sourceSkillsDir)) {
    Write-Host "ERROR: $SourceAgent has no skills directory!" -ForegroundColor Red
    exit 1
}

# Find all agents with skills directories
$targetAgents = Get-ChildItem -Path $HubDir -Directory | Where-Object {
    $skillsPath = Join-Path $_.FullName "skills"
    ($_.Name -ne $SourceAgent) -and (Test-Path $skillsPath)
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
    foreach ($skill in $skillsToCopy) {
        if ($SkipValidation -or (Test-ValidSkill -SkillPath $skill.FullName)) {
            $validSkills += $skill
        } else {
            $invalidSkills += $skill
        }
    }

    Write-Host "`n=== Syncing from $SourceAgent (symlinks) ===" -ForegroundColor Cyan
    Write-Host "Valid skills: $($validSkills.Name -join ', ')" -ForegroundColor White
    if ($invalidSkills.Count -gt 0) {
        Write-Host "Invalid (skipped): $($invalidSkills.Name -join ', ')" -ForegroundColor DarkYellow
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
    Write-Host "Symlinked: $linkedCount | Skipped: $skippedCount | Invalid: $($invalidSkills.Count)" -ForegroundColor White
}

# Usage examples
Write-Host "`nUsage:" -ForegroundColor DarkGray
Write-Host "  .\SyncSkills.ps1                           # Symlink all valid skills" -ForegroundColor DarkGray
Write-Host "  .\SyncSkills.ps1 -SkillName 'excel-editor' # Symlink one skill" -ForegroundColor DarkGray
Write-Host "  .\SyncSkills.ps1 -SkillName 'old-skill' -Delete  # Remove symlinks" -ForegroundColor DarkGray
Write-Host "  .\SyncSkills.ps1 -SkipValidation           # Skip skill file validation" -ForegroundColor DarkGray
