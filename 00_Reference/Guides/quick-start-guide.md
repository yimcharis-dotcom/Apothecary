# Quick Start Guide - Obsidian AI Development Workflow

## 🚀 Immediate Setup (15 minutes)

### Step 1: Install & Create Vault
1. Download Obsidian from https://obsidian.md/
2. Create new vault: "AI-Dev-Wiki"
3. Copy this entire folder structure into your vault

### Step 2: Install Essential Plugins
```
Settings → Community Plugins → Browse → Install:

1. Advanced Tables
2. Dataview  
3. Templater
4. QuickAdd
5. Calendar
6. Tag Wrangler
7. Workspaces Plus
8. Commander
9. Hotkeys++
10. Paste URL into selection
```

### Step 3: Configure Hotkeys
```
Settings → Hotkeys → Set these:

Ctrl/Cmd + Shift + I → QuickAdd: Capture prompt
Ctrl/Cmd + Shift + P → QuickAdd: Capture idea  
Ctrl/Cmd + Shift + A → QuickAdd: Capture AI response
Ctrl/Cmd + D → Daily notes
Ctrl/Cmd + O → Quick switcher
Ctrl/Cmd + P → Command palette
Ctrl/Cmd + Shift + F → Global search
```

### Step 4: Create Vault Structure
Copy this structure in your vault:

```
AI-Dev-Wiki/
├── 0-Inbox/
│   ├── daily-capture.md
│   └── ideas.md
├── 1-Projects/
│   ├── system-spec-generator/
│   │   ├── index.md
│   │   ├── prompts/
│   │   ├── examples/
│   │   ├── reviews/
│   │   └── resources/
│   ├── grammar-checker/
│   │   ├── index.md
│   │   ├── prompts/
│   │   ├── examples/
│   │   ├── reviews/
│   │   └── resources/
│   └── custom-gpt-projects/
│       ├── index.md
│       └── [your-gpt-project]/
├── 2-Prompts/
│   ├── by-category/
│   │   ├── code-generation/
│   │   ├── technical-writing/
│   │   ├── analysis/
│   │   ├── creative/
│   │   └── problem-solving/
│   ├── by-model/
│   │   ├── gpt-4/
│   │   ├── claude/
│   │   ├── gemini/
│   │   └── custom-gpt/
│   ├── templates/
│   └── 0-Inbox/
├── 3-Knowledge/
│   ├── ai-concepts/
│   ├── tools-and-frameworks/
│   └── best-practices/
├── 4-Reviews/
│   ├── ai-output-reviews/
│   ├── project-retrospectives/
│   └── improvement-logs/
├── 5-References/
│   ├── bookmarks/
│   ├── articles/
│   └── code-snippets/
├── 6-Templates/
│   ├── daily-template.md
│   ├── project-template.md
│   ├── ai-interaction-template.md
│   ├── prompt-template.md
│   └── review-template.md
└── 7-Archive/
    ├── 2024/
    └── 2025/
```

## 📝 Daily Workflow (Simple Version)

### Morning (5 minutes)
```
1. Ctrl + D → Open daily note
2. Review yesterday's tasks
3. Write 3 priorities for today
4. Check dashboard for active projects
```

### During Work
```
When you use AI:
1. Copy the prompt → Ctrl + Shift + I
2. Copy AI response → Ctrl + Shift + A  
3. Add quick notes about quality
4. Link to project

When you have ideas:
1. Ctrl + Shift + P → Capture idea
2. Tag with relevant project
3. Expand later when you have time
```

### Evening (5 minutes)
```
1. Review what you accomplished
2. Update project status
3. Write 1-2 key learnings
4. Plan tomorrow's focus
```

## 🎯 Project-Specific Examples

### System Spec Generator Workflow

**Step 1: Create Project**
```
1. Navigate to 1-Projects/
2. Create folder: system-spec-generator
3. Copy project-template.md as index.md
4. Fill in basic info
```

**Step 2: Generate Spec**
```
1. Use AI to generate spec
2. Copy prompt: Ctrl + Shift + I
3. Copy response: Ctrl + Shift + A
4. Save in examples/
5. Review quality
```

**Step 3: Iterate**
```
1. Note improvements needed
2. Update prompt template
3. Test new version
4. Compare results
5. Document learnings
```

### Grammar Checker Workflow

**Step 1: Document Current Approach**
```
1. Create project in 1-Projects/grammar-checker/
2. Document current grammar rules
3. List test cases
4. Note accuracy issues
```

**Step 2: Prompt Engineering**
```
1. Create prompt variations in 2-Prompts/
2. Test each systematically
3. Document success rates
4. Keep best performers
```

**Step 3: Performance Tracking**
```
1. Create test dataset
2. Run grammar checker
3. Document results in reviews/
4. Track improvement over time
```

### Custom GPT Workflow

**Step 1: Specification**
```
1. Create project folder
2. Define GPT purpose
3. List capabilities needed
4. Document training approach
```

**Step 2: Training Data**
```
1. Create examples folder
2. Document good interactions
3. Note edge cases
4. Track data quality
```

**Step 3: Evaluation**
```
1. Create evaluation metrics
2. Test systematically
3. Document performance
4. Iterate based on results
```

## ⚡ Quick Capture Examples

### Prompt Capture (Ctrl + Shift + I)
```
"React Component Generator - Create clean, typed React components with TypeScript, error handling, and tests"
```

### Idea Capture (Ctrl + Shift + P)
```
"Idea: Use transformer model for grammar checking instead of rules-based approach - could handle context better"
```

### AI Response Capture (Ctrl + Shift + A)
```
"Generated user management system spec:
- Covers 10k concurrent users
- Includes RBAC
- Missing security details
- Good structure overall"
```

## 🔍 Quick Search Examples

### Find All Prompts for GPT-4
```
Search: tag:#prompt tag:#ai/gpt-4
```

### Find This Week's AI Interactions
```
Search: tag:#ai-interaction date:2024-12-22
```

### Find Active Projects
```
Search: tag:#status/active
```

### Find Reviews Needed
```
Search: tag:#review tag:#pending
```

## ⚙️ PowerToys/Espanso Setup

### PowerToys (Windows)
```
Add these shortcuts:

;prompt → [[2-Prompts/]]
;proj → [[1-Projects/]]
;review → [[4-Reviews/]]
;daily → [[{{date}}]]
;ai → Artificial Intelligence
;obs → Open Obsidian
```

### Espanso (Cross-platform)
Create file: `~/.config/espanso/match/obsidian.yml`

```yaml
matches:
  - trigger: ":prompt"
    replace: "[[2-Prompts/]]"
  
  - trigger: ":proj"
    replace: "[[1-Projects/]]"
  
  - trigger: ":daily"
    replace: "[[{{date}}]]"
    vars:
      - name: date
        type: date
        params:
          format: "%Y-%m-%d"
```

## 📊 Dashboard Queries

Create `0-Inbox/dashboard.md` with these queries:

```markdown
# AI Development Dashboard

## 🚀 Active Projects
```dataview
table status, start_date, priority
from "1-Projects"
where status = "#status/active"
sort priority desc
```

## 📝 Recent AI Interactions
```dataview
table ai_model, project, date
from ""
where contains(tags, "#ai-interaction")
sort date desc
limit 10
```

## 💡 Recent Prompts
```dataview
table category, model, version
from "2-Prompts"
where date >= date(today) - dur(7 days)
sort date desc
limit 5
```
```

## 🎓 Learning Path

### Week 1: Basic Setup
- [ ] Install Obsidian and plugins
- [ ] Create vault structure
- [ ] Set up daily notes
- [ ] Capture 5 AI interactions

### Week 2: Project Documentation
- [ ] Create first project
- [ ] Document AI workflow
- [ ] Create 3 prompt templates
- [ ] Review and iterate

### Week 3: Advanced Features
- [ ] Set up dataview queries
- [ ] Create automation scripts
- [ ] Build dashboard
- [ ] Link everything together

### Week 4: Optimization
- [ ] Review what's working
- [ ] Improve templates
- [ ] Create custom shortcuts
- [ ] Build knowledge base

## ✅ Success Checklist

### Daily Habits
- [ ] Open daily note every morning
- [ ] Capture all AI interactions
- [ ] Update project status
- [ ] Review and plan

### Weekly Habits
- [ ] Sunday review session
- [ ] Update prompt library
- [ ] Archive completed work
- [ ] Plan next week

### Monthly Habits
- [ ] Deep clean vault
- [ ] Review all prompts
- [ ] Update templates
- [ ] Backup everything

## 🆘 Troubleshooting

### Common Issues

**"I forget to capture things"**
→ Set phone reminders
→ Use voice capture
→ Keep Obsidian open

**"My vault is getting messy"**
→ Weekly cleanup sessions
→ Use tags consistently
→ Archive old projects

**"I can't find things quickly"**
→ Use search operators
→ Create dashboards
→ Improve linking

**"Templates are too complex"**
→ Start with simple ones
→ Add fields as needed
→ Customize for your workflow

## 🚀 Start Today

1. Install Obsidian
2. Create basic vault structure
3. Set up daily notes
4. Capture your first AI interaction
5. Don't worry about perfection - iterate!

**Remember:** The best system is the one you'll actually use. Start simple and build up!
