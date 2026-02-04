---
type: session-log
project: "[[AI Hub Refactor]]"
date: 2026-02-04
tags:
  - vibe-coding
  - planning
---

# Refactor Planning Session

## Current State

- [x] Analyzed `src_refactor` scripts.
- [x] Identified "Brain" (`AIToolsConfig.ps1`) vs "Hands" (`SyncSkills.ps1`) separation.
- [x] Fixed `SetupAutoStart_Final.ps1` overwriting bug.

## What I want to Refine (My Thoughts)

- C:\Users\YC\Perplexity - Copy'  

>[03:02:04] NEW FOLDER DETECTED
>[03:02:04]   Name: New folder
>[03:02:04]   Path: C:\Users\YC\New folder
>[03:02:04]   Category: User_Dot
>[03:02:05]   [o] Not identified as AI tool (skipping)

- 'C:\Users\YC\Perplexity'

>[03:02:04] NEW FOLDER DETECTED
>[03:02:04]   Name: New folder
>[03:02:04]   Path: C:\Users\YC\New folder
>[03:02:04]   Category: User_Dot
>[03:02:05]   [o] Not identified as AI tool (skipping)
>[03:02:05] =====================================================

- Deletion not detected

- but i wanna includes files like plans, transcripts, and other information i would likely to go back to not only  conjig

Should be excluded
>[03:10:38] [+] Monitoring: C:\Users\YC\GitHubRepo
>[03:10:38]   Category: Projects_GitHubRepo

- [ ] [Your thought here...]

## Decisions to Make

- Should we move these scripts out of `src_refactor` to the main folder?
- Do we need a "Quiet Mode" toggle in the main menu?
