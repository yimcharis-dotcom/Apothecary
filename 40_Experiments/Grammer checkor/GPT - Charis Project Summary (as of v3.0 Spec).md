


### **Charis Project Summary (as of v3.0 Spec)**

- **Goal:** A grammar and naturalness checker for **C1-level Cantonese L1 users**, usable across GPT and Claude for consistent evaluation.
    
- **System:**
    
    - **Tier 1:** Universal, mechanical grammar (no L1 influence).
        
    - **Tier 2:** Context-dependent grammar + naturalness; two tracks —  
        **T2-G** (articles, prepositions, tense, etc.) and **T2-N** (collocation, word order, register, cohesion, idiomaticity).
        
- **Output:** Four sections — Annotated Text, Explanations, Native-Speaker Alternatives, Corrected Version.
    
    - Tier-2 explanations use:
        
        `[Prescriptive|Descriptive|Naturalness] Tag → Explanation → Rule → Impact → Alternatives`
        
- **Testing:** `[TEST]` footer adds tag and type counts for cross-model evaluation.
    
- **Naturalness:** Every sentence scanned for native-like rhythm and phrasing.
    
- **Span Markup:** Pending final decision; temporary start–end marking works.
    
- **Cantonese L1:** Influence explicitly built into Tier 2; Tier 1 remains universal.
    
- **Next minor update (v3.1):** add one clarifying line in the Purpose section about Cantonese L1 transfer.
    

---

You’re fully caught up.  
When you’re back, start from **“Add Cantonese L1 clarification → finalize span markup.”**