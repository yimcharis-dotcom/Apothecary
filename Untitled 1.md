```powershell
 # Copy all files except node_modules
Get-ChildItem "C:\Users\YC\MCPs\vault-bridge" -Exclude "node_modules" |
    Copy-Item -Destination "C:\Vault\AI hub\Apothecary\vault-bridge\" -Recurse -Force
```

```powershell
# Save this as backup-to-obsidian.ps1 in your vault-bridge folder
$source = "C:\Users\YC\MCPs\vault-bridge"
$dest = "C:\Vault\AI hub\Apothecary\vault-bridge"

# Create destination folder
New-Item -ItemType Directory -Force -Path $dest | Out-Null

# Copy files
Copy-Item "$source\complete_bridge.cjs" -Destination $dest -Force
Copy-Item "$source\config.json" -Destination $dest -Force
Copy-Item "$source\package.json" -Destination $dest -Force

Write-Host "Files copied to Obsidian vault!" -ForegroundColor Green
```
