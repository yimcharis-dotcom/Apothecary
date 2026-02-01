# WatchHub Smart Wrapper
# - Shows "Started" on launch
# - Only logs when errors occur
# - Alerts with error details
# v3: Added -Debug passthrough

param(
    [string]$ScriptPath,
    [switch]$Debug
)

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
$startupMsg = "WatchHub monitoring started`n`nRunning in background..."
if ($Debug) {
    $startupMsg += "`n`nDEBUG MODE: Logging to _Change_log/DEBUG_*.log"
}
Show-Popup -Title "AI HubWatch" -Message $startupMsg -Icon "Information"

$MaxRetries = 5
$RetryCount = 0
$CurrentErrorLog = $null

while ($RetryCount -lt $MaxRetries) {
    try {
        # Run WatchHub (silent - no logging unless -Debug)
        if ($Debug) {
            & $ScriptPath -Debug 2>&1 | Out-Null
        } else {
            & $ScriptPath 2>&1 | Out-Null
        }

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
