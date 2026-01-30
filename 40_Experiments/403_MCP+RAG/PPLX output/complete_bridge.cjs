// complete_bridge.cjs - Multi-provider AI Bridge with Smart Routing
const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

// Provider Configuration
const PROVIDERS = {
  ollama: {
    name: 'Ollama (Local)',
    baseUrl: 'http://localhost:11434/v1/chat/completions',
    apiKey: 'ollama',
    models: ['gpt-oss:20b', 'codellama:7b', 'codeqwen:1.5b', 'qwen3-coder:7b', 'phi3.5:mini'],
    available: true
  },
  lmstudio: {
    name: 'LM Studio (Local)',
    baseUrl: 'http://localhost:1234/v1/chat/completions',
    apiKey: 'lm-studio',
    models: ['local-model'],
    available: false
  },
  grok: {
    name: 'Grok (xAI)',
    baseUrl: 'https://api.x.ai/v1/chat/completions',
    apiKey: process.env.XAI_API_KEY || '',
    models: ['grok-beta', 'grok-vision-beta'],
    available: !!process.env.XAI_API_KEY
  },
  perplexity: {
    name: 'Perplexity',
    baseUrl: 'https://api.perplexity.ai/v2/chat/completions',
    apiKey: process.env.PPLX_API_KEY || '',
    models: ['llama-3.1-sonar-small-128k-online', 'llama-3.1-sonar-large-128k-online'],
    available: !!process.env.PPLX_API_KEY
  },
  anthropic: {
    name: 'Anthropic Claude',
    baseUrl: 'https://api.anthropic.com/v1/messages',
    apiKey: process.env.ANTHROPIC_API_KEY || '',
    models: ['claude-sonnet-4-20250514', 'claude-3-5-sonnet-20241022'],
    available: !!process.env.ANTHROPIC_API_KEY
  }
};

// Configuration
class BridgeConfig {
  constructor() {
    this.configPath = path.join(__dirname, 'bridge_config.json');
    this.config = this.loadConfig();
  }

  loadConfig() {
    try {
      if (fs.existsSync(this.configPath)) {
        return JSON.parse(fs.readFileSync(this.configPath, 'utf8'));
      }
    } catch (error) {
      console.log('Creating default config...');
    }

    return {
      vaultPath: process.env.OBSIDIAN_VAULT || '',
      defaultProvider: 'smart',
      modelPreferences: {
        simple_queries: { provider: 'ollama', model: 'codeqwen:1.5b' },
        code_analysis: { provider: 'ollama', model: 'codellama:7b' },
        complex_reasoning: { provider: 'grok', model: 'grok-beta' },
        large_context: { provider: 'anthropic', model: 'claude-sonnet-4-20250514' }
      },
      smartRouting: {
        enabled: true,
        simpleQueryMaxLength: 100,
        largeContextThreshold: 200000,
        preferLocal: true
      }
    };
  }

  saveConfig() {
    fs.writeFileSync(this.configPath, JSON.stringify(this.config, null, 2));
  }
}

// Smart Model Router
class ModelRouter {
  constructor(config) {
    this.config = config;
  }

  analyzeQuery(question, contextSize = 0) {
    const questionLength = question.length;
    const isCodeQuery = /code|function|class|method|bug|error|debug|implement/i.test(question);
    const isSimple = questionLength < this.config.smartRouting.simpleQueryMaxLength;
    const isLargeContext = contextSize > this.config.smartRouting.largeContextThreshold;

    return { questionLength, isCodeQuery, isSimple, isLargeContext };
  }

  selectOptimalModel(question, contextSize = 0) {
    const analysis = this.analyzeQuery(question, contextSize);

    // Priority 1: Large context needs cloud models
    if (analysis.isLargeContext) {
      if (PROVIDERS.anthropic.available) {
        return { provider: 'anthropic', model: 'claude-sonnet-4-20250514' };
      }
      if (PROVIDERS.grok.available) {
        return { provider: 'grok', model: 'grok-beta' };
      }
    }

    // Priority 2: Local models for privacy and speed (if enabled)
    if (this.config.smartRouting.preferLocal && PROVIDERS.ollama.available) {
      if (analysis.isSimple && contextSize < 50000) {
        return { provider: 'ollama', model: 'codeqwen:1.5b' };
      }

      if (analysis.isCodeQuery) {
        return { provider: 'ollama', model: 'codellama:7b' };
      }

      // Default local model
      return { provider: 'ollama', model: 'gpt-oss:20b' };
    }

    // Priority 3: Cloud fallback
    if (PROVIDERS.grok.available) {
      return { provider: 'grok', model: 'grok-beta' };
    }

    if (PROVIDERS.perplexity.available) {
      return { provider: 'perplexity', model: 'llama-3.1-sonar-small-128k-online' };
    }

    // Final fallback: local if available
    if (PROVIDERS.ollama.available) {
      return { provider: 'ollama', model: 'gpt-oss:20b' };
    }

    throw new Error('No available providers configured');
  }
}

// API Client
class APIClient {
  constructor(provider, model) {
    this.provider = PROVIDERS[provider];
    this.model = model;
  }

  async makeRequest(messages) {
    const url = new URL(this.provider.baseUrl);
    const isHttps = url.protocol === 'https:';
    const httpModule = isHttps ? https : http;

    const requestBody = JSON.stringify({
      model: this.model,
      messages: messages,
      temperature: 0.7,
      max_tokens: 4096
    });

    return new Promise((resolve, reject) => {
      const options = {
        hostname: url.hostname,
        port: url.port || (isHttps ? 443 : 80),
        path: url.pathname,
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(requestBody),
          'Authorization': `Bearer ${this.provider.apiKey}`
        }
      };

      const req = httpModule.request(options, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          try {
            const response = JSON.parse(data);
            resolve(response);
          } catch (error) {
            reject(new Error(`Failed to parse response: ${error.message}`));
          }
        });
      });

      req.on('error', reject);
      req.write(requestBody);
      req.end();
    });
  }
}

// Main Bridge
class AIBridge {
  constructor() {
    this.config = new BridgeConfig();
    this.router = new ModelRouter(this.config.config);
  }

  async query(question, options = {}) {
    const { provider, model, context } = options;
    const contextSize = context ? context.length : 0;

    // Manual selection or smart routing
    let selectedProvider, selectedModel;
    if (provider && model) {
      selectedProvider = provider;
      selectedModel = model;
    } else if (this.config.config.defaultProvider === 'smart') {
      const selection = this.router.selectOptimalModel(question, contextSize);
      selectedProvider = selection.provider;
      selectedModel = selection.model;
    } else {
      selectedProvider = this.config.config.defaultProvider;
      selectedModel = PROVIDERS[selectedProvider].models[0];
    }

    console.log(`\n🤖 Using: ${PROVIDERS[selectedProvider].name} - ${selectedModel}`);
    console.log(`📊 Context size: ${contextSize} chars\n`);

    // Build messages
    const messages = [];
    if (context) {
      messages.push({
        role: 'system',
        content: `Context from vault:\n${context}`
      });
    }
    messages.push({
      role: 'user',
      content: question
    });

    // Make request
    const client = new APIClient(selectedProvider, selectedModel);
    try {
      const response = await client.makeRequest(messages);
      return {
        answer: response.choices[0].message.content,
        provider: selectedProvider,
        model: selectedModel,
        usage: response.usage
      };
    } catch (error) {
      console.error(`❌ Error with ${selectedProvider}:`, error.message);

      // Fallback logic
      if (selectedProvider !== 'ollama' && PROVIDERS.ollama.available) {
        console.log('⚠️  Falling back to Ollama...');
        return this.query(question, { provider: 'ollama', model: 'gpt-oss:20b', context });
      }

      throw error;
    }
  }

  listProviders() {
    console.log('\n📡 Available Providers:\n');
    Object.entries(PROVIDERS).forEach(([key, provider]) => {
      const status = provider.available ? '✅' : '❌';
      console.log(`${status} ${provider.name}`);
      if (provider.available) {
        console.log(`   Models: ${provider.models.join(', ')}`);
      }
    });
  }
}

// CLI Interface
async function main() {
  const args = process.argv.slice(2);
  const bridge = new AIBridge();

  if (args[0] === '--list' || args[0] === '-l') {
    bridge.listProviders();
    return;
  }

  if (args[0] === '--config' || args[0] === '-c') {
    console.log('Current configuration:');
    console.log(JSON.stringify(bridge.config.config, null, 2));
    return;
  }

  if (args.length === 0) {
    console.log(`
AI Bridge - Multi-provider Query System

Usage:
  node complete_bridge.cjs <question>
  node complete_bridge.cjs --list          List available providers
  node complete_bridge.cjs --config        Show current configuration
  node complete_bridge.cjs --provider ollama --model gpt-oss:20b "your question"

Environment variables:
  XAI_API_KEY          - For Grok access
  PPLX_API_KEY         - For Perplexity access
  ANTHROPIC_API_KEY    - For Claude access
  OBSIDIAN_VAULT       - Path to your Obsidian vault
    `);
    return;
  }

  // Parse arguments
  let question = args.join(' ');
  let options = {};

  if (args.includes('--provider')) {
    const providerIndex = args.indexOf('--provider');
    options.provider = args[providerIndex + 1];
    args.splice(providerIndex, 2);
  }

  if (args.includes('--model')) {
    const modelIndex = args.indexOf('--model');
    options.model = args[modelIndex + 1];
    args.splice(modelIndex, 2);
  }

  question = args.join(' ');

  // Execute query
  try {
    const result = await bridge.query(question, options);
    console.log('\n💬 Answer:\n');
    console.log(result.answer);
    console.log('\n📈 Usage:', result.usage);
  } catch (error) {
    console.error('\n❌ Error:', error.message);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { AIBridge, PROVIDERS };
