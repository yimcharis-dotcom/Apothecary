```
module.exports = async (params) => {
    const { app } = params;
    
    // 1. Get the file you are currently editing (the draft)
    const activeFile = app.workspace.getActiveFile();
    if (!activeFile) {
        new Notice("❌ No active file open.");
        return;
    }

    // 2. CONFIGURATION: Set your exact templates folder name here
    const templateFolder = "__Templates"; 
    
    // 3. Define the target path (Same filename, but in the template folder)
    const targetPath = `${templateFolder}/${activeFile.name}`;

    // 4. Read the content of your current draft
    const content = await app.vault.read(activeFile);
    
    // 5. Check if the template file already exists
    const targetFile = app.vault.getAbstractFileByPath(targetPath);

    if (targetFile) {
        // Option A: It exists - Update it
        await app.vault.modify(targetFile, content);
        new Notice(`✅ Updated existing template: ${activeFile.name}`);
    } else {
        // Option B: It doesn't exist - Create it
        await app.vault.create(targetPath, content);
        new Notice(`🆕 Created new template: ${activeFile.name}`);
    }
}


```