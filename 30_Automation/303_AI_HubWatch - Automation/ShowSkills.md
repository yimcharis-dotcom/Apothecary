```
# ShowSkills.ps1
# Quick inventory of skills across all AI agents in the Hub

$HubDir = "C:\Users\YC\AI_hub"

Write-Host "`n=== Skills Inventory ===" -ForegroundColor Cyan

# Get all symlinks that have skills directories
$agentsWithSkills = Get-ChildItem -Path $HubDir -Directory | Where-Object {
    $skillsPath = Join-Path $_.FullName "skills"
    Test-Path $skillsPath
}

# Collect all unique skills
$skillsIndex = @{}
$agentCount = 0

foreach ($agent in $agentsWithSkills) {
    $agentCount++
    $skillsPath = Join-Path $agent.FullName "skills"
    $skills = Get-ChildItem -Path $skillsPath -Directory -ErrorAction SilentlyContinue

    Write-Host "`n$($agent.Name):" -ForegroundColor Green

    if ($skills.Count -eq 0) {
        Write-Host "  (no skills)" -ForegroundColor DarkGray
    } else {
        foreach ($skill in $skills) {
            Write-Host "  - $($skill.Name)" -ForegroundColor White

            # Track which agents have this skill
            if (-not $skillsIndex.ContainsKey($skill.Name)) {
                $skillsIndex[$skill.Name] = @()
            }
            $skillsIndex[$skill.Name] += $agent.Name
        }
    }
}

# Summary
Write-Host "`n=== Summary ===" -ForegroundColor Cyan
Write-Host "Total agents with skills: $agentCount"
Write-Host "Unique skills found: $($skillsIndex.Count)"

Write-Host "`n=== Skills Distribution ===" -ForegroundColor Cyan
$skillsIndex.GetEnumerator() | Sort-Object { $_.Value.Count } -Descending | ForEach-Object {
    $count = $_.Value.Count
    $agents = $_.Value -join ", "
    Write-Host "`n$($_.Key) ($count agents):" -ForegroundColor Yellow
    Write-Host "  $agents" -ForegroundColor DarkGray
}
```
