---
category: software-development
description: When the user prompt contains "use tools", this skill activates. It forces
  deep context loading before execution.
name: use-tools
---

# SKILL.md — AI Agency: Use Tools Trigger

## Purpose
When the user prompt contains "use tools", this skill activates. It forces deep context loading before execution.

## Trigger
User message contains the exact phrase **"use tools"** (case-insensitive).

## Pre-Execution Context Loading (MANDATORY)

Before responding to any "use tools" prompt, read ALL of the following:

1. **TOOLS.md** — `~/.openclaw/workspace/TOOLS.md`
   - Available services, bridges, cron jobs, models
   - Hermes/DeerFlow/Scrapling bridge capabilities

2. **Skills folder** — `~/.openclaw/workspace/skills/`
   - List all available skills
   - Match user's intent to relevant skill(s)

3. **SOUL.md** — `~/.openclaw/workspace/SOUL.md`
   - Who I am, how I behave, boundaries

4. **Memory files** — `~/.openclaw/workspace/memory/`
   - Recent daily logs (today + yesterday)
   - Any context relevant to the task

5. **Skills index** — `~/ai-agents/awesome-agent-skills/skills-index.json`
   - 718+ indexed skills from VoltAgent's awesome-agent-skills
   - Match user's domain to available skill categories

## Execution Flow

```
User says "use tools" + task description
  ↓
Read TOOLS.md (services, bridges, tools available)
  ↓
Read skills/ folder (scan for matching skill)
  ↓
Read SOUL.md (personality, boundaries)
  ↓
Read memory/ files (recent context)
  ↓
Read skills-index.json (match domain → skill)
  ↓
SELECT best tool/bridge/skill for the task
  ↓
EXECUTE with full context
```

## Tool Selection Logic

| Task Type | Tool/Bridge | Command |
|-----------|-------------|---------|
| Terminal/shell | OpenClaw exec | `exec` directly |
| Docker/SSH | Hermes | `hermes.sh exec '<cmd>' docker` |
| Code sandbox | DeerFlow | `deerflow.sh sandbox '<code>' python` |
| Research | DeerFlow | `deerflow.sh research '<query>' deep` |
| Web scraping | Scrapling | `scrapling.sh get '<url>'` |
| Cloudflare bypass | Scrapling | `scrapling.sh stealthy '<url>' '' true` |
| Planning | DeerFlow | `deerflow.sh call planning '{"goal":"..."}'` |
| Subagent task | DeerFlow | `deerflow.sh call subagent_run '{"task":"..."}'` |
| Cron/schedule | OpenClaw cron | `cron add` |
| Memory store | OpenClaw memory | `memory_store` |
| File ops | OpenClaw read/write/edit | native tools |

## Domain Matching

When user's task matches a skill domain from the awesome-agent-skills index:
- Mention the skill exists and what it covers
- Suggest it as a reference for best practices
- Do NOT execute external skills directly — use the index as guidance

Example: "use tools to set up a Next.js app" → mention `vercel-labs/next-best-practices` exists, then use DeerFlow sandbox or direct exec to scaffold.

## Rules
1. NEVER skip the context loading steps
2. Always mention which tool/bridge you're using and why
3. If multiple tools could work, pick the most specific one
4. Report what you used after execution
