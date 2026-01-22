# Complete Obsidian Workflow for AI Development & Personal Wiki

## Table of Contents
1. [Initial Setup & Configuration](#initial-setup--configuration)
2. [Vault Structure & Organization](#vault-structure--organization)
3. [Note-Taking Workflows](#note-taking-workflows)
4. [Prompt Library Management](#prompt-library-management)
5. [AI Project Documentation](#ai-project-documentation)
6. [Review & Iteration Systems](#review--iteration-systems)
7. [Quick Access & Productivity](#quick-access--productivity)
8. [Templates & Automation](#templates--automation)

---

## Initial Setup & Configuration

### Step 1: Install Obsidian & Essential Plugins

1. **Download Obsidian**
   - Visit https://obsidian.md/
   - Download for your OS (Windows/Mac/Linux)
   - Install and create new vault named "AI-Dev-Wiki"

2. **Install Core Community Plugins**
   ```
   Settings → Community Plugins → Browse
   
   Essential Plugins:
   - Advanced Tables
   - Dataview
   - Templater
   - QuickAdd
   - Calendar
   - Tag Wrangler
   - Workspaces Plus
   - Commander
   - Hotkeys++
   - Paste URL into selection
   - Regex Find/Replace
   - File Recovery
   ```

3. **Enable Core Plugins**
   ```
   Settings → Core Plugins
   
   Enable:
   - Tags (ON)
   - Daily notes (ON)
   - Command palette (ON)
   - Quick switcher (ON)
   - Starred (ON)
   - Search (ON)
   - Backlinks (ON)
   - Outgoing links (ON)
   - Tag pane (ON)
   - Page preview (ON)
   - Slides (ON)
   - Audio recorder (ON)
   ```

### Step 2: Configure Settings for AI Work

1. **Files & Links**
   ```
   Settings → Files & Links
   
   - Default location for new notes: "AI-Projects/0-Inbox"
   - New link format: "Relative path to file"
   - Use [[Wikilinks]]: ON
   - Detect all file extensions: OFF
   - Auto convert HTML: ON
   ```

2. **Hotkeys Setup**
   ```
   Settings → Hotkeys
   
   Assign these essential hotkeys:
   - Ctrl/Cmd + Shift + I → QuickAdd: Capture prompt
   - Ctrl/Cmd + Shift + P → QuickAdd: Capture idea
   - Ctrl/Cmd + Shift + A → QuickAdd: Capture AI response
   - Ctrl/Cmd + D → Daily notes
   - Ctrl/Cmd + O → Quick switcher
   - Ctrl/Cmd + P → Command palette
   - Ctrl/Cmd + Shift + F → Global search
   - Ctrl/Cmd + Shift + T → New tag
   ```

3. **Appearance & Themes**
   ```
   Settings → Appearance
   
   - Theme: "Minimal" (recommended for focus)
   - Base color scheme: Dark
   - Interface font: San Francisco/Segoe UI
   - Text font: JetBrains Mono (for code)
   - Font size: 14
   - Quick font size adjustment: ON
   ```

---

## Vault Structure & Organization

### Main Directory Structure

```
AI-Dev-Wiki/
├── 0-Inbox/                    # Quick capture
│   ├── daily-capture.md
│   └── temp-notes.md
├── 1-Projects/                 # Active projects
│   ├── system-spec-generator/
│   ├── grammar-checker/
│   └── custom-gpt-projects/
├── 2-Prompts/                  # Prompt library
│   ├── by-category/
│   ├── by-model/
│   └── templates/
├── 3-Knowledge/                # Learning resources
│   ├── ai-concepts/
│   ├── tools-and-frameworks/
│   └── best-practices/
├── 4-Reviews/                  # Review & iteration
│   ├── ai-output-reviews/
│   ├── project-retrospectives/
│   └── improvement-logs/
├── 5-References/               # External resources
│   ├── bookmarks/
│   ├── articles/
│   └── code-snippets/
├── 6-Templates/                # Reusable templates
│   ├── project-templates/
│   ├── prompt-templates/
│   └── review-templates/
└── 7-Archive/                  # Completed/old
    ├── 2024/
    └── 2025/
```

### File Naming Conventions

```
# Projects: YYYY-MM-DD-project-name-version
2024-12-22-system-spec-generator-v1.md
2024-12-23-grammar-checker-concept-v2.md

# Prompts: category-subcategory-purpose
prompt-code-review-js-react.md
prompt-technical-writing-api-docs.md

# Knowledge: topic-subtopic-level
ai-llm-prompt-engineering-advanced.md
tool-obsidian-dataview-queries.md

# Reviews: YYYY-MM-DD-review-project
2024-12-22-review-spec-generator.md

# Daily: YYYY-MM-DD
2024-12-22.md
```

### Tag System

```
# Project types
#project/spec-generator
#project/grammar-checker
#project/custom-gpt

# Content types
#type/prompt
#type/template
#type/review
#type/reference
#type/tutorial

# Status tags
#status/active
#status/review
#status/completed
#status/archived

# AI model tags
#ai/gpt-4
#ai/claude
#ai/gemini
#ai/custom-model

# Priority tags
#priority/high
#priority/medium
#priority/low

# Topic tags
#topic/prompt-engineering
#topic/code-generation
#topic/technical-writing
#topic/system-design
```

---

## Note-Taking Workflows

### Workflow 1: Daily Capture System

**Morning Setup (5 minutes)**
```
1. Open Daily Note (Ctrl/Cmd + D)
2. Add date and day
3. Copy daily template
4. Review yesterday's tasks
```

**Daily Template Structure**
```markdown
---
date: 2024-12-22
tags: #daily #ai-dev
mood: 
focus: 
---

# 2024-12-22 - Saturday

## 🎯 Today's Focus
- [ ] Project: 
- [ ] Learning: 
- [ ] Review: 

## 💡 Ideas Captured
- 

## 🤖 AI Interactions
### Prompts Used
- 

### Responses Reviewed
- 

### Improvements Noted
- 

## 📚 What I Learned
- 

## 🔄 Iterations Made
- 

## 📝 Notes & Thoughts
- 

## ✅ Completed
- 

## 📋 Tomorrow's Priority
- 
```

### Workflow 2: Project Documentation

**When starting new project:**

1. **Create Project Index**
   ```
   File: 1-Projects/system-spec-generator/index.md
   ```

2. **Project Template**
   ```markdown
   ---
   project: System Spec Generator
   start_date: 2024-12-22
   status: #status/active
   tags: #project/spec-generator #ai/gpt-4
   ---

   # System Spec Generator Project

   ## 🎯 Project Overview
   **Goal:** 
   **Problem:** 
   **Solution:** 

   ## 📋 Requirements
   - [ ] Requirement 1
   - [ ] Requirement 2

   ## 🏗️ Architecture
   - **Frontend:** 
   - **Backend:** 
   - **AI Model:** 
   - **Database:** 

   ## 🔄 Development Phases
   - [ ] Phase 1: 
   - [ ] Phase 2: 

   ## 📝 Key Decisions
   - Decision 1: 
   - Decision 2: 

   ## 📊 Metrics & Evaluation
   - Metric 1: 
   - Metric 2: 

   ## 🔗 Related Notes
   - [[prompt-spec-generation-template]]
   - [[review-spec-generator-2024-12-22]]

   ## 📁 Project Files
   - `main.py`
   - `prompts.json`
   - `README.md`
   ```

### Workflow 3: AI Interaction Logging

**Every AI interaction should be documented:**

```markdown
---
date: 2024-12-22
ai_model: GPT-4
tags: #ai-interaction #spec-generator
---

# AI Interaction - System Spec Generation

## 🎯 Objective
Generate technical specifications for user management system

## 💬 Prompt Used
```
You are a technical architect. Generate a detailed system specification for a user management system with the following requirements:
- Support 10,000 concurrent users
- Role-based access control
- OAuth integration
- Audit logging
```

## 🤖 AI Response
```
# User Management System Specification

## 1. Overview
This specification defines the architecture for a user management system...

## 2. Functional Requirements
- User registration and authentication
- Role-based access control (RBAC)
- OAuth 2.0 integration
- Comprehensive audit logging

## 3. Technical Architecture
- **Frontend:** React 18 with TypeScript
- **Backend:** Node.js with Express
- **Database:** PostgreSQL 15
- **Cache:** Redis
- **Authentication:** JWT tokens
```

## ✅ Quality Check
- [ ] Meets requirements
- [ ] Technically accurate
- [ ] Complete coverage
- [ ] Actionable

## 🔄 Iteration Notes
**Improvements needed:**
- Add database schema
- Include API endpoints
- Specify security measures

**Next iteration:**
- Include performance benchmarks
- Add monitoring specifications

## 📊 Evaluation
- **Accuracy:** 8/10
- **Completeness:** 7/10
- **Actionability:** 9/10
- **Overall:** 8/10

## 🔗 Related
- [[project-spec-generator]]
- [[prompt-spec-generation-v2]]
```

---

## Prompt Library Management

### Prompt Organization System

**Directory: 2-Prompts/**

```
2-Prompts/
├── by-category/
│   ├── code-generation/
│   ├── technical-writing/
│   ├── analysis/
│   ├── creative/
│   └── problem-solving/
├── by-model/
│   ├── gpt-4/
│   ├── claude/
│   ├── gemini/
│   └── custom-gpt/
└── templates/
    ├── system-prompts/
    ├── few-shot-examples/
    └── prompt-chains/
```

### Prompt Template Structure

```markdown
---
category: code-generation
model: GPT-4
tags: #prompt #code #react
version: 1.0
tested: 2024-12-22
---

# Prompt: React Component Generator

## 🎯 Purpose
Generate clean, typed React components with best practices

## 📝 Prompt Template
```
You are an expert React developer. Create a React component based on these requirements:

**Component Name:** {{component_name}}
**Purpose:** {{purpose}}
**Props:** {{props}}
**Features:** {{features}}

Requirements:
- Use TypeScript
- Follow functional component pattern
- Include PropTypes or TypeScript interfaces
- Add basic styling with CSS modules
- Include error handling
- Write comprehensive comments

Generate:
1. Main component file
2. TypeScript types/interfaces
3. Basic test file
4. Usage example
```

## 🧪 Variables
- `{{component_name}}` - Name of the component
- `{{purpose}}` - What the component does
- `{{props}}` - Props the component accepts
- `{{features}}` - Specific features needed

## 💡 Example Usage
```
component_name: "UserProfileCard"
purpose: "Display user information in a card layout"
props: "user object with name, email, avatar"
features: "editable fields, save button, validation"
```

## 🔧 Parameters
- **Temperature:** 0.7
- **Max Tokens:** 2000
- **Top P:** 0.9

## ✅ Quality Checklist
- [ ] Component follows naming conventions
- [ ] TypeScript types are accurate
- [ ] Error handling included
- [ ] Tests are comprehensive
- [ ] Documentation is clear

## 🔄 Iteration History
- v1.0: Initial version
- v1.1: Added error handling requirements

## 📊 Performance
- **Success Rate:** 85%
- **Avg Quality Score:** 8.5/10
- **Best For:** CRUD components

## 🔗 Related Prompts
- [[prompt-react-form-generator]]
- [[prompt-typescript-interface]]
```

### Prompt Capture Workflow

**Using QuickAdd Plugin:**

1. **Setup QuickAdd Capture**
   ```
   Settings → QuickAdd → Manage Macros
   
   Add new capture:
   - Name: "Capture Prompt"
   - Capture to: "2-Prompts/0-Inbox/new-prompt.md"
   - Template: "6-Templates/prompt-capture-template.md"
   - Format: "{Date:YYYY-MM-DD-HHmm} - {value}"
   ```

2. **Capture Workflow**
   ```
   Hotkey: Ctrl/Cmd + Shift + I
   → Type prompt description
   → Automatically creates file with template
   → Fill in details later
   ```

---

## AI Project Documentation

### System Spec Generator Project Structure

```
1-Projects/system-spec-generator/
├── index.md                    # Project overview
├── requirements.md             # Requirements gathering
├── architecture.md             # Technical architecture
├── prompts/                    # Project-specific prompts
│   ├── initial-spec-prompt.md
│   ├── review-prompt.md
│   └── refinement-prompt.md
├── examples/                   # Example outputs
│   ├── user-management-spec.md
│   └── api-gateway-spec.md
├── reviews/                    # Review logs
│   ├── 2024-12-22-review.md
│   └── 2024-12-23-review.md
└── resources/                  # External resources
    ├── bookmarks.md
    └── references.md
```

### Grammar Checker Project Structure

```
1-Projects/grammar-checker/
├── index.md
├── language-rules.md           # Grammar rules database
├── prompt-evolution.md         # How prompts improved
├── test-cases.md              # Test scenarios
├── performance-metrics.md     # Accuracy tracking
├── reviews/
└── examples/
```

### Custom GPT Project Structure

```
1-Projects/custom-gpt-projects/
├── index.md
├── gpt-specifications.md       # Custom GPT configs
├── training-data.md           # Training datasets
├── evaluation-metrics.md      # Performance tracking
├── prompt-chains.md           # Multi-step prompts
├── integration-guides.md      # Implementation guides
└── [project-name]/            # Individual GPT projects
```

---

## Review & Iteration Systems

### AI Output Review Workflow

**File: 4-Reviews/ai-output-reviews/review-template.md**

```markdown
---
date: 2024-12-22
project: system-spec-generator
ai_model: GPT-4
review_type: quality-assurance
tags: #review #ai-output #spec-generator
---

# AI Output Review - System Spec Generator

## 📋 Review Summary
**Date:** 2024-12-22
**AI Model:** GPT-4
**Prompt Version:** v2.1
**Output Evaluated:** User Management System Spec

## ✅ Quality Metrics

### Accuracy (8/10)
- ✓ Technical details correct
- ✓ Follows industry standards
- ⚠ Missing security specifications
- ⚠ Database indexing not addressed

### Completeness (7/10)
- ✓ Covers main requirements
- ✓ Includes architecture overview
- ⚠ Missing edge cases
- ⚠ No performance benchmarks

### Actionability (9/10)
- ✓ Clear implementation steps
- ✓ Specific technology choices
- ✓ Well-structured sections
- ⚠ Missing code examples

### Consistency (8/10)
- ✓ Follows template structure
- ✓ Consistent terminology
- ⚠ Some formatting inconsistencies

## 🔄 Improvement Areas

### Critical Issues
1. **Security Gap:** No authentication flow detailed
2. **Performance:** Missing load testing specs
3. **Scalability:** No horizontal scaling plan

### Minor Issues
1. **Formatting:** Inconsistent heading levels
2. **Clarity:** Some technical jargon unexplained
3. **Examples:** No code samples provided

## 📝 Iteration Notes

### Next Prompt Version (v2.2)
**Add to prompt:**
```
Additional requirements:
- Include detailed authentication and authorization flow
- Specify performance benchmarks (response time < 200ms)
- Address horizontal scaling for 10x growth
- Provide code examples for critical components
```

### Test Cases for Next Version
- [ ] Security requirements covered
- [ ] Performance metrics included
- [ ] Scalability plan present
- [ ] Code examples provided

## 📊 Comparison with Previous Versions

| Version | Accuracy | Completeness | Actionability | Overall |
|---------|----------|--------------|---------------|---------|
| v1.0    | 6/10     | 5/10         | 7/10          | 6/10    |
| v2.0    | 7/10     | 6/10         | 8/10          | 7/10    |
| v2.1    | 8/10     | 7/10         | 9/10          | 8/10    |

## 🎯 Action Items
- [ ] Update prompt template with security requirements
- [ ] Add performance testing specifications
- [ ] Create code example library
- [ ] Test v2.2 with 3 different system types

## 🔗 Related Reviews
- [[review-spec-generator-v2-0]]
- [[review-prompt-effectiveness-2024-12-21]]
```

### Weekly Review Process

**Every Sunday: 30-minute review session**

1. **Review AI Interactions**
   ```
   Search: #ai-interaction date:this-week
   → Evaluate quality trends
   → Identify improvement areas
   → Update prompt templates
   ```

2. **Project Progress Review**
   ```
   Check: 1-Projects/*/index.md
   → Update project status
   → Move completed items
   → Plan next week
   ```

3. **Prompt Library Maintenance**
   ```
   Review: 2-Prompts/
   → Archive outdated prompts
   → Update successful ones
   → Add new variations
   ```

4. **Knowledge Base Updates**
   ```
   Review: 3-Knowledge/
   → Add new learnings
   → Link related concepts
   → Update outdated info
   ```

---

## Quick Access & Productivity

### Using PowerToys (Windows) or Espanso

**PowerToys Setup (Windows):**

1. **Install PowerToys**
   ```
   Microsoft Store → PowerToys → Install
   ```

2. **Configure Text Replacement**
   ```
   PowerToys → Text Expander
   
   Add shortcuts:
   - ;ai → Artificial Intelligence
   - ;prompt → [[prompt-|]]
   - ;proj → [[1-Projects/]]
   - ;review → [[4-Reviews/]]
   - ;temp → [[6-Templates/]]
   - ;date → {YYYY-MM-DD}
   - ;time → {HH:mm}
   ```

3. **Quick Obsidian Shortcuts**
   ```
   ;ob → Open Obsidian
   ;daily → Open today's note
   ;inbox → Open 0-Inbox
   ;search → Focus search
   ```

**Espanso Setup (Cross-platform):**

1. **Install Espanso**
   ```bash
   # Windows
   winget install espanso
   
   # Mac
   brew install espanso
   
   # Linux
   sudo snap install espanso --classic
   ```

2. **Create Obsidian Package**
   ```yaml
   # ~/.config/espanso/match/obsidian.yml
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
     
     - trigger: ":ai"
       replace: "Artificial Intelligence"
   ```

### Quick Access Workflow

**Morning Routine (10 minutes):**
```
1. Win + R → obsidian (open vault)
2. Ctrl + D → Daily note
3. Review yesterday's tasks
4. Plan today's focus
```

**During Work:**
```
Quick Capture:
- Ctrl + Shift + I → Capture prompt idea
- Ctrl + Shift + P → Capture project thought
- Ctrl + Shift + A → Capture AI response

Navigation:
- Ctrl + O → Quick switcher to any note
- Ctrl + Shift + F → Search across all notes
- Ctrl + P → Command palette for actions
```

**End of Day:**
```
1. Review daily note
2. Update project status
3. Capture learnings
4. Plan tomorrow
```

### Dataview Queries for Quick Access

**Create Dashboard: 0-Inbox/dashboard.md**

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

## 🎯 Today's Tasks
```dataview
task
from ""
where due = date(today)
```

## 💡 Recent Prompts
```dataview
table category, model, version
from "2-Prompts"
where date >= date(today) - dur(7 days)
sort date desc
limit 5
```

## 🔍 Needs Review
```dataview
table review_date, project
from "4-Reviews"
where review_date <= date(today)
sort review_date asc
```
```

---

## Templates & Automation

### Essential Templates

**1. Project Start Template**
```markdown
---
project: {{project_name}}
start_date: {{date}}
status: #status/active
priority: #priority/medium
tags: #project/{{category}}
---

# {{project_name}}

## 🎯 Project Overview
**Goal:** {{goal}}
**Problem:** {{problem}}
**Solution:** {{solution}}

## 📋 Requirements Checklist
- [ ] {{requirement_1}}
- [ ] {{requirement_2}}
- [ ] {{requirement_3}}

## 🏗️ Technical Stack
- **Frontend:** 
- **Backend:** 
- **AI Model:** 
- **Database:** 
- **Other Tools:** 

## 🔄 Development Phases
### Phase 1: Setup & Research
- [ ] 

### Phase 2: Core Development
- [ ] 

### Phase 3: Testing & Refinement
- [ ] 

## 📊 Success Metrics
- Metric 1: 
- Metric 2: 

## 📝 Key Decisions Log
- [date] Decision: 
- [date] Decision: 

## 🔗 Related Resources
- 

## 📁 Files & Structure
```

**2. AI Interaction Template**
```markdown
---
date: {{date}}
time: {{time}}
project: {{project}}
ai_model: {{model}}
tags: #ai-interaction #{{project}}
---

# AI Interaction - {{title}}

## 🎯 Objective
{{objective}}

## 💬 Prompt
```
{{prompt}}
```

## 🤖 Response
```
{{response}}
```

## ✅ Quality Check
- [ ] Meets requirements
- [ ] Technically accurate
- [ ] Complete
- [ ] Actionable

## 🔄 Iteration Notes
**Improvements:**
- 

**Next version changes:**
- 

## 📊 Evaluation
- **Accuracy:** /10
- **Completeness:** /10
- **Actionability:** /10
- **Overall:** /10

## 🔗 Related
- 
```

**3. Prompt Template**
```markdown
---
category: {{category}}
model: {{model}}
tags: #prompt #{{category}}
version: 1.0
tested: {{date}}
---

# Prompt: {{title}}

## 🎯 Purpose
{{purpose}}

## 📝 Prompt Template
```
{{prompt_template}}
```

## 🧪 Variables
{{variables}}

## 💡 Example Usage
```
{{example}}
```

## 🔧 Parameters
- **Temperature:** 
- **Max Tokens:** 
- **Top P:** 

## ✅ Quality Checklist
- [ ] 

## 🔄 Iteration History
- v1.0: Initial version

## 📊 Performance
- **Success Rate:** %
- **Avg Quality Score:** /10

## 🔗 Related Prompts
- 
```

**4. Review Template**
```markdown
---
date: {{date}}
project: {{project}}
ai_model: {{model}}
review_type: {{type}}
tags: #review #{{project}}
---

# Review: {{title}}

## 📋 Review Summary
**Date:** {{date}}
**AI Model:** {{model}}
**Prompt Version:** {{version}}

## ✅ Quality Metrics

### Accuracy (/10)
- ✓ 
- ⚠ 

### Completeness (/10)
- ✓ 
- ⚠ 

### Actionability (/10)
- ✓ 
- ⚠ 

## 🔄 Improvement Areas

### Critical Issues
1. 

### Minor Issues
1. 

## 📝 Iteration Notes

### Next Version Changes
```
```

### Test Cases
- [ ] 

## 📊 Comparison
| Version | Accuracy | Completeness | Actionability | Overall |
|---------|----------|--------------|---------------|---------|

## 🎯 Action Items
- [ ] 

## 🔗 Related
- 
```

### Templater Automation

**Setup Templater Scripts:**

1. **Create Template Folder**
   ```
   6-Templates/templater-scripts/
   ```

2. **Daily Note Auto-creation**
   ```javascript
   // 6-Templates/templater-scripts/daily-note.js
   
   ```

3. **Project Index Generator**
   ```javascript
   // 6-Templates/templater-scripts/project-index.js
   
   ```

### QuickAdd Automation

**Setup QuickAdd Captures:**

1. **Prompt Capture**
   ```
   QuickAdd → Add Choice → Capture
   
   Name: "Capture Prompt"
   Capture to: "2-Prompts/0-Inbox/{{DATE:YYYY-MM-DD-HHmm}}-prompt.md"
   Template: "6-Templates/quick-prompt-template.md"
   Format: "{{VALUE}}"
   Hotkey: Ctrl + Shift + I
   ```

2. **Idea Capture**
   ```
   QuickAdd → Add Choice → Capture
   
   Name: "Capture Idea"
   Capture to: "0-Inbox/ideas.md"
   Format: "- {{DATE:YYYY-MM-DD HH:mm}} - {{VALUE}}"
   Hotkey: Ctrl + Shift + P
   ```

3. **AI Response Capture**
   ```
   QuickAdd → Add Choice → Capture
   
   Name: "Capture AI Response"
   Capture to: "0-Inbox/ai-responses.md"
   Format: "## {{DATE:YYYY-MM-DD HH:mm}}\n{{VALUE}}\n\n---\n"
   Hotkey: Ctrl + Shift + A
   ```

---

## Step-by-Step Daily Workflow

### Morning Routine (15 minutes)

1. **Open Daily Note**
   ```
   Ctrl + D → Create/Open today's note
   ```

2. **Review Dashboard**
   ```
   Open: 0-Inbox/dashboard.md
   → Check active projects
   → Review pending reviews
   → See recent AI interactions
   ```

3. **Plan Day**
   ```
   In daily note:
   → Add focus areas
   → List 3 main tasks
   → Check project priorities
   ```

### During Work

**Working on Spec Generator:**
```
1. Open project: Ctrl + O → "system-spec-generator"
2. Review requirements in index.md
3. Create new interaction: Ctrl + Shift + A
4. Document AI response with template
5. Update project progress
6. Capture learnings immediately
```

**Developing Grammar Checker:**
```
1. Navigate to grammar-checker project
2. Review test cases
3. Create new prompt variation
4. Test and document results
5. Update performance metrics
6. Log iteration decisions
```

**Custom GPT Work:**
```
1. Open custom-gpt project folder
2. Review GPT specifications
3. Document training data changes
4. Test prompt chains
5. Evaluate performance
6. Update integration guides
```

### Capture Everything

**Ideas (Ctrl + Shift + P):**
```
"Idea: Use transformer model for grammar checking instead of rules-based approach"
```

**Prompts (Ctrl + Shift + I):**
```
"Prompt: Code review for React performance optimization"
```

**AI Responses (Ctrl + Shift + A):**
```
Copy AI output directly with context
```

### Evening Routine (10 minutes)

1. **Review Daily Note**
   ```
   → Mark completed tasks
   → Add learnings
   → Capture insights
   ```

2. **Update Projects**
   ```
   → Move completed items
   → Update status tags
   → Plan next steps
   ```

3. **Prepare Tomorrow**
   ```
   → List 3 priorities
   → Set focus areas
   → Schedule reviews
   ```

---

## Weekly Maintenance Workflow

### Sunday Review Session (45 minutes)

1. **Project Review (15 min)**
   ```
   Search: #status/active
   → Update all project indices
   → Move completed to archive
   → Plan next week
   ```

2. **Prompt Library Review (15 min)**
   ```
   Review: 2-Prompts/
   → Test top 5 prompts
   → Archive outdated ones
   → Update success rates
   ```

3. **Knowledge Base Update (15 min)**
   ```
   Review: 3-Knowledge/
   → Add new learnings
   → Link related notes
   → Update outdated info
   ```

### Monthly Deep Clean (1 hour)

1. **Archive Old Projects**
   ```
   Move completed projects to 7-Archive/
   → Update all links
   → Create summary
   ```

2. **Review All Prompts**
   ```
   Evaluate every prompt:
   → Success rate > 70%?
   → Still relevant?
   → Needs update?
   ```

3. **Update Templates**
   ```
   Review: 6-Templates/
   → Improve based on usage
   → Add new templates
   → Remove unused ones
   ```

---

## Advanced Tips & Tricks

### Dataview Queries for AI Work

**Query 1: Find all prompts by success rate**
```dataview
table category, model, version, success_rate
from "2-Prompts"
where success_rate >= 80
sort success_rate desc
```

**Query 2: Recent AI interactions by project**
```dataview
table ai_model, date, file.name
from ""
where contains(tags, "#ai-interaction")
group by project
sort date desc
```

**Query 3: Projects needing review**
```dataview
table status, priority, start_date
from "1-Projects"
where status = "#status/review"
sort priority desc
```

**Query 4: Learning progress by topic**
```dataview
table topic, date, understanding_level
from "3-Knowledge"
where date >= date(today) - dur(30 days)
sort topic asc
```

### Search Operators for Quick Find

```
# Find prompts for specific model
tag:#prompt tag:#ai/gpt-4

# Find all reviews this week
tag:#review date:2024-12-22

# Find interactions with low scores
tag:#ai-interaction "Overall: 6"

# Find all active projects
tag:#status/active

# Find files by type and date
tag:#type/prompt file:(2024-12)
```

### Linking Strategy

**Always link:**
- AI outputs to prompts used
- Reviews to original outputs
- Projects to related prompts
- Learnings to projects
- Iterations to previous versions

**Example linking:**
```markdown
# In AI interaction note:
## 🔗 Related
- [[prompt-spec-generator-v2-1]] (prompt used)
- [[project-system-spec-generator]] (project)
- [[review-spec-output-2024-12-22]] (review)

# In project note:
## 📋 Recent Interactions
- [[ai-interaction-2024-12-22-0930]]
- [[ai-interaction-2024-12-21-1400]]
```

### Backup & Sync

**Recommended Setup:**

1. **Git-based backup**
   ```bash
   cd /path/to/vault
   git init
   git add .
   git commit -m "Initial vault setup"
   
   # Daily backup script
   #!/bin/bash
   cd /path/to/vault
   git add .
   git commit -m "Daily backup: $(date)"
   git push origin main
   ```

2. **Obsidian Sync (Paid)**
   ```
   Settings → Sync → Set up
   → Sync across devices
   → Version history
   → End-to-end encryption
   ```

3. **Manual Export**
   ```
   Weekly: Settings → Export → Markdown
   → Keep in cloud storage
   → Multiple format backup
   ```

---

## Summary Checklist

### Setup Complete ✓
- [ ] Obsidian installed with all plugins
- [ ] Vault structure created
- [ ] Hotkeys configured
- [ ] Templates created
- [ ] QuickAdd workflows set up
- [ ] PowerToys/Espanso configured

### Daily Workflow ✓
- [ ] Morning: Review dashboard, plan day
- [ ] During work: Capture everything
- [ ] Evening: Review, update, plan

### Project Management ✓
- [ ] Each project has index.md
- [ ] All AI interactions documented
- [ ] Prompts saved and tagged
- [ ] Reviews scheduled and completed

### Maintenance ✓
- [ ] Weekly review (Sunday)
- [ ] Monthly deep clean
- [ ] Regular backups
- [ ] Prompt library updates

### Quick Access ✓
- [ ] Dashboard with dataview queries
- [ ] Hotkeys for common actions
- [ ] Text expansion shortcuts
- [ ] Quick switcher proficiency

---

## Next Steps

1. **Start Small:** Begin with one project
2. **Build Habit:** Capture everything for 1 week
3. **Iterate:** Improve templates based on usage
4. **Expand:** Add more projects gradually
5. **Review:** Weekly reviews are crucial
6. **Share:** Export useful prompts to team

**Remember:** The system is useless without consistent use. Start with daily notes and project documentation, then expand as you see value.
