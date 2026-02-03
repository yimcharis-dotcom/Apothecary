# AIToolsConfig.ps1
# Single source of truth for AI tool detection
# Used by: WatchHub_Realtime.ps1, TrackInstallation.ps1, SyncSkills.ps1

# ============================================================================
# Configuration
# ============================================================================

$script:HubDir = if ($env:AI_HUB_PATH) { $env:AI_HUB_PATH } else { "$env:USERPROFILE\AI_hub" }
$script:TaskName = "AI_HubWatch_AutoMonitor"

# ============================================================================
# AI Tool Definitions
# Each tool has:
#   - Names: Exact folder names to match (case-insensitive)
#   - ConfigFiles: Files that MUST exist to validate it's a real AI tool
#   - Category: For organizing in the hub
# ============================================================================

$script:AIToolDefinitions = @{
    # CLI/Agent Config Folders (dotfiles in user home)
    "claude" = @{
        Names = @(".claude", "claude")
        ConfigFiles = @("settings.json", "claude_desktop_config.json", "projects.json")
        Category = "CLI_Agent"
    }
    "cursor" = @{
        Names = @(".cursor", "cursor", "Cursor")
        ConfigFiles = @("settings.json", "extensions.json", "state.vscdb")
        Category = "IDE"
    }
    "ollama" = @{
        Names = @(".ollama", "ollama", "Ollama")
        ConfigFiles = @("models", "id_ed25519", "id_ed25519.pub")
        Category = "LLM_Runtime"
    }
    "zed" = @{
        Names = @("zed", "Zed", ".zed")
        ConfigFiles = @("settings.json", "keymap.json", "themes")
        Category = "IDE"
    }
    "windsurf" = @{
        Names = @("windsurf", "Windsurf", ".windsurf")
        ConfigFiles = @("settings.json", "extensions")
        Category = "IDE"
    }
    "codeium" = @{
        Names = @(".codeium", "codeium", "Codeium")
        ConfigFiles = @("config.json", "manager_dir")
        Category = "Extension"
    }
    "continue" = @{
        Names = @(".continue", "continue")
        ConfigFiles = @("config.json", "config.ts")
        Category = "Extension"
    }
    "copilot" = @{
        Names = @("github-copilot", "copilot", ".copilot")
        ConfigFiles = @("hosts.json", "versions.json")
        Category = "Extension"
    }
    "aider" = @{
        Names = @(".aider", "aider")
        ConfigFiles = @(".aider.conf.yml", "aider.conf.yml", ".aider.model.settings.yml")
        Category = "CLI_Agent"
    }
    "cody" = @{
        Names = @(".cody", "cody", "sourcegraph-cody")
        ConfigFiles = @("config.json", "cody.json")
        Category = "Extension"
    }
    "tabnine" = @{
        Names = @(".tabnine", "tabnine", "TabNine")
        ConfigFiles = @("config.json", "tabnine_config.json")
        Category = "Extension"
    }
    "supermaven" = @{
        Names = @(".supermaven", "supermaven")
        ConfigFiles = @("config.json", "settings.json")
        Category = "Extension"
    }
    # GUI Applications (AppData locations)
    "anthropic" = @{
        Names = @("Anthropic", "anthropic", "Claude")
        ConfigFiles = @("config.json", "claude_desktop_config.json", "Local State")
        Category = "Desktop_App"
    }
    "vscode" = @{
        Names = @("Code", "code", "VSCode")
        ConfigFiles = @("settings.json", "extensions.json", "User")
        Category = "IDE"
    }
    "openai" = @{
        Names = @("openai", "OpenAI", "ChatGPT")
        ConfigFiles = @("config.json", "auth.json")
        Category = "Desktop_App"
    }
    # MCP Related
    "mcp" = @{
        Names = @(".mcp", "mcp", "mcp-servers")
        ConfigFiles = @("config.json", "servers.json", "mcp.json")
        Category = "MCP"
    }
}

# ============================================================================
# Strict Keywords - Only these trigger detection
# Avoids false positives from generic words like 'ai', 'agent'
# ============================================================================

$script:StrictKeywords = @(
    'claude', 'cursor', 'zed', 'ollama', 'gemini', 'windsurf',
    'mcp', 'anthropic', 'openai', 'copilot', 'codeium',
    'tabnine', 'cody', 'aider', 'continue', 'supermaven',
    'chatgpt', 'codegpt'
)

# Generic keywords that need additional validation (folder must have config files)
$script:GenericKeywords = @(
    'llm', 'gpt'
)

# ============================================================================
# Detection Functions
# ============================================================================

function Test-IsAIToolByName {
    <#
    .SYNOPSIS
        Quick check if folder name matches known AI tool
    .RETURNS
        $true if name matches strict keywords, $false otherwise
    #>
    param([string]$FolderName)

    $cleanName = $FolderName.ToLower() -replace '^\.', ''

    foreach ($keyword in $script:StrictKeywords) {
        if ($cleanName -eq $keyword -or $cleanName -like "*$keyword*") {
            return $true
        }
    }
    return $false
}

function Test-IsAIToolByConfig {
    <#
    .SYNOPSIS
        Validate folder contains expected AI tool config files
    .PARAMETER FolderPath
        Full path to the folder to validate
    .RETURNS
        Hashtable with IsValid, ToolName, and MatchedFiles
    #>
    param([string]$FolderPath)

    $folderName = Split-Path $FolderPath -Leaf
    $cleanName = $folderName.ToLower() -replace '^\.', ''

    $result = @{
        IsValid = $false
        ToolName = $null
        MatchedFiles = @()
        Category = "Unknown"
    }

    foreach ($tool in $script:AIToolDefinitions.Keys) {
        $def = $script:AIToolDefinitions[$tool]

        # Check if folder name matches any of the tool's known names
        $nameMatch = $def.Names | Where-Object {
            $cleanName -eq $_.ToLower() -or
            $cleanName -like "*$($_.ToLower())*"
        }

        if ($nameMatch) {
            # Check for config files
            $matchedFiles = @()
            foreach ($configFile in $def.ConfigFiles) {
                $configPath = Join-Path $FolderPath $configFile
                if (Test-Path $configPath) {
                    $matchedFiles += $configFile
                }
            }

            if ($matchedFiles.Count -gt 0) {
                $result.IsValid = $true
                $result.ToolName = $tool
                $result.MatchedFiles = $matchedFiles
                $result.Category = $def.Category
                return $result
            }
        }
    }

    return $result
}

function Get-AIToolInfo {
    <#
    .SYNOPSIS
        Get full info about an AI tool folder
    .PARAMETER FolderPath
        Full path to the folder
    .RETURNS
        Hashtable with detection results and recommendations
    #>
    param([string]$FolderPath)

    $folderName = Split-Path $FolderPath -Leaf

    $info = @{
        FolderName = $folderName
        FolderPath = $FolderPath
        NameMatch = Test-IsAIToolByName -FolderName $folderName
        ConfigValidation = Test-IsAIToolByConfig -FolderPath $FolderPath
        ShouldLink = $false
        Reason = ""
    }

    # Decision logic
    if ($info.ConfigValidation.IsValid) {
        $info.ShouldLink = $true
        $info.Reason = "Valid AI tool: $($info.ConfigValidation.ToolName) (found: $($info.ConfigValidation.MatchedFiles -join ', '))"
    }
    elseif ($info.NameMatch) {
        # Name matches but no config files - could be new/empty install
        # Check if folder is not empty
        $items = Get-ChildItem -Path $FolderPath -ErrorAction SilentlyContinue
        if ($items.Count -gt 0) {
            $info.ShouldLink = $true
            $info.Reason = "Name matches AI tool, folder has content (may be new install)"
        }
        else {
            $info.ShouldLink = $false
            $info.Reason = "Name matches but folder is empty - skipping"
        }
    }
    else {
        $info.ShouldLink = $false
        $info.Reason = "Not recognized as AI tool"
    }

    return $info
}

# ============================================================================
# Skill Validation
# ============================================================================

$script:SkillSignatureFiles = @(
    "skill.json",
    "package.json",
    "index.js",
    "index.ts",
    "main.py",
    "__init__.py",
    "skill.yaml",
    "skill.yml"
)

# ============================================================================
# Multi-Source Skill Locations
# Different AI tools store skills/extensions in different places
# ============================================================================

$script:SkillSources = @{
    "Claude" = @{
        AgentPattern = "Claude*"
        SkillsSubfolder = "skills"
        Format = "MCP"
    }
    "Cursor" = @{
        AgentPattern = "Cursor*", "cursor*"
        SkillsSubfolder = "extensions"
        Format = "VSCode"
    }
    "Continue" = @{
        AgentPattern = "Continue*", "continue*"
        SkillsSubfolder = "."  # Root level config.json contains skills
        Format = "Continue"
    }
    "VSCode" = @{
        AgentPattern = "Code*", "VSCode*"
        SkillsSubfolder = "extensions"
        Format = "VSCode"
    }
    "Zed" = @{
        AgentPattern = "Zed*", "zed*"
        SkillsSubfolder = "extensions"
        Format = "Zed"
    }
    "Cody" = @{
        AgentPattern = "Cody*", "cody*", "sourcegraph*"
        SkillsSubfolder = "."
        Format = "Cody"
    }
}

# Skill format signatures - how to identify skill type
$script:SkillFormats = @{
    "MCP" = @{
        Signatures = @("skill.json", "mcp.json")
        EntryPoints = @("index.js", "index.ts", "main.py")
        Description = "Model Context Protocol skill"
    }
    "VSCode" = @{
        Signatures = @("package.json", "extension.js")
        EntryPoints = @("extension.js", "out/extension.js")
        Description = "VSCode/Cursor extension"
    }
    "Continue" = @{
        Signatures = @("config.json", "config.ts")
        EntryPoints = @()
        Description = "Continue dev extension"
    }
    "Zed" = @{
        Signatures = @("extension.toml", "Cargo.toml")
        EntryPoints = @("src/lib.rs", "extension.wasm")
        Description = "Zed extension"
    }
    "Generic" = @{
        Signatures = @("package.json", "setup.py", "pyproject.toml")
        EntryPoints = @("index.js", "main.py", "__init__.py")
        Description = "Generic skill package"
    }
}

# ============================================================================
# Security Configuration
# ============================================================================

# Dangerous file extensions that should trigger warnings
$script:DangerousExtensions = @(
    ".exe", ".msi", ".bat", ".cmd", ".com", ".scr",
    ".vbs", ".vbe", ".wsf", ".wsh", ".ps1", ".psm1",
    ".jar", ".dll", ".sys"
)

# Suspicious patterns in file names
$script:SuspiciousPatterns = @(
    "keylog", "stealer", "inject", "hook", "dump",
    "crack", "keygen", "patch", "loader"
)

function Test-SkillSecurity {
    <#
    .SYNOPSIS
        Check if skill folder contains potentially dangerous files
    .PARAMETER SkillPath
        Full path to the skill folder
    .RETURNS
        Hashtable with IsSafe, Warnings, DangerousFiles
    #>
    param([string]$SkillPath)

    $result = @{
        IsSafe = $true
        Warnings = @()
        DangerousFiles = @()
        SuspiciousFiles = @()
    }

    # Get all files recursively
    $files = Get-ChildItem -Path $SkillPath -Recurse -File -ErrorAction SilentlyContinue

    foreach ($file in $files) {
        # Check for dangerous extensions
        if ($script:DangerousExtensions -contains $file.Extension.ToLower()) {
            $result.DangerousFiles += $file.FullName
            $result.Warnings += "Dangerous file type: $($file.Name)"
        }

        # Check for suspicious names
        foreach ($pattern in $script:SuspiciousPatterns) {
            if ($file.Name -like "*$pattern*") {
                $result.SuspiciousFiles += $file.FullName
                $result.Warnings += "Suspicious filename: $($file.Name)"
            }
        }
    }

    if ($result.DangerousFiles.Count -gt 0 -or $result.SuspiciousFiles.Count -gt 0) {
        $result.IsSafe = $false
    }

    return $result
}

# ============================================================================
# Agent Validation
# ============================================================================

function Test-IsValidAgent {
    <#
    .SYNOPSIS
        Verify folder is a real AI agent (not just any folder with skills/)
    .PARAMETER AgentPath
        Full path to the agent folder in Hub
    .RETURNS
        Hashtable with IsValid, ToolType, ConfigFiles
    #>
    param([string]$AgentPath)

    $result = @{
        IsValid = $false
        ToolType = "Unknown"
        ConfigFiles = @()
        SkillsFormat = "Unknown"
    }

    $folderName = Split-Path $AgentPath -Leaf

    # Check against known AI tool definitions
    foreach ($tool in $script:AIToolDefinitions.Keys) {
        $def = $script:AIToolDefinitions[$tool]

        # Check if folder name matches any of the tool's known names
        $nameMatch = $def.Names | Where-Object {
            $folderName -like "*$_*" -or $folderName -like "${_}_*"
        }

        if ($nameMatch) {
            # Check for config files
            foreach ($configFile in $def.ConfigFiles) {
                $configPath = Join-Path $AgentPath $configFile
                if (Test-Path $configPath) {
                    $result.ConfigFiles += $configFile
                }
            }

            if ($result.ConfigFiles.Count -gt 0) {
                $result.IsValid = $true
                $result.ToolType = $tool
                $result.SkillsFormat = $def.Category
                return $result
            }
        }
    }

    # Fallback: if has skills folder with valid skills, consider it valid
    $skillsPath = Join-Path $AgentPath "skills"
    if (Test-Path $skillsPath) {
        $skills = Get-ChildItem -Path $skillsPath -Directory -ErrorAction SilentlyContinue
        $validSkillCount = 0
        foreach ($skill in $skills) {
            if (Test-IsValidSkill -SkillPath $skill.FullName) {
                $validSkillCount++
            }
        }
        if ($validSkillCount -gt 0) {
            $result.IsValid = $true
            $result.ToolType = "Unknown (has valid skills)"
            return $result
        }
    }

    return $result
}

function Get-SkillFormat {
    <#
    .SYNOPSIS
        Detect the format/type of a skill
    .PARAMETER SkillPath
        Full path to the skill folder
    .RETURNS
        String: MCP, VSCode, Continue, Zed, Generic, or Unknown
    #>
    param([string]$SkillPath)

    foreach ($format in $script:SkillFormats.Keys) {
        $def = $script:SkillFormats[$format]

        foreach ($sig in $def.Signatures) {
            $sigPath = Join-Path $SkillPath $sig
            if (Test-Path $sigPath) {
                return $format
            }
        }
    }

    return "Unknown"
}

function Test-IsValidSkill {
    <#
    .SYNOPSIS
        Check if folder is a valid skill (has expected files)
    .PARAMETER SkillPath
        Full path to the skill folder
    .RETURNS
        $true if valid skill, $false otherwise
    #>
    param([string]$SkillPath)

    foreach ($file in $script:SkillSignatureFiles) {
        $filePath = Join-Path $SkillPath $file
        if (Test-Path $filePath) {
            return $true
        }
    }
    return $false
}

# ============================================================================
# Export for dot-sourcing
# ============================================================================

# When this script is dot-sourced, these become available:
# - $script:HubDir
# - $script:TaskName
# - $script:AIToolDefinitions
# - $script:StrictKeywords
# - $script:SkillSources
# - $script:SkillFormats
# - $script:DangerousExtensions
# - Test-IsAIToolByName
# - Test-IsAIToolByConfig
# - Get-AIToolInfo
# - Test-IsValidSkill
# - Test-SkillSecurity
# - Test-IsValidAgent
# - Get-SkillFormat
