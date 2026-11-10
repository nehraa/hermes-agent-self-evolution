---
category: software-development
description: Captures learnings, errors, and corrections to enable continuous improvement.
name: self-improving-agent
---

# Self-Improving Agent

Captures learnings, errors, and corrections to enable continuous improvement.

## When to Use

Trigger self-improvement when any of these occur:

1. **Command failures** — A shell command, script, or tool exits with an unexpected error
2. **User corrections** — The user explicitly states something is wrong or different ("No, that's wrong...", "Actually it should be...", "Try a different approach...")
3. **Missing capabilities** — User requests functionality that doesn't exist in your current toolset
4. **API/tool errors** — External services return unexpected status codes, timeouts, or malformed responses
5. **Outdated knowledge** — You recognize that your training data or assumptions may be incorrect
6. **Better solutions discovered** — You find a more efficient, reliable, or maintainable approach during a task

## Process

Follow these four steps for every learning:

| Step | Action | Description |
|------|--------|-------------|
| **1. Identify** | What happened? | Determine the root cause, not just the symptom |
| **2. Document** | Create a memory entry | Record the context, error, and correction |
| **3. Apply** | How will you improve? | Define concrete changes to your approach |
| **4. Communicate** | Share with user | Briefly acknowledge what you learned and what you'll do differently |

## Examples

### Command fails with permission error

- **Situation**: ` Operation not permitted` or `sudo: command not found`
- **Learning**: The operation requires elevated privileges
- **Application**: Prepend commands with `sudo` or explicitly request permission before attempting

### User rejects your approach

- **Situation**: User says "That's not right" or provides an alternative specification
- **Learning**: Your understanding of the requirement was incorrect
- **Application**: Confirm requirements before executing; update your model of the user's preferences

### External API returns an error

- **Situation**: API returns 404, 500, timeout, or rate limit
- **Learning**: The endpoint, authentication, or service state has changed
- **Application**: Check current API documentation, use an alternative endpoint, or inform the user of the limitation

### Discovering a better solution mid-task

- **Situation**: While solving X, you find a simpler pattern or more efficient command
- **Learning**: Your initial approach was suboptimal
- **Application**: Adopt the better approach immediately and note it for future reference

### Syntax or command remembered incorrectly

- **Situation**: Command fails because you used wrong flags or syntax
- **Learning**: Your recall of this command was inaccurate
- **Application**: Use `man` or `--help` before executing unfamiliar commands

## Memory Entry Format

Create a structured entry for each learning:

markdown
# Learning: [Brief descriptive title]

**Timestamp**: YYYY-MM-DD HH:MM
**Situation**: What triggered this learning?
**Error/Failure**: What went wrong?
**Root Cause**: Why did it fail?
**Correction**: What is the correct approach?
**Application**: How will you apply this going forward?
**Tags**: [relevant tags for retrieval]
Store these entries in a persistent memory system (e.g., a `~/.agent-learnings/` directory or notes file).

## Before Major Tasks

Before starting significant work:

1. **Scan recent learnings** — Check your memory entries for relevant past mistakes
2. **Identify blockers** — Note any patterns to avoid or prerequisites to handle
3. **Adjust strategy** — Apply lessons to your approach before execution begins
4. **Confirm scope** — Verify with the user if your approach aligns with their expectations

## Principles

- **Never repeat the same mistake** — If something failed before, acknowledge it and do it differently
- **Be specific in documentation** — "Permission denied on /var/log" is better than "Commands sometimes fail"
- **Update proactively** — When you realize mid-task that you were wrong, stop and correct before continuing
- **Learn from user corrections** — Treat every correction as a signal to update your model

---

**Goal**: Each interaction makes you more effective. Accumulate knowledge systematically and apply it consistently.