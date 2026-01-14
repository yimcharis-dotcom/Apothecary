This system will allow AI providers (Perplexity, Grok, ChatGPT) to:

- 📖 Read files from your Obsidian vault
- 🔍 Search through your notes
- ✏️ Edit existing files
- 📁 Create new files
- 🗂️ Move/organize files

## 📁 Project Structure

First, let's create the complete project structure:

```
C:\Users\YC\MCPs\obsidian-bridge\
├── package.json
├── bridge-cli.js           # Main CLI interface
├── lib/
│   ├── mcp-client.js      # MCP server communication
│   ├── providers.js       # AI provider adapters
│   ├── file-manager.js    # File operations wrapper
│   └── safety.js          # Safety checks
├── config/
│   └── config.json        # Configuration file
├── logs/
└── README.md
```

## 📦 Step 1: Initialize Project

```bash
# Create project directory
mkdir C:\Users\YC\MCPs\obsidian-bridge
cd C:\Users\YC\MCPs\obsidian-bridge

# Initialize npm project
npm init -y

# Install dependencies
npm install commander chalk inquirer dotenv ora
npm install @modelcontextprotocol/sdk
npm install openai axios
```

## 📄 Step 2: Package.json

```json
{
  "name": "obsidian-mcp-bridge",
  "version": "1.0.0",
  "description": "MCP Bridge for Obsidian vault interaction with AI providers",
  "main": "bridge-cli.js",
  "type": "module",
  "bin": {
    "obs-bridge": "./bridge-cli.js"
  },
  "scripts": {
    "start": "node bridge-cli.js",
    "test": "node bridge-cli.js test"
  },
  "dependencies": {
    "commander": "^11.1.0",
    "chalk": "^5.3.0",
    "inquirer": "^9.2.12",
    "dotenv": "^16.3.1",
    "ora": "^7.0.1",
    "@modelcontextprotocol/sdk": "^0.5.0",
    "openai": "^4.24.0",
    "axios": "^1.6.5"
  },
  "engines": {
    "node": ">=18.0.0"
  }
}
```

## 🔧 Step 3: Configuration File

Create `config/config.json`:

```json
{
  "vault": {
    "path": "C:\\Vault\\AI hub\\Apothecary",
    "backupPath": "C:\\Vault\\AI hub\\Backup",
    "trashPath": "_Trash"
  },
  "mcp": {
    "serverPath": "npx",
    "serverArgs": ["@modelcontextprotocol/server-filesystem"],
    "timeout": 30000
  },
  "providers": {
    "grok": {
      "apiUrl": "https://api.groq.com/v1/chat/completions",
      "model": "grok-3",
      "maxTokens": 2000
    },
    "perplexity": {
      "apiUrl": "https://api.perplexity.ai/chat/completions",
      "model": "llama-3.1-sonar-small-128k-online",
      "maxTokens": 2000
    },
    "openai": {
      "apiUrl": "https://api.openai.com/v1/chat/completions",
      "model": "gpt-4-turbo-preview",
      "maxTokens": 2000
    }
  },
  "safety": {
    "allowedExtensions": [".md", ".txt", ".json", ".yml", ".yaml"],
    "maxFileSize": 1048576,
    "protectedFolders": [".obsidian", "node_modules", ".git"],
    "confirmDestructive": true
  }
}
```

## 🔐 Step 4: Environment Variables

Create `.env`:

```bash
# API Keys
GROK_API_KEY=your_grok_api_key_here
PERPLEXITY_API_KEY=your_perplexity_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Vault Path (override config if needed)
VAULT_PATH=C:\Vault\AI hub\Apothecary

# Python for indexing (future use)
PYTHON_PATH=C:\Users\YC\LocalDocs\.venv\Scripts\python.exe
PYTHONIOENCODING=utf-8
```

## 💻 Step 5: MCP Client Module

Create `lib/mcp-client.js`:

```javascript
import { spawn } from "child_process";
import { EventEmitter } from "events";
import path from "path";
import fs from "fs/promises";

export class MCPClient extends EventEmitter {
  constructor(config) {
    super();
    this.config = config;
    this.server = null;
    this.buffer = "";
  }

  async start(vaultPath) {
    return new Promise((resolve, reject) => {
      const serverPath = this.config.serverPath;
      const serverArgs = [...this.config.serverArgs, vaultPath];

      console.log(`Starting MCP server for: ${vaultPath}`);

      this.server = spawn(serverPath, serverArgs, {
        shell: true,
        stdio: ["pipe", "pipe", "pipe"],
        env: { ...process.env, PYTHONIOENCODING: "utf-8" },
      });

      this.server.stdout.on("data", (data) => {
        this.buffer += data.toString();
        this.processBuffer();
      });

      this.server.stderr.on("data", (data) => {
        const message = data.toString();
        if (message.includes("running on stdio")) {
          console.log("✅ MCP server started successfully");
          resolve(true);
        }
      });

      this.server.on("error", (error) => {
        reject(new Error(`Failed to start MCP server: ${error.message}`));
      });

      setTimeout(() => {
        reject(new Error("MCP server startup timeout"));
      }, this.config.timeout);
    });
  }

  processBuffer() {
    const lines = this.buffer.split("\n");
    this.buffer = lines.pop() || "";

    for (const line of lines) {
      if (line.trim()) {
        try {
          const message = JSON.parse(line);
          this.emit("message", message);
        } catch (e) {
          // Not JSON, might be plain text output
          this.emit("output", line);
        }
      }
    }
  }

  async sendRequest(method, params = {}) {
    return new Promise((resolve, reject) => {
      const request = {
        jsonrpc: "2.0",
        id: Date.now(),
        method,
        params,
      };

      const responseHandler = (message) => {
        if (message.id === request.id) {
          this.removeListener("message", responseHandler);
          if (message.error) {
            reject(new Error(message.error.message));
          } else {
            resolve(message.result);
          }
        }
      };

      const outputHandler = (output) => {
        // Handle plain text responses (like list_directory)
        if (method === "tools/list_directory") {
          this.removeListener("output", outputHandler);
          resolve(this.parseDirectoryListing(output));
        }
      };

      this.on("message", responseHandler);
      this.on("output", outputHandler);

      this.server.stdin.write(JSON.stringify(request) + "\n");

      setTimeout(() => {
        this.removeListener("message", responseHandler);
        this.removeListener("output", outputHandler);
        reject(new Error(`Request timeout for ${method}`));
      }, 10000);
    });
  }

  parseDirectoryListing(output) {
    const files = [];
    const dirs = [];

    const lines = output.split("\n");
    for (const line of lines) {
      if (line.startsWith("[FILE]")) {
        files.push(line.substring(6).trim());
      } else if (line.startsWith("[DIR]")) {
        dirs.push(line.substring(5).trim());
      }
    }

    return { files, dirs };
  }

  async listDirectory(dirPath) {
    try {
      const response = await this.sendRequest("tools/list_directory", {
        path: dirPath,
      });
      return response;
    } catch (error) {
      // Fallback to parsing plain text output
      return this.parseDirectoryListing(error.message || "");
    }
  }

  async readFile(filePath) {
    return this.sendRequest("tools/read_file", {
      path: filePath,
    });
  }

  async writeFile(filePath, content) {
    return this.sendRequest("tools/write_file", {
      path: filePath,
      content,
    });
  }

  async editFile(filePath, oldContent, newContent) {
    return this.sendRequest("tools/edit_file", {
      path: filePath,
      old_str: oldContent,
      new_str: newContent,
    });
  }

  async moveFile(sourcePath, destPath) {
    return this.sendRequest("tools/move_file", {
      source: sourcePath,
      destination: destPath,
    });
  }

  async searchFiles(pattern, dirPath = null) {
    return this.sendRequest("tools/search_files", {
      pattern,
      path: dirPath || this.config.vaultPath,
    });
  }

  async createDirectory(dirPath) {
    return this.sendRequest("tools/create_directory", {
      path: dirPath,
    });
  }

  async getFileInfo(filePath) {
    return this.sendRequest("tools/get_file_info", {
      path: filePath,
    });
  }

  stop() {
    if (this.server) {
      this.server.kill();
      this.server = null;
    }
  }
}
```

## 🤖 Step 6: AI Provider Adapters

Create `lib/providers.js`:

```javascript
import axios from "axios";
import { OpenAI } from "openai";

export class ProviderAdapter {
  constructor(config) {
    this.config = config;
  }

  async query(prompt, context = "", provider = "grok") {
    const providerConfig = this.config.providers[provider];
    if (!providerConfig) {
      throw new Error(`Unknown provider: ${provider}`);
    }

    switch (provider) {
      case "grok":
        return this.queryGrok(prompt, context, providerConfig);
      case "perplexity":
        return this.queryPerplexity(prompt, context, providerConfig);
      case "openai":
        return this.queryOpenAI(prompt, context, providerConfig);
      default:
        throw new Error(`Provider ${provider} not implemented`);
    }
  }

  async queryGrok(prompt, context, config) {
    const apiKey = process.env.GROK_API_KEY;
    if (!apiKey) throw new Error("GROK_API_KEY not set");

    const systemPrompt = `You are an assistant helping with an Obsidian vault. 
    You have access to the following context from the vault:\n\n${context}`;

    try {
      const response = await axios.post(
        config.apiUrl,
        {
          model: config.model,
          messages: [
            { role: "system", content: systemPrompt },
            { role: "user", content: prompt },
          ],
          max_tokens: config.maxTokens,
          temperature: 0.7,
        },
        {
          headers: {
            Authorization: `Bearer ${apiKey}`,
            "Content-Type": "application/json",
          },
        }
      );

      return response.data.choices[0].message.content;
    } catch (error) {
      throw new Error(`Grok API error: ${error.message}`);
    }
  }

  async queryPerplexity(prompt, context, config) {
    const apiKey = process.env.PERPLEXITY_API_KEY;
    if (!apiKey) throw new Error("PERPLEXITY_API_KEY not set");

    const systemPrompt = `You are analyzing content from an Obsidian vault. 
    Use the following context to provide accurate answers:\n\n${context}`;

    try {
      const response = await axios.post(
        config.apiUrl,
        {
          model: config.model,
          messages: [
            { role: "system", content: systemPrompt },
            { role: "user", content: prompt },
          ],
          max_tokens: config.maxTokens,
        },
        {
          headers: {
            Authorization: `Bearer ${apiKey}`,
            "Content-Type": "application/json",
          },
        }
      );

      return response.data.choices[0].message.content;
    } catch (error) {
      throw new Error(`Perplexity API error: ${error.message}`);
    }
  }

  async queryOpenAI(prompt, context, config) {
    const apiKey = process.env.OPENAI_API_KEY;
    if (!apiKey) throw new Error("OPENAI_API_KEY not set");

    const openai = new OpenAI({ apiKey });

    try {
      const response = await openai.chat.completions.create({
        model: config.model,
        messages: [
          {
            role: "system",
            content: `You are managing an Obsidian vault. Context:\n\n${context}`,
          },
          {
            role: "user",
            content: prompt,
          },
        ],
        max_tokens: config.maxTokens,
      });

      return response.choices[0].message.content;
    } catch (error) {
      throw new Error(`OpenAI API error: ${error.message}`);
    }
  }
}
```

## 🛡️ Step 7: Safety Module

Create `lib/safety.js`:

```javascript
import path from "path";
import fs from "fs/promises";

export class SafetyManager {
  constructor(config) {
    this.config = config.safety;
  }

  async validatePath(filePath, vaultPath) {
    const normalizedPath = path.normalize(filePath);
    const normalizedVault = path.normalize(vaultPath);

    if (!normalizedPath.startsWith(normalizedVault)) {
      throw new Error("Path is outside vault");
    }

    // Check for protected folders
    for (const protected of this.config.protectedFolders) {
      if (normalizedPath.includes(path.sep + protected + path.sep)) {
        throw new Error(`Cannot modify protected folder: ${protected}`);
      }
    }

    return true;
  }

  validateExtension(filePath) {
    const ext = path.extname(filePath).toLowerCase();
    if (!this.config.allowedExtensions.includes(ext)) {
      throw new Error(`File type ${ext} not allowed`);
    }
    return true;
  }

  async validateFileSize(filePath) {
    try {
      const stats = await fs.stat(filePath);
      if (stats.size > this.config.maxFileSize) {
        throw new Error(`File too large: ${stats.size} bytes`);
      }
      return true;
    } catch (error) {
      // File doesn't exist yet (for new files)
      return true;
    }
  }

  async createBackup(filePath) {
    try {
      const content = await fs.readFile(filePath, "utf-8");
      const backupPath = filePath + ".backup." + Date.now();
      await fs.writeFile(backupPath, content);
      return backupPath;
    } catch (error) {
      // File doesn't exist yet
      return null;
    }
  }

  async softDelete(filePath, trashPath) {
    const fileName = path.basename(filePath);
    const timestamp = new Date().toISOString().replace(/:/g, "-");
    const trashFile = path.join(trashPath, `${timestamp}_${fileName}`);

    await fs.rename(filePath, trashFile);
    return trashFile;
  }
}
```

## 🎮 Step 8: Main CLI Application

Create `bridge-cli.js`:

```javascript
#!/usr/bin/env node

import { Command } from "commander";
import chalk from "chalk";
import inquirer from "inquirer";
import ora from "ora";
import dotenv from "dotenv";
import path from "path";
import fs from "fs/promises";
import { fileURLToPath } from "url";
import { MCPClient } from "./lib/mcp-client.js";
import { ProviderAdapter } from "./lib/providers.js";
import { SafetyManager } from "./lib/safety.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load environment variables
dotenv.config();

// Load configuration
const configPath = path.join(__dirname, "config", "config.json");
const config = JSON.parse(await fs.readFile(configPath, "utf-8"));

// Override vault path from env if available
if (process.env.VAULT_PATH) {
  config.vault.path = process.env.VAULT_PATH;
}

class ObsidianBridge {
  constructor() {
    this.mcpClient = new MCPClient(config.mcp);
    this.provider = new ProviderAdapter(config);
    this.safety = new SafetyManager(config);
    this.vaultPath = config.vault.path;
  }

  async initialize() {
    const spinner = ora("Initializing MCP server...").start();
    try {
      await this.mcpClient.start(this.vaultPath);
      spinner.succeed("MCP server initialized");
      return true;
    } catch (error) {
      spinner.fail(`Failed to initialize: ${error.message}`);
      return false;
    }
  }

  async search(query) {
    console.log(chalk.blue(`\n🔍 Searching for: ${query}\n`));

    try {
      // Search for files matching the query
      const results = await this.mcpClient.searchFiles(query);

      if (!results || results.length === 0) {
        console.log(chalk.yellow("No files found matching your query"));
        return [];
      }

      console.log(chalk.green(`Found ${results.length} matching files:\n`));
      results.forEach((file, index) => {
        console.log(`${index + 1}. ${file}`);
      });

      return results;
    } catch (error) {
      console.error(chalk.red(`Search error: ${error.message}`));
      return [];
    }
  }

  async read(filePath) {
    console.log(chalk.blue(`\n📖 Reading: ${filePath}\n`));

    try {
      await this.safety.validatePath(filePath, this.vaultPath);
      await this.safety.validateExtension(filePath);

      const content = await this.mcpClient.readFile(filePath);
      console.log(chalk.green("File content:"));
      console.log(content);
      return content;
    } catch (error) {
      console.error(chalk.red(`Read error: ${error.message}`));
      return null;
    }
  }

  async write(filePath, content) {
    console.log(chalk.blue(`\n✏️ Writing to: ${filePath}\n`));

    try {
      await this.safety.validatePath(filePath, this.vaultPath);
      await this.safety.validateExtension(filePath);

      // Create backup if file exists
      const backupPath = await this.safety.createBackup(filePath);
      if (backupPath) {
        console.log(chalk.yellow(`Backup created: ${backupPath}`));
      }

      await this.mcpClient.writeFile(filePath, content);
      console.log(chalk.green("File written successfully"));
      return true;
    } catch (error) {
      console.error(chalk.red(`Write error: ${error.message}`));
      return false;
    }
  }

  async edit(filePath, oldText, newText) {
    console.log(chalk.blue(`\n📝 Editing: ${filePath}\n`));

    try {
      await this.safety.validatePath(filePath, this.vaultPath);
      await this.safety.validateExtension(filePath);

      // Create backup
      const backupPath = await this.safety.createBackup(filePath);
      if (backupPath) {
        console.log(chalk.yellow(`Backup created: ${backupPath}`));
      }

      await this.mcpClient.editFile(filePath, oldText, newText);
      console.log(chalk.green("File edited successfully"));
      return true;
    } catch (error) {
      console.error(chalk.red(`Edit error: ${error.message}`));
      return false;
    }
  }

  async move(sourcePath, destPath) {
    console.log(chalk.blue(`\n📁 Moving: ${sourcePath} -> ${destPath}\n`));

    try {
      await this.safety.validatePath(sourcePath, this.vaultPath);
      await this.safety.validatePath(destPath, this.vaultPath);

      if (config.safety.confirmDestructive) {
        const { confirm } = await inquirer.prompt([
          {
            type: "confirm",
            name: "confirm",
            message: "This will move the file. Continue?",
            default: false,
          },
        ]);

        if (!confirm) {
          console.log(chalk.yellow("Operation cancelled"));
          return false;
        }
      }

      await this.mcpClient.moveFile(sourcePath, destPath);
      console.log(chalk.green("File moved successfully"));
      return true;
    } catch (error) {
      console.error(chalk.red(`Move error: ${error.message}`));
      return false;
    }
  }

  async delete(filePath) {
    console.log(chalk.blue(`\n🗑️ Deleting: ${filePath}\n`));

    try {
      await this.safety.validatePath(filePath, this.vaultPath);

      if (config.safety.confirmDestructive) {
        const { confirm } = await inquirer.prompt([
          {
            type: "confirm",
            name: "confirm",
            message: "This will move the file to trash. Continue?",
            default: false,
          },
        ]);

        if (!confirm) {
          console.log(chalk.yellow("Operation cancelled"));
          return false;
        }
      }

      // Soft delete to trash
      const trashPath = path.join(this.vaultPath, config.vault.trashPath);
      await this.mcpClient.createDirectory(trashPath);

      const trashFile = await this.safety.softDelete(filePath, trashPath);
      console.log(chalk.green(`File moved to trash: ${trashFile}`));
      return true;
    } catch (error) {
      console.error(chalk.red(`Delete error: ${error.message}`));
      return false;
    }
  }

  async ask(question, provider = "grok") {
    console.log(chalk.blue(`\n🤖 Asking ${provider}: ${question}\n`));

    try {
      // Search for relevant files
      const searchResults = await this.mcpClient.searchFiles(question);

      let context = "";
      if (searchResults && searchResults.length > 0) {
        console.log(
          chalk.yellow(
            `Reading ${Math.min(3, searchResults.length)} relevant files...`
          )
        );

        // Read top 3 files
        for (let i = 0; i < Math.min(3, searchResults.length); i++) {
          const content = await this.mcpClient.readFile(searchResults[i]);
          context += `\n\n--- File: ${searchResults[i]} ---\n${content}`;
        }
      }

      // Query AI provider
      const spinner = ora(`Querying ${provider}...`).start();
      const response = await this.provider.query(question, context, provider);
      spinner.succeed(`${provider} responded`);

      console.log(chalk.green("\nResponse:"));
      console.log(response);

      return response;
    } catch (error) {
      console.error(chalk.red(`Query error: ${error.message}`));
      return null;
    }
  }

  async interactive() {
    console.log(chalk.cyan("\n🎮 Interactive Mode\n"));

    const actions = [
      "Search files",
      "Read file",
      "Write file",
      "Edit file",
      "Move file",
      "Delete file",
      "Ask AI",
      "List directory",
      "Exit",
    ];

    while (true) {
      const { action } = await inquirer.prompt([
        {
          type: "list",
          name: "action",
          message: "What would you like to do?",
          choices: actions,
        },
      ]);

      switch (action) {
        case "Search files": {
          const { query } = await inquirer.prompt([
            {
              type: "input",
              name: "query",
              message: "Enter search query:",
            },
          ]);
          await this.search(query);
          break;
        }

        case "Read file": {
          const { filePath } = await inquirer.prompt([
            {
              type: "input",
              name: "filePath",
              message: "Enter file path:",
            },
          ]);
          await this.read(path.join(this.vaultPath, filePath));
          break;
        }

        case "Write file": {
          const { filePath, content } = await inquirer.prompt([
            {
              type: "input",
              name: "filePath",
              message: "Enter file path:",
            },
            {
              type: "editor",
              name: "content",
              message: "Enter content:",
            },
          ]);
          await this.write(path.join(this.vaultPath, filePath), content);
          break;
        }

        case "Edit file": {
          const { filePath } = await inquirer.prompt([
            {
              type: "input",
              name: "filePath",
              message: "Enter file path:",
            },
          ]);

          // Read current content
          const currentContent = await this.read(
            path.join(this.vaultPath, filePath)
          );
          if (!currentContent) break;

          const { oldText, newText } = await inquirer.prompt([
            {
              type: "input",
              name: "oldText",
              message: "Enter text to replace:",
            },
            {
              type: "input",
              name: "newText",
              message: "Enter new text:",
            },
          ]);
          await this.edit(
            path.join(this.vaultPath, filePath),
            oldText,
            newText
          );
          break;
        }

        case "Move file": {
          const { source, dest } = await inquirer.prompt([
            {
              type: "input",
              name: "source",
              message: "Enter source path:",
            },
            {
              type: "input",
              name: "dest",
              message: "Enter destination path:",
            },
          ]);
          await this.move(
            path.join(this.vaultPath, source),
            path.join(this.vaultPath, dest)
          );
          break;
        }

        case "Delete file": {
          const { filePath } = await inquirer.prompt([
            {
              type: "input",
              name: "filePath",
              message: "Enter file path to delete:",
            },
          ]);
          await this.delete(path.join(this.vaultPath, filePath));
          break;
        }

        case "Ask AI": {
          const { question, provider } = await inquirer.prompt([
            {
              type: "input",
              name: "question",
              message: "Enter your question:",
            },
            {
              type: "list",
              name: "provider",
              message: "Select AI provider:",
              choices: ["grok", "perplexity", "openai"],
              default: "grok",
            },
          ]);
          await this.ask(question, provider);
          break;
        }

        case "List directory": {
          const { dirPath } = await inquirer.prompt([
            {
              type: "input",
              name: "dirPath",
              message: "Enter directory path (or press Enter for root):",
              default: "",
            },
          ]);

          const fullPath = dirPath
            ? path.join(this.vaultPath, dirPath)
            : this.vaultPath;

          try {
            const listing = await this.mcpClient.listDirectory(fullPath);
            console.log(chalk.green("\nDirectories:"));
            listing.dirs.forEach((dir) => console.log(`  📁 ${dir}`));
            console.log(chalk.green("\nFiles:"));
            listing.files.forEach((file) => console.log(`  📄 ${file}`));
          } catch (error) {
            console.error(chalk.red(`List error: ${error.message}`));
          }
          break;
        }

        case "Exit":
          console.log(chalk.cyan("Goodbye! 👋"));
          this.mcpClient.stop();
          process.exit(0);
      }

      console.log(""); // Add spacing
    }
  }

  cleanup() {
    this.mcpClient.stop();
  }
}

// CLI Command Setup
const program = new Command();

program
  .name("obs-bridge")
  .description("MCP Bridge for Obsidian vault interaction")
  .version("1.0.0");

program
  .command("search <query>")
  .description("Search for files in the vault")
  .action(async (query) => {
    const bridge = new ObsidianBridge();
    if (await bridge.initialize()) {
      await bridge.search(query);
      bridge.cleanup();
    }
  });

program
  .command("read <filepath>")
  .description("Read a file from the vault")
  .action(async (filepath) => {
    const bridge = new ObsidianBridge();
    if (await bridge.initialize()) {
      const fullPath = path.join(config.vault.path, filepath);
      await bridge.read(fullPath);
      bridge.cleanup();
    }
  });

program
  .command("write <filepath>")
  .description("Write content to a file")
  .option("-c, --content <content>", "Content to write")
  .action(async (filepath, options) => {
    const bridge = new ObsidianBridge();
    if (await bridge.initialize()) {
      const fullPath = path.join(config.vault.path, filepath);
      const content = options.content || "";
      await bridge.write(fullPath, content);
      bridge.cleanup();
    }
  });

program
  .command("move <source> <dest>")
  .description("Move a file within the vault")
  .action(async (source, dest) => {
    const bridge = new ObsidianBridge();
    if (await bridge.initialize()) {
      const sourcePath = path.join(config.vault.path, source);
      const destPath = path.join(config.vault.path, dest);
      await bridge.move(sourcePath, destPath);
      bridge.cleanup();
    }
  });

program
  .command("delete <filepath>")
  .description("Delete a file (moves to trash)")
  .action(async (filepath) => {
    const bridge = new ObsidianBridge();
    if (await bridge.initialize()) {
      const fullPath = path.join(config.vault.path, filepath);
      await bridge.delete(fullPath);
      bridge.cleanup();
    }
  });

program
  .command("ask <question>")
  .description("Ask AI about your vault")
  .option(
    "-p, --provider <provider>",
    "AI provider (grok/perplexity/openai)",
    "grok"
  )
  .action(async (question, options) => {
    const bridge = new ObsidianBridge();
    if (await bridge.initialize()) {
      await bridge.ask(question, options.provider);
      bridge.cleanup();
    }
  });

program
  .command("interactive")
  .description("Start interactive mode")
  .action(async () => {
    const bridge = new ObsidianBridge();
    if (await bridge.initialize()) {
      await bridge.interactive();
    }
  });

program
  .command("test")
  .description("Test MCP connection")
  .action(async () => {
    console.log(chalk.cyan("Testing MCP connection...\n"));
    const bridge = new ObsidianBridge();

    if (await bridge.initialize()) {
      console.log(chalk.green("✅ MCP connection successful"));
      console.log(`Vault path: ${config.vault.path}`);

      try {
        const listing = await bridge.mcpClient.listDirectory(config.vault.path);
        console.log(
          `\nFound ${listing.dirs.length} directories and ${listing.files.length} files`
        );
      } catch (error) {
        console.error(chalk.red(`Test failed: ${error.message}`));
      }

      bridge.cleanup();
    }
  });

// Parse command line arguments
program.parse(process.argv);

// If no command provided, show help
if (!process.argv.slice(2).length) {
  program.outputHelp();
}
```

## 📝 Step 9: Create README.md

````markdown
# Obsidian MCP Bridge

A powerful bridge that allows AI providers (Perplexity, Grok, ChatGPT) to interact with your Obsidian vault through the Model Context Protocol (MCP).

## Features

- 🔍 **Search** - Find files in your vault using pattern matching
- 📖 **Read** - Read any file from your vault
- ✏️ **Write** - Create or update files
- 📝 **Edit** - Make targeted edits to existing files
- 📁 **Move** - Reorganize files within your vault
- 🗑️ **Delete** - Safely move files to trash
- 🤖 **AI Integration** - Query your vault using Grok, Perplexity, or OpenAI

## Installation

1. Clone this repository:

```bash
cd C:\Users\YC\MCPs
git clone [repository-url] obsidian-bridge
cd obsidian-bridge
```
````

2. Install dependencies:

```bash
npm install
```

3. Configure your vault path in `config/config.json`:

```json
{
  "vault": {
    "path": "C:\\Your\\Vault\\Path"
  }
}
```

4. Set up API keys in `.env`:

```bash
GROK_API_KEY=your_key_here
PERPLEXITY_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
```

## Usage

### Interactive Mode (Recommended)

```bash
npm start interactive
```

### Command Line

Search for files:

```bash
npm start search "prompt engineering"
```

Read a file:

```bash
npm start read "1-Projects/system-spec-generator/index.md"
```

Ask AI about your vault:

```bash
npm start ask "What are my active projects?" --provider grok
```

Write a new file:

```bash
npm start write "new-note.md" --content "# New Note\n\nContent here"
```

Move a file:

```bash
npm start move "old-location.md" "new-location.md"
```

Delete a file (moves to trash):

```bash
npm start delete "unwanted-file.md"
```

### Test Connection

```bash
npm start test
```

## Safety Features

- **Path Validation** - Prevents access outside vault
- **Protected Folders** - Cannot modify .obsidian, .git, etc.
- **Automatic Backups** - Creates backups before edits
- **Soft Delete** - Files moved to trash, not permanently deleted
- **Confirmation Prompts** - Requires confirmation for destructive operations

## Architecture

```
User → CLI → MCP Client → MCP Server → Vault Files
               ↓
         AI Providers → Response
```

## Troubleshooting

### MCP Server Won't Start

- Ensure Node.js is installed and in PATH
- Check that npx is available: `npx -v`
- Verify vault path exists

### API Errors

- Check API keys in .env file
- Verify API quotas and limits
- Check network connectivity

### File Access Issues

- Ensure vault path is correct
- Check file permissions
- Verify no other process is locking files

## Development

Run tests:

```bash
npm test
```

Add new provider:

1. Add configuration in `config/config.json`
2. Implement query method in `lib/providers.js`
3. Add to CLI options

## License

MIT

## Support

For issues and questions, please open an issue on GitHub.

````

## 🚀 Step 10: Setup and Run

### Installation Steps:

1. **Create the project directory:**
```powershell
# In PowerShell
mkdir C:\Users\YC\MCPs\obsidian-bridge
cd C:\Users\YC\MCPs\obsidian-bridge
````

2. **Create all the files above in their respective locations**
3. **Install dependencies:**

```powershell
npm install
```

4. **Configure your vault path:** Edit `config/config.json` and update the vault path to your actual Obsidian vault location.
5. **Add your API keys:** Create `.env` file with your actual API keys.
6. **Test the connection:**

```powershell
npm start test
```

7. **Start interactive mode:**

```powershell
npm start interactive
```

## 🎯 Usage Examples

### Example 1: Search and Read

```powershell
# Search for AI-related notes
npm start search "AI prompt"

# Read a specific file
npm start read "1-Projects/system-spec-generator/index.md"
```

### Example 2: Ask AI About Your Vault

```powershell
# Using Grok (default)
npm start ask "What projects am I working on?"

# Using Perplexity
npm start ask "Summarize my prompt library" --provider perplexity
```

### Example 3: Create a New Note

```powershell
# Create a new project note
npm start write "1-Projects/new-project/index.md" --content "# New Project\n\n## Goals\n- Goal 1\n- Goal 2"
```

### Example 4: Organize Files

```powershell
# Move a file to archive
npm start move "old-project.md" "7-Archive/2024/old-project.md"

# Delete (move to trash)
npm start delete "draft.md"
```

## 🛡️ Safety Features

The system includes multiple safety layers:

1. **Path Validation** - Can't access files outside your vault
2. **Extension Filtering** - Only works with .md, .txt, .json, .yml files
3. **Automatic Backups** - Creates `.backup` files before edits
4. **Soft Delete** - Moves to `_Trash` folder instead of permanent deletion
5. **Protected Folders** - Can't modify `.obsidian`, `.git`, `node_modules`
6. **Confirmation Prompts** - Asks before destructive operations

## 🔧 Customization

### Add a New AI Provider

To add a new AI provider, edit `lib/providers.js`:

```javascript
async queryNewProvider(prompt, context, config) {
  // Your implementation here
  const response = await fetch(config.apiUrl, {
    // API call details
  });
  return response.data;
}
```

### Change File Restrictions

Edit `config/config.json`:

```json
"safety": {
  "allowedExtensions": [".md", ".txt", ".json", ".yml", ".pdf"],
  "maxFileSize": 5242880,  // 5MB
  "protectedFolders": [".obsidian", ".git"]
}
```

## 🎉 Success!

Your Obsidian MCP Bridge is now ready! The system provides:

- ✅ Full read/write access to your vault
- ✅ AI integration with multiple providers
- ✅ Safety features to prevent accidents
  - ✅ Interactive and command-line modes
- ✅ Extensible architecture

Start with `npm start interactive` for the easiest experience, or use the command-line interface for scripting and automation.
