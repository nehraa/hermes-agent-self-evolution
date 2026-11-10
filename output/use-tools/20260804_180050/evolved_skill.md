---
category: software-development
description: When the user prompt contains "use tools", this skill activates. It forces deep context loading before execution.
name: use-tools
---

# use-tools Skill

## Purpose

This skill activates when a user prompt contains "use tools" (case-insensitive). It enforces mandatory deep context loading before executing any task, ensuring the agent has full awareness of available tools, skills, memory, and personality before responding.

## Trigger

**Activation phrase:** `"use tools"` (case-insensitive match)

Any user message containing this phrase activates this skill and mandates the full context loading sequence.

---

## Mandatory Pre-Execution Context Loading

Before responding to any "use tools" request, **read ALL** of the following files in order:

### 1. TOOLS.md
**Location:** `~/.openclaw/workspace/TOOLS.md`

Contains:
- Available services and bridges
- Cron jobs configuration
- Available models
- Hermes/DeerFlow/Scrapling bridge capabilities

### 2. Skills Folder
**Location:** `~/.openclaw/workspace/skills/`

Actions:
- List all available skills in the folder
- Match user's intent to relevant skill(s)
- Load matching skill files for reference

### 3. SOUL.md
**Location:** `~/.openclaw/workspace/SOUL.md`

Contains:
- Agent identity and personality
- Behavioral guidelines
- Operational boundaries and constraints

### 4. Memory Files
**Location:** `~/.openclaw/workspace/memory/`

Actions:
- Read today's daily log
- Read yesterday's daily log
- Load any context files relevant to the current task

### 5. Skills Index
**Location:** `~/ai-agents/awesome-agent-skills/skills-index.json`

Contains:
- 718+ indexed skills from VoltAgent's awesome-agent-skills repository
- Use for domain matching when local skills don't match

---

## Execution Flow

User Input: "use tools" + task description
    │
    ▼
Read TOOLS.md
    │
    ▼
Scan skills/ folder for matching skill
    │
    ▼
Read SOUL.md for personality & boundaries
    │
    ▼
Load memory/ files (today + yesterday)
    │
    ▼
Query skills-index.json for domain match
    │
    ▼
Select best tool/bridge/skill for task
    │
    ▼
Execute with full context loaded
---

## Tool Selection Matrix

Select the appropriate tool based on task type:

| Task Type | Tool/Bridge | Execution Command |
|-----------|-------------|-------------------|
| Terminal/shell commands | OpenClaw exec | Use `exec` directly |
| Docker containers | Hermes | `hermes.sh exec '<cmd>' docker` |
| SSH remote execution | Hermes | `hermes.sh exec '<cmd>' ssh` |
| Code execution/sandbox | DeerFlow | `deerflow.sh sandbox '<code>' python` |
| Deep research | DeerFlow | `deerflow.sh research '<query>' deep` |
| Web page scraping | Scrapling | `scrapling.sh get '<url>'` |
| Bypassing Cloudflare | Scrapling | `scrapling.sh stealthy '<url>' '' true` |
| Task planning | DeerFlow | `deerflow.sh call planning '{"goal":"..."}'` |
| Subagent delegation | DeerFlow | `deerflow.sh call subagent_run '{"task":"..."}'` |
| Scheduled tasks | OpenClaw cron | `cron add '<schedule>' '<command>'` |
| Persistent memory | OpenClaw memory | `memory_store '<key>' '<value>'` |
| File operations | OpenClaw native | Read/write/edit files directly |

---

## Domain Matching Strategy

When the user's task does not match a local skill in `skills/`:

1. Parse the task to identify the domain (e.g., "image processing", "API integration", "data analysis")
2. Query `skills-index.json` for skills in that domain
3. If a relevant indexed skill exists:
   - Load the skill definition
   - Adapt execution to match the skill's requirements
4. If no match found:
   - Fall back to core tools (terminal, file ops, DeerFlow)
   - Inform user of limited match and propose alternatives

---

## Important Notes

- **Never skip context loading** — even for simple tasks, the mandatory files must be read
- **Tool first, then skill** — prioritize native tools before external skills
- **Match intent, not keywords** — interpret what the user wants to accomplish, not just the words they use
- **Context compounds** — earlier context in the flow affects later decisions; read in order