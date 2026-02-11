# Script to Enable Auto-Sync of Model Prices
# This tells LiteLLM to check GitHub for new model definitions/prices periodically.
# Useful for "Day-0 Launch" support without restarting the proxy.

# Load environment variables (specifically LITELLM_MASTER_KEY)
$ScriptDir = Split-Path $MyInvocation.MyCommand.Path
. "$ScriptDir\set-env.ps1"

$ProxyUrl = "http://127.0.0.1:4000"
$MasterKey = $env:LITELLM_MASTER_KEY

if (-not $MasterKey) {
    Write-Host "Error: LITELLM_MASTER_KEY not found in environment." -ForegroundColor Red
    exit 1
}

Write-Host "🔄 Scheduling Auto-Sync for Model Prices..." -ForegroundColor Cyan

try {
    # Default: Check every 6 hours
    $Hours = 6
    $Uri = "$ProxyUrl/schedule/model_cost_map_reload?hours=$Hours"
    
    $Response = Invoke-RestMethod -Uri $Uri `
        -Method Post `
        -Headers @{ "Authorization" = "Bearer $MasterKey" }

    Write-Host "✅ Auto-sync scheduled successfully!" -ForegroundColor Green
    Write-Host "   LiteLLM will check for new model prices every $Hours hours." -ForegroundColor Gray
    Write-Host "   Response: $($Response | ConvertTo-Json -Depth 1)" -ForegroundColor DarkGray
} catch {
    Write-Host "❌ Failed to schedule auto-sync." -ForegroundColor Red
    Write-Host "   Error: $_" -ForegroundColor Red
    Write-Host "   Ensure the proxy is running at $ProxyUrl" -ForegroundColor Yellow
}
