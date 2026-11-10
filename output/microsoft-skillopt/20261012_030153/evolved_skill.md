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

SkillOpt-Sleep transforms a Hermes agent's own session history into actionable skill improvements. It treats natural-language skill documents as trainable state, applying a disciplined pipeline that learns from past behavior while maintaining strict safety boundaries.

### Pipeline Stages

| Stage | Purpose |
|-------|---------|
| **Harvest** | Extract read-only session data from Hermes `state.db` |
| **Mine** | Identify recurring tasks, patterns, and frequent operations |
| **Replay** | Validate identified patterns through controlled playback |
| **Reflect** | Generate bounded edits to SKILL.md files |
| **Validate** | Pass proposals through a held-out validation gate |
| **Stage** | Present approved changes for human review |
| **Adopt** | Apply accepted changes with automatic backup |

## Architecture

### Directory Structure

/home/Hermes/repos/skillopt/           # SkillOpt repository
├── .venv/                             # Isolated Python environment
└── [skillopt source]

/home/Hermes/.hermes/skillopt/         # Hermes integration layer
├── hermes_skillopt.py                 # Hermes adapter (tool interface)
├── run-hermes-skillopt.sh             # Launcher script
├── _parse_gate.py                     # Validation gate parser
└── working directory for proposals

/home/Hermes/.hermes/skills/           # Live skill definitions (read-only by default)
### Hermes Integration

#### Tool: `skillopt_run`

| Property | Value |
|----------|-------|
| Toolset | `skills` |
| Actions | `status`, `inspect`, `run`, `manifest` |

**Usage Example:**

bash
# Check SkillOpt status
skillopt_run status

# Inspect current skill state
skillopt_run inspect

# Execute optimization pipeline
skillopt_run run

# List available skill manifests
skillopt_run manifest
#### Cron Job: `SkillOpt-Sleep Nightly Consolidation`

| Property | Value |
|----------|-------|
| Job ID | `364ae7d380ff` |
| Schedule | Every 6 hours |
| Backend | Mock |
| Delivery | Local |
| Agent Mode | `no_agent` (background operation) |

## Safety Contract

SkillOpt enforces strict safety boundaries to prevent unintended modifications:

| Rule | Enforcement |
|------|-------------|
| **Read-only state access** | Adapter opens `state.db` in read-only mode only |
| **Session filtering** | Processes only real user sessions (`telegram`, `whatsapp`, `cli`); excludes machine-generated sessions (cron, background jobs) |
| **Secret redaction** | Text is clipped and redacted before provider API calls |
| **Pre-staging requirement** | All changes must pass validation gate before staging |
| **Backup before adopt** | Automatic backup created before applying approved changes |

### Data Flow

Hermes Session Data (read-only)
    ↓
Session Filter (user-only)
    ↓
Secret Redaction
    ↓
Pattern Mining
    ↓
Validation Gate ← (blocking gate)
    ↓
Proposal Staging (review required)
    ↓
Human Approval
    ↓
Backup Creation
    ↓
Change Adoption
## Configuration

### Environment Requirements

- Python 3.10+ with isolated virtual environment (`.venv`)
- Read access to Hermes `state.db`
- Write access to `/home/Hermes/.hermes/skillopt/` for proposals and backups

### Validation Gate

The held-out validation gate prevents low-quality or unsafe proposals from reaching staging:

1. **Syntax validation** — Ensures SKILL.md remains valid YAML/frontmatter
2. **Semantic checks** — Validates skill metadata and structure
3. **Safety bounds** — Rejects edits that violate the safety contract
4. **Pattern confirmation** — Requires mined patterns to appear in multiple sessions

## Workflow Examples

### Manual Optimization Run

bash
# Invoke via Hermes tool
skillopt_run run --dry-run

# Review staged proposals
ls /home/Hermes/.hermes/skillopt/proposals/

# Apply approved changes
skillopt_run adopt --proposal <id>
### Viewing Optimization Status

bash
# Current status and last run info
skillopt_run status

# Detailed inspection of current skills
skillopt_run inspect --verbose

# List all managed skill manifests
skillopt_run manifest
## Troubleshooting

| Issue | Resolution |
|-------|------------|
| `state.db` access denied | Verify read permissions on Hermes data directory |
| No sessions found | Check that user sessions exist in `telegram`, `whatsapp`, or `cli` channels |
| Validation gate failures | Review `_parse_gate.py` output for specific rejection reasons |
| Empty proposal queue | Run with extended history window: `skillopt_run run --history-days 30` |

## References

- **Project Homepage:** https://github.com/microsoft/SkillOpt
- **SkillOpt-Sleep Documentation:** https://microsoft.github.io/SkillOpt/docs/sleep/README/