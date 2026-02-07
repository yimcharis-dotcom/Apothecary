# WatchHub Auto-Start Setup (User-Level - No Admin Required)
# - Shows "Started" notification on launch
# - Only logs when errors occur
# - Runs at user level (no elevation needed)

param([switch]$Remove)

$TaskName = "AI_HubWatch_AutoMonitor"
$ScriptPath = "$PSScriptRoot\WatchHub_Realtime.ps1"

# ============================================================================
# UNINSTALL
# ============================================================================
if ($Remove) {
    Write-Host "`n=== Removing Auto-Start ===" -ForegroundColor Yellow

    $task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    if ($task) {
        if ($task.State -eq 'Running') {
            Stop-ScheduledTask -TaskName $TaskName
        }
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
        Write-Host "[+] Removed: $TaskName" -ForegroundColor Green
    }

    $wrapperPath = "$PSScriptRoot\WatchHub_Wrapper.ps1"
    if (Test-Path $wrapperPath) {
        Remove-Item $wrapperPath -Force
        Write-Host "[+] Removed: WatchHub_Wrapper.ps1" -ForegroundColor Green
    }

    Write-Host "`nAuto-start disabled." -ForegroundColor Cyan
    Read-Host "Press Enter to exit"
    exit
}

# ============================================================================
# INSTALL
# ============================================================================

Write-Host "`n=== Setting Up WatchHub Auto-Start ===" -ForegroundColor Cyan
Write-Host "Running as: $env:USERNAME (User-Level)" -ForegroundColor Green

if (-not (Test-Path $ScriptPath)) {
    Write-Host "[!] ERROR: WatchHub_Realtime.ps1 not found!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Create smart wrapper
$WrapperPath = "$PSScriptRoot\WatchHub_Wrapper.ps1"
$WrapperContent = @'
# WatchHub Smart Wrapper
# - Shows "Started" on launch
# - Only logs when errors occur
# - Alerts with error details

param([string]$ScriptPath)

$ErrorLogDir = Split-Path $ScriptPath | Join-Path -ChildPath "_Change_log"
if (-not (Test-Path $ErrorLogDir)) {
    New-Item -ItemType Directory -Path $ErrorLogDir -Force | Out-Null
}

function Show-Popup {
    param([string]$Title, [string]$Message, [string]$Icon = "Information")

    Add-Type -AssemblyName System.Windows.Forms
    $iconType = switch($Icon) {
        "Error"   { [System.Windows.Forms.MessageBoxIcon]::Error }
        "Warning" { [System.Windows.Forms.MessageBoxIcon]::Warning }
        default   { [System.Windows.Forms.MessageBoxIcon]::Information }
    }
    [System.Windows.Forms.MessageBox]::Show($Message, $Title, 'OK', $iconType) | Out-Null
}

function Start-ErrorLog {
    param([string]$ErrorMsg, [string]$StackTrace)

    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $logFile = Join-Path $ErrorLogDir "ERROR_$timestamp.log"

    $logContent = @"
===============================================
WatchHub Error Log
Started: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
===============================================

ERROR:
$ErrorMsg

STACK TRACE:
$StackTrace

===============================================
RESTART ATTEMPTS:
===============================================

"@
    Set-Content -Path $logFile -Value $logContent -Encoding UTF8
    return $logFile
}

function Add-ErrorLog {
    param([string]$LogFile, [string]$Message)

    $entry = "[$(Get-Date -Format "HH:mm:ss")] $Message"
    Add-Content -Path $LogFile -Value $entry -Encoding UTF8
}

# Show startup notification
Show-Popup -Title "AI HubWatch" -Message "WatchHub monitoring started`n`nRunning in background..." -Icon "Information"

$MaxRetries = 5
$RetryCount = 0
$CurrentErrorLog = $null

while ($RetryCount -lt $MaxRetries) {
    try {
        # Run WatchHub (silent - no logging)
        & $ScriptPath 2>&1 | Out-Null

        # Normal exit (user stopped it)
        if ($CurrentErrorLog) {
            Add-ErrorLog $CurrentErrorLog "WatchHub stopped normally after recovery"
            Show-Popup -Title "AI HubWatch Recovered" -Message "WatchHub recovered and stopped normally.`n`nError log: $(Split-Path $CurrentErrorLog -Leaf)" -Icon "Information"
        }
        break

    } catch {
        $RetryCount++
        $errorMsg = $_.Exception.Message
        $stackTrace = $_.ScriptStackTrace

        # First error - create log and alert
        if (-not $CurrentErrorLog) {
            $CurrentErrorLog = Start-ErrorLog -ErrorMsg $errorMsg -StackTrace $stackTrace

            # Show error alert with details
            $alertMsg = @"
WatchHub encountered an error:

$errorMsg

Starting error logging...
Attempt: $RetryCount / $MaxRetries

Error log: $(Split-Path $CurrentErrorLog -Leaf)
"@
            Show-Popup -Title "AI HubWatch ERROR" -Message $alertMsg -Icon "Error"
        }

        # Log retry attempt
        Add-ErrorLog $CurrentErrorLog "Error occurred: $errorMsg"

        if ($RetryCount -lt $MaxRetries) {
            Add-ErrorLog $CurrentErrorLog "Restarting in 10 seconds... (Attempt $($RetryCount + 1)/$MaxRetries)"
            Start-Sleep -Seconds 10
        } else {
            Add-ErrorLog $CurrentErrorLog "Max retries reached. Giving up."
            Add-ErrorLog $CurrentErrorLog "==============================================="
            Add-ErrorLog $CurrentErrorLog "STOPPED: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"

            # Final failure alert
            $failMsg = @"
WatchHub failed after $MaxRetries attempts.

Last error: $errorMsg

Check error log:
$(Split-Path $CurrentErrorLog -Leaf)

Location: $ErrorLogDir
"@
            Show-Popup -Title "AI HubWatch FAILED" -Message $failMsg -Icon "Error"
        }
    }
}
'@

Write-Host "[1/2] Creating wrapper..." -ForegroundColor Yellow
Set-Content -Path $WrapperPath -Value $WrapperContent -Encoding UTF8
Write-Host "[+] Created: WatchHub_Wrapper.ps1" -ForegroundColor Green

# Remove existing task
$existingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Write-Host "[*] Removing existing task..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# Create scheduled task
Write-Host "[2/2] Creating auto-start task..." -ForegroundColor Yellow

$Action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-WindowStyle Hidden -ExecutionPolicy Bypass -NoProfile -File `"$WrapperPath`" -ScriptPath `"$ScriptPath`""

$Trigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME

$Principal = New-ScheduledTaskPrincipal `
    -UserId $env:USERNAME `
    -LogonType Interactive `
    -RunLevel Limited

$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Days 0)

try {
    Register-ScheduledTask `
        -TaskName $TaskName `
        -Action $Action `
        -Trigger $Trigger `
        -Principal $Principal `
        -Settings $Settings `
        -Description "AI HubWatch auto-monitor for $env:USERNAME" `
        | Out-Null

    Write-Host "[+] Task created: $TaskName" -ForegroundColor Green

    # Start now
    Write-Host "`nStarting WatchHub..." -ForegroundColor Yellow
    Start-ScheduledTask -TaskName $TaskName
    Start-Sleep -Seconds 3

    $task = Get-ScheduledTask -TaskName $TaskName
    Write-Host "[+] Status: $($task.State)" -ForegroundColor Green

    Write-Host ""
    Write-Host "==================================================" -ForegroundColor Cyan
    Write-Host "  Setup Complete!" -ForegroundColor Cyan
    Write-Host "==================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Behavior:" -ForegroundColor White
    Write-Host "  - Runs at USER level (no admin)" -ForegroundColor DarkGray
    Write-Host "  - Shows popup on startup: 'Started'" -ForegroundColor DarkGray
    Write-Host "  - Runs silently (no logging)" -ForegroundColor DarkGray
    Write-Host "  - On error: Alerts + creates error log" -ForegroundColor DarkGray
    Write-Host "  - Error logs: _Change_log\ERROR_*.log" -ForegroundColor DarkGray
    Write-Host "  - Auto-restarts up to 5 times" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "Management:" -ForegroundColor White
    Write-Host "  Stop:      Stop-ScheduledTask '$TaskName'" -ForegroundColor DarkGray
    Write-Host "  Start:     Start-ScheduledTask '$TaskName'" -ForegroundColor DarkGray
    Write-Host "  Status:    Get-ScheduledTask '$TaskName'" -ForegroundColor DarkGray
    Write-Host "  Uninstall: .\SetupAutoStart_Final.ps1 -Remove" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "You should see a startup popup shortly..." -ForegroundColor Yellow
    Write-Host ""

} catch {
    Write-Host "[!] ERROR: Failed to create task" -ForegroundColor Red
    Write-Host "    $($_.Exception.Message)" -ForegroundColor Red
}

Read-Host "Press Enter to exit"
