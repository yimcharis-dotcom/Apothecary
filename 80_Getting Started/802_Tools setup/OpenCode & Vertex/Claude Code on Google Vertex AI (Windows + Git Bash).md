---
title: Claude Code on Google Vertex AI (Windows + Git Bash)
type: setup
status: draft
tags:
  - claude-code
  - vertex-ai
  - setup
created: 2026-02-11
project_id: gen-lang-client-0127739997
---
## Goal
Run Claude Code using Google Vertex AI with project `gen-lang-client-0127739997`.
## Prereqs
- `gcloud` installed and working
- Claude Code installed (you can run `claude`)
## Step 2: Enable Vertex AI API
```bash
gcloud services enable aiplatform.googleapis.com
```
Verify:
```bash
gcloud services list --enabled | grep aiplatform
```
## Step 3: Create Application Default Credentials (ADC)
```bash
gcloud auth application-default login
```
Verify:
```bash
gcloud auth application-default print-access-token >/dev/null && echo "ADC OK"
```
## Step 4: Set env vars (session only)
Required:
```bash
export CLAUDE_CODE_USE_VERTEX=1 
export CLOUD_ML_REGION=global 
export ANTHROPIC_VERTEX_PROJECT_ID=gen-lang-client-0127739997
```
Optional (only if you want to force models):
```bash
export ANTHROPIC_MODEL='claude-opus-4-6' 
export ANTHROPIC_DEFAULT_MODEL='claude-sonnet-4-5@20250929'
export ANTHROPIC_SMALL_FAST_MODEL='claude-haiku-4-5@20251001'

export VERTEX_REGION_CLAUDE_3_5_SONNET=global

export VERTEX_REGION_CLAUDE_4_5_HAIKU=global 
export VERTEX_REGION_CLAUDE_4_5_OPUS=global 
export VERTEX_REGION_CLAUDE_4_5_SONNET=global 
export VERTEX_REGION_CLAUDE_4_6_OPUS=global
```
Verify:
```bash
env | grep -E'CLAUDE_CODE_USE_VERTEX|CLOUD_ML_REGION|ANTHROPIC_VERTEX_PROJECT_ID|ANTHROPIC_MODEL|ANTHROPIC_SMALL_FAST_MODEL' | sort
```
---
>[!Remarks] Anthropic's models are easy. Starting with 0 Quota and request increase will have to be reviewed). So Abort. FYI below: 

# Make env vars permanent (Git Bash)
```
Open your bash profile:

`notepad ~/.bashrc`

Add:

`export CLAUDE_CODE_USE_VERTEX=1 export CLOUD_ML_REGION=global export ANTHROPIC_VERTEX_PROJECT_ID=gen-lang-client-0127739997 # Optional: # export ANTHROPIC_MODEL='claude-opus-4-6' # export ANTHROPIC_SMALL_FAST_MODEL='claude-haiku-4-5@20251001'`

Apply in the current terminal:

`source ~/.bashrc`

## Troubleshooting (only if the first prompt errors)

### 404 / model not found

Stop forcing the model and retry:

`unset ANTHROPIC_MODEL`

### 403 / permission denied

If you control IAM, grant yourself:

`gcloud projects add-iam-policy-binding gen-lang-client-0127739997 \   --member="user:YOUR_GOOGLE_EMAIL" \   --role="roles/aiplatform.user"`

### 429 / quota

This is quota/rate limiting. Increase quota or retry later.

