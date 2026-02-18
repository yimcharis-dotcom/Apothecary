#!/usr/bin/env python3
"""
Generate Obsidian-formatted session notes from coding session data.

Creates properly formatted Obsidian markdown notes with YAML frontmatter,
wikilinks, tags, and structured content for different note types.

Usage:
    python generate_session_notes.py --project "Name" --session 5 --type session-log --output ./
    python generate_session_notes.py --project "Name" --type runbook --version "1.0.0" --output ./
    python generate_session_notes.py --project "Name" --type decision --title "Use Prisma" --output ./
    python generate_session_notes.py --project "Name" --type version-snapshot --version "0.2.0" --output ./

Arguments:
    --project       Project name (used in frontmatter and wikilinks)
    --type          Note type: session-log, runbook, decision, version-snapshot
    --session       Session number (for session-log type)
    --version       Version string (for runbook and version-snapshot types)
    --title         Decision title (for decision type)
    --tools         Comma-separated tools used (default: cursor)
    --stack         Tech stack (for runbook type)
    --output        Output directory
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime


def get_today() -> str:
    """Get today's date in ISO format."""
    return datetime.now().strftime("%Y-%m-%d")


def get_today_human() -> str:
    """Get today's date in human-readable format."""
    return datetime.now().strftime("%B %d, %Y")


def generate_session_log(project: str, session: int, tools: list) -> tuple[str, str]:
    """Generate a session log note."""
    date = get_today()
    date_human = get_today_human()
    tools_yaml = ", ".join(tools)
    
    content = f"""---
type: session-log
project: "[[{project}]]"
date: {date}
session: {session}
tools: [{tools_yaml}]
tags:
  - vibe-coding
  - session-log
  - {project.lower().replace(' ', '-')}
---

# Session {session:03d} — {date_human}

## What I Built
- 

## Decisions Made

| Decision | Rationale | Alternatives Considered |
|----------|-----------|------------------------|
|  |  |  |

## Architecture Changes


## Prompts That Worked
> 

## Issues Encountered
- 

## Tech Debt Introduced
- [ ] 

## Next Session
- [ ] 

## Files Changed

"""
    
    filename = f"Session-{session:03d}.md"
    return filename, content


def generate_runbook(project: str, version: str, stack: str = "") -> tuple[str, str]:
    """Generate a runbook note."""
    date = get_today()
    
    stack_section = ""
    if stack:
        stack_items = [s.strip() for s in stack.split(",")]
        stack_section = "\n".join(f"- {item}" for item in stack_items)
    else:
        stack_section = "- [List technologies here]"
    
    content = f"""---
type: runbook
project: "[[{project}]]"
version: "{version}"
updated: {date}
tags:
  - runbook
  - ops
  - {project.lower().replace(' ', '-')}
---

# Runbook — {project} v{version}

## Quick Start

```bash
# Clone and install
git clone [repo-url]
cd {project.lower().replace(' ', '-')}
npm install  # or pip install -r requirements.txt

# Run
npm run dev  # or python main.py
```

## Prerequisites

{stack_section}

## Environment Variables

```bash
# .env
# DATABASE_URL=
# API_KEY=
```

## Development

```bash
# Start dev server
npm run dev

# Run in watch mode
npm run dev -- --watch
```

## Testing

```bash
# Run all tests
npm test

# Run specific test
npm test -- --grep "feature name"
```

## Build & Deploy

```bash
# Build for production
npm run build

# Deploy
npm run deploy
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Port in use | `lsof -i :3000` then `kill -9 [PID]` |
| Deps out of sync | `rm -rf node_modules && npm install` |
|  |  |

## Architecture Overview

```
{project.lower().replace(' ', '-')}/
├── src/
│   ├── components/
│   ├── lib/
│   └── pages/
├── tests/
├── public/
└── config/
```

## Key Files

| File | Purpose |
|------|---------|
|  |  |
"""
    
    filename = f"Runbook-v{version}.md"
    return filename, content


def generate_decision(project: str, title: str) -> tuple[str, str]:
    """Generate an architecture decision record."""
    date = get_today()
    date_human = get_today_human()
    
    # Generate ADR number from title hash (simple approach)
    adr_num = abs(hash(title + date)) % 1000
    
    slug = title.lower().replace(' ', '-')[:40]
    
    content = f"""---
type: decision
project: "[[{project}]]"
date: {date}
status: accepted
tags:
  - decision
  - architecture
  - {project.lower().replace(' ', '-')}
---

# ADR-{adr_num:03d}: {title}

**Date:** {date_human}
**Status:** Accepted
**Project:** [[{project}]]

## Context

[What problem or situation prompted this decision?]

## Decision

[What was decided?]

## Rationale

[Why this choice? What factors weighed most heavily?]

## Consequences

**Positive:**
- 

**Negative:**
- 

**Risks:**
- 

## Alternatives Considered

### Option A: [Name]
[Description and why it was rejected]

### Option B: [Name]
[Description and why it was rejected]

## Related
- [[Session-XXX]] — Session where this was discussed
"""
    
    filename = f"ADR-{adr_num:03d}-{slug}.md"
    return filename, content


def generate_version_snapshot(project: str, version: str) -> tuple[str, str]:
    """Generate a version snapshot note."""
    date = get_today()
    date_human = get_today_human()
    
    content = f"""---
type: version-snapshot
project: "[[{project}]]"
version: "{version}"
date: {date}
tags:
  - version
  - milestone
  - {project.lower().replace(' ', '-')}
---

# {project} — v{version}

**Released:** {date_human}

## Summary

[One paragraph describing what this version achieves]

## What's New

### Features
- 

### Improvements
- 

### Bug Fixes
- 

## Breaking Changes

- None

## Sessions Since Last Version

[Link to sessions that contributed to this version]
- [[Session-XXX]]

## Decisions Made

[Link to ADRs from this version cycle]
- [[ADR-XXX]]

## Known Issues

- [ ] 

## Metrics

| Metric | Value |
|--------|-------|
| Total files | |
| Lines of code | |
| Test coverage | |
| Dependencies | |

## Runbook

See [[Runbook-v{version}]] for setup and deployment instructions.

## Next Version Goals

- [ ] 
"""
    
    filename = f"v{version}.md"
    return filename, content


def main():
    parser = argparse.ArgumentParser(
        description="Generate Obsidian-formatted session notes",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("--project", required=True, help="Project name")
    parser.add_argument("--type", required=True,
                       choices=["session-log", "runbook", "decision", "version-snapshot"],
                       help="Type of note to generate")
    parser.add_argument("--session", type=int, help="Session number (for session-log)")
    parser.add_argument("--version", help="Version string (for runbook/version-snapshot)")
    parser.add_argument("--title", help="Decision title (for decision type)")
    parser.add_argument("--tools", default="cursor",
                       help="Comma-separated tools used (default: cursor)")
    parser.add_argument("--stack", default="",
                       help="Tech stack, comma-separated (for runbook)")
    parser.add_argument("--output", required=True, help="Output directory")
    
    args = parser.parse_args()
    
    # Validate required args per type
    if args.type == "session-log" and not args.session:
        print("❌ --session required for session-log type")
        sys.exit(1)
    if args.type in ("runbook", "version-snapshot") and not args.version:
        print(f"❌ --version required for {args.type} type")
        sys.exit(1)
    if args.type == "decision" and not args.title:
        print("❌ --title required for decision type")
        sys.exit(1)
    
    # Parse tools
    tools = [t.strip() for t in args.tools.split(",")]
    
    # Generate content
    generators = {
        "session-log": lambda: generate_session_log(args.project, args.session, tools),
        "runbook": lambda: generate_runbook(args.project, args.version, args.stack),
        "decision": lambda: generate_decision(args.project, args.title),
        "version-snapshot": lambda: generate_version_snapshot(args.project, args.version),
    }
    
    filename, content = generators[args.type]()
    
    # Write output
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_path = output_dir / filename
    output_path.write_text(content)
    
    print(f"✅ Generated {args.type}: {output_path}")
    print(f"   Project: {args.project}")
    if args.session:
        print(f"   Session: {args.session}")
    if args.version:
        print(f"   Version: {args.version}")


if __name__ == "__main__":
    main()
