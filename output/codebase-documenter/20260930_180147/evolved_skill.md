---
category: software-development
description: Use this skill when users need help documenting codebases, creating README files, writing architecture documentation, adding code comments, or generating API documentation. Apply this skill when users request getting-started guides, project structure explanations, or assistance making codebases accessible to new developers. The skill provides templates, best practices, and structured approaches for creating clear, beginner-friendly documentation.
name: codebase-documenter
---

# Codebase Documenter

Create comprehensive, beginner-friendly documentation that helps new users understand and contribute to projects quickly.

## When to Use This Skill

Use this skill when users request:

- Help writing README files or project documentation
- Architecture or design documentation
- Code comments and inline documentation
- API documentation or reference guides
- Getting-started guides or tutorials
- Explanations of project structure
- Documentation for onboarding new developers

## Core Principles

### 1. Lead with Purpose

Explain **why** the project exists before describing how it works. Answer: "What problem does this solve?"

### 2. Progressive Disclosure

Organize information from simple to complex:
- **Level 1:** What is this? (one sentence)
- **Level 2:** How do I get started? (5 minutes)
- **Level 3:** How does it work? (concepts)
- **Level 4:** Deep dive (reference)

### 3. Show, Don't Just Tell

Include working code examples for every concept. Never describe functionality without demonstrating it.

### 4. Assume Beginner Knowledge

Define technical terms. Avoid unexplained jargon. When you must use acronyms, expand them on first use.

### 5. Enable Quick Wins

Users should accomplish something meaningful within 5 minutes of reading.

### 6. Visualize Structure

Use diagrams, file trees, and flowcharts to show relationships that are hard to convey in text.

## Documentation Types

### README Documentation

**When to create:** Project root, major feature modules, standalone packages, or library entry points.

**Template:**

markdown
# Project Name

One-sentence description of what this does and who it's for.

## Quick Start

Step-by-step instructions to get running in under 5 minutes.
Include every command with expected output.

## What This Is For

Explain the core purpose and use cases.
Answer: "When would I use this?"

## Installation

Prerequisites → Installation → Verification
Test every command before documenting it.

## Project Structure

├── src/              # Description of this directory
│   ├── main/         # Description
│   └── utils/        # Description
├── tests/            # Description
└── docs/             # Description
Explain the structure visually. Link to detailed docs.

## Common Tasks

Step-by-step guides for 3-5 most frequent operations:
1. Task name → Prerequisites → Steps → Expected result
2. ...

## Examples

Real-world usage examples with complete, runnable code.

## Troubleshooting

Common issues → Causes → Solutions
Format: "If you see [error], it means [cause], and [fix] resolves it."

## Contributing

How to set up development environment, coding standards,
where to find help, how to submit changes.
**Best practices:**
- Place the most important information first
- Include working, tested commands
- Add a visual structure overview
- Link to deeper documentation
- Keep it focused—move details to separate docs

---

### Architecture Documentation

**When to create:** Complex projects, distributed systems, projects with multiple components, or when explaining design decisions to new contributors.

**Template:**

markdown
# Architecture Overview

## System Purpose

[2-3 sentences on what this system does]

## High-Level Diagram

┌─────────────┐     ┌─────────────┐
│   Client    │────▶│   API       │
└─────────────┘     └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  Services   │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
         ┌────────┐   ┌────────┐   ┌────────┐
         │ Store  │   │ Cache  │   │ Queue  │
         └────────┘   └────────┘   └────────┘
## Components

### Component Name
- **Purpose:** What it does
- **Technology:** Language/framework used
- **Dependencies:** What it depends on
- **Key files:** Important files to understand

## Data Flow

1. [Step description with diagram]
2. [Step description with diagram]
3. ...

## Key Design Decisions

| Decision | Reason | Alternative Considered |
|----------|--------|----------------------|
| [What]   | [Why]  | [What else was tried]|

## Security Model

How authentication and authorization work.
**Best practices:**
- Include diagrams—text alone can't convey system relationships
- Explain the "why" behind major decisions
- Document trade-offs considered
- Keep diagrams consistent with legend/notation

---

### Code Comments

**When to use:** Complex algorithms, non-obvious implementations, business logic, workarounds, or areas requiring specific caution.

**Good comment patterns:**

python
# Calculate shipping cost using zone-based pricing
# We use zones instead of weight to reduce API calls to carrier
def calculate_shipping(weight, zone):
    ...

# TODO(maria): Remove this workaround after upgrading to API v3
# The old API doesn't support batch operations for inventory
def legacy_batch_update(items):
    ...
**Template:**

markdown
# [File/Purpose]
# 
# [When to read this file, what problems it solves]
#
# Key concepts:
# - [Concept 1]: [Plain-English explanation]
# - [Concept 2]: [Plain-English explanation]

# [Function/purpose block]

def function_name(param):
    """What this does.

    More detail if needed about behavior.

    Args:
        param: Description (type if non-obvious)

    Returns:
        Description (type if non-obvious)

    Raises:
        ExceptionType: When this is raised

    Example:
        >>> result = function_name(value)
        >>> print(result)
        expected_output
    """
    # Implementation comment (explains "why", not "what")
**Rules:**
- Explain **why** code does something, not **what** it does (the code shows what)
- Document non-obvious decisions, not obvious ones
- Update comments when code changes
- Never leave TODO comments without context or author initials

---

### API Documentation

**When to create:** Public APIs, internal service contracts, or library interfaces.

**Template:**

markdown
# API Reference

## Authentication

[How to authenticate, example requests]

## Endpoints

### Resource Name

`POST /resources` Create a new resource

**Request:**
json
{
  "name": "string (required)",
  "type": "string (enum: a, b, c)",
  "config": "object (optional)"
}
**Response:** `201 Created`
json
{
  "id": "uuid",
  "name": "string",
  "created_at": "ISO8601 timestamp"
}
**Errors:**
| Status | Condition | Response |
|--------|-----------|----------|
| 400    | Invalid input | `{"error": "message"}` |
| 401    | Missing auth | `{"error": "unauthorized"}` |

**Example:**
bash
curl -X POST /api/v1/resources \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"name": "my-resource"}'
## Rate Limits

[Limits and headers returned]

## Error Codes

[All possible error codes with meanings]
**Best practices:**
- Show working curl examples for every endpoint
- Document all error responses
- Include request and response examples
- Specify which fields are required vs optional
- Document rate limits upfront

---

## Quick Reference Checklist

Use this checklist before finalizing any documentation:

- [ ] Purpose is explained in one sentence
- [ ] Getting started works in under 5 minutes
- [ ] Every concept has a working example
- [ ] Technical terms are defined on first use
- [ ] Project structure is visualized
- [ ] Common errors have documented solutions
- [ ] All commands are tested and accurate
- [ ] Links to deeper documentation are provided
- [ ] Content is scannable (headings, bullets, code blocks)

## Common Mistakes to Avoid

| Mistake | Instead |
|---------|---------|
| "See the code" as explanation | Explain intent and context |
| Walls of text | Use headings, bullets, diagrams |
| Outdated examples | Test and update regularly |
| Assuming expertise | Define terms, explain basics |
| Covering everything | Link to details, focus on essentials |
| Generic template content | Customize for your specific project |