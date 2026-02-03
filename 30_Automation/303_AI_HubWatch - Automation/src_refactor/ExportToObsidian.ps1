# ExportToObsidian.ps1
# Auto-generate AI Hub inventory as Obsidian note
# v2: + Portable paths

param(
    [string]$VaultPath = "$env:USERPROFILE\Vault\Apothecary\20_AI tools",
    [string]$NoteName = "AI_Hub_Inventory_AUTO.md"
)

# Load shared config
$configPath = Join-Path $PSScriptRoot "AIToolsConfig.ps1"
if (Test-Path $configPath) {
    . $configPath
}

$HubDir = if ($script:HubDir) { $script:HubDir } elseif ($env:AI_HUB_PATH) { $env:AI_HUB_PATH } else { "$env:USERPROFILE\AI_hub" }
$OutputPath = Join-Path $VaultPath $NoteName

Write-Host "Generating AI Hub inventory for Obsidian..." -ForegroundColor Cyan

# Collect data
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$agents = Get-ChildItem -Path $HubDir -Directory | Sort-Object Name
$agentsWithSkills = $agents | Where-Object {
    Test-Path (Join-Path $_.FullName "skills")
}

# Collect skills
$skillsIndex = @{}
foreach ($agent in $agentsWithSkills) {
    $skillsPath = Join-Path $agent.FullName "skills"
    $skills = Get-ChildItem -Path $skillsPath -Directory -ErrorAction SilentlyContinue
    foreach ($skill in $skills) {
        if (-not $skillsIndex.ContainsKey($skill.Name)) {
            $skillsIndex[$skill.Name] = @()
        }
        $skillsIndex[$skill.Name] += $agent.Name
    }
}

# Collect configs
$configPatterns = @("config.json", "settings.json", "*.yaml", "*.toml", ".env", "mcp*.json")
$configCount = 0
foreach ($agent in $agents) {
    foreach ($pattern in $configPatterns) {
        $found = Get-ChildItem -Path $agent.FullName -Filter $pattern -File -ErrorAction SilentlyContinue
        $configCount += $found.Count
    }
}

# Generate markdown using here-string
$markdown = @"
---
tags: [ai-tools, automation, inventory, auto-generated]
created: $timestamp
last_updated: $timestamp
type: dashboard
---

# AI Hub Inventory

> **Auto-generated on**: $timestamp
> **Source**: ``$HubDir``
> **Total Agents**: $($agents.Count)
> **Agents with Skills**: $($agentsWithSkills.Count)  

---

## Quick Stats

| Metric | Count |
|--------|-------|
| Total AI Agents | $($agents.Count) |
| Agents with Skills Support | $($agentsWithSkills.Count) |
| Unique Skills | $($skillsIndex.Count) |
| Config Files Found | $configCount |

---

## Skills Distribution

| Skill | Agent Count |
|-------|-------------|
$( ($skillsIndex.GetEnumerator() | Sort-Object { $_.Value.Count } -Descending | ForEach-Object { "| ``$($_.Key)`` | $($_.Value.Count) |" }) -join "`n" )

---

## Management Commands

### View Inventory
``````powershell
cd $HubDir
.\ShowSkills.ps1        # File system view
npx skills list -g      # Skills CLI view
.\ShowConfigs.ps1       # Find all configs
``````

### Install Skills
``````powershell
# Install to all agents
npx skills add vercel-labs/agent-skills --all -g -y

# Update all skills
npx skills update -y
``````

### Export to Obsidian
``````powershell
# Regenerate this file
.\ExportToObsidian.ps1
``````

---

## Related Notes

- [[AI_Ecosystem_Dashboard]]
- [[Claude_AI_Ecosystem_Discovery]]

---

*Last updated: $timestamp*
*Auto-generated from $HubDir*

"@

# Write to file
$markdown | Set-Content -Path $OutputPath -Encoding UTF8

Write-Host "`n[OK] Exported to: $OutputPath" -ForegroundColor Green
Write-Host "  Agents: $($agents.Count)" -ForegroundColor White
Write-Host "  Skills: $($skillsIndex.Count) unique" -ForegroundColor White
Write-Host "  Configs: $configCount files" -ForegroundColor White
Write-Host "`nOpen in Obsidian!" -ForegroundColor Cyan

