param(
    [switch]$DryRun,
    [int]$TimeoutSeconds = 8
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path $PSScriptRoot -Parent
$configPath = Join-Path $repoRoot "config.yaml"
$setEnvPath = Join-Path $PSScriptRoot "set-env.ps1"
$orchestratorPath = Join-Path $PSScriptRoot "discovery-orchestrator.py"

if (-not (Test-Path $setEnvPath)) {
    Write-Host "Missing script: $setEnvPath" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $orchestratorPath)) {
    Write-Host "Missing script: $orchestratorPath" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $configPath)) {
    Write-Host "Missing config: $configPath" -ForegroundColor Red
    exit 1
}

. $setEnvPath

$argsList = @(
    $orchestratorPath,
    "--config", $configPath,
    "--timeout", $TimeoutSeconds
)
if ($DryRun) {
    $argsList += "--dry-run"
}

python @argsList
if ($LASTEXITCODE -ne 0) {
    Write-Host "Orchestrator discovery failed." -ForegroundColor Red
    exit $LASTEXITCODE
}

Write-Host "Orchestrator discovery completed." -ForegroundColor Green
