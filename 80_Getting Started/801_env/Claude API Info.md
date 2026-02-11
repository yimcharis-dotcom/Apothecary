---
Tags:
  - ai/integration
  - Claude
  - plugin
  - ai/api
Created: 2026-01-08
updated: 2026-02-10T22:02:00
Status: Active
---

# Claude API Reference
## Credentials & Config
**API Key** (v 2026-01-08):
```
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
```

- **Base URL**: `https://api.anthropic.com`
- **Version**: `2023-06-01`
- **Docs**: [Official Documentation](https://console.anthropic.com/docs/en/home) | [API Reference](https://docs.anthropic.com/claude/reference/)

## Available APIs

**General Availability:**
- **[Messages API]** : `POST /v1/messages`
- **[Message Batches API]**: `POST /v1/messages/batches`
- **[Token Counting API]**: `POST /v1/messages/count_tokens`
- **[Models API]**: `GET /v1/models`

## Authentication

All requests to the Claude API must include these headers:

|Header|Value|Required|
|---|---|---|
|`x-api-key`|`{{API_KEY}}`|Yes|
|`anthropic-version`|`2023-06-01`|Yes|
|`content-type`|`application/json`|Yes|

If you are using the [Client SDKs](https://console.anthropic.com/docs/en/api/overview#client-sdks), the SDK will send these headers automatically. For API versioning details, see [API versions](https://console.anthropic.com/docs/en/api/versioning).
