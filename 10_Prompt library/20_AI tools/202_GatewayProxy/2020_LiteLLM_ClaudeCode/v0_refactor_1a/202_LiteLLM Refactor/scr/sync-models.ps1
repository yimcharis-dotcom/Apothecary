# Manual Model Sync Script
# Force immediate sync of model pricing data from GitHub

param(
    [switch]$Verbose,
    [switch]$Force
)

# Load environment variables
$ScriptDir = Split-Path $MyInvocation.MyCommand.Path
. "$ScriptDir\set-env.ps1"

$ProxyUrl = "http://127.0.0.1:4000"
$MasterKey = $env:LITELLM_MASTER_KEY

if (-not $MasterKey) {
    Write-Host "Error: LITELLM_MASTER_KEY not found in environment." -ForegroundColor Red
    exit 1
}

Write-Host "🔄 Manual Model Sync" -ForegroundColor Cyan
Write-Host "===================" -ForegroundColor Cyan

# Check if proxy is running
try {
    $HealthResponse = Invoke-RestMethod -Uri "$ProxyUrl/health" -Method Get -TimeoutSec 5
    Write-Host "✅ Proxy is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Proxy is NOT running!" -ForegroundColor Red
    Write-Host "   Please start the proxy first with: .\start-proxy.ps1" -ForegroundColor Red
    exit 1
}

# Get current model count before sync
try {
    if ($Verbose) {
        Write-Host "📊 Counting current models..." -ForegroundColor Yellow
        $ModelsResponse = Invoke-RestMethod -Uri "$ProxyUrl/v1/models" -Method Get -TimeoutSec 10
        $BeforeCount = $ModelsResponse.data.Count
        Write-Host "🔢 Models before sync: $BeforeCount" -ForegroundColor Gray
    }
} catch {
    Write-Host "⚠️  Could not count models before sync" -ForegroundColor Yellow
}

# Perform the sync
try {
    Write-Host "🔄 Syncing model cost map..." -ForegroundColor Yellow
    
    $Uri = "$ProxyUrl/reload/model_cost_map"
    $Response = Invoke-RestMethod -Uri $Uri `
        -Method Post `
        -Headers @{ 
            "Authorization" = "Bearer $MasterKey"
            "Content-Type" = "application/json"
        } `
        -TimeoutSec 30

    Write-Host "✅ Sync completed successfully!" -ForegroundColor Green
    
    if ($Verbose -and $Response) {
        Write-Host "Response details:" -ForegroundColor Gray
        $Response | ConvertTo-Json -Depth 2 | Write-Host
    }

} catch {
    Write-Host "❌ Sync failed!" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    
    if ($_.Exception.Response) {
        Write-Host "   HTTP Status: $($_.Exception.Response.StatusCode)" -ForegroundColor Red
        
        if ($_.Exception.Response.StatusCode -eq "Unauthorized") {
            Write-Host "   Check your LITELLM_MASTER_KEY in set-env.ps1" -ForegroundColor Yellow
        }
    }
    
    exit 1
}

# Get updated model count
try {
    if ($Verbose) {
        Write-Host "📊 Counting updated models..." -ForegroundColor Yellow
        Start-Sleep -Seconds 2  # Brief pause for server to update
        $ModelsResponse = Invoke-RestMethod -Uri "$ProxyUrl/v1/models" -Method Get -TimeoutSec 10
        $AfterCount = $ModelsResponse.data.Count
        
        if ($BeforeCount) {
            $Difference = $AfterCount - $BeforeCount
            $Color = if ($Difference -gt 0) { "Green" } elseif ($Difference -lt 0) { "Yellow" } else { "Gray" }
            Write-Host "🔢 Models after sync: $AfterCount" -ForegroundColor Gray
            Write-Host "📈 Change: $($Difference > 0 ? '+' : '')$Difference models" -ForegroundColor $Color
        } else {
            Write-Host "🔢 Models after sync: $AfterCount" -ForegroundColor Gray
        }
    }
} catch {
    Write-Host "⚠️  Could not count models after sync" -ForegroundColor Yellow
}

# Show a sample of available models
try {
    Write-Host "`n🤖 Sample of Available Models:" -ForegroundColor Cyan
    Write-Host "===============================" -ForegroundColor Gray
    
    $ModelsResponse = Invoke-RestMethod -Uri "$ProxyUrl/v1/models" -Method Get -TimeoutSec 10
    $SampleModels = $ModelsResponse.data | Where-Object { 
        $_.id -like "grok*" -or 
        $_.id -like "perplexity*" -or 
        $_.id -like "gemini*" 
    } | Select-Object -First 10 | Sort-Object id
    
    foreach ($Model in $SampleModels) {
        $Provider = if ($Model.id -like "grok*") { "xAI" }
                   elseif ($Model.id -like "perplexity*") { "Perplexity" }
                   elseif ($Model.id -like "gemini*") { "Google" }
                   else { "Other" }
        
        Write-Host "  $($Model.id) [$Provider]" -ForegroundColor White
    }
    
    $TotalModels = $ModelsResponse.data.Count
    Write-Host "`n📊 Total models available: $TotalModels" -ForegroundColor Green

} catch {
    Write-Host "⚠️  Could not fetch model list after sync" -ForegroundColor Yellow
}

# Test cost tracking functionality
try {
    Write-Host "`n💰 Testing Cost Tracking..." -ForegroundColor Yellow
    
    # Get spend report (might be empty if no requests made)
    $SpendUri = "$ProxyUrl/global/spend/report"
    $SpendResponse = Invoke-RestMethod -Uri $SpendUri `
        -Method Get `
        -Headers @{ "Authorization" = "Bearer $MasterKey" } `
        -TimeoutSec 10
    
    Write-Host "✅ Cost tracking endpoint accessible" -ForegroundColor Green
    
    if ($SpendResponse -and $SpendResponse.Count -gt 0) {
        Write-Host "💸 Existing spend data found" -ForegroundColor White
    } else {
        Write-Host "💸 No spend data yet (make some test requests)" -ForegroundColor Gray
    }

} catch {
    Write-Host "⚠️  Cost tracking test failed" -ForegroundColor Yellow
    Write-Host "   This may be normal if no requests have been made" -ForegroundColor Gray
}

Write-Host "`n🎉 Sync process completed!" -ForegroundColor Green
Write-Host "`n💡 Next steps:" -ForegroundColor Cyan
Write-Host "   • Make test requests to verify the models work" -ForegroundColor Gray
Write-Host "   • Check cost tracking with: .\view-spend.ps1" -ForegroundColor Gray
Write-Host "   • Enable auto-sync with: .\enable-auto-sync.ps1" -ForegroundColor Gray

if ($Verbose) {
    Write-Host "`n📋 Full sync log:" -ForegroundColor Gray
    Write-Host "   Timestamp: $(Get-Date)" -ForegroundColor DarkGray
    Write-Host "   Proxy URL: $ProxyUrl" -ForegroundColor DarkGray
    Write-Host "   Sync endpoint: /reload/model_cost_map" -ForegroundColor DarkGray
    Write-Host "   Auth method: Bearer token" -ForegroundColor DarkGray
}