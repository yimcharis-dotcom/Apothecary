---
name: obsidian-vibe-flow
description: "Full-loop workflow bridging Obsidian and vibe coding tools (Cursor, Antigravity, VS Code). Use when the user asks to create a project spec or brief from notes, generate .cursorrules or context files, capture a coding session as Obsidian notes, create a runbook or session summary for Obsidian, generate QuickAdd templates for versioning, plan a coding session from Obsidian vault notes, bridge their knowledge base to their coding workflow, or any task combining Obsidian note-taking with AI-assisted coding tools."
---

# Obsidian Vibe Flow

Bridge Obsidian thinking with vibe coding execution. Plan in Obsidian, code in Cursor/Antigravity, capture everything back.

## The Loop

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   OBSIDIAN   │────▶│  VIBE CODE       │────▶│  CAPTURE BACK   │
│   Plan/Think │     │  Cursor/AGY/VSC  │     │  to Obsidian    │
└──────┬───────┘     └──────────────────┘     └────────┬────────┘
       │                                               │
       └───────────────── VERSION ◀────────────────────┘
                      (QuickAdd)
```

**Four phases, each with concrete outputs:**

1. **Plan** → Obsidian notes become coding specs and .cursorrules
2. **Code** → Vibe code with full context from your vault
3. **Capture** → Session summaries, runbooks, decision logs → Obsidian
4. **Version** → QuickAdd templates snapshot each iteration

## Phase 1: Plan — Obsidian to Coding Context

Transform Obsidian notes into structured context for vibe coding sessions.

### Generate a Project Brief

When the user has Obsidian notes (specs, ideas, requirements, architecture thoughts), generate a **project brief** optimized for AI coding tools:

```markdown
# Project Brief: [Name]

## Goal
[One sentence from user's notes]

## Tech Stack
[Extracted or confirmed with user]

## Features (Priority Order)
1. [Feature] — [acceptance criteria]
2. [Feature] — [acceptance criteria]

## Architecture Decisions
- [Decision]: [Rationale from notes]

## Constraints
- [Timeline, dependencies, limitations]

## Out of Scope
- [Explicitly excluded items]
```

Save as `project-brief.md` in the project root.

### Generate .cursorrules

Create a `.cursorrules` file from the user's Obsidian notes about their project conventions, tech stack, and preferences:

```
You are working on [Project Name].

## Tech Stack
- [Framework/Language/Tools]

## Project Structure
[Directory layout]

## Conventions
- [Naming conventions from user's notes]
- [Code style preferences]
- [Testing approach]

## Context
[Key architecture decisions and rationale]

## What NOT to do
- [Anti-patterns the user wants avoided]
```

### Generate Antigravity Skills

For Antigravity users, generate skill files (`.skill.md`) that follow the Antigravity progressive disclosure format:

```markdown
---
name: [project-context]
description: [When this skill applies]
---

# [Project] Context

[Instructions for the Antigravity agent about this specific project]
```

## Phase 2: Code — Context-Aware Vibe Coding

During coding, the user works in Cursor/Antigravity/VS Code. This phase is about providing the right context documents.

### Context Documents

Generate these files at the project root when starting a session:

**`CONTEXT.md`** — Living project context for AI tools:
```markdown
# Session Context

## Current Sprint/Focus
[What the user is working on now]

## Recent Changes
[Summary of last session's work]

## Open Questions
[Decisions pending]

## Known Issues
[Bugs or tech debt from previous sessions]
```

**`TODO.md`** — Structured task list the AI agent can reference:
```markdown
# TODO

## In Progress
- [ ] [Task] — [details]

## Up Next
- [ ] [Task] — [details]

## Backlog
- [ ] [Task] — [details]

## Done (this session)
- [x] [Task] — [details]
```

## Phase 3: Capture — Coding Session to Obsidian

This is the most important automation. After a vibe coding session, generate Obsidian-formatted notes.

### Session Summary Note

Generate with the `generate_session_notes.py` script or manually structure as:

```markdown
---
type: session-log
project: "[[Project Name]]"
date: {{date}}
session: {{session_number}}
tools: [cursor, antigravity]
tags:
  - vibe-coding
  - session-log
---

# Session {{session_number}} — {{date}}

## What I Built
[Bullet summary of features/changes implemented]

## Decisions Made
| Decision | Rationale | Alternatives Considered |
|----------|-----------|------------------------|
| [Decision] | [Why] | [What else was considered] |

## Architecture Changes
[Any structural changes to the codebase]

## Prompts That Worked
> [Effective prompts worth reusing]

## Issues Encountered
- [Issue] → [Resolution or workaround]

## Tech Debt Introduced
- [ ] [Item that needs cleanup later]

## Next Session
- [ ] [What to tackle next]

## Files Changed
[Key files added/modified/deleted]
```

### Runbook

Generate a runbook documenting how to run, test, and deploy the current state:

```markdown
---
type: runbook
project: "[[Project Name]]"
version: "{{version}}"
updated: {{date}}
tags:
  - runbook
  - ops
---

# Runbook — {{Project Name}} v{{version}}

## Quick Start
```bash
[Commands to get running]
```

## Environment Setup
[Prerequisites, env vars, dependencies]

## Development
```bash
[Dev server, hot reload, etc.]
```

## Testing
```bash
[How to run tests]
```

## Build & Deploy
```bash
[Build and deployment steps]
```

## Troubleshooting
| Problem | Solution |
|---------|----------|
| [Common issue] | [Fix] |

## Architecture Overview
[Brief structural description, key files]
```

### Decision Log Entry

For significant decisions, generate a standalone decision record:

```markdown
---
type: decision
project: "[[Project Name]]"
date: {{date}}
status: accepted
tags:
  - decision
  - architecture
---

# ADR: [Decision Title]

## Context
[What prompted this decision]

## Decision
[What was decided]

## Rationale
[Why this choice over alternatives]

## Consequences
- **Positive:** [Benefits]
- **Negative:** [Tradeoffs]
- **Risks:** [What could go wrong]

## Alternatives Considered
1. [Alternative] — [Why rejected]
2. [Alternative] — [Why rejected]
```

## Phase 4: Version — QuickAdd Templates

Generate QuickAdd-compatible templates for Obsidian that make capture fast and consistent.

### QuickAdd Capture Template: Session Log

For QuickAdd's Capture type, create a template the user can trigger after each coding session:

**Template file:** `Templates/Session Log.md`

See [assets/templates/session-log.md](assets/templates/session-log.md) for the ready-to-use template.

### QuickAdd Capture Template: Version Snapshot

For versioning milestones — a snapshot of what the project looks like at a specific point:

**Template file:** `Templates/Version Snapshot.md`

See [assets/templates/version-snapshot.md](assets/templates/version-snapshot.md) for the ready-to-use template.

### QuickAdd Macro: New Coding Session

Create a QuickAdd Macro that chains:
1. Creates a new session log note from template
2. Increments the session counter
3. Opens the note for editing

See [references/quickadd-patterns.md](references/quickadd-patterns.md) for the JavaScript macro script.

### QuickAdd Macro: Version Bump

Create a QuickAdd Macro that:
1. Prompts for version number
2. Creates version snapshot note
3. Links to the latest session logs since last version
4. Tags as a milestone

See [references/quickadd-patterns.md](references/quickadd-patterns.md) for implementation.

## Generating Output Files

### For Obsidian Notes

Use the session notes generator for consistent output:

```bash
python scripts/generate_session_notes.py \
  --project "My Project" \
  --session 5 \
  --type session-log \
  --output ./output
```

Supported types: `session-log`, `runbook`, `decision`, `version-snapshot`

### For Cursor/Antigravity Context

```bash
python scripts/generate_cursor_context.py \
  --project "My Project" \
  --stack "Next.js, TypeScript, Prisma" \
  --output ./project-root
```

### For QuickAdd Templates

```bash
python scripts/generate_quickadd_templates.py \
  --vault-path "~/ObsidianVault" \
  --project "My Project"
```

## Obsidian Folder Structure

Recommended vault structure for vibe coding projects:

```
Vault/
├── Projects/
│   └── Project Name/
│       ├── 00-Brief.md          ← Project brief
│       ├── 01-Architecture.md   ← Architecture decisions
│       ├── Sessions/
│       │   ├── Session-001.md
│       │   ├── Session-002.md
│       │   └── ...
│       ├── Runbooks/
│       │   └── Runbook-v1.0.md
│       ├── Decisions/
│       │   ├── ADR-001.md
│       │   └── ADR-002.md
│       └── Versions/
│           ├── v0.1.0.md
│           └── v0.2.0.md
├── Templates/
│   ├── Session Log.md
│   ├── Runbook.md
│   ├── Decision Record.md
│   └── Version Snapshot.md
└── QuickAdd/
    └── scripts/
        ├── new-session.js
        └── version-bump.js
```

## Dataview Queries

For users with the Dataview plugin, include these queries in a project dashboard:

**Recent Sessions:**
````markdown
```dataview
TABLE date, session as "Session #"
FROM "Projects/My Project/Sessions"
WHERE type = "session-log"
SORT date DESC
LIMIT 10
```
````

**Open Tech Debt:**
````markdown
```dataview
TASK
FROM "Projects/My Project/Sessions"
WHERE !completed AND contains(text, "tech debt")
```
````

**Decision Timeline:**
````markdown
```dataview
TABLE date, status
FROM "Projects/My Project/Decisions"
SORT date ASC
```
````

## Formatting Rules

All generated Obsidian notes must follow these conventions:

- **YAML frontmatter** on every note with `type`, `project`, `date`, `tags`
- **Wikilinks** for cross-references: `[[Project Name]]`, `[[Session-001]]`
- **Tags** as YAML arrays, not inline hashtags
- **ISO dates** in frontmatter: `2026-02-02`
- **Human dates** in headings: `February 2, 2026`
- **Checkboxes** for actionable items: `- [ ]` and `- [x]`
