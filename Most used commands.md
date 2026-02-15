# Powershell 

> ## Find all using keywords
> ```pwsh
> Get-ChildItem -Path C:\ -Recurse -Filter *notebook* -ErrorAction SilentlyContinue
> ```
> 
> ```pwsh
> Gci -Path ~\ -r -fi "*notebook*"
> ```
> PowerShell aliases:
> - gci → Get-ChildItem
> - -r → -Recurse
> - -fi → -Filter
> 
> ## After uninstalled
> ### 1. Program folders
> Search the two main install locations first:
> ```pwsh
> gci "C:\Program Files","C:\Program Files (x86)" -Recurse -Directory -Filter "*appname*"
> ```
> ### 2. AppData (very common)
> Many uninstallers ignore user data.
> ```pwsh
> gci $env:LOCALAPPDATA,$env:APPDATA -Recurse -Directory -Filter "*appname*"
> ```
> Typical leftovers:
> - caches
> - configs
> - logs
> ### 3. ProgramData 
> Often used for shared machine data:
> ```pwsh
> gci "C:\ProgramData" -Recurse -Directory -Filter "*appname*"
> ```
> 
> ## Extremely useful trick (most people never use this)
> Search by **today’s changes** instead of name:
> ```pwsh
> gci C:\ -Recurse -ErrorAction SilentlyContinue | where LastWriteTime -gt (Get-Date).AddHours(-2)


---
## Active Tasks
> ``` pwsh
> Schtasks /query /fo LIST /v
> ```

