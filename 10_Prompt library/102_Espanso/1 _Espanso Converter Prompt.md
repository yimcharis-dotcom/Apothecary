
```
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
~~~yaml
  # YAML comment describing what the trigger does
  - trigger: "TRIGGER"
    replace: |
      PROMPT (verbatim, indented under replace)
~~~
 INPUT:
Trigger:
<<TRIGGER>>
	  
Prompt:
<<PROMPT>>
```

```
```