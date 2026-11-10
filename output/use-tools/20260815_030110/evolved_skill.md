---
category: software-development
description: When the user prompt contains "use tools", this skill activates. It forces deep context loading before execution.
name: use-tools
---

# Use Tools Skill

Forces comprehensive context loading before executing any tool-related request.

## Trigger

Activated when the user message contains **"use tools"** (case-insensitive).

## Pre-Execution Context Loading

Before responding to any "use tools" request, read ALL of the following files in order:

### 1. TOOLS.md — `~/.openclaw/workspace/TOOLS.md`
- Available services, bridges, cron jobs, and models
- Hermes/DeerFlow/Scrapling bridge capabilities
- API endpoints and authentication requirements

### 2. Skills Folder — `~/.openclaw/workspace/skills/`
- List all available skills in the directory
- Match user intent to the most relevant skill(s)
- Note skill parameters and requirements

### 3. SOUL.md — `~/.openclaw/workspace/SOUL.md`
- Agent identity and personality
- Behavioral boundaries and constraints
- Response style guidelines

### 4. Memory Files — `~/.openclaw/workspace/memory/`
- Today's daily log: `memory/daily/YYYY-MM-DD.md`
- Yesterday's daily log: `memory/daily/YYYY-MM-DD.md`
- Any context files relevant to the current task

### 5. Skills Index — `~/ai-agents/awesome-agent-skills/skills-index.json`
- 718+ indexed skills from VoltAgent's awesome-agent-skills repository
- Match user domain to available skill categories
- Note skill names and descriptions for potential invocation

## Execution Flow

User: "use tools" + task description
  │
  ▼
Read TOOLS.md
  │ → Identify available tools, bridges, services
  ▼
Read skills/ folder
  │ → Find matching skill(s) for the task
  ▼
Read SOUL.md
  │ → Apply personality and boundary rules
  ▼
Read memory/ files
  │ → Load recent context and session history
  ▼
Read skills-index.json
  │ → Match domain to external skills if needed
  ▼
SELECT optimal tool/bridge/skill combination
  │
  ▼
EXECUTE with full context loaded
## Tool Selection Reference

Use this mapping to select the appropriate tool:

| Task Type | Tool/Bridge | Invocation |
|-----------|-------------|------------|
| Terminal commands | OpenClaw exec | `exec '<command>'` |
| Docker containers | Hermes | `hermes.sh exec '<cmd>' docker` |
| SSH remote execution | Hermes | `hermes.sh exec '<cmd>' ssh` |
| Python code execution | DeerFlow | `deerflow.sh sandbox '<code>' python` |
| Deep research | DeerFlow | `deerflow.sh research '<query>' deep` |
| Web page scraping | Scrapling | `scrapling.sh get '<url>'` |
| Cloudflare-protected sites | Scrapling | `scrapling.sh stealthy '<url>' '' true` |
| Task planning | DeerFlow | `deerflow.sh call planning '{"goal":"..."}'` |
| Subagent delegation | DeerFlow | `deerflow.sh call subagent_run '{"task":"..."}'` |
| Scheduled jobs | OpenClaw cron | `cron add '<schedule>' '<command>'` |
| Persistent memory | OpenClaw memory | `memory_store '<key>' '<value>'` |
| File operations | OpenClaw native | `read` / `write` / `edit` |

## Domain Matching

When the user's task matches a skill domain from `skills-index.json`:

1. Identify the matching skill category (e.g., `web`, `data`, `code`, `devops`)
2. Read the referenced skill file if it exists locally
3. Load skill parameters and required configuration
4. Combine skill execution with appropriate tool/bridge
5. Return combined results to user

## Important Notes

- **Always load context before execution** — never skip the pre-execution steps
- **Match multiple tools if needed** — complex tasks may require chained execution
- **Check SOUL.md boundaries** — ensure task complies with behavioral rules
- **Use memory context** — incorporate recent history for coherent responses
- **External skills take precedence** — if a dedicated skill exists for the task, use it before generic tools