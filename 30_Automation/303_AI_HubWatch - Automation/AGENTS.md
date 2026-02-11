# AI HubWatch Agent Guide

## Canonical Doc

This is the canonical multi-agent guide for this project.

- Claude-specific runtime/deployment notes: `./.claude.md`
- Dashboard-specific notes: `./dashboard/CLAUDE.md`

## Scope

This project has two active tracks:

- `src_v2_refactor`: watcher + automation runtime (`WatchHub_Realtime.ps1`, `SyncSkills.ps1`, `Hub.ps1`)
- `dashboard`: inventory/dashboard collectors and reporting

## Current Architecture Direction

- Top hierarchy is provider-first: 1 provider = 1 top-level identity.
- Detection flow is:
  1. `keywords` (Layer 1 local aliases)
  2. `subagent` (Layer 2 evidence enrichment)
  3. `human` (final decision for pending/ambiguous cases)
- Automation actions must be gated by decision state:
  - `approved`: allow linking/sync/export
  - `pending`: queue only
  - `rejected`: suppress

## Operational Files (Watcher)

Under `./src_v2_refactor`:

- `provider_registry.json`: canonical provider aliases for Layer 1
- `detection_decisions.csv`: decision ledger for Layer 2/3 workflow
- `WatchHub_Realtime.ps1`: writes pending decisions for low-confidence detections

## Rules

- Do not use broad generic keyword-only matching as final truth.
- Prefer provider mapping over product/folder naming.
- Preserve safety on delete operations (verify target before removal).
- Keep documentation in sync when detection logic changes.
