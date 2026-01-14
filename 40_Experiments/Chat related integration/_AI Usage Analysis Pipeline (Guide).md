---
Title:
Created: 2026-01-10
Tags:
  - ai/usage
  - Pipeline
  - Guide
  - chatgpt
  - PPLX
---

## Purpose

This note documents a repeatable pipeline to analyze my own AI usage patterns.
The goal is diagnostic: understand session length, intensity, and where limits or quotas interrupt meaningful work.  
This pipeline is **not** a permanent data system. It is designed to be rerun occasionally with minimal setup.

---

## Overview of the pipeline
The pipeline has three practical stages:  
- Export raw data from platforms
- Normalize usage into comparable units
- Analyze session shape and flow  

Optional Perplexity CLI work is documented separately.

---  
## Working directory (important)
All steps assume this directory:
```
C:\Users\YC\OneDrive\Desktop\AI hub\ai usages\
```
Recommended structure:  
- Exports/ → raw platform exports
- Out/ → generated CSVs and reports
- Scripts live at the root  
Keeping everything under one folder avoids path confusion.
---
## Step 1: Export data
### ChatGPT
- Use ChatGPT → Export Data
- You will receive a `.zip`
- Place it at:   `Exports/chatgpt. Zip`    
 ChatGPT exports include **per-message timestamps**, which are critical.
---

### Perplexity (web / desktop)

- Use the Perplexity export extension
- Export each thread as Markdown
- Place files in: `Exports/pplx/`  

**Limitation:**
- These exports are thread-level only
- No per-message timestamps

This is acceptable for coarse comparison.

---

## Step 2: Sanity-check Perplexity exports

Before parsing, confirm structure once.

Run the script documented in:
[[AI Usage Analysis – Core Scripts]]

Purpose:
- Confirm frontmatter exists
- Confirm headings are present
- Confirm timestamps are absent (expected)

This step is only needed once per exporter.

---

## Step 3: Normalize data

Normalization decisions:

- ChatGPT → user message = one event
- Perplexity → one thread = one event

This asymmetry is intentional and acknowledged.

Scripts used:
- `Parse_pplx_threads. Py`
- `Parse_chatgpt_and_daily. Py`

Details live in:
[[AI Usage Analysis – Core Scripts]]

---

## Step 4: Analyze usage

Analysis focuses on:

- Active days
- Events per day
- ChatGPT sessionization

A session is defined as:
- A sequence of user turns
- Broken by >30 minutes of inactivity

The goal is not precision but **shape**.

---
## Links

- [[AI Usage Analysis – Core Scripts]]
- [[AI Usage Analysis – Perplexity CLI Branch]]
