---
name: github-code-review
description: "Review PRs: diffs, inline comments via gh or REST."
version: 1.2.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [GitHub, Code-Review, Pull-Requests, Git, Quality]
    related_skills: [github-auth, github-pr-workflow]
---

# GitHub Code Review

Review pull requests on GitHub or perform code reviews on local changes before pushing. Local reviews use plain `git`. PR-level interactions use `gh` CLI or GitHub REST API.

## Prerequisites

- Authenticated with GitHub (see `github-auth` skill)
- Inside a git repository

---

## Setup: Detecting Environment and Repository Context

Run this block at the start of any PR interaction to configure authentication and repository details:

bash
# Detect authentication method (gh CLI preferred, fallback to git with token)
if command -v gh &>/dev/null && gh auth status &>/dev/null; then
  AUTH="gh"
else
  AUTH="git"
  # Fallback: find GitHub token from common locations
  if [ -z "$GITHUB_TOKEN" ]; then
    if [ -f ~/.hermes/.env ] && grep -q "^GITHUB_TOKEN=" ~/.hermes/.env; then
      GITHUB_TOKEN=$(grep "^GITHUB_TOKEN=" ~/.hermes/.env | head -1 | cut -d= -f2 | tr -d '\n\r')
    elif [ -f ~/.git-credentials ] && grep -q "github.com" ~/.git-credentials; then
      GITHUB_TOKEN=$(grep "github.com" ~/.git-credentials | head -1 | sed 's|https://[^:]*:\([^@]*\)@.*|\1|')
    fi
  fi
fi

# Extract repository context from git remote
REMOTE_URL=$(git remote get-url origin 2>/dev/null)
OWNER_REPO=$(echo "$REMOTE_URL" | sed -E 's|.*github\.com[:/]||; s|\.git$||')
OWNER=$(echo "$OWNER_REPO" | cut -d/ -f1)
REPO=$(echo "$OWNER_REPO" | cut -d/ -f2)
---

## 1. Reviewing Local Changes (Pre-Push)

Use these commands when you want to review changes before pushing or opening a PR. No API authentication needed — works offline.

### Get the Diff

bash
# Staged changes (what will be committed on next push)
git diff --staged

# All uncommitted changes vs main branch
git diff main...HEAD

# All changes since branching from main
git diff main..HEAD

# Only changed file names
git diff main...HEAD --name-only

# Stat summary: insertions/deletions per file
git diff main...HEAD --stat

# Diff specific file or directory
git diff main...HEAD -- path/to/file.py
### Systematic Review Strategy

**Step 1: Get the big picture**

bash
git diff main...HEAD --stat
git log main..HEAD --oneline
**Step 2: Review file by file** — use `read_file` for full context, then diff to see changes:

bash
git diff main...HEAD -- path/to/file.py
**Step 3: Check for common issues**

bash
# Debug code left behind
git diff main...HEAD | grep -n "print(\|console\.log\|TODO\|FIXME\|HACK\|XXX\|debugger"

# Large files accidentally staged
git diff main...HEAD --stat | awk '{print $5, $2}' | sort -rn | head -10

# Secrets or credential patterns
git diff main...HEAD | grep -Ein "password|secret|api_key|token.*=|private_key"

# Merge conflict markers
git diff main...HEAD | grep -n "^<<<<\|^====\|^>>>>"
---

## 2. Reviewing GitHub Pull Requests

Use `gh` CLI (preferred) or direct API calls for PR-level interactions.

### List and Select PRs

bash
# List open PRs for the current branch (if any)
gh pr list --state open

# View PR details
gh pr view PR_NUMBER

# Get diff for a PR
gh pr diff PR_NUMBER
### Viewing PR Changes

bash
# Full diff of a PR
gh pr diff 123

# Diff with stat summary
gh pr diff 123 --stat

# Review a specific file in the PR
gh pr diff 123 -- path/to/file.py
### Inline Comments with gh

bash
# Create a review with inline comments
gh pr review PR_NUMBER \
  --body "Reviewed the changes. Overall looks good but see inline comments." \
  --request-changes  # or --approve or --comment

# Add a single inline comment on a specific line
gh pr comment PR_NUMBER \
  --body "Consider using a constant here instead of magic number." \
  --path path/to/file.py \
  --line 42
---

## 3. Advanced Review Techniques

### Deep File Analysis

bash
# Show commits that modified a file
git log --oneline main..HEAD -- path/to/file.py

# Show who changed each line (blame)
git blame path/to/file.py

# Compare two branches directly
git diff main..feature-branch -- path/to/file.py

# View staged changes with word diff (see actual text changes)
git diff --staged --word-diff
### Contextual Review Commands

bash
# Review files by type
git diff main...HEAD -- '*.py'   # Python files
git diff main...HEAD -- '*.ts'    # TypeScript files

# Show only added lines (green in diff)
git diff main...HEAD -- . | grep "^+" | grep -v "^+++"

# Find files with most changes (likely highest risk)
git diff main...HEAD --stat | sort -t'|' -k2 -rn | head -5

# Check for whitespace issues
git diff main...HEAD | grep -n " +$"
---

## 4. Common Workflows

### Review Before Push

bash
# 1. Check what will be pushed
git status

# 2. Review changes against main
git diff main...HEAD --stat

# 3. Spot-check key files
git diff main...HEAD -- src/

# 4. Run any pre-commit hooks
git diff --staged | head -100  # quick sanity check
### Review a colleague's PR

bash
# Fetch and view their branch
gh pr checkout PR_NUMBER

# Review systematically
gh pr diff PR_NUMBER --stat

# Add review comments
gh pr review PR_NUMBER --comment --body "See inline comments"
---

## Error Handling

- **No token found**: Ensure `GITHUB_TOKEN` is set or authenticate with `gh auth login`
- **Not in a repo**: Navigate to a directory with `.git/` or clone a repository
- **gh not installed**: Install from https://cli.github.com/ or fall back to API calls
- **Permission denied on PR**: Ensure you have push access or the repo allows PR reviews from maintainers

---

## Related Skills

- `github-auth` — GitHub authentication setup
- `github-pr-workflow` — Creating and managing pull requests