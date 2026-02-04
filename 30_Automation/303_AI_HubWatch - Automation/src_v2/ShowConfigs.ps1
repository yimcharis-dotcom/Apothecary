# ShowConfigs.ps1
# Find and display config files across all AI agents in the Hub
# v1: Initial implementation

# Load shared config
$configPath = Join-Path $PSScriptRoot "AIToolsConfig.ps1"
if (Test-Path $configPath) {
    . $configPath
}

$HubDir = if ($script:HubDir) { $script:HubDir } elseif ($env:AI_HUB_PATH) { $env:AI_HUB_PATH } else { "$env:USERPROFILE\AI_hub" }

# Config file patterns to search for
$configPatterns = @(
    "config.json",
    "settings.json",
    "claude_desktop_config.json",
    "mcp*.json",
    "*.yaml",
    "*.yml",
    "*.toml",
    ".env",
    "hosts.json",
    "keymap.json",
    "extensions.json"
)

Write-Host "`n=== Config Files Inventory ===" -ForegroundColor Cyan

# Get all agents
$agents = Get-ChildItem -Path $HubDir -Directory | Sort-Object Name

$totalConfigs = 0
$configIndex = @{}

foreach ($agent in $agents) {
    $agentConfigs = @()

    foreach ($pattern in $configPatterns) {
        $found = Get-ChildItem -Path $agent.FullName -Filter $pattern -File -Recurse -Depth 2 -ErrorAction SilentlyContinue
        if ($found) {
            $agentConfigs += $found
        }
    }

    if ($agentConfigs.Count -gt 0) {
        Write-Host "`n$($agent.Name):" -ForegroundColor Green

        foreach ($config in $agentConfigs) {
            # Get relative path from agent folder
            $relativePath = $config.FullName.Substring($agent.FullName.Length + 1)
            Write-Host "  - $relativePath" -ForegroundColor White

            # Track config types
            $configType = $config.Name
            if (-not $configIndex.ContainsKey($configType)) {
                $configIndex[$configType] = @()
            }
            $configIndex[$configType] += $agent.Name

            $totalConfigs++
        }
    }
}

# Summary
Write-Host "`n=== Summary ===" -ForegroundColor Cyan
Write-Host "Total agents scanned: $($agents.Count)"
Write-Host "Total config files found: $totalConfigs"
Write-Host "Unique config types: $($configIndex.Count)"

# Config type distribution
Write-Host "`n=== Config Types ===" -ForegroundColor Cyan
$configIndex.GetEnumerator() | Sort-Object { $_.Value.Count } -Descending | ForEach-Object {
    $count = $_.Value.Count
    Write-Host "  $($_.Key): $count agents" -ForegroundColor Yellow
}

# MCP-specific configs
Write-Host "`n=== MCP Configurations ===" -ForegroundColor Magenta
$mcpConfigs = Get-ChildItem -Path $HubDir -Filter "mcp*.json" -Recurse -File -ErrorAction SilentlyContinue
if ($mcpConfigs) {
    foreach ($mcp in $mcpConfigs) {
        Write-Host "  $($mcp.FullName)" -ForegroundColor White
    }
} else {
    Write-Host "  (none found)" -ForegroundColor DarkGray
}
