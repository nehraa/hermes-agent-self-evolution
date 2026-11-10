---
category: software-development
name: codebase-documenter
description: This skill should be used when writing documentation for codebases, including README files, architecture documentation, code comments, and API documentation. Use this skill when users request help documenting their code, creating getting-started guides, explaining project structure, or making codebases more accessible to new developers. The skill provides templates, best practices, and structured approaches for creating clear, beginner-friendly documentation.
---

# Codebase Documenter

## Overview

This skill enables creating comprehensive, beginner-friendly documentation for codebases. It provides structured templates and best practices for writing READMEs, architecture guides, code comments, and API documentation that help new users quickly understand and contribute to projects.

## Core Principles for Beginner-Friendly Documentation

When documenting code for new users, follow these fundamental principles:

1. **Start with the "Why"** - Explain the purpose before diving into implementation details
2. **Use Progressive Disclosure** - Present information in layers from simple to complex
3. **Provide Context** - Explain not just what the code does, but why it exists
4. **Include Examples** - Show concrete usage examples for every concept
5. **Assume No Prior Knowledge** - Define terms and avoid jargon when possible
6. **Visual Aids** - Use diagrams, flowcharts, and file tree structures
7. **Quick Wins** - Help users get something running within 5 minutes

## Documentation Types and Templates

### 1. README Documentation

**When to create:** Project root directories, major feature modules, or standalone components.

**Template:**
markdown
# Project Name

## What This Does
[1-2 sentence plain-English explanation of the project's purpose]

## Quick Start
[Minimal steps to get users running the project in < 5 minutes]

## Project Structure
[Visual file tree with brief explanations]

## Key Concepts
[Core concepts users need to understand]

## Common Tasks
[Step-by-step guides for frequent operations]

## Troubleshooting
[Common issues and solutions]

## Contributing
[How to contribute, coding standards, PR process]

## License
[License information]
**Best practices:**
- Lead with the project's value proposition
- Include setup instructions that actually work (test them first)
- Provide a visual overview of the project structure
- Link to deeper documentation for advanced topics
- Keep the root README focused on getting started
- Include badges for CI status, version, and key metrics

---

### 2. Architecture Documentation

**When to create:** For understanding system design, component relationships, and decision rationale.

**Template:**
markdown
# Architecture Overview

## System Diagram
[ASCII or embedded diagram showing components and relationships]

## Components

### Component Name
- **Purpose:** What this component does
- **Dependencies:** What it depends on
- **Interface:** Key inputs/outputs

## Data Flow
[How data moves through the system]

## Key Decisions
| Decision | Alternative Considered | Rationale |
|----------|----------------------|-----------|
| Choice made | Rejected option | Why this works better |

## Security Considerations
[Authentication, authorization, data handling]
**Best practices:**
- Include visual diagrams (C4 model, sequence diagrams, flowcharts)
- Document the "why" behind major decisions
- Keep diagrams at appropriate abstraction levels
- Update architecture docs when system changes

---

### 3. Code Comments

**When to create:** For complex logic, non-obvious implementations, and business rules.

**Template:**
markdown
// [What the code does - imperative mood]
// [Why it does it this way - context and constraints]
// [Any edge cases or important considerations]
**Examples:**

**Good - explains reasoning:**
javascript
// Using setTimeout instead of requestAnimationFrame here
// because we need this to run even when tab is hidden.
// The callback is lightweight so performance impact is minimal.
**Good - explains complex logic:**
python
# Normalize scores to 0-1 range using min-max scaling.
# We use this instead of z-scores because the distribution
# is bounded and we need interpretable output for the UI.
**Bad - states the obvious:**
javascript
// Loop through users
for (const user of users) {
    // Call the function
    processUser(user);
}
**Best practices:**
- Comment the *why*, not the *what*
- Use inline comments sparingly
- Document preconditions and postconditions
- Explain magic numbers or constants
- Keep comments up-to-date with code changes

---

### 4. API Documentation

**When to create:** For public interfaces, REST APIs, library functions, or SDKs.

**Template:**
markdown
## Endpoint/Function Name

### Description
[What this does in plain language]

### Parameters/Arguments
| Name | Type | Required | Description |
|------|------|----------|-------------|
| param1 | string | Yes | What this parameter does |

### Returns
[What is returned, including error cases]

### Examples
language
// Example usage with expected output
### Error Codes/Exceptions
| Code | Condition | Resolution |
|------|-----------|------------|
| 404 | Resource not found | Check ID validity |

### Notes
[Any caveats, version changes, or related endpoints]
**Best practices:**
- Provide working code examples for every endpoint
- Document error responses and edge cases
- Include request/response examples
- Specify authentication requirements
- Use OpenAPI/Swagger for REST APIs
- Document rate limits and quotas

---

## Project Structure Documentation

For explaining directory layouts, use this template:

markdown
## Project Structure

project-name/
├── src/                    # Source code
│   ├── components/         # Reusable UI components
│   │   └── Button.tsx      # Primary action button
│   ├── pages/              # Route pages
│   └── utils/              # Helper functions
├── tests/                  # Test files (mirror src structure)
├── docs/                   # Documentation
├── scripts/                # Build and deployment scripts
├── package.json            # Dependencies and scripts
└── README.md               # Entry point documentation
**Best practices:**
- Explain *purpose* of directories, not just contents
- Use consistent naming conventions
- Group related files together
- Keep deeply nested structures flat when possible

## Getting Started Guide Template

**Use when:** Onboarding new contributors or users to a project.

markdown
# Getting Started with [Project Name]

## Prerequisites
- Software/tool versions required
- Accounts or access needed

## Installation (5 minutes or less)
Step-by-step commands to get running

## Your First [Task]
Complete a simple, rewarding task that demonstrates core workflow

## Next Steps
- Link to deeper documentation
- Suggest which part of the codebase to explore next
- Point to beginner-friendly issues for contributions
## Writing Checklist

Before finalizing documentation, verify:

- [ ] Does the documentation answer "what is this?" in the first paragraph?
- [ ] Can a new user run or use this within 5 minutes?
- [ ] Are all code examples tested and working?
- [ ] Is jargon defined or avoided?
- [ ] Are there visual elements (diagrams, trees, screenshots)?
- [ ] Are common pitfalls and errors documented?
- [ ] Is the structure consistent with other project docs?
- [ ] Are related resources linked?

## Quick Reference: When to Use Each Type

| Documentation Type | Purpose | Audience |
|--------------------|---------|----------|
| README | Entry point, quick start | Everyone |
| Architecture | System design understanding | Developers, architects |
| Code Comments | Implementation details | Future maintainers |
| API Docs | How to use interfaces | Integrators, consumers |
| Getting Started | Onboarding | New contributors/users |