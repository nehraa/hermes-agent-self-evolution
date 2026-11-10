---
name: full-output-enforcement
description: Overrides default LLM truncation behavior. Enforces complete code generation, bans placeholder patterns, and handles token-limit splits cleanly. Apply to any task requiring exhaustive, unabridged output.
---

# Full-Output Enforcement

## Purpose

Every task is production-critical. A partial output is a broken output. This skill enforces complete, unabridged generation by default—overriding the LLM's tendency to truncate, summarize, or use placeholder patterns. Apply whenever exhaustive output is required.

---

## Banned Patterns

These patterns are hard failures. Never produce them under any circumstances.

### Code Placeholders

| Banned Pattern | Examples |
|----------------|----------|
| Ellipsis omission | `...`, `// ...`, `/* ... */` |
| Descriptive skip | `// rest of code`, `// implement here`, `// similar to above` |
| Task deferral | `// TODO`, `// add more as needed`, `// continue pattern` |

### Prose Truncation

- "Let me know if you want me to continue"
- "I can provide more details if needed"
- "for brevity", "the rest follows the same pattern"
- "similarly for the remaining", "and so on"
- "I'll leave that as an exercise"

### Structural Shortcuts

- Outputting a skeleton when a full implementation was requested
- Showing only first and last sections while skipping the middle
- Replacing repeated logic with one example and a description
- Describing what code should do instead of writing it

---

## Execution Process

### Step 1: Scope the Request

Before writing anything:
1. Read the request completely
2. Identify the exact number of deliverables (files, functions, components, sections, answers)
3. Lock that count as your baseline

### Step 2: Generate Completely

- Produce every deliverable in full
- No partial drafts, no "extend this later" suggestions
- Write at full quality throughout

### Step 3: Cross-Check Before Output

Re-read the original request and verify:
- Your deliverable count matches the scope count
- No requested item is missing or truncated
- All code is complete and runnable

---

## Handling Token Limits

If you approach the token limit mid-output:

1. **Do not** compress remaining sections
2. **Do not** skip to a conclusion
3. **Do** stop at a clean breakpoint (end of function, file, or section)
4. **Do** output the pause signal below, then stop

[PAUSED — X of Y complete. Send "continue" to resume from: next section name]
On "continue": resume exactly where you stopped. No recap, no repetition.

---

## Pre-Output Checklist

Before sending any response, verify all of the following:

- [ ] Zero banned patterns appear anywhere in the output
- [ ] Every requested deliverable is present and finished
- [ ] All code blocks contain complete, runnable code (no ellipses, no TODO placeholders)
- [ ] All prose is complete (no "the rest follows the same pattern" or similar truncations)
- [ ] The deliverable count matches the original scope

If any item fails the check, correct it before responding.