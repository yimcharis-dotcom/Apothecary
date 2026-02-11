---
Tags:
  - Ai/integration
  - GitHub
  - Plugin
  - tokens
Created: 2026-01-08
---





## Fine-grained Personal Access Token (PAT)

**Purpose**: Grants scoped access to GitHub resources. Regenerate every 90 days for security.
**Token**:
```
 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
```
**Scopes**:
- **Read-only**: Dependabot alerts, actions, administration, artifacts, attestations, code, codespaces (metadata/lifecycle), commit statuses, custom repo properties, deployments, discussions, environments, issues, merge queues, metadata, pages, PRs, repo advisories/hooks, secret scanning (alerts/dismissals/bypass), secrets, security events.
- **Read/Write**: Codespaces secrets, workflows.

**Security**:
- Store in Obsidian's encrypted fields or env vars.
- Revoke if compromised: GitHub Settings > Developer settings > Personal access tokens.
- Usage: In scripts, use 
  
```
  curl -H "Authorization: token $TOKEN" https://api.github.com/user
```