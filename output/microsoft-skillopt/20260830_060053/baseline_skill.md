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

Microsoft SkillOpt treats a natural-language skill document as trainable state. SkillOpt-Sleep applies that method to an agent's own sessions through a pipeline that:

1. **Harvests** read-only session data from Hermes
2. **Mines** recurring tasks and patterns
3. **Replays** identified patterns for analysis
4. **Reflects** with bounded edits to SKILL.md files
5. **Validates** through a held-out validation gate
6. **Stages** proposals for review
7. **Adopts** approved changes with automatic backups

## Architecture

### Installation Paths

| Component | Path |
|-----------|------|
| Repository | `/home/Hermes/repos/skillopt/` |
| Isolated Python | `/home/Hermes/repos/skillopt/.venv/` |
| Hermes Adapter | `/home/Hermes/.hermes/skillopt/hermes_skillopt.py` |
| Launcher Script | `/home/Hermes/.hermes/skillopt/run-hermes-skillopt.sh` |
| Gate Parser | `/home/Hermes/.hermes/skillopt/_parse_gate.py` |
| Working Directory | `/home/Hermes/.hermes/skillopt/` |
| Live Skills | `/home/Hermes/.hermes/skills/` (untouched by default) |

### Hermes Integration

**Tool:** `skillopt_run`
- Toolset: `skills`
- Actions: `status`, `inspect`, `run`, `manifest`

**Cron Job:** `SkillOpt-Sleep Nightly Consolidation`
- Job ID: `364ae7d380ff`
- Frequency: Every 6 hours
- Backend: Mock
- Delivery: Local

## Safety Contract

The integration enforces strict safety boundaries:

| Rule | Description |
|------|-------------|
| **Read-only state** | Adapter opens `state.db` in read-only mode only |
| **Session filtering** | Processes only real user sessions (`telegram`, `whatsapp`, `cli`); excludes cron and background sessions (machine-generated) |
| **Secret redaction** | Text is clipped and SkillOpt's secret redaction applied before provider calls |
| **Pre-staging** | Uses runtime-sanitizer patterns to prevent secret-shaped strings in `write_file` outputs |

## Reference Documentation

| Document | Purpose |
|----------|---------|
| `references/minimax-env-recipe.md` | Verified environment contract for MiniMax + SkillOpt-Sleep (auth mode, compat max tokens, troubleshooting matrix) |
| `references/runtime-sanitizer-patterns.md` | How Hermes runtime rewrites secret-shaped strings in `write_file` outputs and the pre-staging trick the launcher uses |
| `scripts/verify-mock-cycle.sh` | Re-runnable regression test covering upstream tests, deterministic experiments, adapter smoke test, and Hermes skill suite |

## Usage

### Via Hermes Tool

skillopt_run status    # Check current state and last run results
skillopt_run inspect   # View pending proposals
skillopt_run run       # Execute optimization cycle
skillopt_run manifest  # List tracked skills and their optimization status
### Via Cron

The `SkillOpt-Sleep Nightly Consolidation` cron job automatically runs every 6 hours, processing new session data and staging optimization proposals for review.