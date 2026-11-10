---
category: software-development
description: When the user prompt contains "use tools", this skill activates. It forces deep context loading before execution.
name: use-tools
---

# Use Tools Skill

## Purpose

This skill activates when the user says "use tools" followed by a task description. It ensures **comprehensive context loading** before executing any tool, bridge, or skill — enabling informed, accurate responses instead of blind execution.

## Trigger

**Activation phrase:** `"use tools"` (case-insensitive)

Examples that trigger this skill:
- "use tools to deploy to production"
- "Use tools: analyze this codebase"
- "I need to use tools for web scraping"
## Pre-Execution Context Loading

**MANDATORY:** Read ALL files below before responding to any "use tools" prompt. Do not skip any step.

### Step 1: TOOLS.md
**Path:** `~/.openclaw/workspace/TOOLS.md`

Read this first to understand:
- Available services and bridges
- Cron jobs and scheduled tasks
- Available models (LLM, embedding)
- Hermes/DeerFlow/Scrapling bridge capabilities and limitations

### Step 2: Skills Folder
**Path:** `~/.openclaw/workspace/skills/`

Actions:
1. List all available skills in the folder
2. Identify skills matching the user's task domain
3. Note the trigger phrases and capabilities of matched skills

### Step 3: SOUL.md
**Path:** `~/.openclaw/workspace/SOUL.md`

Read to understand:
- Agent personality and behavior patterns
- Operational boundaries and constraints
- Communication style preferences

### Step 4: Memory Files
**Path:** `~/.openclaw/workspace/memory/`

Load in order:
1. Today's log (`memory/YYYY-MM-DD.md`)
2. Yesterday's log
3. Any files relevant to the current task

### Step 5: Skills Index
**Path:** `~/ai-agents/awesome-agent-skills/skills-index.json`

Contains 718+ indexed skills from VoltAgent's awesome-agent-skills repository.

**Match user's domain to available skill categories:**
- Identify the primary domain (e.g., data, web, devops, writing)
- Search index for relevant skills
- Note skill names and trigger conditions

## Execution Flow

User: "use tools" + task description
│
├─► Step 1: Read TOOLS.md
│        └─► What services/bridges are available?
│
├─► Step 2: Read skills/
│        └─► Which skills match this task?
│
├─► Step 3: Read SOUL.md
│        └─► How should I behave? What are my limits?
│
├─► Step 4: Read memory/
│        └─► What recent context exists?
│
├─► Step 5: Read skills-index.json
│        └─► What external skills apply?
│
└─► Step 6: SELECT best tool/bridge/skill
         └─► Execute with full context
## Tool Selection Reference

| Task Type | Tool/Bridge | Command Syntax |
|-----------|-------------|----------------|
| Terminal commands | OpenClaw exec | `exec` directly |
| Docker/SSH execution | Hermes | `hermes.sh exec '<cmd>' docker` |
| Python code execution | DeerFlow | `deerflow.sh sandbox '<code>' python` |
| Deep research | DeerFlow | `deerflow.sh research '<query>' deep` |
| Quick web search | DeerFlow | `deerflow.sh research '<query>' quick` |
| Fetch webpage content | Scrapling | `scrapling.sh get '<url>'` |
| Stealth web scraping | Scrapling | `scrapling.sh stealthy '<url>' '' true` |
| Complex planning | DeerFlow | `deerflow.sh call planning '{"goal":"..."}'` |
| Delegate to subagent | DeerFlow | `deerflow.sh call subagent_run '{"task":"..."}'` |
| Schedule recurring task | OpenClaw cron | `cron add <schedule> <command>` |
| Persistent memory | OpenClaw memory | `memory_store <key> <value>` |
| File read/write | OpenClaw native | `read`, `write`, `edit` tools |

## Decision Framework

### 1. Identify Task Category

Ask: What is the primary action?

- **Execute** → Use `exec` or Hermes
- **Research** → Use DeerFlow
- **Fetch** → Use Scrapling
- **Schedule** → Use `cron add`
- **Store** → Use `memory_store`

### 2. Match Skill if Available

Check `skills/` folder and `skills-index.json` for:

1. Exact match with user's request
2. Partial match requiring adaptation
3. No match → fall back to tool selection table

### 3. Consider Fallbacks

If primary tool fails:

| Primary | Fallback |
|---------|----------|
| DeerFlow research | DeerFlow sandbox with curl |
| Scrapling get | DeerFlow sandbox with requests |
| Hermes exec | DeerFlow sandbox |

## Output Requirements

After context loading and tool selection:

1. **Acknowledge** the task in user's terms
2. **Confirm** which tool/bridge/skill you're using
3. **Execute** with the loaded context
4. **Report** results with relevant details

## Error Handling

| Error | Response |
|-------|----------|
| Tool unavailable | Check alternative from tool table, then report inability |
| Context file missing | Log warning, continue with available context |
| Skill not found | Proceed with native tools, inform user |
| Execution failure | Attempt fallback, report full error details |

## Quick Reference Card

"use tools" detected → Load context in order:
1. TOOLS.md           (capabilities)
2. skills/            (available skills)
3. SOUL.md            (boundaries)
4. memory/            (recent context)
5. skills-index.json  (external skills)

Then:
→ Match task to tool/bridge/skill
→ Execute with full context
→ Report results