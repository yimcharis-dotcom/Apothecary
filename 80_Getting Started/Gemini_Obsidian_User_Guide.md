---
created: 2026-02-19T04:56:40
tags: [setup, gemini]
---

# Gemini Obsidian Extension User Guide

## Overview
This vault is now integrated with Gemini CLI, allowing you to search, query, and manage your notes using AI.

## 🚀 Key Commands

| Command | Description |
| :--- | :--- |
| `/obsidian:ask` | **RAG Query**: Ask questions about your notes. <br>_Example: 'What did I learn about React hooks?'_ |
| `/obsidian:search` | **Fuzzy Search**: Find files by name or content. <br>_Example: 'project specs'_ |
| `/obsidian:daily` | **Journaling**: Open or append to today's daily note. |
| `/obsidian:index` | **Re-index**: Update the search index after adding many notes. |

## 🧠 Capabilities

### 1. Semantic Search (RAG)
Instead of just matching keywords, you can ask questions in natural language. The AI understands the *meaning* of your notes.
- 'Summarize my meetings from last week.'
- 'What is the connection between Project A and Project B?'

### 2. Graph Traversal
The AI can see links between notes.
- 'What notes link to this one?'
- 'Find all backlinks for System Architecture.'

### 3. Note Management
You can ask Gemini to:
- Create new notes: 'Create a note for the new marketing strategy.'
- Append to notes: 'Add this link to the Resources note.'
- Update metadata: 'Add status: active to the frontmatter.'

## 🔧 Troubleshooting
If the search feels outdated, run `/obsidian:index` to refresh the knowledge base.
