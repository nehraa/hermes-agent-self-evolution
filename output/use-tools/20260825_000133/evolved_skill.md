---
category: software-development
description: When the user prompt contains "use tools", this skill activates. It forces deep context loading before execution.
name: use-tools
---

# use-tools — AI Agency Tool Invocation Skill

## Purpose

This skill activates when the user prompt contains **"use tools"**. It forces comprehensive context loading from multiple sources before executing any task, ensuring the agent has full awareness of available capabilities, recent history, and relevant skills.

## Trigger

User message contains the exact phrase **"use tools"** (case-insensitive).

---

## Pre-Execution Context Loading

**MANDATORY** — Read all files in the exact order listed below before responding to any "use tools" prompt:

### 1. TOOLS.md
**Path:** `~/.openclaw/workspace/TOOLS.md`

- Available services, bridges, and cron jobs
- Model configurations
- Hermes/DeerFlow/Scrapling bridge capabilities and endpoints

### 2. Skills Folder
**Path:** `~/.openclaw/workspace/skills/`

- Scan and list all available skills
- Match user intent to the most relevant skill(s) by keyword and domain

### 3. SOUL.md
**Path:** `~/.openclaw/workspace/SOUL.md`

- Agent identity and personality
- Behavioral guidelines and boundaries
- Communication style preferences

### 4. Memory Files
**Path:** `~/.openclaw/workspace/memory/`

- Today's daily log
- Yesterday's daily log
- Any context files relevant to the current task

### 5. Skills Index
**Path:** `~/ai-agents/awesome-agent-skills/skills-index.json`

- 718+ indexed skills from VoltAgent's awesome-agent-skills repository
- Match user domain to available skill categories

---

## Execution Flow

User prompt: "use tools" + task description
    │
    ▼
┌─────────────────────────────────────┐
│ 1. Read TOOLS.md                    │
│    → Identify available tools       │
│       and bridges                   │
└─────────────────┬───────────────────┘
                  ▼
┌─────────────────────────────────────┐
│ 2. Read skills/ folder             │
│    → Scan for matching skills       │
│       by name and domain            │
└─────────────────┬───────────────────┘
                  ▼
┌─────────────────────────────────────┐
│ 3. Read SOUL.md                     │
│    → Apply personality and          │
│       behavioral boundaries         │
└─────────────────┬───────────────────┘
                  ▼
┌─────────────────────────────────────┐
│ 4. Read memory/ files              │
│    → Load recent context           │
│       (today + yesterday)          │
└─────────────────┬───────────────────┘
                  ▼
┌─────────────────────────────────────┐
│ 5. Read skills-index.json          │
│    → Match domain to external       │
│       skill repository             │
└─────────────────┬───────────────────┘
                  ▼
┌─────────────────────────────────────┐
│ 6. SELECT best tool/bridge/skill   │
│    → Choose optimal execution       │
│       path for the task            │
└─────────────────┬───────────────────┘
                  ▼
         EXECUTE with full context
---

## Tool Selection Reference

### Terminal & Shell Operations

| Use Case | Tool | Command |
|----------|------|---------|
| Direct shell execution | OpenClaw exec | `exec` directly |
| Docker container commands | Hermes bridge | `hermes.sh exec '<cmd>' docker` |
| SSH remote execution | Hermes bridge | `hermes.sh exec '<cmd>' ssh '<host>'` |

### Code & Development

| Use Case | Tool | Command |
|----------|------|---------|
| Python code sandbox | DeerFlow | `deerflow.sh sandbox '<code>' python` |
| JavaScript/Node sandbox | DeerFlow | `deerflow.sh sandbox '<code>' node` |
| Code review | DeerFlow | `deerflow.sh call code_review '{"file":"..."}'` |

### Research & Data

| Use Case | Tool | Command |
|----------|------|---------|
| Deep research query | DeerFlow | `deerflow.sh research '<query>' deep` |
| Quick lookup | DeerFlow | `deerflow.sh research '<query>' fast` |
| Web content extraction | Scrapling | `scrapling.sh get '<url>'` |
| Bypassing Cloudflare | Scrapling | `scrapling.sh stealthy '<url>' '' true` |
| HTML parsing | Scrapling | `scrapling.sh parse '<url>' '<selector>'` |

### Planning & Automation

| Use Case | Tool | Command |
|----------|------|---------|
| Strategic planning | DeerFlow | `deerflow.sh call planning '{"goal":"..."}'` |
| Subagent delegation | DeerFlow | `deerflow.sh call subagent_run '{"task":"..."}'` |
| Task breakdown | DeerFlow | `deerflow.sh call breakdown '{"task":"..."}'` |

### System Operations

| Use Case | Tool | Command |
|----------|------|---------|
| Schedule recurring task | OpenClaw cron | `cron add '<schedule>' '<command>'` |
| Store persistent memory | OpenClaw memory | `memory_store '<key>' '<value>'` |
| Read file | OpenClaw read | `read '<path>'` |
| Write file | OpenClaw write | `write '<path>' '<content>'` |
| Edit file | OpenClaw edit | `edit '<path>' '<old>' '<new>'` |

---

## Domain Matching

When the user's task matches a domain category from `skills-index.json`, cross-reference with local skills in `~/.openclaw/workspace/skills/`:

1. **Extract domain keywords** from user prompt
2. **Match against index categories**: code, research, automation, devops, data, web, etc.
3. **Prioritize local skills** over external ones when functionality overlaps
4. **Return matched skill name and execution command** in response

---

## Error Handling

- If any required file is unreadable, log a warning and continue with available context
- If no matching tool/skill is found, respond with available alternatives and suggest manual tool specification
- If bridge commands fail, fall back to OpenClaw native tools where possible

---

## Summary

This skill ensures every "use tools" request is answered with full context awareness by mandating sequential loading of system configuration, skill inventory, agent identity, recent memory, and the external skills index. The execution flow guarantees informed tool selection before any command runs.