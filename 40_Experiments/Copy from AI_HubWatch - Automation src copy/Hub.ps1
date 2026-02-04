# Hub.ps1
# Master control script for AI Hub management

param(
    [Parameter(Position = 0)]
    [string]$Command = "menu"
)

$HubDir = "C:\Users\YC\AI_hub"

function Show-Menu {
    Clear-Host
    Write-Host "`n╔═══════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║         AI Hub Control Center             ║" -ForegroundColor Cyan
    Write-Host "╚═══════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "INVENTORY" -ForegroundColor Yellow
    Write-Host "  1. Show all skills" -ForegroundColor White
    Write-Host "  2. Show all configs" -ForegroundColor White
    Write-Host "  3. List all agents" -ForegroundColor White
    Write-Host ""
    Write-Host "SKILLS MANAGEMENT" -ForegroundColor Yellow
    Write-Host "  4. Sync skills from Claude to all" -ForegroundColor White
    Write-Host "  5. Install new skill to all agents" -ForegroundColor White
    Write-Host "  6. Update all skills" -ForegroundColor White
    Write-Host ""
    Write-Host "UTILITIES" -ForegroundColor Yellow
    Write-Host "  7. Open Hub in VSCode" -ForegroundColor White
    Write-Host "  8. Export to Obsidian" -ForegroundColor White
    Write-Host "  9. Start WatchHub monitor (v2)" -ForegroundColor White
    Write-Host " 10. Stop WatchHub monitor" -ForegroundColor White
    Write-Host " 11. Track Installation (before/after)" -ForegroundColor White
    Write-Host ""
    Write-Host "  Q. Quit" -ForegroundColor DarkGray
    Write-Host ""
}

function Show-AllAgents {
    Write-Host "`n=== All AI Agents in Hub ===" -ForegroundColor Cyan
    $agents = Get-ChildItem -Path $HubDir -Directory | Sort-Object Name

    $byCategory = @{
        "User_Dot"        = @()
        "AppData_Roaming" = @()
        "AppData_Local"   = @()
        "Projects"        = @()
        "System"          = @()
        "Root"            = @()
    }

    foreach ($agent in $agents) {
        $name = $agent.Name
        if ($name -like "*_User_Dot") { $byCategory["User_Dot"] += $name }
        elseif ($name -like "*_AppData_Roaming") { $byCategory["AppData_Roaming"] += $name }
        elseif ($name -like "*_AppData_Local") { $byCategory["AppData_Local"] += $name }
        elseif ($name -like "*_Projects*") { $byCategory["Projects"] += $name }
        elseif ($name -like "*_System*") { $byCategory["System"] += $name }
        elseif ($name -like "*_Root_Dot") { $byCategory["Root"] += $name }
    }

    foreach ($category in $byCategory.Keys | Sort-Object) {
        if ($byCategory[$category].Count -gt 0) {
            Write-Host "`n$category ($($byCategory[$category].Count)):" -ForegroundColor Green
            $byCategory[$category] | ForEach-Object { Write-Host "  - $_" -ForegroundColor White }
        }
    }

    Write-Host "`nTotal agents: $($agents.Count)" -ForegroundColor Cyan
}

function Install-SkillToAll {
    Write-Host "`nEnter skill repository (e.g., vercel-labs/agent-skills):" -ForegroundColor Yellow
    $repo = Read-Host "Repo"

    Write-Host "`nInstalling $repo to all agents..." -ForegroundColor Cyan
    npx skills add $repo --all --global --yes

    Write-Host "`nDone!" -ForegroundColor Green
}

function Open-InVSCode {
    Write-Host "`nOpening AI Hub in VSCode..." -ForegroundColor Cyan
    code $HubDir
}

function Start-WatchHub {
    Write-Host "`nStarting WatchHub Real-Time Monitor v2..." -ForegroundColor Cyan
    Write-Host "Press Ctrl+C to stop" -ForegroundColor DarkGray
    & "$HubDir\WatchHub_Realtime.ps1"
}

function Stop-WatchHub {
    Write-Host "`nStopping WatchHub Auto Monitor..." -ForegroundColor Cyan
    $task = Get-ScheduledTask -TaskName "AI_HubWatch_AutoMonitor" -ErrorAction SilentlyContinue
    if ($null -eq $task) {
        Write-Host "[!] Task not found: AI_HubWatch_AutoMonitor" -ForegroundColor Yellow
        return
    }

    if ($task.State -eq 'Running') {
        Stop-ScheduledTask -TaskName "AI_HubWatch_AutoMonitor"
        Write-Host "[+] Stopped scheduled task: AI_HubWatch_AutoMonitor" -ForegroundColor Green
    } else {
        Write-Host "[i] Task is not running (state: $($task.State))" -ForegroundColor DarkGray
    }
}

function Track-Installation {
    & "$HubDir\TrackInstallation.ps1"
}

# Command dispatch
switch ($Command.ToLower()) {
    "menu" {
        while ($true) {
            Show-Menu
            $choice = Read-Host "Select option"

            switch ($choice) {
                "1" { & "$HubDir\ShowSkills.ps1"; pause }
                "2" { & "$HubDir\ShowConfigs.ps1"; pause }
                "3" { Show-AllAgents; pause }
                "4" { & "$HubDir\SyncSkills.ps1"; pause }
                "5" { Install-SkillToAll; pause }
                "6" { npx skills update --yes; pause }
                "7" { Open-InVSCode; pause }
                "8" { & "$HubDir\ExportToObsidian.ps1"; pause }
                "9" { Start-WatchHub }
                "10" { Stop-WatchHub; pause }
                "11" { Track-Installation; pause }
                "q" { exit 0 }
                default { Write-Host "Invalid option!" -ForegroundColor Red; Start-Sleep 1 }
            }
        }
    }
    "skills" { & "$HubDir\ShowSkills.ps1" }
    "configs" { & "$HubDir\ShowConfigs.ps1" }
    "agents" { Show-AllAgents }
    "sync" { & "$HubDir\SyncSkills.ps1" }
    "code" { Open-InVSCode }
    "obsidian" { & "$HubDir\ExportToObsidian.ps1" }
    "watch" { Start-WatchHub }
    "track" { Track-Installation }
    default {
        Write-Host "Unknown command: $Command" -ForegroundColor Red
        Write-Host "`nAvailable commands:" -ForegroundColor Yellow
        Write-Host "  .\Hub.ps1 menu     - Interactive menu"
        Write-Host "  .\Hub.ps1 skills   - Show skills inventory"
        Write-Host "  .\Hub.ps1 configs  - Show config files"
        Write-Host "  .\Hub.ps1 agents   - List all agents"
        Write-Host "  .\Hub.ps1 sync     - Sync skills"
        Write-Host "  .\Hub.ps1 code     - Open in VSCode"
        Write-Host "  .\Hub.ps1 obsidian - Export to Obsidian"
        Write-Host "  .\Hub.ps1 watch    - Start WatchHub v2"
        Write-Host "  .\Hub.ps1 track    - Track installation"
    }
}
