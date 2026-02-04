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
