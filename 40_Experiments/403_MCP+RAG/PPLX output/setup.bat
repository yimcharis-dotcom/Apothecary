@echo off
echo ========================================
echo AI Bridge Setup for Windows
echo ========================================
echo.

REM Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Node.js not found! Please install from https://nodejs.org/
    pause
    exit /b 1
)

echo ✅ Node.js found: 
node --version
echo.

REM Check if Ollama is running
echo Checking Ollama status...
curl -s http://localhost:11434/api/tags >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo ✅ Ollama is running
) else (
    echo ⚠️  Ollama not detected. Install from https://ollama.com
)
echo.

REM Create default config
echo Creating default configuration...
node complete_bridge.cjs --config >nul 2>nul
echo ✅ Config created
echo.

REM Test the bridge
echo Testing bridge...
node complete_bridge.cjs --list
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Set API keys (optional for cloud providers):
echo    setx XAI_API_KEY "your-grok-key"
echo    setx ANTHROPIC_API_KEY "your-claude-key"
echo.
echo 2. Test a query:
echo    node complete_bridge.cjs "What is recursion?"
echo.
echo 3. Force a specific provider:
echo    node complete_bridge.cjs --provider ollama --model gpt-oss:20b "Explain async/await"
echo.
pause
