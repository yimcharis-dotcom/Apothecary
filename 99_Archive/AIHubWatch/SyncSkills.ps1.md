# SyncSkills.ps1
# Copy skills from one agent to all others (simpler than npx skills)

param(
    [Parameter(Mandatory=$false)]
    [string]$SourceAgent = "Claude_User_Dot",

    [Parameter(Mandatory=$false)]
    [string]$SkillName = "*"  # Default: all skills
)

$HubDir = "C:\Users\YC\AI_hub"

# Get source skills directory
$sourcePath = Join-Path $HubDir $SourceAgent
$sourceSkillsDir = Join-Path $sourcePath "skills"

if (-not (Test-Path $sourceSkillsDir)) {
    Write-Host "ERROR: $SourceAgent has no skills directory!" -ForegroundColor Red
    exit 1
}

# Get skills to copy
$skillsToCopy = Get-ChildItem -Path $sourceSkillsDir -Directory -Filter $SkillName

if ($skillsToCopy.Count -eq 0) {
    Write-Host "No skills matching '$SkillName' found in $SourceAgent" -ForegroundColor Yellow
    exit 0
}

Write-Host "`n=== Syncing from $SourceAgent ===" -ForegroundColor Cyan
Write-Host "Skills to sync: $($skillsToCopy.Name -join ', ')" -ForegroundColor White

# Find all agents with skills directories
$targetAgents = Get-ChildItem -Path $HubDir -Directory | Where-Object {
    $skillsPath = Join-Path $_.FullName "skills"
    ($_.Name -ne $SourceAgent) -and (Test-Path $skillsPath)
}

$copiedCount = 0
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
            Write-Host "  + $($skill.Name) [copying...]" -ForegroundColor Yellow
            Copy-Item -Path $skill.FullName -Destination $targetPath -Recurse -Force
            $copiedCount++
        }
    }
}

Write-Host "`n=== Summary ===" -ForegroundColor Cyan
Write-Host "Copied: $copiedCount | Skipped: $skippedCount" -ForegroundColor White

# Usage examples
Write-Host "`nUsage examples:" -ForegroundColor DarkGray
Write-Host "  .\SyncSkills.ps1" -ForegroundColor DarkGray
Write-Host "  .\SyncSkills.ps1 -SourceAgent 'Cursor_User_Dot'" -ForegroundColor DarkGray
Write-Host "  .\SyncSkills.ps1 -SkillName 'excel-editor'" -ForegroundColor DarkGray
