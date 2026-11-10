--- (YAML frontmatter)
6. Use markdown syntax naturally

The current skill covers:
- Prerequisites
- Setup for PR interactions
- Reviewing local changes (pre-push)
- Getting diffs
- Review strategy

The current content seems to be cut off at the end (about merge conflict markers). I should complete the thought and also improve the overall structure and clarity.

Let me rewrite this to be more comprehensive and clear:

1. Keep the YAML frontmatter as-is
2. Improve the introduction
3. Better organize prerequisites
4. Keep the setup script but maybe simplify/comment it
5. Better organize the local review section with clearer subsections
6. Add a PR review section (since the title mentions "Review PRs: diffs, inline comments via gh or REST")
7. Make the common issues check more useful
8. Add guidance on what to look for in reviews

Let me write this out properly.
</think>

---
name: github-code-review
description: "Review PRs: diffs, inline comments via gh or REST."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [GitHub, Code-Review, Pull-Requests, Git, Quality]
    related_skills: [github-auth, github-pr-workflow]
---

# GitHub Code Review

Perform code reviews on local changes before pushing, or review open pull requests on GitHub using `gh` CLI or the REST API. Most operations use plain `git` — the `gh`/`curl` distinction only applies to PR-specific interactions.

## Prerequisites

- GitHub authentication configured (see `github-auth` skill)
- Working inside a git repository

## Setup

Before running PR operations, source the authentication block below. This detects whether `gh` CLI is available and authenticated, falling back to token-based authentication via `GITHUB_TOKEN`, `~/.hermes/.env`, or `~/.git-credentials`.

bash
# Detect authentication method
if command -v gh &>/dev/null && gh auth status &>/dev/null; then
  AUTH="gh"
else
  AUTH="git"
  # Try to load token from environment or config files
  if [ -z "$GITHUB_TOKEN" ]; then
    if [ -f ~/.hermes/.env ] && grep -q "^GITHUB_TOKEN=" ~/.hermes/.env; then
      GITHUB_TOKEN=$(grep "^GITHUB_TOKEN=" ~/.hermes/.env | head -1 | cut -d= -f2 | tr -d '\n\r')
    elif grep -q "github.com" ~/.git-credentials 2>/dev/null; then
      GITHUB_TOKEN=$(grep "github.com" ~/.git-credentials 2>/dev/null | head -1 | sed 's|https://[^:]*:\([^@]*\)@.*|\1|')
    fi
  fi
fi

# Extract repository information from origin remote
REMOTE_URL=$(git remote get-url origin)
OWNER_REPO=$(echo "$REMOTE_URL" | sed -E 's|.*github\.com[:/]||; s|\.git$||')
OWNER=$(echo "$OWNER_REPO" | cut -d/ -f1)
REPO=$(echo "$OWNER_REPO" | cut -d/ -f2)
---

## 1. Review Local Changes (Pre-Push)

Review code locally before pushing. No API calls required — pure `git` commands work everywhere.

### Get the Diff

bash
# View staged changes (what would be committed)
git diff --staged

# View all changes from main branch to current HEAD
git diff main...HEAD

# View changes against a different base branch
git diff develop...HEAD

# List only changed file names
git diff main...HEAD --name-only

# Stat summary: insertions/deletions per file
git diff main...HEAD --stat

# Show diff for a specific file
git diff main...HEAD -- path/to/file.py
### Review Workflow

**Step 1: Get the big picture**

bash
# Summary of all changes
git diff main...HEAD --stat

# Commit history between branches
git log main..HEAD --oneline
**Step 2: Examine individual files**

bash
# Review a specific file's changes
git diff main...HEAD -- src/auth/login.py

# Read full file for context
read_file path/to/file.py
**Step 3: Check for common issues**

bash
# Debug statements and temporary code left behind
git diff main...HEAD | grep -n "print(\|console\.log\|TODO\|FIXME\|HACK\|XXX\|debugger"

# Large files accidentally staged
git diff main...HEAD --stat | awk '{print $1, $6}' | sort -t'/' -k2 -rn | head -10

# Hardcoded secrets or credentials
git diff main...HEAD | grep -in "password\|secret\|api_key\|token.*=\|private_key"

# Unresolved merge conflict markers
git diff main...HEAD | grep -n "^<<<<<<<\|^=======\|^>>>>>>>"
---

## 2. Review Pull Requests on GitHub

### List Open PRs

bash
# Using gh CLI (preferred if available)
gh pr list --state open --repo "$OWNER/$REPO"

# Using REST API
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/$OWNER/$REPO/pulls?state=open"
### View PR Details

bash
# PR metadata (title, author, branch, description)
gh pr view 123 --repo "$OWNER/$REPO"

# List commits in a PR
gh pr view 123 --repo "$OWNER/$REPO" --json commits

# Get PR diff/patch
gh pr diff 123 --repo "$OWNER/$REPO"
### Review Files Changed

bash
# List all changed files with stats
gh pr diff 123 --repo "$OWNER/$REPO" --stat

# Full diff
gh pr diff 123 --repo "$OWNER/$REPO"

# Diff for specific file
gh pr diff 123 --repo "$OWNER/$REPO" -- src/app.py
### Add Inline Comments

bash
# Comment on a specific line (gh CLI)
gh pr comment 123 --repo "$OWNER/$REPO" \
  --body "Consider extracting this logic into a helper function." \
  --line 42 --path src/app.py

# Approve a PR
gh pr review 123 --approve --repo "$OWNER/$REPO" \
  --body "LGTM - good work!"

# Request changes
gh pr review 123 --request-changes --repo "$OWNER/$REPO" \
  --body "This function needs error handling before we can merge."

# Comment without approving or requesting changes
gh pr review 123 --comment --repo "$OWNER/$REPO" \
  --body "Nice approach. One minor suggestion:"
### Using the REST API for Comments

bash
# Create a review comment on a specific line
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.github.com/repos/$OWNER/$REPO/pulls/123/comments" \
  -d '{
    "body": "Consider adding input validation here.",
    "commit_id": "abc123",
    "path": "src/app.py",
    "line": 42,
    "side": "RIGHT"
  }'

# Get existing review comments
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/$OWNER/$REPO/pulls/123/comments"
---

## Review Checklist

Use this checklist when reviewing code:

### Correctness
- [ ] Does the code do what the PR description claims?
- [ ] Are edge cases handled properly?
- [ ] Are there any obvious bugs or logic errors?
- [ ] Are API responses or return values handled correctly?

### Security
- [ ] Are secrets or credentials hardcoded?
- [ ] Is user input properly sanitized/validated?
- [ ] Are database queries parameterized (no SQL injection)?
- [ ] Are file paths validated before use?

### Code Quality
- [ ] Are functions and variables named descriptively?
- [ ] Is the code DRY (no excessive duplication)?
- [ ] Are complex functions broken into smaller pieces?
- [ ] Is there appropriate error handling?

### Testing
- [ ] Does the PR include tests for new functionality?
- [ ] Are edge cases covered by tests?
- [ ] Do existing tests still pass?

### Performance
- [ ] Are there any N+1 query patterns?
- [ ] Are large datasets processed efficiently?
- [ ] Are expensive operations cached where appropriate?