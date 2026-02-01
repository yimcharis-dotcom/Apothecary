module.exports = async (params) => {
    const { app } = params;
    const fs = require('fs');

    // 1. Get the current active document
    const activeFile = app.workspace.getActiveFile();
    if (!activeFile) {
        new Notice("❌ No active file open.");
        return;
    }

    // 2. Determine filenames
    // e.g., "Hub.ps1.md" -> scriptName: "Hub.ps1", type: "powershell"
    const fileName = activeFile.name;
    const scriptName = fileName.replace(".md", "");
    
    // 3. Define the destinations
    const hubPath = `C:/Users/YC/AI_hub/${scriptName}`;
    const runningFolder = "C:/Vault/Apothecary/00_System/000_Scripts - running/0001_AI_HubWatch scripts - running";
    const runningPath = `${runningFolder}/!${scriptName}`;

    try {
        // 4. Read the note content
        const noteContent = await app.vault.read(activeFile);

        // 5. EXTRACT THE SCRIPT PORTION
        // It looks for everything between ```powershell and ```
        const codeBlockRegex = /```(?:powershell|javascript|js)?\n([\s\S]*?)```/;
        const match = noteContent.match(codeBlockRegex);

        if (!match || !match[1]) {
            new Notice("❌ No code block found in this note!");
            return;
        }

        const pureCode = match[1].trim();

        // 6. DEPLOY TO AI_HUB (The Working Version)
        fs.writeFileSync(hubPath, pureCode);

        // 7. DEPLOY TO RUNNING (The Production Version with !)
        if (!fs.existsSync(runningFolder)) fs.mkdirSync(runningFolder, { recursive: true });
        fs.writeFileSync(runningPath, pureCode);

        new Notice(`🚀 Extracted & Deployed ${scriptName}`);

    } catch (e) {
        console.error(e);
        new Notice(`❌ Deployment Error: ${e.message}`);
    }
}
