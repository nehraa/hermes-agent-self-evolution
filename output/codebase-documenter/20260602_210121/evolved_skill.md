---
category: software-development
description: Creates comprehensive, beginner-friendly documentation for codebases including READMEs, architecture guides, API documentation, and code comments. Use when users need help documenting code, creating getting-started guides, explaining project structure, or making codebases accessible to new developers.
name: codebase-documenter
---

# Codebase Documenter

Creates comprehensive, beginner-friendly documentation for codebases including READMEs, architecture guides, API documentation, and code comments.

## When to Use This Skill

Use this skill when users need help with:
- Writing or improving README files
- Creating architecture or design documentation
- Adding code comments and inline documentation
- Documenting APIs or libraries
- Creating getting-started guides
- Explaining project structure to new contributors
- Making a codebase more accessible to newcomers

## Core Principles for Beginner-Friendly Documentation

Follow these principles when documenting for new users:

1. **Start with the "Why"** — Explain purpose before implementation details
2. **Use Progressive Disclosure** — Present information in layers from simple to complex
3. **Provide Context** — Explain not just what the code does, but why it exists
4. **Include Examples** — Show concrete usage examples for every concept
5. **Assume No Prior Knowledge** — Define terms and avoid jargon when possible
6. **Use Visual Aids** — Include diagrams, flowcharts, and file tree structures
7. **Enable Quick Wins** — Help users get something running within 5 minutes

## Documentation Types and Templates

### 1. README Documentation

**When to create:** Project root, major feature modules, or standalone components.

**Template:**
markdown
# Project Name

## What This Does
[1-2 sentence plain-English explanation of the project's purpose]

## Quick Start
[Steps to get users running in under 5 minutes]

## Project Structure
[Visual file tree with brief explanations]

## Key Concepts
[Core concepts users need to understand first]

## Common Tasks
[Step-by-step guides for frequent operations]

## Troubleshooting
[Common issues and solutions]

## Contributing
[How to contribute, where to get help]
**Best practices:**
- Lead with the project's value proposition and what problem it solves
- Test all setup instructions before publishing
- Provide a visual overview of the project structure
- Link to deeper documentation for advanced topics
- Keep the root README focused on getting started; link out for details

---

### 2. Architecture Documentation

**When to create:** Complex projects needing design rationale, system overview, or contribution guidelines.

**Template:**
markdown
# Architecture Overview

## High-Level Design
[1-2 diagrams showing system components and their relationships]

## Key Components
[Description of each major component and its responsibility]

## Data Flow
[How data moves through the system]

## Decision Rationale
[Why important architectural choices were made]

## Directory Structure
[Explanation of the codebase organization]
**Best practices:**
- Use diagrams liberally—Mermaid, ASCII art, or standard notation
- Explain the "why" behind major decisions, not just the "what"
- Include what changed and why when documenting existing architecture
- Connect code to business logic for non-technical readers

---

### 3. API Documentation

**When to create:** Libraries, SDKs, HTTP APIs, or internal modules with public interfaces.

**Template:**
markdown
# API Reference

## Installation / Setup
[How to install and configure]

## Quick Example
[Minimal working example]

## Core Functions/Endpoints
### Function/Endpoint Name
- **Purpose:** What it does
- **Parameters/Payload:** What to pass
- **Returns:** What it returns
- **Example:** Working code snippet

## Error Handling
[Common errors and how to handle them]
**Best practices:**
- Provide runnable code examples for every method/endpoint
- Document error codes and their causes
- Show both success and failure examples
- Include type signatures for strongly-typed languages

---

### 4. Code Comments

**When to write comments:**
- Explain *why* something is done, not *what* is done (code shows what)
- Document non-obvious decisions or workarounds
- Clarify complex algorithms or business rules
- Mark technical debt or known issues

**Comment templates:**

**Function/method documentation:**
javascript
/**
 * Description of what this function does.
 * @param {type} paramName - Description of the parameter
 * @returns {type} Description of the return value
 * @throws {ErrorType} When/if this condition occurs
 */
**Inline rationale:**
javascript
// We do X instead of Y because [reason including edge case]
// TODO: [description] - [ticket number if applicable]
// NOTE: This behavior differs from standard practice because [reason]
---

## Quick Wins Strategy

To help users experience success within 5 minutes:

1. **Simplest path first** — Show the minimum viable setup, not all options
2. **Include working commands** — Copy-pasteable terminal commands with expected output
3. **One happy path** — Focus on the most common use case before edge cases
4. **Verify works** — Test your documentation by following it yourself

## Measuring Documentation Quality

Use these questions to evaluate documentation:

| Question | Good Answer |
|----------|-------------|
| Can a new developer run this in under 5 minutes? | Yes |
| Is the purpose explained before technical details? | Yes |
| Are there runnable examples for key features? | Yes |
| Is jargon explained on first use? | Yes |
| Does troubleshooting address real issues? | Yes |

---

## Common Mistakes to Avoid

- **No examples** — Code without examples is nearly unusable
- **Outdated instructions** — Test your docs on a fresh system regularly
- **Missing context** — Don't assume readers understand your mental model
- **Inconsistent depth** — Either document everything or explicitly scope what you don't cover
- **Jargon without definitions** — Terms like "microservices," "semantic versioning," or "CRUD" need explaining