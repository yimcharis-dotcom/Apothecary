---
created: 2026-02-07
updated: 2026-02-07T16:42:00  
plugin: Smart Composer
tags: [obsidian,plugin, MCP]
---

### Multi_Fetch

```json
{
  "command": "npx",
  "args": [
    "-y",
    "@upstash/context7-mcp@latest"
  ],
  "env": {
    "DEFAULT_MINIMUM_TOKENS": "10000"
  }
}
```

### Context7  [[Context 7 API Info]]

```json
{
  "command": "npx",
  "args": [
    "-y",
    "@lmcc-dev/mult-fetch-mcp-server"
  ],
  "env": {
    "MCP_LANG": "Auto-detected based on system"
  }
}
```
