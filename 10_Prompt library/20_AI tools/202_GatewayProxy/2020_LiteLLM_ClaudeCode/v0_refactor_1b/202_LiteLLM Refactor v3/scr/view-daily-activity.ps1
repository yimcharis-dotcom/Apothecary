# Enhanced Daily Activity Report Script
# Shows detailed breakdown of LLM usage by day, model, and API key

param(
    [string]$StartDate = (Get-Date).AddDays(-7).ToString("yyyy-MM-dd"),
    [string]$EndDate = (Get-Date).ToString("yyyy-MM-dd"),
    [string]$UserId = $null,
    [string]$TeamId = $null,
    [switch]$Summary,
    [switch]$ExportCSV
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

Write-Host "📊 Generating Daily Activity Report" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan
Write-Host "Period: $StartDate to $EndDate" -ForegroundColor Yellow

# Build query parameters
$QueryParams = @{
    start_date = $StartDate
    end_date = $EndDate
}

if ($UserId) { $QueryParams.user_id = $UserId }
if ($TeamId) { $QueryParams.team_id = $TeamId }

# Build the URI with parameters
$UriBuilder = [System.UriBuilder]("$ProxyUrl/user/daily/activity")
$UriBuilder.Query = ($QueryParams.GetEnumerator() | ForEach-Object { "$($_.Key)=$($_.Value)" }) -join "&"
$Uri = $UriBuilder.ToString()

try {
    Write-Host "Fetching data from proxy..." -ForegroundColor Yellow
    $Response = Invoke-RestMethod -Uri $Uri `
        -Method Get `
        -Headers @{ "Authorization" = "Bearer $MasterKey" } `
        -TimeoutSec 30

    if (-not $Response.results -or $Response.results.Count -eq 0) {
        Write-Host "No usage data found for the specified period." -ForegroundColor Yellow
        exit 0
    }

    # Process and display results
    $ReportData = @()
    
    foreach ($DayData in $Response.results) {
        $Date = $DayData.date
        $Metrics = $DayData.metrics
        
        Write-Host "`n📅 Date: $Date" -ForegroundColor Green
        Write-Host "─────────────────────────────────" -ForegroundColor Gray
        
        # Summary metrics
        Write-Host "💰 Total Spend: $($Metrics.spend.ToString('C'))" -ForegroundColor White
        Write-Host "🔤 Total Tokens: $($Metrics.total_tokens:N0)" -ForegroundColor Gray
        Write-Host "📝 Input Tokens: $($Metrics.prompt_tokens:N0)" -ForegroundColor Gray
        Write-Host "💬 Output Tokens: $($Metrics.completion_tokens:N0)" -ForegroundColor Gray
        Write-Host "🔄 API Requests: $($Metrics.api_requests:N0)" -ForegroundColor Gray

        # Model breakdown
        if ($DayData.breakdown.models) {
            Write-Host "`n🤖 Model Breakdown:" -ForegroundColor Cyan
            $DayData.breakdown.models.PSObject.Properties | ForEach-Object {
                $ModelName = $_.Name
                $ModelData = $_.Value
                Write-Host "  $ModelName`: $($ModelData.spend.ToString('C')) ($($ModelData.total_tokens:N0) tokens)" -ForegroundColor White
            }
        }

        # Provider breakdown
        if ($DayData.breakdown.providers) {
            Write-Host "`n🏢 Provider Breakdown:" -ForegroundColor Cyan
            $DayData.breakdown.providers.PSObject.Properties | ForEach-Object {
                $ProviderName = $_.Name
                $ProviderData = $_.Value
                Write-Host "  $ProviderName`: $($ProviderData.spend.ToString('C')) ($($ProviderData.total_tokens:N0) tokens)" -ForegroundColor White
            }
        }

        # Add to report data for export
        $ReportData += [PSCustomObject]@{
            Date = $Date
            TotalSpend = $Metrics.spend
            TotalTokens = $Metrics.total_tokens
            PromptTokens = $Metrics.prompt_tokens
            CompletionTokens = $Metrics.completion_tokens
            APIRequests = $Metrics.api_requests
            AvgCostPerToken = if ($Metrics.total_tokens -gt 0) { $Metrics.spend / $Metrics.total_tokens } else { 0 }
        }
    }

    # Overall summary
    $TotalSpend = $Response.metadata.total_spend
    $TotalTokens = $Response.metadata.total_prompt_tokens + $Response.metadata.total_completion_tokens
    $TotalRequests = $Response.metadata.total_api_requests

    Write-Host "`n📈 OVERALL SUMMARY" -ForegroundColor Green
    Write-Host "==================" -ForegroundColor Green
    Write-Host "💰 Total Period Spend: $($TotalSpend.ToString('C'))" -ForegroundColor White
    Write-Host "🔤 Total Tokens: $($TotalTokens:N0)" -ForegroundColor Gray
    Write-Host "🔄 Total Requests: $($TotalRequests:N0)" -ForegroundColor Gray
    Write-Host "💸 Avg Cost per 1K Tokens: $(if ($TotalTokens -gt 0) { ($TotalSpend * 1000 / $TotalTokens).ToString('C') } else { '$0.00' })" -ForegroundColor Gray

    # Export to CSV if requested
    if ($ExportCSV) {
        $CSVPath = "litellm-usage-report-$(Get-Date -Format 'yyyyMMdd-HHmmss').csv"
        $ReportData | Export-Csv -Path $CSVPath -NoTypeInformation
        Write-Host "`n💾 Report exported to: $CSVPath" -ForegroundColor Green
    }

} catch {
    Write-Host "❌ Failed to fetch daily activity report." -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "   Ensure the proxy is running at $ProxyUrl" -ForegroundColor Yellow
    
    if ($_.Exception.Response) {
        Write-Host "   HTTP Status: $($_.Exception.Response.StatusCode)" -ForegroundColor Red
    }
}