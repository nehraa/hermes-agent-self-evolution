---
category: software-development
name: senior-architect
description: 'Use when user asks to design system architecture, evaluate microservices vs monolith, create architecture diagrams, analyze dependencies, choose a database, plan for scalability, make technical decisions, review system design, or generate Architecture Decision Records (ADRs). Covers tech stack evaluation, system design reviews, dependency analysis, and diagram generation in Mermaid, PlantUML, or ASCII format.'
---

# Senior Architect

System architecture design, analysis, and decision-making tools for informed technical choices.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Tools](#tools)
  - [Architecture Diagram Generator](#1-architecture-diagram-generator)
  - [Dependency Analyzer](#2-dependency-analyzer)
  - [Project Architect](#3-project-architect)
- [Decision Workflows](#decision-workflows)
  - [Database Selection](#database-selection)
  - [Architecture Pattern Selection](#architecture-pattern-selection)
  - [Monolith vs Microservices](#monolith-vs-microservices)
- [Tech Stack Coverage](#tech-stack-coverage)
- [Common Commands Reference](#common-commands-reference)

---

## Quick Start

bash
# Generate architecture diagram (Mermaid format)
python scripts/architecture_diagram_generator.py ./my-project --format mermaid

# Analyze dependencies for issues and vulnerabilities
python scripts/dependency_analyzer.py ./my-project --output json

# Get comprehensive architecture assessment
python scripts/project_architect.py ./my-project --verbose
---

## Tools

### 1. Architecture Diagram Generator

Parses project structure and generates visual architecture diagrams.

**When to use:** "I need to visualize my system architecture for documentation, stakeholder presentation, or team alignment"

**Input:** Project directory path  
**Output:** Diagram code in specified format

**Supported diagram types:**

| Type | Use Case | Description |
|------|----------|-------------|
| `component` | Module relationships | Shows modules, packages, and their dependencies |
| `layer` | Layered architecture | Presents architectural layers (UI, business, data) |
| `deployment` | Infrastructure | Shows deployment topology and infrastructure mapping |

**Usage:**

bash
# Mermaid format (default)
python scripts/architecture_diagram_generator.py ./project --format mermaid --type component

# PlantUML format
python scripts/architecture_diagram_generator.py ./project --format plantuml --type layer

# ASCII format (terminal output)
python scripts/architecture_diagram_generator.py ./project --format ascii --type deployment

# Custom output path
python scripts/architecture_diagram_generator.py ./project --output ./docs/diagrams/architecture.mmd
---

### 2. Dependency Analyzer

Analyzes project dependencies for security vulnerabilities, version conflicts, and maintenance issues.

**When to use:** "I need to audit my dependencies for security risks or understand coupling between modules"

**Checks performed:**
- Known security vulnerabilities (CVEs)
- Outdated packages with known issues
- Circular dependencies
- License compatibility
- Unused dependencies

**Output formats:** `json` (machine-readable), `html` (report), `table` (terminal)

bash
# JSON output for CI/CD integration
python scripts/dependency_analyzer.py ./my-project --output json

# HTML report for documentation
python scripts/dependency_analyzer.py ./my-project --output html --output-path ./reports/deps.html

# Focus on security issues only
python scripts/dependency_analyzer.py ./my-project --check security --severity high

# Check for circular dependencies
python scripts/dependency_analyzer.py ./my-project --check cycles
---

### 3. Project Architect

Provides comprehensive architecture assessment and recommendations for a project.

**When to use:** "I want an expert review of my current architecture or need guidance on architectural improvements"

**Assessment areas:**
- Architectural pattern identification
- Code organization evaluation
- Coupling and cohesion analysis
- Scalability concerns
- Technical debt assessment

bash
# Full verbose assessment
python scripts/project_architect.py ./my-project --verbose

# Specific focus areas
python scripts/project_architect.py ./my-project --focus scalability,maintainability

# Generate architecture decision records
python scripts/project_architect.py ./my-project --generate-adr --output ./docs/adr/
---

## Decision Workflows

### Database Selection

Use this workflow when asked "which database should I use?" or evaluating database options.

**Decision criteria:**

| Factor | SQL | NoSQL | Graph | Time-Series |
|--------|-----|-------|-------|-------------|
| **Data structure** | Structured, relational | Flexible, document | Connected data | Metrics, events |
| **Relationships** | Complex joins needed | Simple documents | Deep relationships | Sequential |
| **Scale** | Medium | High | Medium | Very high |
| **Transactions** | ACID required | Eventual OK | Varies | Append-only |
| **Examples** | PostgreSQL, MySQL | MongoDB, DynamoDB | Neo4j, Amazon Neptune | InfluxDB, TimescaleDB |

**Workflow:**
1. Analyze data model requirements
2. Identify query patterns
3. Evaluate consistency needs
4. Consider scale requirements
5. Review team expertise

---

### Architecture Pattern Selection

Choose the appropriate architectural pattern based on requirements.

| Pattern | Best For | Avoid When |
|---------|----------|------------|
| **Monolithic** | Small teams, MVPs, simple domains | Multiple teams, complex domains |
| **Modular Monolith** | Growing teams, clear boundaries | No clear domain boundaries |
| **Microservices** | Large teams, independent deployability | Small teams, tight consistency needs |
| **Event-Driven** | Real-time systems, loose coupling | Simple CRUD workflows |
| **Hexagonal (Ports/Adapters)** | Testability, framework independence | Rapid prototyping |

---

### Monolith vs Microservices

**Choose Monolith when:**
- Team size < 10 developers
- Rapid iteration is critical
- Domain boundaries are unclear
- Operations overhead is a concern
- Strong consistency required

**Choose Microservices when:**
- Team size > 10 with clear ownership
- Independent deployment is essential
- Different domains have different needs
- Scale requirements vary by component
- Organizational boundaries align with technical boundaries

**Migration path:** Consider Modular Monolith as an intermediate step.

---

## Tech Stack Coverage

**Languages:** Python, JavaScript/TypeScript, Java, Go, Rust, C#, Ruby, PHP

**Frameworks:**
- Web: Django, Flask, FastAPI, Express, Spring Boot, Rails, Laravel, ASP.NET Core
- Microservices: Kubernetes, Docker, Istio, Linkerd
- Serverless: AWS Lambda, Azure Functions, Google Cloud Functions

**Databases:**
- SQL: PostgreSQL, MySQL, MariaDB, SQL Server, Oracle
- NoSQL: MongoDB, Cassandra, DynamoDB, CouchDB
- Graph: Neo4j, Amazon Neptune, ArangoDB
- Cache: Redis, Memcached
- Search: Elasticsearch, Solr

**Infrastructure:** AWS, Azure, GCP, On-premises, Hybrid

**Messaging:** Apache Kafka, RabbitMQ, AWS SQS/SNS, Azure Service Bus

---

## Common Commands Reference

bash
# Architecture Diagram
python scripts/architecture_diagram_generator.py <path> --format <mermaid|plantuml|ascii> --type <component|layer|deployment>

# Dependency Analysis
python scripts/dependency_analyzer.py <path> --output <json|html|table> --check <security|cycles|licenses>

# Architecture Assessment
python scripts/project_architect.py <path> --verbose --focus <areas> --generate-adr

# Generate Architecture Decision Record
python scripts/adr_generator.py --decision "<title>" --context "<problem>" --decision "<choice>" --consequences "<outcome>"
---

## Pro Tips

1. **Start with diagrams** — Visualizing the current state reveals insights before proposing changes
2. **Document decisions** — Use ADRs to capture context and reasoning for future maintainers
3. **Analyze dependencies early** — Dependency issues compound over time
4. **Consider team topology** — Conway's Law applies; design systems that match organizational structure
5. **Plan for failure** — Architecture decisions should account for partial failures and graceful degradation