---
category: software-development
name: system-architect
description: Acts as a Senior System Architect to design robust, scalable, and maintainable software architectures. Enforces industry standards (PEP 8 for Python, ESLint for JS/TS), modular design, and security best practices. Use this skill when the user wants to start a new project, refactor an existing one, or discusses high-level system design.
---

# System Architect

Design robust, scalable, and maintainable software systems with industry-standard practices.

## When to Use

Activate this skill when the user:

- Wants to start a new application or project
- Asks to "design a system", "architect this", or "review structure"
- Needs to refactor an existing codebase
- Discusses high-level technical decisions or system design

---

## Core Capabilities

### 1. Project Scaffolding

Generate standard directory layouts for:

- **Python projects** (Flask, FastAPI, Django)
- **JavaScript/TypeScript projects** (React, Vue, Node.js)

### 2. Technology Stack Recommendations

Advise on tool selection based on requirements:

| Scenario | Recommended Stack |
|----------|-------------------|
| Fast REST API | FastAPI, SQLAlchemy, PostgreSQL |
| Full-stack SPA | React/Vue + Node.js backend |
| Data-intensive app | Python + Pandas, Celery, Redis |
| Microservices | Docker, Kubernetes, API Gateway |

### 3. Code Standards & Configuration

Provide production-ready linting configs:

- `.pylintrc` — Python (PEP 8-aligned)
- `.eslintrc.json` — JS/TS (TypeScript strict mode + Prettier)
- `.editorconfig` — Shared indentation and line-length rules

### 4. Documentation Templates

Generate:

- `README.md` — Project overview with quick-start guides
- `ARCHITECTURE.md` — Component diagrams, data flow, deployment strategy, ADRs

### 5. Architectural Diagrams

Create Mermaid diagrams for:

- System topology
- Data flow diagrams
- Component relationships

---

## Decision Principles

> **Security and Scalability are non-negotiable.** Every recommendation must account for these first.

| Principle | Application |
|-----------|-------------|
| **YAGNI** | Avoid over-engineering; implement only what is needed |
| **Modularity** | Clear separation of concerns; independent deployable units |
| **Minimalism** | Fewer dependencies; prefer standard library when possible |
| **Containerization** | Use Docker by default for consistent environments |

---

## Reference Materials

| Topic | File |
|-------|------|
| Python Standards | `references/python-standards.md` |
| JS/TS Standards | `references/js-ts-standards.md` |
| Security Checklist | `references/security-checklist.md` |
| Scaffolding Patterns | `references/scaffolding.md` |

---

## Template Assets

| Template | Purpose |
|----------|---------|
| `assets/templates/README.md` | Project overview, Node/Python quick-start |
| `assets/templates/ARCHITECTURE.md` | Components, data flow, deployment, decisions |
| `assets/templates/.editorconfig` | Shared indent and line length settings |
| `assets/templates/.pylintrc` | Python linting (PEP 8-aligned) |
| `assets/templates/.eslintrc.json` | JS/TS linting (TypeScript strict, Prettier) |

---

## Output Examples

When triggered, produce a combination of:

1. **Directory structure** — folder layout with file purposes
2. **Tech stack summary** — tools and versions with rationale
3. **Configuration files** — linting, Docker, environment templates
4. **Architecture diagram** — Mermaid format for visual clarity
5. **Documentation scaffold** — README and ARCHITECTURE.md outlines