# View User-Specific Spend Report
# Track individual user usage across all models

param(
    [Parameter(Mandatory=$true)]
    [string]$UserId,
    
    [string]$StartDate = (Get-Date).AddDays(-30).ToString("yyyy-MM-dd"),
    [string]$EndDate = (Get-Date).ToString("yyyy-MM-dd"),
    
    [switch]$Detailed,
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

Write-Host "👤 User Spend Report" -ForegroundColor Cyan
Write-Host "===================" -ForegroundColor Cyan
Write-Host "User ID: $UserId" -ForegroundColor Yellow
Write-Host "Period: $StartDate to $EndDate" -ForegroundColor Yellow

try {
    # Get user info
    $Uri = "$ProxyUrl/user/info?user_id=$UserId"
    Write-Host "Fetching user data..." -ForegroundColor Yellow
    
    $UserResponse = Invoke-RestMethod -Uri $Uri `
        -Method Get `
        -Headers @{ "Authorization" = "Bearer $MasterKey" } `
        -TimeoutSec 30

    if (-not $UserResponse) {
        Write-Host "No data found for user: $UserId" -ForegroundColor Yellow
        exit 0
    }

    # Display user summary
    $UserInfo = $UserResponse.user_info
    Write-Host "`n💰 Total User Spend: $($UserInfo.spend.ToString('C'))" -ForegroundColor Green

    # API Keys breakdown
    if ($UserResponse.keys -and $UserResponse.keys.Count -gt 0) {
        Write-Host "`n🔑 API Keys ($($UserResponse.keys.Count)):" -ForegroundColor Cyan
        Write-Host "────────────────────────────────────" -ForegroundColor Gray
        
        foreach ($Key in $UserResponse.keys) {
            Write-Host "Key: $($Key.key_alias.Substring(0, 20))..." -ForegroundColor White
            Write-Host "  Spend: $($Key.spend.ToString('C'))" -ForegroundColor Gray
            Write-Host "  Requests: $(if ($Key.model_spend) { $Key.model_spend.PSObject.Properties | ForEach-Object { $_.Value.api_requests } | Measure-Object -Sum | Select-Object -ExpandProperty Sum } else { 'N/A' })" -ForegroundColor Gray
            Write-Host "  Models: $(if ($Key.model_spend) { $Key.model_spend.PSObject.Properties.Name -join ', ' } else { 'None' })" -ForegroundColor Gray
            Write-Host ""
        }
    }

    # Teams breakdown
    if ($UserResponse.teams -and $UserResponse.teams.Count -gt 0) {
        Write-Host "👥 Teams ($($UserResponse.teams.Count)):" -ForegroundColor Cyan
        Write-Host "─────────────────────────────" -ForegroundColor Gray
        
        foreach ($Team in $UserResponse.teams) {
            Write-Host "Team: $($Team.team_name)" -ForegroundColor White
            Write-Host "  Spend: $($Team.spend.ToString('C'))" -ForegroundColor Gray
        }
    }

    # Get detailed activity if requested
    if ($Detailed) {
        Write-Host "`n📊 Detailed Activity" -ForegroundColor Cyan
        Write-Host "===================" -ForegroundColor Cyan
        
        # Get daily activity for this user
        $ActivityUri = "$ProxyUrl/user/daily/activity?start_date=$StartDate&end_date=$EndDate&user_id=$UserId"
        $ActivityResponse = Invoke-RestMethod -Uri $ActivityUri `
            -Method Get `
            -Headers @{ "Authorization" = "Bearer $MasterKey" } `
            -TimeoutSec 30

        if ($ActivityResponse.results -and $ActivityResponse.results.Count -gt 0) {
            $ReportData = @()
            
            foreach ($DayData in $ActivityResponse.results) {
                $Date = $DayData.date
                $Metrics = $DayData.metrics
                
                Write-Host "`n📅 $Date" -ForegroundColor Green
                Write-Host "  Spend: $($Metrics.spend.ToString('C'))" -ForegroundColor White
                Write-Host "  Tokens: $($Metrics.total_tokens:N0)" -ForegroundColor Gray
                Write-Host "  Requests: $($Metrics.api_requests:N0)" -ForegroundColor Gray

                # Model breakdown for this day
                if ($DayData.breakdown.models) {
                    $DayData.breakdown.models.PSObject.Properties | ForEach-Object {
                        $ModelName = $_.Name
                        $ModelData = $_.Value
                        Write-Host "    $ModelName`: $($ModelData.spend.ToString('C'))" -ForegroundColor DarkGray
                    }
                }

                # Add to export data
                $ReportData += [PSCustomObject]@{
                    Date = $Date
                    UserId = $UserId
                    TotalSpend = $Metrics.spend
                    TotalTokens = $Metrics.total_tokens
                    PromptTokens = $Metrics.prompt_tokens
                    CompletionTokens = $Metrics.completion_tokens
                    APIRequests = $Metrics.api_requests
                }
            }

            # Export detailed data if requested
            if ($ExportCSV) {
                $CSVPath = "user-$UserId-usage-$(Get-Date -Format 'yyyyMMdd-HHmmss').csv"
                $ReportData | Export-Csv -Path $CSVPath -NoTypeInformation
                Write-Host "`n💾 Detailed report exported to: $CSVPath" -ForegroundColor Green
            }
        } else {
            Write-Host "No detailed activity found for the specified period." -ForegroundColor Yellow
        }
    }

    # Budget analysis
    Write-Host "`n📈 Usage Insights" -ForegroundColor Cyan
    Write-Host "==================" -ForegroundColor Cyan
    
    $DailyAverage = if ($UserResponse.keys) {
        $UserResponse.keys | ForEach-Object { $_.spend } | Measure-Object -Average | Select-Object -ExpandProperty Average
    } else { 0 }
    
    Write-Host "📊 Average Daily Spend: $(($DailyAverage).ToString('C'))" -ForegroundColor White
    Write-Host "🎯 Most Used Models: $(if ($UserResponse.keys -and $UserResponse.keys.Count -gt 0) { ($UserResponse.keys | ForEach-Object { $_.model_spend.PSObject.Properties.Name } | Sort-Object | Get-Unique) -join ', ' } else { 'None' })" -ForegroundColor White

} catch {
    Write-Host "❌ Failed to fetch user spend report." -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "   Ensure the proxy is running at $ProxyUrl" -ForegroundColor Yellow
    
    if ($_.Exception.Response) {
        Write-Host "   HTTP Status: $($_.Exception.Response.StatusCode)" -ForegroundColor Red
        if ($_.Exception.Response.StatusCode -eq "NotFound") {
            Write-Host "   User '$UserId' not found or has no usage data." -ForegroundColor Yellow
        }
    }
}