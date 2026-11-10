---
category: software-development
description: Captures learnings, errors, and corrections to enable continuous improvement.
name: self-improving-agent
---

# Self-Improving Agent

Captures learnings, errors, and corrections to enable continuous improvement.

## When to Use

Use when:
1. A command or operation fails unexpectedly
2. User corrects you ("No, that's wrong...", "Actually...")
3. User requests a capability that doesn't exist
4. An external API or tool fails
5. You realize your knowledge is outdated or incorrect
6. A better approach is discovered for a recurring task

## Process

1. **Identify the learning**: What happened? What went wrong?
2. **Document it**: Create a memory entry or note
3. **Apply the learning**: How will you do better next time?
4. **Share with user**: Let them know what you learned

## Examples

### When a command fails
- **Error**: Command failed with permission denied
- **Learning**: Need elevated permissions for this operation
- **Application**: Use `--sudo` or ask user for permission first

### When user corrects you
- **User**: "No, that's wrong. It should be..."
- **Learning**: I made an error in my reasoning
- **Application**: Acknowledge the correction and adjust approach

### When a tool fails
- **Error**: External API returned 404
- **Learning**: The endpoint has changed or no longer exists
- **Application**: Check documentation or use alternative method

### When discovering a better approach
- **Discovery**: Found a more efficient way to do X
- **Learning**: The previous method was suboptimal
- **Application**: Use the new method for future tasks

## Memory Entry Format

When documenting learnings, use this format:

```
# Learning: [Title]

**Context**: [What happened]
**Error/Failure**: [What went wrong]
**Correction**: [How to fix it]
**Application**: [How to apply this learning]
```

## Before Major Tasks

Before starting important tasks:
1. Review recent learnings
2. Check if any previous mistakes should be avoided
3. Apply lessons learned to current approach

---

**Goal**: Continuous improvement through learning and adaptation.
