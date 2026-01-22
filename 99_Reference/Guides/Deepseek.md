https://chat.deepseek.com/share/n5uzjkq1a7uty7h9r7

# **Comprehensive Obsidian Workflow: AI Learning, Prompt Library & Project Wiki**

## **PHASE 1: FOUNDATIONAL SETUP**

### **Step 1: Initial Obsidian Configuration**
1. **Download & Install Obsidian**
   - Get from https://obsidian.md
   - Create new vault named "AI-Workspace" in a cloud-synced folder (Dropbox, iCloud, or Obsidian Sync)

2. **Essential Core Settings**
   - Preferences → Editor:
     - Default editing mode: Live Preview
     - Strict line breaks: OFF
     - Tab indent size: 4
   - Files & Links:
     - New link format: [[Internal link]]
     - Automatically update internal links: ON
     - Use Wikilinks: ON
   - Appearance → Theme: Install "Minimal" or "Things" theme

3. **Critical Plugin Installation**
   - Core plugins to enable:
     - Templates
     - Daily notes
     - Backlinks
     - Outline
     - Quick switcher
     - Command palette
     - Tag pane
   - Community plugins to install:
     - Dataview (essential for databases)
     - Excalidraw (for diagrams)
     - QuickAdd (automation)
     - Calendar
     - Kanban (project tracking)
     - Tag Wrangler
     - Homepage (set dashboard as default)

### **Step 2: Folder Structure Creation**
```
AI-Workspace/
├── 0-Dashboard/          # Main landing pages
├── 1-Areas/              # Ongoing responsibilities
│   ├── AI-Learning/
│   ├── System-Spec-Generator/
│   ├── Grammar-Checker/
│   └── Custom-GPT-Projects/
├── 2-Resources/          # Reference material
│   ├── AI-Concepts/
│   ├── Prompt-Library/
│   ├── Code-Snippets/
│   ├── Research-Papers/
│   └── Tool-Documentation/
├── 3-Notes/              # Fleeting notes
│   ├── Daily-Notes/
│   ├── Meeting-Notes/
│   └── Idea-Inbox/
├── 4-Archive/            # Completed projects
├── 5-Templates/          # Note templates
└── 6-Attachments/        # Images, files
```

### **Step 3: Template Creation**
Create `/5-Templates/`

**1. AI-Project Template:**
```markdown
---
created: {{date}}
status: active/inactive/completed
type: project
tags: [ai-project, gpt, system]
related: [[]]
---

# {{title}}

## Project Brief
- **Objective**: 
- **Success Metrics**: 
- **Timeline**: 

## Current Status
```dataview
TASK FROM [[{{title}}]] 
WHERE !completed
GROUP BY file.link
```

## Iteration Log
### {{date:YYYY-MM-DD}}
- **Changes Made**:
- **Results**:
- **Lessons**:

## Resources
- [[Related-Note-1]]
- [External Link](url)

## Prompts Used
```dataview
TABLE prompts FROM "2-Resources/Prompt-Library"
WHERE contains(project, "{{title}}")
```

---
```

**2. AI-Interaction Note:**
```markdown
---
interaction_date: {{date}}
model: GPT-4/Claude/LLaMA
context: system-spec/grammar-check/prompt-dev
tags: [ai-output, review-needed]
---

# Interaction with {{model}}

## Original Prompt
```prompt
{{Paste prompt here}}
```

## AI Response
```response
{{Paste response}}
```

## My Assessment
**Accuracy**: /10
**Usefulness**: /10
**Hallucinations Detected**: 
- [ ] None
- [ ] Minor
- [ ] Significant

**Improvements Needed**:
1. 
2. 
3. 

## Revised Version
```improved
{{Improved version if applicable}}
```

## Key Takeaways
- 
```

## **PHASE 2: AI LEARNING & DOCUMENTATION WORKFLOW**

### **Step 4: What to Document Systematically**

**A. For Each AI Model/Service:**
1. **Capability Matrix**
   - Strengths/weaknesses per task type
   - Cost per 1K tokens
   - Context window size
   - Update dates

2. **Performance Log**
   ```markdown
   ## GPT-4 Performance Log
   | Date | Task Type | Accuracy | Latency | Cost | Notes |
   |------|-----------|----------|---------|------|-------|
   | 2024-01-15 | Code gen | 9/10 | 3.2s | $0.06 | Excellent for Python |
   ```

**B. For Prompt Development:**
1. **Prompt Evolution Chain**
   ```
   Prompt v1 → Results → Analysis → Prompt v2
   ```
   Store each iteration with metadata:
   - Tokens used
   - Temperature setting
   - Exact output vs expected

2. **Prompt Testing Framework**
   ```markdown
   ## Prompt Test: {{Test Case}}
   
   **Inputs Tested**:
   - Edge case 1: [result]
   - Edge case 2: [result]
   
   **Failure Modes**:
   - 
   
   **Success Patterns**:
   - 
   ```

**C. For System Spec Generator Project:**
1. **Requirement Documentation**
   - User stories
   - Input/output specifications
   - Validation rules
   - Error handling expectations

2. **Test Cases**
   - Sample inputs
   - Expected outputs
   - Actual AI outputs
   - Variance analysis

### **Step 5: How to Review AI's Work**

**Create Review Checklists:**

1. **Accuracy Review Template:**
```markdown
## AI Output Review Checklist

### [ ] Fact Verification
- Cross-check statistics
- Verify technical specifications
- Confirm code syntax

### [ ] Logical Consistency
- Arguments follow logically
- No contradictory statements
- Complete reasoning chain

### [ ] Completeness Check
- All requirements addressed
- Edge cases considered
- Appropriate detail level

### [ ] Style Assessment
- Tone matches purpose
- Formatting consistent
- Readability score >70%

**Reviewer Notes**:
- 
**Action Items**:
- [ ] Request clarification
- [ ] Correct errors
- [ ] Improve prompt
- [ ] Archive as reference
```

2. **Create Dedicated Review Notes:**
   - Link to original interaction note
   - Add review metadata
   - Use tags: `#review-complete`, `#needs-followup`

### **Step 6: Iteration Documentation**

**For Each Project Iteration:**
1. **Version Control in Notes:**
```
System-Spec-Generator/
├── v0.1-Initial-Prototype.md
├── v0.2-Added-Validation.md
├── v0.3-UI-Improvements.md
└── v0.4-Performance-Optimization.md
```

2. **Iteration Note Structure:**
```markdown
# Iteration {{version}}

## Changes Implemented
1. 
2. 

## Performance Metrics
- Before: [metric]
- After: [metric]
- Delta: [% change]

## Problems Encountered
- 
## Solutions Found
- 

## Next Iteration Focus
1. 
2. 
```

## **PHASE 3: ORGANIZATION & RETRIEVAL SYSTEM**

### **Step 7: Quick Access Setup**

**A. Using Quick Switcher (Ctrl/Cmd + O):**
- Create aliases for frequently used notes
  ```yaml
  alias: ["ai-cheatsheet", "prompts", "gpt4-ref"]
  ```

**B. Dashboard Creation:**
Create `/0-Dashboard/Home.md`
```markdown
# AI Workspace Dashboard

## Today's Focus
```dataview
TABLE status FROM "1-Areas"
WHERE status = "active"
SORT file.ctime DESC
```

## Recent AI Interactions
```dataview
TABLE model, context FROM "3-Notes/Daily-Notes"
WHERE contains(tags, "ai-interaction")
SORT interaction_date DESC
LIMIT 5
```

## Prompt Library Quick Access
- [[System Specification Prompts]]
- [[Grammar Check Prompts]]
- [[Custom GPT Training Prompts]]

## Active Projects
- [[System Spec Generator]] - {{progress}}%
- [[Grammar Checker]] - {{progress}}%
```

**C. Tag System:**
```yaml
#project-status: active/on-hold/completed
#ai-model: gpt-4/claude-2/llama2
#review-status: needs-review/reviewed/approved
#priority: p1/p2/p3
#content-type: concept/project/resource/snippet
```

### **Step 8: Search & Retrieval Optimization**

**1. Saved Searches:**
```markdown
## Common Searches
- `tag:#ai-project and -status:completed`
- `"grammar check" path:2-Resources/Prompt-Library`
- `file:(2024-01) and tag:#review-needed`
```

**2. MOC (Map of Content) Notes:**
Create `/2-Resources/AI-Concepts/MOC-AI-Concepts.md`
```markdown
# AI Concepts Map

## Machine Learning
- [[Supervised Learning]]
- [[Unsupervised Learning]]

## NLP Concepts
- [[Transformer Architecture]]
- [[Attention Mechanism]]
- [[Tokenization]]

## Prompt Engineering
- [[Few-Shot Learning]]
- [[Chain-of-Thought]]
- [[Self-Consistency]]
```

**3. QuickAdd Configuration:**
Setup QuickAdd for:
- New AI interaction note
- Add to prompt library
- Daily review template
- Project status update

### **Step 9: PowerToys vs. Espanso Alternative**

**For Windows (PowerToys):**
1. **Install PowerToys** from Microsoft Store
2. **Configure PowerUser/Text Extractor:**
```
Snippet Examples:
- ;aiint → Creates AI interaction template
- ;prompt → Prompt template
- ;review → Review checklist
- ;spec → System spec template
```

**For All Systems (Obsidian Native):**
1. **Use Templates plugin** with hotkeys
2. **Set up QuickAdd macros:**
   - Macro 1: Capture AI output
   - Macro 2: Log prompt iteration
   - Macro 3: Create project update

## **PHASE 4: PROMPT LIBRARY MANAGEMENT**

### **Step 10: Prompt Organization System**

**Folder: `/2-Resources/Prompt-Library/`**

**1. Categorization:**
```
Prompt-Library/
├── 1-By-Function/
│   ├── Ideation-Prompts/
│   ├── Analysis-Prompts/
│   ├── Writing-Prompts/
│   └── Coding-Prompts/
├── 2-By-Project/
│   ├── System-Spec/
│   ├── Grammar-Check/
│   └── Custom-GPT/
├── 3-By-Model/
│   ├── GPT-4-Optimized/
│   ├── Claude-Optimized/
│   └── Open-Source-Optimized/
└── 4-Tested-Templates/
```

**2. Prompt Note Template:**
```markdown
---
prompt_name: "System Specification Generator v2"
model: GPT-4
temperature: 0.7
max_tokens: 2000
category: [system-spec, code-generation]
tags: [tested, production-ready]
version: 2.1
last_tested: {{date}}
success_rate: 92%
related: [[System Spec Project]]
---

# {{title}}

## Full Prompt
```prompt
You are a system specification generator. Given the following requirements:

{requirements}

Generate a comprehensive system specification including:
1. Architecture diagram description
2. API endpoints
3. Database schema
4. Security considerations
5. Scaling requirements

Format the output in Markdown with clear sections.
```

## Usage Instructions
1. Replace `{requirements}` with user needs
2. Set temperature between 0.5-0.8
3. Expect ~1500 tokens output

## Example Input
```
Requirements: A task management app for small teams
```

## Example Output
```markdown
# System Specification: Task Manager
## Architecture: Microservices...
```

## Performance Notes
- Works best with detailed requirements
- Add example for better formatting
- Include non-functional requirements for completeness

## Iteration History
- v1.0: Basic structure
- v1.5: Added security section
- v2.0: Improved formatting
- v2.1: Fixed hallucination issue

## Related Prompts
- [[Simplified Spec Generator]]
- [[Technical Spec Writer]]
```

**3. Prompt Testing Suite:**
Create test cases with:
- Input variations
- Expected output patterns
- Common failure modes
- Improvement suggestions

## **PHASE 5: WORKFLOW INTEGRATION**

### **Step 11: Daily Workflow**

**Morning (15 min):**
1. Open Daily Note (Ctrl/Cmd + N)
2. Review [[AI Workspace Dashboard]]
3. Check:
   - `tag:#review-needed`
   - `#priority:p1`
   - Latest AI interactions

**During Work:**
1. **AI Interaction:**
   - Use QuickAdd → "New AI Interaction"
   - Paste prompt & response
   - Apply review template
   - Link to related project

2. **Prompt Development:**
   - Create new prompt note
   - Test with 3 variations
   - Document results
   - Add to library

3. **Project Work:**
   - Update project note
   - Log iteration
   - Create tasks

**Evening Review (10 min):**
1. Tag all notes from day
2. Move ideas to appropriate folders
3. Update project statuses
4. Clean up inbox

### **Step 12: Weekly Review**

1. **Gather all weekly notes:**
```
```dataview
TABLE file.ctime as Date, tags FROM "3-Notes/Daily-Notes"
WHERE file.ctime >= date(today) - dur(7 days)
SORT file.ctime DESC
```

2. **Review Projects:**
   - Update progress percentages
   - Identify blockers
   - Plan next week

3. **Clean & Organize:**
   - Archive completed items
   - Update MOCs
   - Back up vault

### **Step 13: Integration with External Tools**

**For System Spec Generator:**
1. **Export/Import:**
   - Use Dataview to export specifications
   - Convert to JSON for APIs
   - Store in version control

2. **Git Integration:**
   - Link Obsidian to Git repository
   - Commit prompts as versioned assets
   - Track prompt changes

**For Grammar Checker:**
1. **Test Case Management:**
   - Create test suite in Obsidian
   - Export to CSV for automation
   - Import results back

## **PHASE 6: ADVANCED OPTIMIZATION**

### **Step 14: Automation with Dataview**

**Create Dynamic Views:**

1. **Active Projects Dashboard:**
```dataview
TABLE status, progress, deadline FROM "1-Areas"
WHERE status != "completed"
SORT deadline ASC
```

2. **Prompt Performance Tracker:**
```dataview
TABLE avg(success_rate) as "Avg Success", 
count(version) as "Versions" 
FROM "2-Resources/Prompt-Library"
GROUP BY category
```

3. **Review Backlog:**
```dataview
LIST FROM #review-needed
SORT file.mtime DESC
```

### **Step 15: Quick Retrieval Methods**

**1. Aliases for Everything:**
- `[[System Spec Generator|spec]]`
- `[[GPT-4 Prompt Guidelines|gpt4tips]]`

**2. Embedded Search Blocks:**
```markdown
## Unreviewed AI Outputs
```query
tag:#ai-output and -tag:#reviewed
```
```

**3. Use Obsidian URI Scheme:**
- `obsidian://open?vault=AI-Workspace&file=Dashboard`
- Create desktop shortcuts
- Integrate with other apps

### **Step 16: Backup & Sync Strategy**

1. **Local Backup:**
   - Git repository initialized in vault
   - Daily automatic commit script
   - Branch for experimental prompts

2. **Cloud Sync:**
   - Obsidian Sync or
   - iCloud/Dropbox with versioning
   - Weekly export to Markdown bundle

3. **Export Critical Data:**
   - Monthly export of prompt library
   - JSON backup of Dataview queries
   - Screenshots of important diagrams

## **IMMEDIATE ACTION PLAN**

**Day 1:**
1. Install Obsidian, create vault
2. Set up folder structure (Step 2)
3. Create 3 essential templates (Step 3)

**Day 2:**
1. Install critical plugins
2. Create Dashboard note
3. Set up Daily Notes

**Day 3:**
1. Migrate existing prompts
2. Create first project note
3. Test AI interaction template

**Week 1:**
- Establish morning/evening routine
- Build prompt library structure
- Configure QuickAdd for frequent actions

**Week 2:**
- Implement review system
- Create project-specific templates
- Set up backup system

**Ongoing:**
- Weekly review & cleanup
- Monthly optimization of workflows
- Quarterly knowledge audit

## **CRITICAL SUCCESS FACTORS**

1. **Consistency Over Perfection:** Daily brief notes beat weekly perfect ones
2. **Link Everything:** Every note should link to at least one other
3. **Review Religiously:** Untagged notes become useless quickly
4. **Iterate Templates:** Adjust templates monthly based on usage
5. **Backup Obsessively:** Your AI knowledge base is valuable IP

This system scales from simple note-taking to enterprise-level AI project management. Start with the core structure, then add complexity as needed. The key is maintaining the workflow daily until it becomes automatic.