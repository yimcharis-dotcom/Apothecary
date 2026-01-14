


**Purpose**  
Single control surface to track what has been tested, what is pending, and high-level conclusions without re-reading raw logs.

**Content**
# LLM Testing Index

## Environment
- OS: Windows 11
- Hardware: ThinkPad X1 Carbon Gen 9
- CPU: i5-1135G7 (4C / 8T)
- RAM: 16 GB
- Inference: CPU-only
- Runtime: Ollama
- Obsidian Plugin: Text Generator

## Plugin Under Test
- Text Generator (Ollama backend)

## Models Tested
| Model | Quant | Status | Notes |
|------|------|--------|------|
| Mistral 7B Instruct | Q4_K_M | Planned | Baseline |
| Qwen2.5 7B Instruct | Q4_K_M | Planned | |
| LLaMA 3.1 8B | Q4_K_M | Planned | |
| Phi-3 Medium | Q4 | Planned | |
| Gemma 2 9B | Q4 | Planned | |

## Task Categories
- Creative brainstorming (uncensored)
- General reasoning
- Light formal writing
- Exploratory coding / learning

## Current Focus
- Establish baseline model behavior
- Measure latency, coherence, instruction-following
