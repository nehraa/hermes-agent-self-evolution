---
category: software-development
name: codebase-documenter
description: Use this skill when writing documentation for codebases, including README files, architecture documentation, code comments, and API documentation. Apply when users request help documenting code, creating getting-started guides, explaining project structure, or making codebases more accessible to new developers. Provides templates, best practices, and structured approaches for creating clear, beginner-friendly documentation.
---

# Codebase Documenter

## Overview

This skill provides structured templates and best practices for creating comprehensive, beginner-friendly documentation. It covers READMEs, architecture guides, code comments, and API documentation that help new users quickly understand and contribute to projects.

## When to Use This Skill

- Writing or updating README files
- Creating getting-started guides
- Documenting project structure and architecture
- Writing API documentation
- Adding code comments and inline documentation
- Onboarding new team members or contributors

## Core Principles

Follow these principles when creating beginner-friendly documentation:

| Principle | Description |
|-----------|-------------|
| **Start with "Why"** | Explain purpose before implementation details |
| **Progressive Disclosure** | Layer information from simple to complex |
| **Provide Context** | Explain not just what code does, but why it exists |
| **Include Examples** | Show concrete usage for every concept |
| **Assume No Prior Knowledge** | Define terms; avoid unexplained jargon |
| **Visual Aids** | Use diagrams, flowcharts, and file trees |
| **Quick Wins** | Help users run something useful within 5 minutes |

## Documentation Types

### 1. README Documentation

**When to use:** Project root directories, major feature modules, or standalone packages.

**Template:**

markdown
# Project Name

## What This Does
[1-2 sentence plain-English explanation of value]

## Quick Start
bash
[Installation commands]
[First run command]
[Alternative: Step-by-step setup in 3-5 numbered steps]

## Project Structure
/
├── src/              # Source code description
├── tests/            # Testing setup description
└── docs/             # Additional documentation
## Key Concepts
[3-5 core concepts with brief explanations]

## Common Tasks
### Task 1
[Step-by-step with code examples]

### Task 2
[Step-by-step with code examples]

## Troubleshooting
| Problem | Solution |
|---------|----------|
| [Error message] | [Fix steps] |

## Resources
- [Link to full documentation]
- [Link to API reference]
- [Link to contributing guide]
**Best practices:**
- Lead with the project's value proposition — what problem does it solve?
- Include setup instructions that actually work (test them first)
- Provide a visual overview of the project structure
- Link to deeper documentation for advanced topics
- Keep the root README focused on getting started; move details elsewhere

---

### 2. Architecture Documentation

**When to use:** Explaining system design, component relationships, data flow, or technical decisions.

**Template:**

markdown
# Architecture Overview

## System Purpose
[What the system does and why it exists]

## High-Level Architecture
[Diagram or visual representation]

## Components

### Component Name
**Purpose:** [What this component does]
**Dependencies:** [What it depends on]
**Key files:**
- `path/to/file` — [description]

## Data Flow
1. [Step 1 description]
2. [Step 2 description]
3. [Step 3 description]

## Key Technical Decisions
| Decision | Rationale |
|----------|-----------|
| [Technology choice] | [Why this was selected] |
| [Pattern used] | [Benefits it provides] |

## Boundaries and Interfaces
[How components communicate]
**Best practices:**
- Include a visual diagram when possible
- Explain the "why" behind major decisions
- Document constraints and trade-offs
- Keep it current — link to ADRs for historical context

---

### 3. API Documentation

**When to use:** Documenting endpoints, methods, classes, or public interfaces.

**Template for endpoints:**

markdown
## Endpoint Name

**Method:** `GET|POST|PUT|DELETE`
**Path:** `/api/resource/{id}`
**Auth:** [Authentication requirements]

### Description
[What this endpoint does]

### Request
**Headers:**
| Header | Required | Description |
|--------|----------|-------------|
| `Authorization` | Yes | Bearer token |

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `id` | string | Yes | Resource identifier |

### Response
**Success (200):**
json
{
  "field": "description"
}
**Error (400):**
json
{
  "error": "description",
  "code": "ERROR_CODE"
}
### Example
bash
curl -X GET "https://api.example.com/resource/123" \
  -H "Authorization: Bearer token"
**Template for classes/functions:**

markdown
## ClassName / functionName

**Module:** `package.module`

### Description
[What this does]

### Parameters
| Name | Type | Default | Description |
|------|------|---------|-------------|
| `param` | `string` | — | [description] |

### Returns
[`Type`] — [description]

### Raises
| Exception | When |
|-----------|------|
| `ValueError` | [condition] |

### Example
python
result = functionName(param="value")
**Best practices:**
- Include working examples for every endpoint/method
- Document error codes and what causes them
- Specify required vs optional parameters
- Include authentication requirements upfront
- Test all examples before publishing

---

### 4. Code Comments

**When to use:** Explaining individual functions, complex logic, or non-obvious decisions.

**Guidelines:**

markdown
# Good comment: explains WHY, not WHAT
def calculate_discount(price, customer_type):
    # Apply tiered discounts to reward loyalty
    # while maintaining minimum margins
    discount_rates = {
        'premium': 0.20,
        'standard': 0.10,
        'basic': 0.05
    }
    return price * (1 - discount_rates.get(customer_type, 0))
**Rules:**
- Comment the *why*, not the *what* — code shows what, comments explain why
- Document non-obvious behavior (magic numbers, workarounds, business rules)
- Keep comments up-to-date — outdated comments are worse than none
- Use docstrings for public APIs, inline comments for internal logic

---

### 5. Getting Started Guide

**When to use:** Onboarding new users or contributors to a project.

**Template:**

markdown
# Getting Started in 5 Minutes

## Prerequisites
- [Software 1] version X or higher
- [Software 2]

## Step 1: Install
bash
[Installation command]
## Step 2: Configure
[Configuration steps with example config]

## Step 3: Run Your First [Task]
[Complete working example from start to finish]

## What's Next?
- [Link to tutorial]
- [Link to full documentation]
- [Link to examples repository]
**Best practices:**
- Every step should work on the first try
- Include all commands to copy/paste
- Verify instructions work on a fresh system
- Celebrate the user's first success

## Documentation Checklist

Before publishing, verify:

- [ ] README explains the project's purpose in one sentence
- [ ] Quick start works in under 5 minutes
- [ ] All code examples are tested and run without errors
- [ ] Technical terms are defined or linked
- [ ] File structure is visualized
- [ ] Common errors have documented solutions
- [ ] Links to deeper documentation exist
- [ ] Someone unfamiliar with the project can follow the docs