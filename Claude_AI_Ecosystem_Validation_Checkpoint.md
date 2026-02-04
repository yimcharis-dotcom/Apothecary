---
words:
  2026-01-31: 663
---
# AI Ecosystem Data Validation - Checkpoint

**Last Updated:** 2026-01-29
**Status:** In Progress - Provider & Product validation complete

---

## Progress Summary

### ✅ Completed

1. **Provider Column Validation**
   - Identified 35 providers (reduced from initial count)
   - Found issues: "Grok IDE" doesn't exist (should be under xAI)
   - Confirmed: Kimi and DeepSeek use Google OAuth, not "None"

2. **Product/Plan Column Validation**
   - Validated all 62 original product entries
   - Applied 13 deletions (non-existent products, custom MCPs)
   - Applied 3 corrections (Windsurf IDE, auth fields)
   - **New count: 49 products**

### 📝 Changes Applied to Master_List.md

**Deletions (13 rows):**
- .ai-agents / Multi-AI Launcher
- AITK / AI Toolkit
- Perplexity MCP
- Grok IDE (Config)
- Grok MCP
- Gemini IDE
- Qwen IDE
- Obsidian AI / Plugin Ecosystem
- Obsidian MCP
- Perplexity MCP Bridge
- OP.GG MCP
- Docs MCP
- Monica (Free)

**Corrections:**
- "Codeium IDE" → "Windsurf IDE"
- Kimi auth: "None" → "Google OAuth"
- DeepSeek auth: "None" → "Google OAuth"

**Notes Added:**
- OpenMCP Config: Configured but not actively used
- Vault Bridge MCP: User's custom creation
- LocalDocs RAG: User's custom creation
- Apothecary Vault: User's custom creation

---

## Next Steps

### 🔄 Resume Point: Capability Column Validation

**Remaining columns to validate:**
1. **Capability** - Validate category names (IDE Integration, Web Chat, CLI, SDK, etc.)
2. **Surface** - Check URLs, paths, app names
3. **Connected To** - Verify integration references
4. **Presence** - Confirm Local/Web/Hybrid classifications
5. **Auth** - Already partially validated, may need spot checks
6. **Status** - Verify active/inactive status (only 1 inactive currently: LiteLLM)

### Validation Approach (Established Pattern)

1. Extract all unique values from the column
2. Check for inconsistencies, typos, duplicates
3. Use web search for questionable entries
4. User provides corrections where needed
5. Apply changes to Master_List.md
6. Move to next column

---

## Key Insights from Validation

1. **Custom vs Provider Products**
   - MCP bridges (Vault Bridge, Perplexity Bridge, OP.GG) are user creations, not provider products
   - Should be treated differently in final dataset

2. **Non-Existent Products**
   - Several "IDE" products don't exist (Grok IDE, Gemini IDE, Qwen IDE)
   - Only actual IDEs: Cursor, VS Code, Windsurf, Zed, Antigravity

3. **Authentication Patterns**
   - Many free chatbots use Google OAuth (Kimi, DeepSeek)
   - Local tools use "Local" or "None"
   - Paid services use OAuth or API Keys

4. **Duplicate Naming**
   - Some products appear multiple times with different surfaces (Claude Code x3)
   - This is intentional - same product, different access methods
   - Will need unique IDs: provider-product-surface pattern

---

## Files Modified

- ✅ `C:\Vault\Apothecary\Claude_AI_Ecosystem_Master_List.md` - 13 deletions, 3 corrections applied
- ✅ `C:\Users\YC\.claude\plans\purrfect-imagining-tome.md` - Original plan file
- ✅ `C:\Vault\Apothecary\Claude_AI_Ecosystem_Validation_Checkpoint.md` - This checkpoint

---

## Schema Design Status

**Current Plan (from purrfect-imagining-tome.md):**
- Extract to JSON with human-readable IDs (slugs)
- Include full verification data (health checks, status)
- Create separate files: providers.json, services.json, connections.json, verification.json

**Still TODO:**
- Finalize schema after all column validation complete
- Extract data to structured JSON
- Build connection graph from Connection Map section
- Add verification data from Discovery_Audit.md

---

## Statistics

| Metric | Before | After |
|--------|--------|-------|
| Total Rows | 62 | 49 |
| Providers | ~35 (needs recount) | TBD |
| Columns Validated | 0 | 2/8 |
| Deletions Applied | 0 | 13 |
| Corrections Applied | 0 | 3 |
| Completion | 0% | 25% |

---

## Resume Command

When ready to continue, use:
```
/resume
```

Claude will pick up at: **Capability Column Validation**

---

## Notes for Future Sessions

- Validation is thorough but time-consuming (intentional - accuracy over speed)
- User corrections are ground truth, web search is backup
- Custom creations (MCPs, LocalDocs, Vault Bridge) are part of ecosystem but flagged as user-made
- Approach is working well for this dataset size (~50 products)
