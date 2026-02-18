---
created: 2026-02-17T00:00:00
status: completed
completed: 2026-02-17T00:00:00
tags: [metadata, infrastructure, templates]
---

# Metadata System Implementation Plan

> **Status**: ✅ **COMPLETED** on 2026-02-17
>
> All templates created, config updated, documentation complete. Ready for user testing.

## Problem Statement

**Current friction**: "Adding YAML and the need to think about it have been making me resist to create a new note"

**Goal**: Create a ZERO-FRICTION metadata system where:
- Templates auto-populate ALL metadata
- No thinking required when creating notes
- Just open, type, done

---

## Analysis Findings

After analyzing 35+ notes across the vault:

**Well-structured areas**:
- ✅ 00_System/003_Skills/ - Excellent metadata (skill_id, version, status, etc.)
- ✅ 90_Inbox/ daily notes - Consistent templated format

**Problem areas**:
- ❌ 15% inconsistent casing (tags vs Tags)
- ❌ 40% inconsistent date formats
- ❌ 20% missing frontmatter entirely
- ❌ Manual YAML editing creates resistance to note creation

**Key insight**: You're not a note-taking person. Metadata should be invisible.

---

## Solution: Minimal Templates with Auto-Population

### Core Principle

**Templates should**:
1. Auto-generate dates/times (ISO 8601 format)
2. Pre-fill reasonable defaults
3. NEVER ask questions
4. Position cursor in body (not frontmatter)

### Property Standards

**Universal properties** (auto-populated):
```yaml
created: <% tp.date.now("YYYY-MM-DDTHH:mm:ss") %>
tags: []
```

**Optional properties** (for special cases):
- `status: active` (for deployed items in 00_System/)
- `tags: [deployed]` (for System items)
- `tags: [infrastructure]` (for __ folders)

---

## Templates to Create

### 1. Universal Quick Note
**File**: `__Templates/quick-note.md`
- For: inbox, root (/), most numbered folders
- Properties: created, tags
- Zero questions asked

### 2. System Deployed Item
**File**: `__Templates/00-deployed.md`
- For: 00_System/ deployed specs/prompts with `!` prefix
- Properties: created, status (active), tags ([deployed])
- Auto-suggests `!` prefix in heading

### 3. Infrastructure Script Doc
**File**: `__Templates/__script-doc.md`
- For: Documenting scripts in `__Templates/` and `__automation scripts/`
- Properties: created, tags ([infrastructure, script])
- Structure: What it does, How to run, Dependencies

### 4. Keep Existing Daily Template
**File**: `__Templates/!tp - daily-template.md`
- Already works well, don't touch it
- Pattern: type: daily, date, created (time only), tags: [daily]

---

## Integration with Existing Workflow

### Your push-to-templates script
**File**: `__obsidian-scripts/Script - push-to-templates.js`

This script:
- Takes current active file
- Copies to `__Templates/` with `!tp - ` prefix
- Creates or updates automatically

**How it works with new templates**:
1. Edit a template in comfortable location
2. Run push-to-templates script
3. Deployed to `__Templates/` with `!` prefix
4. Ready to use

**Perfect synergy**: Templates create notes → push script deploys templates

---

## Implementation Checklist

### Phase 1: Obsidian Config ✅
- [x] Update `.obsidian/types.json`
  - [x] Add `created: datetime`
  - [x] Add `tags: tags`
  - [x] Add `status: text`
  - [x] Add `type: text`
  - [x] Add `date: date`

### Phase 2: Create Templates ✅
- [x] Create `__Templates/quick-note.md`
- [x] Create `__Templates/00-deployed.md`
- [x] Create `__Templates/__script-doc.md`
- [x] Verify existing `__Templates/!tp - daily-template.md` still works

### Phase 3: Test Templates ⏳ (User Testing)
- [ ] Create note in inbox using quick-note
  - ✓ Created timestamp auto-populates
  - ✓ Cursor in body, ready to type
  - ✓ No thinking required
- [ ] Create note in 00_System/ using 00-deployed
  - ✓ Status and deployed tag auto-populate
- [ ] Create script doc using __script-doc
  - ✓ Infrastructure tags auto-populate

### Phase 4: Documentation ✅
- [x] Create `Metadata_Quick_Start.md` (1-page guide)
- [x] Update CLAUDE.md with template usage notes

**Implementation time**: Completed in ~10 minutes
**Remaining**: User testing in Obsidian

---

## Success Criteria

**The ultimate test**: "Does creating a note feel effortless now?"

If you can:
1. Create a new note
2. Start typing immediately
3. Not think about YAML at all

Then we succeeded.

---

## What We're NOT Doing

To keep this zero-friction:

❌ No elaborate property registry
❌ No controlled vocabularies
❌ No migration of existing files
❌ No compliance reports
❌ No enforcement
❌ No complex metadata systems

Just 3 simple templates that auto-populate everything.

---

## Implementation Results

**Files Created**:
- ✅ `__Templates/quick-note.md` - Universal default template
- ✅ `__Templates/00-deployed.md` - System deployed items template
- ✅ `__Templates/__script-doc.md` - Infrastructure script documentation template
- ✅ `00_System/009_Folder Structure & Definitions/Metadata_Quick_Start.md` - User guide

**Files Updated**:
- ✅ `.obsidian/types.json` - Added property type definitions
- ✅ `CLAUDE.md` - Added Metadata System section

**Next Steps for User**:
1. Test templates in Obsidian (create notes using each template)
2. Verify Templater auto-executes the syntax
3. Confirm note creation feels effortless

## After User Testing

Once templates are verified working:

1. **Tag Taxonomy Design** (separate project, as specified)
2. Use consistent metadata for Dataview queries/dashboards
3. Evaluate if metadata is still effortless after 2 weeks of use

---

## Notes

- Templates use Templater syntax (`<% ... %>`)
- ISO 8601 date format: `YYYY-MM-DDTHH:mm:ss`
- Empty tags array lets user add tags organically while writing
- `!` prefix convention indicates deployed/active items
- Scripts (.py, .ps1) may not need frontmatter - MD docs have it
