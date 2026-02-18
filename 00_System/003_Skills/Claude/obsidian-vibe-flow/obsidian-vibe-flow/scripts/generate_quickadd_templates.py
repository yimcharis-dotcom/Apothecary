#!/usr/bin/env python3
"""
Generate QuickAdd-compatible templates and scripts for Obsidian.

Creates template files and JavaScript macro scripts that can be used
with the Obsidian QuickAdd plugin for fast session capture and versioning.

Usage:
    python generate_quickadd_templates.py --project "Name" --output ./vault-templates
    python generate_quickadd_templates.py --project "Name" --output ./vault --include-macros

Arguments:
    --project         Project name
    --output          Output directory (your vault's Templates folder)
    --include-macros  Also generate QuickAdd JS macro scripts
"""

import argparse
import sys
from pathlib import Path


def generate_session_log_template(project: str) -> str:
    """Generate QuickAdd capture template for session logs."""
    
    # QuickAdd uses {{VALUE}} and {{DATE}} syntax
    return f"""---
type: session-log
project: "[[{project}]]"
date: {{{{DATE:YYYY-MM-DD}}}}
session: {{{{VALUE:Session number}}}}
tools: [{{{{VALUE:Tools used (cursor, antigravity, vscode)}}}}]
tags:
  - vibe-coding
  - session-log
  - {project.lower().replace(' ', '-')}
---

# Session {{{{VALUE:Session number}}}} — {{{{DATE:MMMM DD, YYYY}}}}

## What I Built
- {{{{VALUE:What did you build?}}}}

## Decisions Made

| Decision | Rationale | Alternatives |
|----------|-----------|-------------|
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


def generate_runbook_template(project: str) -> str:
    """Generate QuickAdd capture template for runbooks."""
    
    return f"""---
type: runbook
project: "[[{project}]]"
version: "{{{{VALUE:Version (e.g., 1.0.0)}}}}"
updated: {{{{DATE:YYYY-MM-DD}}}}
tags:
  - runbook
  - ops
  - {project.lower().replace(' ', '-')}
---

# Runbook — {project} v{{{{VALUE:Version (e.g., 1.0.0)}}}}

## Quick Start

```bash
{{{{VALUE:Quick start commands}}}}
```

## Environment Setup

{{{{VALUE:Prerequisites and setup steps}}}}

## Development

```bash
{{{{VALUE:Dev commands}}}}
```

## Testing

```bash
{{{{VALUE:Test commands}}}}
```

## Build & Deploy

```bash
{{{{VALUE:Build/deploy commands}}}}
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
|  |  |

## Architecture Overview


## Key Files

| File | Purpose |
|------|---------|
|  |  |
"""


def generate_decision_template(project: str) -> str:
    """Generate QuickAdd capture template for decision records."""
    
    return f"""---
type: decision
project: "[[{project}]]"
date: {{{{DATE:YYYY-MM-DD}}}}
status: {{{{VALUE:Status (accepted, proposed, deprecated)}}}}
tags:
  - decision
  - architecture
  - {project.lower().replace(' ', '-')}
---

# ADR: {{{{VALUE:Decision title}}}}

**Date:** {{{{DATE:MMMM DD, YYYY}}}}
**Status:** {{{{VALUE:Status (accepted, proposed, deprecated)}}}}
**Project:** [[{project}]]

## Context

{{{{VALUE:What prompted this decision?}}}}

## Decision

{{{{VALUE:What was decided?}}}}

## Rationale

{{{{VALUE:Why this choice?}}}}

## Consequences

**Positive:**
- 

**Negative:**
- 

## Alternatives Considered

1. {{{{VALUE:Alternative considered}}}} — [Why rejected]
"""


def generate_version_snapshot_template(project: str) -> str:
    """Generate QuickAdd capture template for version snapshots."""
    
    return f"""---
type: version-snapshot
project: "[[{project}]]"
version: "{{{{VALUE:Version (e.g., 0.2.0)}}}}"
date: {{{{DATE:YYYY-MM-DD}}}}
tags:
  - version
  - milestone
  - {project.lower().replace(' ', '-')}
---

# {project} — v{{{{VALUE:Version (e.g., 0.2.0)}}}}

**Released:** {{{{DATE:MMMM DD, YYYY}}}}

## Summary

{{{{VALUE:One-line summary of this version}}}}

## What's New

### Features
- {{{{VALUE:New features}}}}

### Improvements
- 

### Bug Fixes
- 

## Breaking Changes
- None

## Sessions Since Last Version
- [[Session-]]

## Decisions Made
- [[ADR-]]

## Known Issues
- [ ] 

## Next Version Goals
- [ ] 
"""


def generate_new_session_macro(project: str) -> str:
    """Generate QuickAdd JavaScript macro for creating new sessions."""
    
    slug = project.lower().replace(' ', '-')
    
    return f"""/**
 * QuickAdd Macro: New Coding Session
 * 
 * Creates a new session log note with auto-incremented session number.
 * 
 * Setup in QuickAdd:
 * 1. Create a new Macro
 * 2. Add a "User Script" step pointing to this file
 * 3. Assign a hotkey or command palette trigger
 */

module.exports = async (params) => {{
    const {{ app, quickAddApi }} = params;
    
    // Find the project sessions folder
    const sessionsFolder = "Projects/{project}/Sessions";
    
    // Get existing session files to determine next number
    const folder = app.vault.getAbstractFileByPath(sessionsFolder);
    let nextSession = 1;
    
    if (folder && folder.children) {{
        const sessionFiles = folder.children
            .filter(f => f.name.startsWith("Session-"))
            .map(f => {{
                const match = f.name.match(/Session-(\\d+)/);
                return match ? parseInt(match[1]) : 0;
            }})
            .filter(n => n > 0);
        
        if (sessionFiles.length > 0) {{
            nextSession = Math.max(...sessionFiles) + 1;
        }}
    }}
    
    // Pad session number
    const sessionNum = String(nextSession).padStart(3, '0');
    const today = new Date();
    const dateISO = today.toISOString().split('T')[0];
    const dateHuman = today.toLocaleDateString('en-US', {{
        year: 'numeric', month: 'long', day: 'numeric'
    }});
    
    // Ask for tools being used
    const tools = await quickAddApi.inputPrompt(
        "Tools for this session?",
        "cursor, antigravity",
        "cursor"
    );
    
    // Create the note content
    const content = `---
type: session-log
project: "[[{project}]]"
date: ${{dateISO}}
session: ${{nextSession}}
tools: [${{tools || 'cursor'}}]
tags:
  - vibe-coding
  - session-log
  - {slug}
---

# Session ${{sessionNum}} — ${{dateHuman}}

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

`;
    
    // Create the file
    const filePath = `${{sessionsFolder}}/Session-${{sessionNum}}.md`;
    
    // Ensure folder exists
    if (!app.vault.getAbstractFileByPath(sessionsFolder)) {{
        await app.vault.createFolder(sessionsFolder);
    }}
    
    const file = await app.vault.create(filePath, content);
    
    // Open the new note
    const leaf = app.workspace.getLeaf(false);
    await leaf.openFile(file);
    
    new Notice(`✅ Created Session ${{sessionNum}} for {project}`);
}};
"""


def generate_version_bump_macro(project: str) -> str:
    """Generate QuickAdd JavaScript macro for version snapshots."""
    
    slug = project.lower().replace(' ', '-')
    
    return f"""/**
 * QuickAdd Macro: Version Bump
 * 
 * Creates a version snapshot note and links recent sessions.
 * 
 * Setup in QuickAdd:
 * 1. Create a new Macro
 * 2. Add a "User Script" step pointing to this file
 * 3. Assign a hotkey or command palette trigger
 */

module.exports = async (params) => {{
    const {{ app, quickAddApi }} = params;
    
    // Ask for version number
    const version = await quickAddApi.inputPrompt(
        "Version number?",
        "e.g., 0.2.0"
    );
    
    if (!version) {{
        new Notice("❌ Version number required");
        return;
    }}
    
    // Ask for summary
    const summary = await quickAddApi.inputPrompt(
        "One-line version summary?",
        "e.g., Added user authentication and dashboard"
    );
    
    const today = new Date();
    const dateISO = today.toISOString().split('T')[0];
    const dateHuman = today.toLocaleDateString('en-US', {{
        year: 'numeric', month: 'long', day: 'numeric'
    }});
    
    // Find recent sessions since last version
    const versionsFolder = "Projects/{project}/Versions";
    const sessionsFolder = "Projects/{project}/Sessions";
    
    let recentSessions = "";
    const sessionFolder = app.vault.getAbstractFileByPath(sessionsFolder);
    if (sessionFolder && sessionFolder.children) {{
        const sessions = sessionFolder.children
            .filter(f => f.name.startsWith("Session-"))
            .sort((a, b) => b.name.localeCompare(a.name))
            .slice(0, 10);  // Last 10 sessions
        
        recentSessions = sessions
            .map(f => `- [[${{f.name.replace('.md', '')}}]]`)
            .join('\\n');
    }}
    
    if (!recentSessions) {{
        recentSessions = "- [[Session-XXX]]";
    }}
    
    // Create version snapshot content
    const content = `---
type: version-snapshot
project: "[[{project}]]"
version: "${{version}}"
date: ${{dateISO}}
tags:
  - version
  - milestone
  - {slug}
---

# {project} — v${{version}}

**Released:** ${{dateHuman}}

## Summary

${{summary || '[Version summary]'}}

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

${{recentSessions}}

## Decisions Made

- [[ADR-]]

## Known Issues

- [ ] 

## Metrics

| Metric | Value |
|--------|-------|
| Total files | |
| Lines of code | |
| Test coverage | |

## Runbook

See [[Runbook-v${{version}}]] for setup and deployment instructions.

## Next Version Goals

- [ ] 
`;
    
    // Create the file
    const filePath = `${{versionsFolder}}/v${{version}}.md`;
    
    // Ensure folder exists
    if (!app.vault.getAbstractFileByPath(versionsFolder)) {{
        await app.vault.createFolder(versionsFolder);
    }}
    
    const file = await app.vault.create(filePath, content);
    
    // Open the new note
    const leaf = app.workspace.getLeaf(false);
    await leaf.openFile(file);
    
    new Notice(`✅ Created version snapshot v${{version}} for {project}`);
}};
"""


def main():
    parser = argparse.ArgumentParser(
        description="Generate QuickAdd templates and macros for Obsidian",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("--project", required=True, help="Project name")
    parser.add_argument("--output", required=True,
                       help="Output directory (vault Templates folder)")
    parser.add_argument("--include-macros", action="store_true",
                       help="Also generate JavaScript macro scripts")
    
    args = parser.parse_args()
    
    output_dir = Path(args.output)
    
    # Create Templates directory
    templates_dir = output_dir / "Templates"
    templates_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate templates
    templates = {
        "Session Log.md": generate_session_log_template(args.project),
        "Runbook.md": generate_runbook_template(args.project),
        "Decision Record.md": generate_decision_template(args.project),
        "Version Snapshot.md": generate_version_snapshot_template(args.project),
    }
    
    for filename, content in templates.items():
        (templates_dir / filename).write_text(content)
        print(f"✅ Generated template: Templates/{filename}")
    
    # Generate macros if requested
    if args.include_macros:
        macros_dir = output_dir / "QuickAdd" / "scripts"
        macros_dir.mkdir(parents=True, exist_ok=True)
        
        macros = {
            "new-session.js": generate_new_session_macro(args.project),
            "version-bump.js": generate_version_bump_macro(args.project),
        }
        
        for filename, content in macros.items():
            (macros_dir / filename).write_text(content)
            print(f"✅ Generated macro: QuickAdd/scripts/{filename}")
    
    # Create project folder structure
    project_dir = output_dir / "Projects" / args.project
    for subfolder in ["Sessions", "Runbooks", "Decisions", "Versions"]:
        (project_dir / subfolder).mkdir(parents=True, exist_ok=True)
    
    # Create project index note
    index_content = f"""---
type: project
project: "{args.project}"
tags:
  - project
  - {args.project.lower().replace(' ', '-')}
---

# {args.project}

## Overview

[Project description]

## Quick Links

- **Sessions:** [[Sessions/]]
- **Runbooks:** [[Runbooks/]]
- **Decisions:** [[Decisions/]]
- **Versions:** [[Versions/]]

## Current Status

[What's happening now]

## Recent Sessions

```dataview
TABLE date, session as "#"
FROM "Projects/{args.project}/Sessions"
WHERE type = "session-log"
SORT date DESC
LIMIT 5
```

## Versions

```dataview
TABLE version, date
FROM "Projects/{args.project}/Versions"
WHERE type = "version-snapshot"
SORT date DESC
```

## Open Tech Debt

```dataview
TASK
FROM "Projects/{args.project}/Sessions"
WHERE !completed AND contains(text, "tech debt")
```
"""
    
    (project_dir / f"{args.project}.md").write_text(index_content)
    print(f"✅ Generated project index: Projects/{args.project}/{args.project}.md")
    print(f"✅ Created folder structure: Projects/{args.project}/[Sessions|Runbooks|Decisions|Versions]")
    
    print(f"\n✅ All QuickAdd files generated in: {output_dir}")
    print("\nSetup instructions:")
    print("1. Copy the Templates/ folder contents to your vault's Templates folder")
    print("2. In QuickAdd settings, create Capture choices pointing to each template")
    if args.include_macros:
        print("3. Copy QuickAdd/scripts/ to your vault")
        print("4. In QuickAdd, create Macros pointing to each .js file")
    print(f"5. The project folder structure is ready at Projects/{args.project}/")


if __name__ == "__main__":
    main()
