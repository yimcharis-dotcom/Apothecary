param(
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path $PSScriptRoot -Parent
$configPath = Join-Path $repoRoot "config.yaml"
$setEnvPath = Join-Path $PSScriptRoot "set-env.ps1"
$discoveryPath = Join-Path $PSScriptRoot "discovery-subagents.py"

if (-not (Test-Path $setEnvPath)) {
    Write-Host "Missing script: $setEnvPath" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $discoveryPath)) {
    Write-Host "Missing script: $discoveryPath" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $configPath)) {
    Write-Host "Missing config: $configPath" -ForegroundColor Red
    exit 1
}

. $setEnvPath

$argsList = @($discoveryPath, "--config", $configPath)
if ($DryRun) {
    $argsList += "--dry-run"
}

python @argsList
if ($LASTEXITCODE -ne 0) {
    Write-Host "Subagent discovery failed." -ForegroundColor Red
    exit $LASTEXITCODE
}

Write-Host "Subagent discovery completed." -ForegroundColor Green
