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

### Component Paths

| Component | Path |
|-----------|------|
| Repository | `/home/Hermes/repos/skillopt/` |
| Isolated Python Environment | `/home/Hermes/repos/skillopt/.venv/` |
| Hermes Adapter | `/home/Hermes/.hermes/skillopt/hermes_skillopt.py` |
| Launcher Script | `/home/Hermes/.hermes/skillopt/run-hermes-skillopt.sh` |
| Gate Parser | `/home/Hermes/.hermes/skillopt/_parse_gate.py` |
| Working Directory | `/home/Hermes/.hermes/skillopt/` |
| Live Skills | `/home/Hermes/.hermes/skills/` (untouched by default) |

## Hermes Integration

### Tool Registration

**Tool Name:** `skillopt_run`

| Property | Value |
|----------|-------|
| Toolset | `skills` |
| Actions | `status`, `inspect`, `run`, `manifest` |

### Cron Job

| Property | Value |
|----------|-------|
| Name | `SkillOpt-Sleep Nightly Consolidation` |
| Job ID | `364ae7d380ff` |
| Frequency | Every 6 hours |
| Backend | Mock |
| Delivery | Local |
| Agent Mode | `no_agent` (watchdog) |

## Pipeline Stages

### 1. Harvest

Extracts session data from Hermes `state.db` using read-only access. Captures user prompts, agent responses, and metadata without modifying source data.

### 2. Mine

Analyzes harvested sessions to identify:
- Recurring task patterns
- Common workflows
- Improvement opportunities in existing skills
- Missing capabilities

### 3. Replay

Simulates identified patterns to validate their consistency and usefulness before proposing changes.

### 4. Reflect

Applies bounded edits to SKILL.md files based on mined insights. Edits are constrained to prevent runaway modifications:
- Maximum edit size limits
- Structured change boundaries
- Change density constraints

### 5. Validate

Held-out validation gate evaluates proposed changes against:
- Syntax correctness
- Schema compliance
- Semantic consistency with existing skills
- Safety rule adherence

### 6. Stage

Approved proposals are staged for review. Staging creates a diff view showing:
- Original content
- Proposed changes
- Change rationale

### 7. Adopt

After review approval, changes are adopted with:
- Automatic backup of original files
- Timestamp-based versioning
- Rollback capability

## Safety Contract

The integration enforces strict safety boundaries to prevent unintended modifications:

| Rule | Description |
|------|-------------|
| **Read-only state** | Adapter opens `state.db` in read-only mode only; no writes to source database |
| **Session filtering** | Processes only real user sessions (`telegram`, `whatsapp`, `cli`); excludes cron and background sessions (machine-generated) |
| **Secret redaction** | Text is clipped and SkillOpt's secret redaction applied before provider calls |
| **Pre-staging** | Uses runtime-sanitized diff generation before any filesystem operations |
| **Backup enforcement** | Original files backed up before any adoption; rollback possible on failure |
| **Bounded edits** | Edit size and density constrained; prevents runaway modifications |
| **Approval gate** | All changes require explicit review and approval before adoption |

## Usage

### Via Hermes Tool

bash
# Check SkillOpt status
skillopt_run status

# Inspect current skill state
skillopt_run inspect

# Run optimization pipeline
skillopt_run run

# List available skills in manifest
skillopt_run manifest
### Via Cron

The watchdog cron automatically runs every 6 hours without user intervention, staging proposals for review.

## Requirements

- Python 3.8+ with isolated virtual environment
- Hermes Agent with state.db access
- SkillOpt repository cloned at `/home/Hermes/repos/skillopt/`
- Write access to `/home/Hermes/.hermes/skillopt/` for staging and backups