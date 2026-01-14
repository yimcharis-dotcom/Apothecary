



### **A. Folder Structure: The Logical Foundation**

**Why This Structure Works:**

```
0-Dashboard/          # Always visible landing pages
1-Areas/              # Ongoing responsibilities (PARA method)
2-Resources/          # Reference material (Building knowledge)
3-Notes/              # Fleeting/temporary notes (Inbox system)
4-Archive/            # Closed items (Digital attic)
5-Templates/          # Note blueprints (Productivity multiplier)
6-Attachments/        # Files/images (Centralized media)
```

**Detailed Folder Rules:**

1. **0-Dashboard** (The Control Center)
    
    ```
    0-Dashboard/
    ├── Home.md                    # Main landing page (Ctrl+Home)
    ├── Weekly-Review.md           # Weekly planning template
    ├── Monthly-Goals.md           # Monthly objectives
    └── Quick-Links.md             # Custom link collection
    ```
    
    - **Rule**: Every note here must be actionable
    - **Tip**: Use `` as homepage in Settings → Core plugins → Homepage
    - **Trick**: Add `cssclass: dashboard` to YAML frontmatter for special styling
2. **1-Areas** (Your Life's Domains)
    
    ```
    1-Areas/
    ├── AI-Learning/              # Active AI projects
    │   ├── System-Spec-Generator/
    │   │   ├── 01-Requirements.md
    │   │   ├── 02-Architecture.md
    │   │   ├── 03-Test-Cases.md
    │   │   └── 04-Iteration-Log.md
    │   ├── Grammar-Checker/
    │   └── Custom-GPT-Projects/
    ├── Professional/             # Audit & Accounting
    │   ├── Client-Work/
    │   ├── Internal-Projects/
    │   └── Continuous-Learning/
    ├── Personal-Development/
    ├── Health/
    └── Finances/
    ```
    
    - **Rule**: Each area folder gets its own MOC (Map of Content)
    - **Tip**: Use numbering (01-, 02-) for logical order in file explorer
    - **Trick**: Create a `_README.md` in each folder explaining its purpose
3. **2-Resources** (Your Digital Library)
    
    ```
    2-Resources/
    ├── AI-Knowledge/
    │   ├── 01-Fundamentals/
    │   ├── 02-Advanced-Concepts/
    │   ├── 03-Tools-&-Frameworks/
    │   └── 04-Research-Papers/
    ├── Audit-&-Accounting/
    │   ├── Standards/            # GAAP, IFRS, etc.
    │   ├── Regulations/          # SOX, PCAOB, etc.
    │   ├── Methodologies/
    │   └── Case-Studies/
    ├── Prompt-Library/           # Detailed structure below
    ├── Code-Snippets/
    ├── Book-Notes/
    └── Course-Notes/
    ```
    
    - **Rule**: Never edit resource notes directly—always create linked working notes
    - **Tip**: Use Zettelkasten IDs: `YYYYMMDDHHMM-topic.md`
    - **Trick**: Add `source: [book/article/website]` in frontmatter
4. **3-Notes** (The Inbox System)
    
    ```
    3-Notes/
    ├── Daily-Notes/              # Auto-created with Calendar plugin
    │   ├── 2024-01-15.md
    │   └── 2024-01-16.md
    ├── Meeting-Notes/
    │   ├── Client-Meetings/
    │   └── Team-Meetings/
    ├── Idea-Inbox/               # Raw, unprocessed ideas
    │   ├── AI-Ideas/
    │   ├── Business-Ideas/
    │   └── Random-Thoughts/
    └── Temporary/                # Notes waiting to be filed
    ```
    
    - **Rule**: Process inbox notes within 24 hours
    - **Tip**: Use QuickAdd to send notes directly to appropriate inbox
    - **Trick**: Create a keyboard shortcut for "Move to Inbox"

## **PHASE 4: PROMPT LIBRARY MANAGEMENT**

### **Step 10: Prompt Organization System**

**Folder: `/2-Resources/Prompt-Library/`**

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