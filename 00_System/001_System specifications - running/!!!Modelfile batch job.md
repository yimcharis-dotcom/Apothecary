### PowerShell Script (Copy-Paste & Run)

```powershell
# === CONFIGURATION - Change these if you want ===
$ModelBase = "llama3.2:3b"                  # The base model (change to :1b if you prefer ultra-speed)
$CustomName = "llama32-safe"                # Name of your new custom model
$DumpFolder = "C:\Users\YC\Obsidian\AI-Modelfiles"  # Folder where the Modelfile will be saved

# Create the dump folder if it doesn't exist
if (!(Test-Path $DumpFolder)) {
    New-Item -ItemType Directory -Path $DumpFolder | Out-Null
    Write-Host "Created folder: $DumpFolder"
}

# === The strict system prompt (your bulletproof constraints) ===
$ModelfileContent = @"
FROM $ModelBase

SYSTEM You are a fast, factual local LLM for Obsidian PKM.
- Never invent plugins, paths, commands, URLs, or vault details.
- Only use facts the user explicitly provides.
- If unsure or missing info, say "Unknown" and ask ONE clarification question.
- Be concise. Focus on summarizing notes, templates, tagging, checklists.
- No assumptions about my setup.

PARAMETER temperature 0.4
PARAMETER num_ctx 128000
PARAMETER repeat_penalty 1.2
"@

# Save Modelfile to disk
$ModelfilePath = Join-Path $DumpFolder "Modelfile-$CustomName"
$ModelfileContent | Out-File -FilePath $ModelfilePath -Encoding UTF8
Write-Host "Modelfile saved to: $ModelfilePath"

# === Create the custom model in Ollama ===
Write-Host "Creating Ollama model '$CustomName' from base '$ModelBase'..."
ollama create $CustomName -f $ModelfilePath

Write-Host "`nDone! Your new bulletproof model '$CustomName' is ready."
Write-Host "Run it with: ollama run $CustomName"
Write-Host "All files backed up in: $DumpFolder"
```

### How to Use It
1. Open **PowerShell** (no need for admin).
2. Paste the entire script.
3. Press Enter — it will:
   - Create the folder (if needed)
   - Write the Modelfile there
   - Build `llama32-safe` in Ollama

### Result
- You get a **super-fast + strictly honest** Llama 3.2 3B model.
- The Modelfile is safely backed up so you can recreate it anytime (or tweak it later).

Now hook `llama32-safe` to your favorite plugin (Text Generator, Copilot, Perplexed) — you’ll have lightning speed **and** no more dumper behavior.

Run the script and let me know how fast it feels! 😄