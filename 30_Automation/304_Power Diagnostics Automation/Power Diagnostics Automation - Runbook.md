---
Created: 2026-02-03
Updated: 2026-02-03T00:00:00
Tags:
  - runbook
  - powercfg
  - battery
  - diagnostics
  - automation
  - schtasks
words:
  2026-02-03: 583
---
## Purpose

Collect repeatable power/battery diagnostics without manual steps. This produces timestamped HTML reports plus a small CSV you can graph later.

It is designed for Modern Standby systems, but also works on standard sleep systems.

## Outputs

All output goes to: [`C:\PowerDiagnostics\`](file:///C:/PowerDiagnostics) 

Files created:
- `batteryreport-YYYYMMDD-HHMMSS.html`
- `sleepstudy-YYYYMMDD-HHMMSS.html` (best-effort; may fail on some builds)
- `battery-metrics.csv` (appended trend log)
- Optional: `energy-YYYYMMDD-HHMMSS.html` (admin-only)

## Prerequisites

- Windows built-in tool: `powercfg` (present on Windows 10/11).
- Create directories:   - [`C:\PowerDiagnostics_Scripts\`](file:///C:/PowerDiagnostics_Scripts)
- 
- and  [`C:\PowerDiagnostics\`](file:///C:/PowerDiagnostics) 
- If you schedule the optional `energy` report: run the task with elevated privileges.

## Install steps

1) Create folders:
   - [`C:\PowerDiagnostics_Scripts\`](file:///C:/PowerDiagnostics_Scripts)
   - [`C:\PowerDiagnostics\`](file:///C:/PowerDiagnostics) 

2) Save the script below as:
   - [`C:\PowerDiagnostics_Scripts\`](file:///C:/PowerDiagnostics_Scripts) 

3) Test run manually:
   - Open PowerShell and run the command in **Run manually** below.

4) Schedule it:
   - Use the `schtasks` command in **Schedule** below.

## Script: Save-[PowerDiagnostics.ps1](file:///C:/PowerDiagnostics/PowerDiagnostics.ps1)

```powershell
$root = "C:\PowerDiagnostics"
New-Item -ItemType Directory -Force -Path $root | Out-Null

$ts = Get-Date -Format "yyyyMMdd-HHmmss"
$batPath   = Join-Path $root "batteryreport-$ts.html"
$sleepPath = Join-Path $root "sleepstudy-$ts.html"
$logPath   = Join-Path $root "battery-metrics.csv"

# Battery report
powercfg /batteryreport /output $batPath | Out-Null

# Sleep study (Modern Standby). Best-effort.
try {
  powercfg /sleepstudy /output $sleepPath | Out-Null
} catch {}

# Parse a few metrics from the battery report HTML (best-effort parsing).
$html = Get-Content -Raw -Encoding UTF8 $batPath

function Get-FirstMatch($text, $pattern) {
  $m = [regex]::Match($text, $pattern, "IgnoreCase")
  if ($m.Success) { return $m.Groups[1].Value.Trim() }
  return ""
}

$design = Get-FirstMatch $html 'DESIGN CAPACITY</td>\s*<td[^>]*>\s*([\d,]+)\s*mWh'
$full   = Get-FirstMatch $html 'FULL CHARGE CAPACITY</td>\s*<td[^>]*>\s*([\d,]+)\s*mWh'
$cycles = Get-FirstMatch $html 'CYCLE COUNT</td>\s*<td[^>]*>\s*([\d,]+)'
$health = ""

if ($design -and $full) {
  $d = [double]($design -replace ",","")
  $f = [double]($full   -replace ",","")
  if ($d -gt 0) { $health = "{0:P1}" -f ($f / $d) }
}

if (!(Test-Path $logPath)) {
  "timestamp,design_mWh,full_mWh,cycle_count,full_vs_design" | Out-File -Encoding UTF8 $logPath
}

"$ts,$($design -replace ',',''),$($full -replace ',',''),$($cycles -replace ',',''),$health" |
  Out-File -Append -Encoding UTF8 $logPath

# Optional: energy report (usually requires admin). Uncomment if desired.
# $energyPath = Join-Path $root "energy-$ts.html"
# powercfg /energy /duration 60 /output $energyPath | Out-Null
```

## Run manually
```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\Scripts\Save-PowerDiagnostics.ps1
```

# Schedule (Task Scheduler via #schtasks ) 

**Creates a daily task at 03:00 that runs as SYSTEM with highest privileges:**

```bat
schtasks /Create /TN "PowerDiagnostics" /SC WEEKLY /D SUN /ST 03:00 /RU SYSTEM /RL HIGHEST ^
 /TR "powershell.exe -NoProfile -ExecutionPolicy Bypass -File  C:\PowerDiagnostics_Scripts\Save-PowerDiagnostics.ps1"

```

-Verify it exists:

```bat
schtasks /Query /TN "PowerDiagnostics" /V /FO LIST
```

-Run it once immediately:

```bat
schtasks /Run /TN "PowerDiagnostics"
```
# Operational notes

For consistent results, prefer running when:

- The machine is plugged in.
    
- The lid is open and the system is idle (no heavy downloads, calls, games).
    
- You do not have external USB devices that constantly wake the system (optional).
    

If you use smart charging (charge cap), the “full charge capacity” estimate can drift. Use trends over weeks, not single readings.

## Removal

Delete the scheduled task:

```bat
schtasks /Delete /TN "PowerDiagnostics" /F

```
Remove folders (optional):

- [PowerDiagnostics.ps1](file:///C:/PowerDiagnostics/PowerDiagnostics.ps1)
    
- [`C:\PowerDiagnostics\`](file:///C:/PowerDiagnostics) 
    
