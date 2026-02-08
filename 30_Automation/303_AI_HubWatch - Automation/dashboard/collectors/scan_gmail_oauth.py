#!/usr/bin/env python3
"""
Gmail OAuth Scanner
Scans Gmail account for connected third-party apps and OAuth grants.

This script will:
1. Authenticate with Google APIs
2. List apps that have access to your Google account
3. Extract scopes, permissions, and metadata
4. Save results to gmail_connections.json

Note: Google doesn't provide a direct API to list all connected apps for regular users.
This script uses available APIs and provides instructions for manual export.
"""

import os
import json
import csv
import datetime
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the token.json file.
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'openid',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
]

# Output directory
OUTPUT_DIR = Path(__file__).parent.parent / 'data'
OUTPUT_FILE = OUTPUT_DIR / 'gmail_connections.json'
CSV_FILE = OUTPUT_DIR / 'oauth_connections_table.csv'
TOKEN_FILE = Path(__file__).parent / 'token.json'
CREDENTIALS_FILE = Path(__file__).parent / 'credentials.json'


def get_credentials():
    """Authenticate and get Google API credentials."""
    creds = None
    
    # The file token.json stores the user's access and refresh tokens
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    
    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_FILE.exists():
                print("\n" + "="*70)
                print("ERROR: credentials.json not found!")
                print("="*70)
                print("\nYou need to set up Google Cloud OAuth credentials.")
                print("\nSteps to get credentials.json:")
                print("1. Go to: https://console.cloud.google.com/")
                print("2. Create a new project (or select existing)")
                print("3. Enable these APIs:")
                print("   - Gmail API")
                print("   - People API")
                print("4. Go to: APIs & Services > Credentials")
                print("5. Click: Create Credentials > OAuth client ID")
                print("6. Choose: Desktop app")
                print("7. Download the JSON file")
                print(f"8. Save it as: {CREDENTIALS_FILE}")
                print("\nThen run this script again.")
                print("="*70 + "\n")
                return None
            
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    
    return creds


def get_user_info(creds):
    """Get basic user information."""
    try:
        service = build('oauth2', 'v2', credentials=creds)
        user_info = service.userinfo().get().execute()
        return {
            'email': user_info.get('email'),
            'name': user_info.get('name'),
            'id': user_info.get('id')
        }
    except HttpError as error:
        print(f'An error occurred getting user info: {error}')
        return None


def analyze_gmail_messages(creds):
    """
    Analyze Gmail messages to identify apps that have sent emails.
    This gives us a partial view of connected services.
    """
    try:
        service = build('gmail', 'v1', credentials=creds)
        
        # Search for automated emails from various services
        # These patterns help identify OAuth-connected apps
        search_queries = [
            'from:noreply@',
            'from:no-reply@',
            'from:notify@',
            'from:notifications@',
            'subject:"signed in"',
            'subject:"new sign-in"',
            'subject:"authorized"'
        ]
        
        detected_services = {}
        
        print("Scanning Gmail for service notifications...")
        for query in search_queries:
            try:
                results = service.users().messages().list(
                    userId='me',
                    q=query,
                    maxResults=50
                ).execute()
                
                messages = results.get('messages', [])
                
                for msg in messages[:10]:  # Limit to prevent too many API calls
                    message = service.users().messages().get(
                        userId='me',
                        id=msg['id'],
                        format='metadata',
                        metadataHeaders=['From', 'Subject', 'Date']
                    ).execute()
                    
                    headers = {h['name']: h['value'] for h in message['payload']['headers']}
                    from_email = headers.get('From', '')
                    
                    # Extract service name from email
                    if '@' in from_email:
                        domain = from_email.split('@')[-1].split('>')[0].strip()
                        service_name = domain.split('.')[0]
                        
                        if service_name not in detected_services:
                            detected_services[service_name] = {
                                'name': service_name,
                                'domain': domain,
                                'from_email': from_email,
                                'last_seen': headers.get('Date', 'Unknown'),
                                'source': 'gmail_analysis'
                            }
                
            except HttpError as error:
                print(f'Error searching "{query}": {error}')
                continue
        
        return list(detected_services.values())
        
    except HttpError as error:
        print(f'An error occurred: {error}')
        return []


def get_manual_instructions():
    """
    Provide instructions for manually exporting connected apps.
    Google doesn't provide a public API for this, so manual export is needed.
    """
    return {
        'manual_export_required': True,
        'instructions': [
            "Google doesn't provide a public API to list all connected apps.",
            "To get your complete list of connected apps:",
            "",
            "METHOD 1: Manual Export from Google Account",
            "1. Go to: https://myaccount.google.com/permissions",
            "2. You'll see all third-party apps with access",
            "3. For each app, note down:",
            "   - App name",
            "   - What it has access to (scopes)",
            "   - When you granted access",
            "4. Fill them into oauth_connections_table.csv",
            "5. Run import_oauth_connections_from_csv.py",
            "",
            "METHOD 2: Google Takeout (Complete Data Export)",
            "1. Go to: https://takeout.google.com/",
            "2. Select: 'My Activity' and 'Security'",
            "3. Download your data",
            "4. Extract and look for connected apps info",
            "",
            "The script below has detected some services from Gmail activity,",
            "but this is not a complete list of OAuth connections."
        ],
        'useful_links': [
            'https://myaccount.google.com/permissions',
            'https://myaccount.google.com/security',
            'https://takeout.google.com/'
        ]
    }


def export_oauth_csv(detected_services):
    """Write a CSV table for OAuth connections (editable by humans)."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    fields = [
        "app_name",
        "provider",
        "oauth_scopes",
        "grant_date",
        "last_used",
        "access_type",
        "source",
        "evidence_domain",
        "evidence_from_email",
        "evidence_last_seen",
    ]

    rows = []
    for svc in detected_services:
        rows.append({
            "app_name": svc.get("name", ""),
            "provider": "",
            "oauth_scopes": "",
            "grant_date": "",
            "last_used": svc.get("last_seen", ""),
            "access_type": "oauth",
            "source": "gmail_analysis",
            "evidence_domain": svc.get("domain", ""),
            "evidence_from_email": svc.get("from_email", ""),
            "evidence_last_seen": svc.get("last_seen", ""),
        })

    with open(CSV_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main():
    """Main function to scan Gmail OAuth connections."""
    print("\n" + "="*70)
    print("Gmail OAuth Connection Scanner")
    print("="*70 + "\n")
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Get credentials
    creds = get_credentials()
    if not creds:
        return
    
    print("✓ Authentication successful\n")
    
    # Get user info
    user_info = get_user_info(creds)
    if user_info:
        print(f"Logged in as: {user_info['email']}")
        print(f"Name: {user_info['name']}\n")
    
    # Analyze Gmail for service connections
    detected_services = analyze_gmail_messages(creds)
    print(f"\n✓ Detected {len(detected_services)} services from Gmail activity\n")
    
    # Get manual export instructions
    manual_info = get_manual_instructions()
    
    # Prepare output data
    output_data = {
        'scan_date': datetime.datetime.now().isoformat(),
        'user_email': user_info.get('email') if user_info else 'unknown',
        'scan_method': 'gmail_api_analysis',
        'note': 'This is a partial list detected from Gmail activity. For complete OAuth connections, see manual_export_instructions.',
        'manual_export_instructions': manual_info,
        'detected_services': detected_services,
        'oauth_connections': []
    }
    
    # Save to JSON
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    export_oauth_csv(detected_services)
    
    print("="*70)
    print(f"✓ Results saved to: {OUTPUT_FILE}")
    print(f"✓ CSV table saved to: {CSV_FILE}")
    print("="*70)
    print("\nIMPORTANT:")
    print("- Gmail API doesn't expose all OAuth connections directly")
    print("- Visit https://myaccount.google.com/permissions for complete list")
    print("- Fill oauth_connections_table.csv and import it")
    print("="*70 + "\n")
    
    # Print summary
    print("DETECTED SERVICES FROM GMAIL ACTIVITY:")
    for service in detected_services[:10]:
        print(f"  • {service['name']} ({service['domain']})")
    
    if len(detected_services) > 10:
        print(f"  ... and {len(detected_services) - 10} more")
    
    print("\nNext steps:")
    print("1. Open https://myaccount.google.com/permissions")
    print("2. Review all connected apps")
    print(f"3. Fill {CSV_FILE}")
    print("4. Run: python import_oauth_connections_from_csv.py")
    print("5. Run the Windows app scanner next: scan_windows_apps.py")
    print()


if __name__ == '__main__':
    main()
