#!/usr/bin/env node
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { config } from "dotenv";
import { GmailClient } from "./gmail-client.js";
// Load environment variables
config();
const GMAIL_EMAIL = process.env.GMAIL_EMAIL;
const GMAIL_APP_PASSWORD = process.env.GMAIL_APP_PASSWORD;
if (!GMAIL_EMAIL || !GMAIL_APP_PASSWORD) {
    console.error("Error: GMAIL_EMAIL and GMAIL_APP_PASSWORD environment variables are required");
    process.exit(1);
}
// Initialize Gmail client
const gmail = new GmailClient({
    email: GMAIL_EMAIL,
    appPassword: GMAIL_APP_PASSWORD,
});
// Create MCP server
const server = new McpServer({
    name: "gmail-mcp",
    version: "1.0.0",
});
// =============================================================================
// PRIMARY TOOLS - Gmail Categories (Most Important)
// =============================================================================
server.tool("get_primary_emails", "Get emails from Primary category - important conversations from real people", {
    limit: z.number().min(1).max(50).default(10).describe("Number of emails to fetch"),
    after: z.string().optional().describe("Filter emails after this date (YYYY/MM/DD or YYYY-MM-DD)"),
    before: z.string().optional().describe("Filter emails before this date (YYYY/MM/DD or YYYY-MM-DD)"),
}, async ({ limit, after, before }) => {
    const emails = await gmail.getEmailsByCategory("primary", limit, { after, before });
    return {
        content: [
            {
                type: "text",
                text: JSON.stringify(emails, null, 2),
            },
        ],
    };
});
server.tool("get_social_emails", "Get emails from Social category - notifications from social networks like Facebook, Twitter, LinkedIn", {
    limit: z.number().min(1).max(50).default(10).describe("Number of emails to fetch"),
    after: z.string().optional().describe("Filter emails after this date (YYYY/MM/DD or YYYY-MM-DD)"),
    before: z.string().optional().describe("Filter emails before this date (YYYY/MM/DD or YYYY-MM-DD)"),
}, async ({ limit, after, before }) => {
    const emails = await gmail.getEmailsByCategory("social", limit, { after, before });
    return {
        content: [
            {
                type: "text",
                text: JSON.stringify(emails, null, 2),
            },
        ],
    };
});
server.tool("get_promotions_emails", "Get emails from Promotions category - marketing emails, deals, offers, newsletters", {
    limit: z.number().min(1).max(50).default(10).describe("Number of emails to fetch"),
    after: z.string().optional().describe("Filter emails after this date (YYYY/MM/DD or YYYY-MM-DD)"),
    before: z.string().optional().describe("Filter emails before this date (YYYY/MM/DD or YYYY-MM-DD)"),
}, async ({ limit, after, before }) => {
    const emails = await gmail.getEmailsByCategory("promotions", limit, { after, before });
    return {
        content: [
            {
                type: "text",
                text: JSON.stringify(emails, null, 2),
            },
        ],
    };
});
server.tool("get_updates_emails", "Get emails from Updates category - transactional emails like receipts, bills, statements, order confirmations", {
    limit: z.number().min(1).max(50).default(10).describe("Number of emails to fetch"),
    after: z.string().optional().describe("Filter emails after this date (YYYY/MM/DD or YYYY-MM-DD)"),
    before: z.string().optional().describe("Filter emails before this date (YYYY/MM/DD or YYYY-MM-DD)"),
}, async ({ limit, after, before }) => {
    const emails = await gmail.getEmailsByCategory("updates", limit, { after, before });
    return {
        content: [
            {
                type: "text",
                text: JSON.stringify(emails, null, 2),
            },
        ],
    };
});
server.tool("get_forums_emails", "Get emails from Forums category - mailing lists, discussion groups, online forums", {
    limit: z.number().min(1).max(50).default(10).describe("Number of emails to fetch"),
    after: z.string().optional().describe("Filter emails after this date (YYYY/MM/DD or YYYY-MM-DD)"),
    before: z.string().optional().describe("Filter emails before this date (YYYY/MM/DD or YYYY-MM-DD)"),
}, async ({ limit, after, before }) => {
    const emails = await gmail.getEmailsByCategory("forums", limit, { after, before });
    return {
        content: [
            {
                type: "text",
                text: JSON.stringify(emails, null, 2),
            },
        ],
    };
});
// =============================================================================
// SECONDARY TOOLS - Search, Read, Send
// =============================================================================
server.tool("search_emails", "Search emails using keywords - searches in subject and sender", {
    query: z.string().describe("Search query (searches subject and sender)"),
    limit: z.number().min(1).max(50).default(10).describe("Maximum results"),
}, async ({ query, limit }) => {
    const emails = await gmail.searchEmails(query, limit);
    return {
        content: [
            {
                type: "text",
                text: JSON.stringify(emails, null, 2),
            },
        ],
    };
});
server.tool("get_email_content", "Get full content of a specific email by its UID", {
    uid: z.number().describe("Email UID (from email list results)"),
}, async ({ uid }) => {
    const email = await gmail.getEmailContent(uid);
    if (!email) {
        return {
            content: [{ type: "text", text: "Email not found" }],
        };
    }
    return {
        content: [
            {
                type: "text",
                text: JSON.stringify(email, null, 2),
            },
        ],
    };
});
server.tool("get_emails_by_label", "Get emails from a specific label or folder (e.g., Github, Naukri jobs, Notes)", {
    label: z.string().describe("Label name (e.g., 'Github', 'Naukri jobs', 'Purchases')"),
    limit: z.number().min(1).max(50).default(10).describe("Number of emails to fetch"),
}, async ({ label, limit }) => {
    const emails = await gmail.getEmailsByLabel(label, limit);
    return {
        content: [
            {
                type: "text",
                text: JSON.stringify(emails, null, 2),
            },
        ],
    };
});
server.tool("list_labels", "List all Gmail labels and folders", {}, async () => {
    const labels = await gmail.listLabels();
    return {
        content: [
            {
                type: "text",
                text: JSON.stringify(labels, null, 2),
            },
        ],
    };
});
// =============================================================================
// ACTION TOOLS - Send, Reply, Manage
// =============================================================================
server.tool("send_email", "Send a new email with optional attachments", {
    to: z.string().describe("Recipient email address"),
    subject: z.string().describe("Email subject"),
    body: z.string().describe("Email body content"),
    cc: z.string().optional().describe("CC recipients (comma-separated)"),
    bcc: z.string().optional().describe("BCC recipients (comma-separated)"),
    html: z.boolean().default(false).describe("Send as HTML email"),
    attachments: z
        .array(z.object({
        filename: z.string().describe("Name of the attachment file"),
        path: z.string().optional().describe("Absolute file path to attach"),
        content: z.string().optional().describe("Base64 encoded content (alternative to path)"),
        encoding: z.string().optional().describe("Content encoding (e.g., 'base64')"),
    }))
        .optional()
        .describe("Array of attachments. Use 'path' for local files or 'content' with 'encoding: base64' for inline content"),
}, async ({ to, subject, body, cc, bcc, html, attachments }) => {
    const result = await gmail.sendEmail(to, subject, body, { cc, bcc, html, attachments });
    return {
        content: [
            {
                type: "text",
                text: result.success
                    ? `Email sent successfully! Message ID: ${result.messageId}${attachments?.length ? ` (${attachments.length} attachment(s))` : ""}`
                    : `Failed to send email: ${result.error}`,
            },
        ],
    };
});
server.tool("reply_to_email", "Reply to an existing email", {
    uid: z.number().describe("UID of the email to reply to"),
    body: z.string().describe("Reply message body"),
    html: z.boolean().default(false).describe("Send as HTML"),
}, async ({ uid, body, html }) => {
    const result = await gmail.replyEmail(uid, body, { html });
    return {
        content: [
            {
                type: "text",
                text: result.success
                    ? `Reply sent successfully! Message ID: ${result.messageId}`
                    : `Failed to send reply: ${result.error}`,
            },
        ],
    };
});
server.tool("mark_as_read", "Mark an email as read", {
    uid: z.number().describe("Email UID"),
}, async ({ uid }) => {
    const success = await gmail.markAsRead(uid, true);
    return {
        content: [
            {
                type: "text",
                text: success ? "Email marked as read" : "Failed to mark email as read",
            },
        ],
    };
});
server.tool("mark_as_unread", "Mark an email as unread", {
    uid: z.number().describe("Email UID"),
}, async ({ uid }) => {
    const success = await gmail.markAsRead(uid, false);
    return {
        content: [
            {
                type: "text",
                text: success ? "Email marked as unread" : "Failed to mark email as unread",
            },
        ],
    };
});
server.tool("star_email", "Star or unstar an email", {
    uid: z.number().describe("Email UID"),
    starred: z.boolean().default(true).describe("true to star, false to unstar"),
}, async ({ uid, starred }) => {
    const success = await gmail.starEmail(uid, starred);
    return {
        content: [
            {
                type: "text",
                text: success
                    ? `Email ${starred ? "starred" : "unstarred"}`
                    : "Failed to update star status",
            },
        ],
    };
});
server.tool("delete_email", "Move an email to trash", {
    uid: z.number().describe("Email UID"),
}, async ({ uid }) => {
    const success = await gmail.deleteEmail(uid);
    return {
        content: [
            {
                type: "text",
                text: success ? "Email moved to trash" : "Failed to delete email",
            },
        ],
    };
});
server.tool("apply_label", "Apply a label to an email", {
    uid: z.number().describe("Email UID"),
    label: z.string().describe("Label to apply"),
}, async ({ uid, label }) => {
    const success = await gmail.applyLabel(uid, label);
    return {
        content: [
            {
                type: "text",
                text: success ? `Label "${label}" applied` : "Failed to apply label",
            },
        ],
    };
});
// =============================================================================
// ATTACHMENT TOOLS
// =============================================================================
server.tool("download_attachment", "Download an email attachment and return it as Base64 encoded data. Use this to save attachments locally.", {
    uid: z.number().describe("Email UID"),
    filename: z.string().describe("Exact filename of the attachment to download"),
}, async ({ uid, filename }) => {
    const attachment = await gmail.downloadAttachment(uid, filename);
    if (!attachment) {
        return {
            content: [
                {
                    type: "text",
                    text: `Attachment "${filename}" not found in email ${uid}`,
                },
            ],
        };
    }
    return {
        content: [
            {
                type: "text",
                text: JSON.stringify({
                    filename: attachment.filename,
                    contentType: attachment.contentType,
                    size: attachment.size,
                    content: attachment.content,
                }, null, 2),
            },
        ],
    };
});
server.tool("list_attachments", "List all attachments in an email (without downloading content)", {
    uid: z.number().describe("Email UID"),
}, async ({ uid }) => {
    const attachments = await gmail.listAttachments(uid);
    return {
        content: [
            {
                type: "text",
                text: attachments.length > 0
                    ? JSON.stringify(attachments, null, 2)
                    : "No attachments found",
            },
        ],
    };
});
server.tool("save_attachment", "Download an email attachment and save it to a specified file path", {
    uid: z.number().describe("Email UID"),
    filename: z.string().describe("Exact filename of the attachment to download"),
    savePath: z.string().describe("Full file path where to save the attachment"),
}, async ({ uid, filename, savePath }) => {
    const attachment = await gmail.downloadAttachment(uid, filename);
    if (!attachment) {
        return {
            content: [
                {
                    type: "text",
                    text: `Attachment "${filename}" not found in email ${uid}`,
                },
            ],
        };
    }
    // Save the file
    const fs = await import("fs/promises");
    const path = await import("path");
    try {
        // Ensure directory exists
        const dir = path.dirname(savePath);
        await fs.mkdir(dir, { recursive: true });
        // Write the file
        const buffer = Buffer.from(attachment.content, "base64");
        await fs.writeFile(savePath, buffer);
        return {
            content: [
                {
                    type: "text",
                    text: JSON.stringify({
                        success: true,
                        savedTo: savePath,
                        filename: attachment.filename,
                        contentType: attachment.contentType,
                        size: attachment.size,
                    }, null, 2),
                },
            ],
        };
    }
    catch (error) {
        return {
            content: [
                {
                    type: "text",
                    text: `Failed to save attachment: ${error instanceof Error ? error.message : "Unknown error"}`,
                },
            ],
        };
    }
});
// =============================================================================
// START SERVER
// =============================================================================
async function main() {
    const transport = new StdioServerTransport();
    await server.connect(transport);
    console.error("Gmail MCP Server running on stdio");
}
main().catch((error) => {
    console.error("Fatal error:", error);
    process.exit(1);
});
// Cleanup on exit
process.on("SIGINT", async () => {
    await gmail.disconnect();
    process.exit(0);
});
process.on("SIGTERM", async () => {
    await gmail.disconnect();
    process.exit(0);
});
//# sourceMappingURL=index.js.map