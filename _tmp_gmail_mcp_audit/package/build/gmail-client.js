import Imap from "imap";
import { simpleParser } from "mailparser";
import nodemailer from "nodemailer";
// Gmail categories
const GMAIL_CATEGORIES = ["primary", "social", "promotions", "updates", "forums"];
export class GmailClient {
    config;
    smtpTransport = null;
    constructor(config) {
        this.config = config;
    }
    // Create IMAP connection
    createImapConnection() {
        return new Imap({
            user: this.config.email,
            password: this.config.appPassword,
            host: "imap.gmail.com",
            port: 993,
            tls: true,
            tlsOptions: { rejectUnauthorized: false },
        });
    }
    // Initialize SMTP transport
    getSmtpTransport() {
        if (!this.smtpTransport) {
            this.smtpTransport = nodemailer.createTransport({
                host: "smtp.gmail.com",
                port: 465,
                secure: true,
                auth: {
                    user: this.config.email,
                    pass: this.config.appPassword,
                },
            });
        }
        return this.smtpTransport;
    }
    // Helper to run IMAP operations
    runImapOperation(operation) {
        return new Promise((resolve, reject) => {
            const imap = this.createImapConnection();
            imap.once("ready", () => {
                operation(imap, resolve, reject);
            });
            imap.once("error", (err) => {
                reject(err);
            });
            imap.connect();
        });
    }
    // Get emails by Gmail category using X-GM-RAW
    async getEmailsByCategory(category, limit = 10, dateFilter) {
        return this.runImapOperation((imap, resolve, reject) => {
            imap.openBox("INBOX", true, (err) => {
                if (err) {
                    imap.end();
                    reject(err);
                    return;
                }
                // Build search query with category and optional date filters
                let searchQuery = `category:${category}`;
                if (dateFilter?.after) {
                    searchQuery += ` after:${dateFilter.after}`;
                }
                if (dateFilter?.before) {
                    searchQuery += ` before:${dateFilter.before}`;
                }
                // Use X-GM-RAW for Gmail category search
                imap.search([["X-GM-RAW", searchQuery]], (err, uids) => {
                    if (err) {
                        imap.end();
                        reject(err);
                        return;
                    }
                    if (!uids || uids.length === 0) {
                        imap.end();
                        resolve([]);
                        return;
                    }
                    // Get the most recent emails (last N)
                    const recentUids = uids.slice(-limit);
                    const emails = [];
                    const fetch = imap.fetch(recentUids, {
                        bodies: ["HEADER.FIELDS (FROM TO SUBJECT DATE)"],
                        struct: true,
                    });
                    fetch.on("message", (msg) => {
                        let uid = 0;
                        let headers = {};
                        const flags = [];
                        msg.on("body", (stream) => {
                            let buffer = "";
                            stream.on("data", (chunk) => {
                                buffer += chunk.toString("utf8");
                            });
                            stream.once("end", () => {
                                headers = Imap.parseHeader(buffer);
                            });
                        });
                        msg.once("attributes", (attrs) => {
                            uid = attrs.uid;
                            if (attrs.flags) {
                                flags.push(...attrs.flags);
                            }
                        });
                        msg.once("end", () => {
                            emails.push({
                                id: uid.toString(),
                                uid,
                                subject: headers.subject?.[0] || "(No Subject)",
                                from: headers.from?.[0] || "Unknown",
                                to: headers.to?.[0] || "",
                                date: headers.date?.[0] || "",
                                snippet: "",
                                labels: [],
                                isRead: flags.includes("\\Seen"),
                                isStarred: flags.includes("\\Flagged"),
                            });
                        });
                    });
                    fetch.once("error", (err) => {
                        imap.end();
                        reject(err);
                    });
                    fetch.once("end", () => {
                        imap.end();
                        // Return in reverse order (most recent first)
                        resolve(emails.reverse());
                    });
                });
            });
        });
    }
    // Get emails from a specific label/folder
    async getEmailsByLabel(label, limit = 10) {
        return this.runImapOperation((imap, resolve, reject) => {
            // Try to open the label as a mailbox
            const mailboxPath = label.startsWith("[Gmail]") ? label : label;
            imap.openBox(mailboxPath, true, (err) => {
                if (err) {
                    imap.end();
                    reject(err);
                    return;
                }
                imap.search(["ALL"], (err, uids) => {
                    if (err) {
                        imap.end();
                        reject(err);
                        return;
                    }
                    if (!uids || uids.length === 0) {
                        imap.end();
                        resolve([]);
                        return;
                    }
                    const recentUids = uids.slice(-limit);
                    const emails = [];
                    const fetch = imap.fetch(recentUids, {
                        bodies: ["HEADER.FIELDS (FROM TO SUBJECT DATE)"],
                        struct: true,
                    });
                    fetch.on("message", (msg) => {
                        let uid = 0;
                        let headers = {};
                        const flags = [];
                        msg.on("body", (stream) => {
                            let buffer = "";
                            stream.on("data", (chunk) => {
                                buffer += chunk.toString("utf8");
                            });
                            stream.once("end", () => {
                                headers = Imap.parseHeader(buffer);
                            });
                        });
                        msg.once("attributes", (attrs) => {
                            uid = attrs.uid;
                            if (attrs.flags) {
                                flags.push(...attrs.flags);
                            }
                        });
                        msg.once("end", () => {
                            emails.push({
                                id: uid.toString(),
                                uid,
                                subject: headers.subject?.[0] || "(No Subject)",
                                from: headers.from?.[0] || "Unknown",
                                to: headers.to?.[0] || "",
                                date: headers.date?.[0] || "",
                                snippet: "",
                                labels: [],
                                isRead: flags.includes("\\Seen"),
                                isStarred: flags.includes("\\Flagged"),
                            });
                        });
                    });
                    fetch.once("error", (err) => {
                        imap.end();
                        reject(err);
                    });
                    fetch.once("end", () => {
                        imap.end();
                        resolve(emails.reverse());
                    });
                });
            });
        });
    }
    // Search emails using X-GM-RAW (Gmail search syntax)
    async searchEmails(query, limit = 10) {
        return this.runImapOperation((imap, resolve, reject) => {
            imap.openBox("INBOX", true, (err) => {
                if (err) {
                    imap.end();
                    reject(err);
                    return;
                }
                // Use X-GM-RAW for Gmail search syntax
                imap.search([["X-GM-RAW", query]], (err, uids) => {
                    if (err) {
                        imap.end();
                        reject(err);
                        return;
                    }
                    if (!uids || uids.length === 0) {
                        imap.end();
                        resolve([]);
                        return;
                    }
                    const recentUids = uids.slice(-limit);
                    const emails = [];
                    const fetch = imap.fetch(recentUids, {
                        bodies: ["HEADER.FIELDS (FROM TO SUBJECT DATE)"],
                        struct: true,
                    });
                    fetch.on("message", (msg) => {
                        let uid = 0;
                        let headers = {};
                        const flags = [];
                        msg.on("body", (stream) => {
                            let buffer = "";
                            stream.on("data", (chunk) => {
                                buffer += chunk.toString("utf8");
                            });
                            stream.once("end", () => {
                                headers = Imap.parseHeader(buffer);
                            });
                        });
                        msg.once("attributes", (attrs) => {
                            uid = attrs.uid;
                            if (attrs.flags) {
                                flags.push(...attrs.flags);
                            }
                        });
                        msg.once("end", () => {
                            emails.push({
                                id: uid.toString(),
                                uid,
                                subject: headers.subject?.[0] || "(No Subject)",
                                from: headers.from?.[0] || "Unknown",
                                to: headers.to?.[0] || "",
                                date: headers.date?.[0] || "",
                                snippet: "",
                                labels: [],
                                isRead: flags.includes("\\Seen"),
                                isStarred: flags.includes("\\Flagged"),
                            });
                        });
                    });
                    fetch.once("error", (err) => {
                        imap.end();
                        reject(err);
                    });
                    fetch.once("end", () => {
                        imap.end();
                        resolve(emails.reverse());
                    });
                });
            });
        });
    }
    // Get full email content by UID
    async getEmailContent(uid) {
        return this.runImapOperation((imap, resolve, reject) => {
            imap.openBox("INBOX", true, (err) => {
                if (err) {
                    imap.end();
                    reject(err);
                    return;
                }
                const fetch = imap.fetch([uid], { bodies: "" });
                fetch.on("message", (msg) => {
                    let emailContent = null;
                    const flags = [];
                    msg.on("body", (stream) => {
                        simpleParser(stream, (err, parsed) => {
                            if (err) {
                                return;
                            }
                            // Use text body if available, otherwise fall back to HTML
                            const textBody = parsed.text?.trim() || "";
                            const htmlBody = parsed.html || "";
                            const body = textBody.length > 0 ? textBody : htmlBody;
                            emailContent = {
                                id: uid.toString(),
                                uid,
                                subject: parsed.subject || "(No Subject)",
                                from: parsed.from?.text || "Unknown",
                                to: Array.isArray(parsed.to) ? parsed.to.map(a => a.text).join(", ") : parsed.to?.text || "",
                                date: parsed.date?.toISOString() || "",
                                snippet: (parsed.text || "").substring(0, 200),
                                labels: [],
                                isRead: flags.includes("\\Seen"),
                                isStarred: flags.includes("\\Flagged"),
                                body,
                                attachments: (parsed.attachments || []).map((att) => ({
                                    filename: att.filename || "unknown",
                                    contentType: att.contentType || "application/octet-stream",
                                    size: att.size || 0,
                                })),
                            };
                        });
                    });
                    msg.once("attributes", (attrs) => {
                        if (attrs.flags) {
                            flags.push(...attrs.flags);
                        }
                    });
                    msg.once("end", () => {
                        // Wait a bit for parsing to complete
                        setTimeout(() => {
                            imap.end();
                            resolve(emailContent);
                        }, 100);
                    });
                });
                fetch.once("error", (err) => {
                    imap.end();
                    reject(err);
                });
                fetch.once("end", () => {
                    // Handled in message end
                });
            });
        });
    }
    // List all labels/folders
    async listLabels() {
        return this.runImapOperation((imap, resolve, reject) => {
            imap.getBoxes((err, boxes) => {
                if (err) {
                    imap.end();
                    reject(err);
                    return;
                }
                const labels = [];
                const extractLabels = (boxObj, prefix = "") => {
                    for (const name in boxObj) {
                        const fullPath = prefix ? `${prefix}/${name}` : name;
                        labels.push(fullPath);
                        if (boxObj[name].children) {
                            extractLabels(boxObj[name].children, fullPath);
                        }
                    }
                };
                extractLabels(boxes);
                imap.end();
                resolve(labels);
            });
        });
    }
    // Send email
    async sendEmail(to, subject, body, options) {
        try {
            const transport = this.getSmtpTransport();
            const mailOptions = {
                from: this.config.email,
                to,
                subject,
                [options?.html ? "html" : "text"]: body,
            };
            if (options?.cc)
                mailOptions.cc = options.cc;
            if (options?.bcc)
                mailOptions.bcc = options.bcc;
            if (options?.replyTo)
                mailOptions.replyTo = options.replyTo;
            if (options?.attachments && options.attachments.length > 0) {
                mailOptions.attachments = options.attachments.map((att) => ({
                    filename: att.filename,
                    path: att.path,
                    content: att.content,
                    encoding: att.encoding,
                }));
            }
            const result = await transport.sendMail(mailOptions);
            return {
                success: true,
                messageId: result.messageId,
            };
        }
        catch (error) {
            return {
                success: false,
                error: error instanceof Error ? error.message : "Unknown error",
            };
        }
    }
    // Reply to an email
    async replyEmail(uid, body, options) {
        const original = await this.getEmailContent(uid);
        if (!original) {
            return { success: false, error: "Original email not found" };
        }
        const subject = original.subject.startsWith("Re:")
            ? original.subject
            : `Re: ${original.subject}`;
        // Extract email address from "Name <email>" format
        const fromMatch = original.from.match(/<(.+)>/) || [null, original.from];
        const replyTo = fromMatch[1] || original.from;
        return this.sendEmail(replyTo, subject, body, {
            html: options?.html,
            replyTo: replyTo,
        });
    }
    // Mark email as read/unread
    async markAsRead(uid, read = true) {
        return this.runImapOperation((imap, resolve, reject) => {
            imap.openBox("INBOX", false, (err) => {
                if (err) {
                    imap.end();
                    reject(err);
                    return;
                }
                const operation = read ? imap.addFlags.bind(imap) : imap.delFlags.bind(imap);
                operation([uid], ["\\Seen"], (err) => {
                    imap.end();
                    if (err) {
                        reject(err);
                    }
                    else {
                        resolve(true);
                    }
                });
            });
        });
    }
    // Star/unstar email
    async starEmail(uid, starred = true) {
        return this.runImapOperation((imap, resolve, reject) => {
            imap.openBox("INBOX", false, (err) => {
                if (err) {
                    imap.end();
                    reject(err);
                    return;
                }
                const operation = starred ? imap.addFlags.bind(imap) : imap.delFlags.bind(imap);
                operation([uid], ["\\Flagged"], (err) => {
                    imap.end();
                    if (err) {
                        reject(err);
                    }
                    else {
                        resolve(true);
                    }
                });
            });
        });
    }
    // Delete email (move to trash)
    async deleteEmail(uid) {
        return this.runImapOperation((imap, resolve, reject) => {
            imap.openBox("INBOX", false, (err) => {
                if (err) {
                    imap.end();
                    reject(err);
                    return;
                }
                imap.move([uid], "[Gmail]/Trash", (err) => {
                    imap.end();
                    if (err) {
                        reject(err);
                    }
                    else {
                        resolve(true);
                    }
                });
            });
        });
    }
    // Apply label to email
    async applyLabel(uid, label) {
        return this.runImapOperation((imap, resolve, reject) => {
            imap.openBox("INBOX", false, (err) => {
                if (err) {
                    imap.end();
                    reject(err);
                    return;
                }
                imap.copy([uid], label, (err) => {
                    imap.end();
                    if (err) {
                        reject(err);
                    }
                    else {
                        resolve(true);
                    }
                });
            });
        });
    }
    // Download attachment from email
    async downloadAttachment(uid, filename) {
        return this.runImapOperation((imap, resolve, reject) => {
            imap.openBox("INBOX", true, (err) => {
                if (err) {
                    imap.end();
                    reject(err);
                    return;
                }
                const fetch = imap.fetch([uid], { bodies: "" });
                fetch.on("message", (msg) => {
                    let attachmentData = null;
                    msg.on("body", (stream) => {
                        simpleParser(stream, (err, parsed) => {
                            if (err) {
                                return;
                            }
                            // Find the attachment by filename
                            const attachment = (parsed.attachments || []).find((att) => att.filename === filename || att.filename?.toLowerCase() === filename.toLowerCase());
                            if (attachment) {
                                attachmentData = {
                                    filename: attachment.filename || "unknown",
                                    contentType: attachment.contentType || "application/octet-stream",
                                    size: attachment.size || 0,
                                    content: attachment.content.toString("base64"),
                                };
                            }
                        });
                    });
                    msg.once("end", () => {
                        // Wait a bit for parsing to complete
                        setTimeout(() => {
                            imap.end();
                            resolve(attachmentData);
                        }, 100);
                    });
                });
                fetch.once("error", (err) => {
                    imap.end();
                    reject(err);
                });
                fetch.once("end", () => {
                    // Handled in message end
                });
            });
        });
    }
    // List all attachments from an email
    async listAttachments(uid) {
        return this.runImapOperation((imap, resolve, reject) => {
            imap.openBox("INBOX", true, (err) => {
                if (err) {
                    imap.end();
                    reject(err);
                    return;
                }
                const fetch = imap.fetch([uid], { bodies: "" });
                fetch.on("message", (msg) => {
                    let attachments = [];
                    msg.on("body", (stream) => {
                        simpleParser(stream, (err, parsed) => {
                            if (err) {
                                return;
                            }
                            attachments = (parsed.attachments || []).map((att) => ({
                                filename: att.filename || "unknown",
                                contentType: att.contentType || "application/octet-stream",
                                size: att.size || 0,
                            }));
                        });
                    });
                    msg.once("end", () => {
                        // Wait a bit for parsing to complete
                        setTimeout(() => {
                            imap.end();
                            resolve(attachments);
                        }, 100);
                    });
                });
                fetch.once("error", (err) => {
                    imap.end();
                    reject(err);
                });
                fetch.once("end", () => {
                    // Handled in message end
                });
            });
        });
    }
    // Close connections
    async disconnect() {
        if (this.smtpTransport) {
            this.smtpTransport.close();
            this.smtpTransport = null;
        }
    }
}
//# sourceMappingURL=gmail-client.js.map