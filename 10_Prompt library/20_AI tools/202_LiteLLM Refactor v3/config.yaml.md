model_list:

# ========== GROK MODELS (X.AI) ==========
  
# Grok 4.1 - Fast with reasoning

- model_name: grok-4-1-fast-reasoning
    litellm_params:
      model: xai/grok-4-1-fast-reasoning
      api_key: os.environ/XAI_API_KEY

# Grok 4.1 - Fast without reasoning

- model_name: grok-4-1-fast-non-reasoning
    litellm_params:
      model: xai/grok-4-1-fast-non-reasoning
      api_key: os.environ/XAI_API_KEY

# Grok 4 - Fast with reasoning

- model_name: grok-4-fast-reasoning
    litellm_params:
      model: xai/grok-4-fast-reasoning
      api_key: os.environ/XAI_API_KEY

# Grok 4 - Fast without reasoning

- model_name: grok-4-fast-non-reasoning
    litellm_params:
      model: xai/grok-4-fast-non-reasoning
      api_key: os.environ/XAI_API_KEY

# Grok 4 - Stable version (July 9, 2024)

- model_name: grok-4-07-09
    litellm_params:
      model: xai/grok-4-07-09
      api_key: os.environ/XAI_API_KEY

# Grok Code - Optimized for coding

- model_name: grok-code-fast-1
    litellm_params:
      model: xai/grok-code-fast-1
      api_key: os.environ/XAI_API_KEY

# Grok 3 Beta

- model_name: grok-3-beta
    litellm_params:
      model: xai/grok-3-beta
      api_key: os.environ/XAI_API_KEY

# Grok 3 Mini Beta

- model_name: grok-3-mini-beta
    litellm_params:
      model: xai/grok-3-mini-beta
      api_key: os.environ/XAI_API_KEY

# Grok 2 - Image generation

- model_name: grok-2-image-1212
    litellm_params:
      model: xai/grok-2-image-1212
      api_key: os.environ/XAI_API_KEY

# Grok 2 - Vision (can read images)

- model_name: grok-2-vision-1212
    litellm_params:
      model: xai/grok-2-vision-1212
      api_key: os.environ/XAI_API_KEY

# ========== PERPLEXITY MODELS ==========

- model_name: perplexity-sonar
    litellm_params:
      model: perplexity/sonar
      api_key: os.environ/PERPLEXITY_API_KEY

- model_name: perplexity-sonar-pro
    litellm_params:
      model: perplexity/sonar-pro
      api_key: os.environ/PERPLEXITY_API_KEY

- model_name: perplexity-sonar-deep-research
    litellm_params:
      model: perplexity/sonar-deep-research
      api_key: os.environ/PERPLEXITY_API_KEY

- model_name: perplexity-sonar-reasoning-pro
    litellm_params:
      model: perplexity/sonar-reasoning-pro
      api_key: os.environ/PERPLEXITY_API_KEY

# ========== OPENAI MODELS (Via OpenRouter or API Key) ==========

# Note: ChatGPT Plus Subscription does NOT provide an API Key

# Use OpenRouter or purchase API credits at platform.openai.com
  
# - model_name: gpt-4o

# litellm_params

# model: openai/gpt-4o

# api_key: os.environ/OPENAI_API_KEY

# - model_name: gpt-4o-mini

# litellm_params

# model: openai/gpt-4o-mini

# api_key: os.environ/OPENAI_API_KEY

# - model_name: o1

# litellm_params

# model: openai/o1

# api_key: os.environ/OPENAI_API_KEY

# - model_name: o3-mini

# litellm_params

# model: openai/o3-mini

# api_key: os.environ/OPENAI_API_KEY

# ========== GOOGLE AI STUDIO (GEMINI) ==========

# Free tier available at aistudio.google.com

- model_name: gemini-2.0-flash
    litellm_params:
      model: gemini/gemini-2.0-flash
      api_key: os.environ/GEMINI_API_KEY

- model_name: gemini-1.5-pro
    litellm_params:
      model: gemini/gemini-1.5-pro
      api_key: os.environ/GEMINI_API_KEY

# ========== OPENROUTER MODELS ==========
  
- model_name: openrouter-claude-3-7-sonnet
    litellm_params:
      model: openrouter/anthropic/claude-3.7-sonnet
      api_key: os.environ/OPENROUTER_API_KEY

- model_name: openrouter-deepseek-r1
    litellm_params:
      model: openrouter/deepseek/deepseek-r1
      api_key: os.environ/OPENROUTER_API_KEY

- model_name: openrouter-gpt-4o
    litellm_params:
      model: openrouter/openai/gpt-4o
      api_key: os.environ/OPENROUTER_API_KEY

litellm_settings:
  master_key: "sk-litellm-master-key-12345"
  drop_params: true
  set_verbose: true

general_settings:
  database_url: "sqlite:///C:\Users\YC\LiteLLM\litellm.db" # Local SQLite for cost tracking
  store_model_in_db: true

general_settings:
  database_url: "sqlite:///C:\Users\YC\LiteLLM\litellm.db" # Local SQLite for cost tracking
  store_model_in_db: true
