---
category: software-development
description: 'This skill should be used when writing documentation for codebases, including README files, architecture documentation, code comments, and API documentation. Use this skill when users request help documenting their code, creating getting-started guides, explaining project structure, or making codebases more accessible to new developers. The skill provides templates, best practices, and structured approaches for creating clear, beginner-friendly documentation.'
name: codebase-documenter
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

## Documentation Types and When to Use Them

### 1. README Documentation

**When to create:** For project root directories, major feature modules, or standalone components.

**Structure to follow:**

markdown
# Project Name

One sentence that explains what this does and who it's for.

## Quick Start

Commands to get the project running in under 5 minutes.

## What This Does

1-2 paragraphs explaining the project's purpose, key features, and value.

## Project Structure

project/
├── src/           # Description of this directory
├── tests/         # Description of this directory
└── docs/          # Description of this directory
## Key Concepts

Explanation of core concepts users need to understand before diving deeper.

## Common Tasks

Step-by-step guides for frequent operations:
- Task 1
- Task 2
- Task 3

## Troubleshooting

Common issues and solutions.

## Contributing

How to contribute to the project.
**Best practices:**
- Lead with the project's value proposition
- Include setup instructions that actually work (test them!)
- Provide a visual overview of the project structure
- Link to deeper documentation for advanced topics
- Keep the root README focused on getting started

### 2. Architecture Documentation

**When to create:** For complex systems, multiple contributors, or when explaining design decisions.

**Structure to follow:**

markdown
# Architecture Overview

## System Diagram

[ASCII or Mermaid diagram showing high-level components]

## Components

### Component Name
- **Purpose:** What this component does
- **Dependencies:** What it relies on
- **Boundaries:** How it communicates with other components

## Data Flow

[Explain how data moves through the system]

## Design Decisions

| Decision | Rationale | Alternative Considered |
|----------|-----------|------------------------|
| Database X | Reason | Database Y |

## Key Patterns

Description of architectural patterns used (e.g., event-driven, microservices).
### 3. API Documentation

**When to create:** For any public API, library, or service with endpoints/classes that external users will consume.

**For each endpoint/method, document:**

markdown
### Endpoint Name

**What it does:** Brief description

**Request:**
- Method: GET/POST/etc.
- Path: /api/resource
- Headers: Authorization, Content-Type
- Body: JSON schema or example

**Response:**
- Success (200): Response schema + example
- Error (400): What went wrong + example
- Error (401): What went wrong + example

**Example:**
bash
curl -X POST https://api.example.com/resource \
  -H "Authorization: Bearer token" \
  -d '{"key": "value"}'
### 4. Code Comments

**When to write comments:**
- **Why, not what** - Explain reasoning behind non-obvious code
- **Business logic** - Document rules that aren't obvious from the code
- **Complex algorithms** - Explain the approach when it requires thought
- **Technical debt** - Mark areas that need attention with TODO/FIXME

**Comment templates:**

python
# Why: We process in batches to avoid memory issues with large datasets.
# Trade-off: This increases latency but prevents OOM errors.
# See: https://github.com/org/repo/issues/123
def process_large_dataset(data):
    pass

# TODO(maria): Remove this hack after upgrading to v2 API
# Reason: The v1 endpoint returns data in a format we don't control
def workaround_for_v1_bug():
    pass
**What NOT to comment:**
- Obvious code that explains itself
- Comments that describe what the code does (the code already does this)
- Outdated comments (keep them in sync or remove them)

## Documentation Templates by Use Case

### Getting Started Guide

markdown
# Getting Started with [Project Name]

Estimated time: X minutes

## Prerequisites

- Item 1
- Item 2

## Installation

Step-by-step installation commands.

## Your First [Feature]

Walk through creating/deleting/configuring something simple.

## Next Steps

- Link to full documentation
- Link to tutorials
- Link to examples
### Contributing Guide

markdown
# Contributing to [Project Name]

## Code of Conduct

Link to CoC.

## Getting Started

1. Fork the repo
2. Clone it
3. Run setup commands

## Development Workflow

How to run tests, lint, and develop locally.

## Pull Request Process

1. Create feature branch
2. Make changes
3. Add tests
4. Submit PR

## Coding Standards

Style guide references and enforcement tools.
## Quick Reference: File Naming Conventions

| Documentation Type | Recommended Filename |
|-------------------|---------------------|
| Project overview | `README.md` |
| Architecture | `ARCHITECTURE.md` |
| Contributing | `CONTRIBUTING.md` |
| API reference | `API.md` or `api-reference.md` |
| Setup guides | `docs/getting-started.md` |
| Troubleshooting | `TROUBLESHOOTING.md` or `docs/troubleshooting.md` |
| Changelog | `CHANGELOG.md` |

## Maintenance Checklist

- [ ] README accurately reflects current project state
- [ ] Setup instructions tested on a clean environment
- [ ] Links to deeper documentation are functional
- [ ] Code comments are up-to-date
- [ ] Examples produce expected output
- [ ] Architecture docs match implementation