---
category: software-development
name: senior-architect
description: "Design system architecture, evaluate microservices vs monolith, create architecture diagrams, analyze dependencies, choose a database, plan for scalability, make technical decisions, or review system design. Use for architecture decision records (ADRs), tech stack evaluation, system design reviews, dependency analysis, and generating architecture diagrams in Mermaid, PlantUML, or ASCII format."
---

# Senior Architect

Architecture design and analysis tools for making informed technical decisions.

## Table of Contents

- [Quick Start](#quick-start)
- [Tools Overview](#tools-overview)
- [Decision Workflows](#decision-workflows)
- [Reference Documentation](#reference-documentation)
- [Tech Stack Coverage](#tech-stack-coverage)
- [Common Commands](#common-commands)

---

## Quick Start

bash
# Generate architecture diagram from project
python scripts/architecture_diagram_generator.py ./my-project --format mermaid

# Analyze dependencies for issues
python scripts/dependency_analyzer.py ./my-project --output json

# Get architecture assessment
python scripts/project_architect.py ./my-project --verbose
---

## Tools Overview

### 1. Architecture Diagram Generator

Generates architecture diagrams from project structure in multiple formats.

**Solves:** "I need to visualize my system architecture for documentation or team discussion"

| Parameter | Description | Default |
|-----------|-------------|---------|
| `path` | Project directory path | Required |
| `--format` | Output format: `mermaid`, `plantuml`, `ascii` | `mermaid` |
| `--type` | Diagram type: `component`, `layer`, `deployment` | `component` |

**Supported diagram types:**

- `component` — Shows modules and their relationships (recommended for most use cases)
- `layer` — Shows architectural layers (presentation, business, data)
- `deployment` — Shows deployment topology and infrastructure

**Usage:**

bash
# Mermaid format (default)
python scripts/architecture_diagram_generator.py ./project --format mermaid --type component

# PlantUML format
python scripts/architecture_diagram_generator.py ./project --format plantuml --type layer

# ASCII format (terminal-friendly output)
python scripts/architecture_diagram_generator.py ./project --format ascii --type deployment
---

### 2. Dependency Analyzer

Scans project dependencies for security vulnerabilities, version conflicts, and circular dependencies.

**Solves:** "I need to understand what's in my dependency tree and identify risks"

| Parameter | Description | Default |
|-----------|-------------|---------|
| `path` | Project directory path | Required |
| `--output` | Output format: `json`, `text`, `html` | `text` |
| `--depth` | Analysis depth for nested dependencies | `3` |

**Detects:**

- Known security vulnerabilities (CVEs)
- Outdated dependencies with known issues
- Circular dependency chains
- License compliance issues
- Unused dependencies

**Usage:**

bash
# Basic analysis
python scripts/dependency_analyzer.py ./my-project

# JSON output for automation
python scripts/dependency_analyzer.py ./my-project --output json

# Deep analysis with increased depth
python scripts/dependency_analyzer.py ./my-project --depth 5 --output html
---

### 3. Project Architect

Provides comprehensive architecture assessment and recommendations for a project.

**Solves:** "I need an expert review of my current architecture"

**Output includes:**

- Architecture pattern identification (monolith, microservices, event-driven, etc.)
- Strengths and weaknesses assessment
- Scalability concerns and recommendations
- Technical debt analysis
- Improvement suggestions with priority levels

**Usage:**

bash
# Standard assessment
python scripts/project_architect.py ./my-project

# Detailed output
python scripts/project_architect.py ./my-project --verbose

# Generate report
python scripts/project_architect.py ./my-project --report ./architecture-review.md
---

## Decision Workflows

### Database Selection Workflow

Use when choosing a database for a new project or migration.

**Decision factors:**

1. **Data structure**: Structured (SQL) vs. Semi-structured (NoSQL) vs. Graph (GraphDB)
2. **Scale requirements**: Transactions per second, data volume, horizontal scaling needs
3. **Consistency requirements**: ACID compliance vs. eventual consistency
4. **Query patterns**: Complex joins vs. simple key-value lookups vs. full-text search
5. **Operational complexity**: Managed service vs. self-hosted considerations

**Common scenarios:**

| Scenario | Recommended Type | Examples |
|----------|-------------------|----------|
| Complex relationships, transactions | Relational | PostgreSQL, MySQL |
| High write throughput, simple queries | Wide-column | Cassandra, DynamoDB |
| Flexible schema, fast iteration | Document | MongoDB, CouchDB |
| Network/graph relationships | Graph | Neo4j, Amazon Neptune |
| Cache and session storage | Key-Value | Redis, Memcached |
| Time-series data | Time-series | InfluxDB, TimescaleDB |

---

### Architecture Pattern Selection Workflow

Use when designing system architecture from scratch or refactoring existing systems.

**Patterns covered:**

| Pattern | Best For | Avoid When |
|---------|----------|------------|
| Monolithic | Small teams, MVPs, simple domains | Large teams, complex domains, frequent scaling |
| Modular Monolith | Medium complexity, team autonomy needs | Full microservices overhead unjustified |
| Microservices | Large teams, independent deployability | Small teams, tight latency requirements |
| Event-Driven | Async processing, real-time updates | Simple CRUD workflows |
| Serverless | Variable load, bursty traffic | Consistent high-throughput workloads |

**Evaluation criteria:**

1. Team size and distribution
2. Domain complexity and boundaries
3. Scalability requirements (current and projected)
4. Operational maturity and tooling
5. Deployment frequency needs

---

### Monolith vs. Microservices Decision

Use when evaluating whether to split or merge services.

**Consider microservices when:**

- Team size exceeds 10-12 engineers on a single service
- Distinct domain boundaries exist with minimal coupling
- Independent deployment cycles are required
- Different scalability characteristics exist per domain
- Technology diversity is justified by domain needs

**Stick with monolith (or modular monolith) when:**

- Team is small (fewer than 5-8 engineers)
- Domain boundaries are unclear or tightly coupled
- Operational complexity would exceed team capacity
- Early-stage product with evolving requirements
- Latency between services is unacceptable

**Hybrid approach:** Consider strangler fig pattern for gradual migration.

---

## Reference Documentation

### Architecture Decision Records (ADRs)

Structure for documenting significant architectural decisions:

markdown
# ADR-001: Database Selection

## Status
Accepted

## Context
Project requires persistence layer for user data with following requirements:
- 10,000 concurrent users
- Complex query patterns
- ACID compliance required

## Decision
PostgreSQL 15 with read replicas

## Consequences
- Positive: ACID compliance, mature ecosystem, excellent tooling
- Negative: Requires schema migrations, vertical scaling limits

## Alternatives Considered
- MongoDB: Rejected due to eventual consistency requirements
- MySQL: Rejected due to JSON support limitations
---

## Tech Stack Coverage

### Languages Supported

- JavaScript/TypeScript (Node.js)
- Python
- Java/Kotlin
- Go
- Rust
- C#/.NET

### Frameworks & Patterns

- RESTful APIs
- GraphQL
- gRPC
- Event-driven (Kafka, RabbitMQ, SQS)
- Serverless (AWS Lambda, Azure Functions, Cloud Functions)

### Infrastructure

- Containers (Docker, Podman)
- Orchestration (Kubernetes, Docker Swarm)
- Cloud providers (AWS, Azure, GCP)
- IaC tools (Terraform, Pulumi, CloudFormation)

---

## Common Commands

bash
# Generate component diagram
python scripts/architecture_diagram_generator.py ./src --format mermaid --type component

# Generate layer diagram
python scripts/architecture_diagram_generator.py ./src --format mermaid --type layer

# Analyze dependencies
python scripts/dependency_analyzer.py ./project --output json > deps-report.json

# Full architecture review
python scripts/project_architect.py ./project --verbose --report review.md

# Generate deployment diagram
python scripts/architecture_diagram_generator.py ./infra --format plantuml --type deployment