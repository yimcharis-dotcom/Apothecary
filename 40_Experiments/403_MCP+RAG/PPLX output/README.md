# AI Bridge - Multi-Provider Query System

A smart routing system that automatically selects the best AI provider (local or cloud) based on your query.

## Features

✅ **Smart Model Routing** - Automatically picks the right model for your query
✅ **Local-First** - Uses Ollama for privacy and speed when possible
✅ **Cloud Fallback** - Seamlessly switches to Grok/Claude for complex tasks
✅ **Multiple Providers** - Ollama, LM Studio, Grok, Perplexity, Claude
✅ **Cost Optimization** - Saves API costs by using local models for simple queries

## Installation

### Windows
```bash
# Run setup
setup.bat

# Or manually install Node.js from https://nodejs.org/
# Then install Ollama from https://ollama.com
```

### Linux/Mac
```bash
# Make setup executable
chmod +x setup.sh

# Run setup
./setup.sh
```

## Quick Start

### 1. Test Available Providers
```bash
node complete_bridge.cjs --list
```

### 2. Ask a Question (Smart Routing)
```bash
node complete_bridge.cjs "Explain async/await in JavaScript"
```

### 3. Force a Specific Provider
```bash
node complete_bridge.cjs --provider ollama --model codellama:7b "Write a binary search function"
```

## Configuration

Edit `bridge_config.json` to customize:

```json
{
  "defaultProvider": "smart",
  "smartRouting": {
    "enabled": true,
    "preferLocal": true
  },
  "modelPreferences": {
    "code_analysis": {"provider": "ollama", "model": "codellama:7b"}
  }
}
```

## Smart Routing Logic

The bridge automatically selects models based on:

| Query Type | Model Used | Reason |
|------------|------------|--------|
| Simple questions (<100 chars) | `codeqwen:1.5b` | Fast, local |
| Code-related | `codellama:7b` | Specialized |
| Large context (>200K chars) | `claude-sonnet-4` | Best context window |
| Complex reasoning | `grok-beta` | Advanced reasoning |

## Environment Variables

```bash
# Optional - for cloud providers
export XAI_API_KEY="your-grok-key"
export ANTHROPIC_API_KEY="your-claude-key"
export PPLX_API_KEY="your-perplexity-key"

# Optional - Obsidian vault path
export OBSIDIAN_VAULT="/path/to/your/vault"
```

## Examples

### Simple Query (Uses Local Ollama)
```bash
node complete_bridge.cjs "What is a promise?"
# 🤖 Using: Ollama (Local) - codeqwen:1.5b
```

### Code Analysis (Uses CodeLlama)
```bash
node complete_bridge.cjs "Debug this function: const x = () => { return undefined }"
# 🤖 Using: Ollama (Local) - codellama:7b
```

### Complex Task (Uses Cloud if Available)
```bash
node complete_bridge.cjs "Explain the CAP theorem with real-world database examples"
# 🤖 Using: Grok (xAI) - grok-beta
```

## Troubleshooting

### "No available providers"
- Install Ollama: https://ollama.com
- Pull a model: `ollama pull gpt-oss:20b`

### "Connection refused"
- Check Ollama is running: `ollama serve`
- For LM Studio: Start the local server on port 1234

### API Key Issues
- Set environment variables before running
- Verify keys are correct in your shell

## Integration with Claude Code

To use with Claude Code pointing to this bridge:

```bash
export ANTHROPIC_AUTH_TOKEN=your-api-key-here
export ANTHROPIC_BASE_URL=http://localhost:11434
claude --model gpt-oss:20b
```

## License

MIT - Feel free to modify and distribute
