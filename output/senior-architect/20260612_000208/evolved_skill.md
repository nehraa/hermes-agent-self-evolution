---
category: software-development
description: 'Design system architecture, evaluate architectural patterns, analyze dependencies, choose databases, plan scalability, and make technical decisions. Use for architecture decision records (ADRs), tech stack evaluation, system design reviews, dependency analysis, and generating architecture diagrams.'
name: senior-architect
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
- [Architecture Decision Records](#architecture-decision-records)
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

| Type | Description | Use Case |
|------|-------------|----------|
| `component` | Shows modules and their relationships | Internal architecture overview |
| `layer` | Shows architectural layers (presentation, business, data) | Layered architecture documentation |
| `deployment` | Shows deployment topology | Infrastructure and DevOps planning |
| `sequence` | Shows interaction flow between components | API and service communication |
| `class` | Shows data models and relationships | Domain modeling |

**Usage:**

bash
# Mermaid format (default)
python scripts/architecture_diagram_generator.py ./project --format mermaid --type component

# PlantUML format
python scripts/architecture_diagram_generator.py ./project --format plantuml --type layer

# ASCII format (terminal-friendly)
python scripts/architecture_diagram_generator.py ./project --format ascii --type deployment

# Output to file
python scripts/architecture_diagram_generator.py ./project --format mermaid --output architecture.mmd
**Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `--format` | Output format: `mermaid`, `plantuml`, `ascii` | `mermaid` |
| `--type` | Diagram type: `component`, `layer`, `deployment`, `sequence`, `class` | `component` |
| `--output` | Output file path | stdout |
| `--depth` | Directory depth to traverse | 5 |
| `--exclude` | Patterns to exclude (comma-separated) | `node_modules,dist,build,.git` |

---

### 2. Dependency Analyzer

Analyzes project dependencies for security vulnerabilities, version conflicts, and architectural issues.

**Solves:** "I need to audit my dependencies for security risks and architectural problems"

**Input:** Project directory path or lock file  
**Output:** JSON or HTML report

**Checks performed:**

- Security vulnerabilities (CVEs)
- Outdated packages
- License compatibility
- Circular dependencies
- Unused dependencies
- Duplicate dependencies
- Deprecated packages

**Usage:**

bash
# Full dependency analysis
python scripts/dependency_analyzer.py ./my-project --output json

# Security-focused scan
python scripts/dependency_analyzer.py ./my-project --check security --output json

# HTML report for review
python scripts/dependency_analyzer.py ./my-project --output html --report ./deps-report.html

# Check specific lock file
python scripts/dependency_analyzer.py --lockfile ./package-lock.json --output json
**Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `--output` | Output format: `json`, `html`, `table` | `table` |
| `--check` | Check type: `all`, `security`, `licenses`, `versions`, `circular` | `all` |
| `--fail-on` | Exit code on findings: `critical`, `high`, `medium`, `none` | `critical` |
| `--ignore` | Package patterns to ignore (comma-separated) | none |

---

### 3. Project Architect

Provides comprehensive architecture assessment and recommendations for a project.

**Solves:** "I need an expert review of my project's architecture"

**Input:** Project directory path  
**Output:** Assessment report with recommendations

**Assessment areas:**

- Project structure and organization
- Technology stack evaluation
- Scalability concerns
- Maintainability metrics
- Code quality indicators
- Security posture
- Performance bottlenecks

**Usage:**

bash
# Full architecture assessment
python scripts/project_architect.py ./my-project --verbose

# Quick assessment
python scripts/project_architect.py ./my-project

# Generate recommendations report
python scripts/project_architect.py ./my-project --recommendations --output ./arch-report.md
**Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `--verbose` | Include detailed analysis | false |
| `--recommendations` | Generate actionable recommendations | false |
| `--output` | Output file path | stdout |
| `--format` | Output format: `markdown`, `json`, `html` | `markdown` |

---

## Decision Workflows

### Database Selection Workflow

Use this workflow when asked: "Which database should I use?", "SQL vs NoSQL?", "What database for [specific use case]?"

**Step 1: Identify Data Characteristics**

| Characteristic | Questions to Ask | Considerations |
|----------------|------------------|----------------|
| Structure | Is data highly structured or flexible? | SQL for structured, NoSQL for flexible |
| Volume | What's the expected data size? | Document stores for large volumes |
| Relationships | Are relationships complex? | Graph databases for complex relations |
| Transactions | Is ACID compliance required? | SQL databases for strict consistency |
| Query Patterns | Read-heavy or write-heavy? | Affects indexing strategy |

**Step 2: Evaluate Database Categories**

Database Type          Best For
─────────────────────────────────────────────────────────────────
Relational (PostgreSQL, MySQL)
    └── Structured data, complex joins, ACID compliance

Document (MongoDB, CouchDB)
    └── Flexible schema, hierarchical data, rapid iteration

Key-Value (Redis, DynamoDB)
    └── Caching, sessions, simple lookups, high performance

Column-Family (Cassandra, HBase)
    └── Time-series, write-heavy, distributed scale

Graph (Neo4j, Amazon Neptune)
    └── Social networks, recommendations, fraud detection

Search (Elasticsearch, Solr)
    └── Full-text search, log analysis, analytics

Time-Series (InfluxDB, TimescaleDB)
    └── Metrics, monitoring, IoT data

Object (Amazon S3, MinIO)
    └── Files, images, backups, static assets
**Step 3: Decision Matrix**

| Criteria | Weight | PostgreSQL | MongoDB | Cassandra | Redis | Neo4j |
|----------|--------|------------|---------|-----------|-------|-------|
| Structured data | 20% | ✓✓✓ | ✓ | ✓ | ○ | ✓ |
| Scalability | 20% | ✓ | ✓✓ | ✓✓✓ | ✓✓ | ✓ |
| Query flexibility | 15% | ✓✓✓ | ✓✓ | ✓ | ○ | ✓✓ |
| Transaction safety | 15% | ✓✓✓ | ✓ | ○ | ✓✓ | ✓✓ |
| Performance | 15% | ✓ | ✓✓ | ✓✓✓ | ✓✓✓ | ✓ |
| Team expertise | 15% | (Rate) | (Rate) | (Rate) | (Rate) | (Rate) |

---

### Architecture Pattern Selection Workflow

Use this workflow when asked: "What architecture pattern should I use?", "How should I structure my application?"

**Pattern Comparison:**

| Pattern | Complexity | Scalability | Team Size | Use Case |
|---------|------------|-------------|-----------|----------|
| Monolithic | Low | Limited vertical | Small (1-5) | MVPs, simple apps |
| Modular Monolith | Medium | Moderate vertical | Medium (5-15) | Growing apps |
| Layered | Low-Medium | Moderate | Any | Enterprise apps |
| Microservices | High | High horizontal | Large (15+) | Complex systems |
| Event-Driven | High | High | Medium-Large | Real-time systems |
| Serverless | Medium | Very High | Small | Spiky workloads |
| Edge Computing | Medium | Distributed | Medium | IoT, low-latency |

**Selection Criteria:**

START HERE
    │
    ▼
How large is your team?
    │
    ├─── Small (< 5) ──► Monolithic or Modular Monolith
    │                         │
    │                         ▼
    │                    How complex is the domain?
    │                         │
    │                         ├── Simple ──► Monolithic
    │                         └── Complex ──► Modular Monolith
    │
    ├─── Medium (5-15) ──► Modular Monolith or Layered
    │                          │
    │                          ▼
    │                     What's the growth trajectory?
    │                          │
    │                          ├── Stable ──► Modular Monolith
    │                          └── Growing ──► Consider microservices
    │
    └─── Large (15+) ──► Microservices or Event-Driven
                             │
                             ▼
                        Do you need real-time processing?
                             │
                             ├── Yes ──► Event-Driven
                             └── No ──► Microservices
---

### Monolith vs Microservices Decision

Use this workflow when asked: "Should I use monolith or microservices?", "When to break apart a monolith?", "Convert monolith to microservices?"

**Decision Matrix:**

| Factor | Monolith | Microservices |
|--------|----------|---------------|
| Development speed | Faster initially | Slower to start |
| Deployment | Single deploy | Multiple deploys |
| Scaling | Scale entire app | Scale components |
| Technology lock-in | Yes | No |
| Debugging | Easier | Complex |
| Data isolation | Shared database | Separate databases |
| Team autonomy | Limited | High |
| Infrastructure cost | Lower initially | Higher |
| Operational complexity | Lower | Higher |

**Red Flags for Microservices (Don't start here):**

- [ ] Team size < 10 developers
- [ ] Unclear domain boundaries
- [ ] Limited DevOps maturity
- [ ] Tight budget for infrastructure
- [ ] No existing observability
- [ ] Undefined service contracts

**Green Lights for Microservices:**

- [ ] Team size > 15 developers
- [ ] Well-understood bounded contexts
- [ ] Mature DevOps practices (CI/CD, monitoring)
- [ ] Budget for orchestration (Kubernetes, service mesh)
- [ ] Existing observability (metrics, logging, tracing)
- [ ] Stable API contracts

**Migration Path: Monolith → Modular Monolith → Microservices**

Phase 1: Modular Monolith          Phase 2: Extract Services         Phase 3: Full Microservices
┌─────────────────────────┐        ┌─────────────────────────┐       ┌─────────────────────────┐
│  Presentation Layer     │        │  Presentation Layer     │       │  API Gateway            │
├─────────────────────────┤        ├─────────────────────────┤       ├─────────────────────────┤
│  Business Layer         │        │  Service A  │ Service B │       │  Service A │ Service B │
│  ┌─────┐ ┌─────┐ ┌─────┐│        │  ┌─────┐    │ ┌─────┐   │       │  ┌─────┐  │ ┌─────┐   │
│  │Mod A│ │Mod B│ │Mod C││   ──►  │  │ A   │    │ │ B   │   │  ──►  │  │ A   │  │ │ B   │   │
│  └─────┘ └─────┘ └─────┘│        │  └─────┘    │ └─────┘   │       │  └─────┘  │ └─────┘   │
├─────────────────────────┤        ├─────────────────────────┤       ├─────────────────────────┤
│  Data Access Layer      │        │  Database A │ Database B│       │  Database A │ Database B│
└─────────────────────────┘        └─────────────────────────┘       └─────────────────────────┘
---

## Architecture Decision Records

Create ADRs for significant architectural decisions.

**ADR Structure:**

markdown
# ADR-001: Use PostgreSQL as Primary Database

## Status
Accepted

## Context
We need to select a primary database for our e-commerce platform that will handle:
- Product catalog with 100K+ SKUs
- User accounts and authentication
- Order processing with transactions
- Real-time inventory updates

## Decision
We will use PostgreSQL as our primary database.

## Consequences

### Positive
- ACID compliance ensures order integrity
- Rich JSON support for flexible product attributes
- Excellent performance with proper indexing
- Strong community and mature tooling

### Negative
- Horizontal scaling requires more effort
- Schema changes require migrations

## Alternatives Considered

### MongoDB
- Pro: Flexible schema for product variations
- Con: Weaker transaction support than PostgreSQL

### MySQL
- Pro: Good performance characteristics
- Con: Less feature-rich than PostgreSQL
**When to Create an ADR:**

- Selecting new technology or framework
- Changing architectural pattern
- Significant refactoring decisions
- Third-party service integrations
- Performance optimization strategies
- Security architecture changes

---

## Reference Documentation

### Common Architecture Patterns

| Pattern | Description | When to Use |
|---------|-------------|-------------|
| Layered | Separate layers (UI, Business, Data) | Traditional web applications |
| MVC | Model-View-Controller | Web frameworks (Rails, Django) |
| Event Sourcing | Store events instead of state | Audit trails, complex domains |
| CQRS | Separate read/write models | High-read or high-write systems |
| Hexagonal | Ports and adapters | Testable business logic |
| DDD | Domain-Driven Design | Complex business domains |
| Clean | Onion architecture | Maintainable large codebases |

### Scalability Principles

Horizontal Scaling (Scale Out)          Vertical Scaling (Scale Up)
─────────────────────────────           ──────────────────────────────
Add more servers                         Add more power to existing server
Stateless services                       More CPU, RAM, storage
Load balancers required                  No load balancer needed
Complex data synchronization             Single data source
Higher availability                      Simpler architecture
                                        Limited by hardware
### CAP Theorem

Consistency
            /\
           /  \
          /    \
         / CAP  \
        /────────\
       /          \
      /            \
  Availability ─── Partition Tolerance

Pick 2 of 3:
┌──────────────────┬──────────────────┬──────────────────┐
│  CA Systems      │  CP Systems      │  AP Systems      │
│  (CA)            │  (CP)            │  (AP)            │
├──────────────────┼──────────────────┼──────────────────┤
│  PostgreSQL      │  MongoDB         │  Cassandra       │
│  MySQL           │  HBase           │  CouchDB         │
│                  │  Redis           │  DynamoDB        │
│                  │  (with raft)     │  S3              │
└──────────────────┴──────────────────┴──────────────────┘
---

## Tech Stack Coverage

### Frontend

| Category | Options |
|----------|---------|
| Frameworks | React, Vue, Angular, Svelte, Next.js, Nuxt.js |
| State Management | Redux, MobX, Zustand, Pinia, Vuex |
| Styling | Tailwind, CSS Modules, Styled Components |
| Testing | Jest, Cypress, Playwright |

### Backend

| Category | Options |
|----------|---------|
| Languages | Python, Node.js, Go, Rust, Java, C# |
| Frameworks | Django, FastAPI, Express, Spring, Rails |
| API | REST, GraphQL, gRPC, tRPC |
| Messaging | Kafka, RabbitMQ, Redis Pub/Sub, SQS |

### Databases

| Category | Options |
|----------|---------|
| Relational | PostgreSQL, MySQL, MariaDB, SQLite |
| Document | MongoDB, CouchDB |
| Key-Value | Redis, DynamoDB, etcd |
| Search | Elasticsearch, Meilisearch |
| Time-Series | InfluxDB, TimescaleDB |
| Graph | Neo4j, Amazon Neptune |

### Infrastructure

| Category | Options |
|----------|---------|
| Cloud | AWS, GCP, Azure, Vercel, Netlify |
| Containers | Docker, Podman |
| Orchestration | Kubernetes, Docker Swarm |
| IaC | Terraform, Pulumi, CloudFormation |
| CI/CD | GitHub Actions, GitLab CI, Jenkins |

### Observability

| Category | Options |
|----------|---------|
| Monitoring | Prometheus, Datadog, CloudWatch |
| Logging | ELK Stack, Loki, Splunk |
| Tracing | Jaeger, Zipkin, OpenTelemetry |
| Alerting | PagerDuty, OpsGenie, Alertmanager |

---

## Common Commands

bash
# Architecture Diagram Generation
python scripts/architecture_diagram_generator.py ./project --format mermaid --type component
python scripts/architecture_diagram_generator.py ./project --format plantuml --type layer --output diagram.puml
python scripts/architecture_diagram_generator.py ./project --format ascii --type deployment

# Dependency Analysis
python scripts/dependency_analyzer.py ./project --output json --check security
python scripts/dependency_analyzer.py ./project --output html --report ./security-report.html
python scripts/dependency_analyzer.py ./project --fail-on critical

# Project Architecture Assessment
python scripts/project_architect.py ./project --verbose --recommendations
python scripts/project_architect.py ./project --output ./assessment.md --format markdown

# Quick Project Scan
python scripts/project_architect.py ./project && python scripts/dependency_analyzer.py ./project --check all
---

## Best Practices

### Architecture Design

1. **Start simple, add complexity when needed** - Avoid over-engineering
2. **Make decisions reversible where possible** - Avoid premature optimization
3. **Document the "why"** - Future developers need context
4. **Consider operations from day one** - Deployment, monitoring, recovery
5. **Validate assumptions** - Prototype critical components

### Dependency Management

1. **Pin exact versions** - Use lock files consistently
2. **Audit regularly** - Schedule dependency reviews monthly
3. **Minimize dependencies** - Each dependency is a liability
4. **Prefer well-maintained packages** - Check activity and community
5. **Review licenses** - Ensure compatibility with your project

### Documentation

1. **Keep diagrams up to date** - Automated generation helps
2. **Document decisions, not details** - Code shows how, docs show why
3. **Use consistent notation** - Stick to one diagram format
4. **Include runbooks** - How to operate and troubleshoot
5. **Version your docs** - Architecture evolves, documentation should too