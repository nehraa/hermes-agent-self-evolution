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

Review code changes locally before pushing, or review open pull requests on GitHub. Local reviews use pure `git`. PR-level interactions use either `gh` CLI or GitHub REST API.

## Prerequisites

- Authenticated with GitHub (see `github-auth` skill)
- Inside a git repository

## Setup

Run this block to initialize authentication and repo context for PR interactions:

bash
# Determine auth method
if command -v gh &>/dev/null && gh auth status &>/dev/null; then
  AUTH="gh"
else
  AUTH="git"
  # Fallback token sources
  if [ -z "$GITHUB_TOKEN" ]; then
    if [ -f ~/.hermes/.env ] && grep -q "^GITHUB_TOKEN=" ~/.hermes/.env; then
      GITHUB_TOKEN=$(grep "^GITHUB_TOKEN=" ~/.hermes/.env | head -1 | cut -d= -f2 | tr -d '\n\r')
    elif [ -f ~/.git-credentials ] && grep -q "github.com" ~/.git-credentials; then
      GITHUB_TOKEN=$(grep "github.com" ~/.git-credentials | head -1 | sed 's|https://[^:]*:\([^@]*\)@.*|\1|')
    fi
  fi
fi

# Extract owner/repo from origin remote
REMOTE_URL=$(git remote get-url origin 2>/dev/null || git remote get-url origin)
OWNER_REPO=$(echo "$REMOTE_URL" | sed -E 's|.*github\.com[:/]||; s|\.git$||')
OWNER=$(echo "$OWNER_REPO" | cut -d/ -f1)
REPO=$(echo "$OWNER_REPO" | cut -d/ -f2)
---

## 1. Reviewing Local Changes (Pre-Push)

Pure `git` — works offline, no API required.

### Get the Diff

bash
# Staged changes only (what would be committed)
git diff --staged

# All changes vs main branch (equivalent to what a PR would contain)
git diff main...HEAD

# File names only
git diff main...HEAD --name-only

# Stat summary with insertions/deletions per file
git diff main...HEAD --stat

# Diff for a specific file
git diff main...HEAD -- path/to/file.ext
### Review Workflow

**Step 1: Get the big picture**

bash
git diff main...HEAD --stat
git log main..HEAD --oneline
**Step 2: Review file by file**

For each changed file, use `read_file` to understand the full context, then use the diff to see what changed:

bash
git diff main...HEAD -- path/to/file.ext
**Step 3: Check for common issues**

bash
# Debug statements and temporary code left behind
git diff main...HEAD | grep -n "print\|console\.log\|TODO\|FIXME\|HACK\|XXX\|debugger"

# Large files accidentally staged
git diff main...HEAD --stat | sort -t'|' -k2 -rn | head -10

# Hardcoded secrets or credentials
git diff main...HEAD | grep -in "password\|secret\|api_key\|token.*=\|private_key"

# Merge conflict markers
git diff main...HEAD | grep -n "^<<<<\|^====\|^>>>>"
---

## 2. Reviewing Open Pull Requests

### Using `gh` CLI

bash
# List open PRs
gh pr list

# View PR details and changes
gh pr view <PR_NUMBER> --json body,title,files,additions,deletions

# Checkout PR locally for deeper review
gh pr checkout <PR_NUMBER>

# Add an inline comment on a specific line
gh pr comment <PR_NUMBER> --body "Consider extracting this logic into a helper function."
### Using GitHub REST API

bash
# Set base URL
API_BASE="https://api.github.com/repos/$OWNER/$REPO"

# List open PRs
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "$API_BASE/pulls?state=open" | jq '.[] | {number, title, state}'

# Get PR details
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "$API_BASE/pulls/<PR_NUMBER>" | jq '{title, body, additions, deletions, changed_files}'

# Get diff of a PR
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "$API_BASE/pulls/<PR_NUMBER>" --silent | jq -r '.diff_url' | xargs curl -s | head -500

# List changed files
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "$API_BASE/pulls/<PR_NUMBER>/files" | jq '.[] | {filename, additions, deletions, patch}'
---

## 3. Writing Review Comments

### On a Specific Line (gh)

bash
# Comment on a line in the PR diff
gh api repos/$OWNER/$REPO/pulls/<PR_NUMBER>/comments \
  -f body="This function is doing too much. Consider splitting it." \
  -f commit_id=$(gh pr view <PR_NUMBER> --json headRefOid -q '.headRefOid') \
  -f path=src/auth/login.py \
  -f line=42 \
  -f side=RIGHT
### On a PR Overall

bash
# Post a general review comment
gh pr review <PR_NUMBER> --body "Good progress, but please address:
- Error handling in auth.js
- Add tests for the new endpoint
- Update CHANGELOG.md"
---

## 4. Common Review Checks

| Check | Command |
|-------|---------|
| Files changed | `git diff main...HEAD --name-only` |
| Lines added/removed | `git diff main...HEAD --shortstat` |
| Search for TODOs | `git diff main...HEAD | grep "TODO"` |
| Find secrets | `git diff main...HEAD | grep -iE "password|secret|key|token"` |
| Check whitespace | `git diff main...HEAD --check` |
| Review commits | `git log main..HEAD --oneline` |

---

## 5. Configuration

For faster reviews, configure git aliases:

bash
git config --global alias.review 'diff main...HEAD --stat'
git config --global alias.review-files 'diff main...HEAD --name-only'