---
Tags:
  - ai/integration
  - ai/Claude
  - plugin
Created: 2026-01-08
---

[Documentation - Claude Docs](https://console.anthropic.com/docs/en/home)

## Available APIs

The Claude API includes the following APIs:

API Key v 2026-01-08 21:58
```
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
```
**General Availability:**
- **[Messages API]** : Send messages to Claude for conversational interactions (`POST /v1/messages`)
- **[Message Batches API]**: Process large volumes of Messages requests asynchronously with 50% cost reduction (`POST /v1/messages/batches`)
- **[Token Counting API]**: Count tokens in a message before sending to manage costs and rate limits (`POST /v1/messages/count_tokens`)
- **[Models API]**: List available Claude models and their details (`GET /v1/models`)

## Authentication

All requests to the Claude API must include these headers:

|Header|Value|Required|
|---|---|---|
|`x-api-key`|Your API key from Console|Yes|
|`anthropic-version`|API version (e.g., `2023-06-01`)|Yes|
|`content-type`|`application/json`|Yes|

If you are using the [Client SDKs](https://console.anthropic.com/docs/en/api/overview#client-sdks), the SDK will send these headers automatically. For API versioning details, see [API versions](https://console.anthropic.com/docs/en/api/versioning).
