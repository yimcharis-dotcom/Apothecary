# LiteLLM Proxy Startup Script
# Load environment variables and start the proxy

# Load API keys and Claude Code settings
. C:\Users\YC\LiteLLM\litellm-config\set-env.ps1

Write-Host "`n=====================================" -ForegroundColor Cyan
Write-Host "🚀 Starting LiteLLM Proxy" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📍 Config: C:\Users\YC\LiteLLM\litellm-config\config.yaml" -ForegroundColor Yellow
Write-Host "🌐 Proxy URL: http://127.0.0.1:4000" -ForegroundColor Yellow
Write-Host ""
Write-Host "Available models:" -ForegroundColor Cyan
Write-Host "  🧠 Grok: grok-code-fast-1, grok-4-1-fast-reasoning, ..." -ForegroundColor Gray
Write-Host "  🔍 Perplexity: perplexity-sonar-pro, ..." -ForegroundColor Gray
Write-Host ""
Write-Host "Press Ctrl+C to stop the proxy" -ForegroundColor Yellow
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Start the proxy
litellm --config C:\Users\YC\LiteLLM\litellm-config\config.yaml
