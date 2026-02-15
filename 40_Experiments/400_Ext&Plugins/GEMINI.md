# Tutorial: Building a Gemini CLI Extension (OpenRouter)

## Objective
The goal of this project is to teach the user how to build, configure, and deploy a custom extension for the Gemini CLI. We are specifically building an **OpenRouter integration** to enable access to 300+ AI models directly from the terminal.

## Project Structure
- **Development/Working Folder**: `C:\Users\YC\Ext&Plugins\gemini-openrouter-custom`
  - *This is where we write code and test the extension.*
- **Workbench & Reference**: `C:\Vault\Apothecary\40_Experiments\400_Ext&Plugins`
  - *This is where we keep documentation, research, and final versions of the experiment.*

---

## Step-by-Step Roadmap

### Phase 1: Scaffolding
- [ ] Create project directories.
- [ ] Initialize `package.json` with ESM support.
- [ ] Create `gemini-extension.json` (The manifest file that tells the CLI what this extension does).

### Phase 2: Core Logic
- [ ] Implement `src/index.js`.
- [ ] Create a command handler for `openrouter <prompt>`.
- [ ] Add argument parsing (for model selection).
- [ ] Implement secure API key loading from `.gemini/.env`.

### Phase 3: Integration
- [ ] Install dependencies (`yargs`).
- [ ] Link the extension to the Gemini CLI.
- [ ] Verify functionality with a test query.
---

## Key Concepts to Learn
1. **Gemini Extension Hooks**: Understanding how the CLI discovers and executes custom code.
2. **ES Modules in Node.js**: Using modern `import/export` syntax for extension development.
3. **Environment Management**: Handling secrets securely within the Gemini ecosystem.
4. **API Integration**: Talking to external LLM providers (OpenRouter) using `fetch`.
