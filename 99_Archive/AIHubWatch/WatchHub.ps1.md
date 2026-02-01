# WatchHub.ps1
# Automatically monitors directories for new AI tools and creates junctions in the AI Hub.
# Now with Layer 3 "Signature Discovery" and specific AppData support.

$HubDir = "C:\Users\YC\AI_hub"
$WatchConfigs = @(
     # Layer 1: Configuration & Settings
     @{ Path = "C:\Users\YC"; Suffix = "User_Dot"; Filter = "." },
     @{ Path = "C:\Users\YC\AppData\Roaming"; Suffix = "AppData_Roaming"; Filter = "" },
     @{ Path = "C:\Users\YC\AppData\Local"; Suffix = "AppData_Local"; Filter = "" },
     @{ Path = "C:\"; Suffix = "Root_Dot"; Filter = "." },
    
     # Layer 2: Custom Installations & Projects
     @{ Path = "C:\Program Files"; Suffix = "System_ProgramFiles"; Filter = "" },
     @{ Path = "C:\Program Files (x86)"; Suffix = "System_ProgramFiles_x86"; Filter = "" },
     @{ Path = "C:\Users\YC\GitHubRepo"; Suffix = "Projects_GitHubRepo"; Filter = "" },
     @{ Path = "C:\Users\YC\MCPs"; Suffix = "Projects_User_Root"; Filter = "" },

     # Layer 3: No-Choice Installation "Hidden" Paths
     @{ Path = "C:\Users\YC\AppData\Local\Programs"; Suffix = "System_AppDataLocal"; Filter = "" }
)

# AI Keywords for name matching
$AIKeywords = @("ai", "claude", "gpt", "llama", "ollama", "zed", "cursor", "gemini", "cline", "roo", "trae", "openhands", "grok", "qwen", "aider", "openai", "anthropic", "perplexity", "anythingllm", "kombai", "factory", "azad", "kiro", "kode", "pochi", "pi", "deepseek", "mistral", "vllm", "mcp")

# Binary Signatures for Layer 3 discovery
$BinarySignatures = @("claude.exe", "cursor.exe", "zed.exe", "ollama.exe", "perplexity.exe", "windsurf.exe", "antigravity.exe", "anythingllm.exe")

# Rule Signatures for AI Codebases
$RuleSignatures = @(".cursorrules", ".windsurfrules", "mcp.json", "modelfile", "requirements.ai.txt")

function New-HubJunction {
     param($SourcePath, $Suffix)
    
     $Leaf = Split-Path $SourcePath -Leaf
    
     # Check if AI related by Name
     $IsAI = $false
     if ($Leaf.StartsWith(".")) { $IsAI = $true }
     foreach ($kw in $AIKeywords) {
          if ($Leaf -like "*$kw*") { $IsAI = $true; break }
     }
    
     # Content-based/Signature Discovery (Deep Search if Name doesn't match)
     if (-not $IsAI) {
          # Check for executable binaries
          foreach ($bin in $BinarySignatures) {
               if (Test-Path (Join-Path $SourcePath $bin)) { $IsAI = $true; break }
               # Also check subfolders (shallow) if it's a Program installation
               if (Test-Path (Join-Path $SourcePath "bin\$bin")) { $IsAI = $true; break }
               if (Test-Path (Join-Path $SourcePath "app\$bin")) { $IsAI = $true; break }
          }
     }

     if (-not $IsAI) {
          # Check for rule files
          foreach ($sig in $RuleSignatures) {
               if (Test-Path (Join-Path $SourcePath $sig)) { $IsAI = $true; break }
          }
     }

     if (-not $IsAI) { return }

     # Clean name for the link
     $CleanName = $Leaf
     if ($CleanName.StartsWith(".")) { $CleanName = $CleanName.Substring(1) }
    
     # Sanitize name for junction (remove spaces, special chars)
     $CleanName = $CleanName -replace '[^a-zA-Z0-9]', ''
     # Capitalize first letter
     if ($CleanName.Length -gt 0) {
          $CleanName = $CleanName.Substring(0, 1).ToUpper() + $CleanName.Substring(1)
     }
     else {
          return # Skip if name is empty after sanitization
     }
    
     $TargetName = "${CleanName}_${Suffix}"
     $TargetPath = Join-Path $HubDir $TargetName
    
     if (-not (Test-Path $TargetPath)) {
          Write-Host "[$(Get-Date -Format 'HH:mm:ss')] New tool! Linking: $SourcePath -> $TargetPath"
          # Using cmd for robust junction creation
          cmd /c mklink /J "`"$TargetPath`"" "`"$SourcePath`""
     }
}

Write-Host "AI Hub Watcher (v2.1) started."
Write-Host "Monitoring Layers 1, 2, & 3 for AI tool patterns..."

# Watch Loop
while ($true) {
     foreach ($cfg in $WatchConfigs) {
          if (Test-Path $cfg.Path) {
               Get-ChildItem -Path $cfg.Path -Directory -ErrorAction SilentlyContinue | ForEach-Object {
                    New-HubJunction -SourcePath $_.FullName -Suffix $cfg.Suffix
               }
          }
     }
     Start-Sleep -Seconds 30
}
