---
name: microsoft-skillopt
category: autonomous-ai-agents
description: "Microsoft SkillOpt-Sleep integration for Hermes Agent: harvest Hermes sessions, mine recurring tasks, optimize SKILL.md files with bounded edits and a held-out validation gate, stage proposals for review, and optionally adopt them with backups. Registered as a Hermes tool (`skillopt_run`) and a no_agent watchdog cron (`SkillOpt-Sleep Nightly Consolidation`, every 6h)."
metadata:
  hermes:
    tags: [skillopt, skill-evolution, self-improvement, hermes, validation-gate]
    homepage: https://github.com/microsoft/SkillOpt
    docs: https://microsoft.github.io/SkillOpt/docs/sleep/README/
---

# Microsoft SkillOpt for Hermes

## Overview

Microsoft SkillOpt treats a natural-language skill document as trainable state. SkillOpt-Sleep applies that method to an agent's own sessions, enabling self-optimization through:

read-only session harvest → recurring-task mining → replay → bounded reflection
    → held-out validation gate → staged proposal → explicit adoption
This integration runs as both a Hermes tool and a scheduled cron job, enabling continuous skill improvement with human review gates.

---

## Pipeline Stages

| Stage | Description |
|-------|-------------|
| **Session Harvest** | Reads Hermes sessions from `state.db` in read-only mode |
| **Task Mining** | Identifies recurring tasks and patterns across sessions |
| **Replay Analysis** | Replays session sequences to understand task contexts |
| **Bounded Reflection** | Generates improvement suggestions within constrained bounds |
| **Validation Gate** | Tests proposals against held-out session data |
| **Staged Proposal** | Presents validated changes for explicit review |
| **Adoption** | Applies approved changes with automatic backup |

---

## Component Locations

### Core Integration

| Component | Path |
|-----------|------|
| Repository | `/home/Hermes/repos/skillopt/` |
| Isolated Python | `/home/Hermes/repos/skillopt/.venv/` |
| Hermes Adapter | `/home/Hermes/.hermes/skillopt/hermes_skillopt.py` |
| Launcher Script | `/home/Hermes/.hermes/skillopt/run-hermes-skillopt.sh` |
| Gate Parser | `/home/Hermes/.hermes/skillopt/_parse_gate.py` |
| State/Output | `/home/Hermes/.hermes/skillopt/` |

### Hermes Registration

| Registration | Details |
|--------------|---------|
| Tool Name | `skillopt_run` |
| Toolset | `skills` |
| Actions | `status`, `inspect`, `run`, `manifest` |
| Cron Job | `SkillOpt-Sleep Nightly Consolidation` |
| Cron ID | `364ae7d380ff` |
| Cron Schedule | Every 6 hours |
| Delivery | `local` (mock backend) |
| Hermes Skills Dir | `/home/Hermes/.hermes/skills/` (untouched by default) |

---

## Reference Materials

### Environment Configuration
- **`references/minimax-env-recipe.md`** — Verified environment contract for MiniMax + SkillOpt-Sleep including:
  - Auth mode settings
  - Compatibility max tokens
  - Troubleshooting matrix

### Runtime Security
- **`references/runtime-sanitizer-patterns.md`** — Runtime patterns for:
  - Secret-shaped string rewriting in `write_file` outputs
  - Pre-staging tricks used by the SkillOpt launcher

### Testing
- **`scripts/verify-mock-cycle.sh`** — Re-runnable regression test covering:
  - Upstream tests
  - Deterministic experiments
  - Adapter smoke tests
  - Hermes skill suite validation

---

## Usage

### Via Hermes Tool

bash
# Check current status
skillopt_run status

# Inspect pending proposals
skillopt_run inspect

# Run optimization cycle
skillopt_run run

# List available skills in manifest
skillopt_run manifest
### Via Cron Job

The `SkillOpt-Sleep Nightly Consolidation` cron runs every 6 hours to:
1. Harvest new sessions since last run
2. Mine for recurring task patterns
3. Generate bounded improvement proposals
4. Validate against held-out data
5. Stage approved proposals for review

---

## Safety Contract

### Read-Only Database Access
- Adapter opens `state.db` **read-only**
- No write operations to Hermes state

### Session Filtering
- Processes only **real user sessions**: `telegram`, `whatsapp`, `cli`
- **Excludes**: `cron` and `background` sessions (machine-generated, non-representative)

### Data Sanitization
- Session text is **clipped** before processing
- **Secret redaction** applied via SkillOpt's built-in sanitizer before:
  - Provider API calls
  - Output staging
  - Proposal generation

### Backup & Rollback
- All proposals staged before adoption
- Explicit human review gate before changes apply
- Automatic backup of original SKILL.md files

---

## Architecture Diagram

┌─────────────────────────────────────────────────────────────┐
│                    Hermes Agent                             │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │ skillopt_run│    │   state.db  │    │  cron job   │     │
│  │   (tool)    │───▶│ (read-only) │◀───│ (6h cycle)  │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              SkillOpt-Sleep Pipeline                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Sessions ──▶ Mine Tasks ──▶ Replay ──▶ Reflect            │
│      │                                           │          │
│      │         ┌─────────────────────┐           │          │
│      │         │  Validation Gate    │◀──────────┘          │
│      │         │  (held-out data)    │                      │
│      │         └──────────┬──────────┘                      │
│      │                    │                                  │
│      │         ┌──────────▼──────────┐                      │
│      │         │  Staged Proposal   │                      │
│      │         └──────────┬──────────┘                      │
│      │                    │                                  │
│      │         ┌──────────▼──────────┐                      │
│      │         │  Explicit Review   │                      │
│      │         └──────────┬──────────┘                      │
│      │                    │                                  │
│      │         ┌──────────▼──────────┐                      │
│      └────────▶│  Bounded Edit +     │                      │
│                │  Backup             │                      │
│                └─────────────────────┘                      │
└─────────────────────────────────────────────────────────────┘