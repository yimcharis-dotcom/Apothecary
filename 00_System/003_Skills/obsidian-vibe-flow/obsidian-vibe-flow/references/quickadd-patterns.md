# QuickAdd Patterns for Vibe Coding Workflow

Reference for configuring Obsidian QuickAdd plugin to support the vibe coding workflow.

## Table of Contents

1. [QuickAdd Setup](#quickadd-setup)
2. [Capture Choices](#capture-choices)
3. [Macro Choices](#macro-choices)
4. [Recommended Hotkeys](#recommended-hotkeys)
5. [Advanced: Templater Integration](#advanced-templater-integration)

---

## QuickAdd Setup

### Installing QuickAdd

1. Open Obsidian Settings → Community Plugins → Browse
2. Search "QuickAdd" and install
3. Enable the plugin
4. Open QuickAdd settings

### Core Concepts

- **Capture**: Appends content to an existing note or creates a new note from a template
- **Template**: Creates a new note from a template file (simpler than Capture)
- **Macro**: Runs JavaScript code for complex operations

---

## Capture Choices

### Session Log Capture

Create a QuickAdd **Capture** choice:

| Setting | Value |
|---------|-------|
| Name | New Session Log |
| Type | Capture |
| Capture To | `Projects/{{VALUE:Project name}}/Sessions/Session-{{VALUE:Session number}}.md` |
| Template | `Templates/Session Log.md` |
| Create file if it doesn't exist | ✅ Yes |
| Open file after capture | ✅ Yes |

### Quick Decision Capture

For logging decisions during a coding session without leaving your editor:

| Setting | Value |
|---------|-------|
| Name | Quick Decision |
| Type | Capture |
| Capture To | `Projects/{{VALUE:Project}}/Decisions/ADR-{{DATE:YYMMDDHHmm}}.md` |
| Template | `Templates/Decision Record.md` |
| Create file if it doesn't exist | ✅ Yes |

### Session Append (Quick Note During Coding)

For adding quick notes to the current session while coding:

| Setting | Value |
|---------|-------|
| Name | Session Quick Note |
| Type | Capture |
| Capture To | Active file |
| Capture format | `\n- **{{DATE:HH:mm}}** — {{VALUE:Quick note}}` |
| Insert after | `## Issues Encountered` |

This lets you hotkey a quick note into your active session log without interrupting flow.

---

## Macro Choices

### New Session Macro

The `new-session.js` script auto-increments session numbers. To set it up:

1. Place `new-session.js` in your vault (e.g., `QuickAdd/scripts/new-session.js`)
2. In QuickAdd settings, create a new **Macro**
3. Click the ⚙️ gear icon to configure the macro
4. Add a **User Script** step
5. Select `new-session.js`
6. Save and assign to command palette or hotkey

**What the macro does:**
- Scans the Sessions folder to find the highest session number
- Increments by 1
- Asks which tools you're using
- Creates the note with all frontmatter pre-filled
- Opens the note

### Version Bump Macro

The `version-bump.js` script creates version snapshots. Setup:

1. Place `version-bump.js` in your vault
2. Create a new **Macro** in QuickAdd
3. Add **User Script** step pointing to `version-bump.js`
4. Save and assign trigger

**What the macro does:**
- Prompts for version number and summary
- Finds recent sessions to auto-link
- Creates version snapshot note
- Opens the note

### End-of-Session Macro

Create a composite macro that runs at the end of each coding session:

```javascript
/**
 * QuickAdd Macro: End Session
 * 
 * Prompts for session summary and updates the current session note.
 */

module.exports = async (params) => {
    const { app, quickAddApi } = params;
    
    // Get the active file (should be the current session note)
    const activeFile = app.workspace.getActiveFile();
    
    if (!activeFile || !activeFile.name.startsWith("Session-")) {
        // Find the most recent session note
        new Notice("⚠️ No session note open. Open your session note first.");
        return;
    }
    
    // Prompt for summary
    const built = await quickAddApi.inputPrompt("What did you build?");
    const nextSteps = await quickAddApi.inputPrompt("What's next session?");
    const techDebt = await quickAddApi.inputPrompt("Any tech debt? (leave blank if none)");
    
    // Read current content
    let content = await app.vault.read(activeFile);
    
    // Update "What I Built" section
    if (built) {
        content = content.replace(
            "## What I Built\n- ",
            `## What I Built\n- ${built}`
        );
    }
    
    // Update "Next Session" section
    if (nextSteps) {
        content = content.replace(
            "## Next Session\n- [ ] ",
            `## Next Session\n- [ ] ${nextSteps}`
        );
    }
    
    // Update "Tech Debt" section
    if (techDebt) {
        content = content.replace(
            "## Tech Debt Introduced\n- [ ] ",
            `## Tech Debt Introduced\n- [ ] ${techDebt}`
        );
    }
    
    await app.vault.modify(activeFile, content);
    new Notice("✅ Session note updated!");
};
```

---

## Recommended Hotkeys

Assign these in QuickAdd settings for fast access:

| Action | Suggested Hotkey | When to Use |
|--------|-----------------|-------------|
| New Session | `Ctrl/Cmd + Shift + S` | Start of coding session |
| Session Quick Note | `Ctrl/Cmd + Shift + N` | During coding, log a thought |
| Quick Decision | `Ctrl/Cmd + Shift + D` | When making architecture decision |
| End Session | `Ctrl/Cmd + Shift + E` | End of coding session |
| Version Bump | `Ctrl/Cmd + Shift + V` | Milestone reached |

---

## Advanced: Templater Integration

If you also use the Templater plugin, you can combine it with QuickAdd for more power.

### Auto-Calculate Session Number with Templater

Instead of the QuickAdd `{{VALUE}}` prompt, use Templater to auto-calculate:

```markdown
001
```

### Auto-Link Related Notes

Use Templater to auto-find and link related decision records:

```markdown
## Related Decisions

```

---

## Tips

**Start simple.** Begin with just the Session Log capture and add complexity as needed.

**Use the command palette.** If you forget hotkeys, all QuickAdd choices appear in `Ctrl/Cmd + P`.

**Combine with Daily Notes.** Add a link to your session in your daily note for easy cross-referencing.

**Mobile-friendly.** QuickAdd works on Obsidian Mobile — you can log quick thoughts from your phone.
