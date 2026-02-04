Git Workflow Guide
---

updated: 20260204
created: 20260204
tags: #git, #workflow, #guide, #cheatsheet

## 1. The Golden Rule: "Pull First"

Always "read" the latest changes from the server before you start "writing" new ones.

## 2. The Daily Routine

1. **Sit down.**
2. **Check:** `git status` (Is my desk clean?)
3. **Pull:** `git pull` (Get latest updates)
4. **Work:** (Do your magic)
5. **Save:** `git add -A` -> `git commit -m "Update"`
6. **Push:** `git push`

## 3. Dealing with Agents (Branches)

If an agent pushes to a new "Branch" (like `claude/...`):

1. `git fetch` (Update list)
2. `git checkout <branch-name>` (Switch to their version)
3. Review their work.
4. If good:
    * `git checkout main` (Go back to main)
    * `git merge <branch-name>` (Combine their work into main)
    * `git push`
5. `git switch -c claude-work` (Create a new branch for yourself)

## 4. Status Symbols (What You
See in `git status -sb`)

`M` = modified file  
`D` = deleted file  
`??` = untracked (new) file  
`## main...origin/main` = local branch matches remote tracking branch

## 5. Switching Branches When You Have Changes

If `git switch main` is blocked, choose one path:

1. Commit now
2. Stash temporarily
3. Discard changes

### Commit Now (keep changes)

```bash
git add -A
git commit -m "WIP"
git switch main
```

### Stash (pause changes)

```bash
git stash -u
git switch main
git stash pop
```

### Discard (lose changes)

```bash
git reset --hard
git clean -fd
git switch main
```

## 6. `git add .` vs `git add -A`

`git add .` = new + modified (may miss deletions)  
`git add -A` = new + modified + deletions

## 7. Remote Tracking (`origin/main`)

`origin` = remote name (usually GitHub)  
`origin/main` = your local copy of the remote `main` branch  
Use `git fetch` to refresh it.

## 8. Common Warnings (Windows)

LF → CRLF warnings are line-ending notices. They are not errors.  
`invalid path 'nul'` means a Windows reserved filename was created.  
Embedded repo warning means a folder inside your repo contains a `.git` folder.

## 9. Safe Merge Flow (Local Work → `main`)

```bash
git status -sb
git add -A
git commit -m "WIP: merge work"
git switch main
git merge <your-branch>
git push origin main
```
