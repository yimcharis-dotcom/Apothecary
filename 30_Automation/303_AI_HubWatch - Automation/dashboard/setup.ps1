# Quick Start Script for AI Dashboard Setup
# Run this from the dashboard folder

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "AI Ecosystem Dashboard - Quick Start" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check Python installation
Write-Host "[1/5] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Python not found!" -ForegroundColor Red
    Write-Host "  Please install Python 3.8+ from https://www.python.org/downloads/" -ForegroundColor Red
    exit 1
}

# Check if we're in the right directory
Write-Host "`n[2/5] Checking directory structure..." -ForegroundColor Yellow
$currentDir = Get-Location
if (-not (Test-Path "requirements.txt")) {
    Write-Host "  ✗ requirements.txt not found!" -ForegroundColor Red
    Write-Host "  Make sure you're running this from the dashboard folder" -ForegroundColor Red
    exit 1
}
Write-Host "  ✓ In correct directory: $currentDir" -ForegroundColor Green

# Create necessary directories
Write-Host "`n[3/5] Creating directory structure..." -ForegroundColor Yellow
$dirs = @("collectors", "data")
foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "  ✓ Created: $dir\" -ForegroundColor Green
    } else {
        Write-Host "  ✓ Exists: $dir\" -ForegroundColor DarkGray
    }
}

# Install Python dependencies
Write-Host "`n[4/5] Installing Python dependencies..." -ForegroundColor Yellow
Write-Host "  This may take a few minutes..." -ForegroundColor DarkGray
try {
    pip install -r requirements.txt --quiet
    Write-Host "  ✓ All dependencies installed" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Failed to install dependencies" -ForegroundColor Red
    Write-Host "  Try running: pip install -r requirements.txt" -ForegroundColor Red
}

# Check for Google credentials
Write-Host "`n[5/5] Checking Google Cloud credentials..." -ForegroundColor Yellow
$credPath = "collectors\credentials.json"
if (Test-Path $credPath) {
    Write-Host "  ✓ credentials.json found" -ForegroundColor Green
} else {
    Write-Host "  ✗ credentials.json NOT found" -ForegroundColor Yellow
    Write-Host "`n  You need to set up Google Cloud OAuth credentials." -ForegroundColor Yellow
    Write-Host "  See: SETUP_GMAIL_SCANNER.md for detailed instructions" -ForegroundColor Yellow
    Write-Host "`n  Quick steps:" -ForegroundColor Cyan
    Write-Host "  1. Go to: https://console.cloud.google.com/" -ForegroundColor White
    Write-Host "  2. Create a new project" -ForegroundColor White
    Write-Host "  3. Enable Gmail API and People API" -ForegroundColor White
    Write-Host "  4. Create OAuth Desktop credentials" -ForegroundColor White
    Write-Host "  5. Download and save as: $credPath`n" -ForegroundColor White
}

# Summary
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Setup Summary" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "✓ Python installed" -ForegroundColor Green
Write-Host "✓ Directory structure created" -ForegroundColor Green
Write-Host "✓ Dependencies installed" -ForegroundColor Green

if (Test-Path $credPath) {
    Write-Host "✓ Google credentials configured" -ForegroundColor Green
    Write-Host "`n[READY] You can now run:" -ForegroundColor Green
    Write-Host "  python collectors\scan_gmail_oauth.py`n" -ForegroundColor White
} else {
    Write-Host "⚠ Google credentials needed" -ForegroundColor Yellow
    Write-Host "`n[NEXT STEP] Set up Google Cloud credentials:" -ForegroundColor Yellow
    Write-Host "  1. Read: SETUP_GMAIL_SCANNER.md" -ForegroundColor White
    Write-Host "  2. Get credentials.json from Google Cloud Console" -ForegroundColor White
    Write-Host "  3. Place it in: collectors\credentials.json" -ForegroundColor White
    Write-Host "  4. Run: python collectors\scan_gmail_oauth.py`n" -ForegroundColor White
}

Write-Host "========================================`n" -ForegroundColor Cyan
