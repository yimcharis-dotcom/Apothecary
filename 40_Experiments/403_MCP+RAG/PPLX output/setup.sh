#!/bin/bash

echo "========================================"
echo "AI Bridge Setup for Linux/Mac"
echo "========================================"
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found! Please install from https://nodejs.org/"
    exit 1
fi

echo "✅ Node.js found:" 
node --version
echo ""

# Check if Ollama is running
echo "Checking Ollama status..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✅ Ollama is running"
else
    echo "⚠️  Ollama not detected. Install from https://ollama.com"
fi
echo ""

# Create default config
echo "Creating default configuration..."
node complete_bridge.cjs --config > /dev/null 2>&1
echo "✅ Config created"
echo ""

# Test the bridge
echo "Testing bridge..."
node complete_bridge.cjs --list
echo ""

echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Set API keys (optional for cloud providers):"
echo "   export XAI_API_KEY='your-grok-key'"
echo "   export ANTHROPIC_API_KEY='your-claude-key'"
echo ""
echo "2. Test a query:"
echo "   node complete_bridge.cjs 'What is recursion?'"
echo ""
echo "3. Force a specific provider:"
echo "   node complete_bridge.cjs --provider ollama --model gpt-oss:20b 'Explain async/await'"
echo ""
