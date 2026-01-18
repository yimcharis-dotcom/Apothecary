// File: complete_bridge.cjs
const { spawn } = require('child_process');
const { Client } = require('@modelcontextprotocol/sdk/client/index.js');
const { StdioClientTransport } = require('@modelcontextprotocol/sdk/client/stdio.js');
const fs = require('fs');
const path = require('path');
const readline = require('readline');

// Node 24+ has built-in fetch, no need for node-fetch

// ========== CONFIG FILE ==========
function loadConfig() {
const configPath = path.join(\_\_dirname, 'config.json');
const defaults = {
vaultPath: "C:\\Vault\\Apothecary",
pythonExe: "C:\\Users\\YC\\OneDrive\\Desktop\\LocalDocs\\.venv\\Scripts\\python.exe",
pythonScript: "C:\\Users\\YC\\OneDrive\\Desktop\\LocalDocs\\rag_query_working.py",
pythonCwd: "C:\\Users\\YC\\OneDrive\\Desktop\\LocalDocs",
maxFiles: 5,
maxBytes: 200000,
defaultProvider: "grok",
temperature: 0.7
};

if (fs.existsSync(configPath)) {
try {
const userConfig = JSON.parse(fs.readFileSync(configPath, 'utf8'));
return { ...defaults, ...userConfig };
} catch (e) {
console.warn('⚠️ Config file invalid, using defaults');
}
}
return defaults;
}

const config = loadConfig();

// ========== PROVIDER CONFIG ==========
const PROVIDERS = {
grok: {
name: 'Grok (X.AI)',
url: '<https://api.x.ai/v1/chat/completions>',
key: process.env.XAI_API_KEY || config.xaiApiKey,
models: ['grok-4-1-fast-reasoning', 'grok-4-1-fast-non-reasoning','grok-4-fast-reasoning','grok-4-fast-non-reasoning','grok-4-0709','grok-code-fast-1', 'grok-3','grok-3-mini', 'grok-2-image-1212', 'grok-2-vision-1212']
},
pplx: {
name: 'Perplexity',
url: '<https://api.perplexity.ai/chat/completions>',
key: process.env.PPLX_API_KEY || config.pplxApiKey,
models: ['sonar', 'sonar-pro', 'sonar-deep-research', 'sonar-reasoning-pro']
}
};

// ========== INTERACTIVE SELECTION ==========
function createInterface() {
return readline.createInterface({
input: process.stdin,
output: process.stdout
});
}

function askQuestion(rl, prompt) {
return new Promise((resolve) => {
rl.question(prompt, resolve);
});
}

async function selectProviderAndModel() {
const rl = createInterface();

console.log('\n📋 Available Providers:');
const providerKeys = Object.keys(PROVIDERS);
providerKeys.forEach((key, i) => {
const p = PROVIDERS[key];
const hasKey = p.key ? '✅' : '❌';
console.log(`${i + 1}. ${hasKey} ${p.name}`);
});

let providerKey;
while (true) {
const answer = await askQuestion(rl, `\nSelect provider (1-${providerKeys.length}) or name [${config.defaultProvider}]:`);
const choice = answer.trim() || config.defaultProvider;

    if (providerKeys.includes(choice.toLowerCase())) {
      providerKey = choice.toLowerCase();
      break;
    }
    const num = parseInt(choice);
    if (num >= 1 && num <= providerKeys.length) {
      providerKey = providerKeys[num - 1];
      break;
    }
    console.log('❌ Invalid choice, try again');

}

const provider = PROVIDERS[providerKey];
if (!provider.key) {
rl.close();
throw new Error(`Missing API key for ${provider.name}. Set ${providerKey.toUpperCase() === 'GROK' ? 'XAI' : 'PPLX'}_API_KEY`);
}

console.log(`\n📋 Available Models for ${provider.name}:`);
provider.models.forEach((model, i) => {
console.log(`${i + 1}. ${model}`);
});

let model;
while (true) {
const answer = await askQuestion(rl, `\nSelect model (1-${provider.models.length}) or name [${provider.models[0]}]:`);
const choice = answer.trim() || provider.models[0];

    if (provider.models.includes(choice)) {
      model = choice;
      break;
    }
    const num = parseInt(choice);
    if (num >= 1 && num <= provider.models.length) {
      model = provider.models[num - 1];
      break;
    }
    console.log('❌ Invalid choice, try again');

}

rl.close();
return { provider: providerKey, model };
}

// ========== HELP TEXT ==========
function showHelp() {
console.log(`
🔍 Obsidian Vault Q&A Bridge
Usage:
node complete_bridge.cjs --vault <path> [options] "your question"

Required:
--vault <path> Path to Obsidian vault (or use config.json)

Options:
--provider <name> AI provider: grok, pplx (default: grok)
--model <name> Model name (use --list-models to see options)
--temperature <N> Creativity: 0.0-2.0 (default: 0.7)
--max-files <N> Max files to read (default: 5)
--max-bytes <N> Max characters to read (default: 200000)
--interactive, -i Interactive provider/model selection
--verbose Show detailed logs
--list-models Show available models
--list-models <provider> Show models for specific provider
--help Show this help

Examples:
node complete_bridge.cjs --vault "C:\\Vault\\Apothecary" "What are my TODOs?"
node complete_bridge.cjs --vault "C:\\Vault\\Apothecary" --provider pplx --model sonar-pro --temperature 0.9 "Explain my MCP setup"
node complete_bridge.cjs --vault "C:\\Vault\\Apothecary" --model grok-3 "What's in my vault?"
node complete_bridge.cjs --list-models
node complete_bridge.cjs --list-models pplx
node complete_bridge.cjs --interactive "your question"
`);
}

function listModels(providerName = null) {
if (providerName) {
const provider = PROVIDERS[providerName.toLowerCase()];
if (!provider) {
console.log(`❌ Unknown provider: ${providerName}`);
console.log(`Available: ${Object.keys(PROVIDERS).join(', ')}`);
return;
}
console.log(`\n📋 Models for ${provider.name}:`);
provider.models.forEach((model, i) => {
console.log(`${i + 1}. ${model}`);
});
} else {
console.log('\n📋 Available Models by Provider:');
Object.entries(PROVIDERS).forEach(([key, provider]) => {
console.log(`\n${provider.name} (${key}):`);
provider.models.forEach(model => console.log(`- ${model}`));
});
}
}

// ========== RAG QUERY ==========
async function queryRAG(question, verbose = false) {
return new Promise((resolve, reject) => {
if (verbose) console.log(`🔍 Searching: "${question.substring(0, 50)}${question.length > 50 ? '...' : ''}"`);

    const pythonProcess = spawn(config.pythonExe, [config.pythonScript, question], {
      cwd: config.pythonCwd
    });

    let stdout = '';
    let stderr = '';

    pythonProcess.stdout.on('data', data => stdout += data.toString());
    pythonProcess.stderr.on('data', data => {
      stderr += data.toString();
      if (verbose) process.stdout.write('  ' + data.toString());
    });

    pythonProcess.on('close', code => {
      if (code !== 0) {
        reject(new Error(`RAG failed: ${stderr}`));
        return;
      }

      try {
        const result = JSON.parse(stdout);
        if (verbose) console.log(`\n📄 Found ${result.total_found} relevant files`);
        resolve(result);
      } catch (e) {
        reject(new Error(`JSON error: ${e.message}`));
      }
    });

});
}

// ========== MCP CLIENT ==========
async function readFilesWithMCP(vaultPath, filePaths, maxFiles = config.maxFiles, maxBytes = config.maxBytes, verbose = false) {
if (verbose) console.log(`📖 Reading files via MCP (max ${maxFiles} files, ${maxBytes} chars)...`);

const transport = new StdioClientTransport({
command: 'npx.cmd',
args: ['-y', '@modelcontextprotocol/server-filesystem', vaultPath]
});

const client = new Client(
{ name: 'obsidian-bridge', version: '1.0.0' },
{ capabilities: { tools: {} } }
);

try {
await client.connect(transport);

    const excerpts = [];
    let totalBytes = 0;

    for (const filePath of filePaths.slice(0, maxFiles)) {
      if (totalBytes >= maxBytes) break;

      try {
        const result = await client.callTool({
          name: 'read_text_file',
          arguments: { path: filePath }
        });

        const content = result.content?.[0]?.text || '';
        if (content) {
          const remainingBytes = maxBytes - totalBytes;
          const truncated = content.length > remainingBytes
            ? content.substring(0, remainingBytes) + '\n[...truncated]'
            : content;

          excerpts.push({
            path: filePath,
            content: truncated,
            length: content.length,
            truncated: content.length > remainingBytes
          });

          totalBytes += content.length;

          if (verbose) {
            console.log(`  ✅ ${path.basename(filePath)} (${content.length} chars)`);
          }
        }
      } catch (error) {
        if (verbose) {
          console.log(`  ⚠️  Skipped ${path.basename(filePath)}: ${error.message}`);
        }
      }
    }

    return excerpts;

} finally {
await client.close();
}
}

// ========== AI ANSWER ==========
async function askAI(question, context, providerKey, model, temperature = 0.7) {
const provider = PROVIDERS[providerKey];
if (!provider || !provider.key) {
throw new Error(`Invalid provider or missing API key: ${providerKey}`);
}

const systemPrompt = `You are an AI assistant querying the user's Obsidian vault via MCP.

Rules:

- Answer ONLY from provided vault excerpts
- If info missing, say "Not found in vault"
- Be thorough but concise
- Start with direct answer (1-2 sentences)
- Use bullets for details
- Format as clean Markdown

Always end with:

## Sources

List files used with [[wikilinks]] or paths`;

const userPrompt = `QUESTION: ${question}

VAULT CONTENT:
${context}

ANSWER (based only on above content):`;

const response = await fetch(provider.url, {
method: 'POST',
headers: {
'Authorization': `Bearer ${provider.key}`,
'Content-Type': 'application/json'
},
body: JSON.stringify({
model: model,
messages: [
{ role: 'system', content: systemPrompt },
{ role: 'user', content: userPrompt }
],
temperature: temperature,
max_tokens: 1500
})
});

if (!response.ok) {
const errorText = await response.text();
throw new Error(`${provider.name} API error (${response.status}): ${errorText}`);
}

const data = await response.json();
return data.choices[0].message.content;
}

// ========== MAIN ==========
async function askVault(question, options = {}) {
const vaultPath = options.vaultPath || config.vaultPath;
const providerKey = options.provider || config.defaultProvider;
const model = options.model || PROVIDERS[providerKey]?.models[0];
const temperature = options.temperature !== undefined ? options.temperature : config.temperature;
const maxFiles = options.maxFiles || config.maxFiles;
const maxBytes = options.maxBytes || config.maxBytes;
const verbose = options.verbose || false;

if (verbose) {
console.log('='.repeat(60));
console.log('🔍 Obsidian Vault Q&A Bridge');
console.log(`📁 Vault: ${vaultPath}`);
console.log(`🤖 Provider: ${providerKey} (${model})`);
console.log(`❓ Question: ${question}`);
console.log('='.repeat(60) + '\n');
}

// 1. RAG search
const ragResults = await queryRAG(question, verbose);

if (ragResults.total_found === 0) {
return "No relevant files found in vault.";
}

if (verbose) {
console.log(`📄 RAG found ${ragResults.total_found} relevant files\n`);
}

// 2. Get unique file paths
const uniquePaths = [...new Set(ragResults.results.map(r => r.path))];

// 3. Read files via MCP
const excerpts = await readFilesWithMCP(vaultPath, uniquePaths, maxFiles, maxBytes, verbose);

if (excerpts.length === 0) {
return "Could not read any files.";
}

// 4. Build context
const context = excerpts.map(e =>
`=== ${e.path} ===\n${e.content}\n`
).join('\n');

// 5. Ask AI
if (verbose) console.log('\n💭 Processing with AI...\n');
const answer = await askAI(question, context, providerKey, model, temperature);

return {
answer: answer,
sources: excerpts.map(e => ({
path: e.path,
length: e.length,
truncated: e.truncated
}))
};
}

// ========== CLI ==========
async function main() {
const args = process.argv.slice(2);

// Handle help
if (args.includes('--help') || args.includes('-h')) {
showHelp();
return;
}

// Handle list-models
if (args.includes('--list-models')) {
const idx = args.indexOf('--list-models');
const provider = args[idx + 1] && !args[idx + 1].startsWith('--') ? args[idx + 1] : null;
listModels(provider);
return;
}

// Parse arguments
const interactive = args.includes('--interactive') || args.includes('-i');
const verbose = args.includes('--verbose');

let question = '';
let vaultPath = config.vaultPath;
let provider = config.defaultProvider;
let model = null;
let temperature = config.temperature;
let maxFiles = config.maxFiles;
let maxBytes = config.maxBytes;

for (let i = 0; i < args.length; i++) {
const arg = args[i];
if (arg === '--vault' && args[i + 1]) {
vaultPath = args[++i];
} else if (arg === '--provider' && args[i + 1]) {
provider = args[++i].toLowerCase();
} else if (arg === '--model' && args[i + 1]) {
model = args[++i];
} else if (arg === '--temperature' && args[i + 1]) {
temperature = parseFloat(args[++i]);
} else if (arg === '--max-files' && args[i + 1]) {
maxFiles = parseInt(args[++i]);
} else if (arg === '--max-bytes' && args[i + 1]) {
maxBytes = parseInt(args[++i]);
} else if (!arg.startsWith('--') && arg !== '-i') {
question += arg + ' ';
}
}

question = question.trim();

// Interactive mode
if (interactive) {
try {
const selection = await selectProviderAndModel();
provider = selection.provider;
model = selection.model;
} catch (error) {
console.error('❌', error.message);
process.exit(1);
}
}

if (!question) {
const rl = createInterface();
question = await askQuestion(rl, '❓ Enter your question: ');
rl.close();
if (!question.trim()) {
console.log('❌ No question provided');
showHelp();
return;
}
}

try {
const result = await askVault(question, {
vaultPath,
provider,
model,
temperature,
maxFiles,
maxBytes,
verbose
});

    console.log('\n' + '='.repeat(60));
    console.log('💡 ANSWER:');
    console.log('='.repeat(60));
    console.log(result.answer);
    console.log('='.repeat(60));

    console.log('\n📚 Sources used:');
    result.sources.forEach((source, i) => {
      const trunc = source.truncated ? ' (truncated)' : '';
      console.log(`${i + 1}. ${source.path} (${source.length} chars${trunc})`);
    });

} catch (error) {
console.error('\n❌ Error:', error.message);
console.log('\n💡 Tips:');
console.log(' - For Grok: $env:XAI_API_KEY="your-key"');
console.log(' - For Perplexity: $env:PPLX_API_KEY="your-key"');
console.log(' - Use --help for usage information');
}
}

if (require.main === module) {
main();
}

module.exports = { askVault, loadConfig };
