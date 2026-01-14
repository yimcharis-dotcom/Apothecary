---
created: 2026-01-10 13:47
Type: project-plan
Tags:
  - Project/invoicing
  - Excel
  - Automation
  - Work-in-progress
---
#Excel 
## Core Workflow Concept #

**Tab 1 - Input Form** (like a PwC working paper style)

- Clean, simple data entry interface
- Dropdown menus for client selection, payment terms, etc.
- Maybe a "Draft" vs "Issue Invoice" button distinction
- Clear fields after submission or [ v] ]keep for quick duplicates?

**Tab 2 - Invoice Register** (the database)

- Gets populated automatically when form is submitted
- Columns: Invoice #, Status (Draft/Issued/Void/Paid), Date Issued, Client, Amount, PDF Link, etc.
- Maybe color-coding by status?

**Tab 3+ - Individual Invoice Tabs**

- Pre-numbered (INV-001, INV-002, etc.)
- Each gets populated from the form data
- Once "issued," the tab gets protected (read-only)

## Questions to think through:

**Pre-numbering & Tab Generation:**

- Do we pre-create like 50 blank invoice tabs upfront, or dynamically generate them? (VBA could do this, or we keep it simpler with pre-made tabs)
- At what trigger does an invoice move from "Draft" to "Issued" and lock down? A button click? Changing status in register?

**The "Issue" Action:**

- When you hit "Issue Invoice," it should: populate the next available invoice tab, mark it in the register, protect the sheet, generate PDF, store PDF link?
- Should issuing also auto-increment to the next invoice number in the form?

**Void Function:**

- Should void invoices stay visible but marked, or get hidden?
- Do you need to track void reasons?

**Bulk Actions:**

- What would you bulk process? Multiple invoices at once? Bulk PDF export? Bulk email?

**Technical approach:**

- Are you comfortable with VBA macros (gives us buttons, automation)? Or keep it formula-based with manual steps?

What's your priority order for features?