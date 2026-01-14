
```shell

# 1. Define the content of your Modelfile (The content is excellent!)
$ModelfileContent = @"
FROM llama3.2:8b
SYSTEM You are a local LLM running entirely offline via Ollama on the user's laptop. You have no internet access, cannot browse websites, and no knowledge beyond your training data. If unsure about current events, facts, or commands, say "I don't know" or ask for clarification. Never invent information, plugin names, commands, URLs, packages, or installation steps. Be helpful and objective for Obsidian PKM (Personal Knowledge Management) tasks like summarizing notes, brainstorming, rewriting, maintaining and organizing the vault. Do not flatter, be neutral.
PARAMETER temperature 0.3
PARAMETER num_ctx 4096
"@

# 2. Output the content to a file named 'Modelfile' in a dedicated folder
# NOTE: Replace the path with the *actual* folder you created
$OutputPath = "C:\Users\YC\OneDrive\Desktop\AI hub\ollama modlife\Modelfile"

$ModelfileContent | Out-File -Encoding utf8 $OutputPath
```

``` shell
# =================================================================
# STEP 1: DEFINE VARIABLES & OUTPUT LOCATION
# =================================================================

# 1a. Define the name for your custom model
$NewModelName = "pkm-helper" 

# 1b. Define the path where the Modelfile will be created
# NOTE: Using a simple path for easier access. The file will be named 'Modelfile'.
$ScriptFolder = "C:\Users\YC\OneDrive\Desktop\AI hub\ollama_modelfiles"
$ModelfilePath = Join-Path $ScriptFolder "Modelfile"

# 1c. Ensure the project folder exists
if (-not (Test-Path $ScriptFolder)) {
    Write-Host "Creating folder: $ScriptFolder"
    New-Item -Path $ScriptFolder -ItemType Directory | Out-Null
}


# =================================================================
# STEP 2: DEFINE THE MODELFILE CONTENT
# =================================================================

# Using the improved Llama 3.2 8B tag and your custom instructions.
$ModelfileContent = @"
FROM llama3.2:8b
SYSTEM You are a local LLM running entirely offline via Ollama on the user's laptop. You have no internet access, cannot browse websites, and no knowledge beyond your training data. If unsure about current events, facts, or commands, say "I don't know" or ask for clarification. Never invent information, plugin names, commands, URLs, packages, or installation steps. Be helpful and objective for Obsidian PKM (Personal Knowledge Management) tasks like summarizing notes, brainstorming, rewriting, maintaining and organizing the vault. Do not flatter, be neutral.
PARAMETER temperature 0.3
PARAMETER num_ctx 4096
"@


# =================================================================
# STEP 3: WRITE THE FILE AND CREATE THE MODEL
# =================================================================

Write-Host "Writing Modelfile to $ModelfilePath"
# Write the content to the file. -Force overwrites if it already exists.
$ModelfileContent | Out-File -Encoding utf8 $ModelfilePath -Force

# Change the current directory to where the Modelfile is saved
Set-Location $ScriptFolder

Write-Host "Building custom model '$NewModelName' from Modelfile..."
# This is the core Ollama command to build and save the model internally
ollama create $NewModelName -f $ModelfilePath

Write-Host "Creation complete. You can now run your model:"
Write-Host "ollama run $NewModelName"
```

> [!failure]- Failure 
>   AbortError: signal is aborted without reason
>   
>   - plugin:obsidian-textgenerator-plugin:2070 I7.endLoading
>     plugin:obsidian-textgenerator-plugin:2070:360
>   
>   - plugin:obsidian-textgenerator-plugin:2145 t.callback
>     plugin:obsidian-textgenerator-plugin:2145:13800
>   
>   - app.js:1 K0
>     app://obsidian.md/app.js:1:2651891
>   
>   - app.js:1 t.onChooseItem
>     app://obsidian.md/app.js:1:3012125
>   
>   - app.js:1 t.onChooseSuggestion
>     app://obsidian.md/app.js:1:2202902
>   
>   - app.js:1 t.selectSuggestion
>     app://obsidian.md/app.js:1:2202307
>   
>   - app.js:1 e.useSelectedItem
>     app://obsidian.md/app.js:1:1262715
>   
>   - app.js:1 e.onSuggestionClick
>     app://obsidian.md/app.js:1:1262450
>   
>   - enhance.js:1 HTMLDivElement.s
>     app://obsidian.md/enhance.js:1:10558
>   
>  
