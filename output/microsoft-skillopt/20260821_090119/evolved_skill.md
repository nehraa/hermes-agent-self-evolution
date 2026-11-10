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

### Component Locations

| Component | Path |
|-----------|------|
| Repository | `/home/Hermes/repos/skillopt/` |
| Isolated Python Environment | `/home/Hermes/repos/skillopt/.venv/` |
| Hermes Adapter | `/home/Hermes/.hermes/skillopt/hermes_skillopt.py` |
| Launcher Script | `/home/Hermes/.hermes/skillopt/run-hermes-skillopt.sh` |
| Gate Parser | `/home/Hermes/.hermes/skillopt/_parse_gate.py` |
| Working Directory | `/home/Hermes/.hermes/skillopt/` |
| Live Skills | `/home/Hermes/.hermes/skills/` (untouched by default) |

### Hermes Integration

**Tool:** `skillopt_run`

| Property | Value |
|----------|-------|
| Toolset | `skills` |
| Actions | `status`, `inspect`, `run`, `manifest` |

**Cron Job:** `SkillOpt-Sleep Nightly Consolidation`

| Property | Value |
|----------|-------|
| Job ID | `364ae7d380ff` |
| Frequency | Every 6 hours |
| Backend | Mock |
| Delivery | Local |

## Pipeline Stages

### 1. Harvest

Extracts read-only session data from Hermes `state.db`. All database access uses read-only mode to prevent accidental mutations.

### 2. Mine

Analyzes harvested sessions to identify:
- Recurring task patterns
- Frequent tool sequences
- Common failure modes
- Successful workflow patterns

### 3. Replay

Simulates identified patterns to validate they represent genuine improvements rather than noise or one-off events.

### 4. Reflect

Generates bounded edits to target SKILL.md files. Bounded edits ensure:
- Changes are scoped to specific sections
- No wholesale rewrites
- Reviewable diffs

### 5. Validate

Applies a held-out validation gate that tests proposed changes against:
- Existing test suites (if present)
- Syntax and format validation
- Consistency checks with other skills

### 6. Stage

Places validated proposals in a review queue. Proposals include:
- Diff view of proposed changes
- Validation results
- Confidence metrics

### 7. Adopt

Upon approval, changes are applied with automatic backup. Rollback is supported by restoring from the most recent backup.

## Safety Contract

The integration enforces strict safety boundaries to prevent unintended modifications:

| Rule | Description |
|------|-------------|
| **Read-only state** | Adapter opens `state.db` in read-only mode only; never writes to the database |
| **Session filtering** | Processes only real user sessions (`telegram`, `whatsapp`, `cli`); excludes cron and background sessions (machine-generated events) |
| **Secret redaction** | All text is clipped and processed through SkillOpt's secret redaction before any provider calls |
| **Pre-staging** | Uses runtime-sandboxed pre-staging before final adoption |
| **Automatic backups** | Full backup of target SKILL.md before any change; rollback path always available |
| **No live skill modification** | Live skills in `/home/Hermes/.hermes/skills/` are untouched by default; changes require explicit approval |

## Usage

### Via Hermes Tool

bash
skillopt_run status
skillopt_run inspect <skill-name>
skillopt_run run --target <skill-name>
skillopt_run manifest
### Via Cron Job

The watchdog cron runs automatically every 6 hours, processing new sessions and staging any detected improvements.

### Manual Trigger

bash
/home/Hermes/.hermes/skillopt/run-hermes-skillopt.sh
## Validation Gate

The held-out validation gate ensures proposed changes meet quality thresholds before staging:

1. **Syntax validation** — Markdown is well-formed
2. **Schema validation** — YAML frontmatter matches expected structure
3. **Contextual validation** — Changes don't conflict with other skill definitions
4. **Safety validation** — No destructive operations or secret exposure

Failed validation results in rejection with an explanation. Approved changes proceed to staging for human review.

## Rollback

To revert an adopted change:

1. Locate the backup in the working directory
2. Restore the target SKILL.md from the most recent backup
3. Verify restoration via `skillopt_run inspect <skill-name>`

## Requirements

- Python 3.10+
- Hermes Agent with skillopt repository cloned
- Read access to `state.db`
- Network access for provider calls (redaction pipeline)

## References

- **Homepage:** https://github.com/microsoft/SkillOpt
- **Documentation:** https://microsoft.github.io/SkillOpt/docs/sleep/README/