---
category: software-development
name: senior-architect
description: 'This skill should be used when the user asks to "design system architecture", "evaluate microservices vs monolith", "create architecture diagrams", "analyze dependencies", "choose a database", "plan for scalability", "make technical decisions", or "review system design". Use for architecture decision records (ADRs), tech stack evaluation, system design reviews, dependency analysis, and generating architecture diagrams in Mermaid, PlantUML, or ASCII format.'
---

# Senior Architect

Architecture design and analysis tools for making informed technical decisions.

## Table of Contents

- [Quick Start](#quick-start)
- [Tools Overview](#tools-overview)
- [Decision Workflows](#decision-workflows)
- [Reference Documentation](#reference-documentation)
- [Common Commands](#common-commands)

---

## Quick Start

bash
# Generate architecture diagram
python scripts/architecture_diagram_generator.py ./my-project --format mermaid

# Analyze dependencies
python scripts/dependency_analyzer.py ./my-project --output json

# Get architecture assessment
python scripts/project_architect.py ./my-project --verbose
---

## Tools Overview

### 1. Architecture Diagram Generator

Generates architecture diagrams from project structure in multiple formats.

**Use when:** You need to visualize system architecture for documentation, team discussion, or technical planning.

**Supported formats:**
- `mermaid` — Default, web-rendered, ideal for markdown docs
- `plantuml` — UML-standard, enterprise tooling compatible
- `ascii` — Terminal-friendly, git-friendly diffs

**Supported diagram types:**

| Type | Use Case |
|------|----------|
| `component` | Module relationships and internal structure |
| `layer` | Architectural layers (presentation, business, data) |
| `deployment` | Infrastructure topology and runtime placement |

**Usage:**

bash
# Generate component diagram (default)
python scripts/architecture_diagram_generator.py ./project --format mermaid --type component

# Generate layer diagram in PlantUML
python scripts/architecture_diagram_generator.py ./project --format plantuml --type layer

# Generate deployment diagram in ASCII
python scripts/architecture_diagram_generator.py ./project --format ascii --type deployment

# Save to file
python scripts/architecture_diagram_generator.py ./project --format mermaid --output architecture.mmd
**Output:** Diagram code ready for rendering or embedding in documentation.

---

### 2. Dependency Analyzer

Scans project dependencies for version conflicts, security issues, and architectural problems.

**Use when:** You need to audit dependencies, find circular references, or evaluate upgrade paths.

**Capabilities:**
- Detect circular dependencies
- Identify version conflicts
- Flag deprecated packages
- Report unused dependencies
- Generate dependency graphs

**Usage:**

bash
# Analyze and output JSON report
python scripts/dependency_analyzer.py ./my-project --output json

# Analyze with dependency graph
python scripts/dependency_analyzer.py ./my-project --graph --format mermaid

# Check for security vulnerabilities
python scripts/dependency_analyzer.py ./my-project --security --min-severity high

# Find circular dependencies
python scripts/dependency_analyzer.py ./my-project --circular
**Output formats:**
- `json` — Structured data for CI/CD integration
- `mermaid` — Visual dependency graph
- `html` — Interactive report
- `text` — Human-readable summary

---

### 3. Project Architect

Provides comprehensive architecture assessment and recommendations.

**Use when:** You need a quick audit, want architectural guidance, or need to document current architecture.

**Capabilities:**
- Assess architectural patterns in use
- Identify anti-patterns
- Score complexity and maintainability
- Suggest improvements
- Generate Architecture Decision Records (ADRs)

**Usage:**

bash
# Full verbose assessment
python scripts/project_architect.py ./my-project --verbose

# Generate ADR for recent decisions
python scripts/project_architect.py ./my-project --generate-adr --decision "Choose PostgreSQL over MongoDB"

# Export architecture report
python scripts/project_architect.py ./my-project --report markdown --output architecture-report.md

# Compare architectures
python scripts/project_architect.py ./project-a --compare ./project-b
---

## Decision Workflows

### Database Selection Workflow

Use when choosing a database for a project.

**Step 1: Identify data characteristics**

| Characteristic | Options |
|----------------|---------|
| Schema flexibility needed? | No → SQL. Yes → Document, Key-Value |
| Relationships critical? | Yes → Relational. Optional → Consider Graph |
| Scale requirements | <10K writes/s → Most databases. >100K → Specialized |
| Query patterns | Simple key-value → KV. Complex joins → Relational/Graph |

**Step 2: Evaluate candidates**

bash
# Compare database options for your workload
python scripts/project_architect.py ./my-project --evaluate-db --workload "high-read-reporting"
**Step 3: Document decision**

bash
# Generate ADR for database selection
python scripts/project_architect.py ./my-project --generate-adr --decision "PostgreSQL for transactional data"
**Common patterns:**

| Use Case | Recommended | Alternatives |
|----------|-------------|--------------|
| Transactions, financial data | PostgreSQL | MySQL, CockroachDB |
| Flexible schemas, rapid iteration | MongoDB, PostgreSQL JSON | CouchDB |
| High-scale key-value cache | Redis | Memcached |
| Full-text search | Elasticsearch, PostgreSQL FTS | Meilisearch |
| Graph relationships | Neo4j, Amazon Neptune | PostgreSQL + recurs |
| Time-series data | TimescaleDB, InfluxDB | PostgreSQL + partitioning |

---

### Architecture Pattern Selection Workflow

**Step 1: Assess team and organization**

| Factor | Consideration |
|--------|----------------|
| Team size | <5 → Monolith simpler. >20 → Microservices manageable |
| Deployment frequency needed | Rare → Monolith. Continuous → Modular/microservices |
| Regulatory requirements | Independent scaling needed → Services |

**Step 2: Analyze workload characteristics**

bash
# Get workload analysis
python scripts/project_architect.py ./my-project --analyze-workload
**Step 3: Match patterns to needs**

| Pattern | Best For | Avoid When |
|---------|----------|------------|
| Monolith | MVPs, small teams, tight deadlines | Multiple teams, varied scaling needs |
| Modular Monolith | Growing teams, eventual microservices | - |
| Layered Architecture | Business apps, CRUD systems | High-performance, event-driven |
| Clean Architecture | Complex domain logic, testability priority | Simple CRUD apps |
| Hexagonal Architecture | Plugin systems, multiple adapters | - |
| Event-Driven | Real-time, loosely coupled, async workflows | Synchronous requirements |
| Microservices | Independent deployability, polyglot needs | Small teams, tight coupling |

---

### Monolith vs Microservices Decision

**Choose Monolith when:**
- Team size < 10 developers
- Application is a single bounded context
- You need to validate product-market fit
- Deployment and operations complexity should be minimized
- Transactional consistency is critical across features

**Choose Microservices when:**
- Team size > 15 with clear ownership boundaries
- Different components have fundamentally different requirements (languages, scaling, deployment)
- Independent deployability is a hard requirement
- You have成熟的 DevOps culture and tooling

**Evaluate hybrid approaches:**
- Modular Monolith — Single deploy, clear internal boundaries
- Services by team — Aligned to team boundaries, not technical layers
- Strangler Fig — Migrate incrementally from monolith

bash
# Get recommendation based on project characteristics
python scripts/project_architect.py ./my-project --recommend-architecture
---

## Reference Documentation

### Tech Stack Coverage

**Languages:** Python, JavaScript/TypeScript, Java, Go, Rust, C#, Ruby, PHP

**Databases:**
- Relational: PostgreSQL, MySQL, MariaDB, SQLite
- Document: MongoDB, CouchDB
- Key-Value: Redis, DynamoDB
- Graph: Neo4j, Amazon Neptune
- Time-series: TimescaleDB, InfluxDB

**Frameworks:** Django, FastAPI, Express, Spring Boot, .NET Core, Rails, Laravel

**Infrastructure:** Docker, Kubernetes, AWS, Azure, GCP

**Messaging:** RabbitMQ, Kafka, SQS, Redis Pub/Sub

---

### Common Commands

bash
# Architecture Diagrams
python scripts/architecture_diagram_generator.py <path> --format mermaid --type component
python scripts/architecture_diagram_generator.py <path> --format plantuml --type layer
python scripts/architecture_diagram_generator.py <path> --format ascii --type deployment

# Dependency Analysis
python scripts/dependency_analyzer.py <path> --output json
python scripts/dependency_analyzer.py <path> --circular --graph
python scripts/dependency_analyzer.py <path> --security --min-severity high

# Architecture Assessment
python scripts/project_architect.py <path> --verbose
python scripts/project_architect.py <path> --generate-adr --decision "<description>"
python scripts/project_architect.py <path> --recommend-architecture

# Compare architectures
python scripts/project_architect.py <path-a> --compare <path-b>