---
category: software-development
name: senior-architect
description: This skill should be used when the user asks to "design system architecture", "evaluate microservices vs monolith", "create architecture diagrams", "analyze dependencies", "choose a database", "plan for scalability", "make technical decisions", or "review system design". Use for architecture decision records (ADRs), tech stack evaluation, system design reviews, dependency analysis, and generating architecture diagrams in Mermaid, PlantUML, or ASCII format.
---

# Senior Architect

Architecture design and analysis tools for making informed technical decisions.

## Table of Contents

- [Quick Start](#quick-start)
- [Tools Overview](#tools-overview)
  - [Architecture Diagram Generator](#1-architecture-diagram-generator)
  - [Dependency Analyzer](#2-dependency-analyzer)
  - [Project Architect](#3-project-architect)
- [Decision Workflows](#decision-workflows)
  - [Database Selection](#database-selection-workflow)
  - [Architecture Pattern Selection](#architecture-pattern-selection-workflow)
  - [Monolith vs Microservices](#monolith-vs-microservices-decision)
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

**Input:** Project directory path
**Output:** Diagram code (Mermaid, PlantUML, or ASCII)

**Supported diagram types:**

| Type | Use Case | Description |
|------|----------|-------------|
| `component` | Module relationships | Shows modules and their dependencies |
| `layer` | Layered architecture | Displays presentation, business, and data layers |
| `deployment` | Infrastructure | Shows deployment topology and infrastructure |
| `sequence` | Flow analysis | Documents API request/response flows |
| `class` | Data models | Shows entity relationships and data structures |

**Usage:**

bash
# Generate component diagram in Mermaid (default)
python scripts/architecture_diagram_generator.py ./project --format mermaid --type component

# Generate layered diagram in PlantUML
python scripts/architecture_diagram_generator.py ./project --format plantuml --type layer

# Generate deployment diagram in ASCII (terminal-friendly)
python scripts/architecture_diagram_generator.py ./project --format ascii --type deployment

# Include specific directories only
python scripts/architecture_diagram_generator.py ./project --include src,lib --exclude test

# Save output to file
python scripts/architecture_diagram_generator.py ./project --output ./docs/architecture.mmd
**Output Example (Mermaid):**

mermaid
graph TB
    subgraph Frontend
        UI[React App]
        State[State Management]
    end
    subgraph Backend
        API[REST API]
        Service[Business Logic]
        DB[(Database)]
    end
    UI --> API
    API --> Service
    Service --> DB
---

### 2. Dependency Analyzer

Analyzes project dependencies for security vulnerabilities, version conflicts, and architectural issues.

**Solves:** "I need to audit my dependencies or understand coupling between modules"

**Input:** Project directory or dependency manifest
**Output:** JSON, CSV, or formatted report

**Capabilities:**

- **Security scanning**: Identifies known CVEs in dependencies
- **Version analysis**: Detects outdated or conflicting versions
- **Circular dependency detection**: Finds problematic circular imports
- **Unused dependency detection**: Identifies packages not referenced in code
- **License compliance**: Flags problematic open-source licenses
- **Architecture conformance**: Validates against defined architecture rules

**Usage:**

bash
# Full dependency analysis with JSON output
python scripts/dependency_analyzer.py ./project --output json

# Security-focused scan
python scripts/dependency_analyzer.py ./project --focus security --severity high,critical

# Check for circular dependencies only
python scripts/dependency_analyzer.py ./project --check circular

# Generate HTML report
python scripts/dependency_analyzer.py ./project --output html --report ./deps-report.html

# Analyze specific package manager (npm, pip, maven, gradle)
python scripts/dependency_analyzer.py ./project --package-manager npm
**Output Example:**

json
{
  "summary": {
    "total_dependencies": 142,
    "vulnerable": 3,
    "outdated": 18,
    "circular_deps": 1,
    "unused": 5
  },
  "critical_issues": [
    {
      "package": "lodash",
      "version": "4.17.15",
      "cve": "CVE-2021-23337",
      "severity": "high"
    }
  ]
}
---

### 3. Project Architect

Provides comprehensive architecture assessment and recommendations for existing projects.

**Solves:** "I need to understand the current architecture or get modernization recommendations"

**Input:** Project directory path
**Output:** Assessment report with findings and recommendations

**Assessment Areas:**

| Area | What It Checks |
|------|----------------|
| **Structure** | Directory organization, module boundaries, naming conventions |
| **Coupling** | Inter-module dependencies, circular references, tight coupling |
| **Cohesion** | Module organization, single responsibility principle adherence |
| **Scalability** | Horizontal/vertical scaling readiness, stateless design |
| **Observability** | Logging, monitoring, tracing infrastructure |
| **Resilience** | Error handling, retry logic, circuit breakers |
| **Security** | Authentication, authorization, data protection patterns |

**Usage:**

bash
# Full architecture assessment
python scripts/project_architect.py ./project --verbose

# Quick scan (faster, less detailed)
python scripts/project_architect.py ./project --quick

# Focus on specific area
python scripts/project_architect.py ./project --focus scalability

# Compare against reference architecture
python scripts/project_architect.py ./project --reference microservices

# Generate actionable recommendations
python scripts/project_architect.py ./project --recommendations
---

## Decision Workflows

### Database Selection Workflow

Use this workflow when asked "which database should I use?" or "what's the best database for X?"

**Decision Tree:**

┌─────────────────┐
                    │ Need ACID?      │
                    │ (Transactions)  │
                    └────────┬────────┘
                             │
              ┌──────────────┴──────────────┐
              │ NO                          │ YES
              ▼                             ▼
    ┌─────────────────┐           ┌─────────────────┐
    │ High volume?    │           │ Need horizontal │
    │ Millions+ rows  │           │ scaling?        │
    └────────┬────────┘           └────────┬────────┘
             │                             │
    ┌────────┴────────┐           ┌────────┴────────┐
    │ NO              │ YES       │ NO              │ YES
    ▼                 ▼           ▼                 ▼
┌────────┐     ┌──────────┐ ┌────────┐      ┌──────────────┐
│SQLite  │     │Cassandra │ │Postgre │      │NewSQL        │
│MySQL   │     │DynamoDB  │ │SQL     │      │(CockroachDB) │
└────────┘     └──────────┘ └────────┘      └──────────────┘
**Database Selection Matrix:**

| Use Case | Primary Choice | Alternatives | Avoid |
|----------|---------------|---------------|-------|
| Transactional (OLTP) | PostgreSQL | MySQL, CockroachDB | MongoDB, Redis |
| Analytical (OLAP) | ClickHouse | BigQuery, Snowflake | PostgreSQL |
| Caching | Redis | Memcached | PostgreSQL |
| Search | Elasticsearch | OpenSearch, Meilisearch | PostgreSQL (for large) |
| Time-series | InfluxDB | TimescaleDB | MySQL |
| Graph relationships | Neo4j | Amazon Neptune | PostgreSQL |
| Document storage | MongoDB | PostgreSQL (JSONB) | MySQL |
| Key-value | Redis | DynamoDB | PostgreSQL |
| Object storage | S3 | MinIO | PostgreSQL |

**When to recommend each:**

| Question | Answer | Recommendation |
|----------|--------|----------------|
| Need complex joins? | Yes | PostgreSQL, MySQL |
| Need horizontal scaling? | Yes | CockroachDB, Cassandra, DynamoDB |
| Schema changing frequently? | Yes | MongoDB, PostgreSQL (JSONB) |
| Need full-text search? | Yes | Elasticsearch, PostgreSQL (tsvector) |
| 80%+ reads? | Yes | Redis (cache layer) |
| Time-series data? | Yes | InfluxDB, TimescaleDB |

---

### Architecture Pattern Selection Workflow

Use this workflow for "which architecture pattern should I use?" questions.

**Pattern Comparison:**

| Pattern | Best For | Complexity | Team Size | Time to Market |
|---------|----------|------------|-----------|----------------|
| **Monolith** | Small teams, MVPs, simple domains | Low | 1-10 | Fast |
| **Modular Monolith** | Growing teams, clear domains | Medium | 5-20 | Medium |
| **SOA** | Enterprise, legacy modernization | High | 20+ | Slow |
| **Microservices** | Scale, multiple teams, polyglot | Very High | 30+ | Slow |
| **Event-Driven** | Real-time, async processing | High | 10+ | Medium |
| **Serverless** | Variable load, cost optimization | Medium | 1-15 | Fast |

**Selection Criteria:**

┌─────────────────────────────────────────────────────────────────┐
│                    ARCHITECTURE PATTERN SELECTION                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Team Size              │  Recommendation                       │
│  ──────────────────────────────────────────────────────────────  │
│  1-5 developers         │  Monolith                             │
│  5-15 developers        │  Modular Monolith                     │
│  15-30 developers       │  Modular Monolith → Microservices     │
│  30+ developers         │  Microservices or Micro-frontends     │
│                                                                  │
│  ─────────────────────────────────────────────────────────────── │
│                                                                  │
│  Deployment Frequency   │  Recommendation                       │
│  ──────────────────────────────────────────────────────────────  │
│  Weekly or less         │  Monolith                             │
│  Daily                  │  Modular Monolith                     │
│  Multiple times/day     │  Microservices                        │
│  Continuous (CI/CD)     │  Microservices + Feature Flags        │
│                                                                  │
│  ─────────────────────────────────────────────────────────────── │
│                                                                  │
│  Domain Complexity      │  Recommendation                       │
│  ──────────────────────────────────────────────────────────────  │
│  Single bounded context │  Monolith                             │
│  Few bounded contexts   │  Modular Monolith                     │
│  Many bounded contexts  │  Microservices                        │
│  Independent scaling    │  Microservices                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
**Pattern Characteristics:**

| Pattern | Pros | Cons | Migration Path |
|---------|------|------|----------------|
| Monolith | Simple, fast, easy debugging | Hard to scale, tightly coupled | → Modular Monolith |
| Modular Monolith | Domain isolation, easy migration | Requires discipline | → Services per module |
| Microservices | Independent deploy, polyglot | Complexity, observability needed | Incremental extraction |
| Event-Driven | Loose coupling, async capable | Eventual consistency, tracing | Add events to monolith |

---

### Monolith vs Microservices Decision

Use this workflow when asked "monolith or microservices?" or "should I break apart my monolith?"

**Decision Framework:**

┌──────────────────────────────────────────────────────────────────┐
│                    START HERE                                     │
│                    Should I use Microservices?                    │
└──────────────────────────────┬───────────────────────────────────┘
                               │
           ┌───────────────────┴───────────────────┐
           │                                       │
           ▼                                       ▼
    ┌──────────────┐                       ┌──────────────┐
    │ Team < 10?   │                       │ Team >= 10?  │
    └──────┬───────┘                       └──────┬───────┘
           │                                      │
     ┌─────┴─────┐                          ┌─────┴─────┐
     │ YES       │                          │ YES       │
     ▼           ▼                          ▼           ▼
┌─────────┐  ┌───────────┐           ┌──────────┐  ┌──────────────┐
│Monolith │  │ Need      │           │ Have     │  │ Can handle   │
│Recommended│ │ independent│           │ DevOps   │  │ distributed  │
│         │  │ scaling?  │           │ maturity? │  │ tracing?    │
└────┬────┘  └─────┬─────┘           └────┬─────┘  └──────┬───────┘
     │             │                       │               │
     │        ┌────┴────┐                  │          ┌────┴────┐
     │        │ YES     │                  │          │ YES     │
     │        ▼         ▼                  │          ▼         ▼
     │   ┌─────────┐ ┌─────────┐           │     ┌─────────┐ ┌─────────┐
     │   │Micro-   │ │Modular  │           │     │Micro-   │ │ Consider │
     │   │services │ │Monolith │           │     │services │ │ maturity │
     │   └─────────┘ └─────────┘           │     └─────────┘ └─────────┘
     │                                    │          │
     │                                    │          ▼
     │                                    │   ┌─────────────────┐
     │                                    │   │ Microservices   │
     │                                    │   │ if team ready   │
     └────────────────────────────────────┴───└─────────────────┘
**Microservices Readiness Checklist:**

| Category | Requirement | Weight |
|----------|-------------|--------|
| **Team** | Dedicated DevOps/SRE team | Required |
| **Team** | Team autonomy for deployments | Required |
| **Team** | Clear bounded contexts | Required |
| **Infrastructure** | Container orchestration (K8s) | High |
| **Infrastructure** | Service mesh capability | High |
| **Observability** | Distributed tracing | Required |
| **Observability** | Centralized logging | Required |
| **Observability** | Metrics and alerting | Required |
| **Processes** | CI/CD for each service | Required |
| **Processes** | API versioning strategy | High |
| **Resilience** | Circuit breaker patterns | Required |
| **Resilience** | Graceful degradation | Required |

**Start with monolith if:**
- Team is fewer than 10 developers
- Building an MVP or validating product-market fit
- Domain boundaries are not yet clear
- No dedicated DevOps team
- Budget/resources are limited
- First-time architecture for the domain

**Consider microservices when:**
- Team exceeds 10-15 developers
- Multiple independent product areas
- Need independent scaling of components
- Different teams own different domains
- Polyglot persistence is needed
- Organizational structure supports Conway's Law

**Extraction Strategy (from Monolith to Microservices):**

1. **Strangler Fig Pattern** - Incrementally replace functionality
2. **Identify seams** - Find natural bounded contexts
3. **Start with data** - Separate database first
4. **Extract read models** - Start with read replicas
5. **Move writes last** - Critical path for transactions

---

## Reference Documentation

### Architecture Decision Records (ADRs)

Generate ADRs using the standard format:

bash
# Create new ADR
python scripts/adr_tool.py new "Use PostgreSQL as primary database"

# List existing ADRs
python scripts/adr_tool.py list ./docs/adr

# Export ADR to markdown
python scripts/adr_tool.py export ./docs/adr/001-postgresql-decision.md
**ADR Template Structure:**

markdown
# ADR-001: Database Selection

## Status
Accepted

## Context
We need to select a primary database for our application that handles
transactional data with complex joins and requires ACID compliance.

## Decision
We will use PostgreSQL as our primary database.

## Consequences
### Positive
- ACID compliance for transactions
- Complex query support with JOINs
- Mature ecosystem and community

### Negative
- Horizontal scaling complexity
- Requires operational expertise

## Alternatives Considered
- MySQL: Less mature JSON support
- MongoDB: Insufficient for complex joins
### Tech Stack Evaluation Template

| Category | Option A | Option B | Option C | Winner |
|----------|----------|----------|----------|--------|
| **Language** | Node.js | Python | Go | TBD |
| **Framework** | Express | FastAPI | Gin | TBD |
| **Database** | PostgreSQL | MySQL | MongoDB | TBD |
| **Cache** | Redis | Memcached | No cache | TBD |
| **Queue** | RabbitMQ | Kafka | SQS | TBD |
| **Container** | Docker | Podman | None | TBD |

### System Quality Attributes Matrix

| Attribute | Definition | Measurement | Target |
|-----------|------------|-------------|--------|
| **Availability** | Uptime percentage | (Total - Downtime) / Total | 99.9% |
| **Latency** | Response time | P50, P95, P99 | P99 < 200ms |
| **Throughput** | Requests per second | RPS capacity | 1000 RPS |
| **Scalability** | Scaling factor | Auto-scaling trigger rate | 2x on load |
| **MTTR** | Mean time to recovery | Incident duration average | < 1 hour |
| **MTBF** | Mean time between failures | Uptime incidents | > 30 days |

---

## Tech Stack Coverage

### Supported Languages and Frameworks

| Language | Frameworks | Package Managers |
|----------|------------|------------------|
| **JavaScript/TypeScript** | Node.js, Express, NestJS, Next.js | npm, yarn, pnpm |
| **Python** | Django, Flask, FastAPI | pip, poetry |
| **Java** | Spring Boot, Micronaut | Maven, Gradle |
| **Go** | Gin, Echo, Fiber | go modules |
| **Rust** | Actix, Rocket | Cargo |
| **C#/.NET** | ASP.NET Core | NuGet |
| **Ruby** | Rails, Sinatra | Bundler |
| **PHP** | Laravel, Symfony | Composer |

### Supported Diagram Formats

| Format | Best For | Tool Support |
|--------|----------|--------------|
| **Mermaid** | GitHub, GitLab, Markdown docs | All diagram types |
| **PlantUML** | Enterprise docs, complex diagrams | UML diagrams |
| **ASCII** | Terminal, quick sketches | Component only |
| **DOT/Graphviz** | Complex graphs | Dependency analysis |
| **draw.io** | Interactive editing | Export to multiple formats |

### Supported Databases

| Category | Databases |
|----------|-----------|
| **Relational** | PostgreSQL, MySQL, MariaDB, SQLite |
| **NoSQL Document** | MongoDB, CouchDB |
| **NoSQL Key-Value** | Redis, DynamoDB, Cassandra |
| **NoSQL Graph** | Neo4j, Amazon Neptune |
| **Time-series** | InfluxDB, TimescaleDB, Prometheus |
| **Search** | Elasticsearch, OpenSearch |
| **Data Warehouse** | BigQuery, Snowflake, Redshift |
| **NewSQL** | CockroachDB, TiDB |

### Supported Cloud Platforms

| Provider | Services Covered |
|----------|-----------------|
| **AWS** | EC2, ECS, EKS, Lambda, RDS, DynamoDB, S3, SQS, SNS, API Gateway |
| **GCP** | Compute, GKE, Cloud Run, Cloud SQL, BigQuery, Pub/Sub |
| **Azure** | VMs, AKS, App Service, Azure SQL, Cosmos DB |
| **Multi-cloud** | Terraform support, Pulumi cross-cloud |

---

## Common Commands

### Generate Architecture Diagram

bash
# Basic component diagram
python scripts/architecture_diagram_generator.py ./project

# Layer diagram with specific output
python scripts/architecture_diagram_generator.py ./project --format plantuml --type layer --output diagram.puml

# Deployment diagram for Kubernetes
python scripts/architecture_diagram_generator.py ./project --format mermaid --type deployment --runtime k8s

# Generate sequence diagram for specific endpoint
python scripts/architecture_diagram_generator.py ./project --type sequence --endpoint /api/users
### Analyze Dependencies

bash
# Full security audit
python scripts/dependency_analyzer.py ./project --focus security --format html --output report.html

# Find circular dependencies
python scripts/dependency_analyzer.py ./project --check circular --verbose

# Check specific language ecosystem
python scripts/dependency_analyzer.py ./project --package-manager pip --check outdated

# Export to SARIF (Security)
python scripts/dependency_analyzer.py ./project --format sarif --output results.sarif
### Project Architecture Assessment

bash
# Full assessment with recommendations
python scripts/project_architect.py ./project --full --recommendations

# Quick health check
python scripts/project_architect.py ./project --quick --output health.json

# Compare against microservices reference
python scripts/project_architect.py ./project --reference microservices --gaps

# Generate migration roadmap
python scripts/project_architect.py ./project --roadmap --timeline 6months
### Architecture Decision Records

bash
# Create new ADR with template
python scripts/adr_tool.py create "Microservices Adoption" --context ./project

# List all ADRs
python scripts/adr_tool.py list --directory ./docs/adr

# Update ADR status
python scripts/adr_tool.py update ./docs/adr/001-postgresql.md --status deprecated

# Generate ADR index
python scripts/adr_tool.py index ./docs/adr --output index.md
### Generate Tech Stack Report

bash
# Full technology audit
python scripts/tech_stack_analyzer.py ./project --report

# Compare against industry best practices
python scripts/tech_stack_analyzer.py ./project --benchmark --output benchmark.json

# License compliance report
python scripts/tech_stack_analyzer.py ./project --licenses
---

## Best Practices

### Architecture Documentation

1. **Keep diagrams updated** - Update on every architectural change
2. **Use consistent notation** - Stick to one diagram format per context
3. **Document decisions** - Use ADRs for all significant choices
4. **Include context** - Explain why, not just what
5. **Version diagrams** - Track changes over time

### Dependency Management

1. **Pin versions in production** - Use exact versions or lockfiles
2. **Audit regularly** - Schedule monthly security reviews
3. **Remove unused dependencies** - Clean up periodically
4. **Monitor transitive dependencies** - Don't ignore indirect deps
5. **Plan for upgrades** - Don't let deps fall too far behind

### Architecture Reviews

1. **Review early** - Engage architect in design phase
2. **Document non-obvious choices** - Future maintainers will thank you
3. **Consider operational costs** - Complexity has a price
4. **Plan for failure** - Assume components will fail
5. **Measure, don't guess** - Use metrics to validate decisions