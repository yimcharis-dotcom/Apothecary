---
tags:
  - git
  - cheatsheet
  - workflow
  - collab
  - claude
created: 2026-01-22
updated: 2026-02-04
aliases:
  - Git-Cheatsheet
  - Claude-Git-Workflow
---
# Explanation of the Git Commands

### **Command Breakdown:**

```bash
git checkout claude/setup-mcp-client-K5lbl
```

**What it does:** Switches your working directory to Claude's feature branch  
**Why:** Lets you inspect what Claude changed before merging  
**Result:** You're now on Claude's branch, can see his files and commits

```bash
git log --oneline -5
```

**What it does:** Shows the last 5 commits in compact format  
**Why:** Quick overview of what Claude committed  
**Result:** See commit hashes and messages like "26 df 142 Update paths: Remove OneDrive/Desktop..."

```bash
git checkout main
```

**What it does:** Switches back to your main branch  
**Why:** Merging happens FROM a feature branch INTO main  
**Result:** You're back on main, ready to merge

```bash
git merge claude/setup-mcp-client-K5lbl
```

**What it does:** Integrates Claude's branch changes into main  
**Why:** Brings Claude's work into your main codebase  
**Result:** main now contains Claude's commits (fast-forward merge if no conflicts)

```bash
git commit -m "Merge Claude's MCP client setup"
```

**What it does:** Creates a merge commit (only needed if not fast-forward)  
**Why:** Documents the merge in git history  
**Result:** Permanent record of when/why branches were merged

## 🔄 **Why This Workflow?**

- **Safety:** Inspect changes before merging
- **Clarity:** See exactly what's being integrated
- **History:** Clean git log showing the merge point
- **Reversible:** Can undo if something breaks

---

### After Claude Finishes (Remote Session)

```bash
# 1. Download latest info
git fetch origin              

# 2. Check what's available
git status                    

# 3. Merge Claude's changes
git pull origin main          

# 4. Verify merge
git status                    
```

## 🔍 Reviewing Claude's Changes Before Merging

```bash
# 1. Switch to Claude's feature branch
git checkout claude/setup-mcp-client-K5lbl

# 2. Inspect recent commits
git log --oneline -5

# 3. Return to main
git checkout main

# 4. Merge Claude's work
git merge claude/setup-mcp-client-K5lbl

# 5. Create merge commit (if needed)
git commit -m "Merge Claude's MCP client setup"

# 6. Push to remote
git push origin main
```

## 📋 Complete Workflow Summary

```bash
# Step 1: Prepare (before Claude works)
git status && git pull origin main

# Step 2: Claude works remotely → commits & pushes

# Step 3: Sync Claude's changes
git fetch origin && git pull origin main

# Step 4: Add your local changes (if any)
git add -A
git commit -m "Local updates"
git push origin main
```

## 🚨 Conflict Resolution

```bash
git pull origin main
# If conflicts occur:
# 1. Edit conflicted files in your editor
# 2. Stage resolved files
git add <resolved-files>
# 3. Complete the merge
git commit  # Git suggests merge commit message
# 4. Push changes
git push origin main
```

## 🎯 Key Principles

1. **Always pull before starting** - ensures you're up-to-date
2. **Fetch first, then pull** - safer, shows what's coming
3. **Check status frequently** - know what state you're in
4. **Commit logical units** - group related changes together
5. **Push promptly** - keep remote repository in sync

## 💡 Pro Tips

### Use Branches for Experimental Work

```bash
git checkout -b feature/new-idea
# Work on feature
git add . && git commit -m "Feature complete"
git push origin feature/new-idea
```

### Stash Local Changes Before Pulling

```bash
git stash                     # Save local changes
git pull                      # Update from remote
git stash pop                 # Restore local changes
```

### Check Recent History

```bash
git log --oneline -5          # Last 5 commits
git log --graph --all         # Visual branch history
```

### Clean Up Old Branches

```bash
git branch -d <branch-name>   # Delete local branch
git push origin --delete <branch-name>  # Delete remote branch
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

- **Green dots**: Staged changes (ready to commit)
- **Orange dots**: Modified but unstaged files  
- **No dots**: Clean working directory

## ⚠️ Common Issues

### "Your branch is behind 'origin/main'"

```bash
git pull origin main
```

### "You have diverged branches"

```bash
git fetch origin
git rebase origin/main  # Or: git merge origin/main
```

### "Merge conflicts"

```bash
# Fix conflicts in editor, then:
git add <resolved-files>
git commit
```

## ✅ Quick Definitions

- `origin` = the remote name (usually GitHub)
- `origin/main` = your local copy of the remote `main` branch
- `git add -A` = stage new + modified + deleted files
- `git add .` = stage new + modified (may miss deletions)

## ✅ `git status -sb` Symbols

- `M` = modified
- `D` = deleted
- `??` = untracked (new)
- `## main...origin/main` = local `main` matches remote tracking branch

## ✅ Windows Warnings (Common)

- LF → CRLF warnings are line-ending notices, not errors.
- Embedded repo warning means a folder inside your repo has its own `.git`.
- `invalid path 'nul'` means a Windows reserved filename was created.

## 📚 Related Notes

- [[MCP Bridge Setup]]
- [[Python Virtual Environment Setup]]
- [[Obsidian Vault Structure]]

---

**Last Updated**: 2026-02-04  
**Tested With**: Git 2.x, Claude Code, Cursor IDE
