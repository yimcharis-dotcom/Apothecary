# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is **Apothecary**, an Obsidian vault designed as a comprehensive workspace for AI tool management, prompt engineering, automation, and knowledge management. The vault follows a structured 4-stage pipeline workflow and serves as a central hub for Claude Code skills, automation scripts, and AI tool tracking.

## Core Architecture

### Folder Structure Philosophy

The vault follows a **4-stage pipeline** for content development:

1. **40_Experiments/** - Early development and testing (0-60 day lifespan)
2. **30_Automation/** / **30_Projects/** - Active refinement workspace (0-14 day lifespan)
3. **10_Prompt library/** - Production-ready, tested prompts (canonical sources)
4. **00_System/** - Infrastructure and deployed configurations (read-only targets)

**Critical Rule**: NEVER edit `00_System/` files directly. Always copy to Projects/Experiments, revise, then redeploy. This prevents breaking production configurations.

### Key Directory Purposes

- **00_System/003_Skills/** - Claude Code skills (custom + Codex system skills)
  - Contains both skill source directories and packaged `.skill` files
  - Skills use SKILL.md frontmatter + scripts/ + references/ + assets/ structure
  - Codex skills marked with `.codex-system-skills.marker` file

- **00_System/002_Espanso/** - Text expansion snippet configurations
  - YAML snippets for Espanso text expander
  - Location: `C:\Users\YC\AppData\Roaming\espanso\match\`

- **30_Automation/** - Active automation projects:
  - `303_AI_HubWatch` - PowerShell watcher + Python dashboard for AI tool inventory
  - `301_hkex_Daily_quote` - Playwright-based stock quote automation
  - `300_HKICPA-Download-Automation` - Document download automation

- **10_Prompt library/** - Organized by category (Accounting, AI_Development, Grammar, etc.)

- **99_env/** - API keys and environment configurations (NOT committed to git)
  - Contains connection info for Claude API, Deepseek, Grok, OpenRouter, etc.

- **99_Reference/** - External documentation and guides (read-only)

## Technology Stack

### Python
- **Primary use**: Automation scripts, data collection, OAuth management
- **Common libraries**: google-auth, google-api-python-client, streamlit, pandas, plotly
- **Install dependencies**: `pip install -r requirements.txt` (found in project subdirectories)

### PowerShell
- **Primary use**: Windows automation, file system watching, AI tool tracking
- **Key scripts**: `WatchHub_Realtime.ps1`, `TrackInstallation.ps1`, `SyncSkills.ps1`
- **Location**: `30_Automation/303_AI_HubWatch - Automation/src_v2/`

### Playwright
- **Primary use**: Browser automation for data scraping (HKEX quotes)
- **Setup**: Install via `pip install playwright` then `playwright install`

## Common Development Tasks

### Working with Claude Code Skills

**Creating a new skill:**
```bash
# Use the skill-builder skill (if available)
# Or manually create structure:
mkdir -p "00_System/003_Skills/skill-name/{scripts,references,assets}"
# Create SKILL.md with proper frontmatter
```

**Validating a skill:**
```bash
python "00_System/003_Skills/Claude/skill-builder/scripts/validate_skill.py" path/to/skill/
```

**Packaging a skill:**
```bash
python "00_System/003_Skills/Claude/skill-builder/scripts/package_skill.py" path/to/skill/
# Creates a .skill file for distribution
```

### Working with AI_HubWatch Automation

**Running the file watcher:**
```powershell
cd "30_Automation/303_AI_HubWatch - Automation/src_v2"
.\WatchHub_Realtime.ps1
```

**Scanning Gmail OAuth connections:**
```bash
cd "30_Automation/303_AI_HubWatch - Automation/dashboard"
python collectors/scan_gmail_oauth.py
# Outputs gmail_connections.json and oauth_connections_table.csv
```

**Installing dashboard dependencies:**
```bash
cd "30_Automation/303_AI_HubWatch - Automation/dashboard"
pip install -r requirements.txt
```

### Working with Espanso Snippets

**Snippet file location**: `C:\Users\YC\AppData\Roaming\espanso\match\`

**After editing snippets in vault:**
1. Copy from `00_System/002_Espanso/` to Espanso match directory
2. Restart Espanso or reload configuration

## Git Workflow

- **Main branch**: `main` (use for pull requests)
- **Current branch**: Check with `git branch --show-current`
- **Staging changes**: Prefer staging specific files over `git add -A` to avoid committing sensitive files
- **Commit messages**: Follow existing style (imperative, descriptive)

**Files to NEVER commit**:
- API keys in `99_env/` (already in .gitignore)
- `.obsidian/workspace.json` and similar session files (already ignored)
- Large binary files or vector databases (`.tar.gz` files)

## Project-Specific Notes

### AI_HubWatch Dashboard

**Purpose**: Track all AI tools installed on Windows, monitor OAuth connections, visualize relationships

**Current state**:
- ✅ Gmail OAuth scanner implemented
- ✅ PowerShell file watcher working
- ⏳ Dashboard UI (Streamlit) planned but not built
- ⏳ Windows app scanner, config hunter, data merger not yet implemented

**Data schema**: See `30_Automation/303_AI_HubWatch - Automation/dashboard/CLAUDE.md` for detailed inventory structure

**AI Hub location**: `%USERPROFILE%\AI_hub` (uses junctions/symlinks to track tools)

### Skills Architecture

**Skill structure**:
```
skill-name/
├── SKILL.md              # Main documentation with YAML frontmatter
├── scripts/              # Executable scripts (Python, PowerShell, Bash)
├── references/           # Documentation read into context
└── assets/               # Templates, images (not read into context)
```

**Skill frontmatter fields**:
- `name`: Display name
- `description`: Brief (1-2 sentences) usage trigger description
- `author`, `version`, `license`: Metadata
- `requirements`: Dependencies needed

**Skill development guide**: See `00_System/003_Skills/claude-skill-creation-guide.md` for complete methodology

## Obsidian Integration Notes

- **Community plugins**: Managed in `.obsidian/community-plugins.json`
- **CSS snippets**: In `.obsidian/snippets/` (e.g., `compact-reading.css`)
- **Templates**: In `__Templates/` directory
- **Dataview queries**: Used for dashboards in Library index files

## Important Conventions

1. **No direct System edits**: Always copy → revise → redeploy
2. **Lifespan awareness**: Projects folders are temporary staging areas, not storage
3. **Canonical sources**: Library files are the source of truth, System files are deployed copies
4. **File linking**: Use relative Obsidian `[[wikilinks]]` for cross-references
5. **Prefixes**: Folders use numeric prefixes (00_, 10_, 30_, etc.) for sort order
6. **Underscores**: Special folders like `__Templates/` and `__automation scripts/` use double underscores

## Automation Script Locations

- **HKEX quotes**: `30_Automation/301_hkex_Daily_quote/scr/`
- **HKICPA downloads**: `30_Automation/300_HKICPA-Download-Automation/python-scripts/`
- **AI_HubWatch**: `30_Automation/303_AI_HubWatch - Automation/`
  - PowerShell scripts: `src_v2/`
  - Python collectors: `dashboard/collectors/`
- **General automation**: `__automation scripts/`

## Testing Commands

Since this is primarily a knowledge management vault (not a software project), traditional testing commands don't apply. However:

**For Python scripts:**
```bash
# Run script directly (most automation scripts are standalone)
python path/to/script.py
```

**For PowerShell scripts:**
```powershell
# Execute with appropriate execution policy
powershell -ExecutionPolicy Bypass -File script.ps1
```

**For Playwright scripts:**
```bash
playwright test  # If test files exist
python script.py  # For standalone Playwright scripts
```

## File Permissions & Sensitive Data

- **Environment files** in `99_env/` contain API credentials - handle with care
- **Home.md** contains Gmail bearer token example - do not commit real tokens
- **.gitignore** already excludes workspace files, data.json, and archives
- **OAuth tokens**: Managed by Python scripts in `dashboard/data/` directory

## References

- **Claude Code skill development**: `00_System/003_Skills/claude-skill-creation-guide.md`
- **Folder structure definitions**: `00_System/009_Folder Structure & Definitions/Folder Structure & Definitions.md`
- **AI_HubWatch architecture**: `30_Automation/303_AI_HubWatch - Automation/dashboard/CLAUDE.md`
- **Obsidian setup**: `99_env/Obsidian setup spec.md`
