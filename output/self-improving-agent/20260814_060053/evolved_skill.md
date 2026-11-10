---
category: software-development
description: Captures learnings, errors, and corrections to enable continuous improvement.
name: self-improving-agent
---

# Self-Improving Agent

Captures learnings, errors, and corrections to enable continuous improvement.

## When to Use

Use this skill when any of the following occur:

- A command fails with an unexpected error (permission denied, not found, timeout)
- A user explicitly corrects you ("No, that's wrong", "Actually it should be...")
- A user requests functionality you cannot perform
- An external API, tool, or service fails or returns an unexpected response
- You discover your knowledge or approach was incorrect
- You find a better/more efficient method for a task you've done before

## Process

Follow these steps when a learning opportunity arises:

1. **Identify the trigger** — What happened? What was the expected vs. actual outcome?
2. **Extract the lesson** — What is the core learning? What should you do differently?
3. **Document it** — Record the context, error, and correction for future reference
4. **Acknowledge to user** — Briefly communicate what you learned (when appropriate)
5. **Apply going forward** — Use the lesson to improve your next action

## Examples

### Command Fails with Permission Error

Error: "Permission denied" when running `docker build`
Learning: Docker commands require elevated permissions in this environment
Application: Prefix docker commands with `sudo` or ask user to grant permissions
### User Provides Correction

User: "No, that's wrong. The API endpoint is `/api/v2/users`, not `/api/users`"
Learning: I had outdated endpoint information for this API
Application: Use `/api/v2/users` for this service; verify API versions before use
### External Service Failure

Error: HTTP 404 from external API
Learning: The endpoint has moved or been deprecated
Application: Check API documentation or try alternative endpoints before assuming success
### Discovered Better Approach

Previous approach: Run commands sequentially
Discovery: Commands X and Y can run in parallel safely
Learning: Parallel execution reduces total time without increasing risk
Application: Check for parallelization opportunities in similar future tasks
## Memory Entry Format

Document learnings consistently using this structure:

markdown
# Learning: [Brief, descriptive title]

**Date**: YYYY-MM-DD
**Context**: What were you trying to accomplish?
**What went wrong**: The error, mistake, or failure
**Correction**: What should have been done or will be done
**Application**: When and how to apply this going forward
### Example Entry

markdown
# Learning: Terraform requires explicit state file for remote backends

**Date**: 2024-01-15
**Context**: Running `terraform plan` in a new workspace
**What went wrong**: State file not found; resources needed to be recreated
**Correction**: Always specify `-backend-config` or use workspace-specific configuration
**Application**: When working with Terraform in any environment, verify state backend is configured before apply
## Before Important Tasks

Before starting significant or complex tasks:

1. Review any relevant prior learnings
2. Check for documented mistakes to avoid
3. Apply lessons from previous similar tasks
4. Note any assumptions that should be verified

## Principles

- **Be specific** — Record concrete details, not vague observations
- **Be actionable** — Every learning should tell you what to do differently
- **Be honest** — Acknowledge errors without defensiveness
- **Be consistent** — Use the same format every time for easy searching

---

**Goal**: Build a cumulative knowledge base that makes each interaction better than the last.