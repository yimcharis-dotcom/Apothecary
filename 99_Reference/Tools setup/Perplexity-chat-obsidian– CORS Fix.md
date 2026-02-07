---
title: Perplexity Chat (Obsidian) – CORS Fix
created: 2026-02-07
updated: 2026-02-07T16:42:00
plugin: perplexity-chat-obsidian
path: C:\Vault\Apothecary\.obsidian\plugins\perplexity-chat-obsidian\main.js
tags: [obsidian, pplx, plugin, CORS]
---

## What Changed
Replaced browser `fetch` with Obsidian's `requestUrl` to bypass CORS (Obsidian runs in a webview, so `fetch` is blocked by `app://obsidian.md`).

## Diff (Core Change)
```diff
- const response = yield fetch("https://api.perplexity.ai/v2/chat/completions", options);
-
- if (!response.ok) {
-   const errText = yield response.text();
-   throw new Error(`HTTP ${response.status}: ${errText}`);
- }
-
- return yield response.json();
+ const response = yield import_obsidian.requestUrl({
+   url: "https://api.perplexity.ai/v2/chat/completions",
+   method: "POST",
+   headers: options.headers,
+   body: options.body
+ });
+
+ if (response.status < 200 || response.status >= 300) {
+   const errText = response.text ?? JSON.stringify(response.json ?? {});
+   throw new Error(`HTTP ${response.status}: ${errText}`);
+ }
+
+ return response.json;
```

## Reusable Snippet
```ts
import { requestUrl } from "obsidian";

async function postJson(url: string, body: any, headers: Record<string, string>) {
  const res = await requestUrl({
    url,
    method: "POST",
    headers,
    body: JSON.stringify(body),
  });

  if (res.status < 200 || res.status >= 300) {
    const err = res.text ?? JSON.stringify(res.json ?? {});
    throw new Error(`HTTP ${res.status}: ${err}`);
  }

  return res.json;
}
```

## Why It Works
`requestUrl` runs in Obsidian's Node/Electron layer, so browser CORS rules don’t apply. `fetch` runs in the webview and is blocked by CORS.
