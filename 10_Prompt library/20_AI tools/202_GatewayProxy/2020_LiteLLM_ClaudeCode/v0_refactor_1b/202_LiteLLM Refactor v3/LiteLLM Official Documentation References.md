---
tags: [litellm, official-docs, references, documentation]
created: 2025-02-11
status: complete
---

# LiteLLM Official Documentation References

Complete reference to official LiteLLM documentation and resources for your setup.

## 📖 Core Documentation

### Main Docs
- **🏠 Official Website:** https://docs.litellm.ai/
- **📚 Getting Started:** https://docs.litellm.ai/docs/
- **⚡ Quick Start:** https://docs.litellm.ai/docs/simple_proxy
- **🐙 GitHub Repository:** https://github.com/BerriAI/litellm

### API Reference
- **🔗 Swagger API:** https://litellm-api.up.railway.app/
- **🤖 Model Cost Map:** https://github.com/BerriAI/litellm/blob/main/model_prices_and_context_window.json
- **💸 Live Cost Tracker:** https://models.litellm.ai/

## 🔧 Configuration & Setup

### Configuration Files
- **⚙️ Config.yaml Guide:** https://docs.litellm.ai/docs/proxy/configs
- **🔑 Environment Variables:** https://docs.litellm.ai/docs/proxy/enterprise
- **🌐 Proxy Deployment:** https://docs.litellm.ai/docs/proxy/quick_start
- **🐳 Docker Setup:** https://docs.litellm.ai/docs/proxy/docker_quick_start

### Authentication & Security
- **🔐 Virtual Keys:** https://docs.litellm.ai/docs/proxy/virtual_keys
- **🛡️ Guardrails:** https://docs.litellm.ai/docs/proxy/guardrails/quick_start
- **📋 User Management:** https://docs.litellm.ai/docs/proxy/users

## 💰 Cost Management & Tracking

### Spend Tracking
- **📊 Cost Tracking:** https://docs.litellm.ai/docs/proxy/cost_tracking
- **🏷️ Request Tags:** https://docs.litellm.ai/docs/proxy/request_tags
- **💸 Custom Pricing:** https://docs.litellm.ai/docs/proxy/custom_pricing
- **🧮 Pricing Calculator:** https://docs.litellm.ai/docs/proxy/pricing_calculator

### Budgets & Limits
- **💳 Budget Management:** https://docs.litellm.ai/docs/budget_manager
- **⏱️ Rate Limiting:** https://docs.litellm.ai/docs/proxy/users#set-rate-limits
- **📈 Usage Analytics:** https://docs.litellm.ai/docs/proxy/dynamic_logging

## 🔄 Model Management

### Auto-Sync & Updates
- **🔄 Auto-Sync Models:** https://docs.litellm.ai/docs/proxy/sync_models_github
- **🤖 Model Access:** https://docs.litellm.ai/docs/proxy/model_access_guide
- **📋 Supported Models:** https://docs.litellm.ai/docs/providers

### Routing & Load Balancing
- **🔄 Router Configuration:** https://docs.litellm.ai/docs/routing-load-balancing
- **⚖️ Load Balancing:** https://docs.litellm.ai/docs/routing-load-balancing
- **🔄 Fallbacks:** https://docs.litellm.ai/docs/routing-load-balancing
- **🧪 A/B Testing:** https://docs.litellm.ai/docs/traffic_mirroring

## 🚀 Advanced Features

### Enterprise
- **🏢 Enterprise Features:** https://docs.litellm.ai/docs/proxy/enterprise
- **📊 Billing & Invoicing:** https://docs.litellm.ai/docs/proxy/billing
- **🔧 Management CLI:** https://docs.litellm.ai/docs/proxy/management_cli
- **🔐 Secret Managers:** https://docs.litellm.ai/docs/secret_managers/overview

### Performance & Monitoring
- **📈 Caching:** https://docs.litellm.ai/docs/proxy/caching
- **📊 Logging & Metrics:** https://docs.litellm.ai/docs/proxy/dynamic_logging
- **⚡ Performance Tuning:** https://docs.litellm.ai/docs/benchmarks
- **🔍 Observability:** https://docs.litellm.ai/docs/observability/callbacks

### Specialized Gateways
- **🤖 A2A Agent Gateway:** https://docs.litellm.ai/docs/a2a
- **🔌 MCP Gateway:** https://docs.litellm.ai/docs/mcp

## 🔌 Integrations

### AI Tools Integration
- **🤖 Claude Code:** https://docs.litellm.ai/docs/ai_tools
- **🧠 LangChain:** https://docs.litellm.ai/docs/tutorials/langchain
- **🦜 LlamaIndex:** https://docs.litellm.ai/docs/tutorials/llamaindex

### Observability Platforms
- **📊 Langfuse:** https://docs.litellm.ai/docs/observability/langfuse_callback
- **🔭 Lunary:** https://docs.litellm.ai/docs/observability/lunary_callback
- **🌀 Helicone:** https://docs.litellm.ai/docs/observability/helicone_callback
- **📈 MLflow:** https://docs.litellm.ai/docs/observability/mlflow_callback

## 🛠️ Development & Troubleshooting

### Development
- **🔧 Local Development:** https://docs.litellm.ai/docs/extras/contributing_code
- **🧪 Testing:** https://docs.litellm.ai/docs/troubleshoot
- **🐛 Issue Reporting:** https://docs.litellm.ai/docs/troubleshoot/prisma_migrations

### Troubleshooting
- **🚨 Common Issues:** https://docs.litellm.ai/docs/troubleshoot
- **📝 Migration Guides:** https://docs.litellm.ai/docs/troubleshoot/prisma_migrations
- **🔍 Debug Mode:** Use `--detailed_debug` flag

## 🌐 Community & Support

### Getting Help
- **💬 Discord Community:** https://www.litellm.ai/support
- **🐛 GitHub Issues:** https://github.com/BerriAI/litellm/issues
- **📧 Support Email:** support@litellm.ai
- **📅 Calendar Booking:** https://calendly.com/d/4mp-gd3-k5k/litellm-1-1-onboarding-chat

### Social & Updates
- **🐦 Twitter:** https://twitter.com/LiteLLM
- **📝 Blog:** https://www.litellm.ai/blog
- **📈 Release Notes:** https://github.com/BerriAI/litellm/releases

## 📋 Quick Reference Cards

### Environment Variables
```bash
# Core
LITELLM_MASTER_KEY=sk-your-master-key
DATABASE_URL=sqlite:///path/to/litellm.db

# Auto-sync
LITELLM_MODEL_COST_MAP_URL=https://raw.githubusercontent.com/BerriAI/litellm/main/model_prices_and_context_window.json
LITELLM_LOCAL_MODEL_COST_MAP=true

# Debug
LITELLM_DEBUG=true
```

### Common API Endpoints
```bash
# Health check
GET /health

# Models list
GET /v1/models

# Spend tracking
GET /global/spend/report
GET /spend/logs

# Sync management
POST /reload/model_cost_map
POST /schedule/model_cost_map_reload?hours=6
GET /schedule/model_cost_map_reload/status
```

### Configuration Snippets
```yaml
litellm_settings:
  master_key: "sk-your-master-key"
  set_verbose: true
  drop_params: true
  track_cost: true

general_settings:
  database_url: "sqlite:///litellm.db"
  store_model_in_db: true

router_settings:
  model_group_alias:
    "gpt4": "openai/gpt-4"
    "claude": "anthropic/claude-3-sonnet"
```

## 🎯 Your Setup References

Your current configuration matches these official guides:

1. **📖 Startup Guide** → Official: https://docs.litellm.ai/docs/proxy/quick_start
2. **💰 Cost Tracking** → Official: https://docs.litellm.ai/docs/proxy/cost_tracking  
3. **🔄 Auto-Sync** → Official: https://docs.litellm.ai/docs/proxy/sync_models_github
4. **🤖 Model Config** → Official: https://docs.litellm.ai/docs/proxy/configs

## 📚 Learning Resources

### Tutorials
- **🚀 Quick Start Tutorial:** https://docs.litellm.ai/docs/proxy/docker_quick_start
- **📊 Budget Management:** https://docs.litellm.ai/docs/budget_manager
- **🔌 AI Tools Integration:** https://docs.litellm.ai/docs/ai_tools

### Best Practices
- **🛡️ Security Best Practices:** https://docs.litellm.ai/docs/proxy/virtual_keys
- **⚡ Performance Tips:** https://docs.litellm.ai/docs/benchmarks
- **💰 Cost Optimization:** https://docs.litellm.ai/docs/proxy/cost_tracking

## 🔄 Version Information

- **Current Stable:** Check [GitHub Releases](https://github.com/BerriAI/litellm/releases)
- **Your Version:** 1.81.1 (from installation docs)
- **Update:** `pip install --upgrade litellm[proxy]`

---

## 💡 Pro Tips

1. **📚 Bookmark Key Pages:** Save the main docs and Swagger API
2. **🔔 Enable Updates:** Watch GitHub repo for releases
3. **💬 Join Community:** Discord for real-time help
4. **🧪 Test Features:** Use demo.cloud.litellm.ai for testing
5. **📊 Monitor Costs:** Regular check-ins with spend tracking

## 🆘 Quick Help Commands

```powershell
# Check proxy status
curl http://localhost:4000/health

# View models
curl http://localhost:4000/v1/models

# Check spend
.\scr\view-spend.ps1

# Sync models
.\scr\sync-models.ps1

# Monitor logs
Get-Content "C:\Users\YC\LiteLLM\logs\proxy.log" -Tail 50
```

---

*This document is maintained as part of your LiteLLM setup. Check the official docs for the most current information.*