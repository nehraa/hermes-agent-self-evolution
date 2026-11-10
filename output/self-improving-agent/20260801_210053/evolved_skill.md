---
category: software-development
description: Captures learnings, errors, and corrections to enable continuous improvement.
name: self-improving-agent
---

# Self-Improving Agent

Captures learnings, errors, and corrections to enable continuous improvement.

## When to Use

Activate this skill when any of the following occurs:

1. **Command failures** — A shell command, script, or tool exits with an unexpected error
2. **User corrections** — User explicitly states something is wrong ("No", "Actually", "Try again")
3. **Missing capabilities** — User requests functionality that doesn't exist or isn't available
4. **API/tool failures** — External services return errors or unexpected responses
5. **Knowledge gaps** — You recognize your information may be outdated or incorrect
6. **Better solutions discovered** — You find a more efficient approach for a recurring task
7. **Permission issues** — Operations fail due to access restrictions
8. **Configuration errors** — Misconfigured files, environment variables, or dependencies

## Process

### 1. Detect

Recognize that something went wrong or that a better approach exists.

### 2. Analyze

- What was the expected outcome?
- What actually happened?
- What is the root cause?

### 3. Document

Record the learning in your memory with context and application.

### 4. Apply

Adjust your approach immediately and for future similar tasks.

### 5. Communicate

Briefly inform the user of what you learned and how you'll proceed.

## Examples

### Command Fails with Permission Error

Error: mkdir: cannot create directory '/opt/app': Permission denied
Learning: Operation requires elevated privileges
Application: Prepend commands with `sudo` or request permission before attempting
### User Provides Correction

User: "No, that's not right. The config file goes in /etc/nginx/sites-available/, not sites-enabled/"
Learning: Nginx config files go in sites-available and get symlinked to sites-enabled
Application: Follow proper Nginx conventions for future config tasks
### External API Returns Error

Error: GET https://api.example.com/v1/users - 404 Not Found
Learning: Endpoint structure has changed or resource was removed
Application: Check API documentation for current endpoint paths before retrying
### Discovering Better Approach

Previous approach: grep -r "pattern" ./directory (slow on large repos)
Better approach: rg "pattern" ./directory (ripgrep, much faster)
Learning: Use ripgrep instead of grep for improved performance
Application: Default to ripgrep for all text searching tasks
## Memory Entry Format

Use this structured format when documenting learnings:

markdown
# Learning: [Concise Title]

**Date**: YYYY-MM-DD
**Category**: [error | correction | optimization | missing-capability | knowledge-gap]

## Context
What triggered this learning? Include the command, code snippet, or situation.

## What Happened
Actual result or error message received.

## Root Cause
Why did this happen? (optional, if identifiable)

## Correction / Solution
How to fix or avoid this issue.

## Application
Specific situations or tasks where this learning applies. Include code snippets or commands when relevant.

## Priority
[ ] Low — edge case, unlikely to recur
[x] Medium — useful for similar tasks
[ ] High — critical for common workflows
## Before Important Tasks

Before starting significant work:

1. **Scan recent learnings** — Check your memory for relevant past mistakes
2. **Identify blockers** — Note any known permission or dependency requirements
3. **Apply patterns** — Incorporate lessons from similar previous tasks
4. **Validate assumptions** — Confirm environment and context match expectations

## Best Practices

- **Document immediately** — Capture learnings before moving to the next task
- **Be specific** — Include exact error messages, commands, and file paths
- **Prioritize high-impact learnings** — Focus on corrections that prevent recurring failures
- **Keep entries actionable** — Write so future self can immediately apply the fix
- **Review periodically** — Check accumulated learnings before starting new projects

**Goal**: Build a continuously improving system by learning from every interaction, error, and correction.