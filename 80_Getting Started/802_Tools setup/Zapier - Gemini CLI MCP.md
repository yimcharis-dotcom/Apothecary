---
Type: setup
Tags:
  - geminicli
  - MCP
  - Setup
Created: 2026-02-17
---

# Configuring Zapier MCP in Gemini CLI
### 1. Update .env
Add your Zapier Connection URL to your `.env` file:
```bash
ZAPIER_MCP_URL=https://mcp.zapier.com/mcp/servers/6ac82273-c2f1-40f8-a372-6f4e5cc82984/connections
```

### 2. Configure settings.json
Refer to the variable in your configuration:
```json
{
  "mcpServers": {
    "zapier": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "${ZAPIER_MCP_URL}",
        "--transport",
        "http-only"
      ],
      "trust": true
    }
  }
}
```