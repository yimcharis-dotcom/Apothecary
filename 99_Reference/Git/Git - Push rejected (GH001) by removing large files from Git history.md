---
created: 2026-02-08
updated: 2026-02-08T10:43:00
tags:
  - git
  - github
  - powershell
  - troubleshooting
  - history-rewrite
  - filter-repo
source: https://github.com/newren/git-filter-repo
---

## Context

GitHub rejects pushes when any file in the pushed history exceeds 100 MB (GH001). `.gitignore` prevents future tracking but does not remove files already committed. The fix is to remove the large file from the index (for the current state) and, if it was ever committed, purge it from history.

This note assumes:
- Windows + PowerShell
- Repo root is `C:\Vault\Apothecary`
- Large file example:  
  `30_Automation/303_AI_HubWatch - Automation/dashboard/collectors/All mail Including Spam and Trash.mbox`

## 0) Confirm you are in the repo root

```powershell
cd C:\Vault\Apothecary
git status
````

## 1) Add ignore rule (prevents re-tracking later)

Edit `.gitignore` and add one of the following patterns (prefer folder-wide for mailbox exports):

Ignore all `.mbox` in that folder:

```
30_Automation/303_AI_HubWatch - Automation/dashboard/collectors/*.mbox
```

Or ignore only that file (narrow):

```
30_Automation/303_AI_HubWatch - Automation/dashboard/collectors/All mail Including Spam and Trash.mbox
```

Notes:

- Use forward slashes in `.gitignore`.
    
- Do not wrap patterns in quotes.
    

## 2) Stop tracking the file in the current snapshot (index only)

```powershell
git rm --cached "30_Automation/303_AI_HubWatch - Automation/dashboard/collectors/All mail Including Spam and Trash.mbox"
git add .gitignore
git commit -m "Ignore mailbox exports"
```

This keeps the file on disk but removes it from Git tracking.

## 3) If GitHub still rejects push (file exists in past commits): purge history

### 3.1 Verify Python is available

```powershell
python --version
```

### 3.2 Run git-filter-repo via Python module (avoids PATH issues)

```powershell
python -m git_filter_repo --path "30_Automation/303_AI_HubWatch - Automation/dashboard/collectors/All mail Including Spam and Trash.mbox" --invert-paths --force
```

What to expect:

- It rewrites history.
    
- It may remove the `origin` remote to prevent accidental push.
    

## 4) Re-add the remote if filter-repo removed it

```powershell
git remote add origin https://github.com/yimcharis-dotcom/Apothecary.git
git remote -v
```

## 5) Force push rewritten history

```powershell
git push --force --set-upstream origin main
```

If you use tags:

```powershell
git push --force --tags
```

## 6) Confirm the large file is gone from history (optional)

```powershell
git log -- "30_Automation/303_AI_HubWatch - Automation/dashboard/collectors/All mail Including Spam and Trash.mbox"
```

Expected: no output.

## 7) Common PowerShell gotcha

In PowerShell, `&` is the call operator, not “run in background” like Bash.  
Do not use `&` between `git rm --cached` and a path.

## Aftercare

- Any other clones of the repo must re-clone or hard reset because commit IDs changed.
    
- Keep the `.gitignore` rule so mailbox exports cannot re-enter Git history.
    
- Consider storing large exports outside the repo (or use Git LFS if truly needed).
    

---

## References

- GitHub large file rejection: GH001 (100 MB limit)
    
- `git-filter-repo` manual: explains history rewriting and why remotes may be removed
    

```