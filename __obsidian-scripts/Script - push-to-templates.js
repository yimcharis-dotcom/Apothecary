module.exports = async (params) => {
    const { app } = params;
    
    // 1. Get the current active file
    const activeFile = app.workspace.getActiveFile();
    if (!activeFile) {
        new Notice("❌ No active file open.");
        return;
    }

    // 2. CONFIGURATION
    const templateFolder = "__Templates"; 
    const prefix = "!tp - "; // The prefix you want to add

    // 3. Construct the target name: "!tp - filename.md"
    const targetName = `${prefix}${activeFile.name}`;
    const targetPath = `${templateFolder}/${targetName}`;

    // 4. Read content from the draft
    const content = await app.vault.read(activeFile);
    
    // 5. Check if it exists and update/create
    const targetFile = app.vault.getAbstractFileByPath(targetPath);

    if (targetFile) {
        await app.vault.modify(targetFile, content);
        new Notice(`✅ Updated: ${targetName}`);
    } else {
        await app.vault.create(targetPath, content);
        new Notice(`🆕 Created: ${targetName}`);
    }
}
