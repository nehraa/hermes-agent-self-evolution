---
name: codebase-documenter
description: This skill should be used when writing documentation for codebases, including README files, architecture documentation, code comments, and API documentation. Use this skill when users request help documenting their code, creating getting-started guides, explaining project structure, or making codebases more accessible to new developers. The skill provides templates, best practices, and structured approaches for creating clear, beginner-friendly documentation.
---

# Codebase Documenter

## Overview

This skill enables creating comprehensive, beginner-friendly documentation for codebases. It provides structured templates and best practices for writing READMEs, architecture guides, code comments, and API documentation that help new users quickly understand and contribute to projects.

## When to Use This Skill

Use this skill when users:

- Request help documenting their code
- Ask for help creating README files
- Need architecture or design documentation
- Want to explain project structure
- Request getting-started guides or tutorials
- Ask for help with inline code comments
- Need API documentation created or improved
- Want to make a codebase more accessible to contributors

## Core Principles for Beginner-Friendly Documentation

### The Seven Principles

1. **Start with the "Why"** — Explain the purpose before diving into implementation details. Answer "what problem does this solve?"
2. **Use Progressive Disclosure** — Present information in layers: simple concepts first, advanced topics later. Link to deeper documentation rather than overwhelming readers.
3. **Provide Context** — Explain not just what the code does, but why it exists. Include the reasoning behind decisions.
4. **Include Examples** — Show concrete usage examples for every concept. Code speaks louder than prose.
5. **Assume No Prior Knowledge** — Define terms, explain jargon, and avoid assumptions about what readers know.
6. **Use Visual Aids** — Include diagrams, flowcharts, ASCII file trees, and screenshots where they aid understanding.
7. **Enable Quick Wins** — Help users get something running within 5 minutes. Success early builds confidence.

### Documentation Quality Checklist

Before finalizing any documentation, verify:

- [ ] A new contributor can run the project without asking questions
- [ ] Every code example is tested and works
- [ ] Terms are defined or linked on first use
- [ ] Visual structure (headings, bullets, code blocks) aids scanning
- [ ] Common errors and solutions are documented
- [ ] Complex concepts have diagrams or analogies
- [ ] There's a clear path from beginner to advanced usage

## Documentation Types and Templates

### 1. README Documentation

**When to create:** Project root directories, major feature modules, or standalone packages.

**Template:**
markdown
# Project Name

One-sentence description that answers "what does this do and for whom?"

## Quick Start

Step-by-step instructions to get running in under 5 minutes.
Include every command verbatim — no placeholders.

## Features

Bulleted list of key capabilities with one-line explanations.

## Project Structure

├── src/              # Source code — what lives here
├── tests/            # Test files — how to run them
├── docs/             # Documentation
└── README.md         # This file
## Getting Started

Prerequisites → Installation → Basic Usage → Next Steps

## Configuration

Environment variables, config files, and their defaults.

## Contributing

Link to CONTRIBUTING.md or brief guidelines.

## License

Standard header with license name.
**Best practices:**

- Lead with the project's value proposition in plain language
- Include setup instructions that are tested and work on the first try
- Provide a visual overview of the project structure
- Link to deeper documentation for advanced topics
- Keep the root README focused on getting started (move advanced content elsewhere)
- Include badges for CI status, version, and package manager

---

### 2. Architecture Documentation

**When to create:** When explaining system design, component relationships, data flow, or design decisions to other developers.

**Template:**
markdown
# Architecture Overview

## System Purpose

[2-3 sentences on what this system does and why it exists]

## High-Level Diagram

[ASCII or Mermaid diagram showing main components]

## Components

### Component Name
- **Purpose:** What this component does
- **Dependencies:** What it relies on
- **Key files:** Where to find the implementation

## Data Flow

1. [Step description]
2. [Step description]
3. [Step description]

## Design Decisions

### Why [X] over [Y]?
**Decision:** [What was chosen]
**Rationale:** [Why this was the right choice]

## Patterns Used

Brief explanation of architectural patterns (e.g., event-driven, repository pattern).
**Best practices:**

- Include a visual diagram even if simple (text diagrams are fine)
- Explain the "why" behind major decisions
- Keep it at the right level — architecture docs are for understanding, not implementation details
- Update when significant changes occur

---

### 3. Code Comments

**When to use:** When explaining complex logic, non-obvious decisions, or edge cases in source code.

**Guidelines for effective code comments:**

| Type | When to Use | Example |
|------|-------------|---------|
| **Summary** | Every function/method | `// Parses user input and validates email format` |
| **Why** | When explaining non-obvious decisions | `// Using setTimeout instead of setInterval to avoid drift` |
| **Warning** | Potential pitfalls or edge cases | `// WARNING: This modifies the original array` |
| **Reference** | External sources or documentation | `// See: RFC 4234 for implementation details` |
| **TODO/FIXME** | Known issues or future work | `// TODO(v2): Remove this workaround after upgrading` |

**What NOT to comment:**

- Obvious code that reads like English (`i++  // increment i`)
- Commented-out code (delete it — use version control)
- Comments that contradict the code (keep them in sync)

---

### 4. API Documentation

**When to create:** For public libraries, microservices, or any API consumed by other developers.

**Template:**
markdown
# API Reference

## Base URL

`https://api.example.com/v1`

## Authentication

Describe authentication method and how to include credentials.

## Endpoints

### Resource Name

#### GET /resources

**Description:** What this endpoint returns.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `page` | integer | No | Page number (default: 1) |

**Response:**
json
{
  "data": [],
  "meta": {
    "page": 1,
    "total": 100
  }
}
**Example:**
bash
curl https://api.example.com/v1/resources?page=2
#### POST /resources

**Request Body:**

json
{
  "name": "required string",
  "enabled": false
}
**Response:** `201 Created` with created resource object.

**Errors:**

| Status | Meaning |
|--------|---------|
| 400 | Invalid request body |
| 401 | Missing or invalid authentication |
**Best practices:**

- Provide runnable examples for every endpoint
- Document error codes and what causes them
- Include response examples for each status code
- Keep parameter descriptions concise but complete
- Use consistent naming and structure across endpoints

---

### 5. Getting Started Guide

**When to create:** For onboarding new users or contributors to a project.

**Structure:**

1. **Prerequisites** — What must be installed/configured first
2. **Installation** — Step-by-step setup commands
3. **Hello World** — Minimal working example
4. **First Task** — Complete a simple, realistic task
5. **Next Steps** — Where to go from here

**Golden rule:** A new user should succeed in under 5 minutes with zero prior knowledge.

---

### 6. Contributing Guide

**When to create:** For open source projects or teams accepting contributions.

**Include:**

- Development setup instructions
- Code style and linting rules
- Branch naming conventions
- Commit message format
- Pull request process
- What to expect in code review
- How to run tests

---

## File Naming Conventions

| Document | Filename | Location |
|----------|----------|----------|
| Project overview | `README.md` | Root |
| Contribution guidelines | `CONTRIBUTING.md` | Root |
| Architecture/design | `ARCHITECTURE.md` or `/docs/architecture.md` | Root or docs/ |
| API reference | `API.md` or `/docs/api.md` | Root or docs/ |
| Changelog | `CHANGELOG.md` | Root |
| Code of conduct | `CODE_OF_CONDUCT.md` | Root |

## Common Mistakes to Avoid

1. **Outdated documentation** — Keep docs in sync with code changes
2. **No examples** — "Do this, then that" without showing actual code
3. **Inconsistent style** — Use the same structure across similar documents
4. **Too much depth in one place** — Use links to deeper content
5. **Assuming expertise** — Define terms, explain context
6. **Missing troubleshooting** — Document what you already know from debugging

## Output Format

When applying this skill, produce documentation that:

- Uses markdown formatting for structure and readability
- Includes code blocks with syntax highlighting
- Provides actionable templates users can adapt
- Contains specific examples rather than generic advice
- Follows progressive disclosure (simple → advanced)
- References external resources for deep dives