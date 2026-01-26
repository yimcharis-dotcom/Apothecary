### Key Points
- Research suggests Obsidian is an effective tool for building a personal wiki focused on AI learning, prompt libraries, and projects like system spec generators or custom GPTs, thanks to its flexible linking and plugin ecosystem.
- It seems likely that organizing notes atomically—with one idea per note—and using tags, folders, and backlinks will enhance quick retrieval for iterative AI work, though personal experimentation is key to refinement.
- Evidence leans toward using Espanso over PowerToys for quick prompt expansion, as PowerToys excels in utilities like quick launch but lacks native text expansion features.
- For reviewing AI outputs during iterations, an iterative workflow involving planning, implementation, testing, and evaluation helps catch issues early, with notes capturing metrics, failures, and improvements.
- Collecting prompts from open libraries like PromptBase or God of Prompt can accelerate projects, while storing them in Obsidian with metadata ensures easy versioning and reuse.

### Obsidian Setup Workflow
Start by downloading Obsidian from https://obsidian.md and installing it on your device. Create a vault by selecting a folder to store your notes—name it something like "AI Knowledge Base" for focus on your projects. Add initial notes for categories: one for AI concepts, one for prompts, and folders for specific projects like "System Spec Generator" or "Custom GPT." Install core plugins via Settings > Community Plugins, such as Dataview for querying notes and Templater for prompt templates. Use Markdown for formatting, and link notes with [[Note Title]] to build connections.

### Note-Taking During AI Iterations and Reviews
When iterating on projects like a grammar checker, jot down inputs, AI outputs, errors, and tweaks in dedicated notes—e.g., "Iteration 1: Prompt Test Results." Review AI work by comparing outputs against benchmarks, noting biases or inaccuracies, and logging improvements for the next cycle. For quick organization, use tags like #ai/prompt or #Project-Iteration, and backlinks to trace changes.

### Organizing, Saving, and Quick Access
Save notes automatically in your vault, organized by folders (e.g., /Prompts, /Projects) and tags for cross-referencing. For fast use, set up Espanso (download from https://espanso.org) to expand shortcuts like ":specgen" into full prompts. PowerToys can handle quick searches via PowerToys Run (Alt+Space), but for text expansion, Espanso is more direct—install it, edit config files for custom triggers.

### Sourcing and Storing Prompts
Gather prompts from free libraries like AI for Education (https://www.aiforeducation.io/prompt-library) or PromptBase (https://promptbase.com). In Obsidian, create a "/Prompt Library" folder with one note per prompt, including fields like description, variables, and examples—use YAML frontmatter for metadata to enable searches.




---
Setting up a personal wiki in Obsidian for AI learning, prompt management, and projects such as a system spec generator, grammar checker, or custom GPTs involves a structured yet flexible approach that leverages the app's Markdown-based, linked-note system. This setup transforms scattered ideas into an interconnected knowledge base, facilitating quick retrieval and iterative development. Below, we outline exhaustive, actionable workflows drawn from established practices in personal knowledge management (PKM) and AI project handling. These steps emphasize thoroughness, incorporating note-taking strategies, review processes, organization techniques, and tools for efficiency. We'll cover installation, configuration, note types, iteration logging, AI review methods, quick-access integrations, prompt sourcing, and additional note-worthy elements.

#### Step-by-Step Workflow: Setting Up Obsidian as a Personal Wiki
Obsidian excels as a free, local-first tool for building a wiki-like system, where notes link like Wikipedia pages, creating a "second brain" for AI-related work. Here's a detailed, exhaustive process:

1. **Download and Install Obsidian**: Visit the official site (https://obsidian.md) and download the installer for your OS (Windows, macOS, Linux, or mobile). Run the setup—it's lightweight and doesn't require an account. For sync across devices, use a cloud service like Dropbox or Git for the vault folder (avoid iCloud for potential conflicts).

2. **Create Your Vault**: Launch Obsidian and select "Create new vault." Choose a local folder (e.g., Documents/AI-Wiki) as the storage location. This vault holds all notes as plain Markdown (.md) files, ensuring portability and version control via tools like Git.

3. **Configure Basic Settings**: Go to Settings > Appearance to select a theme (e.g., Minimal for clean AI-focused work). Enable Safe Mode off to access plugins. Under Editor, turn on features like auto-pairing brackets for code snippets in prompts.

4. **Install Essential Plugins**: In Settings > Community Plugins > Browse, search and install:
   - **Dataview**: For querying notes, e.g., listing all #ai/prompt .
   - **Templater**: For creating reusable prompt templates.
   - **Calendar**: To track project iterations by date.
   - **Advanced URI**: For deep links to notes from external tools.
   - **File Organizer (or AI File Organizer 2000)**: Automates sorting AI-generated notes.
   Restart Obsidian after installations.

5. **Set Up Folder Structure**: Create folders like:
   - /AI-Concepts (for learning notes on models, algorithms).
   - /Prompt-Library (categorized subfolders: /System-Spec, /Grammar-Checker, /Custom-GPT).
   - /Projects (subfolders per project, e.g., /System-Spec-Generator with notes on specs, code, tests).
   - /Iterations (for logs and reviews).
   - /Resources (external links, PDFs).

6. **Implement Linking and Tagging**: Create a "Home" note as your wiki entry point with links like [[AI-Concepts/Index]]. Use tags (#Learning-AI, #Prompt-Engineering) for cross-cutting searches. Enable Graph View (icon in sidebar) to visualize connections—nodes represent notes, edges are links.

7. **Add Mobile Sync and Backups**: Install the Obsidian app on your phone. For backups, use Git: Initialize a repo in your vault folder (git init), commit regularly (git add . && git commit -m "Daily update").

8. **Test and Iterate**: Create sample notes, link them, and use Search (Ctrl/Cmd + P) to verify organization. Review weekly to refine structure.


<argument name="image_id">0</argument>
<argument name="size">SMALL</argument>
</grok:render> (Example of Obsidian's graph view showing linked notes for AI topics.)

#### What to Take as Notes: Exhaustive Categories for AI Learning and Projects
For AI learning and projects, adopt atomic note-taking—one focused idea per note—to avoid overwhelm and enable recombination. Key note types include:

- **Concept Notes**: Definitions, explanations (e.g., "Neural Networks: Basics" with diagrams, links to resources).
- **Experiment Notes**: Inputs/outputs from AI tools (e.g., "GPT Test: Grammar Checker Prompt V1" with code blocks).
- **Iteration Logs**: Timestamped entries on changes (e.g., "2025-12-22: System Spec Generator Iteration 3 – Fixed edge case").
- **Review Summaries**: Metrics like accuracy scores, qualitative feedback (e.g., "AI Output Review: Bias Detected in Response").
- **Prompt Notes**: Full prompts with variables (e.g., using YAML: type: grammar-checker, variables: [text]).
- **Resource Notes**: Summaries of articles, books, or videos (e.g., "Prompt Engineering Guide from OpenAI").
- **Meta-Notes**: Reflections on workflows (e.g., "Lessons from Custom GPT Project").

Additional elements: Always include timestamps, sources (e.g., via embeds), and tags for filtering. For projects, use MOCs (Maps of Content)—index notes linking related sub-notes.

| Note Type | Purpose | Example Content | Organization Tips |
|-----------|---------|-----------------|-------------------|
| Concept | Learning foundational AI | Definition, pros/cons, links to experiments | Tag #AI-Core; Folder: /AI-Concepts |
| Prompt | Storing reusable AI inputs | Full text, variables, example output | YAML frontmatter; Folder: /Prompt-Library/Subcategory |
| Iteration | Tracking project changes | Date, changes made, results | Daily notes with embeds; Folder: /Projects/ProjectName/Iterations |
| Review | Evaluating AI work | Metrics (e.g., accuracy 85%), improvements | Linked to iteration notes; Use Dataview queries |

#### Step-by-Step Workflow: Iterations, Reviewing AI Work, and Note-Taking
AI projects thrive on iteration, blending agile practices with systematic evaluation. Here's an exhaustive process:

1. **Plan Phase**: Define goals (e.g., "Improve grammar checker accuracy"). Note: Objectives, benchmarks (e.g., 90% error detection), resources needed. Create a new note: "Project-Plan: Grammar-Checker-V1."

2. **Implement Phase**: Build/test AI (e.g., run custom GPT). Note: Code/prompts used, initial outputs. Use code blocks in Obsidian for syntax highlighting.

3. **Test Phase**: Run edge cases. Note: Inputs, expected vs. actual outputs, errors (e.g., screenshots via embeds).

4. **Review Phase**: Evaluate quantitatively (metrics like precision/recall) and qualitatively (bias, coherence). Note: Scores, failures, insights. Use checklists: "Does it handle slang? Bias check?" Compare against baselines.

5. **Improve Phase**: Tweak based on review (e.g., refine prompt). Note: Changes, rationale. Link to previous iteration note.

6. **Document and Archive**: Summarize in a review note, archive old versions. Use Git for versioning.

7. **Retrospective**: Weekly, review all iterations. Note: Overall learnings, workflow adjustments.

Repeat cycles until goals met. For AI-specific reviews, check for hallucinations, ethical issues—log in dedicated "Ethics-Review" notes.

#### Organizing, Saving, Viewing, and Using Notes Quickly
- **Organize**: Folders for hierarchy, tags for themes, backlinks for relations. Use Dataview to create dynamic tables (e.g., query "LIST FROM 'Prompt-Library' WHERE type='grammar'").
- **Save**: Obsidian auto-saves; commit to Git for history.
- **View**: Sidebar for quick previews, Graph View for overviews, Search for full-text queries.
- **Use Quickly**: For prompts, copy-paste or integrate with Espanso. PowerToys' Run (Alt+Space) can launch Obsidian notes via shortcuts, but for expansion: Install Espanso, edit `config/default.yml` with matches like `- trigger: ":gramcheck" replace: "Full prompt text here"`. Type the trigger anywhere to expand. Alternatives: AutoHotkey on Windows for similar functionality.


<argument name="image_id">3</argument>
<argument name="size">SMALL</argument>
</grok:render> (Espanso expanding a text snippet, adaptable for AI prompts.)

#### How to Get Prompts and Use Obsidian to Store Them
Sourcing prompts: Start with free libraries—browse PromptBase for 240,000+ options (https://promptbase.com), God of Prompt for categorized collections (https://www.godofprompt.ai/prompt-library), or Claude's library (https://platform.claude.com/docs/en/resources/prompt-library/library). GitHub repos like EasyPrompt offer open-source ones (search "ChatGPT prompts GitHub"). For your projects, adapt from AI tools' examples (e.g., OpenAI playground).

Storing in Obsidian:
1. Create "/Prompt-Library" folder.
2. New note per prompt (e.g., "System-Spec-Generator-Prompt.md").
3. Use YAML frontmatter: `--- type: system-spec variables: [hardware, software] ---` followed by the prompt text, examples, and version history.
4. Tag and link: #prompt/system-prompt, link to project notes.
5. Query with Dataview: Embed tables of prompts in an index note.
6. Version: Duplicate notes for edits (e.g., V1, V2), or use Git diffs.
7. Integrate AI: Plugins like Obsidian-CoPilot can run prompts directly from notes.

#### What Else to Take as Notes
Beyond basics, capture:
- **Workflow Diagrams**: Mermaid code for flowcharts (e.g., AI project pipeline).
- **Tool Integrations**: Notes on APIs (e.g., "Custom GPT Setup with OpenAI API").
- **Ethical Considerations**: Potential biases in your grammar checker.
- **Performance Metrics**: Tables of benchmark results over iterations.
- **Inspirations**: Quotes from AI papers, linked to arXiv PDFs (embed via browse tools).
- **Failures Archive**: "What Went Wrong" notes to avoid repeats.
- **Collaboration**: If sharing, use Obsidian Publish for wiki export.

This comprehensive system evolves with use—review monthly to prune redundant notes and refine tags. By integrating these workflows, your Obsidian setup becomes a dynamic hub for AI innovation, balancing depth with accessibility.

### Key Citations
- [Master Life Management with a Personal Wiki in Obsidian](https://www.jordanrobison.net/p/creating-personal-wiki-obsidian-life-management)
- [Obsidian 101: How to Get Started and Stay Organized!](https://dev.to/proflead/obsidian-101-how-to-get-started-and-stay-organized-326b)
- [8 Must-Know Hacks for Academic Note Taking in Obsidian](https://effortlessacademic.com/8-must-know-hacks-for-academic-note-taking-in-obsidian/)
- [Espanso - A Privacy-first, Cross-platform Text Expander](https://espanso.org/)
- [Microsoft PowerToys - Windows Utilities for Power Users](https://learn.microsoft.com/en-us/windows/powertoys/)
- [Guide to Iterative Workflows: Steps & Best Practices](https://thedigitalprojectmanager.com/pmo/iterative-workflow-process/)
- [The AI Project Lifecycle: A Step-by-Step Guide for Project Managers](https://medium.com/%40sfells/the-ai-project-lifecycle-a-step-by-step-guide-for-project-managers-60255593c1f2)
- [Prompt Library — AI for Education](https://www.aiforeducation.io/prompt-library)
- [Biggest AI Prompt Library for ChatGPT & Midjourney - God of Prompt](https://www.godofprompt.ai/prompt-library)
- [AI Prompts | PromptBase: The #1 Marketplace for AI Prompts](https://promptbase.com/)
- [Anyone using Obsidian for AI prompt management?](https://www.reddit.com/r/ObsidianMD/comments/1hqiaz3/anyone_using_obsidian_for_ai_prompt_management/)
- [Where to store AI prompts: Comparing 4 common options](https://webtextexpander.com/blog/where-to-store-ai-prompts.html)