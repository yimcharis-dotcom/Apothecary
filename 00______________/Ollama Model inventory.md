---
alias: [AI Tools Link Manager, Ollama GPT 4 All Symlink Guide]
tags:
  - ai/models
  - ai/local-ai
  - system/automation
  - how-to
  - #
created: 2026-01-05
---
updated: `=dateformat(date(today), "yyyy-MM-dd")`

Base Url: http://localhost:11434
URL: http://127.0.0.1:11434

``` css 
NAME                          ID              SIZE      MODIFIED
phi4-mini:latest              587b3b536409    3.2 GB    About an hour ago
phi4-mini-reasoning:latest    3ca8c2865ce9    3.2 GB    About an hour ago
phi3-mini:latest              2fa0f718cffe    2.2 GB    2 hours ago
bge-m3:latest                 790764642607    1.2 GB    4 days ago
gemma2:9b                     ff02c3702f32    5.4 GB    7 days ago
qwen2.5:3b                    357c53fb659c    1.9 GB    7 days ago
gemma2:2b                     8ccf136fdd52    1.6 GB    7 days ago
llama3.2:latest               a80c4f17acd5    2.0 GB    7 days ago
llama3_1:latest               6ccd81b5413c    5.7 GB    8 days ago
qwen2.5:7b-instruct           845dbda0ea48    4.7 GB    8 days ago
mistral-4k:latest             f14a5be852dd    4.4 GB    9 days ago
```


# 🔗 Ollama ↔ GPT4All Symbolic Link Manager

This note documents the setup for using Ollama-downloaded language models directly within the GPT4All desktop application via **Windows Symbolic Links (symlinks)**. This saves significant disk space by avoiding duplicate model downloads.

> **Core Concept**: A symlink is a special file that acts as a pointer to another file or folder located elsewhere on your system.

## 📁 Current Symlink Status

Run the command below to see all symlinks in your GPT4All directory and their status. This is your primary diagnostic tool.

```powershell
Get-ChildItem "C:\Users\YC\AppData\Local\nomic.ai\GPT4All" | Format-Table Mode, LastWriteTime, Length, Name, Target -AutoSize
```

### 🔍 How to Interpret the Output
The **`Mode`** column is key. Look for the letter `L`:

| Mode Attribute | What It Means | Status |
| :--- | :--- | :--- |
| **`La---`** | `L` = **Reparse Point (Symlink)**, `a` = Archive. The link is **valid and active**. | ✅ **Working** |
| **`-a---`** | **No `L`**. This is a regular file, **not a symlink**. Often means the symlink creation failed or the target is missing. | ❌ **Broken / Not a Link** |
| **`da----`** | `d` = Directory. Not applicable for model files. | ➖ |

## 🛠 Corrected Symlink Commands

Below are the corrected `New-Item` commands for each model, using valid Windows filenames (colons `:` replaced with hyphens `-`) and the verified target paths from your inventory.

### 1. Phi 4 - mini-latest #
**Command to Create Link:** #snipetts
```powershell
New-Item -ItemType SymbolicLink -Path "C:\Users\YC\AppData\Local\nomic.ai\GPT4All\phi4mini-.gguf" -Target "sha256-f4dd2368e6c32725dc1c5c5548ae9ee2724d6a79052952eb50b65e26288022c4" -Force
```
**Status:** ✅ **CONFIRMED WORKING** (Shows `La---` in directory listing).
--- phi4-mini-reasoning:latest ---

FROM C:\Users\YC\.ollama\models\blobs\sha256-f4dd2368e6c32725dc1c5c5548ae9ee2724d6a79052952eb50b65e26288022c4
### 2. Llama 3.2-latest
**Command to Create/Repair Link:**
> **Issue Identified**: The previous command had typos in the target path (`node1a` instead of `models`, user `VC` instead of `YC`).
```powershell
# First, remove any broken file/symlink
Remove-Item "C:\Users\YC\AppData\Local\nomic.ai\GPT4All\llama3.2-latest.gguf" -ErrorAction SilentlyContinue

# Create the correct symlink
New-Item -ItemType SymbolicLink -Path "C:\Users\YC\AppData\Local\nomic.ai\GPT4All\llama3.2-latest.gguf" -Target "C:\Users\YC\.ollama\models\blobs\sha256-dde5aa3fc5ffc17176b5e8bdc82f587b24b2678c6c66101bf7da77af9f7ccdff" -Force
```

### 3. Phi 3-mini #
**Command to Create Link:** #snipetts
```powershell
New-Item -ItemType SymbolicLink -Path "C:\Users\YC\AppData\Local\nomic.ai\GPT4All\phi3-mini-latest-.gguf" -Target "C:\Users\YC\.ollama\models\blobs\sha256-633fc5be925f9a484b61d6f9b9a78021eeb462100bd557309f01ba84cac26adf" -Force
```
**Status:** ✅ **CONFIRMED WORKING** (Shows `La---` in directory listing).

### 4. Other Models (qwen 2.5:3b,  latest, etc.)
For all other models, the **recommended approach is to use the automated script below**, which handles naming and path corrections in bulk.

## 🤖 Complete Automated Synchronization Script

This PowerShell script creates symlinks for **all models listed in your inventory** at once. It fixes filenames and provides feedback.

**Instructions:** Copy the entire script below, paste it into a PowerShell window, and run it **as Administrator**.
#scripts #snipetts #ai/automation 
```powershell
# === Ollama to GPT4All Bulk Symlink Creator ===
# Run this script in PowerShell AS ADMINISTRATOR.

# 1. Define your base paths (VERIFY THESE)
$ollamaBlobPath = "C:\Users\YC\.ollama\models\blobs"
$gpt4allModelPath = "C:\Users\YC\AppData\Local\nomic.ai\GPT4All"

# 2. Model Map: Ollama Model Name -> SHA256 Hash (UPDATED)
$modelMap = @{
    "bge-m3:latest" = "daec91ffb5dd0c27411bd71f29932917c49cf529a641d0168496c3a501e3062c"
    "gemma2:9b" = "ff1d1fc78170d787ee1201778e2dd65ea211654ca5fb7d69b5a2e7b123a50373"
    "qwen2.5:3b" = "5ee4f07cdb9beadbbb293e85803c569b01bd37ed059d2715faa7bb405f31caa6"
    "gemma2:2b" = "7462734796d67c40ecec2ca98eddf970e171dbb6b370e43fd633ee75b69abe1b"
    "nomic-embed-text:latest" = "970aa74c0a90ef7482477cf803618e776e173c007bf957f635f1015bfcfef0e6"
    "llama3.2:latest" = "dde5aa3fc5ffc17176b5e8bdc82f587b24b2678c6c66101bf7da77af9f7ccdff"
    "llama3_1:latest" = "1ae48274baafb576c66af17eca484ba3d44759316a0e9cbef252b6235af9ceef"
    "qwen2.5:7b-instruct" = "2bada8a7450677000f678be90653b85d364de7db25eb5ea54136ada5f3933730"
    "mistral-4k:latest" = "f5074b1221da0f5a2910d33b642efa5b9eb58cfdddca1c79e16d7ad28aa2b31f"
    # ===== UPDATED ENTRIES =====
    "phi3-mini:latest" = "633fc5be925f9a484b61d6f9b9a78021eeb462100bd557309f01ba84cac26adf"
    "phi4-mini:latest" = "f4dd2368e6c32725dc1c5c5548ae9ee2724d6a79052952eb50b65e26288022c4"
}
}

Write-Host "Starting bulk symlink creation..." -ForegroundColor Cyan
Write-Host "GPT4All Path: $gpt4allModelPath" -ForegroundColor Gray
Write-Host "Ollama Blobs: $ollamaBlobPath`n" -ForegroundColor Gray

# 3. Create a symlink for each model
foreach ($model in $modelMap.GetEnumerator()) {
    $safeModelName = $model.Name -replace "[:]", "-"  # Fix: Replace colon with hyphen
    $targetFile = "sha256-$($model.Value)"
    $symlinkPath = Join-Path $gpt4allModelPath "$safeModelName.gguf"
    $targetPath = Join-Path $ollamaBlobPath $targetFile

    Write-Host "Processing: $($model.Name) -> $safeModelName.gguf" -ForegroundColor Cyan

    # Remove existing broken symlink/file if it exists
    if (Test-Path $symlinkPath) {
        Remove-Item $symlinkPath -Force -ErrorAction SilentlyContinue
        Write-Host "  Cleared previous file/link." -ForegroundColor DarkYellow
    }

    # Create the new symbolic link
    New-Item -ItemType SymbolicLink -Path $symlinkPath -Target $targetPath -Force -ErrorAction SilentlyContinue

    # Verify
    if (Test-Path $symlinkPath -PathType Leaf) {
        $item = Get-Item $symlinkPath
        if ($item.LinkType -eq "SymbolicLink") {
            Write-Host "  SUCCESS: Symlink created." -ForegroundColor Green
        } else {
            Write-Host "  WARNING: File created, but is NOT a symlink." -ForegroundColor Yellow
        }
    } else {
        Write-Host "  FAILED: Could not create. Check target path: $targetPath" -ForegroundColor Red
    }
}

Write-Host "`nBulk creation process finished." -ForegroundColor Yellow
Write-Host "-> Please RESTART GPT4All and check the 'Local Models' tab." -ForegroundColor Yellow
```

## 📚 Integration with Your PKM Workflow

1.  **Link to Your Model Inventory**: Connect this note to your main `Ollama Model Inventory.md` using `[[Ollama Model Inventory]]`.
2.  **Usage Log**: Consider creating a `Model Performance Log.md` note to record which model works best for tasks like coding, writing, or analysis.
3.  **Automation**: Place this note in a folder like `_Templates` or `Systems` for easy access.

## ⚠️ Notes & Limitations

- **GPT 4 All Compatibility**: Not all Ollama models are in the `.gguf` format GPT 4 All expects. Embedding models (e.g., `bge-m3`, `nomic-embed-text`) will likely **not** appear or work in GPT 4 All's chat interface.
- **Administrator Privileges**: Creating symlinks in Windows **always requires** running PowerShell as Administrator.
- **Model Updates**: If you update/pull a model in Ollama, it may generate a new blob file with a different SHA 256 hash, breaking the symlink. Re-run the bulk script to fix it.

---
*This note was generated and last revised on `=dateformat(date(today), "yyyy-MM-dd")` to consolidate working commands and diagnostics.*
```

You can save this directly as a new note in your Obsidian vault (e.g., `Ollama GPT4All Symlink Manager.md`). This note provides you with a complete, actionable guide, from understanding the diagnostic output to running the corrected bulk operations.