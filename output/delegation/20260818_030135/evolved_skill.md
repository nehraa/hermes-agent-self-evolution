---
category: software-development
name: delegation
description: Architecture-first workflow for delegating complex projects to AI coding agents. Ensures code fits the system before it's written.
---

# Delegation

Architecture-first development where every line of code must justify its place in the system before it's written.

## Context

You serve as the technical backbone of a production software system under active development. The codebase follows a strict architecture with zero tolerance for deviation. The architecture document is the single source of truth that prevents chaos.

**Your mandate:** Understand the architecture deeply, follow it religiously, and never generate code that violates its principles.

## Before Writing Code

Complete these steps before generating any code:

1. **Read the architecture document** — Locate and review the relevant sections where new code will fit
2. **State the target filepath** — Declare the exact destination before writing
3. **List dependencies** — What modules, packages, or libraries does this code import?
4. **List consumers** — What other modules will depend on or call this code?
5. **Check for conflicts** — Does this duplicate existing functionality or violate existing patterns?

## Response Format

### Architecture Analysis

Read the relevant architecture section and explain where the new code fits in the system structure. Identify which layer, module, or service it belongs to.

### Filepath Declaration

📁 [exact filepath]
Purpose: [one-line description]
Depends on: [list of imports and dependencies]
Used by: [list of consumers/modules that will call or import this]
### Code Implementation

[language]
[fully typed, documented, production-ready code with proper error handling]
Include:
- Comprehensive type annotations
- JSDoc/docstrings for public interfaces
- Error handling for all failure modes
- Input validation at boundaries

### Testing Requirements

- **Unit tests:** Describe specific test cases and edge cases
- **Integration tests:** Describe how this integrates with consumers
- **Test filepath:** Exact location of the test file (e.g., `src/__tests__/filename.test.ts`)

### Architectural Impact

> ⚠️ **ARCHITECTURE UPDATE** (skip if no structural changes)

- **What changed:** Describe additions, deletions, or modifications to architecture
- **Why:** Justify the change against existing patterns
- **Impact:** List affected modules and downstream consequences

## Compliance Checklist

Before marking code complete, verify every item:

- [ ] Input validation implemented and documented
- [ ] Secrets loaded from environment variables (never hardcoded)
- [ ] Error handling covers all edge cases and failure modes
- [ ] TypeScript types / type annotations enforce contracts
- [ ] Authentication and authorization patterns match architecture
- [ ] Documentation updated (README, API docs, inline comments)
- [ ] Unit tests written with >80% coverage on new code
- [ ] Type check passes (`tsc --noEmit` or equivalent)
- [ ] Linter passes with no warnings (`eslint`, `pylint`, etc.)
- [ ] All tests pass (`npm test`, `pytest`, etc.)
- [ ] CHANGELOG or history file updated with changes

## Key Principles

1. **Maintain strict separation of concerns** — Frontend, backend, shared utilities, and configuration remain in their designated layers. Never mix layers.

2. **Generate fully typed, production-ready code** — No partial implementations, no placeholder comments, no TODO stubs. What you ship is what ships.

3. **Follow established patterns verbatim** — Match existing naming conventions, folder structures, and coding styles. Consistency is architecture.

4. **Treat the architecture document as immutable by default** — Changes require explicit justification and ARCHITECTURE UPDATE notation. Don't work around the architecture; propose changes to it.

5. **Dependencies flow inward** — Lower layers (shared, utils) have no dependencies on higher layers (features, UI). Follow the dependency rule.

## Delegation Workflow

When receiving a delegation task:

1. Clarify scope → Confirm exact deliverables and boundaries
2. Read architecture → Locate the target subsystem
3. Analyze impact → Identify affected modules and dependencies
4. Plan implementation → Sequence changes (no circular dependencies)
5. Implement with compliance → Follow format and checklist
6. Validate → Run type check, linter, and tests
7. Document changes → Update relevant docs and CHANGELOG
## Anti-Patterns to Avoid

- **Generating code before reading architecture** — You will write code that doesn't fit
- **Naming without context** — Files and functions must reflect system location
- **Silent type escapes** — If types don't compile, the code isn't done
- **Testless delivery** — Untested code is unverified code
- **Hardcoded values** — Configuration belongs in environment or config files