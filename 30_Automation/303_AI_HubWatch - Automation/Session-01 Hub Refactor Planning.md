---
type: session-log
project: "[[AI Hub Refactor]]"
date: 2026-02-04
updated: 2026-02-07
tags:
  - vibe-coding
  - planning
  
---

# Refactor Planning Session

## Current State

- [x] Analyzed `src_refactor` scripts.
- [x] Identified "Brain" (`AIToolsConfig.ps1`) vs "Hands" (`SyncSkills.ps1`) separation.
- [x] Fixed `SetupAutoStart_Final.ps1` overwriting bug.

## Refactor Direction (Provider-First)

### Target Model

- 1 folder = 1 provider at top hierarchy.
- Product/tool names are metadata under provider, not top-level folders.
- Detection flow: `keywords -> subagent -> human`.

### Detection Pipeline

1. Layer 1: keyword/alias matcher (fast local pass)
   - Uses provider aliases and shorthands only.
   - Includes well-known brand nicknames and package IDs.
2. Layer 2: subagent evidence pass (only when low confidence)
   - Collects evidence from local package metadata, domains, and approved external signals.
   - Can use web and email signup traces for provider disambiguation.
3. Layer 3: human decision
   - Prompt on every low-confidence detection.
   - Questions: AI-related?, provider?, supports skills?, supports MCP?, approve auto-actions?

### Automation Gates

- `approved`: create/update provider link, skills sync auto, deletion sync auto, export auto.
- `pending`: hold actions except evidence logging.
- `rejected`: ignore and suppress repeats unless artifact changes.

## Data Contracts (Operational)

### Decision Table (CSV/JSON)

- `event_id`
- `detected_at`
- `artifact_path`
- `artifact_type` (folder, package, process, extension, mcp_server)
- `layer1_provider`
- `layer1_confidence`
- `layer2_provider`
- `layer2_confidence`
- `evidence_local`
- `evidence_external`
- `is_ai_related` (yes/no/pending)
- `provider_final`
- `supports_skills` (yes/no/unknown)
- `supports_mcp` (yes/no/unknown)
- `action_state` (approved/pending/rejected)
- `reviewed_by`
- `reviewed_at`
- `notes`

### Provider Registry

- Canonical provider names and aliases.
- Maps keywords/shorthands/package names to provider.
- Supports manual overrides.

## Issues to Include in Refactor Plan

### P0 - Correctness / Data Integrity

- Current watcher is product/folder-name-first, not provider-first.
- Deletion flow can remove by derived name without strict target verification.
- `Claude_AI_Ecosystem_Master_List.json` has corrupted row data (`Presence` for VS Code is malformed).

### P1 - Detection Quality

- Current detection can still produce false positives or miss providers.
- Shared strict definitions exist but are not consistently used across scripts.

### P2 - Operational Gaps

- No structured decision ledger for ambiguous detections.
- No confidence thresholds and no explicit state machine.
- Runbook and current behavior are out of sync in parts.

## Execution Plan

### Phase 1: Foundation

1. Add provider registry file (canonical provider + aliases).
2. Add decision table file and loader utilities.
3. Add watcher state machine (`pending/approved/rejected`).

### Phase 2: Detection Flow

1. Implement Layer 1 keyword matcher in `AIToolsConfig.ps1`.
2. Add Layer 2 subagent hook interface (pluggable evidence collector).
3. Add human prompt in `Hub.ps1` or watcher wrapper for pending items.

### Phase 3: Safe Automation

1. Gate symlink/skill/export actions on `approved`.
2. Add strict deletion safety: verify link target before remove.
3. Add suppression cache for rejected artifacts.

### Phase 4: Data Cleanup + Migration

1. Fix malformed rows in master JSON/CSV.
2. Migrate existing product-first entries into provider-first structure.
3. Regenerate summary outputs.

## Next Step (Immediate)

- Draft and commit the two new schemas first:
  1. `provider_registry.json`
  2. `detection_decisions.csv` (with headers only)
- Then wire `WatchHub_Realtime.ps1` to write `pending` records instead of direct auto-linking for unknown cases.

## Decisions to Make

- Should human prompt run inline during watch events or from a queue review command?
- Should all unknowns require approval, or allow auto-approve above a high confidence threshold?
- Should exports target only CSV/JSON (and keep Obsidian optional)?
