# [[LLM Test Protocol]]

## Objective
Evaluate local LLM behavior inside Obsidian using Text Generator with fixed prompts and controlled settings.

## Rules
- Same plugin settings for all models
- Same prompts for all models
- Change only the model and quantization
- No prompt tweaking between models

## Plugin Settings
- Backend: Ollama
- Temperature: 0.7 (unless stated otherwise)
- Max tokens: 1024
- System prompt: Minimal / neutral

## Evaluation Dimensions
- Latency (time to first token and completion)
- Instruction adherence
- Output completeness
- Coherence and structure
- Hallucination risk
- Practical usability

## Rating Scale (Informal)
- Excellent
- Good
- Acceptable
- Poor
- Unusable
