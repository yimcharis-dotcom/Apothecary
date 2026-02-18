---
created: 2026-02-17T00:00:00
status: active
tags: [metadata, infrastructure, guide]
---

# Metadata Quick Start

## Philosophy

**Metadata should be invisible** - templates auto-populate everything so you can just create notes and start typing.

---

## Templates Available

### 1. **quick-note.md** (Default)
**Use for**: Inbox, root (/), most folders
**What it does**: Adds timestamp + empty tags, positions cursor in body
**When**: Anytime you want to just dump thoughts

### 2. **00-deployed.md**
**Use for**: 00_System/ deployed specs/prompts
**What it does**: Adds "deployed" tag, "active" status, suggests `!` prefix
**When**: Documenting something that's running in production

### 3. **__script-doc.md**
**Use for**: `__Templates/` and `__automation scripts/`
**What it does**: Adds infrastructure tags, provides script doc structure
**When**: Documenting scripts that run directly from __ folders

### 4. **!tp - daily-template.md** (Existing)
**Use for**: Daily notes in 90_Inbox/
**What it does**: Full daily note structure with navigation
**When**: Creating daily notes (already configured)

---

## Decision Tree: Which Template?

```
Need to create a note?
├─ Daily note? → Use daily template
├─ Quick thought/dump? → Use quick-note
├─ Documenting deployed item? → Use 00-deployed
└─ Documenting a script? → Use __script-doc
```

---

## Properties Explained

### `created` (datetime)
- **Format**: `2026-02-17T14:30:00` (ISO 8601)
- **Auto-populated**: Templates insert current timestamp
- **You never need to think about this**

### `tags` (array)
- **Format**: `tags: []` or `tags: [tag1, tag2]`
- **Auto-populated**: Templates insert empty array or defaults
- **Add tags organically** as you write

### `status` (text)
- **Values**: `active`, `deprecated`, `archived`
- **Only for**: Deployed items in 00_System/
- **Auto-populated**: Defaults to `active` for deployed items

### `type` (text)
- **Values**: `daily`, `prompt`, `skill`, etc.
- **Only for**: Specific note types (daily notes, skills)
- **Usually optional**: Most notes don't need this

---

## Adding Properties Manually

If you want to add metadata to an existing note:

1. **In Obsidian**: Click the "Add property" button at the top of a note
2. **Type property name**: e.g., `tags`, `status`
3. **Enter value**: Obsidian suggests property types
4. **Done**: Property appears in frontmatter

**But honestly, just use templates for new notes.**

---

## Date Format Standard

**ISO 8601**: `YYYY-MM-DDTHH:mm:ss`

Examples:
- ✅ `2026-02-17T14:30:00` (full timestamp)
- ✅ `2026-02-17` (date only)
- ✅ `14:30` (time only, for daily notes)

**You don't need to remember this** - templates do it automatically.

---

## Integration with push-to-templates Script

Your existing `__obsidian-scripts/Script - push-to-templates.js` works perfectly:

1. Edit a template in a comfortable location
2. Run the push-to-templates script
3. It copies to `__Templates/` with `!tp - ` prefix
4. Template ready to use

**Templates create notes. Scripts deploy templates. Clean separation.**

---

## Success Criterion

**Does creating a note feel effortless?**

If you can:
1. Create a new note
2. Start typing immediately
3. Not think about YAML at all

Then we succeeded. ✅

---

## Next Steps

After you're comfortable with metadata:
1. **Tag Taxonomy Design** (separate project)
2. **Dataview Dashboards** (use consistent metadata for queries)
3. Evaluate if system still feels effortless after 2 weeks

---

## Files Reference

- Templates: `__Templates/`
- Implementation plan: `00_System/009_Folder Structure & Definitions/Metadata_Implementation_Plan.md`
- CLAUDE.md: Updated with metadata system notes
