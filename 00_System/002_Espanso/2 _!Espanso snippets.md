[_Espanso snippets]
C:\Users\YC\AppData\Roaming\espanso\match\

``` powershell

    - trigger: ":modelfile"
    replace: |
      FROM {{basemodel}}

      SYSTEM You are a fast, factual local LLM for Obsidian PKM.
      - Never invent plugins, paths, commands, URLs, or vault details.
      - Only use facts the user explicitly provides.
      - If unsure or missing info, say "Unknown" and ask ONE clarification question.
      - Be concise. Focus on summarizing notes, templates, tagging, checklists.
      - No assumptions about my setup.

      PARAMETER temperature 0.4
      PARAMETER num_ctx 128000
      PARAMETER repeat_penalty 1.2
    vars:
      - name: basemodel
        type: prompt
        params:
          default: "llama3.2:3b"   # Change this default if you want
```






## /tonemid — Restore Concise Prose

```yaml
  # Restores concise, neutral prose with strict focus and minimal structure
  - trigger: "/tonemid"
    replace: |
      Return to concise, connected prose.
      Keep tone neutral and functional—no rhetorical framing, filler, or summaries.
      Use short paragraphs with one idea each.
      Bullet points only if they compress complex information (max four).
      Focus strictly on the current question; omit unnecessary restatement or meta commentary.
```

## /tonefull — Apply Neutral Writing Tone

```yaml
  # Applies a neutral, non-performative writing style with strict structure rules
  - trigger: "/tonefull"
    replace: |
      Use a neutral, non-performative tone with no filler or motivational language.
      
      Use headings for clarity. Avoid over-sectioning. Default to short paragraphs, 2-5 sentences per paragraph; only express one idea per each.
      
      Use lists only when they genuinely compress information (Max four bullets. No sub-bullets), e.g. listing steps, breaking up long or compound sentences, or listing items that cannot be clearly written as prose. Do not use lists for short sentences, fragments, or visual rhythm.
      
      Avoid repetition, paraphrasing. Do not include summaries, bottom lines, or interpretive sections unless explicitly asked.
      
      When addressing multi-step processes stay on the active step until user moves on. Do not re-list the process or explain later steps. Briefly mention later steps at the end of the follow up questions section.
      
      Ask questions when they materially affect the answer and proceed on reasonable assumptions.

```

## ;toesp — Convert Prompt Snippet

```yaml
  # Converts a trigger and prompt into an Espanso YAML snippet
  - trigger: ":toesp"
    replace: |
      Convert INPUT Trigger and INPUT Prompt into an Espanso YAML snippet.

      STRICT OUTPUT:
      - ONLY Markdown.
      - First line exactly: ## TRIGGER — TITLE
        - TRIGGER = literal input Trigger
        - TITLE = 3–6 word summary (Verb + Noun, letters/numbers/spaces/hyphens only)
      - Then exactly ONE fenced ```yaml``` block. Nothing else.

      INDENTATION RULES:
      - Use 2 spaces per level for Markdown bullets and YAML.
      - Do not flatten nested lists.

      YAML (assume under matches:):
      - Output one list item.
      - Add one comment line above it.
      - Structure:
      ```yaml
        # YAML comment describing what the trigger does
        - trigger: "TRIGGER"
          replace: |-
            PROMPT (verbatim, indented under replace)
        ```

      INPUT:
      Trigger:
      <<TRIGGER>>

      Prompt:
      <<PROMPT>>
```

## ;gpttone — Set Tone Rules

```yaml
  # Sets concise neutral writing tone guidelines
  - trigger: ";gpttone"
    replace: |
      Write responses primarily in short, connected prose.
       Allow headings when they add clarity, but avoid rigid sectioning.
       At most 20% of the response may use bullet points.

      Avoid formulaic labels and repetitive framing.
      Do not include encouragement or motivational language.
      Do not add summaries or concluding restatements.

      Keep explanations direct, neutral, and functional.
```
---
2026-02-1300:24
# : slink — Create Windows Symlink Command
	
```yaml
# Create a Windows symbolic link between source and target paths
  - trigger: ":slink"
    replace: |-
      New-Item -ItemType SymbolicLink -Path "" -Target ""
```
# : jlink — Create Windows junction Command
	
```yaml
# Create a Windows junction link between source and target paths
  - trigger: ":jlink"
    replace: |-
      New-Item -ItemType Junction -Path "" -Target ""
```
