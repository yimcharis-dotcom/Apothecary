# Test Claude Code with LiteLLM Proxy
# Run this AFTER starting the proxy in another shell

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Testing Claude Code with LiteLLM Proxy" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Load environment variables
Write-Host "Setting environment variables..." -ForegroundColor Yellow
$env:XAI_API_KEY = "xai-ap3FR5Oo56oqBOAapUvEmH6XUKwL3bBysMNu5POmqRvkZedTDMMGdUs2KelXRQT43TD0nxRnZeaxRDMk"
$env:PERPLEXITY_API_KEY = "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"
$env:ANTHROPIC_BASE_URL = "http://127.0.0.1:4000"
$env:ANTHROPIC_AUTH_TOKEN = "sk-litellm-master-key-12345"

Write-Host "✓ Environment variables set`n" -ForegroundColor Green

# Display configuration
Write-Host "Configuration:" -ForegroundColor Yellow
Write-Host "  XAI_API_KEY: " -NoNewline
Write-Host $env:XAI_API_KEY.Substring(0, 20) + "..." -ForegroundColor Gray
Write-Host "  PERPLEXITY_API_KEY: " -NoNewline
Write-Host $env:PERPLEXITY_API_KEY.Substring(0, 20) + "..." -ForegroundColor Gray
Write-Host "  ANTHROPIC_BASE_URL: " -NoNewline
Write-Host $env:ANTHROPIC_BASE_URL -ForegroundColor Gray
Write-Host "  ANTHROPIC_AUTH_TOKEN: " -NoNewline
Write-Host $env:ANTHROPIC_AUTH_TOKEN.Substring(0, 20) + "..." -ForegroundColor Gray
Write-Host ""

# Check if proxy is running
Write-Host "Checking if proxy is running..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://127.0.0.1:4000/health" -Method Get -TimeoutSec 5
    Write-Host "✓ Proxy is running`n" -ForegroundColor Green
} catch {
    Write-Host "✗ Proxy is NOT running!" -ForegroundColor Red
    Write-Host "  Please start the proxy first with: .\start-proxy.ps1`n" -ForegroundColor Red
    exit 1
}

# Test with Perplexity Sonar
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Testing: claude --model perplexity-sonar" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Running Claude Code with Perplexity Sonar model..." -ForegroundColor Yellow
Write-Host "Command: claude --model perplexity-sonar`n" -ForegroundColor Gray

# Instructions for manual test
Write-Host "`nREADY TO TEST!" -ForegroundColor Green
Write-Host "`nNow run this command:" -ForegroundColor Yellow
Write-Host "  claude --model perplexity-sonar" -ForegroundColor White
Write-Host "`nOr try other models:" -ForegroundColor Yellow
Write-Host "  claude --model grok-4-1-fast-reasoning" -ForegroundColor White
Write-Host "  claude --model grok-code-fast-1" -ForegroundColor White
Write-Host "  claude --model sonar-deep-research" -ForegroundColor White
Write-Host ""

# Keep environment active
Write-Host "Environment variables are set in this session." -ForegroundColor Green
Write-Host "You can now run claude commands with any configured model.`n" -ForegroundColor Green