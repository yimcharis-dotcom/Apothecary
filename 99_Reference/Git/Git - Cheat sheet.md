---
tags: [git, cheatsheet, workflow, collab, claude]
---

# Git Cheat Sheet

## 📥 Fetching & Pulling

| Command | What it does |
|---|---|
| `git fetch` | Download remote changes only (safe, no changes to files) |
| `git merge` | Apply changes with a merge commit |
| `git rebase` | Apply changes cleanly (no merge commit) |
| `git pull` | Fetch + merge |
| `git pull --rebase` | Fetch + rebase ✅ (recommended) |

```bash
git pull --rebase         # Recommended way to pull
git pull origin main      # Pull specific branch
```

## 📤 Staging & Committing

```bash
git status                # Check what's changed
git add .                 # Stage all changes
git add <file>            # Stage specific file
git commit -m "message"   # Commit with message
git push                  # Push to remote
```

## 🔀 Branching

```bash
git branch                        # List branches
git branch <branch-name>          # Create branch
git checkout <branch-name>        # Switch branch
git checkout -b <branch-name>     # Create and switch
git branch -d <branch-name>       # Delete local branch
git push origin --delete <branch-name>  # Delete remote branch
```

## 🕒 History

```bash
git log --oneline -5          # Last 5 commits
git log --graph --all         # Visual branch history
```

## 📦 Stashing

```bash
git stash                     # Save local changes
git pull                      # Update from remote
git stash pop                 # Restore local changes
```

## ⚠️ Common Issues

### "Your branch is behind 'origin/main'"

```bash
git pull --rebase
```

### "You have diverged branches"

```bash
git fetch origin
git rebase origin/main
```

### "Merge conflicts"

```bash
# Fix conflicts in editor, then:
git add <resolved-file>
git commit
```

## 🔄 Two Claude Code Modes

### Remote Repository Mode

- Claude connects to GitHub repository
- Changes committed and pushed remotely
- You pull them later
- **No dots in Cursor** until you pull

### Local MCP Filesystem Mode

- Claude uses MCP to edit local files
- Changes made directly on your machine
- **Dots appear immediately** in Cursor
- You stage and commit manually

## 📊 Git Status Indicators in Cursor

| Indicator | Meaning |
|---|---|
| 🟢 Green dots | Staged changes (ready to commit) |
| 🟠 Orange dots | Modified but unstaged |
| No dots | Clean working directory |

## 📚 Related Notes

- [[MCP Bridge Setup]]
- [[Python Virtual Environment Setup]]
- [[Obsidian Vault Structure]]
