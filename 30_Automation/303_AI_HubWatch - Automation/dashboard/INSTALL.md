# 🚀 Installation Instructions

## What You Just Downloaded

This is the **Gmail OAuth Scanner** - Phase 1a of your AI Ecosystem Dashboard project.

## 📦 Files Included

```
dashboard/
├── collectors/
│   └── scan_gmail_oauth.py          # Gmail OAuth scanner script
├── data/
│   └── gmail_connections_template.json  # Template for manual entries
├── CLAUDE.md                         # Complete project documentation
├── README.md                         # Dashboard overview
├── SETUP_GMAIL_SCANNER.md           # Detailed setup guide
├── requirements.txt                  # Python dependencies
├── setup.ps1                        # Quick setup script
└── .gitignore                       # Protect sensitive files
```

## 🎯 Installation Steps

### 1. Copy Files to Your System

Copy the entire `dashboard` folder to:
```
C:\Vault\Apothecary\30_Automation\303_AI_HubWatch - Automation\dashboard\
```

Your structure should look like:
```
C:\Vault\Apothecary\30_Automation\303_AI_HubWatch - Automation\
├── CLAUDE.md (already exists or create it)
├── src_v2_refactor\
│   └── (your existing watcher scripts)
└── dashboard\          ← NEW FOLDER
    ├── collectors\
    ├── data\
    ├── README.md
    └── setup.ps1
```

### 2. Run Setup Script

Open **PowerShell** (not Command Prompt) and run:

```powershell
cd "C:\Vault\Apothecary\30_Automation\303_AI_HubWatch - Automation\dashboard"
.\setup.ps1
```

This will:
- ✓ Check Python installation
- ✓ Install dependencies
- ✓ Create directories
- ✓ Check for credentials

### 3. Set Up Google Cloud Credentials

**You must do this manually** - it's a one-time setup:

1. Open `SETUP_GMAIL_SCANNER.md` in the dashboard folder
2. Follow **Step 2: Set Up Google Cloud Credentials**
3. Download `credentials.json` from Google Cloud Console
4. Save it to: `dashboard\collectors\credentials.json`

**Quick link:** https://console.cloud.google.com/

### 4. Run the Gmail OAuth Scanner

Once you have `credentials.json`:

```powershell
cd collectors
python scan_gmail_oauth.py
```

This will:
1. Open your browser for Google authentication
2. Scan Gmail for service notifications
3. Create `data/gmail_connections.json`

### 5. Manual OAuth Entry

**Important:** The script can't get ALL OAuth connections automatically.

1. Go to: https://myaccount.google.com/permissions
2. Review all connected apps
3. Open: `data/gmail_connections.json`
4. Add each app to the `oauth_connections` array

Example:
```json
{
  "app_name": "Claude Desktop",
  "provider": "Anthropic",
  "oauth_scopes": ["email", "profile"],
  "grant_date": "2024-11-15",
  "last_used": "2025-02-07",
  "access_type": "oauth",
  "source": "manual_entry"
}
```

## ✅ Success Checklist

- [ ] Dashboard folder copied to correct location
- [ ] Ran `setup.ps1` successfully
- [ ] Created Google Cloud project
- [ ] Enabled Gmail API and People API
- [ ] Created OAuth Desktop credentials
- [ ] Downloaded `credentials.json`
- [ ] Placed `credentials.json` in `collectors/` folder
- [ ] Ran `scan_gmail_oauth.py`
- [ ] Authenticated with Google
- [ ] `gmail_connections.json` created
- [ ] Manually added OAuth apps from Google Account settings

## 🎉 What's Next?

After completing the Gmail OAuth scanner:

### Phase 1b - Additional Scanners
1. **Windows App Scanner** - Scan installed apps (TODO)
2. **Hub Log Parser** - Parse your AI_hub logs (TODO)
3. **Config Hunter** - Find config files (TODO)

### Phase 2 - Dashboard
1. Build Streamlit dashboard
2. Visualize all data
3. Show relationships

### Phase 3 - Integration
1. Connect with your watcher script
2. Auto-refresh on changes
3. Export to Obsidian

## 🆘 Need Help?

**Documentation:**
- `README.md` - Dashboard overview
- `SETUP_GMAIL_SCANNER.md` - Detailed setup
- `CLAUDE.md` - Complete project architecture

**Common Issues:**
- **credentials.json not found**: Follow Step 3 above
- **Python not found**: Install from python.org
- **Access blocked**: Add yourself as Test User in Google Cloud

**Where to get help:**
- Check the SETUP_GMAIL_SCANNER.md troubleshooting section
- Review the CLAUDE.md for architecture details

## 📝 Notes

- All data stays **local** - nothing uploaded to cloud
- `credentials.json` and `token.json` are protected by `.gitignore`
- Manual OAuth entry is required because Google doesn't expose this via API
- The scanner detected services are from Gmail activity, not comprehensive

---

**Ready to go?** Start with Step 1 above! 🚀
