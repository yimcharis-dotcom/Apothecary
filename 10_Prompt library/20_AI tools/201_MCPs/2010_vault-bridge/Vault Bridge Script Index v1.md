---
Type: index
Tags:
  - Ai/mcp
  - Index
  - Documentation
  - scripts
Created: 2026-01-13
Updated: 2026-01-13 hh:mm
Version: 1.0.0
Status: WIP
---

# 📚 Vault Bridge - Script Index

> **Complete index of all scripts, configuration files, and documentation for the Obsidian Vault Q&A Bridge MCP server**
---

## 📖 Documentation

### Main Guide
- [[Obsidian Vault Q&A Bridge - Complete Production Guide v1]] - Complete production guide with installation, usage, troubleshooting, and examples
---

## 🔧 Script Files

### Main Script
- [[@complete_bridge.Cjs]] - Main MCP bridge server implementation
  - **Location**: `scr/complete_bridge.Cjs`
  - **Type**: CommonJS Module (Node. Js)
  - **Purpose**: Core bridge connecting Obsidian vault with AI providers

### Configuration Files
- [[@config.json]] - Configuration file with paths, API keys, and settings
  - **Location**: `scr/config.json`
  - **Type**: JSON Configuration
  - **Purpose**: Stores vault path, Python paths, API keys, and default settings

### Dependencies
- [[@package.json]] - Node. Js package dependencies and metadata ^2bcc8d
  - **Location**: `scr/package.json`
  - **Type**: NPM Package Configuration
  - **Purpose**: Defines project dependencies (@modelcontextprotocol/sdk)
    
- ### Query pipeline
- - [[@complete_bridge.Cjs]] – Query execution and orchestration ^query
-   - **Location**: `scr/complete_bridge.cjs`
-   - **Type**: Runtime Pipeline
-   - **Purpose**: 
-     - Runs Python RAG search to identify relevant vault files
-     - Reads selected files using MCP filesystem server
-     - Sends extracted context to the selected AI provider and model
- 
