---

### **Part 2: Obsidian Architecture (Folder Structure)**

Create this exact folder structure. It separates "Learning" from "Building" and "Assets."

Markdown

```
00_Inbox            <-- Raw ideas, quick pastes from AI chats
10_Projects         <-- Active builds (System Spec Gen, Grammar Checker)
   11_Specs         <-- Your generators
   12_Grammar       <-- Your checker
   13_CustomGPTs    <-- Knowledge files for GPTs
20_Learning_AI      <-- Concepts (Transformers, RAG, quantization)
30_Prompt_Library   <-- The core asset (Modular prompts)
   31_Roles         <-- "Act as a Senior PM", "Act as a Python Expert"
   32_Formats       <-- "Markdown Table", "JSON", "Mermaid Chart"
   33_Chains        <-- Full prompt chains
40_Archives
99_System           <-- Templates, Scripts
```



### 🗄️ Obsidian Vault Structure

|Folder Name|Description & Purpose|Your Key Notes|
|---|---|---|
|**00_Inbox** 📥|**Temporary Holding Area:** Use the `Daily Note` here. Everything starts here: quick meeting notes, web clips, raw AI outputs.|`2025-12-22.md`|
|**10_Projects** 🚀|**Active Work:** Notes directly related to specific deliverables and clients.|`11_AI_Gen/System_Spec_Log.md`|
||**11_AI_Gen**|Your AI iteration logs (System Spec Generator, Grammar Checker).|
||**12_Audit_Clients**|Client-specific files, issues, and engagement summaries.|
|**20_Learning** 🧠|**Knowledge Base:** Structured concepts you are actively studying.|`21_AI_Concepts/RAG_Overview.md`|
||**21_AI_Concepts**|Deep dives into AI architectures (Transformers, RAG, etc.).|
||**22_Accounting_Standards**|Summaries and interpretations of GAAP/IFRS.|
|**30_Prompt_Library** 🧱|**The AI Asset:** Modular, atomic prompts for quick assembly.|`31_Roles/Role_Architect.md`|
||**31_Roles**|Prompts like "Act as a Senior PM."|
||**32_Formats**|Prompts like "Output must be a Markdown table."|
||**33_Chains**|Full, tested prompt sequences.|
|**40_Wiki_Topics** 💡|**Personal Wiki (MOCs):** Where your diverse interests live, using the **Map of Content (MOC)** method.|`MOC_Personal_Interests.md`|
|**99_System** ⚙️|**Automation & Utilities:** Files for consistency and speed.|`91_Templates/Project_Start.md`|
||**91_Templates**|Templates for new projects, clients, and learning notes (using the Templater plugin).|
||**92_Checklists**|Reusable checklists (e.g., audit steps, AI testing protocols).|