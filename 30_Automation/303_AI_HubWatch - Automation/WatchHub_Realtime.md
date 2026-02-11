```
# ============================================================================
# WatchHub_Realtime.ps1
# Real-time FileSystemWatcher for AI Hub
# Instantly detects new AI tools and auto-links them
# v2: + Deletion detection + individual logs (_add / _del)
#     + Skills auto-sync (symlinks) on add/delete
# v3: + Debouncing (prevents duplicate events)
#     + Duplicate junction detection (checks target path)
#     + Efficient event wait (30s intervals)
#     + Debug logging option
#     + Mutex locking (prevents concurrent conflicts)
# ============================================================================

param(
    [string]$HubPath = "$env:USERPROFILE\AI_hub",
    [switch]$Verbose,
    [switch]$Debug
)

# ============================================================================
# Debounce Configuration (prevents duplicate events)
# ============================================================================
$script:eventCache = @{}
$script:debounceMsec = 2000  # Ignore duplicate events within 2 seconds
$script:DebugMode = $Debug

# ============================================================================
# Concurrency Control (prevents simultaneous operations from conflicting)
# ============================================================================
$script:mutex = New-Object System.Threading.Mutex($false, "Global\AI_HubWatch_Mutex")
$script:mutexTimeout = 10000  # 10 seconds max wait for mutex

# ============================================================================
# Configuration
# ============================================================================

$LogsFolder = Join-Path $HubPath "_Change_log"

$monitorPaths = @{
    "UserHome" = @{
        Path = "$env:USERPROFILE"
        Category = "User_Dot"
        Pattern = "^\."
    }
    "AppDataRoaming" = @{
        Path = "$env:APPDATA"
        Category = "AppData_Roaming"
        Pattern = ".*"
    }
    "AppDataLocalPrograms" = @{
        Path = "$env:LOCALAPPDATA\Programs"
        Category = "AppData_Local"
        Pattern = ".*"
    }
    "AppDataLocal" = @{
        Path = "$env:LOCALAPPDATA"
        Category = "AppData_Local"
        Pattern = ".*"
    }
    "GitHubRepo" = @{
        Path = "$env:USERPROFILE\GitHubRepo"
        Category = "Projects_GitHubRepo"
        Pattern = ".*"
    }
    "RootDot" = @{
        Path = "C:\"
        Category = "Root_Dot"
        Pattern = "^\."
    }
}

$aiKeywords = @(
    'claude', 'cursor', 'zed', 'ollama', 'gemini', 'windsurf',
    'mcp', 'anthropic', 'openai', 'copilot', 'codeium',
    'tabnine', 'github', 'llm', 'ai', 'gpt', 'chatbot',
    'agent', 'aider', 'continue', 'cody', 'supermaven'
)

# ============================================================================
# Helper Functions
# ============================================================================

function Write-Log {
    param([string]$Message, [string]$Color = "White", [switch]$DebugOnly)
    $timestamp = Get-Date -Format "HH:mm:ss"

    # Skip debug messages unless Debug mode is on
    if ($DebugOnly -and -not $script:DebugMode) { return }

    Write-Host "[$timestamp] $Message" -ForegroundColor $Color

    # Write to debug log file if Debug mode is on
    if ($script:DebugMode) {
        $debugLogPath = Join-Path $LogsFolder "DEBUG_$(Get-Date -Format 'yyyyMMdd').log"
        $logLine = "[$timestamp] $Message"
        Add-Content -Path $debugLogPath -Value $logLine -ErrorAction SilentlyContinue
    }
}

# Debounce helper: returns $true if event should be processed, $false if duplicate
function Test-Debounce {
    param([string]$EventKey)
    $now = [DateTime]::Now

    if ($script:eventCache.ContainsKey($EventKey)) {
        $lastTime = $script:eventCache[$EventKey]
        $elapsed = ($now - $lastTime).TotalMilliseconds
        if ($elapsed -lt $script:debounceMsec) {
            Write-Log "  [DEBOUNCE] Skipping duplicate event: $EventKey (${elapsed}ms ago)" -Color DarkGray -DebugOnly
            return $false
        }
    }

    $script:eventCache[$EventKey] = $now

    # Clean old entries (older than 10 seconds)
    $keysToRemove = @()
    foreach ($key in $script:eventCache.Keys) {
        if (($now - $script:eventCache[$key]).TotalSeconds -gt 10) {
            $keysToRemove += $key
        }
    }
    foreach ($key in $keysToRemove) {
        $script:eventCache.Remove($key)
    }

    return $true
}

# Check if a junction already exists pointing to the same target
function Test-DuplicateJunction {
    param([string]$TargetPath, [string]$HubPath)

    $existingJunctions = Get-ChildItem -Path $HubPath -Directory -ErrorAction SilentlyContinue |
        Where-Object { $_.Attributes -band [System.IO.FileAttributes]::ReparsePoint }

    foreach ($junction in $existingJunctions) {
        try {
            $target = (Get-Item $junction.FullName -ErrorAction SilentlyContinue).Target
            if ($target -and ($target -eq $TargetPath -or $target -contains $TargetPath)) {
                return $junction.Name
            }
        } catch { }
    }
    return $null
}

# ============================================================================
# Ensure Logs Folder Exists
# ============================================================================

if (-not (Test-Path $LogsFolder)) {
    New-Item -ItemType Directory -Path $LogsFolder -Force | Out-Null
    Write-Log "Created logs folder: $LogsFolder" -Color Green
}

# ============================================================================
# FileSystemWatcher Setup
# ============================================================================

Write-Log "=======================================================" -Color Cyan
Write-Log "  AI Hub Real-Time Monitor v3" -Color Cyan
Write-Log "  + Logs: _Change_log (_add / _del)" -Color DarkCyan
Write-Log "  + Deletion detection & cleanup" -Color DarkCyan
Write-Log "  + Skills auto-sync (symlinks)" -Color DarkMagenta
Write-Log "  + Debouncing (2s dedup window)" -Color DarkGreen
Write-Log "  + Duplicate junction detection" -Color DarkGreen
Write-Log "  + Mutex locking (thread-safe)" -Color DarkGreen
if ($script:DebugMode) {
    Write-Log "  + DEBUG MODE ON (logging to DEBUG_*.log)" -Color Yellow
}
Write-Log "=======================================================" -Color Cyan
Write-Log ""

$watchers = @()
$watcherCount = 0

foreach ($key in $monitorPaths.Keys) {
    $config = $monitorPaths[$key]
    $path = $config.Path

    if (-not (Test-Path $path)) {
        Write-Log "[X] Skipping (not found): $path" -Color DarkGray
        continue
    }

    try {
        $watcher = New-Object System.IO.FileSystemWatcher
        $watcher.Path = $path
        $watcher.IncludeSubdirectories = $false
        $watcher.NotifyFilter = [System.IO.NotifyFilters]::DirectoryName

        # ================================================================
        # CREATED Action
        # ================================================================
        $createAction = {
            $name = $Event.SourceEventArgs.Name
            $changeType = $Event.SourceEventArgs.ChangeType
            $fullPath = $Event.SourceEventArgs.FullPath
            $category = $Event.MessageData.Category
            $pattern = $Event.MessageData.Pattern
            $hubPath = $Event.MessageData.HubPath
            $logsFolder = $Event.MessageData.LogsFolder
            $debugMode = $Event.MessageData.DebugMode
            $eventCache = $Event.MessageData.EventCache
            $debounceMsec = $Event.MessageData.DebounceMsec
            $mutex = $Event.MessageData.Mutex
            $mutexTimeout = $Event.MessageData.MutexTimeout

            function Write-Log {
                param([string]$Message, [string]$Color = "White", [switch]$DebugOnly)
                $timestamp = Get-Date -Format "HH:mm:ss"
                if ($DebugOnly -and -not $debugMode) { return }
                Write-Host "[$timestamp] $Message" -ForegroundColor $Color
                if ($debugMode) {
                    $debugLogPath = Join-Path $logsFolder "DEBUG_$(Get-Date -Format 'yyyyMMdd').log"
                    Add-Content -Path $debugLogPath -Value "[$timestamp] $Message" -ErrorAction SilentlyContinue
                }
            }

            if ($changeType -eq 'Created') {
                # Debounce check
                $eventKey = "CREATE:$fullPath"
                $now = [DateTime]::Now
                if ($eventCache.ContainsKey($eventKey)) {
                    $elapsed = ($now - $eventCache[$eventKey]).TotalMilliseconds
                    if ($elapsed -lt $debounceMsec) {
                        Write-Log "  [DEBOUNCE] Skipping duplicate: $name (${elapsed}ms)" -Color DarkGray -DebugOnly
                        return
                    }
                }
                $eventCache[$eventKey] = $now
                Write-Log "=====================================================" -Color Yellow
                Write-Log "NEW FOLDER DETECTED" -Color Yellow
                Write-Log "  Name: $name" -Color White
                Write-Log "  Path: $fullPath" -Color Gray
                Write-Log "  Category: $category" -Color Gray

                $patternMatch = $name -match $pattern
                $aiKeywords = @(
                    'claude', 'cursor', 'zed', 'ollama', 'gemini', 'windsurf',
                    'mcp', 'anthropic', 'openai', 'copilot', 'codeium',
                    'tabnine', 'github', 'llm', 'ai', 'gpt', 'chatbot',
                    'agent', 'aider', 'continue', 'cody', 'supermaven'
                )
                $nameMatch = $aiKeywords | Where-Object { $name -like "*$_*" }

                if ($nameMatch -or $patternMatch) {
                    Write-Log "  -> Identified as AI tool!" -Color Green

                    $cleanName = $name -replace '^\.', ''
                    $cleanName = $cleanName -replace '[<>:"/\\|?*]', '_'
                    $junctionName = "${cleanName}_${category}"
                    $junctionPath = Join-Path $hubPath $junctionName

                    # Acquire mutex to prevent concurrent junction creation
                    try {
                        $acquired = $mutex.WaitOne($mutexTimeout)
                        if (-not $acquired) {
                            Write-Log "  [!] Mutex timeout - skipping" -Color Red
                            return
                        }
                        Write-Log "  [MUTEX] Acquired lock" -Color DarkGray -DebugOnly

                    if (-not (Test-Path $junctionPath)) {
                        # Check for duplicate junction pointing to same target
                        $existingJunctions = Get-ChildItem -Path $hubPath -Directory -ErrorAction SilentlyContinue |
                            Where-Object { $_.Attributes -band [System.IO.FileAttributes]::ReparsePoint }
                        $duplicateJunction = $null
                        foreach ($junc in $existingJunctions) {
                            try {
                                $target = (Get-Item $junc.FullName -ErrorAction SilentlyContinue).Target
                                if ($target -and ($target -eq $fullPath -or $target -contains $fullPath)) {
                                    $duplicateJunction = $junc.Name
                                    break
                                }
                            } catch { }
                        }

                        if ($duplicateJunction) {
                            Write-Log "  [DUPLICATE] Junction already exists: $duplicateJunction -> $fullPath" -Color DarkYellow
                            Write-Log "  [o] Skipping (use existing junction)" -Color DarkGray
                            return
                        }

                        $result = cmd /c mklink /J "$junctionPath" "$fullPath" 2>&1

                        if ($LASTEXITCODE -eq 0) {
                            Write-Log "  [+] Junction created: $junctionName" -Color Green

                            # Master log
                            $masterLogPath = Join-Path $hubPath "discovery.log"
                            $logEntry = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') | CREATED | $junctionName | $fullPath"
                            Add-Content -Path $masterLogPath -Value $logEntry

                            # Individual _add log
                            $logFileName = "${cleanName}_${category}_add.txt"
                            $folderLogPath = Join-Path $logsFolder $logFileName
                            $folderLogEntry = @"
[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] CREATED
  Folder: $name
  Path: $fullPath
  Category: $category
  Junction: $junctionPath
---
"@
                            Add-Content -Path $folderLogPath -Value $folderLogEntry -Encoding UTF8
                            Write-Log "  [+] Logged to: $logFileName" -Color DarkGreen

                            # Export to Obsidian
                            $exportScript = Join-Path $hubPath "ExportToObsidian.ps1"
                            if (Test-Path $exportScript) {
                                Write-Log "  [*] Updating Obsidian inventory..." -Color Cyan
                                & $exportScript
                            }
                        } else {
                            Write-Log "  [X] Failed to create junction" -Color Red
                        }
                    } else {
                        Write-Log "  [o] Junction already exists" -Color DarkGray
                    }

                    } finally {
                        if ($acquired) {
                            $mutex.ReleaseMutex()
                            Write-Log "  [MUTEX] Released lock" -Color DarkGray -DebugOnly
                        }
                    }
                } else {
                    Write-Log "  [o] Not identified as AI tool (skipping)" -Color DarkGray
                }
                Write-Log "=====================================================" -Color Yellow
                Write-Log ""
            }
        }

        # ================================================================
        # DELETED Action
        # ================================================================
        $deleteAction = {
            $name = $Event.SourceEventArgs.Name
            $changeType = $Event.SourceEventArgs.ChangeType
            $fullPath = $Event.SourceEventArgs.FullPath
            $category = $Event.MessageData.Category
            $hubPath = $Event.MessageData.HubPath
            $logsFolder = $Event.MessageData.LogsFolder
            $debugMode = $Event.MessageData.DebugMode
            $eventCache = $Event.MessageData.EventCache
            $debounceMsec = $Event.MessageData.DebounceMsec
            $mutex = $Event.MessageData.Mutex
            $mutexTimeout = $Event.MessageData.MutexTimeout

            function Write-Log {
                param([string]$Message, [string]$Color = "White", [switch]$DebugOnly)
                $timestamp = Get-Date -Format "HH:mm:ss"
                if ($DebugOnly -and -not $debugMode) { return }
                Write-Host "[$timestamp] $Message" -ForegroundColor $Color
                if ($debugMode) {
                    $debugLogPath = Join-Path $logsFolder "DEBUG_$(Get-Date -Format 'yyyyMMdd').log"
                    Add-Content -Path $debugLogPath -Value "[$timestamp] $Message" -ErrorAction SilentlyContinue
                }
            }

            if ($changeType -eq 'Deleted') {
                # Debounce check
                $eventKey = "DELETE:$fullPath"
                $now = [DateTime]::Now
                if ($eventCache.ContainsKey($eventKey)) {
                    $elapsed = ($now - $eventCache[$eventKey]).TotalMilliseconds
                    if ($elapsed -lt $debounceMsec) {
                        Write-Log "  [DEBOUNCE] Skipping duplicate: $name (${elapsed}ms)" -Color DarkGray -DebugOnly
                        return
                    }
                }
                $eventCache[$eventKey] = $now
                Write-Log "=====================================================" -Color Red
                Write-Log "FOLDER DELETED" -Color Red
                Write-Log "  Name: $name" -Color White
                Write-Log "  Path: $fullPath" -Color Gray
                Write-Log "  Category: $category" -Color Gray

                $cleanName = $name -replace '^\.', ''
                $cleanName = $cleanName -replace '[<>:"/\\|?*]', '_'
                $junctionName = "${cleanName}_${category}"
                $junctionPath = Join-Path $hubPath $junctionName

                # Acquire mutex to prevent concurrent junction removal
                try {
                    $acquired = $mutex.WaitOne($mutexTimeout)
                    if (-not $acquired) {
                        Write-Log "  [!] Mutex timeout - skipping" -Color Red
                        return
                    }
                    Write-Log "  [MUTEX] Acquired lock" -Color DarkGray -DebugOnly

                if (Test-Path $junctionPath) {
                    cmd /c rmdir "$junctionPath" 2>&1 | Out-Null

                    if (-not (Test-Path $junctionPath)) {
                        Write-Log "  [+] Removed junction: $junctionName" -Color Yellow

                        # Master log
                        $masterLogPath = Join-Path $hubPath "discovery.log"
                        $logEntry = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') | DELETED | $junctionName | $fullPath"
                        Add-Content -Path $masterLogPath -Value $logEntry

                        # Individual _del log
                        $logFileName = "${cleanName}_${category}_del.txt"
                        $folderLogPath = Join-Path $logsFolder $logFileName
                        $folderLogEntry = @"
[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] DELETED
  Folder: $name
  Path: $fullPath
  Category: $category
  Junction: $junctionPath (removed)
---
"@
                        Add-Content -Path $folderLogPath -Value $folderLogEntry -Encoding UTF8
                        Write-Log "  [+] Logged to: $logFileName" -Color DarkYellow

                        # Export to Obsidian
                        $exportScript = Join-Path $hubPath "ExportToObsidian.ps1"
                        if (Test-Path $exportScript) {
                            Write-Log "  [*] Updating Obsidian inventory..." -Color Cyan
                            & $exportScript
                        }
                    } else {
                        Write-Log "  [X] Failed to remove junction" -Color Red
                    }
                } else {
                    Write-Log "  [o] No junction found (was not tracked)" -Color DarkGray
                }

                } finally {
                    if ($acquired) {
                        $mutex.ReleaseMutex()
                        Write-Log "  [MUTEX] Released lock" -Color DarkGray -DebugOnly
                    }
                }

                Write-Log "=====================================================" -Color Red
                Write-Log ""
            }
        }

        $messageData = @{
            Category = $config.Category
            Pattern = $config.Pattern
            HubPath = $HubPath
            LogsFolder = $LogsFolder
            Verbose = $Verbose
            DebugMode = $script:DebugMode
            EventCache = $script:eventCache
            DebounceMsec = $script:debounceMsec
            Mutex = $script:mutex
            MutexTimeout = $script:mutexTimeout
        }

        $null = Register-ObjectEvent -InputObject $watcher -EventName Created -Action $createAction -MessageData $messageData
        $null = Register-ObjectEvent -InputObject $watcher -EventName Deleted -Action $deleteAction -MessageData $messageData

        $watcher.EnableRaisingEvents = $true
        $watchers += $watcher
        $watcherCount++

        Write-Log "[+] Monitoring: $path" -Color Green
        Write-Log "  Category: $($config.Category)" -Color DarkGray

    } catch {
        Write-Log "[X] Failed to monitor $path : $_" -Color Red
    }
}

# ============================================================================
# Skills Folder Watcher - Auto-sync skills to all agents
# ============================================================================

$SourceAgent = "Claude_User_Dot"
$skillsPath = Join-Path $HubPath "$SourceAgent\skills"

if (Test-Path $skillsPath) {
    try {
        $skillsWatcher = New-Object System.IO.FileSystemWatcher
        $skillsWatcher.Path = $skillsPath
        $skillsWatcher.IncludeSubdirectories = $false
        $skillsWatcher.NotifyFilter = [System.IO.NotifyFilters]::DirectoryName

        # SKILL CREATED
        $skillCreateAction = {
            $name = $Event.SourceEventArgs.Name
            $fullPath = $Event.SourceEventArgs.FullPath
            $hubPath = $Event.MessageData.HubPath
            $logsFolder = $Event.MessageData.LogsFolder
            $debugMode = $Event.MessageData.DebugMode
            $eventCache = $Event.MessageData.EventCache
            $debounceMsec = $Event.MessageData.DebounceMsec

            function Write-Log {
                param([string]$Message, [string]$Color = "White", [switch]$DebugOnly)
                $timestamp = Get-Date -Format "HH:mm:ss"
                if ($DebugOnly -and -not $debugMode) { return }
                Write-Host "[$timestamp] $Message" -ForegroundColor $Color
                if ($debugMode) {
                    $debugLogPath = Join-Path $logsFolder "DEBUG_$(Get-Date -Format 'yyyyMMdd').log"
                    Add-Content -Path $debugLogPath -Value "[$timestamp] $Message" -ErrorAction SilentlyContinue
                }
            }

            # Debounce check
            $eventKey = "SKILL_CREATE:$fullPath"
            $now = [DateTime]::Now
            if ($eventCache.ContainsKey($eventKey)) {
                $elapsed = ($now - $eventCache[$eventKey]).TotalMilliseconds
                if ($elapsed -lt $debounceMsec) {
                    Write-Log "  [DEBOUNCE] Skipping duplicate skill event: $name" -Color DarkGray -DebugOnly
                    return
                }
            }
            $eventCache[$eventKey] = $now

            Write-Log "=====================================================" -Color Magenta
            Write-Log "NEW SKILL DETECTED" -Color Magenta
            Write-Log "  Name: $name" -Color White
            Write-Log "  Path: $fullPath" -Color Gray

            # Trigger SyncSkills to symlink to all agents
            $syncScript = Join-Path $hubPath "SyncSkills.ps1"
            if (Test-Path $syncScript) {
                Write-Log "  -> Syncing skill to all agents..." -Color Cyan
                & $syncScript -SkillName $name
            }

            # Log to _Change_log
            $logFileName = "${name}_skill_add.txt"
            $folderLogPath = Join-Path $logsFolder $logFileName
            $logEntry = @"
[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] SKILL ADDED
  Skill: $name
  Source: $fullPath
  Action: Symlinked to all agents
---
"@
            Add-Content -Path $folderLogPath -Value $logEntry -Encoding UTF8
            Write-Log "  [+] Logged to: $logFileName" -Color DarkMagenta

            # Update Obsidian
            $exportScript = Join-Path $hubPath "ExportToObsidian.ps1"
            if (Test-Path $exportScript) {
                Write-Log "  [*] Updating Obsidian inventory..." -Color Cyan
                & $exportScript
            }

            Write-Log "=====================================================" -Color Magenta
            Write-Log ""
        }

        # SKILL DELETED
        $skillDeleteAction = {
            $name = $Event.SourceEventArgs.Name
            $fullPath = $Event.SourceEventArgs.FullPath
            $hubPath = $Event.MessageData.HubPath
            $logsFolder = $Event.MessageData.LogsFolder
            $debugMode = $Event.MessageData.DebugMode
            $eventCache = $Event.MessageData.EventCache
            $debounceMsec = $Event.MessageData.DebounceMsec

            function Write-Log {
                param([string]$Message, [string]$Color = "White", [switch]$DebugOnly)
                $timestamp = Get-Date -Format "HH:mm:ss"
                if ($DebugOnly -and -not $debugMode) { return }
                Write-Host "[$timestamp] $Message" -ForegroundColor $Color
                if ($debugMode) {
                    $debugLogPath = Join-Path $logsFolder "DEBUG_$(Get-Date -Format 'yyyyMMdd').log"
                    Add-Content -Path $debugLogPath -Value "[$timestamp] $Message" -ErrorAction SilentlyContinue
                }
            }

            # Debounce check
            $eventKey = "SKILL_DELETE:$fullPath"
            $now = [DateTime]::Now
            if ($eventCache.ContainsKey($eventKey)) {
                $elapsed = ($now - $eventCache[$eventKey]).TotalMilliseconds
                if ($elapsed -lt $debounceMsec) {
                    Write-Log "  [DEBOUNCE] Skipping duplicate skill event: $name" -Color DarkGray -DebugOnly
                    return
                }
            }
            $eventCache[$eventKey] = $now

            Write-Log "=====================================================" -Color DarkMagenta
            Write-Log "SKILL DELETED" -Color DarkMagenta
            Write-Log "  Name: $name" -Color White
            Write-Log "  Path: $fullPath" -Color Gray

            # Trigger SyncSkills to remove symlinks from all agents
            $syncScript = Join-Path $hubPath "SyncSkills.ps1"
            if (Test-Path $syncScript) {
                Write-Log "  -> Removing skill symlinks from all agents..." -Color Yellow
                & $syncScript -SkillName $name -Delete
            }

            # Log to _Change_log
            $logFileName = "${name}_skill_del.txt"
            $folderLogPath = Join-Path $logsFolder $logFileName
            $logEntry = @"
[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] SKILL DELETED
  Skill: $name
  Source: $fullPath
  Action: Removed symlinks from all agents
---
"@
            Add-Content -Path $folderLogPath -Value $logEntry -Encoding UTF8
            Write-Log "  [+] Logged to: $logFileName" -Color DarkYellow

            # Update Obsidian
            $exportScript = Join-Path $hubPath "ExportToObsidian.ps1"
            if (Test-Path $exportScript) {
                Write-Log "  [*] Updating Obsidian inventory..." -Color Cyan
                & $exportScript
            }

            Write-Log "=====================================================" -Color DarkMagenta
            Write-Log ""
        }

        $skillsMessageData = @{
            HubPath = $HubPath
            LogsFolder = $LogsFolder
            DebugMode = $script:DebugMode
            EventCache = $script:eventCache
            DebounceMsec = $script:debounceMsec
            Mutex = $script:mutex
            MutexTimeout = $script:mutexTimeout
        }

        $null = Register-ObjectEvent -InputObject $skillsWatcher -EventName Created -Action $skillCreateAction -MessageData $skillsMessageData
        $null = Register-ObjectEvent -InputObject $skillsWatcher -EventName Deleted -Action $skillDeleteAction -MessageData $skillsMessageData

        $skillsWatcher.EnableRaisingEvents = $true
        $watchers += $skillsWatcher

        Write-Log "[+] Monitoring Skills: $skillsPath" -Color Magenta
        Write-Log "  Auto-sync to all agents on add/delete" -Color DarkMagenta

    } catch {
        Write-Log "[X] Failed to monitor skills: $_" -Color Red
    }
} else {
    Write-Log "[X] Skills folder not found: $skillsPath" -Color DarkGray
}

Write-Log ""
Write-Log "=======================================================" -Color Cyan
Write-Log "  Monitoring $watcherCount locations + Skills" -Color Green
Write-Log "  Logs: $LogsFolder" -Color DarkCyan
Write-Log "  Press Ctrl+C to stop" -Color Yellow
Write-Log "=======================================================" -Color Cyan
Write-Log ""

# ============================================================================
# Keep Running (efficient - 30 second sleep vs 1 second)
# ============================================================================

# Note: Using longer sleep interval (30s vs 1s) reduces CPU wake-ups by 30x
# FileSystemWatcher events fire independently of this loop
# The loop only exists to keep the process alive and allow Ctrl+C handling

try {
    Write-Log "[*] Idle loop: 30s intervals (30x fewer wake-ups)" -Color DarkGray -DebugOnly
    while ($true) {
        Start-Sleep -Seconds 30

        # Optional: Clean stale debounce cache entries periodically
        $now = [DateTime]::Now
        $staleKeys = @($script:eventCache.Keys | Where-Object {
            ($now - $script:eventCache[$_]).TotalSeconds -gt 60
        })
        foreach ($key in $staleKeys) {
            $script:eventCache.Remove($key)
        }
    }
} finally {
    Write-Log ""
    Write-Log "Shutting down watchers..." -Color Yellow
    $watchers | ForEach-Object { $_.EnableRaisingEvents = $false; $_.Dispose() }
    Get-EventSubscriber | Unregister-Event -ErrorAction SilentlyContinue
    if ($script:mutex) {
        $script:mutex.Dispose()
        Write-Log "Mutex disposed" -Color Gray
    }
    Write-Log "Monitoring stopped." -Color Red
}

```