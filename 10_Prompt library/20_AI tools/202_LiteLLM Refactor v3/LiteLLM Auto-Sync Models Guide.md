---
tags: [litellm, auto-sync, model-updates, day-zero-launches, automation]
created: 2025-02-11
status: enhanced
docs: https://docs.litellm.ai/docs/proxy/sync_models_github
---

# LiteLLM Auto-Sync Models (Day-0 Launch Support)

Automatically keep your model pricing and context window data up to date without restarting your service. This enables zero-downtime support for new model launches.

## What is Auto-Sync?

When providers like OpenAI, Anthropic, or xAI release new models (e.g., GPT-5, Claude 4), LiteLLM needs the latest pricing and context window data to:

- Calculate accurate costs
- Set proper rate limits
- Configure token limits
- Enable new model features

**Auto-sync eliminates the need to restart your proxy** when new models are released.

## Benefits

✅ **Zero Downtime:** New models work immediately after release  
✅ **Accurate Pricing:** Always current cost calculations  
✅ **Set It & Forget It:** Configure once, run forever  
✅ **Day-0 Support:** Use new models the moment they launch  

## Quick Start

### Enable Auto-Sync (Recommended)

```powershell
# Schedule automatic sync every 6 hours
.\scr\enable-auto-sync.ps1
```

This configures LiteLLM to:
- Check GitHub every 6 hours for updates
- Update model pricing automatically
- Log successful syncs
- Continue running without restart

### Manual Sync

Force an immediate update:

```powershell
# One-time manual sync
.\scr\sync-models.ps1
```

## Available Scripts

### 1. Enable Auto-Sync
```powershell
.\scr\enable-auto-sync.ps1 [-Hours 6]
```

**Parameters:**
- `Hours` (default: 6) - Sync frequency in hours

**What it does:**
- Schedules periodic model cost map reloads
- Validates proxy is running
- Confirms sync schedule

### 2. Sync Models Now
```powershell
.\scr\sync-models.ps1
```

**What it does:**
- Forces immediate model pricing update
- Fetches latest data from GitHub
- Reports new models found
- Shows pricing changes

### 3. Check Sync Status
```powershell
.\scr\check-sync-status.ps1
```

**What it does:**
- Shows last sync time
- Displays next scheduled sync
- Reports sync success/failure rate
- Lists available models count

## Configuration Options

### Sync Frequency

Choose your sync schedule:

| Environment | Recommended Frequency | Command |
|-------------|---------------------|---------|
| Production | 6 hours | `.\scr\enable-auto-sync.ps1 6` |
| Development | 1 hour | `.\scr\enable-auto-sync.ps1 1` |
| Testing | 12 hours | `.\scr\enable-auto-sync.ps1 12` |

### Custom Cost Map URL

Use a custom model pricing source:

```powershell
# In set-env.ps1
$env:LITELLM_MODEL_COST_MAP_URL = "https://raw.githubusercontent.com/BerriAI/litellm/main/model_prices_and_context_window.json"
```

### Local Cost Map

Use a local file (air-gapped environments):

```powershell
# In set-env.ps1  
$env:LITELLM_LOCAL_MODEL_COST_MAP = "true"
```

Then place `model_prices_and_context_window.json` in your LiteLLM directory.

## API Endpoints

### Manual Sync
```bash
curl -X POST "http://localhost:4000/reload/model_cost_map" \
  -H "Authorization: Bearer sk-litellm-master-key-12345" \
  -H "Content-Type: application/json"
```

### Schedule Sync
```bash
curl -X POST "http://localhost:4000/schedule/model_cost_map_reload?hours=6" \
  -H "Authorization: Bearer sk-litellm-master-key-12345" \
  -H "Content-Type: application/json"
```

### Cancel Schedule
```bash
curl -X DELETE "http://localhost:4000/schedule/model_cost_map_reload" \
  -H "Authorization: Bearer sk-litellm-master-key-12345"
```

### Check Status
```bash
curl -X GET "http://localhost:4000/schedule/model_cost_map_reload/status" \
  -H "Authorization: Bearer sk-litellm-master-key-12345"
```

## What Gets Updated?

### Model Information
- **Pricing:** Input/output token costs
- **Context Windows:** Maximum token limits
- **Model Names:** Standardized naming conventions
- **Provider Info:** API endpoints and authentication

### Example Updates

**When xAI releases `grok-5`:**
- ✅ Pricing automatically updated
- ✅ Context window set correctly  
- ✅ Available immediately via proxy
- ✅ Cost tracking works from day 1

**When OpenAI updates `gpt-4o` pricing:**
- ✅ New rates applied immediately
- ✅ Historical costs remain accurate
- ✅ Budget calculations update automatically

## Sync Process

### 1. Data Source
LiteLLM fetches from the official repository:
```
https://github.com/BerriAI/litellm/blob/main/model_prices_and_context_window.json
```

### 2. Validation
- JSON structure validation
- Pricing sanity checks
- Duplicate model detection
- Version compatibility verification

### 3. Update Process
- In-memory updates (no restart needed)
- Database cache refresh
- Active request completion with old data
- New requests use updated data

### 4. Logging
```json
{
  "timestamp": "2025-02-11T10:30:00Z",
  "action": "model_cost_map_reload",
  "status": "success",
  "models_updated": 5,
  "new_models": ["grok-5-preview"],
  "pricing_changes": 12
}
```

## Monitoring Auto-Sync

### Check Last Sync
```powershell
# View sync logs
Get-Content "C:\Users\YC\LiteLLM\logs\proxy.log" | Select-String "model_cost_map_reload"
```

### Monitor New Models
```powershell
# Script to alert on new models
.\scr\monitor-new-models.ps1
```

### Verify Pricing Accuracy
```powershell
# Compare against expected costs
.\scr\verify-pricing.ps1 -Model "grok-code-fast-1"
```

## Troubleshooting

### Common Issues

**Sync Fails with Network Error:**
```powershell
# Check internet connectivity
Test-NetConnection github.com -Port 443

# Use proxy if needed
$env:HTTPS_PROXY = "http://company-proxy:8080"
```

**No New Models Detected:**
```powershell
# Force refresh
.\scr\sync-models.ps1

# Check current model count
curl http://localhost:4000/v1/models | ConvertFrom-Json | Measure-Object
```

**Pricing Seems Wrong:**
```powershell
# Check manual sync response
curl -X POST "http://localhost:4000/reload/model_cost_map" \
  -H "Authorization: Bearer sk-litellm-master-key-12345"
```

### Recovery Procedures

**If Sync Corrupts Data:**
```powershell
# Stop proxy
Stop-Process -Name litellm -Force

# Restart (loads fresh data)
.\scr\start-proxy.ps1
```

**If Schedule Stops Working:**
```powershell
# Reschedule
.\scr\enable-auto-sync.ps1

# Verify
.\scr\check-sync-status.ps1
```

## Best Practices

### 1. Production Setup
- Use 6-hour sync intervals
- Monitor sync success rates
- Set up alerts for sync failures
- Test sync in staging first

### 2. Development Setup  
- Use 1-hour sync intervals
- Check for new models daily
- Verify pricing after major releases

### 3. Security
- Validate JSON structure before applying
- Monitor for pricing anomalies
- Keep backup of known-good configuration

### 4. Performance
- Schedule syncs during low-traffic periods
- Monitor memory usage during sync
- Ensure sufficient disk space for logs

## Example Use Cases

### Day-0 Model Launch
When xAI announces `grok-5`:
```bash
# 10:00 AM - Model announced on Twitter
# 10:15 AM - LiteLLM team updates cost map
# 10:30 AM - Your auto-sync runs automatically  
# 10:31 AM - grok-5 available via your proxy
# 10:32 AM - Users start using grok-5 with accurate pricing
```

### Pricing Update Response
When OpenAI reduces GPT-4o pricing:
```bash
# Immediate: New pricing applied to all requests
# Historical: Old costs preserved in logs
# Budgets: All calculations use new rates
# Alerts: Cost spike alerts adjust automatically
```

---

## Official Documentation

- 📖 [Auto-Sync Docs](https://docs.litellm.ai/docs/proxy/sync_models_github)
- 📊 [Model Cost Map](https://github.com/BerriAI/litellm/blob/main/model_prices_and_context_window.json)
- 🔧 [API Reference](https://litellm-api.up.railway.app/)
- 💬 [Community Support](https://discord.com/invite/wuPM9dRgDw)