# SyncSkills.ps1
# Symlink skills from source agent to all others
# v2: Uses symlinks instead of copies + supports deletion

param(
    [Parameter(Mandatory=$false)]
    [string]$SourceAgent = "Claude_User_Dot",

    [Parameter(Mandatory=$false)]
    [string]$SkillName = "*",  # Default: all skills

    [Parameter(Mandatory=$false)]
    [switch]$Delete  # Remove symlinks instead of creating
)

$HubDir = "C:\Users\YC\AI_hub"

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

    Write-Host "`n=== Syncing from $SourceAgent (symlinks) ===" -ForegroundColor Cyan
    Write-Host "Skills to sync: $($skillsToCopy.Name -join ', ')" -ForegroundColor White

    $linkedCount = 0
    $skippedCount = 0

    foreach ($agent in $targetAgents) {
        $targetSkillsDir = Join-Path $agent.FullName "skills"

        Write-Host "`n$($agent.Name):" -ForegroundColor Green

        foreach ($skill in $skillsToCopy) {
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
    Write-Host "Symlinked: $linkedCount | Skipped: $skippedCount" -ForegroundColor White
}

# Usage examples
Write-Host "`nUsage:" -ForegroundColor DarkGray
Write-Host "  .\SyncSkills.ps1                           # Symlink all skills" -ForegroundColor DarkGray
Write-Host "  .\SyncSkills.ps1 -SkillName 'excel-editor' # Symlink one skill" -ForegroundColor DarkGray
Write-Host "  .\SyncSkills.ps1 -SkillName 'old-skill' -Delete  # Remove symlinks" -ForegroundColor DarkGray
