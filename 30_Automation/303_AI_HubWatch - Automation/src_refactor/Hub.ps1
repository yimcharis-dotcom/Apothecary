# Hub.ps1
# Master control script for AI Hub management
param(
    [Parameter(Position = 0)]
    [string]$Command = "menu"
)

$HubDir = if ($env:AI_HUB_PATH) { $env:AI_HUB_PATH } else { "$env:USERPROFILE\AI_hub" }
$TaskName = "AI_HubWatch_AutoMonitor"

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
    Write-Host ""
    Write-Host "WATCHHUB" -ForegroundColor Yellow
    Write-Host "  9. Start WatchHub monitor" -ForegroundColor White
    Write-Host " 10. Stop WatchHub monitor" -ForegroundColor White
    Write-Host " 11. WatchHub status" -ForegroundColor White
    Write-Host " 12. Track Installation (before/after)" -ForegroundColor White
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
    Write-Host "`nStarting WatchHub Real-Time Monitor..." -ForegroundColor Cyan
    Write-Host "Press Ctrl+C to stop" -ForegroundColor DarkGray
    & "$PSScriptRoot\WatchHub_Realtime.ps1"
}

function Stop-WatchHub {
    Write-Host "`n=== Stopping WatchHub ===" -ForegroundColor Yellow

    # Stop scheduled task if running
    $task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    if ($task -and $task.State -eq 'Running') {
        Stop-ScheduledTask -TaskName $TaskName
        Write-Host "[+] Stopped scheduled task: $TaskName" -ForegroundColor Green
    }

    # Kill any running PowerShell processes with WatchHub
    $procs = Get-Process -Name powershell, pwsh -ErrorAction SilentlyContinue | Where-Object {
        $_.CommandLine -like "*WatchHub*" -or $_.CommandLine -like "*WatchHub_Realtime*"
    }

    if ($procs) {
        $procs | ForEach-Object {
            Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
            Write-Host "[+] Killed process: $($_.Id)" -ForegroundColor Green
        }
    }

    # Alternative: find by window title or script path
    Get-CimInstance Win32_Process -Filter "Name = 'powershell.exe'" -ErrorAction SilentlyContinue |
        Where-Object { $_.CommandLine -like "*WatchHub*" } |
        ForEach-Object {
            Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue
            Write-Host "[+] Killed process: $($_.ProcessId)" -ForegroundColor Green
        }

    Write-Host "`nWatchHub stopped. Safe to run manual inventory." -ForegroundColor Cyan
}

function Get-WatchHubStatus {
    Write-Host "`n=== WatchHub Status ===" -ForegroundColor Cyan

    # Check scheduled task
    $task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    if ($task) {
        $stateColor = switch ($task.State) {
            'Running' { 'Green' }
            'Ready' { 'Yellow' }
            default { 'DarkGray' }
        }
        Write-Host "`nScheduled Task:" -ForegroundColor White
        Write-Host "  Name:   $TaskName" -ForegroundColor DarkGray
        Write-Host "  State:  $($task.State)" -ForegroundColor $stateColor
    } else {
        Write-Host "`nScheduled Task: Not installed" -ForegroundColor DarkGray
    }

    # Check running processes
    $watchHubProcs = Get-CimInstance Win32_Process -Filter "Name = 'powershell.exe'" -ErrorAction SilentlyContinue |
        Where-Object { $_.CommandLine -like "*WatchHub*" }

    Write-Host "`nRunning Processes:" -ForegroundColor White
    if ($watchHubProcs) {
        $watchHubProcs | ForEach-Object {
            Write-Host "  PID $($_.ProcessId): Running" -ForegroundColor Green
        }
    } else {
        Write-Host "  None" -ForegroundColor DarkGray
    }

    # Check recent logs
    $logsDir = Join-Path $HubDir "_Change_log"
    if (Test-Path $logsDir) {
        $recentLogs = Get-ChildItem $logsDir -Filter "*.txt" -ErrorAction SilentlyContinue |
            Sort-Object LastWriteTime -Descending |
            Select-Object -First 3

        Write-Host "`nRecent Activity:" -ForegroundColor White
        if ($recentLogs) {
            $recentLogs | ForEach-Object {
                Write-Host "  $($_.Name) - $($_.LastWriteTime)" -ForegroundColor DarkGray
            }
        } else {
            Write-Host "  No recent logs" -ForegroundColor DarkGray
        }
    }
}

function Track-Installation {
    & "$PSScriptRoot\TrackInstallation.ps1"
}

# Command dispatch
switch ($Command.ToLower()) {
    "menu" {
        while ($true) {
            Show-Menu
            $choice = Read-Host "Select option"

            switch ($choice) {
                "1" { & "$PSScriptRoot\ShowSkills.ps1"; pause }
                "2" { & "$PSScriptRoot\ShowConfigs.ps1"; pause }
                "3" { Show-AllAgents; pause }
                "4" { & "$PSScriptRoot\SyncSkills.ps1"; pause }
                "5" { Install-SkillToAll; pause }
                "6" { npx skills update --yes; pause }
                "7" { Open-InVSCode; pause }
                "8" { & "$PSScriptRoot\ExportToObsidian.ps1"; pause }
                "9" { Start-WatchHub }
                "10" { Stop-WatchHub; pause }
                "11" { Get-WatchHubStatus; pause }
                "12" { Track-Installation; pause }
                "q" { exit 0 }
                default { Write-Host "Invalid option!" -ForegroundColor Red; Start-Sleep 1 }
            }
        }
    }
    "skills" { & "$PSScriptRoot\ShowSkills.ps1" }
    "configs" { & "$PSScriptRoot\ShowConfigs.ps1" }
    "agents" { Show-AllAgents }
    "sync" { & "$PSScriptRoot\SyncSkills.ps1" }
    "code" { Open-InVSCode }
    "obsidian" { & "$PSScriptRoot\ExportToObsidian.ps1" }
    "watch" { Start-WatchHub }
    "stop" { Stop-WatchHub }
    "status" { Get-WatchHubStatus }
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
        Write-Host "  .\Hub.ps1 watch    - Start WatchHub"
        Write-Host "  .\Hub.ps1 stop     - Stop WatchHub"
        Write-Host "  .\Hub.ps1 status   - WatchHub status"
        Write-Host "  .\Hub.ps1 track    - Track installation"
    }
}
