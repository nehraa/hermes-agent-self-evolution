---
category: software-development
name: CTO
description: Be the CTO with technical strategy, architecture decisions, team scaling, hiring, tech debt management, and engineering leadership.
slug: cto
version: 1.1.0
homepage: https://clawic.com/skills/cto
changelog: "Restructured for clarity, completed Build vs Buy framework, added decision trees and examples"
metadata:
  emoji: "⚙️"
  requires:
    bins: []
  os: ["linux", "darwin", "win32"]
---

## Role Overview

Act as the Chief Technology Officer when facing decisions about:

- **Strategy** — Technical roadmap, technology selection, architectural direction
- **Architecture** — System design, data models, service boundaries, infrastructure
- **People** — Hiring, firing, team structure, culture, career development
- **Process** — Engineering methodology, delivery, quality, incident response
- **Risk** — Tech debt, technical risk, build vs buy, vendor decisions

---

## Core Principles

### 1. Business Outcome First

Technology is a means to an end. Every technical decision must connect to a business metric. Cool tech that doesn't move the needle is a hobby project, not a strategy.

**Rule:** If you can't explain how a technical choice impacts revenue, customer acquisition, retention, or operational efficiency, reconsider the investment.

### 2. Right-Size the Solution

| Stage | Architecture | Data | Deployment |
|-------|--------------|------|------------|
| **Seed/Startup** | Monolith, MVC | Single database, simple schema | Single server or simple PaaS |
| **Growth** | Modular monolith, emerging services | Read replicas, basic caching | Load balancer, CDN |
| **Scale** | Domain-driven services, event-driven | Sharding, data warehouse | Kubernetes, multi-region |
| **Enterprise** | Distributed systems, microservices where justified | Polyglot persistence | Multi-cloud, sophisticated observability |

**Rule:** Over-engineering kills startups. Under-engineering kills scale-ups. Match complexity to current and near-term needs.

### 3. Boring Technology on the Critical Path

Pick proven, boring technology for systems where failure is costly. Reserve innovation for one layer at a time.

**Examples:**

- Boring choice for payment processing: PostgreSQL with proper transactions
- Innovation layer: New ML model for recommendations

### 4. Microservices When You Feel the Pain

Don't adopt microservices for theoretical benefits. Adopt them when you experience specific pain:

| Pain Point | Microservice Signal |
|------------|---------------------|
| Conflicting deployment schedules | Teams stepping on each other |
| team size > 10-15 engineers | Conway's Law violations |
| Shared codebase causing merge conflicts | Modularity already emerging |
| Different scaling needs per feature | One component crushing the rest |
| Desire for polyglot (justified) | Specific language runtime needed |

**Warning:** Microservices add operational complexity, network latency, distributed tracing burden, and organizational overhead. Only adopt when the pain of NOT decomposing exceeds the cost of distribution.

### 5. Two-Pizza Teams and Service Boundaries

Service boundaries should align with team boundaries. A team that can't be fed by two pizzas (6-8 people) probably owns too little. A team that needs 20 people has too many moving parts to coordinate.

**Conway's Law Enforcement:** If your org chart doesn't match your system architecture, one of them will break. Fix the broken one first.

---

## Technical Strategy Framework

### Building the Roadmap

1. **Start with business goals** — What are the Q1/Q2/Q3 targets? Revenue, users, retention, efficiency?

2. **Identify technical gaps** — What's blocking those goals? Performance, scale, reliability, features?

3. **Prioritize by impact** — Which technical changes unlock business outcomes?

4. **Size the work** — RICE score: Reach × Impact × Confidence ÷ Effort

5. **Communicate with stakeholders** — Engineers want to know why. Executives want to know when. Customers want to know what changed.

**Quarterly Roadmap Template:**

Q1 Focus: [Business Goal]
├── Initiative 1: [Description]
│   └── Owner: [Name] | Target: [Date] | Effort: [Size]
├── Initiative 2: [Description]
│   └── Owner: [Name] | Target: [Date] | Effort: [Size]
└── Tech Debt: [Description]
    └── Owner: [Name] | Target: [Date] | Effort: [Size]
### Build vs Buy vs Open Source

**Build when:**
- Core to your competitive advantage
- Data security/privacy is paramount
- Requirements are highly specialized
- You have unique expertise

**Buy when:**
- Not core to your business
- Vendor is established and reliable
- Integration is straightforward
- Total cost is predictable

**Open Source when:**
- You have the expertise to maintain it
- Community is active
- License aligns with your usage
- You can absorb support burden

**Decision Matrix:**

| Factor | Build | Buy | Open Source |
|--------|-------|-----|-------------|
| Core to business | ✓ | ✗ | ⚠️ |
| Your expertise | High | Low | Medium |
| Maintenance capacity | High | Low | Medium |
| Time to market | Slow | Fast | Medium |
| Long-term cost | Variable | Predictable | Variable |

---

## Architecture Decision Framework

### When Faced with an Architecture Decision

1. **Define the problem** — What specific problem are you solving? Write it down.

2. **Establish constraints** — Time, budget, team expertise, scale requirements, regulatory.

3. **Identify forces** — Conflicting requirements, trade-offs, risks.

4. **Consider options** — Typically 2-4 viable options. More suggests the problem isn't defined enough.

5. **Evaluate against criteria** — Speed to implement, operational complexity, scalability, maintainability, team familiarity.

6. **Make the decision** — Document rationale. Include dissenting opinions.

7. **Review later** — Set a date to revisit. Context changes.

### Architecture Decision Record (ADR) Template

markdown
# ADR-XXX: [Title]

## Status
[Proposed | Accepted | Deprecated | Superseded]

## Context
[What is the issue we're seeing that is motivating this decision?]

## Decision
[What is the change we're making?]

## Consequences
### Positive
- [Benefit 1]
- [Benefit 2]

### Negative
- [Downside 1]
- [Downside 2]

### Neutral
- [Trade-off 1]
- [Trade-off 2]
---

## Team Structure and Scaling

### Hiring Framework

**Define the role clearly:**
- What problem does this person solve?
- What does success look like at 30/60/90 days?
- What level (IC or manager) and scope?

**Interview structure:**
- Screen: Basic competence, culture fit
- Technical: Role-specific skills
- Deep dive: Problem-solving, system design
- Leadership (for senior roles): People management, conflict resolution

**Red flags:**
- Can't explain their past work clearly
- Blames others for failures without self-reflection
- Unwilling to do any task (overqualified for the work)
- Contradicts themselves across interviewers

**Green flags:**
- Explains trade-offs in their decisions
- Asks clarifying questions
- Shows genuine interest in the problem
- Describes learning from failures

### Team Scaling Curve

| Team Size | Structure | Focus |
|-----------|-----------|-------|
| 1-3 | Flat | Full-stack, move fast |
| 4-8 | Flat with tech lead | Feature teams, some coordination |
| 9-15 | Team leads emerge | Dedicated areas, regular syncs |
| 16-30 | Managers + Tech Leads | Clear ownership, processes needed |
| 30+ | Department structure | Organizational design matters |

### Performance Management

**Set clear expectations:**

- **Goals:** What needs to be achieved (OKRs)
- **Competencies:** How to achieve it (technical skills, soft skills)
- **Values:** How to treat others (company values in action)

**Calibration process:**
1. Manager writes self-assessment
2. Peers provide 360 feedback
3. Calibration session with leadership
4. Delivery to employee
5. Career development discussion

---

## Tech Debt Management

### Categorizing Tech Debt

| Type | Urgency | Example | Response |
|------|---------|---------|----------|
| **Horror** | Critical | Security vulnerability, data loss bug | Drop everything, fix now |
| **Accumulated** | High | Copy-paste code, inconsistent patterns | Schedule 20% capacity |
| **Intentional** | Medium | MVP that needs rewrite, fast path | Document, plan migration |
| **Bit rot** | Low | Deprecated API still works | Deprecate gracefully |

### Tech Debt Ratio

Track tech debt as a percentage of total codebase. Target:

- **Healthy:** < 15% tech debt ratio
- **Warning:** 15-30% — Development slowing
- **Critical:** > 30% — Major refactor needed

### Paying Down Tech Debt

1. **Boy scout rule:** Leave code cleaner than you found it
2. **Strangler fig pattern:** Gradually replace old system with new
3. **Feature flags:** Enable parallel implementations
4. **40/20/40 time allocation:** 40% features, 20% tech debt, 40% maintenance/unscheduled

---

## Risk Management

### Technical Risk Categories

1. **Infrastructure risk** — Single points of failure, provider dependency
2. **Data risk** — Loss, corruption, breach, compliance
3. **Security risk** — Vulnerabilities, access control, secrets management
4. **Dependency risk** — Single vendor, abandoned open source, transitive dependencies
5. **Knowledge risk** — Bus factor of 1, no documentation

### Risk Assessment Matrix

| Likelihood → | Rare | Unlikely | Possible | Likely | Almost Certain |
|--------------|------|----------|----------|--------|----------------|
| **Severity ↓** | | | | | |
| Catastrophic | Medium | Medium | High | Critical | Critical |
| Major | Low | Medium | Medium | High | Critical |
| Moderate | Low | Low | Medium | Medium | High |
| Minor | Low | Low | Low | Medium | Medium |
| Negligible | Low | Low | Low | Low | Low |

### Mitigation Strategies

| Risk Type | Mitigation |
|-----------|------------|
| Provider outage | Multi-region, hybrid cloud |
| Data loss | Backups, point-in-time recovery, test restores |
| Security breach | Defense in depth, regular pen testing, bug bounty |
| Vendor lock-in | Abstraction layers, open standards where possible |
| Knowledge loss | Documentation, pair programming, runbooks |

---

## Communication and Stakeholder Management

### For Executives

**What they need:**

- Top 3 priorities and progress
- Key risks and mitigations
- Resource needs (headcount, budget)
- Decisions required

**Communication cadence:**

- Weekly: One-pager on key metrics
- Monthly: Roadmap review
- Quarterly: Strategy alignment

### For Engineers

**What they need:**

- Clear context on why
- Autonomy on how
- Recognition for good work
- Career development

**Communication cadence:**

- Daily: Standups, async updates
- Weekly: Team meetings, demos
- Monthly: All-hands, retrospectives
- Quarterly: Goal setting, OKR alignment

---

## Incident Response

### Severity Levels

| Level | Definition | Response Time | Example |
|-------|------------|---------------|---------|
| **SEV1** | Complete outage, data loss | Immediate | Site down, DB corruption |
| **SEV2** | Major feature broken, partial outage | < 15 min | Checkout broken, auth failing |
| **SEV3** | Degraded experience | < 1 hour | Slow API, minor feature broken |
| **SEV4** | Minor issue | Next business day | Cosmetic bug, non-critical |

### Incident Process

1. **Detect** — Alerting, customer report, monitoring
2. **Triage** — Assess severity, assign incident commander
3. **Communicate** — Notify stakeholders, create status page
4. **Mitigate** — Fix or rollback
5. **Resolve** — Confirm fix, close incident
6. **Review** — blameless postmortem within 48 hours
7. **Action** — Fix root cause, prevent recurrence

### Postmortem Template

markdown
# Postmortem: [Incident Name]

## Summary
[2-3 sentence description of what happened and impact]

## Timeline (UTC)
- HH:MM - [Event]
- HH:MM - [Event]

## Root Cause
[Technical root cause, not "human error"]

## Contributing Factors
- Factor 1
- Factor 2

## Resolution
[How it was fixed]

## Action Items
| Action | Owner | Due Date |
|--------|-------|----------|
| [Action 1] | [Name] | [Date] |
| [Action 2] | [Name] | [Date] |

## Lessons Learned
### What went well
- [Positive observation]

### What could be improved
- [Improvement opportunity]
---

## Decision Trees

### When to Rewrite vs Refactor

Is the current system fundamentally broken?
├── Yes → Rewrite if:
│         ├── Core domain model is wrong
│         ├── Tech stack is truly obsolete
│         └── You have the team and time
└── No → Refactor if:
          └── Existing architecture is salvageable
### When to Add Features

Does this feature:
├── Align with core product strategy?
│   └── No → Reject with explanation
└── Yes → Does it:
          ├── Solve a real user problem?
          │   └── No → Reject
          └── Have acceptable ROI?
              └── Yes → Prioritize against roadmap
### When to Take on Technical Risk

Is this risk:
├── On the critical path (blocks business)?
│   └── Yes → Eliminate or mitigate aggressively
└── Not on critical path → Accept if:
                          ├── Impact is contained
                          ├── You can monitor it
                          └── You can reverse it
---

## Quick Reference Cards

### Startup Phase Checklist

- [ ] Single deployment unit (monolith)
- [ ] PostgreSQL or MySQL for data
- [ ] No premature optimization
- [ ] Monitoring and alerting basics
- [ ] Automated tests for critical paths
- [ ] Documentation for operations
- [ ] At least 2 people who can deploy

### Growth Phase Checklist

- [ ] Monitoring, logging, tracing
- [ ] Database read replicas
- [ ] CDN for static assets
- [ ] Load balancing
- [ ] API rate limiting
- [ ] Basic caching strategy
- [ ] Incident response process
- [ ] Regular deployment cadence

### Scale Phase Checklist

- [ ] Service boundaries defined
- [ ] Async processing for heavy tasks
- [ ] Database sharding strategy
- [ ] Multi-region deployment
- [ ] Advanced observability
- [ ] SLOs and error budgets
- [ ] Platform/infrastructure as code
- [ ] Clear ownership per service

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It's Bad | Better Alternative |
|--------------|--------------|---------------------|
| Not invented here | Rewriting solves nothing | Evaluate existing solutions |
| Big bang rewrite | Too risky, no user value mid-way | Incremental strangler fig |
| Analysis paralysis | Speed matters | Make reversible decisions |
| Shiny object syndrome | Complexity for complexity's sake | Boring technology baseline |
| Hero culture | Bus factor of 1 | Knowledge sharing, docs |
| Perfect is the enemy of good | Delayed shipping | Ship, iterate, improve |
| Tech debt denial | Debt compounds | 20% capacity for maintenance |
| Siloed teams | Conway's Law violation | Cross-functional teams |

---

## When to Escalate

Escalate to leadership when:

- **Timeline impact:** > 2 weeks slip on committed deadline
- **Resource gap:** Need headcount, budget, or vendor approval
- **Strategic decision:** Affects product direction or architecture
- **Risk threshold:** Potential customer data exposure or major revenue impact
- **Team conflict:** Unresolvable disagreement affecting delivery

**Escalation format:**

Situation: [What's happening]
Impact: [Business or technical consequence]
Options: [What you could do]
Recommendation: [What you think we should do]
Decision needed: [What you need from leadership]