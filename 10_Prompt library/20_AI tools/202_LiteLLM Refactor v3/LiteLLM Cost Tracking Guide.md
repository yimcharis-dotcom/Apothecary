---
tags: [litellm, cost-tracking, spend-management, analytics, enterprise]
created: 2025-02-11
status: enhanced
docs: https://docs.litellm.ai/docs/proxy/cost_tracking
---

# LiteLLM Cost Tracking & Spend Management

Complete guide to tracking LLM costs, managing budgets, and analyzing usage across all your AI models.

## Quick Setup

Your LiteLLM proxy is already configured for cost tracking:

- ✅ **Database:** SQLite for spend logs (`C:\Users\YC\LiteLLM\litellm.db`)
- ✅ **Cost Tracking:** Enabled for all known models
- ✅ **User-Agent Tracking:** Automatic tool identification
- ✅ **Custom Tags:** Support for metadata tagging

## Understanding Cost Tracking

### How It Works

1. **Automatic Detection:** LiteLLM automatically calculates costs for 100+ models using the official [model cost map](https://github.com/BerriAI/litellm/blob/main/model_prices_and_context_window.json)
2. **Request Logging:** Every API call is logged with tokens, cost, and metadata
3. **Real-time Tracking:** Costs appear in response headers and database
4. **Multi-dimensional Analysis:** Track by API key, user, team, model, and custom tags

### Response Headers

Every successful request returns:
```http
x-litellm-response-cost: 0.000123
x-litellm-response-tokens: 150
```

## Available Scripts

### 1. View Global Spend
```powershell
.\scr\view-spend.ps1
```
Shows total spend across all models and API keys.

### 2. Daily Activity Report
```powershell
.\scr\view-daily-activity.ps1
```
Detailed breakdown by day, model, and API key.

### 3. User-Specific Spend
```powershell
.\scr\view-user-spend.ps1 -userId "your_username"
```
Track individual user usage.

## Advanced Cost Tracking

### Custom Tags

Track spend by project, department, or any custom category:

#### In Your Requests

**OpenAI Python:**
```python
response = client.chat.completions.create(
    model="grok-code-fast-1",
    messages=[{"role": "user", "content": "Hello"}],
    extra_body={
        "metadata": {
            "tags": ["project:web-app", "team:backend", "env:production"]
        }
    }
)
```

**Curl:**
```bash
curl http://localhost:4000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-litellm-master-key-12345" \
  -d '{
    "model": "grok-code-fast-1",
    "messages": [{"role": "user", "content": "Hello"}],
    "metadata": {
      "tags": ["project:web-app", "team:backend", "env:production"]
    }
  }'
```

#### Supported Tag Categories

- **Project Tracking:** `project:web-app`, `project:api-v2`
- **Team Identification:** `team:ml`, `team:backend`, `team:frontend`
- **Environment:** `env:prod`, `env:staging`, `env:dev`
- **Feature Flags:** `feature:experiment-123`, `feature:beta-test`
- **Cost Centers:** `cost-center:engineering`, `cost-center:research`

### Enterprise Features

#### Spend Reports by Group

**By Team:**
```bash
curl -X GET 'http://localhost:4000/global/spend/report?start_date=2025-01-01&end_date=2025-02-01&group_by=team' \
  -H 'Authorization: Bearer sk-litellm-master-key-12345'
```

**By Customer:**
```bash
curl -X GET 'http://localhost:4000/global/spend/report?start_date=2025-01-01&end_date=2025-02-01&group_by=customer' \
  -H 'Authorization: Bearer sk-litellm-master-key-12345'
```

#### User-Level Tracking

Track individual customer usage:
```python
# Set user identifier in request
response = client.chat.completions.create(
    model="grok-code-fast-1",
    messages=[{"role": "user", "content": "Hello"}],
    user="customer_12345"  # Track by customer ID
)
```

## Budget Management

### Setting Budgets

Create API keys with budget limits:

```bash
curl --location 'http://localhost:4000/key/generate' \
  -H 'Authorization: Bearer sk-litellm-master-key-12345' \
  -H 'Content-Type: application/json' \
  -d '{
    "max_budget": 10.00,
    "budget_duration": "monthly",
    "models": ["grok-code-fast-1", "perplexity-sonar-pro"]
  }'
```

### Budget Alerts

Configure alerts when usage exceeds thresholds:

```yaml
litellm_settings:
  budget_alerts:
    - threshold: 0.8  # 80% of budget
      email: "admin@company.com"
    - threshold: 1.0  # 100% of budget
      email: ["admin@company.com", "finance@company.com"]
      webhook: "https://hooks.slack.com/..."
```

## Cost Optimization Strategies

### 1. Model Selection

Choose cost-effective models per task:

| Task | Recommended Model | Cost (1M tokens) |
|------|-------------------|------------------|
| Coding | `grok-code-fast-1` | $0.50 |
| Reasoning | `grok-4-1-fast-reasoning` | $2.00 |
| Research | `perplexity-sonar-deep-research` | $1.00 |
| Quick Tasks | `grok-4-1-fast-non-reasoning` | $0.30 |

### 2. Caching

Enable response caching to reduce duplicate calls:

```yaml
general_settings:
  cache:
    type: "simple"  # or "redis"
    ttl: 3600       # 1 hour
```

### 3. Rate Limiting

Control usage and prevent cost spikes:

```yaml
general_settings:
  rate_limits:
    - rpm_limit: 100    # requests per minute
    - tpm_limit: 10000  # tokens per minute
```

## Monitoring & Alerts

### Real-time Monitoring

Access the LiteLLM UI:
```
http://localhost:4000/ui
```

View:
- Live usage dashboards
- Cost trends
- Model performance
- User activity

### Slack Integration

Set up Slack notifications for cost alerts:

```yaml
litellm_settings:
  slack_alerts:
    webhook_url: "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"
    alerts:
      - type: "daily_spend"
        threshold: 50.0
      - type: "model_usage"
        model: "grok-code-fast-1"
        threshold: 1000
```

## Database Schema

Your spend data is stored in SQLite:

### Key Tables

**LiteLLM_SpendLogs:**
```sql
CREATE TABLE LiteLLM_SpendLogs (
    id TEXT PRIMARY KEY,
    api_key TEXT,
    user TEXT,
    team_id TEXT,
    request_tags TEXT,
    model_group TEXT,
    api_base TEXT,
    spend REAL,
    total_tokens INTEGER,
    completion_tokens INTEGER,
    prompt_tokens INTEGER,
    created_at TIMESTAMP
);
```

**LiteLLM_VerificationToken:**
```sql
CREATE TABLE LiteLLM_VerificationToken (
    token TEXT PRIMARY KEY,
    spend REAL,
    max_budget REAL,
    user_id TEXT,
    team_id TEXT
);
```

## API Endpoints Reference

### Spend Tracking Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/global/spend/report` | GET | Global spend analytics |
| `/spend/logs` | GET | Individual transaction logs |
| `/user/info` | GET | User-specific usage |
| `/user/daily/activity` | GET | Daily breakdown |

### Examples

**Get Individual Logs:**
```bash
curl -X GET "http://localhost:4000/spend/logs?start_date=2025-02-01&summarize=false" \
  -H "Authorization: Bearer sk-litellm-master-key-12345"
```

**Get User Activity:**
```bash
curl -X GET "http://localhost:4000/user/daily/activity?start_date=2025-02-01&end_date=2025-02-10" \
  -H "Authorization: Bearer sk-litellm-master-key-12345"
```

## Best Practices

### 1. Tag Consistency
Use consistent tag naming:
- `project:frontend` (not `frontend-app`)
- `team:ml` (not `machine-learning`)

### 2. Regular Monitoring
Check spend daily:
```powershell
# Add to your daily routine
.\scr\view-spend.ps1
```

### 3. Budget Planning
Set quarterly budgets and monitor progress:
- Q1: $500 budget
- Q2: $750 budget (growth expected)
- Q3: $600 budget
- Q4: $1000 budget (year-end projects)

### 4. Cost Attribution
Always include cost center tags:
```python
"metadata": {
    "tags": [
        "cost-center:engineering", 
        "project:api-v2", 
        "sprint:sprint-23"
    ]
}
```

## Troubleshooting

### Missing Cost Data
1. Ensure `track_cost: true` in config
2. Check database connectivity
3. Verify model is in [cost map](https://github.com/BerriAI/litellm/blob/main/model_prices_and_context_window.json)

### Inaccurate Costs
1. Update model pricing: `.\scr\enable-auto-sync.ps1`
2. Check custom pricing configuration
3. Verify token counting method

### Database Issues
1. Check SQLite file permissions
2. Verify database URL in config
3. Run LiteLLM with `--detailed_debug` flag

---

## Official Documentation

- 📖 [Cost Tracking Docs](https://docs.litellm.ai/docs/proxy/cost_tracking)
- 🔗 [Model Cost Map](https://github.com/BerriAI/litellm/blob/main/model_prices_and_context_window.json)
- 🎯 [API Reference](https://litellm-api.up.railway.app/)
- 💬 [Community Support](https://discord.com/invite/wuPM9dRgDw)