param(
    [string]$VaultName = "LiteLLM"
)

$ErrorActionPreference = "Stop"

function Get-SecretValue {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Name,
        [Parameter(Mandatory = $true)]
        [string]$Vault
    )

    try {
        return Get-Secret -Name $Name -Vault $Vault -AsPlainText -ErrorAction Stop
    } catch {
        return $null
    }
}

if (-not (Get-Command Get-Secret -ErrorAction SilentlyContinue)) {
    Write-Host "Get-Secret command not found." -ForegroundColor Red
    Write-Host "Install required modules first:" -ForegroundColor Yellow
    Write-Host "  Install-Module Microsoft.PowerShell.SecretManagement -Scope CurrentUser" -ForegroundColor Gray
    Write-Host "  Install-Module Microsoft.PowerShell.SecretStore -Scope CurrentUser" -ForegroundColor Gray
    Write-Host "Then run .\\setup-secretstore.ps1 to create/load secrets." -ForegroundColor Gray
    exit 1
}

if (-not (Get-SecretVault -Name $VaultName -ErrorAction SilentlyContinue)) {
    Write-Host "Secret vault '$VaultName' not found." -ForegroundColor Red
    Write-Host "Run .\\setup-secretstore.ps1 to initialize the vault." -ForegroundColor Yellow
    exit 1
}

# Required secret: proxy auth master key.
$masterKey = Get-SecretValue -Name "LITELLM_MASTER_KEY" -Vault $VaultName
if ([string]::IsNullOrWhiteSpace($masterKey)) {
    Write-Host "Missing required secret: LITELLM_MASTER_KEY" -ForegroundColor Red
    Write-Host "Set it with: Set-Secret -Vault $VaultName -Name LITELLM_MASTER_KEY -Secret '<value>'" -ForegroundColor Yellow
    exit 1
}
$env:LITELLM_MASTER_KEY = $masterKey

# Optional provider secrets. Missing values are allowed.
$optionalSecretNames = @(
    "XAI_API_KEY",
    "PERPLEXITY_API_KEY",
    "GEMINI_API_KEY",
    "OPENROUTER_API_KEY"
)

foreach ($secretName in $optionalSecretNames) {
    $secretValue = Get-SecretValue -Name $secretName -Vault $VaultName
    if (-not [string]::IsNullOrWhiteSpace($secretValue)) {
        Set-Item -Path "env:$secretName" -Value $secretValue
    } else {
        Write-Host "Optional secret not found: $secretName" -ForegroundColor DarkYellow
    }
}

# Claude Code -> LiteLLM proxy routing
$env:ANTHROPIC_BASE_URL = "http://127.0.0.1:4000"
$env:ANTHROPIC_AUTH_TOKEN = $env:LITELLM_MASTER_KEY
$env:ANTHROPIC_API_KEY = $env:LITELLM_MASTER_KEY

# Non-secret runtime config
if ([string]::IsNullOrWhiteSpace($env:LITELLM_DATABASE_URL)) {
    $defaultDbPath = Join-Path $env:USERPROFILE "LiteLLM\litellm.db"
    $env:LITELLM_DATABASE_URL = "sqlite:///$($defaultDbPath -replace '\\','/')"
}

Write-Host "Environment variables loaded from SecretStore vault '$VaultName'." -ForegroundColor Green
