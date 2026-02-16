# Model Sync Status Checker
# Check and display auto-sync status and model information

param(
    [switch]$Detailed,
    [switch]$ListModels,
    [switch]$Monitor  # Continuous monitoring mode
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

function Show-SyncStatus {
    try {
        Write-Host "🔄 Checking Sync Status..." -ForegroundColor Yellow
        
        $Uri = "$ProxyUrl/schedule/model_cost_map_reload/status"
        $Response = Invoke-RestMethod -Uri $Uri `
            -Method Get `
            -Headers @{ "Authorization" = "Bearer $MasterKey" } `
            -TimeoutSec 10

        Write-Host "`n✅ Auto-Sync Status" -ForegroundColor Green
        Write-Host "===================" -ForegroundColor Green
        
        if ($Response.last_sync) {
            $LastSync = [DateTime]$Response.last_sync
            $TimeSince = (Get-Date) - $LastSync
            Write-Host "🕒 Last Sync: $($LastSync.ToString('yyyy-MM-dd HH:mm:ss'))" -ForegroundColor White
            Write-Host "⏱️  Time Since: $($TimeSince.Hours)h $($TimeSince.Minutes)m ago" -ForegroundColor Gray
        } else {
            Write-Host "🕒 Last Sync: Never" -ForegroundColor Red
        }
        
        if ($Response.next_sync) {
            $NextSync = [DateTime]$Response.next_sync
            $TimeUntil = $NextSync - (Get-Date)
            Write-Host "⏭️  Next Sync: $($NextSync.ToString('yyyy-MM-dd HH:mm:ss'))" -ForegroundColor White
            Write-Host "⏰ Time Until: $($TimeUntil.Hours)h $($TimeUntil.Minutes)m" -ForegroundColor Gray
        } else {
            Write-Host "⏭️  Next Sync: Not scheduled" -ForegroundColor Yellow
            Write-Host "💡 Run '.\enable-auto-sync.ps1' to schedule automatic updates" -ForegroundColor Cyan
        }
        
        if ($Response.sync_interval_hours) {
            Write-Host "🔄 Sync Interval: $($Response.sync_interval_hours) hours" -ForegroundColor White
        }
        
        if ($Response.status) {
            $Color = if ($Response.status -eq "active") { "Green" } elseif ($Response.status -eq "error") { "Red" } else { "Yellow" }
            Write-Host "📊 Status: $($Response.status)" -ForegroundColor $Color
        }

        return $Response

    } catch {
        Write-Host "❌ Failed to check sync status." -ForegroundColor Red
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
        
        if ($_.Exception.Response -and $_.Exception.Response.StatusCode -eq "NotFound") {
            Write-Host "   Auto-sync may not be configured. Run '.\enable-auto-sync.ps1' first." -ForegroundColor Yellow
        }
        
        return $null
    }
}

function Show-ModelInfo {
    try {
        Write-Host "`n🤖 Available Models" -ForegroundColor Cyan
        Write-Host "===================" -ForegroundColor Cyan
        
        $Uri = "$ProxyUrl/v1/models"
        $Response = Invoke-RestMethod -Uri $Uri `
            -Method Get `
            -TimeoutSec 10

        $Models = $Response.data | Sort-Object id
        
        Write-Host "Total Models Available: $($Models.Count)" -ForegroundColor Green
        Write-Host ""
        
        # Group by provider
        $GroupedModels = $Models | Group-Object { 
            if ($_.id -like "grok*") { "xAI (Grok)" }
            elseif ($_.id -like "perplexity*") { "Perplexity" }
            elseif ($_.id -like "gemini*") { "Google (Gemini)" }
            elseif ($_.id -like "openrouter*") { "OpenRouter" }
            else { "Other" }
        }
        
        foreach ($Group in $GroupedModels | Sort-Object Name) {
            Write-Host "📦 $($Group.Name) ($($Group.Count) models)" -ForegroundColor White
            Write-Host "─────────────────────────────────" -ForegroundColor Gray
            
            if ($Detailed) {
                foreach ($Model in $Group.Group | Sort-Object id) {
                    Write-Host "  $($Model.id)" -ForegroundColor DarkGray
                }
            } else {
                $ModelNames = ($Group.Group | ForEach-Object { $_.id }) -join ", "
                Write-Host "  $ModelNames" -ForegroundColor DarkGray
            }
            Write-Host ""
        }

        return $Models

    } catch {
        Write-Host "❌ Failed to fetch model list." -ForegroundColor Red
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
        return $null
    }
}

function Show-PricingInfo {
    try {
        Write-Host "`n💰 Pricing Information" -ForegroundColor Cyan
        Write-Host "======================" -ForegroundColor Cyan
        
        # Try to get pricing data from a test request or config
        $TestUri = "$ProxyUrl/global/spend/report"
        $Response = Invoke-RestMethod -Uri $TestUri `
            -Method Get `
            -Headers @{ "Authorization" = "Bearer $MasterKey" } `
            -TimeoutSec 10

        if ($Response -and $Response.Count -gt 0) {
            Write-Host "✅ Pricing data available" -ForegroundColor Green
            Write-Host "📊 Recent activity found with cost tracking" -ForegroundColor White
        } else {
            Write-Host "⚠️  No recent activity with pricing data" -ForegroundColor Yellow
            Write-Host "💡 Make some test requests to verify cost tracking" -ForegroundColor Cyan
        }

    } catch {
        Write-Host "⚠️  Could not verify pricing information" -ForegroundColor Yellow
        Write-Host "   This may be normal if no requests have been made yet" -ForegroundColor Gray
    }
}

# Main execution
if ($Monitor) {
    Write-Host "🔍 Continuous Monitoring Mode (Press Ctrl+C to stop)" -ForegroundColor Green
    Write-Host "=================================================" -ForegroundColor Green
    
    while ($true) {
        Clear-Host
        Write-Host "🔄 LiteLLM Sync Monitor - $(Get-Date)" -ForegroundColor Cyan
        Write-Host "=====================================" -ForegroundColor Cyan
        
        Show-SyncStatus
        
        if ($ListModels) {
            Show-ModelInfo
        }
        
        Write-Host "`n⏳ Refreshing in 60 seconds..." -ForegroundColor Gray
        Start-Sleep -Seconds 60
    }
} else {
    # One-time check
    Show-SyncStatus
    
    if ($ListModels -or $Detailed) {
        Show-ModelInfo
    }
    
    if ($Detailed) {
        Show-PricingInfo
    }
}

Write-Host "`n💡 Tips:" -ForegroundColor Cyan
Write-Host "   • Run '.\enable-auto-sync.ps1' to schedule automatic updates" -ForegroundColor Gray
Write-Host "   • Run '.\sync-models.ps1' to force an immediate update" -ForegroundColor Gray
Write-Host "   • Use -ListModels to see all available models" -ForegroundColor Gray
Write-Host "   • Use -Monitor for continuous status monitoring" -ForegroundColor Gray