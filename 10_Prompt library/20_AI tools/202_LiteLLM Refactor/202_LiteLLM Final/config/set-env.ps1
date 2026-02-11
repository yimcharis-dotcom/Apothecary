# API Keys from your vault-bridge
$env:XAI_API_KEY = "xai-ap3FR5Oo56oqBOAapUvEmH6XUKwL3bBysMNu5POmqRvkZedTDMMGdUs2KelXRQT43TD0nxRnZeaxRDMk"
$env:PERPLEXITY_API_KEY = "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"

# OpenAI (Standard API Key)
# $env:OPENAI_API_KEY = "sk-proj-..."

# Azure OpenAI (Subscription Key)
# $env:AZURE_API_KEY = "your-azure-api-key"

# ChatGPT Subscription (OAuth Token Storage)
# Directory to store OAuth tokens for ChatGPT Subscription auth
$env:CHATGPT_TOKEN_DIR = "C:\Users\YC\LiteLLM\tokens"

# Google AI Studio (Gemini)
$env:GEMINI_API_KEY = "AIzaSyCjYO48hmV10fmQP5y-TNKQp9MT7_tJcJc"

# OpenRouter
$env:OPENROUTER_API_KEY = "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"

# Master Key for LiteLLM Proxy (must match config.yaml)
$env:LITELLM_MASTER_KEY = "sk-litellm-master-key-12345"

# Database URL for Prisma (Required for SQLite cost tracking)
$env:DATABASE_URL = "file:C:/Users/YC/LiteLLM/litellm.db"

# Claude Code -> LiteLLM proxy
$env:ANTHROPIC_BASE_URL = "http://127.0.0.1:4000"
$env:ANTHROPIC_AUTH_TOKEN = "sk-litellm-master-key-12345"

Write-Host "? Environment variables set!"
