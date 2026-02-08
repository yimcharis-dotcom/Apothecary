declare const GMAIL_CATEGORIES: readonly ["primary", "social", "promotions", "updates", "forums"];
type GmailCategory = (typeof GMAIL_CATEGORIES)[number];
export interface EmailMessage {
    id: string;
    uid: number;
    subject: string;
    from: string;
    to: string;
    date: string;
    snippet: string;
    labels: string[];
    isRead: boolean;
    isStarred: boolean;
}
export interface EmailContent extends EmailMessage {
    body: string;
    attachments: Array<{
        filename: string;
        contentType: string;
        size: number;
    }>;
}
export interface AttachmentData {
    filename: string;
    contentType: string;
    size: number;
    content: string;
}
export interface GmailConfig {
    email: string;
    appPassword: string;
}
export declare class GmailClient {
    private config;
    private smtpTransport;
    constructor(config: GmailConfig);
    private createImapConnection;
    private getSmtpTransport;
    private runImapOperation;
    getEmailsByCategory(category: GmailCategory, limit?: number, dateFilter?: {
        after?: string;
        before?: string;
    }): Promise<EmailMessage[]>;
    getEmailsByLabel(label: string, limit?: number): Promise<EmailMessage[]>;
    searchEmails(query: string, limit?: number): Promise<EmailMessage[]>;
    getEmailContent(uid: number): Promise<EmailContent | null>;
    listLabels(): Promise<string[]>;
    sendEmail(to: string, subject: string, body: string, options?: {
        cc?: string;
        bcc?: string;
        html?: boolean;
        replyTo?: string;
        attachments?: Array<{
            filename: string;
            path?: string;
            content?: string;
            encoding?: string;
        }>;
    }): Promise<{
        success: boolean;
        messageId?: string;
        error?: string;
    }>;
    replyEmail(uid: number, body: string, options?: {
        html?: boolean;
    }): Promise<{
        success: boolean;
        messageId?: string;
        error?: string;
    }>;
    markAsRead(uid: number, read?: boolean): Promise<boolean>;
    starEmail(uid: number, starred?: boolean): Promise<boolean>;
    deleteEmail(uid: number): Promise<boolean>;
    applyLabel(uid: number, label: string): Promise<boolean>;
    downloadAttachment(uid: number, filename: string): Promise<AttachmentData | null>;
    listAttachments(uid: number): Promise<Array<{
        filename: string;
        contentType: string;
        size: number;
    }>>;
    disconnect(): Promise<void>;
}
export {};
//# sourceMappingURL=gmail-client.d.ts.map