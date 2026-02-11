# Script to View Global Spend
# Fetches the spend report from the LiteLLM Proxy.

# Load environment variables
$ScriptDir = Split-Path $MyInvocation.MyCommand.Path
. "$ScriptDir\set-env.ps1"

$ProxyUrl = "http://127.0.0.1:4000"
$MasterKey = $env:LITELLM_MASTER_KEY

if (-not $MasterKey) {
    Write-Host "Error: LITELLM_MASTER_KEY not found in environment." -ForegroundColor Red
    exit 1
}

Write-Host "Fetching Global Spend Report..." -ForegroundColor Cyan

# Calculate dates (Current Year)
$StartDate = (Get-Date -Day 1 -Month 1).ToString("yyyy-MM-dd")
$EndDate = (Get-Date).AddDays(1).ToString("yyyy-MM-dd")

try {
    $Uri = "$ProxyUrl/global/spend/report?start_date=$StartDate&end_date=$EndDate"
    
    $Response = Invoke-RestMethod -Uri $Uri `
        -Method Get `
        -Headers @{ "Authorization" = "Bearer $MasterKey" }

    Write-Host "`nSpend Summary ($StartDate to $EndDate)" -ForegroundColor Yellow
    Write-Host "--------------------------------" -ForegroundColor Yellow
    
    # Display the spend
    if ($Response.spend) {
        Write-Host "Total Spend: " -NoNewline
        Write-Host "$($Response.spend)" -ForegroundColor Green
    } else {
        # If response is an array or different format
        $Response | Format-List
    }
    
    Write-Host "`nTo see detailed logs, query the database directly or use the UI." -ForegroundColor DarkGray

} catch {
    Write-Host "Failed to fetch spend report." -ForegroundColor Red
    Write-Host "   Error: $_" -ForegroundColor Red
    Write-Host "   Ensure the proxy is running and 'general_settings.database_url' is configured." -ForegroundColor Yellow
}
