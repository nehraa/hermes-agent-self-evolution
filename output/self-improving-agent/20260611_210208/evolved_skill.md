---
category: software-development
description: Captures learnings, errors, and corrections to enable continuous improvement.
name: self-improving-agent
---

# Self-Improving Agent

Captures learnings, errors, and corrections to enable continuous improvement.

## When to Use

Use this skill when:

1. **Command fails** — A terminal command, script, or operation returns an error or unexpected result
2. **User corrects you** — Explicit feedback like "No, that's wrong...", "Actually...", or "It should be done like this..."
3. **User requests a missing capability** — A feature, tool, or approach you don't have
4. **External service fails** — API returns an error, service is down, or credentials fail
5. **You discover outdated knowledge** — Realize your understanding of a tool, language, or framework is incorrect
6. **Better approach found** — Learn a more efficient or correct method for a recurring task

## How to Apply This Skill

### Step 1: Identify What Happened

- What command or action triggered the issue?
- What was the expected outcome vs. actual result?
- Is this a new problem or recurring pattern?

### Step 2: Determine the Root Cause

- Permission or access issue?
- Incorrect syntax, command, or approach?
- Missing dependency, tool, or configuration?
- Changed API, deprecated feature, or version mismatch?

### Step 3: Document the Learning

Create a memory entry (see format below) to preserve the insight.

### Step 4: Apply the Correction

- Use the correct command, syntax, or approach immediately
- Adjust your approach for similar future tasks
- If you can't fix it now, note what to do when you can

### Step 5: Communicate to the User

Briefly acknowledge what went wrong and what you're doing differently.

## Examples

### Command Fails with Permission Error

Error: "Permission denied" when running npm install -g
Learning: Global installs require elevated permissions on this system
Correction: Use `sudo npm install -g` or configure npm's prefix to a user-writable directory
Application: Always check if a command needs sudo before running; ask user for permission
### User Provides a Correction

User: "No, that's wrong. The database connection string should use port 5433, not 5432."
Learning: This project's database uses a non-standard port
Correction: Use port 5433 for all database connections in this project
Application: Check project-specific config files for port overrides before assuming defaults
### External API Returns an Error

Error: API call returns 404 for /api/users endpoint
Learning: The endpoint path has changed in the latest API version
Correction: Update to /api/v2/users or check API changelog
Application: Always verify current API version and endpoints before making external calls
### Discovering a Better Approach

Previous: Used a for-loop with nested conditionals
Better approach: Used array.filter().map() for cleaner, more performant code
Learning: Modern JavaScript array methods are more readable and efficient than manual loops
Application: Prefer built-in array methods over manual iteration where appropriate
## Memory Entry Format

Use this format when documenting learnings:

markdown
# Learning: [Brief Title]

**Date**: YYYY-MM-DD
**Context**: [What were you trying to accomplish?]
**Error/Failure**: [What went wrong or what was incorrect?]
**Root Cause**: [Why did it fail?]
**Correction**: [How to fix or do it correctly]
**Application**: [When and how to apply this going forward]
**Tags**: [optional tags like #bash, #python, #api, #docker]
## Before Starting Important Tasks

1. **Check for relevant learnings** — Search memory for similar past issues
2. **Review project-specific notes** — Look for port numbers, non-standard configs, known workarounds
3. **Verify tool versions** — Confirm you're using the correct version of frameworks, CLIs, and dependencies
4. **Ask clarifying questions** — If unsure about project conventions, ask before assuming

---

**Goal**: Avoid repeating mistakes, incorporate corrections immediately, and build a growing knowledge base that makes each task more efficient than the last.