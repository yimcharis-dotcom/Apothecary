---
title: Vertex API Calling Debug
type: troubleshooting
status: solved
Updated: 2026-02-11
date: 2026-02-11
tags:
  - opencode
  - vertex-ai
  - gemini
  - troubleshooting
  - cursor
project_id: gen-lang-client-0127739997
---
## Problem
OpenCode failed with a Vertex model error similar to:
```
`Publisher Model projects/gen-lang-client-0127739997/locations/us-east5/publishers/google/models/gemini-3-pro-preview was not found or your project does not have access to it.`
```
**Root cause:** model call used a regional location, while the model needed the global endpoint path.
[Vertex AI partner models for MaaS  \|  Generative AI on Vertex AI  \|  Google Cloud Documentation](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-partner-models#regional_and_global_endpoints)
# Fix Applied
Updated workspace config file `opencode.json` to force Vertex global endpoint settings: [[opencode.json]]
```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "google-vertex": {
      "options": {
        "project": "gen-lang-client-0127739997",
        "location": "global"
      }
    }
  }
}
```
Backup copy saved as `opencode.global.backup.json`.[[opencode.global.backup.json]]
# Verification Performed
1. Confirmed active gcloud project:
   - `gcloud config get-value project` -> `gen-lang-client-0127739997`
2. Tested direct **Vertex API** call:
   - `POST https://aiplatform.googleapis.com/v1/projects/gen-lang-client-0127739997/locations/global/publishers/google/models/gemini-3-pro-preview:generateContent`
   - Result: HTTP 200 with valid model response.
3. Tested OpenCode run:
   - `opencode run -m google-vertex/gemini-3-pro-preview "reply with exactly: OK_GEMINI3"`
   - Result: success.
# Notes
- This fix is for Gemini on Vertex via OpenCode.
- OpenCode updates should not overwrite workspace `opencode.json`.
- If a new workspace has no `opencode.json`, repeat this config or add a global config.

# Important findings (not to miss)
- If Cursor shows `Provider Error` (for example code `57`), it can be a Cursor app/extension-host issue even when Vertex is healthy.
- In this case, direct Vertex and OpenCode checks passed while Cursor logs showed extension conflicts/crashes.
- Useful log file for this incident: `C:\Users\YC\AppData\Roaming\Cursor\logs\20260211T204614\window1\renderer.log`
- OpenCode currently works for Vertex Gemini models with `location: global`.
- Some non-Google Vertex MaaS models may still return `Not Found` in OpenCode due to model path mapping behavior.
# Global Default Applied (all folders)
Created `C:\Users\YC\.config\opencode\opencode.json` with:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "google-vertex": {
      "options": {
        "project": "gen-lang-client-0127739997",
        "location": "global"
      }
    }
  }
}
```
Verified resolved config from outside the workspace (`C:\Users\YC`) with:
`opencode debug config` 
This ensures new OpenCode instances (other folders) inherit the global Vertex location and project settings.

# Quick preflight checks
```bash
opencode debug config
opencode run -m google-vertex/gemini-3-pro-preview "reply with exactly: OPENCODE_OK"
```
