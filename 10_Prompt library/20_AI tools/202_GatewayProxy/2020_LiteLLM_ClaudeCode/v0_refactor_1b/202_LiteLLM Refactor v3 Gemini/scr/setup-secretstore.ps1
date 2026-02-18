param(
    [string]$VaultName = "LiteLLM"
)

$ErrorActionPreference = "Stop"

Write-Host "Setting up SecretManagement + SecretStore..." -ForegroundColor Cyan

if (-not (Get-Command Get-Secret -ErrorAction SilentlyContinue)) {
    Write-Host "Installing required PowerShell modules (CurrentUser scope)..." -ForegroundColor Yellow
    Install-Module Microsoft.PowerShell.SecretManagement -Scope CurrentUser -Force
    Install-Module Microsoft.PowerShell.SecretStore -Scope CurrentUser -Force
}

if (-not (Get-SecretVault -Name $VaultName -ErrorAction SilentlyContinue)) {
    Register-SecretVault -Name $VaultName -ModuleName Microsoft.PowerShell.SecretStore -DefaultVault
    Write-Host "Registered vault: $VaultName" -ForegroundColor Green
}

Write-Host ""
Write-Host "Set secrets (prompts securely):" -ForegroundColor Cyan
$secretNames = @(
    "LITELLM_MASTER_KEY",
    "XAI_API_KEY",
    "PERPLEXITY_API_KEY",
    "GEMINI_API_KEY",
    "OPENROUTER_API_KEY",
    "OPENAI_API_KEY"
)

foreach ($name in $secretNames) {
    Write-Host "Enter value for $name (leave blank to skip):" -ForegroundColor Yellow
    $secure = Read-Host -AsSecureString
    $ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
    try {
        $plain = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr)
    } finally {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr)
    }

    if (-not [string]::IsNullOrWhiteSpace($plain)) {
        Set-Secret -Vault $VaultName -Name $name -Secret $plain
        Write-Host "Saved $name" -ForegroundColor Green
    } else {
        Write-Host "Skipped $name" -ForegroundColor DarkYellow
    }
}

Write-Host ""
Write-Host "Done. Load runtime env with:" -ForegroundColor Cyan
Write-Host "  .\\set-env.ps1" -ForegroundColor Gray
