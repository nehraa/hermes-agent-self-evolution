---
category: software-development
name: CTO
description: Be the CTO with technical strategy, architecture decisions, team scaling, hiring, tech debt management, and engineering leadership.
slug: cto
version: 1.2.0
homepage: https://clawic.com/skills/cto
changelog: "Added complete decision frameworks, hiring decision tree, tech debt prioritization model, build vs buy matrix, and actionable templates"
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
| Team size > 8-10 engineers on single codebase | Services enable team autonomy |
| Independent deployment requirements | Different services have different release cadences |
| Scalability asymmetry | Only specific features need horizontal scaling |
| Technology diversity needs | Different parts need different stacks (e.g., ML vs transactional) |
| Fault isolation requirements | One component's failure shouldn't cascade |

**Rule:** Extract services to solve real problems, not to follow trends. A well-structured modular monolith is often better than a poorly designed microservice architecture.

---

## Technical Strategy Framework

### Decision Hierarchy

When making technical decisions, evaluate in this order:

1. Can we not do this? (Eliminate)
         ↓
2. Can we defer this? (Delay)
         ↓
3. Can we buy this? (Outsource/SaaS)
         ↓
4. Can we open-source this? (Community solutions)
         ↓
5. Can we build this simply? (Build in-house)
         ↓
6. Can we build this robustly? (Full engineering investment)
### Build vs Buy Decision Matrix

| Factor | Build | Buy (SaaS) | Open Source |
|--------|-------|------------|-------------|
| **Core differentiator** | ✅ Always build | ❌ | ❌ |
| **Non-core capability** | ❌ | ✅ Strongly consider | ✅ |
| **Unique requirements** | ✅ | ❌ | Consider |
| **Low customization needs** | ❌ | ✅ | ✅ |
| **Security/compliance critical** | Depends | Vet vendors | Self-host option |
| **Data sensitivity** | Self-host | Review data handling | Self-host |
| **Long-term cost predictable** | Better at scale | Better at low volume | Variable |

**Template for build vs buy:**

markdown
## Build vs Buy Analysis: [Capability Name]

### 1. Is this core to our competitive advantage?
- [ ] Yes → Build
- [ ] No → Continue evaluation

### 2. Cost Comparison (5-year TCO)
| Item | Build | Buy | Notes |
|------|-------|-----|-------|
| Initial investment | $X | $0 | |
| Annual cost | $0 | $Y/month × 12 | |
| Integration cost | A | B | |
| Scaling cost | C | D | |
| **5-year total** | $ | $ | |

### 3. Risk Assessment
| Risk | Build Impact | Buy Impact | Mitigation |
|------|--------------|------------|------------|
| Vendor lock-in | Low | High | Contract terms, exit strategy |
| Security breach | Own | Shared | SLA, breach notification |
| Vendor failure | N/A | Critical | Backup vendors, data portability |

### 4. Decision
[ ] Build | [ ] Buy | [ ] Hybrid
Rationale: _______________
---

## Team Scaling Guide

### Engineering Headcount by Stage

| Stage | Team Size | Structure | Key Hires |
|-------|-----------|-----------|-----------|
| **Pre-product-market-fit** | 1-3 | All hands | Full-stack generalist |
| **Post-PMF, early scale** | 3-8 | Small teams, flat | Specialists emerge |
| **Growth stage** | 8-25 | Team leads appear | Leads, seniors |
| **Scaling** | 25-50 | Functional teams | Engineering managers |
| **Enterprise** | 50+ | Departments, directors | Directors, VP |

### Hiring Decision Tree

Is there urgent work that current team cannot complete?
├── No → Wait for right candidate
└── Yes → 
    ├── Can a contractor/freelancer solve this temporarily?
    │   ├── Yes → Contract
    │   └── No → Continue
    │
    └── Is this a role we'll need long-term (>2 years)?
        ├── No → Contract/freelancer
        └── Yes → Full-time hire
        
Is this a role we can train internally?
├── Yes → Internal promotion + backfill entry-level
└── No → External hire

What's the priority?
├── Critical path → Senior/experienced hire
└── Exploratory → Consider junior + learning time
### Interview Framework for Senior Hires

markdown
## Senior Engineer Interview Structure

### 1. Technical Depth (45 min)
- Past architecture decisions: "Tell me about a system you designed..."
- Trade-off analysis: "What would you change about your last project?"
- Scaling experience: "How did it perform at 10x traffic?"

### 2. Leadership & Influence (30 min)
- Technical mentorship: "How have you grown junior engineers?"
- Cross-team collaboration: "Tell me about a conflict with another team..."
- Technical communication: "Explain [complex topic] to a non-technical stakeholder"

### 3. Problem Solving (30 min)
- System design: Design [relevant system type]
- Debugging: Given symptoms, walk through diagnosis

### 4. Values Alignment (15 min)
- Startup fit: "How do you handle ambiguity?"
- Growth mindset: "What's the most recent thing you learned?"
- Ownership: "Give an example of a problem you fixed without being asked"
---

## Tech Debt Management

### Tech Debt Classification

| Type | Description | Response |
|------|-------------|----------|
| **Prudent & Deliberate** | Known trade-offs made consciously | Document, plan cleanup |
| **Prudent & Unintentional** | Right decision at the time | Track, prioritize when painful |
| **Reckless & Deliberate** | Knew it was bad, shipped anyway | Immediate risk assessment |
| **Reckless & Unintentional** | Didn't know it was bad | Identify patterns, add safeguards |

### Tech Debt Prioritization Model

markdown
## Tech Debt Scoring Matrix

### Impact Score (1-5)
- How often does this affect users? (1=rarely, 5=daily)
- How many users are affected? (1=few, 5=all)
- What is the business impact? (1=minor, 5=critical)
- Does it block new features? (1=no, 5=frequently)

### Effort Score (1-5, inverted for ranking)
- How complex is the fix? (1=simple, 5=architectural overhaul)
- How long will it take? (1=hours, 5=months)
- What dependencies exist? (1=isolated, 5=deeply coupled)

### Priority Score = Impact / Effort

Focus on high-impact, low-effort items first.
### The "Boy Scout Rule" Policy

Every engineer should leave the code cleaner than they found it.
Implement with:
- **10% rule**: 10% of sprint capacity dedicated to cleanup
- **PR requirements**: No new tech debt without explicitly accepting it
- **Debt registry**: Track all known tech debt with estimates

---

## Risk Management

### Technical Risk Categories

| Category | Examples | Mitigation |
|----------|----------|------------|
| **Operational** | Server failure, data loss, downtime | Monitoring, backups, runbooks |
| **Security** | Data breach, injection, DDoS | Security audits, WAF, pen testing |
| **Vendor** | Provider outage, price changes, lock-in | Multi-cloud, exit strategies, contracts |
| **Talent** | Key person dependency, turnover | Documentation, knowledge sharing, retention |
| **Technical** | Scaling limits, tech obsolescence | Architecture reviews, upgrade planning |
| **Compliance** | GDPR, SOC2, industry regulations | Legal counsel, compliance audits |

### Risk Assessment Template

markdown
## Technical Risk Assessment: [Project/Feature]

### Risk Identification
| Risk | Likelihood (1-5) | Impact (1-5) | Risk Score |
|------|------------------|-------------|------------|
| | | | |
| | | | |
| | | | |

### Top Risks Analysis
For each risk score > 15:

**Risk:** _______________
**Mitigation options:**
1. _______________
2. _______________
3. _______________

**Recommended mitigation:** _______________
**Residual risk:** _______________

### Go/No-Go Decision
[ ] Proceed with mitigation
[ ] Proceed with acknowledged risk
[ ] Do not proceed
---

## Incident Response Framework

### Severity Levels

| Severity | Definition | Response Time | Example |
|----------|------------|---------------|---------|
| **SEV1** | Complete outage or data loss | Immediate (< 15 min) | Site down, data corruption |
| **SEV2** | Major feature broken | < 30 min | Payment processing down |
| **SEV3** | Feature degraded | < 2 hours | Slow search results |
| **SEV4** | Minor issue | Next business day | UI glitch, non-critical |

### Incident Timeline Template

markdown
## Incident Report: [Date] - [Brief Description]

### Summary
Brief description of incident and impact.

### Timeline (UTC)
- HH:MM - Event description
- HH:MM - Action taken
- HH:MM - Resolution

### Root Cause
[Detailed explanation of what went wrong]

### Impact
- Users affected: _______
- Duration: _______
- Revenue impact: _______

### Action Items
| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| | | | |
| | | | |

### Lessons Learned
What went well? _______________
What could be improved? _______________
---

## Technical Roadmap Template

markdown
## Technical Roadmap: [Quarter] [Year]

### Theme
[High-level theme for the quarter, tied to business goals]

### OKRs
- **Objective:** [Measurable goal]
  - Key Result: [Specific metric]
  - Key Result: [Specific metric]

### Initiatives

#### Initiative 1: [Name]
**Business justification:** _______________
**Success metric:** _______________
**Team:** _______________
**Timeline:** _______________

#### Initiative 2: [Name]
...

### Dependencies
- [ ] Dependency on team/project
- [ ] Dependency on vendor/feature

### Risks & Mitigations
| Risk | Mitigation |
|------|------------|
| | |

### Capacity Planning
- Planned capacity: ___%
- Buffer for interrupts: ___%
- Available for new work: ___%
---

## Key Questions for Decision-Making

### Before any technical decision, ensure you can answer:

1. **What business problem does this solve?**
2. **What is the cost of doing nothing?**
3. **What are the alternatives?** (Usually at least 3 exist)
4. **What is the worst case scenario?**
5. **Who owns this after launch?**
6. **How will we measure success?**
7. **What can we do to minimize lock-in?**
8. **What happens if this vendor/technology fails?**

---

## Anti-Patterns to Avoid

| Anti-Pattern | Description | Instead |
|--------------|-------------|---------|
| **Not invented here** | Rebuilding existing solutions | Evaluate tools first |
| **Big bang rewrite** | Complete rebuild from scratch | Incremental migration |
| **Premature optimization** | Solving problems we don't have | YAGNI - You Aren't Gonna Need It |
| **Analysis paralysis** | Endless evaluation, no action | Timebox decisions |
| **Hero culture** | One person critical to everything | Documentation, backups, team |
| **Technical novelty** | Using new tech for its own sake | Match tech to actual needs |
| **Ignore the basics** | Complex solutions for simple problems | Master fundamentals first |

---

## Communication Templates

### Escalation Response
markdown
## Incident Escalation: [Brief Title]

**Severity:** [SEV1/2/3/4]
**Status:** [Investigating/Identified/Resolved]
**Current understanding:** [2-3 sentences on what's happening]
**Impact:** [Who/what is affected]
**Next update:** [Time]
**Bridge:** [Link if ongoing]
### Stakeholder Update
markdown
## Technical Update: [Date]

**Key accomplishments:**
- ✅ Completed [feature]
- ✅ Resolved [issue]
- ✅ Improved [metric]

**In progress:**
- 🔄 [Feature] - [status]
- 🔄 [Feature] - [status]

**Upcoming:**
- 📋 [Feature]
- 📋 [Feature]

**Blockers:**
- ⚠️ [Blocker description]

**Metrics:**
- [System] uptime: X%
- [System] latency: Xms
- Team velocity: X points