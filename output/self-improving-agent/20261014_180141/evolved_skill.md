---
category: software-development
description: Captures learnings, errors, and corrections to enable continuous improvement.
name: self-improving-agent
---

# Self-Improving Agent

Captures learnings, errors, and corrections to enable continuous improvement.

## When to Use

Trigger learning capture when any of these situations occur:

| Scenario | Example |
|----------|---------|
| Command or operation fails | `sudo` permission denied, syntax errors, missing dependencies |
| User provides correction | "No, that's not right", "Actually it should be...", "The correct syntax is..." |
| User requests unavailable capability | "Can you do X?" → feature not implemented or unknown |
| External tool or API failure | HTTP 4xx/5xx errors, timeout, rate limiting, deprecated endpoints |
| Knowledge gaps identified | Unsure about a language feature, library version, or best practice |
| Better approach discovered | Faster algorithm found, more idiomatic syntax learned, tool preference changed |

## Learning Capture Process

### 1. Detect
- Identify what failed or what could be improved
- Note the exact error message, command, or context

### 2. Record
- Create a structured memory entry (format below)
- Include all relevant context for future retrieval

### 3. Apply
- Determine how to avoid the same mistake
- Update approach for current and future tasks

### 4. Acknowledge
- Briefly inform the user what was learned
- Confirm the correction if applicable

## Memory Entry Format

markdown
# Learning: [Short descriptive title]

**Date**: YYYY-MM-DD
**Category**: [error | correction | knowledge | tool | process]

**Context**:
What were you trying to do? What was the situation?

**What happened**:
The specific error, mistake, or knowledge gap encountered.

**Correction**:
How to do it correctly, or what approach to use instead.

**Applied to**:
List of file paths, commands, or task types this applies to.

**Prevention**:
How to avoid this issue in the future (if applicable).
## Common Scenarios

### Command Fails with Permission Error

Error: "Permission denied" when running `docker build`

Learning: Docker commands require appropriate permissions on the socket or daemon.

Correction:
- Ensure user is in the `docker` group: `sudo usermod -aG docker $USER`
- Or use: `sudo docker build ...`
- Check if Docker daemon is running: `systemctl status docker`

Applied to: All Docker operations
### User Correction on Output

User: "That's not right. The function should return a list, not a tuple."

Learning: Misunderstood return type requirements.

Correction:
- Always confirm return type expectations with user
- When uncertain, explicitly state assumptions

Applied to: Function definitions, API responses, data transformations
### External API Failure

Error: HTTP 404 from API endpoint /users/v1/profile

Learning: API version or endpoint structure has changed.

Correction:
- Check API documentation for current endpoint
- Look for migration guides or changelog
- Consider caching known-good responses

Applied to: All external API integrations
### Better Approach Discovered

Discovery: `fd` is 3x faster than `find` for common searches

Learning: Task-specific tools often outperform general-purpose alternatives.

Correction:
- Use `fd` for file finding tasks
- Prefer `rg` over `grep`, `fzf` over tab-completion for fuzzy search

Applied to: File operations, search tasks, text processing
## Before Important Tasks

1. **Review recent learnings**: Check memory entries relevant to the current task domain
2. **Scan for applicable corrections**: Look for patterns that match the upcoming work
3. **Verify assumptions**: If a past error involved similar technology, double-check your approach
4. **Proactive flagging**: If uncertain about something that caused problems before, ask the user

## Principles

- **No shame in errors**: Learning is expected; document without judgment
- **Specific over general**: Include exact commands, error messages, and file paths
- **Actionable corrections**: Every learning must lead to a concrete change in behavior
- **User transparency**: When appropriate, share what was learned to build trust

**Goal**: Never make the same mistake twice, and continuously expand capabilities.