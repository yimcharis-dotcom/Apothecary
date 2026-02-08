# gmail-mcp-imap

A Gmail MCP (Model Context Protocol) server that provides email management capabilities through IMAP/SMTP. Works with Claude Desktop, Claude Code, and any MCP-compatible client.

## Features

- **Gmail Categories**: Fetch emails by Gmail's smart categories (Primary, Social, Promotions, Updates, Forums)
- **Full Email Management**: Read, send, reply, star, delete, and label emails
- **Attachment Handling**: List, download, and save attachments to disk
- **No Google API Required**: Uses IMAP/SMTP directly with App Password authentication
- **Date Filtering**: Filter emails by date range

## Installation

```bash
npm install gmail-mcp-imap
```

Or run directly with npx:

```bash
npx gmail-mcp-imap
```

## Prerequisites

1. A Gmail account
2. **App Password** (not your regular password):
   - Go to [Google Account Security](https://myaccount.google.com/security)
   - Enable 2-Step Verification if not already enabled
   - Go to App Passwords (search for "App Passwords" in account settings)
   - Generate a new app password for "Mail"
   - Copy the 16-character password

## Configuration

### Environment Variables

Set these environment variables before running:

```bash
export GMAIL_EMAIL="your-email@gmail.com"
export GMAIL_APP_PASSWORD="your-16-char-app-password"
```

### Claude Desktop Configuration

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "gmail": {
      "command": "npx",
      "args": ["gmail-mcp-imap"],
      "env": {
        "GMAIL_EMAIL": "your-email@gmail.com",
        "GMAIL_APP_PASSWORD": "your-app-password"
      }
    }
  }
}
```

### Claude Code Configuration

Add to your `.mcp.json`:

```json
{
  "mcpServers": {
    "gmail": {
      "command": "npx",
      "args": ["gmail-mcp-imap"],
      "env": {
        "GMAIL_EMAIL": "your-email@gmail.com",
        "GMAIL_APP_PASSWORD": "your-app-password"
      }
    }
  }
}
```

## Available Tools

### Category Tools
| Tool | Description |
|------|-------------|
| `get_primary_emails` | Important conversations from real people |
| `get_social_emails` | Social network notifications |
| `get_promotions_emails` | Marketing emails, deals, offers |
| `get_updates_emails` | Receipts, bills, statements |
| `get_forums_emails` | Mailing lists, discussion groups |

### Search & Read Tools
| Tool | Description |
|------|-------------|
| `search_emails` | Search emails by keywords |
| `get_email_content` | Get full email content by UID |
| `get_emails_by_label` | Get emails from a specific label |
| `list_labels` | List all Gmail labels/folders |

### Action Tools
| Tool | Description |
|------|-------------|
| `send_email` | Send a new email |
| `reply_to_email` | Reply to an existing email |
| `mark_as_read` | Mark email as read |
| `mark_as_unread` | Mark email as unread |
| `star_email` | Star or unstar an email |
| `delete_email` | Move email to trash |
| `apply_label` | Apply a label to an email |

### Attachment Tools
| Tool | Description |
|------|-------------|
| `list_attachments` | List attachments in an email |
| `download_attachment` | Download attachment as Base64 |
| `save_attachment` | Save attachment to disk |

## Usage Examples

Once configured, you can ask Claude:

- "Show me my primary emails from the last week"
- "Search for emails from Amazon"
- "Read the email with UID 12345"
- "Send an email to john@example.com about the meeting"
- "Download the PDF attachment from email 12345"
- "Star the important emails about invoices"

## Why IMAP/SMTP?

This MCP server uses IMAP/SMTP instead of the Google API because:

1. **Simpler Setup**: No OAuth consent screen or API credentials needed
2. **App Passwords**: More secure than storing your main password
3. **No Rate Limits**: Google API has strict quotas; IMAP doesn't
4. **Works Offline**: No dependency on Google's API servers
5. **Privacy**: Your emails aren't processed through additional Google services

## Development

```bash
# Clone the repository
git clone https://github.com/suhailak/gmail-mcp.git
cd gmail-mcp

# Install dependencies
npm install

# Run in development mode
npm run dev

# Build for production
npm run build

# Run production build
npm start
```

## License

MIT

## Author

Suhail ([@ansuhail.ak@gmail.com](mailto:ansuhail.ak@gmail.com))
