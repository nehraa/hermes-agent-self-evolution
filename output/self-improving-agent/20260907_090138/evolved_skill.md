---
category: software-development
description: Captures learnings, errors, and corrections to enable continuous improvement.
name: self-improving-agent
---

# Self-Improving Agent

Captures learnings, errors, and corrections to enable continuous improvement.

## When to Use

Trigger this skill when you encounter:

| Situation | Trigger Phrases | Example |
|-----------|-----------------|---------|
| **Command fails** | Exit code non-zero, permission denied, command not found | `chmod` fails on protected directory |
| **User correction** | "No, that's wrong", "Actually...", "It should be..." | User specifies a different flag than you used |
| **Missing capability** | "Can you...", "I need to...", "There's no way to..." | User requests a feature you can't perform |
| **External failure** | API error, timeout, connection refused, 404 | `curl` returns 503 from an endpoint |
| **Outdated knowledge** | "That's deprecated", "The syntax changed", "That doesn't work anymore" | User corrects a command syntax |
| **Better approach discovered** | None (self-initiated) | Finding a one-liner that replaces a 10-line script |

## Process

┌─────────────────────────────────────────────────────────┐
│  1. DETECT  →  What happened? Is this a pattern?        │
├─────────────────────────────────────────────────────────┤
│  2. CAPTURE →  Log the error, context, and correction   │
├─────────────────────────────────────────────────────────┤
│  3. APPLY   →  How will you act differently next time?  │
├─────────────────────────────────────────────────────────┤
│  4. CONFIRM →  Inform the user: what you learned       │
└─────────────────────────────────────────────────────────┘
### Step Details

1. **Detect**
   - Recognize the failure point or improvement opportunity
   - Ask: "Is this a one-time error or a pattern I should remember?"

2. **Capture**
   - Extract: error message, context, what you tried, what worked
   - Discard noise—remember the actionable insight, not the entire stack trace

3. **Apply**
   - State the fix as a concrete rule: "Next time, do X instead of Y"
   - If no fix exists yet, note what to investigate

4. **Confirm**
   - Brief acknowledgment: "Got it—I'll use `--force` flag in future deletions"
   - Don't over-explain; just confirm the learning lands

## Examples

### Command Fails with Permission Error

Error:   "Operation not permitted" or "Permission denied"
Cause:   Attempted operation on protected resource
Learning: Need elevated privileges for this action
Action:  Check if `--sudo` applies, or explicitly ask user for permission
### User Provides Correct Input

Error:   Used wrong parameter value or approach
Cause:   Misunderstood requirements or made incorrect assumption
Learning: User knows the specific context better than I do
Action:  When uncertain, ask for confirmation before executing
### External API Returns Error

Error:   HTTP 404, 500, timeout, or connection refused
Cause:   Endpoint changed, service down, or network issue
Learning: Verify API availability before relying on it
Action:  Check current documentation; have fallback method ready
### Discovered More Efficient Method

Error:   None—but previous approach was suboptimal
Cause:   Found faster, cleaner, or more maintainable solution
Learning: Current approach can be improved
Action:  Adopt new method; note why it's better for future reference
## Memory Entry Format

Use this structure for persistent learnings:

markdown
# Learning: [Short descriptive title]

**Date**: YYYY-MM-DD
**Situation**: [What you were trying to do]
**What went wrong**: [Error, misstep, or suboptimal approach]
**What fixed it**: [The correction or improvement]
**Rule going forward**: [Specific action to take in similar situations]

Tags: #api #bash #permissions #etc
### Example Memory Entry

markdown
# Learning: Docker commands need `--sudo` on this system

**Date**: 2025-01-15
**Situation**: Attempting to list containers with `docker ps`
**What went wrong**: "permission denied while trying to connect to Docker daemon"
**What fixed it**: Running `sudo docker ps` instead
**Rule going forward**: Prefix all Docker commands with `sudo` unless user confirms otherwise

Tags: #docker #permissions
## Before Starting Major Tasks

bash
1. Recall recent failures:    → "Any past errors in this domain?"
2. Check relevant learnings:  → Apply previous corrections to current approach
3. Validate assumptions:      → Confirm environment/setup matches what you remember
4. Flag uncertainties:        → Note anything that might need updating
### Pre-Task Checklist

- [ ] Reviewed learnings related to this task type
- [ ] Verified environment-specific rules apply (e.g., `sudo` needed)
- [ ] Confirmed API endpoints/services are current
- [ ] Noted any uncertain information to validate during task

## Prioritization

Not everything needs to be remembered. Prioritize:

| Always Remember | Sometimes Remember | Usually Discard |
|-----------------|-------------------|-----------------|
| Environment-specific quirks | One-time API quirks | Generic error messages |
| User preferences and workflow | Rare edge cases | Stack traces without context |
| Permanent corrections to your knowledge |  | Temporary network issues |

## Key Principle

**Learn from mistakes once, not repeatedly.**

Every error you encounter is an opportunity to prevent the same error in the future. The goal is not to remember everything—it's to remember what makes your next response faster, more accurate, and more aligned with the user's expectations.