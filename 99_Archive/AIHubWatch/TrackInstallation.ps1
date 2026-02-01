# ============================================================================
# TrackInstallation.ps1
# Monitors where programs install in real-time
# Shows before/after snapshots to reveal installation locations
# ============================================================================

param(
    [Parameter(Mandatory=$false)]
    [string]$Mode = "menu",  # menu, before, after, predict
    
    [string]$SnapshotFile = "$env:TEMP\install_snapshot.json",
    
    [switch]$ShowAll
)

# ============================================================================
# Configuration - Common Installation Locations
# ============================================================================

$commonPaths = @{
    "User Home Configs" = @{
        Path = "C:\Users\$env:USERNAME"
        Pattern = "^\."
        Examples = @(".claude", ".cursor", ".ollama", ".config")
    }
    "AppData Roaming" = @{
        Path = "$env:APPDATA"
        Pattern = ".*"
        Examples = @("Code", "cursor", "Zed", "obsidian")
    }
    "AppData Local" = @{
        Path = "$env:LOCALAPPDATA"
        Pattern = ".*"
        Examples = @("Programs", "Anthropic", "Microsoft")
    }
    "AppData Local Programs" = @{
        Path = "$env:LOCALAPPDATA\Programs"
        Pattern = ".*"
        Examples = @("cursor", "windsurf", "Microsoft VS Code")
    }
    "Program Files" = @{
        Path = "C:\Program Files"
        Pattern = ".*"
        Examples = @("Python", "Git", "Ollama")
    }
    "Program Files (x86)" = @{
        Path = "C:\Program Files (x86)"
        Pattern = ".*"
        Examples = @("older 32-bit apps")
    }
    "ProgramData" = @{
        Path = "C:\ProgramData"
        Pattern = ".*"
        Examples = @("chocolatey", "shared configs")
    }
}

# Installation patterns by installer type
$installerPatterns = @{
    "MSI Installer" = @{
        Locations = @("C:\Program Files", "C:\Program Files (x86)")
        ConfigLocations = @("$env:APPDATA", "C:\ProgramData")
        RequiresAdmin = $true
    }
    "EXE Installer" = @{
        Locations = @("C:\Program Files", "$env:LOCALAPPDATA\Programs")
        ConfigLocations = @("$env:APPDATA", "$env:LOCALAPPDATA")
        RequiresAdmin = $false
    }
    "Portable/ZIP" = @{
        Locations = @("Anywhere you extract")
        ConfigLocations = @("$env:APPDATA", "Same folder as .exe")
        RequiresAdmin = $false
    }
    "Microsoft Store" = @{
        Locations = @("C:\Program Files\WindowsApps")
        ConfigLocations = @("$env:LOCALAPPDATA\Packages")
        RequiresAdmin = $false
    }
    "Chocolatey" = @{
        Locations = @("C:\ProgramData\chocolatey\lib")
        ConfigLocations = @("C:\ProgramData\chocolatey\config")
        RequiresAdmin = $true
    }
    "Scoop" = @{
        Locations = @("$env:USERPROFILE\scoop\apps")
        ConfigLocations = @("$env:USERPROFILE\scoop\persist")
        RequiresAdmin = $false
    }
    "NPM Global" = @{
        Locations = @("$env:APPDATA\npm", "$env:APPDATA\npm\node_modules")
        ConfigLocations = @("$env:USERPROFILE\.npmrc")
        RequiresAdmin = $false
    }
    "Python/pip" = @{
        Locations = @("Python installation\Scripts", "Python installation\Lib\site-packages")
        ConfigLocations = @("$env:APPDATA\Python")
        RequiresAdmin = $false
    }
}

# ============================================================================
# Helper Functions
# ============================================================================

function Write-Section {
    param([string]$Title)
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host "  $Title" -ForegroundColor White
    Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
}

function Get-DirectorySnapshot {
    param([string[]]$Paths)
    
    $snapshot = @{}
    
    foreach ($path in $Paths) {
        if (Test-Path $path) {
            Write-Host "  Scanning: $path" -ForegroundColor Gray
            
            $items = Get-ChildItem -Path $path -Directory -ErrorAction SilentlyContinue | 
                Select-Object Name, FullName, CreationTime, LastWriteTime
            
            $snapshot[$path] = $items
        }
    }
    
    return $snapshot
}

function Save-Snapshot {
    param(
        [hashtable]$Snapshot,
        [string]$FilePath
    )
    
    $data = @{
        Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        Snapshot = $Snapshot
    }
    
    $data | ConvertTo-Json -Depth 10 | Set-Content -Path $FilePath
    Write-Host "✓ Snapshot saved: $FilePath" -ForegroundColor Green
}

function Load-Snapshot {
    param([string]$FilePath)
    
    if (Test-Path $FilePath) {
        $data = Get-Content -Path $FilePath | ConvertFrom-Json
        return $data
    }
    return $null
}

function Compare-Snapshots {
    param(
        [object]$Before,
        [object]$After
    )
    
    $changes = @()
    
    foreach ($path in $After.Snapshot.PSObject.Properties.Name) {
        $beforeItems = $Before.Snapshot.$path
        $afterItems = $After.Snapshot.$path
        
        if ($beforeItems -and $afterItems) {
            $beforeNames = $beforeItems | ForEach-Object { $_.Name }
            $afterNames = $afterItems | ForEach-Object { $_.Name }
            
            $newItems = $afterNames | Where-Object { $_ -notin $beforeNames }
            
            foreach ($item in $newItems) {
                $fullItem = $afterItems | Where-Object { $_.Name -eq $item }
                $changes += [PSCustomObject]@{
                    Location = $path
                    FolderName = $item
                    FullPath = $fullItem.FullName
                    Created = $fullItem.CreationTime
                }
            }
        }
    }
    
    return $changes
}

function Show-InstallerTypeGuide {
    Write-Section "Installation Type Guide"
    
    foreach ($type in $installerPatterns.Keys | Sort-Object) {
        $pattern = $installerPatterns[$type]
        
        Write-Host ""
        Write-Host "▸ $type" -ForegroundColor Yellow
        Write-Host "  Program files go to:" -ForegroundColor Gray
        foreach ($loc in $pattern.Locations) {
            Write-Host "    • $loc" -ForegroundColor White
        }
        Write-Host "  Config files go to:" -ForegroundColor Gray
        foreach ($loc in $pattern.ConfigLocations) {
            Write-Host "    • $loc" -ForegroundColor White
        }
        Write-Host "  Requires Admin: " -NoNewline -ForegroundColor Gray
        if ($pattern.RequiresAdmin) {
            Write-Host "Yes" -ForegroundColor Red
        } else {
            Write-Host "No" -ForegroundColor Green
        }
    }
}

function Show-CommonLocations {
    Write-Section "Common AI Tool Install Locations"
    
    foreach ($name in $commonPaths.Keys | Sort-Object) {
        $info = $commonPaths[$name]
        
        Write-Host ""
        Write-Host "▸ $name" -ForegroundColor Yellow
        Write-Host "  Path: $($info.Path)" -ForegroundColor White
        Write-Host "  Examples: $($info.Examples -join ', ')" -ForegroundColor Gray
        
        if (Test-Path $info.Path) {
            $count = (Get-ChildItem -Path $info.Path -Directory -ErrorAction SilentlyContinue | Measure-Object).Count
            Write-Host "  Current folders: $count" -ForegroundColor Cyan
        } else {
            Write-Host "  Status: Not found" -ForegroundColor Red
        }
    }
}

function Start-InstallationTracking {
    Write-Section "Before Installation Snapshot"
    
    Write-Host ""
    Write-Host "Taking snapshot of current folders..." -ForegroundColor Yellow
    
    $paths = $commonPaths.Values | ForEach-Object { $_.Path } | Where-Object { Test-Path $_ }
    $snapshot = Get-DirectorySnapshot -Paths $paths
    
    Save-Snapshot -Snapshot $snapshot -FilePath $SnapshotFile
    
    Write-Host ""
    Write-Host "✓ Snapshot complete!" -ForegroundColor Green
    Write-Host ""
    Write-Host "NEXT STEPS:" -ForegroundColor Yellow
    Write-Host "  1. Install your program now" -ForegroundColor White
    Write-Host "  2. After installation, run:" -ForegroundColor White
    Write-Host "     .\TrackInstallation.ps1 -Mode after" -ForegroundColor Cyan
    Write-Host ""
}

function Show-InstallationChanges {
    Write-Section "After Installation - Detecting Changes"
    
    if (-not (Test-Path $SnapshotFile)) {
        Write-Host ""
        Write-Host "✗ No 'before' snapshot found!" -ForegroundColor Red
        Write-Host "  Run this first: .\TrackInstallation.ps1 -Mode before" -ForegroundColor Yellow
        Write-Host ""
        return
    }
    
    $before = Load-Snapshot -FilePath $SnapshotFile
    
    Write-Host ""
    Write-Host "Before snapshot from: $($before.Timestamp)" -ForegroundColor Gray
    Write-Host "Taking new snapshot..." -ForegroundColor Yellow
    
    $paths = $commonPaths.Values | ForEach-Object { $_.Path } | Where-Object { Test-Path $_ }
    $afterSnapshot = Get-DirectorySnapshot -Paths $paths
    
    $after = @{
        Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        Snapshot = $afterSnapshot
    }
    
    Write-Host "Comparing snapshots..." -ForegroundColor Yellow
    
    $changes = Compare-Snapshots -Before $before -After $after
    
    Write-Host ""
    if ($changes.Count -eq 0) {
        Write-Host "No new folders detected." -ForegroundColor Yellow
        Write-Host "The program might have:" -ForegroundColor Gray
        Write-Host "  • Installed to a location we're not monitoring" -ForegroundColor Gray
        Write-Host "  • Only modified existing folders" -ForegroundColor Gray
        Write-Host "  • Been a portable app that didn't create folders" -ForegroundColor Gray
    } else {
        Write-Host "Found $($changes.Count) new folders:" -ForegroundColor Green
        Write-Host ""
        
        $grouped = $changes | Group-Object Location
        
        foreach ($group in $grouped) {
            Write-Host "Location: $($group.Name)" -ForegroundColor Yellow
            foreach ($item in $group.Group) {
                Write-Host "  • $($item.FolderName)" -ForegroundColor White
                Write-Host "    Path: $($item.FullPath)" -ForegroundColor Gray
                Write-Host "    Created: $($item.Created)" -ForegroundColor Gray
                
                # Suggest junction creation
                $isAITool = $item.FolderName -match '(claude|cursor|ollama|ai|mcp|llm|agent|gemini|zed|windsurf|copilot)'
                if ($isAITool) {
                    Write-Host "    → Looks like an AI tool! Consider linking to AI_hub" -ForegroundColor Green
                }
                Write-Host ""
            }
        }
        
        # Generate junction commands
        Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
        Write-Host "  Suggested Junction Commands" -ForegroundColor White
        Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
        Write-Host ""
        
        foreach ($change in $changes) {
            $category = switch -Wildcard ($change.Location) {
                "*AppData\Roaming*" { "AppData_Roaming" }
                "*AppData\Local\Programs*" { "AppData_Local" }
                "*Users\*" { "User_Dot" }
                "*Program Files*" { "System_ProgramFiles" }
                default { "Unknown" }
            }
            
            $name = $change.FolderName -replace '^\.'
            $junctionName = "${name}_${category}"
            
            Write-Host "mklink /J ""$env:USERPROFILE\AI_hub\$junctionName"" ""$($change.FullPath)""" -ForegroundColor Cyan
        }
        Write-Host ""
    }
    
    # Clean up snapshot
    Write-Host "Clean up snapshot file? (Y/N): " -NoNewline -ForegroundColor Yellow
    $response = Read-Host
    if ($response -eq 'Y' -or $response -eq 'y') {
        Remove-Item $SnapshotFile -ErrorAction SilentlyContinue
        Write-Host "✓ Snapshot file removed" -ForegroundColor Green
    }
}

function Show-PredictionGuide {
    Write-Section "Where Will My Program Install?"
    
    Write-Host ""
    Write-Host "Answer these questions:" -ForegroundColor Yellow
    Write-Host ""
    
    Write-Host "1. What type of installer is it?" -ForegroundColor White
    Write-Host "   [M] .MSI file (Windows Installer)" -ForegroundColor Gray
    Write-Host "   [E] .EXE file (Setup executable)" -ForegroundColor Gray
    Write-Host "   [Z] .ZIP/.7z (Portable/extract)" -ForegroundColor Gray
    Write-Host "   [S] Microsoft Store" -ForegroundColor Gray
    Write-Host "   [C] Chocolatey/Scoop/Winget" -ForegroundColor Gray
    Write-Host "   [N] NPM/Node package" -ForegroundColor Gray
    Write-Host "   [P] Python/pip package" -ForegroundColor Gray
    Write-Host ""
    
    $type = Read-Host "Type"
    
    $prediction = switch ($type.ToUpper()) {
        "M" { $installerPatterns["MSI Installer"] }
        "E" { $installerPatterns["EXE Installer"] }
        "Z" { $installerPatterns["Portable/ZIP"] }
        "S" { $installerPatterns["Microsoft Store"] }
        "C" { 
            Write-Host ""
            Write-Host "Which package manager?" -ForegroundColor Yellow
            Write-Host "  [1] Chocolatey" -ForegroundColor Gray
            Write-Host "  [2] Scoop" -ForegroundColor Gray
            $pm = Read-Host "Choice"
            if ($pm -eq "1") { $installerPatterns["Chocolatey"] }
            else { $installerPatterns["Scoop"] }
        }
        "N" { $installerPatterns["NPM Global"] }
        "P" { $installerPatterns["Python/pip"] }
        default { $null }
    }
    
    if ($prediction) {
        Write-Host ""
        Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Green
        Write-Host "  PREDICTION" -ForegroundColor White
        Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Green
        Write-Host ""
        Write-Host "Program files will likely go to:" -ForegroundColor Yellow
        foreach ($loc in $prediction.Locations) {
            Write-Host "  • $loc" -ForegroundColor White
        }
        Write-Host ""
        Write-Host "Config/settings will likely go to:" -ForegroundColor Yellow
        foreach ($loc in $prediction.ConfigLocations) {
            Write-Host "  • $loc" -ForegroundColor White
        }
        Write-Host ""
        Write-Host "Requires Admin: " -NoNewline -ForegroundColor Yellow
        if ($prediction.RequiresAdmin) {
            Write-Host "YES - Run installer as Administrator" -ForegroundColor Red
        } else {
            Write-Host "NO - Can install as normal user" -ForegroundColor Green
        }
        Write-Host ""
    }
}

# ============================================================================
# Main Menu
# ============================================================================

function Show-Menu {
    Clear-Host
    Write-Section "Installation Location Tracker"
    
    Write-Host ""
    Write-Host "What would you like to do?" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  [1] Track installation (Before/After snapshots)" -ForegroundColor White
    Write-Host "  [2] Show common AI tool locations" -ForegroundColor White
    Write-Host "  [3] Predict where a program will install" -ForegroundColor White
    Write-Host "  [4] Show installer type guide" -ForegroundColor White
    Write-Host "  [Q] Quit" -ForegroundColor Gray
    Write-Host ""
    
    $choice = Read-Host "Choice"
    
    switch ($choice.ToUpper()) {
        "1" {
            Write-Host ""
            Write-Host "Installation Tracking" -ForegroundColor Cyan
            Write-Host "  [B] Take 'before' snapshot" -ForegroundColor White
            Write-Host "  [A] Take 'after' snapshot and compare" -ForegroundColor White
            Write-Host ""
            $subChoice = Read-Host "Choice"
            
            if ($subChoice.ToUpper() -eq "B") {
                Start-InstallationTracking
            } elseif ($subChoice.ToUpper() -eq "A") {
                Show-InstallationChanges
            }
            
            Write-Host ""
            Read-Host "Press Enter to continue"
            Show-Menu
        }
        "2" {
            Show-CommonLocations
            Write-Host ""
            Read-Host "Press Enter to continue"
            Show-Menu
        }
        "3" {
            Show-PredictionGuide
            Write-Host ""
            Read-Host "Press Enter to continue"
            Show-Menu
        }
        "4" {
            Show-InstallerTypeGuide
            Write-Host ""
            Read-Host "Press Enter to continue"
            Show-Menu
        }
        "Q" {
            Write-Host ""
            Write-Host "Goodbye!" -ForegroundColor Green
            exit
        }
        default {
            Show-Menu
        }
    }
}

# ============================================================================
# Entry Point
# ============================================================================

switch ($Mode.ToLower()) {
    "before" { Start-InstallationTracking }
    "after" { Show-InstallationChanges }
    "predict" { Show-PredictionGuide }
    "locations" { Show-CommonLocations }
    "guide" { Show-InstallerTypeGuide }
    default { Show-Menu }
}
