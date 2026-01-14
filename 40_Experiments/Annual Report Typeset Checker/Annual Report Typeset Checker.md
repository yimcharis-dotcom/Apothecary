



You want a system that compares versions of typeset annual reports for listed companies and verifies their internal consistency and compliance. It should function like an automated reviewer that checks both text and numeric data in detail.

### Core functions
### Core, stable
- Identify and list textual and numerical changes between versions.
- Recalculate totals and subtotals.
- Cross-check related figures across statements and notes.
- Verify note numbering, page numbering, and references.
- Check required disclosures against a checklist.
### Intermediate, conditionally reliable
- Automated consistency map.
- Trend reconciliation across years.
- Terminology and policy comparison.
- Formatting audit.
- Tag and cross-link generation.
### Advanced, integration-oriented
- Disclosure completeness scoring.
- Exception dashboard.



### Workflow

You upload the prior and current report versions (likely PDFs) and a disclosure checklist. The tool anchors to a baseline version, detects and lists changes, recalculates sums, checks internal references, and generates a factual findings report. It doesn’t modify documents directly but produces a detailed comparison report suitable for quality control or audit review.

Would you like it to also verify formatting consistency (fonts, spacing, alignment), or should it stay limited to content and numeric validation?

### Interpretation of this requirement

The comparison logic must:

- Detect and align content by semantic structure (headings, tables, note references) rather than relying on layout.
- Normalize extracted text and numeric data to allow comparisons even when page layouts differ.
- Identify formatting changes when relevant (e.g., missing tables, note renumbering) but prioritize content accuracy.

If formatting alignment exists, it should take advantage of that to produce more precise location mapping (page and line references). If it doesn’t, it should fall back to contextual anchors such as note titles or captions.

Would you want it to cover multi-year comparisons and policy wording changes, or should it stay focused strictly on same-year version control?