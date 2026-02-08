# AI Ecosystem Dashboard Project

## Project Overview

This project creates a comprehensive dashboard to visualize and track all AI tools, services, and integrations installed on this Windows machine and connected to email/GitHub accounts.

**Goal**: Have a complete overview of what's installed locally, what's connected via OAuth, and how everything relates to each other (configs, skills, MCP servers, plugins).

## What We Want to Track

### 1. Local Installations

- AI applications (Claude Desktop, Cursor, VS Code, Windsurf, etc.)
- IDEs and editors with AI extensions
- CLI tools (npm global packages, pip packages, chocolatey packages)
- Local inference engines (Ollama, llama.cpp)
- MCP servers and their configurations
- Browser extensions

### 2. Cloud Services & OAuth Connections

- Services connected via Gmail OAuth (API grants, app permissions)
- Services connected via GitHub OAuth
- When they were authorized
- What scopes/permissions they have
- Not scraping Google Account Connections page (too manual/fragile)

### 3. Configuration Files & Storage Locations

- Config file paths for each tool (settings.json, config.json, etc.)
- Skills directories and where they're stored
- MCP server config files
- Plugin directories
- Workspace settings

### 4. Relationships

- Which apps use which services (e.g., "Claude Desktop uses Gmail OAuth")
- Which apps share skill directories
- Which MCP servers are used by which apps
- Installation dependencies

## Current State

### Status (as of 2026-02-07)

- ✅ Gmail OAuth scanner + CSV workflow implemented
- ✅ OAuth CSV import script implemented
- ❌ Google Account Connections scraping dropped
- ⏳ Other collectors (Windows apps, hub logs, config scan, merge) not built yet
- ⏳ Dashboard not built yet

### Existing Assets

**Documentation**:

- `C:\Vault\Apothecary\90_Inbox\Claude_AI_Ecosystem_Master_List.json` - Manual inventory of 100+ tools (comprehensive!)
- `C:\Vault\Apothecary\90_Inbox\Claude_AI_Ecosystem_Master_List.md` - Markdown version
- `C:\Vault\Apothecary\90_Inbox\Claude_AI_Ecosystem_Master_List (Excerpt).csv` - CSV export

**Automation**:

- `C:\Vault\Apothecary\30_Automation\303_AI_HubWatch - Automation\src_v2_refactor\` - Watcher scripts
  - `WatchHub_Realtime.ps1` - Real-time filesystem watcher (monitors for new AI tool installations)
  - `TrackInstallation.ps1` - Installation tracker
  - `SyncSkills.ps1` - Skills synchronization
  - `ExportToObsidian.ps1` - Export to Obsidian vault
  - `AIToolsConfig.ps1` - Shared configuration

**AI Hub**:

- Location: `%USERPROFILE%\AI_hub`
- Uses junction/symlinks to track installed tools
- Logs changes in `_Change_log` folder
- `discovery.log` - Master log of all tracked tools

### Current Watcher Script Capabilities

The existing `WatchHub_Realtime.ps1` already:

- ✅ Monitors multiple directories for new AI tool installations
- ✅ Creates junctions in AI_hub when new tools detected
- ✅ Logs all changes with timestamps
- ✅ Auto-syncs skills across agents
- ✅ Has debouncing (prevents duplicate events)
- ✅ Validates config files before adding
- ✅ Security checks for dangerous files
- ✅ Mutex locking (thread-safe)

**What needs improvement**:

- Extract tool metadata (name, version, paths) more reliably
- Better integration with the new dashboard system
- Export data in structured JSON format for dashboard consumption

## Planned Architecture

### Phase 1: Data Collection Scripts (Python)

**1. Gmail OAuth Scanner** (`scan_gmail_oauth.py`) ✅ Implemented

- Use Gmail API to list all authorized apps
- Extract: app name, scopes granted, authorization date, last used
- Output: `gmail_connections.json`
- Auto-export editable CSV table: `oauth_connections_table.csv`
- Import filled CSV back into JSON with: `import_oauth_connections_from_csv.py`
- Optional future: MCP Gmail connector (read-only) if a trusted server is available

**2. Windows App Scanner** (`scan_windows_apps.py`) ⏳ Planned

- Query Windows Registry (HKLM/HKCU Uninstall keys)
- Scan Program Files and AppData
- Check package managers: `npm list -g`, `pip list`, `choco list`
- Check browser extensions (Chrome, Edge)
- Output: `windows_apps.json`

**3. Hub Watcher Integration** (`scan_hub_logs.py`) ⏳ Planned

- Parse existing `AI_hub/_Change_log/*.txt` files
- Parse `AI_hub/discovery.log`
- Extract junction paths and their targets
- Output: `hub_junctions.json`

**4. Config Hunter** (`scan_configs.py`) ⏳ Planned

- Scan common config locations:
  - `%APPDATA%` (AppData\Roaming)
  - `%LOCALAPPDATA%` (AppData\Local)
  - `%USERPROFILE%` (user home directory)
- Find: config.json, settings.json, .config folders
- Identify MCP server configs
- Output: `config_files.json`

**5. Data Merger** (`merge_inventory.py`) ⏳ Planned

- Combine all JSON outputs
- Match local apps with OAuth connections
- Identify relationships
- Output: `master_inventory.json`

### Phase 2: Data Schema

```json
{
  "inventory": [
    {
      "id": "unique-uuid",
      "name": "Claude Desktop",
      "type": "local_app|oauth_service|extension|mcp_server|cli_tool",
      "provider": "Anthropic",
      "category": "Interface",
      "install_location": "C:\\Users\\...\\AppData\\Local\\Programs\\Claude",
      "config_paths": [
        "C:\\Users\\...\\AppData\\Roaming\\Claude\\config.json"
      ],
      "oauth_connected_via": ["gmail"],
      "oauth_scopes": ["email", "profile", "drive.readonly"],
      "oauth_grant_date": "2024-11-15",
      "hub_junction": "Claude_User_Dot",
      "skills_path": "C:\\Users\\...\\Claude\\skills",
      "mcp_servers": [
        {
          "name": "vault-bridge",
          "config": "C:\\Users\\...\\Claude\\mcp_config.json"
        }
      ],
      "last_detected": "2025-02-07",
      "status": "active|inactive|removed"
    }
  ],
  "relationships": [
    {
      "from_id": "uuid-claude-desktop",
      "to_id": "uuid-gmail",
      "type": "oauth",
      "details": "Uses Gmail OAuth for authentication"
    },
    {
      "from_id": "uuid-claude-desktop",
      "to_id": "uuid-mcp-vault",
      "type": "uses_mcp",
      "details": "Connects to Vault Bridge MCP server"
    }
  ],
  "metadata": {
    "last_scan": "2025-02-07T10:30:00",
    "total_apps": 0,
    "total_oauth_connections": 0,
    "total_config_files": 0
  }
}
```

### Phase 3: Dashboard (Python + Streamlit)

**Dashboard Tabs**:

1. **Overview**
   - Total apps count (local + cloud)
   - OAuth connections count
   - Config files tracked
   - Interactive network graph showing relationships

2. **Apps Inventory**
   - Searchable/filterable table
   - Columns: Name, Type, Provider, Install Path, Status
   - Click to see details (configs, skills, MCPs)

3. **OAuth Connections**
   - Gmail authorized apps with scopes
   - GitHub authorized apps
   - Authorization dates and last used
   - Revoke links (to Gmail/GitHub settings)

4. **Config Map**
   - Visual tree of config file locations
   - Skills directories
   - MCP server configs
   - Plugin directories

5. **Hub Monitor**
   - Live view of AI Hub junctions
   - Recent changes from watcher logs
   - Skills sync status
   - Junction health check

6. **Relationship Graph**
   - Interactive D3.js/Plotly network visualization
   - Nodes: Apps, Services, Configs, MCPs
   - Edges: OAuth, Uses, Stores, Connects

## Technical Decisions

### Why Streamlit?

- Fast to build (vs React/Vue web app)
- Python-based (good for system scanning scripts)
- Interactive widgets out of the box
- Can run locally, no deployment needed
- Alternative: Could also export to Obsidian Dataview if preferred

### File Structure

```
C:\Vault\Apothecary\30_Automation\303_AI_HubWatch - Automation\
├── CLAUDE.md (this file)
├── src_v2_refactor/
│   ├── WatchHub_Realtime.ps1 (existing watcher)
│   ├── AIToolsConfig.ps1 (shared config)
│   └── ... (other existing scripts)
├── dashboard/
│   ├── collectors/
│   │   ├── scan_gmail_oauth.py
│   │   ├── import_oauth_connections_from_csv.py
│   ├── data/
│   │   ├── gmail_connections.json
│   │   ├── oauth_connections_table.csv
│   │   └── gmail_connections_template.json
│   ├── dashboard.py (Streamlit app, planned)
│   └── requirements.txt
└── README.md (usage instructions)
```

### Dependencies

**Python Packages** (requirements.txt):

```
streamlit
google-auth
google-auth-oauthlib
google-api-python-client
pandas
plotly
networkx
```

**Windows PowerShell** (already available):

- For registry queries
- For package manager checks

## Integration with Existing Watcher

The existing `WatchHub_Realtime.ps1` will continue to monitor and log changes. The dashboard will:

1. Read from `AI_hub/_Change_log/` to get real-time updates
2. Parse `discovery.log` for historical data
3. Periodically re-scan (manual refresh in dashboard)

**Enhancement to watcher** (optional):

- Export JSON snapshot on each change: `AI_hub/_snapshots/latest.json`
- Dashboard reads this for real-time updates

## CSV Workflow (No Manual JSON Arrays)

Goal: avoid hand-editing `oauth_connections` arrays.

Flow:

1. Run `scan_gmail_oauth.py` → writes `gmail_connections.json` and regenerates `oauth_connections_table.csv`
2. Fill `oauth_connections_table.csv` (table format)
3. Run `import_oauth_connections_from_csv.py` → replaces `oauth_connections` in `gmail_connections.json`

Notes:

- The CSV is regenerated on each Gmail scan (auto-refresh).
- JSON is backed up to `data/gmail_connections.json.bak` on import.
- This workflow is Gmail-only; Google Connections page is intentionally excluded.

## Next Steps

### Immediate (Phase 1a)

1. Build Gmail OAuth scanner first
   - Authenticate with Gmail API
   - List authorized apps and scopes
   - Save to `gmail_connections.json`

2. Build Windows App scanner
   - Query registry for installed programs
   - Check package managers
   - Save to `windows_apps.json`

### Short-term (Phase 1b)

3. Build Hub log parser
2. Build config file hunter
3. Build data merger

### Medium-term (Phase 2)

6. Create Streamlit dashboard skeleton
2. Build Overview tab
3. Build Apps Inventory tab

### Long-term (Phase 3)

9. Add OAuth Connections tab
2. Add Config Map visualization
3. Add Relationship Graph
4. Polish UI and add filters

## Important Notes

- **Privacy**: All data stays local. No cloud uploads.
- **Performance**: Scanning can be slow (especially registry). Cache results.
- **Updates**: Re-run collectors manually or on schedule (Task Scheduler)
- **Obsidian Export**: Keep existing `ExportToObsidian.ps1` working alongside dashboard

## Questions & Decisions Needed

1. ✅ **Dashboard tech**: Streamlit chosen (easier than React/Vue)
2. ⏳ **OAuth scope**: Start with Gmail, add GitHub later?
3. ⏳ **Update frequency**: Manual refresh or auto-scan every N minutes?
4. ⏳ **Obsidian integration**: Export dashboard data to Obsidian Dataview tables?

## Success Criteria

When complete, you should be able to:

- ✅ See all installed AI tools in one dashboard
- ✅ Know which services are connected to Gmail/GitHub
- ✅ Find config files, skills dirs, MCP configs for any tool
- ✅ Understand relationships (what uses what)
- ✅ Track changes over time (via watcher logs)
- ✅ Search/filter by provider, type, status
