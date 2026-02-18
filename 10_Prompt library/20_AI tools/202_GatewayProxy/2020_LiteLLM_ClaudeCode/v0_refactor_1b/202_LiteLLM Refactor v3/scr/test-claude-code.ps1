param(
    [string]$Model = "default",
    [string]$Prompt = "Reply with exactly: OK",
    [int]$TimeoutSec = 30
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path $MyInvocation.MyCommand.Path
. "$ScriptDir\set-env.ps1"

$ProxyUrl = "http://127.0.0.1:4000"
$MasterKey = $env:LITELLM_MASTER_KEY

if ([string]::IsNullOrWhiteSpace($MasterKey)) {
    Write-Host "Missing LITELLM_MASTER_KEY in environment." -ForegroundColor Red
    exit 1
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "LiteLLM Responses API Smoke Test" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

try {
    Write-Host "Debug: Starting health check..." -ForegroundColor Gray
    Invoke-RestMethod `
        -Uri "$ProxyUrl/health" `
        -Method Get `
        -Headers @{ "Authorization" = "Bearer $MasterKey" } `
        -TimeoutSec 5 | Out-Null
    Write-Host "✓ Proxy health check passed" -ForegroundColor Green
} catch {
    $statusCode = $null
    try { $statusCode = [int]$_.Exception.Response.StatusCode } catch {}
    if ($statusCode -eq 401 -or $statusCode -eq 403) {
        Write-Host "⚠️ /health is protected by auth. Continuing with responses test..." -ForegroundColor DarkYellow
    } else {
        Write-Host "⚠️ Health check failed (PowerShell connectivity issue). Trying responses test anyway..." -ForegroundColor DarkYellow
    }
}

$headers = @{
    "Authorization" = "Bearer $MasterKey"
    "Content-Type"  = "application/json"
}

$body = @{
    model = $Model
    input = @(
        @{
            role    = "user"
            content = @(
                @{
                    type = "input_text"
                    text = $Prompt
                }
            )
        }
    )
}

try {
    Write-Host "Debug: Starting responses test with model $Model..." -ForegroundColor Gray
    $resp = Invoke-RestMethod `
        -Uri "$ProxyUrl/v1/responses" `
        -Method Post `
        -Headers $headers `
        -Body ($body | ConvertTo-Json -Depth 8) `
        -TimeoutSec $TimeoutSec

    $text = $null
    if ($resp.output_text) {
        $text = $resp.output_text
    } elseif ($resp.output -and $resp.output.Count -gt 0 -and $resp.output[0].content -and $resp.output[0].content.Count -gt 0) {
        $text = $resp.output[0].content[0].text
    }

    Write-Host "✓ Responses API test passed" -ForegroundColor Green
    Write-Host "  Model: $Model" -ForegroundColor Gray
    Write-Host "  Response ID: $($resp.id)" -ForegroundColor Gray
    if ($text) {
        Write-Host "  Output: $text" -ForegroundColor White
    } else {
        Write-Host "  Output: (no text field found, request still succeeded)" -ForegroundColor DarkYellow
    }
} catch {
    Write-Host "✗ Responses API test failed" -ForegroundColor Red
    Write-Host "  Error: $($_.Exception.Message)" -ForegroundColor Red

    # Try to extract status code and response body
    if ($_.Exception.Response) {
        $statusCode = [int]$_.Exception.Response.StatusCode
        Write-Host "  Status Code: $statusCode" -ForegroundColor Red
        
        try {
            $stream = $_.Exception.Response.GetResponseStream()
            $reader = New-Object System.IO.StreamReader($stream)
            $body = $reader.ReadToEnd()
            if (-not [string]::IsNullOrWhiteSpace($body)) {
                Write-Host "  Response Body: $body" -ForegroundColor DarkRed
            }
        } catch {}
    }

    exit 1
}
