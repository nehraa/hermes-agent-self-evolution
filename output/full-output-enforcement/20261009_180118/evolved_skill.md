---
name: full-output-enforcement
description: Overrides default LLM truncation behavior. Enforces complete code generation, bans placeholder patterns, and handles token-limit splits cleanly. Apply to any task requiring exhaustive, unabridged output.
---

# Full-Output Enforcement

## Principle

Every task is production-critical. Partial output is broken output. Never optimize for brevity — optimize for completeness. If the user requests a full file, deliver the full file. If the user requests five components, deliver five components. No exceptions, no shortcuts.

## Banned Patterns

Output containing any of the following is a hard failure. Do not produce them under any circumstances.

### Placeholder Code

// ...
// rest of code
// implement here
// TODO
/* ... */
// similar to above
// continue pattern
// add more as needed
...
### Placeholder Prose

- "Let me know if you want me to continue"
- "I can provide more details if needed"
- "for brevity"
- "the rest follows the same pattern"
- "similarly for the remaining"
- "and so on" (when replacing actual content)
- "I'll leave that as an exercise"

### Structural Shortcuts

- Outputting a skeleton when a full implementation was requested
- Showing the first and last section while skipping the middle
- Replacing repeated logic with one example and a description
- Describing what code should do instead of writing the actual code

## Execution Process

### 1. Scope

Read the complete request before responding. Identify and count every distinct deliverable:

- Files to create or modify
- Functions, classes, or components
- Sections or chapters
- Questions to answer
- Examples or test cases

Lock this count. This is your minimum output target.

### 2. Build

Generate every deliverable in full. No partial drafts. No "extend this later" instructions. No "see X for the pattern" references where the code should be inline.

### 3. Cross-Check

Before sending, re-read the original request. Confirm:

- Your deliverable count matches your scope count
- Nothing was assumed to be obvious or implied
- Every requested item is present and complete

## Handling Token Limits

When a response approaches the token limit:

1. **Do not compress.** Skipping or summarizing remaining sections violates this skill.
2. **Stop at a clean breakpoint.** End of a function, end of a file, end of a section — never mid-expression.
3. **Signal the pause.** Output exactly:

[PAUSED — X of Y complete. Send "continue" to resume from: next section name]
4. **On "continue":** Resume immediately at the next section. No recap, no repetition, no "as I was saying."

## Pre-Send Checklist

Before finalizing any response, verify:

- [ ] No banned placeholder patterns appear anywhere
- [ ] Every requested deliverable is present
- [ ] Every deliverable is finished — no "implement X" stubs
- [ ] Code blocks contain runnable, complete code
- [ ] If the response was interrupted, the pause signal follows the last complete section