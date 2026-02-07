# AI Ecosystem Dashboard

A comprehensive dashboard to track all AI tools, services, OAuth connections, and configurations on your Windows machine.

## 🎯 What This Does

Tracks and visualizes:
- **Local AI apps** (Claude Desktop, Cursor, VS Code, Windsurf, etc.)
- **OAuth connections** (apps connected via Gmail/GitHub)
- **Configuration files** (where each tool stores its settings, skills, MCP configs)
- **Relationships** (which apps use which services)

## 📋 Prerequisites

- **Windows 10/11**
- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **Google Account** (for Gmail OAuth scanning)
- **Google Cloud Project** (free, [setup guide below](#setup))

## 🚀 Quick Start

### 1. Install Dependencies

```powershell
cd "C:\Vault\Apothecary\30_Automation\303_AI_HubWatch - Automation\dashboard"
.\setup.ps1
```

This will:
- ✓ Check Python installation
- ✓ Create directory structure
- ✓ Install Python packages
- ✓ Check for Google credentials

### 2. Set Up Google Cloud Credentials

See **[SETUP_GMAIL_SCANNER.md](SETUP_GMAIL_SCANNER.md)** for detailed instructions.

**Quick version:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project → Enable Gmail API & People API
3. Create OAuth Desktop credentials
4. Download as `collectors/credentials.json`

### 3. Run the Gmail OAuth Scanner

```powershell
python collectors\scan_gmail_oauth.py
```

This will:
- Open a browser for Google authentication
- Scan Gmail for service notifications
- Create `data/gmail_connections.json`

**Important:** Manually add OAuth apps from https://myaccount.google.com/permissions

### 4. Run Other Scanners (Coming Soon)

```powershell
python collectors\scan_windows_apps.py      # Windows installed apps
python collectors\scan_hub_logs.py          # AI Hub junction logs
python collectors\scan_configs.py           # Config file locations
python collectors\merge_inventory.py        # Combine all data
```

### 5. Launch Dashboard (Coming Soon)

```powershell
streamlit run dashboard.py
```

## 📁 Project Structure

```
dashboard/
├── collectors/              # Data collection scripts
│   ├── scan_gmail_oauth.py     # Gmail OAuth connections
│   ├── scan_windows_apps.py    # Windows installed apps (TODO)
│   ├── scan_hub_logs.py        # AI Hub logs parser (TODO)
│   ├── scan_configs.py         # Config file hunter (TODO)
│   ├── merge_inventory.py      # Merge all data (TODO)
│   ├── credentials.json        # Google OAuth credentials (YOU CREATE)
│   └── token.json              # Auto-generated OAuth token
│
├── data/                    # Collected data (JSON files)
│   ├── gmail_connections.json  # Gmail OAuth data
│   ├── gmail_connections_template.json  # Template for manual entries
│   ├── windows_apps.json       # Windows apps (TODO)
│   ├── hub_junctions.json      # Hub data (TODO)
│   ├── config_files.json       # Config locations (TODO)
│   └── master_inventory.json   # Combined data (TODO)
│
├── dashboard.py             # Streamlit dashboard (TODO)
├── requirements.txt         # Python dependencies
├── setup.ps1               # Quick setup script
├── .gitignore              # Protect sensitive files
├── SETUP_GMAIL_SCANNER.md  # Detailed setup guide
└── README.md               # This file
```

## 🔐 Security & Privacy

- **All data stays local** - nothing uploaded to cloud
- **OAuth tokens protected** - automatically added to .gitignore
- **Sensitive files excluded** - credentials.json, token.json never committed
- **Manual OAuth export** - Google doesn't expose all OAuth connections via API

## 📊 Data Collection Status

| Scanner | Status | Output File |
|---------|--------|-------------|
| Gmail OAuth | ✅ **READY** | `gmail_connections.json` |
| Windows Apps | ⏳ TODO | `windows_apps.json` |
| Hub Logs | ⏳ TODO | `hub_junctions.json` |
| Config Files | ⏳ TODO | `config_files.json` |
| Data Merger | ⏳ TODO | `master_inventory.json` |
| Dashboard | ⏳ TODO | - |

## 🎨 Planned Dashboard Features

### Overview Tab
- Total apps count
- OAuth connections count
- Config files tracked
- Interactive relationship graph

### Apps Inventory Tab
- Searchable table of all apps
- Filter by type, provider, status
- View details (configs, skills, MCPs)

### OAuth Connections Tab
- Gmail authorized apps with scopes
- GitHub authorized apps
- Authorization dates
- Links to revoke access

### Config Map Tab
- Visual tree of config locations
- Skills directories
- MCP server configs

### Hub Monitor Tab
- Live AI Hub junctions
- Recent changes from watcher
- Skills sync status

## 🛠️ Integration with Existing Tools

This dashboard works alongside your existing automation:

- **AI Hub Watcher** (`src_v2_refactor/WatchHub_Realtime.ps1`)
  - Continues to monitor filesystem
  - Dashboard reads from `AI_hub/_Change_log/`
  
- **Manual Inventory** (`90_Inbox/Claude_AI_Ecosystem_Master_List.json`)
  - Used as reference for validation
  - Can import data from it

## 🐛 Troubleshooting

### "credentials.json not found"
- Make sure you created OAuth credentials in Google Cloud Console
- Download the JSON file
- Save it as `collectors/credentials.json`

### "Access blocked: This app's request is invalid"
- Add yourself as a Test User in OAuth consent screen
- Your email must match the test user

### "pip not recognized"
- Make sure Python is in your PATH
- Try: `python -m pip install -r requirements.txt`

### Gmail scanner only finds a few services
- This is expected! Google API doesn't expose all OAuth connections
- Manually add apps from https://myaccount.google.com/permissions
- Edit `data/gmail_connections.json` and add to `oauth_connections` array

## 📝 Next Steps

1. ✅ **Gmail OAuth Scanner** - COMPLETED
2. ⏳ **Windows App Scanner** - Create script to scan registry + packages
3. ⏳ **Hub Log Parser** - Parse AI_hub logs for tracked tools
4. ⏳ **Config Hunter** - Scan for config files across system
5. ⏳ **Data Merger** - Combine all JSON files + match relationships
6. ⏳ **Streamlit Dashboard** - Build interactive UI

## 📚 Documentation

- **[CLAUDE.md](../CLAUDE.md)** - Complete project overview and architecture
- **[SETUP_GMAIL_SCANNER.md](SETUP_GMAIL_SCANNER.md)** - Detailed Gmail scanner setup
- **[src_v2_refactor/](../src_v2_refactor/)** - Existing watcher scripts

## 🤝 Contributing

This is a personal automation project, but improvements welcome:
- Windows registry scanning optimizations
- Better OAuth connection detection
- Dashboard UI enhancements

## 📄 License

Personal use. See existing AI Hub automation license.

---

**Questions or Issues?** Check the SETUP guide or review the CLAUDE.md for architecture details.
