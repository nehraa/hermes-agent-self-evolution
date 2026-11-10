---
category: software-development
name: codebase-documenter
description: This skill should be used when writing documentation for codebases, including README files, architecture documentation, code comments, and API documentation. Use this skill when users request help documenting their code, creating getting-started guides, explaining project structure, or making codebases more accessible to new developers. The skill provides templates, best practices, and structured approaches for creating clear, beginner-friendly documentation.
---

# Codebase Documenter

## Overview

This skill enables creating comprehensive, beginner-friendly documentation for codebases. It provides structured templates and best practices for writing READMEs, architecture guides, code comments, and API documentation that help new users quickly understand and contribute to projects.

## When to Use This Skill

Use this skill when:

- Writing or updating a README file
- Creating architecture or design documentation
- Adding code comments and docstrings
- Writing API documentation
- Creating getting-started guides or tutorials
- Explaining project structure to new team members
- Onboarding new developers to a codebase

## Core Principles for Beginner-Friendly Documentation

### 1. Start with the "Why"

Explain the project's purpose and value before diving into implementation details. Users need to understand *why* they should care before learning *how* it works.

**Example:**
> Instead of: "This service implements OAuth 2.0 authentication"
> Write: "This handles user login so you don't have to build your own security system"

### 2. Use Progressive Disclosure

Present information in layers from simple to complex:

- **Layer 1:** Quick start (what users need *right now*)
- **Layer 2:** Core concepts (what users need to understand the codebase)
- **Layer 3:** Deep dives (advanced topics for power users)

### 3. Provide Context

Explain not just what the code does, but why it exists. Document decisions, constraints, and alternatives considered.

### 4. Include Concrete Examples

Show working examples for every concept. Code examples should be:

- Runnable (test them!)
- Minimal but complete
- Commented for clarity
- Matching common use cases

### 5. Assume No Prior Knowledge

- Define technical terms on first use
- Link to external resources for prerequisite knowledge
- Avoid unexplained jargon or acronyms

### 6. Use Visual Aids

- File tree diagrams for structure
- ASCII diagrams for architecture
- Flowcharts for processes
- Screenshots for UI components

### 7. Enable Quick Wins

Help users get something working within 5 minutes. Success early builds confidence.

---

## Documentation Types and Templates

### 1. README Documentation

**When to create:**
- Project root directory
- Major feature modules
- Standalone packages or libraries

**Required sections:**

markdown
# [Project Name]

One-paragraph explanation of what this does and why it exists.

## Quick Start

Step-by-step instructions to get running in under 5 minutes.
Include exact commands to copy-paste.

## Features

Bulleted list of key capabilities (5-8 items max).

## Project Structure

[Visual file tree with one-line descriptions]

## Usage Examples

Minimal, runnable code examples for common tasks.

## Contributing

Links to development setup, coding standards, and PR process.

## Resources

- [Link to full documentation]
- [Link to API reference]
- [Link to troubleshooting guide]
**Best practices:**
- Keep the root README under 500 words
- Place detailed docs in separate files
- Update with every significant change
- Add a badge row for quick status info (tests, version, license)

---

### 2. Architecture Documentation

**When to create:**
- New projects (document before building)
- Complex existing systems
- Before onboarding new team members
- During architecture reviews

**Template:**

markdown
# [Component] Architecture

## Overview

High-level description of this component's purpose and responsibilities.

## Context

[Diagram showing how this component fits in the system]

## Design Decisions

| Decision | Rationale | Alternatives Considered |
|----------|-----------|------------------------|
| Use X | Benefit A | Y was rejected because... |

## Components

### [Sub-component Name]

**Responsibility:** What it owns
**Boundaries:** What it talks to
**Key patterns:** Important implementation details

## Data Flow

[User Action] → [Component A] → [Component B] → [Result]
## Constraints and Assumptions

- [Known limitations]
- [Prerequisites]
---

### 3. Code Comments

**Inline comments (within functions):**

python
# Use this format for non-obvious implementation details
# Fetch user preferences from cache, falling back to database
# This reduces API calls by ~80% for repeated reads
preferences = cache.get(user_id) or db.fetch_preferences(user_id)
**Docstrings (functions and classes):**

python
def calculate_discount(customer_type: str, amount: float) -> float:
    """
    Calculate the discount percentage for a customer.

    Args:
        customer_type: One of 'retail', 'wholesale', or 'enterprise'
        amount: The purchase amount in dollars

    Returns:
        Discount percentage (0.0 to 1.0)

    Raises:
        ValueError: If customer_type is not recognized

    Example:
        >>> calculate_discount('wholesale', 1000)
        0.15
    """
**Best practices:**
- Explain *why*, not *what* (the code shows what)
- Keep comments up-to-date with code changes
- Don't comment obvious code (it adds noise)
- Use docstrings for public APIs only

---

### 4. API Documentation

**Endpoint documentation template:**

markdown
## [METHOD] /endpoint/path

**Description:** What this endpoint does

**Authentication:** Required/Optional [type]

### Request

**Headers:**
| Header | Required | Description |
|--------|----------|-------------|
| Content-Type | Yes | application/json |

**Body:**
json
{
  "field_name": {
    "type": "string",
    "required": true,
    "description": "What this field means"
  }
}
### Response

**200 OK:**
json
{
  "result": "The returned data structure"
}
**400 Bad Request:**
json
{
  "error": "Description of what went wrong",
  "code": "ERROR_CODE"
}
### Example

bash
curl -X POST /api/endpoint \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"field": "value"}'
---

### 5. Getting Started Guide

**Template:**

markdown
# Getting Started with [Project]

## What You'll Build

[One-paragraph description of a working example]

## Prerequisites

- [Software/tool] version X.X+
- [Account/service] access

## Step 1: [First action]

[Screenshot or diagram]

[Tasy-to-copy commands]

## Step 2: [Second action]

[Continue building the example]

## Step 3: [Third action]

## Next Steps

- [Link to deeper tutorials]
- [Link to API reference]
- [Link to more examples]
---

## Checklist for Documentation Quality

Before publishing documentation, verify:

- [ ] README has a working quick start
- [ ] All code examples are tested and runnable
- [ ] Jargon and acronyms are defined on first use
- [ ] Visual aids clarify (not clutter) the content
- [ ] Users can succeed within 5 minutes
- [ ] Links to deeper resources exist for advanced topics
- [ ] Spelling and grammar are correct
- [ ] Documentation matches current code behavior

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Better Approach |
|--------------|---------|-----------------|
| "See the code" | Forces reading source | Explain intent and design |
| Walls of text | Overwhelms readers | Use headers, bullets, diagrams |
| Outdated examples | Builds mistrust | Test and update regularly |
| Assumes expert knowledge | Excludes newcomers | Define terms, link to prerequisites |
| Docu-hallucination | Invented features | Reference actual implementation |