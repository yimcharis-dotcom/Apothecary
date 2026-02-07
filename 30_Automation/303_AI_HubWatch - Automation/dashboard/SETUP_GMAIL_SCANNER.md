# Gmail OAuth Scanner Setup Guide

## Prerequisites

1. **Python 3.8+** installed on your system
2. **Google Account** (your Gmail account)
3. **Google Cloud Project** (free, we'll set this up)

## Step 1: Install Python Dependencies

Open PowerShell or Command Prompt and run:

```bash
cd "C:\Vault\Apothecary\30_Automation\303_AI_HubWatch - Automation\dashboard"
pip install -r requirements.txt
```

## Step 2: Set Up Google Cloud Credentials

### A. Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **"Select a project"** → **"New Project"**
3. Project name: `AI-Dashboard-Scanner` (or any name you like)
4. Click **"Create"**
5. Wait for the project to be created, then select it

### B. Enable Required APIs

1. In your new project, go to **"APIs & Services"** → **"Library"**
2. Search for and enable these APIs:
   - **Gmail API** (click Enable)
   - **People API** (click Enable)

### C. Create OAuth Credentials

1. Go to **"APIs & Services"** → **"Credentials"**
2. Click **"+ CREATE CREDENTIALS"** → **"OAuth client ID"**
3. If prompted to configure consent screen:
   - Click **"Configure Consent Screen"**
   - Choose **"External"** → Click **"Create"**
   - Fill in:
     - App name: `AI Dashboard Scanner`
     - User support email: Your email
     - Developer contact: Your email
   - Click **"Save and Continue"** through all steps
   - On "Test users", click **"+ ADD USERS"** and add your email
   - Click **"Save and Continue"**

4. Back at **"Create OAuth client ID"**:
   - Application type: **"Desktop app"**
   - Name: `AI Dashboard Desktop`
   - Click **"Create"**

5. Download the credentials:
   - A popup appears with your credentials
   - Click **"DOWNLOAD JSON"**
   - Save the file as `credentials.json`

### D. Place credentials.json

Move the downloaded `credentials.json` to:
```
C:\Vault\Apothecary\30_Automation\303_AI_HubWatch - Automation\dashboard\collectors\credentials.json
```

## Step 3: Run the Gmail OAuth Scanner

```bash
cd "C:\Vault\Apothecary\30_Automation\303_AI_HubWatch - Automation\dashboard\collectors"
python scan_gmail_oauth.py
```

### What happens:
1. A browser window opens asking you to sign in to Google
2. Grant the requested permissions (Gmail read-only access)
3. The script scans your Gmail for service notifications
4. Results are saved to `../data/gmail_connections.json`

## Step 4: Manual OAuth App Export

**Important:** Google doesn't provide a public API to list ALL connected apps. You need to manually export them:

### Option 1: Quick Manual Review (Recommended)

1. Go to: https://myaccount.google.com/permissions
2. You'll see all third-party apps with access to your Google account
3. For each app, note:
   - App name
   - What it has access to
   - When you granted access
4. Manually add them to the `oauth_connections` array in `gmail_connections.json`

Example entry:
```json
{
  "app_name": "Claude Desktop",
  "provider": "Anthropic",
  "oauth_scopes": ["email", "profile", "drive.readonly"],
  "grant_date": "2024-11-15",
  "last_used": "2025-02-07",
  "access_type": "oauth",
  "source": "manual_entry"
}
```

### Option 2: Google Takeout (Complete Export)

1. Go to: https://takeout.google.com/
2. Deselect all, then select:
   - **My Activity**
   - **Security**
3. Click "Next step" → "Create export"
4. Wait for email notification
5. Download and extract the archive
6. Look for connected apps information in the Security folder

## Troubleshooting

### Error: "credentials.json not found"
- Make sure you downloaded the OAuth credentials from Google Cloud Console
- Place it in the `collectors/` folder
- Filename must be exactly `credentials.json`

### Error: "Access blocked: This app's request is invalid"
- Make sure you added yourself as a Test User in the OAuth consent screen
- Your Google account must match the test user email

### Error: "The redirect URI in the request did not match"
- Delete `token.json` if it exists
- Run the script again

### Browser doesn't open automatically
- Copy the URL from the terminal
- Paste it in your browser manually
- Complete the OAuth flow

## Output File Structure

The script creates `data/gmail_connections.json` with this structure:

```json
{
  "scan_date": "2025-02-07T10:30:00",
  "user_email": "your.email@gmail.com",
  "scan_method": "gmail_api_analysis",
  "detected_services": [
    {
      "name": "github",
      "domain": "github.com",
      "from_email": "noreply@github.com",
      "last_seen": "Thu, 6 Feb 2025 10:00:00",
      "source": "gmail_analysis"
    }
  ],
  "oauth_connections": [
    {
      "app_name": "Your App",
      "provider": "Provider Name",
      "oauth_scopes": ["scope1", "scope2"],
      "grant_date": "2024-01-01",
      "last_used": "2025-02-07",
      "access_type": "oauth",
      "source": "manual_entry"
    }
  ]
}
```

## Next Steps

After collecting Gmail OAuth data:

1. Run the Windows app scanner: `python scan_windows_apps.py`
2. Run the Hub log parser: `python scan_hub_logs.py`
3. Run the config hunter: `python scan_configs.py`
4. Merge all data: `python merge_inventory.py`
5. Launch the dashboard: `streamlit run dashboard.py`

## Security Notes

- `token.json` contains your OAuth tokens - **DO NOT commit to Git**
- `credentials.json` contains your OAuth client secrets - **DO NOT share publicly**
- Add both to `.gitignore`
- All data stays local on your machine
