#!/usr/bin/env python3
"""
Generate context files for Cursor, Antigravity, and VS Code from project info.

Creates .cursorrules, CONTEXT.md, TODO.md, and optional Antigravity skill files
that give AI coding tools full context about your project.

Usage:
    python generate_cursor_context.py --project "Name" --stack "Next.js, TS" --output ./project
    python generate_cursor_context.py --project "Name" --stack "Python, FastAPI" --output ./ --antigravity

Arguments:
    --project       Project name
    --stack         Tech stack, comma-separated
    --conventions   Coding conventions, comma-separated
    --output        Project root directory to write files into
    --description   Brief project description
    --antigravity   Also generate Antigravity skill files
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime


def generate_cursorrules(project: str, stack: list, conventions: list,
                         description: str = "") -> str:
    """Generate .cursorrules file content."""
    
    stack_section = "\n".join(f"- {item}" for item in stack)
    
    conventions_section = ""
    if conventions:
        conventions_section = "\n".join(f"- {c}" for c in conventions)
    else:
        conventions_section = """- Use descriptive variable and function names
- Write small, focused functions
- Add comments for non-obvious logic
- Handle errors explicitly"""
    
    desc_line = f"\n{description}\n" if description else "\n[Add project description]\n"
    
    return f"""You are working on {project}.
{desc_line}
## Tech Stack
{stack_section}

## Conventions
{conventions_section}

## Project Structure

Refer to the project's actual directory structure. Key patterns:
- Keep components small and focused
- Co-locate tests with source files when possible
- Use index files for clean imports

## What NOT to do
- Do not add dependencies without mentioning it
- Do not change the project structure without explaining why
- Do not write overly clever code — prefer readability
- Do not skip error handling
- Do not leave TODO comments without also noting them in TODO.md

## Context Files
- See CONTEXT.md for current session state and recent changes
- See TODO.md for the current task list
- See project-brief.md for the full project brief (if present)

## Communication
- When uncertain, ask before implementing
- Explain architectural decisions briefly
- Flag potential issues or tech debt proactively
"""


def generate_context_md(project: str) -> str:
    """Generate CONTEXT.md file content."""
    date = datetime.now().strftime("%Y-%m-%d")
    
    return f"""# Session Context — {project}

> Last updated: {date}

## Current Focus

[What you're working on this session]

## Recent Changes

[Summary of what changed in the last session]

## Open Questions

- [ ] [Decision that needs to be made]

## Known Issues

- [ ] [Bug or issue to be aware of]

## Architecture Notes

[Key patterns and decisions the AI should know about]
"""


def generate_todo_md(project: str) -> str:
    """Generate TODO.md file content."""
    
    return f"""# TODO — {project}

## 🔴 In Progress

- [ ] 

## 🟡 Up Next

- [ ] 

## 🔵 Backlog

- [ ] 

## ✅ Done (this session)

"""


def generate_antigravity_skill(project: str, stack: list,
                                description: str = "") -> str:
    """Generate an Antigravity skill file."""
    
    slug = project.lower().replace(' ', '-')
    stack_str = ", ".join(stack)
    desc = description or f"Context and conventions for the {project} project"
    
    return f"""---
name: {slug}-context
description: {desc}. Tech stack: {stack_str}. Use when working on any files in this project.
---

# {project} Context

## Tech Stack
{chr(10).join(f"- {s}" for s in stack)}

## Key Conventions
- Follow existing code patterns in the project
- Keep changes focused and atomic
- Update CONTEXT.md after significant changes
- Add new tasks to TODO.md

## File References
- `CONTEXT.md` — Current session state
- `TODO.md` — Task list
- `.cursorrules` — Coding conventions (also applies here)
"""


def main():
    parser = argparse.ArgumentParser(
        description="Generate context files for AI coding tools",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("--project", required=True, help="Project name")
    parser.add_argument("--stack", required=True,
                       help="Tech stack, comma-separated")
    parser.add_argument("--output", required=True,
                       help="Project root directory")
    parser.add_argument("--conventions", default="",
                       help="Coding conventions, comma-separated")
    parser.add_argument("--description", default="",
                       help="Brief project description")
    parser.add_argument("--antigravity", action="store_true",
                       help="Also generate Antigravity skill files")
    
    args = parser.parse_args()
    
    # Parse comma-separated values
    stack = [s.strip() for s in args.stack.split(",")]
    conventions = [c.strip() for c in args.conventions.split(",") if c.strip()]
    
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate .cursorrules
    cursorrules = generate_cursorrules(
        args.project, stack, conventions, args.description
    )
    (output_dir / ".cursorrules").write_text(cursorrules)
    print(f"✅ Generated .cursorrules")
    
    # Generate CONTEXT.md
    context = generate_context_md(args.project)
    (output_dir / "CONTEXT.md").write_text(context)
    print(f"✅ Generated CONTEXT.md")
    
    # Generate TODO.md
    todo = generate_todo_md(args.project)
    (output_dir / "TODO.md").write_text(todo)
    print(f"✅ Generated TODO.md")
    
    # Generate Antigravity skill if requested
    if args.antigravity:
        skill_dir = output_dir / ".antigravity" / "skills"
        skill_dir.mkdir(parents=True, exist_ok=True)
        
        skill_content = generate_antigravity_skill(
            args.project, stack, args.description
        )
        slug = args.project.lower().replace(' ', '-')
        (skill_dir / f"{slug}-context.skill.md").write_text(skill_content)
        print(f"✅ Generated Antigravity skill: .antigravity/skills/{slug}-context.skill.md")
    
    print(f"\n✅ All context files generated in: {output_dir}")
    print("\nFiles created:")
    print(f"  .cursorrules     — Cursor/AI coding conventions")
    print(f"  CONTEXT.md       — Session state (update each session)")
    print(f"  TODO.md          — Task tracking")
    if args.antigravity:
        print(f"  .antigravity/    — Antigravity skill files")


if __name__ == "__main__":
    main()
