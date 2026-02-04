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
5. **Save:** `git add .` -> `git commit -m "Update"`
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
