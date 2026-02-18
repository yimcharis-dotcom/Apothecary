# LiteLLM Proxy Startup Script
# Load environment variables and start the proxy

# Fix unicode issues in Windows console
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"

$configPath = Join-Path (Split-Path $PSScriptRoot -Parent) "config.yaml"
$setEnvPath = Join-Path $PSScriptRoot "set-env.ps1"

if (-not (Test-Path $setEnvPath)) {
    Write-Host "Missing script: $setEnvPath" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $configPath)) {
    Write-Host "Missing config: $configPath" -ForegroundColor Red
    exit 1
}

# Load API keys and Claude Code settings
. $setEnvPath

# Default to no-db mode unless explicitly enabled.
if ($env:LITELLM_ENABLE_DB -ne "1") {
    Remove-Item Env:DATABASE_URL -ErrorAction SilentlyContinue
    Remove-Item Env:DIRECT_URL -ErrorAction SilentlyContinue
    Write-Host "[INFO] DB mode disabled (set LITELLM_ENABLE_DB=1 to enable DB)." -ForegroundColor DarkYellow
}

Write-Host "`n=====================================" -ForegroundColor Cyan
Write-Host "   Starting LiteLLM Proxy" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Discovery logic temporarily disabled to ensure stability
# Manual discovery: .\run-orchestrator-discovery.ps1
Write-Host "[INFO] For model updates, run: .\run-orchestrator-discovery.ps1" -ForegroundColor Gray
Write-Host ""

Write-Host "Config: $configPath" -ForegroundColor Yellow
Write-Host "Proxy URL: http://127.0.0.1:4000" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop the proxy" -ForegroundColor Yellow
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Start the proxy safely
$litellmExe = Join-Path $env:APPDATA "Python\Python312\Scripts\litellm.exe"
$litellmArgs = @("--config", $configPath, "--port", "4000")

if (Test-Path $litellmExe) {
    Write-Host "Runtime: Python 3.12 LiteLLM executable" -ForegroundColor Yellow
    & $litellmExe @litellmArgs
} else {
    Write-Host "Runtime: PATH litellm executable" -ForegroundColor Yellow
    & litellm @litellmArgs
}
