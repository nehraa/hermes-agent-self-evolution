---
category: software-development
name: senior-architect
description: This skill should be used when the user asks to "design system architecture", "evaluate microservices vs monolith", "create architecture diagrams", "analyze dependencies", "choose a database", "plan for scalability", "make technical decisions", or "review system design". Use for architecture decision records (ADRs), tech stack evaluation, system design reviews, dependency analysis, and generating architecture diagrams in Mermaid, PlantUML, or ASCII format.
---

# Senior Architect

Architecture design and analysis tools for making informed technical decisions.

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
- [Reference Documentation](#reference-documentation)
- [Tech Stack Coverage](#tech-stack-coverage)

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

## Tools

### 1. Architecture Diagram Generator

Generates architecture diagrams from project structure in multiple formats.

**Use when:** You need to visualize system architecture for documentation, team discussion, or technical planning.

**Supported formats:**
- `mermaid` — Default, web-friendly, renders in GitHub/GitLab
- `plantuml` — Enterprise-friendly, detailed diagrams
- `ascii` — Terminal output, text-based environments

**Supported diagram types:**

| Type | Purpose |
|------|---------|
| `component` | Shows modules and their relationships |
| `layer` | Shows architectural layers (presentation, business, data) |
| `deployment` | Shows deployment topology (servers, containers, cloud services) |
| `sequence` | Shows interaction flow between components |

**Usage:**

bash
# Mermaid component diagram
python scripts/architecture_diagram_generator.py ./project --format mermaid --type component

# PlantUML layer diagram
python scripts/architecture_diagram_generator.py ./project --format plantuml --type layer

# ASCII diagram for terminal
python scripts/architecture_diagram_generator.py ./project --format ascii --type component

# Save output to file
python scripts/architecture_diagram_generator.py ./project --format mermaid --output architecture.md
---

### 2. Dependency Analyzer

Analyzes project dependencies for security issues, version conflicts, and architectural problems.

**Use when:** You need to audit dependencies, identify circular dependencies, or assess maintenance burden.

**Output includes:**
- Dependency tree visualization
- Security vulnerability reports (CVEs)
- Circular dependency detection
- Outdated package identification
- License compatibility checks

**Usage:**

bash
# Analyze and output JSON
python scripts/dependency_analyzer.py ./my-project --output json

# Analyze with security focus
python scripts/dependency_analyzer.py ./my-project --check security

# Analyze with verbose output
python scripts/dependency_analyzer.py ./my-project --verbose

# Generate dependency graph
python scripts/dependency_analyzer.py ./my-project --graph
---

### 3. Project Architect

Provides comprehensive architecture assessment and recommendations for a project.

**Use when:** You need an initial architecture review or want automated recommendations.

**Assessment areas:**
- Current architecture pattern identification
- Scalability assessment
- Technology stack evaluation
- Coupling and cohesion analysis
- Recommended improvements

**Usage:**

bash
# Full architecture assessment
python scripts/project_architect.py ./my-project --verbose

# Quick assessment
python scripts/project_architect.py ./my-project

# Generate architecture decision record (ADR)
python scripts/project_architect.py ./my-project --generate-adr
---

## Decision Workflows

### Database Selection

Use this workflow when choosing a database for a project or service.

**Decision factors to consider:**

1. **Data model**
   - Structured/relational → PostgreSQL, MySQL
   - Document → MongoDB, CouchDB
   - Key-value → Redis, DynamoDB
   - Graph → Neo4j, Amazon Neptune
   - Time-series → InfluxDB, TimescaleDB

2. **Scale requirements**
   - Transaction volume (reads/sec, writes/sec)
   - Data volume and retention period
   - Horizontal vs vertical scaling needs

3. **Consistency requirements**
   - ACID compliance needed → Relational databases
   - Eventual consistency acceptable → NoSQL options

4. **Operational factors**
   - Team expertise
   - Managed service availability
   - Cost structure

**Generate database comparison:**

bash
python scripts/project_architect.py --database-comparison --requirements ./requirements.yaml
---

### Architecture Pattern Selection

Use this workflow when selecting an architectural pattern for a system.

**Common patterns with use cases:**

| Pattern | Best For | Avoid When |
|---------|----------|------------|
| Monolithic | Small teams, MVPs, simple domains | Large teams, complex domains, frequent deploys needed |
| Modular Monolith | Growing teams, bounded contexts emerging | Very large scale, strict team isolation required |
| Microservices | Large teams, independent deployability, polyglot needs | Small teams, simple domains, network latency sensitive |
| Event-Driven | Real-time processing, async workflows, loose coupling | Simple request-response, strict consistency needed |
| Serverless | Variable load, burst traffic, minimal ops | Consistent high load, cold start sensitive |

**Generate pattern recommendation:**

bash
python scripts/project_architect.py --pattern-recommendation --team-size 5 --domain-complexity high --deployment-frequency daily
---

### Monolith vs Microservices

Use this workflow when evaluating monolith vs microservices for a project.

**Favor Monolith when:**
- Team size ≤ 10 developers
- Domain is simple or not well-understood
- Rapid prototyping is priority
- Deployment pipeline is not mature
- Traffic patterns are predictable

**Favor Microservices when:**
- Team size ≥ 20 developers with clear ownership
- Domain is well-bounded and understood
- Independent deployability is required
- Different services need different tech stacks
- Organization has DevOps maturity

**Incremental migration path:**
1. Build modular monolith first
2. Identify bounded contexts
3. Define service contracts (APIs)
4. Extract highest-value service first
5. Repeat for next bounded context

**Generate migration assessment:**

bash
python scripts/project_architect.py ./my-monolith --microservices-evaluation
---

## Reference Documentation

### Architecture Decision Records (ADRs)

ADRs document significant architectural decisions. Each ADR should include:

1. **Title** — Brief description of the decision
2. **Status** — Proposed, Accepted, Deprecated, Superseded
3. **Context** — The situation and requirements
4. **Decision** — The chosen approach
5. **Consequences** — Benefits and drawbacks

**Generate ADR template:**

bash
python scripts/project_architect.py --adr-template "database-selection"
### Common Architecture Diagrams

**Component Diagram:**
┌─────────────────────────────────────────────────────┐
│                  Presentation Layer                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │   Web UI    │  │  Mobile App │  │    API      │  │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  │
└─────────┼────────────────┼────────────────┼─────────┘
          │                │                │
          ▼                ▼                ▼
┌─────────────────────────────────────────────────────┐
│                   Service Layer                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │   User      │  │   Order     │  │  Payment    │  │
│  │   Service   │  │   Service   │  │   Service   │  │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  │
└─────────┼────────────────┼────────────────┼─────────┘
          │                │                │
          ▼                ▼                ▼
┌─────────────────────────────────────────────────────┐
│                    Data Layer                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │Users DB  │  │Orders DB │  │Payments DB│          │
│  └──────────┘  └──────────┘  └──────────┘          │
└─────────────────────────────────────────────────────┘
---

## Tech Stack Coverage

### Languages & Frameworks
- **Backend:** Node.js, Python, Go, Java, .NET, Ruby, Rust
- **Frontend:** React, Vue, Angular, Svelte, Next.js, Nuxt.js
- **Mobile:** React Native, Flutter, Swift, Kotlin

### Databases
- **Relational:** PostgreSQL, MySQL, MariaDB, SQLite
- **NoSQL:** MongoDB, Cassandra, DynamoDB, Couchbase
- **Cache:** Redis, Memcached
- **Search:** Elasticsearch, Solr
- **Graph:** Neo4j, Amazon Neptune

### Infrastructure
- **Containers:** Docker, Kubernetes, Helm
- **Cloud:** AWS, Azure, GCP
- **CI/CD:** GitHub Actions, GitLab CI, Jenkins, ArgoCD
- **Monitoring:** Prometheus, Grafana, Datadog, New Relic

### Message Systems
- **Brokers:** RabbitMQ, Apache Kafka, Amazon SQS, NATS
- **Patterns:** Pub/Sub, Point-to-Point, Event Streaming

---

## Common Commands

bash
# Architecture Analysis
python scripts/project_architect.py ./project --full-assessment
python scripts/project_architect.py ./project --generate-adr

# Diagram Generation
python scripts/architecture_diagram_generator.py ./project --format mermaid --type component
python scripts/architecture_diagram_generator.py ./project --format plantuml --type deployment

# Dependency Analysis
python scripts/dependency_analyzer.py ./project --check security
python scripts/dependency_analyzer.py ./project --check outdated
python scripts/dependency_analyzer.py ./project --check circular

# Decision Support
python scripts/project_architect.py --database-comparison --requirements ./reqs.yaml
python scripts/project_architect.py --pattern-recommendation --team-size 10 --domain-complexity medium
python scripts/project_architect.py ./monolith --microservices-evaluation