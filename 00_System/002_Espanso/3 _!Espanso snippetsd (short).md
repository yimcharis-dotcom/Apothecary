

matches:

---
  # --- AI reply speed ---
  - trigger: ";ans"
    replace: |
      Answers in order:
      1)
      2)
      3)

  - trigger: ";blk"
    replace: |
      Proceed with reasonable assumptions.
      Ask again only if something blocks progress.

  - trigger: ";def"
    replace: |
      Use defaults unless stated otherwise.

  - trigger: ";skip"
    replace: |
      Skip this for now. Continue.

  # --- AI roles ---
  - trigger: ";rolelint"
    replace: |
      ROLE: lint only. Do not rewrite. Report issues only.

  - trigger: ";rolerew"
    replace: |
      ROLE: rewrite. Preserve meaning. Do not change numbers.

  - trigger: ";rolefmt"
    replace: |
      ROLE: formatting only. No content changes.

  - trigger: ";rolespec"
    replace: |
      ROLE: system spec generator. Be explicit and unambiguous.

  # --- Safety / constraints ---
  - trigger: ";nonum"
    replace: |
      Do not change numbers, dates, or units.

  - trigger: ";verbatim"
    replace: |
      Quoted text must remain verbatim.

  - trigger: ";nodrift"
    replace: |
      Do not introduce new assumptions.

  - trigger: ";cite"
    replace: |
      Cite the rule or section for each issue.

  # --- Iteration markers ---
  - trigger: ";ai"
    replace: |
      AI:

  - trigger: ";ins"
    replace: |
      INSTRUCTION:

  - trigger: ";note"
    replace: |
      NOTE:

  - trigger: ";chg"
    replace: |
      CHANGE:

  - trigger: ";dec"
    replace: |
      DECISION:

  # --- Session control ---
  - trigger: ";short"
    replace: |
      Keep response concise. No explanations unless requested.

  - trigger: ";qs"
    replace: |
      Ask questions only if they materially affect the result.

  - trigger: ";go"
    replace: |
      Proceed now.

  # --- Diff / comparison ---
  - trigger: ";diff"
    replace: |
      Show changes only. Do not restate unchanged text.

  - trigger: ";track"
    replace: |
      Track changes explicitly. Before / After format.

  - trigger: ";sum"
    replace: |
      Summarize differences in bullets.

  # --- Learning / coding ---
  - trigger: ";why"
    replace: |
      Explain briefly why this works.

  - trigger: ";ex"
    replace: |
      Give one minimal example.

  - trigger: ";edge"
    replace: |
      List edge cases only.

  - trigger: ";fail"
    replace: |
      Common failure modes:

  # --- End-of-session extraction ---
  - trigger: ";keep"
    replace: |
      Final artifact:

  - trigger: ";ctx"
    replace: |
      Context:

  - trigger: ";out"
    replace: |
      Outcome:
---