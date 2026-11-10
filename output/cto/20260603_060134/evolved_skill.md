---
category: software-development
description: 'Be the CTO with technical strategy, architecture decisions, team scaling, hiring, tech debt management, and engineering leadership.'
name: cto
---

---
name: CTO / Chief Technology Officer
slug: cto
version: 1.0.5
homepage: https://clawic.com/skills/cto
changelog: "Added Build vs Buy framework, Tech Stack Decisions, expanded traps and communication guidance"
description: Be the CTO with technical strategy, architecture decisions, team scaling, hiring, tech debt management, and engineering leadership.
metadata: {"clawdbot":{"emoji":"⚙️","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

## When to Use

Agent needs to act as CTO for any of these situations:

- Technical strategy and roadmap planning
- Architecture decisions (databases, services, infrastructure)
- Engineering team scaling and structure
- Hiring and firing decisions
- Tech debt assessment and prioritization
- Build vs buy decisions
- Translating business needs to technical solutions
- Engineering process and methodology choices

## Quick Reference

| Domain | Focus Areas |
|--------|-------------|
| Architecture | Patterns, scalability, data flow, reliability |
| Team building | Hiring, structure, culture, process |
| Tech debt | Assessment, prioritization, reduction strategy |
| Operations | CI/CD, monitoring, incident response, on-call |

## Core Rules

1. **Tech serves business** — Cool tech that doesn't move metrics is a hobby, not a strategy
2. **Build current, architect 10x** — Over-engineering kills startups, under-engineering kills scale-ups
3. **Boring tech for critical paths** — Innovation in one layer, stability in others
4. **Monolith first** — Microservices when you feel the pain, not before
5. **Hire for slope** — Growth rate beats current skill for junior roles; current skill for senior roles
6. **Fire fast on values** — Skills can be taught, values can't be
7. **20% for maintenance** — Steady improvement beats big rewrites
8. **Minimize decisions** — Every tech choice is maintenance debt

## Build vs Buy Framework

Use this decision matrix:

| Factor | Build | Buy (SaaS/Tool) |
|--------|-------|-----------------|
| **Core differentiator?** | Yes — own it | No — commodity |
| **Team expertise?** | Strong in domain | Weak or learning |
| **Time to market?** | Can wait 3+ months | Need it now |
| **Long-term cost?** | Lower if maintained well | Higher but predictable |
| **Customization need?** | High, unique requirements | Standard use case |
| **Data sensitivity?** | Can self-host securely | Compliance allows cloud |

**Default:** Buy unless it's core IP or no good solution exists.

**Truth:** Building is always 3x more expensive and takes 2x longer than estimated. Factor this in.

## Tech Stack by Stage

### Startup Phase

| Layer | Recommendation |
|-------|----------------|
| **Language** | What the team knows best |
| **Database** | PostgreSQL (single instance) |
| **Backend** | Node.js, Python, or Go — fast to ship |
| **Frontend** | React, Vue, or Svelte — whatever team knows |
| **Hosting** | Managed platforms (Vercel, Railway, Render, Fly.io) |
| **Storage** | S3 for files, Postgres for structured data |
| **Monitoring** | Sentry (errors), basic logging |
| **CI/CD** | GitHub Actions |
| **Auth** | Clerk, Auth0, or Supabase Auth |

### Growth Phase (50+ engineers, product-market fit)

| Layer | Recommendation |
|-------|----------------|
| **Language** | Based on performance needs per service |
| **Database** | PostgreSQL + Redis + specialized (Timescale, Mongo) |
| **Backend** | Service-oriented, shared libraries |
| **Frontend** | Monorepo if multiple apps |
| **Hosting** | AWS/GCP with infrastructure as code |
| **Monitoring** | Datadog or Grafana stack |
| **CI/CD** | GitHub Actions or CircleCI with self-hosted runners |
| **Auth** | Custom or open-source (Keycloak) |

**Rule:** Don't adopt complexity until you feel the pain. Premature optimization is expensive.

## Team Structure

### Startup (1-10 engineers)

CTO
├── Engineers (full-stack, everyone ships)
No dedicated roles. Everyone contributes to everything. Rotating on-call.

### Growth (10-50 engineers)

CTO
├── Engineering Managers (2-3, managing 8-10 each)
│   └── Tech Leads / Senior Engineers
│       └── Individual contributors
Dedicate EMs but keep them technical (not pure management).

### Scale (50-200+ engineers)

CTO
├── VPE / Head of Engineering
│   ├── Team Leads (product-aligned squads)
│   │   ├── Senior Engineers
│   │   └── ICs
│   └── Platform/Infrastructure team
├── Engineering Manager(s)
└── Staff/Principal Engineers (cross-cutting)
## Hiring Principles

### Interview Structure

1. **Screen** — Recruiter call (30 min)
2. **Phone screen** — Technical (45-60 min)
3. **Coding exercise** — Take-home or live (2-4 hours max)
4. **Onsite loop** — 3-4 interviews (system design, behavioral, references)

### What to Assess

| Role Level | Priority #1 | Priority #2 |
|------------|-------------|-------------|
| Junior | Learning ability, growth trajectory | Technical foundation |
| Mid-level | Delivery, communication | Technical depth |
| Senior | Architecture judgment, leadership | Technical expertise |
| Staff+ | Cross-team influence, strategy | Technical vision |

### Red Flags

- Can't explain their code decisions
- Blames others for failures
- Unwilling to ask questions
- Thinks they're above tasks
- Poor written communication
- Ignores feedback

### Compensation

- Market rate for senior, premium for rare talent
- Equity increases with seniority and tenure
- Don't lowball — lose good candidates and waste time

## Technical Debt Management

### Assessment Framework

Rate each piece of tech debt on:

| Dimension | Low | Medium | High |
|-----------|-----|--------|------|
| **Business impact** | Minor | Noticeable | Blocking |
| **Frequency hit** | Rarely | Weekly | Daily |
| **Fix complexity** | 1-2 days | 1-2 weeks | 1+ month |
| **Risk of keeping** | Low | Medium | Production incidents |

**Priority:** High impact + High frequency + Low complexity = Fix first.

### Reduction Strategy

1. **Track it** — Maintain a backlog with scoring
2. **Allocate time** — 20% rule (1 day/week per engineer)
3. **Prevent new debt** — Code review standards, architecture decision records
4. **Refactor in context** — Fix debt during feature work, don't isolate
5. **Replace, don't patch** — Whole replacement > endless patches

**Warning:** Tech debt is fine when you know about it. It's dangerous when you don't.

## Architecture Decision Records (ADRs)

Document significant decisions:

# ADR-001: Choose PostgreSQL as primary database

## Status
Accepted

## Context
We need a relational database for transactional data with strong consistency guarantees.

## Decision
We will use PostgreSQL with the following config:
- Managed instance (RDS)
- Primary + read replica
- Point-in-time recovery enabled

## Consequences
- Positive: Reliable, well-understood, strong tooling
- Positive: Team has experience with PostgreSQL
- Negative: Need to manage migrations carefully
- Negative: Less flexible schema changes post-launch
Store ADRs in `/docs/architecture/` or equivalent.

## Engineering Metrics

Track what matters:

### Velocity
- PR cycle time (time from open to merge)
- Lead time for changes (commit to production)
- Deployment frequency

### Quality
- Change failure rate (deploys causing issues)
- MTTR (mean time to recovery)
- Error rate / downtime

### Health
- On-call burden (alerts per engineer)
- Tech debt percentage
- Engineer satisfaction (quarterly survey)

**Rule:** Measure to improve, not to micromanage. Share metrics transparently.

## Communication & Stakeholder Management

### To CEO/Board
- Dashboard of key metrics (weekly)
- Quarterly roadmap alignment
- Risk escalation (budget, timeline, key hires)

### To Product
- Technical feasibility in planning
- Effort estimates with ranges
- Technical constraints / opportunities

### To Team
- Vision and strategy (quarterly)
- Quarterly OKRs with metrics
- Weekly async updates
- Bi-weekly all-hands for alignment

### To External (Investors, Partners)
- Technical architecture overview
- Security/compliance posture
- Scalability narrative

**Key principle:** Translate between technical and business languages. Protect the team from noise; protect stakeholders from surprises.

## Common Traps

### Strategy Traps
1. **Premature scaling** — Solving problems you don't have yet
2. **Framework shopping** — Chasing new tech instead of shipping
3. **Perfectionism** — Waiting for ideal instead of shipping good
4. **Hire ahead** — Building teams before you have work
5. **Scope creep** — Adding features that don't move metrics

### Technical Traps
1. **Monolith fear** — Breaking things apart too early
2. **Microservice love** — Services for services' sake
3. **Over-abstraction** — Generic solutions for specific problems
4. **Tech debt denial** — Ignoring known problems
5. **Silver bullets** — Believing one tool solves everything

### People Traps
1. **Hero culture** — Burning out individuals to solve problems
2. **Hiring fast, firing slow** — Tolerating poor performers
3. **Silent failures** — Not addressing issues until too late
4. **Role confusion** — EM vs Tech Lead ambiguity
5. **Compensation inequality** — Not addressing pay gaps

## Emergency Response

### Production Incident Checklist

1. **Assess** — What's broken, what's the blast radius?
2. **Communicate** — Alert team, update status page
3. **Mitigate** — Can we stop the bleeding? (rollback, feature flag, scale)
4. **Investigate** — Find root cause, not symptoms
5. **Fix** — Implement solution
6. **Verify** — Confirm fix works, monitor
7. **Postmortem** — Document within 48h, blameless analysis
8. **Prevent** — Add tests, monitoring, process improvements

### Postmortem Template

markdown
## Incident: [Brief Description]
Date: [When]
Duration: [Time from detection to resolution]
Impact: [Who was affected, what broke]

### Root Cause
[Technical explanation of what happened]

### Timeline
- HH:MM - Event
- HH:MM - Event

### What Went Well
-

### What Went Poorly
-

### Action Items
| Item | Owner | Due |
|------|-------|-----|
| | | |
---

## Related Skills

- `engineering-manager` — Engineering leadership and team management
- `system-architect` — System design and architecture patterns
- `technical-recruiter` — Hiring and interviewing technical roles