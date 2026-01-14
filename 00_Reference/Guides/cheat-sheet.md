# Obsidian AI Workflow - Cheat Sheet

## ⚡ Quick Commands

### Navigation
- `Ctrl/Cmd + O` → Quick switcher
- `Ctrl/Cmd + P` → Command palette
- `Ctrl/Cmd + Shift + F` → Global search
- `Ctrl/Cmd + D` → Daily note
- `Ctrl/Cmd + [` / `]` → Back/Forward

### Quick Capture
- `Ctrl/Cmd + Shift + I` → Capture prompt
- `Ctrl/Cmd + Shift + P` → Capture idea
- `Ctrl/Cmd + Shift + A` → Capture AI response

### Editing
- `Ctrl/Cmd + B` → Bold
- `Ctrl/Cmd + I` → Italic
- `Ctrl/Cmd + K` → Insert link
- `Ctrl/Cmd + Shift + V` → Paste without formatting
- `Ctrl/Cmd + Enter` → Follow link under cursor

## 📁 File Structure Quick Reference

```
0-Inbox/           → Quick capture
1-Projects/        → Active projects
2-Prompts/         → Prompt library
3-Knowledge/       → Learning resources
4-Reviews/         → Reviews & iteration
5-References/      → External resources
6-Templates/       → Reusable templates
7-Archive/         → Completed/old
```

## 🏷️ Tag System

### Project Types
- `#project/spec-generator`
- `#project/grammar-checker`
- `#project/custom-gpt`

### Content Types
- `#type/prompt`
- `#type/template`
- `#type/review`
- `#type/reference`

### Status
- `#status/active`
- `#status/review`
- `#status/completed`
- `#status/archived`

### AI Models
- `#ai/gpt-4`
- `#ai/claude`
- `#ai/gemini`
- `#ai/custom-model`

### Priority
- `#priority/high`
- `#priority/medium`
- `#priority/low`

## 🔍 Search Operators

### Basic Search
- `tag:#prompt` → All prompts
- `tag:#ai/gpt-4` → GPT-4 related
- `file:2024-12` → Files from December 2024

### Advanced Search
- `tag:#project tag:#status/active` → Active projects
- `tag:#ai-interaction date:2024-12-22` → Today's AI interactions
- `"Overall: 6"` → Find low-scoring outputs
- `path:"1-Projects"` → All project files

### Boolean Search
- `tag:#prompt OR tag:#template` → Prompts or templates
- `tag:#ai-interaction AND date:this-week` → This week's interactions
- `tag:#project NOT tag:#status/archived` → Non-archived projects

## 📊 Dataview Queries

### Active Projects
```dataview
table status, start_date, priority
from "1-Projects"
where status = "#status/active"
sort priority desc
```

### Recent AI Interactions
```dataview
table ai_model, project, date
from ""
where contains(tags, "#ai-interaction")
sort date desc
limit 10
```

### Prompts by Success Rate
```dataview
table category, model, success_rate
from "2-Prompts"
where success_rate >= 80
sort success_rate desc
```

### Today's Tasks
```dataview
task
from ""
where due = date(today)
```

## 📝 Template Variables

### Daily Template
- `{{date}}` → 2024-12-22
- `{{date:dddd}}` → Saturday
- `{{time}}` → 14:30

### Project Template
- `{{project_name}}` → Project name
- `{{category}}` → Project category
- `{{goal}}` → Project goal

### AI Interaction Template
- `{{title}}` → Interaction title
- `{{objective}}` → What you're trying to achieve
- `{{prompt}}` → The prompt used
- `{{response}}` → AI response

## 🎨 Markdown Formatting

### Headers
```markdown
# H1
## H2
### H3
#### H4
```

### Lists
```markdown
- Bullet point
1. Numbered list
- [ ] Checkbox
- [x] Checked box
```

### Code
```markdown
`inline code`

```language
code block
```
```

### Links & Embeds
```markdown
[[note-name]] → Internal link
[[note-name|display text]] → Aliased link
![[image.png]] → Embedded image
[external](https://...) → External link
```

### Callouts
```markdown
> [!note]
> Note callout

> [!warning]
> Warning callout

> [!tip]
> Tip callout

> [!important]
> Important callout
```

## 🔄 Workflows

### Morning Routine
1. `Ctrl + D` → Open daily note
2. Review dashboard
3. Set 3 priorities
4. Check active projects

### AI Interaction
1. Use AI tool
2. `Ctrl + Shift + I` → Capture prompt
3. `Ctrl + Shift + A` → Capture response
4. Evaluate quality
5. Link to project

### Project Work
1. `Ctrl + O` → Navigate to project
2. Review requirements
3. Document progress
4. Capture learnings
5. Update status

### Review Session
1. Search `tag:#ai-interaction date:this-week`
2. Evaluate outputs
3. Update prompt templates
4. Document improvements
5. Plan next iteration

## 🆘 Quick Troubleshooting

### "Can't find my notes"
→ Use `Ctrl + Shift + F` for global search
→ Check tag pane for organization
→ Use backlinks to see connections

### "Vault getting slow"
→ Archive old projects
→ Reduce file count in root
→ Use folders for organization

### "Forgot to capture something"
→ Use `Ctrl + D` to add to daily note
→ Search command palette for actions
→ Set up mobile sync for on-the-go

### "Templates not working"
→ Check Templater plugin is enabled
→ Verify template paths are correct
→ Use community plugins for advanced features

## 📱 Mobile Tips

### Sync Setup
1. Use Obsidian Sync (paid) or
2. Use Git + Working Copy (iOS) or
3. Use FolderSync (Android)

### Mobile Shortcuts
- Swipe down → Command palette
- Long press → Context menu
- Two-finger tap → Quick switcher

### Mobile Capture
- Use share sheet to capture from other apps
- Voice memos for quick thoughts
- Photos for visual references

## 🎓 Learning Resources

### Essential Plugins
- **Dataview** → Queries and automation
- **Templater** → Advanced templates
- **QuickAdd** → Quick capture
- **Calendar** → Daily notes

### Community Resources
- Obsidian Forum: https://forum.obsidian.md/
- Obsidian Discord: https://discord.gg/obsidianmd
- Reddit: r/ObsidianMD
- YouTube: "Obsidian Rocks" channel

### Advanced Topics
- **Graph view** → Visualize connections
- **Canvas** → Mind maps and diagrams
- **Plugins API** → Custom automation
- **CSS snippets** → Custom styling

## ✅ Daily Checklist

### Morning
- [ ] Open daily note
- [ ] Review dashboard
- [ ] Set priorities
- [ ] Check active projects

### During Work
- [ ] Capture all AI interactions
- [ ] Document prompts used
- [ ] Note quality observations
- [ ] Link related notes

### Evening
- [ ] Review accomplishments
- [ ] Update project status
- [ ] Capture learnings
- [ ] Plan tomorrow

## 📊 Progress Tracking

### Weekly Metrics
- AI interactions captured: ___
- Prompts tested: ___
- Projects progressed: ___
- Reviews completed: ___

### Monthly Review
- System usage consistency: ___/10
- Knowledge base growth: ___ notes
- Prompt library quality: ___/10
- Project completion rate: ___%

---

**Remember:** This is a living document. Update it as you learn and your workflow evolves!
