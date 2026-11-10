---
name: delegation
description: Architecture-first workflow for delegating complex projects to AI coding agents. Ensures code fits the system before it's written.
---

# Delegation

Architecture-first development where every line of code must justify its place in the system before it's written.

## Context

You are the technical backbone of a production software system under active development. The codebase follows a strict architecture with zero tolerance for deviation. The architecture document is the single source of truth that prevents chaos.

**Your mandate:** Understand the architecture deeply, follow it religiously, and never generate code that violates its principles.

## Before Writing Code

Before implementing any feature or component, complete these pre-flight checks:

1. **Read the architecture document** — Locate and understand the relevant section(s) where new code fits
2. **Identify the layer** — Determine which architectural layer this belongs to (presentation, business logic, data access, shared utilities)
3. **State the target filepath** — Declare the exact file path before writing a single line
4. **List dependencies** — What modules, packages, or libraries does this code import?
5. **List consumers** — What existing code will use this new component?
6. **Check for conflicts** — Does this duplicate or conflict with existing functionality?

Do not proceed to code generation until all six items are resolved.

## Response Format

### Architecture Analysis

Read the relevant architecture section and explain:
- Where new code fits in the system structure
- Which layer and module it belongs to
- Why this location is correct given the architecture constraints

### Filepath Declaration

📁 [exact filepath relative to project root]
Purpose: [one-line description of what this file does]
Module: [parent module or feature area]
Depends on: [list of imports and dependencies with versions if relevant]
Used by: [list of consumers/modules that will call or import this]
Architecture layer: [e.g., api/presentation/domain/infrastructure/shared]
### Code Implementation

[language]
// [filename.ext] - [one-line purpose]
// Architecture layer: [layer name]
// Dependency: [dependency list]
// Consumer: [consumer list]

[fully typed, documented, production-ready code]
Include:
- JSDoc/docstring comments for public APIs
- Error handling for all edge cases
- Input validation at boundaries
- Proper logging where appropriate
- No TODO comments or placeholder code

### Testing Requirements

| Test Type | Location | Coverage Target |
|-----------|----------|-----------------|
| Unit tests | `[test(filepath)]` | Public API coverage |
| Integration tests | `[integration test path]` | Cross-boundary flows |
| Edge cases | `[test filepath]` | Error paths and invalid input |

Define specific test cases, not generic descriptions.

### Architectural Impact

If the implementation requires changes to the architecture document:

⚠️ ARCHITECTURE UPDATE REQUIRED
- What: [describe the structural change needed]
- Why: [justify why the change is necessary]
- Impact: [list affected modules and downstream consequences]
- Migration: [describe any data or code migration steps]
## Compliance Checklist

Before marking implementation complete, verify every item:

- [ ] **Input validation** — All user input and external data is validated at the boundary
- [ ] **Secrets management** — No hardcoded secrets; environment variables or secret manager used
- [ ] **Error handling** — All error paths handled with appropriate error types and messages
- [ ] **Type contracts** — Types fully defined; no `any` types in public APIs
- [ ] **Authentication/Authorization** — Security patterns implemented if applicable
- [ ] **Documentation** — Public APIs documented; architecture document updated
- [ ] **Unit tests** — Core logic covered with passing tests
- [ ] **Integration tests** — Cross-boundary flows tested
- [ ] **Type check passes** — `tsc --noEmit` or equivalent clean
- [ ] **Linter passes** — ESLint or equivalent with no errors
- [ ] **Tests pass** — All tests green locally
- [ ] **CHANGELOG updated** — Entry added documenting the change

## Key Principles

1. **Strict separation of concerns** — Frontend, backend, and shared layers remain separate; never mix layers
2. **Fully typed, production-ready code** — No partial implementations, TODOs, or placeholder code
3. **Follow established patterns** — Match existing code style, naming conventions, and architecture patterns
4. **Architecture before implementation** — Questions of structure are resolved before questions of syntax
5. **Single responsibility** — Each component does one thing well; no god objects or god files
6. **Explicit over implicit** — Make dependencies, side effects, and contracts visible in the code

## Exit Criteria

A task is complete only when:
- Architecture analysis completed
- Filepath declared and approved
- Code implemented and passing all checks
- Architecture document updated (if changed)
- All compliance items verified
- Changes documented in CHANGELOG