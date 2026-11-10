---
category: software-development
description: When the user prompt contains "use tools", this skill activates. It forces deep context loading before execution.
name: use-tools
---

# use-tools

Forces comprehensive context loading whenever the user requests tool usage.

## Trigger Condition

Activates when the user message contains **"use tools"** (case-insensitive, anywhere in the prompt).

## Pre-Execution Requirements

Read ALL context files in the specified order BEFORE executing any task:

| Priority | File | Purpose |
|----------|------|---------|
| 1 | `~/.openclaw/workspace/TOOLS.md` | Available services, bridges, cron jobs, models |
| 2 | `~/.openclaw/workspace/skills/` | List all available skills; match to user intent |
| 3 | `~/.openclaw/workspace/SOUL.md` | Agent identity, behavior rules, boundaries |
| 4 | `~/.openclaw/workspace/memory/` | Today's and yesterday's logs; relevant context |
| 5 | `~/ai-agents/awesome-agent-skills/skills-index.json` | 718+ indexed skills from VoltAgent's awesome-agent-skills |

## Execution Flow

User Input: "use tools [task description]"
    │
    ▼
1. Load TOOLS.md → Identify available tools/bridges
    │
    ▼
2. Scan skills/ folder → Match user's intent to relevant skill(s)
    │
    ▼
3. Load SOUL.md → Apply personality and respect boundaries
    │
    ▼
4. Read memory/ files → Incorporate recent context
    │
    ▼
5. Query skills-index.json → Find domain-specific expertise
    │
    ▼
6. Select optimal tool/bridge/skill combination
    │
    ▼
7. Execute with full context awareness
## Tool Selection Matrix

| Task Domain | Primary Tool | Command Format |
|-------------|--------------|----------------|
| Terminal/shell commands | OpenClaw exec | `exec '<command>'` |
| Docker/SSH operations | Hermes bridge | `hermes.sh exec '<cmd>' docker` |
| Python code execution | DeerFlow sandbox | `deerflow.sh sandbox '<code>' python` |
| Deep research | DeerFlow research | `deerflow.sh research '<query>' deep` |
| Web page extraction | Scrapling | `scrapling.sh get '<url>'` |
| Cloudflare-protected sites | Scrapling stealth | `scrapling.sh stealthy '<url>' '' true` |
| Task planning | DeerFlow planning | `deerflow.sh call planning '{"goal":"..."}'` |
| Subagent delegation | DeerFlow subagent | `deerflow.sh call subagent_run '{"task":"..."}'` |
| Scheduled tasks | OpenClaw cron | `cron add <spec> <cmd>` |
| Persistent memory | OpenClaw memory | `memory_store <key> <value>` |
| File operations | OpenClaw native | `read` / `write` / `edit` |

## Domain Matching Strategy

1. Extract the primary domain from user's task description
2. Cross-reference with `skills-index.json` categories
3. If a matching indexed skill exists:
   - Load the skill file from `~/.openclaw/workspace/skills/`
   - Combine skill instructions with base tool capabilities
4. If no match, use direct tool selection from the matrix above

## Context Priority Rules

When context conflicts exist, apply this hierarchy:

1. **SOUL.md** — Identity and boundaries always take precedence
2. **TOOLS.md** — Available tools determine what's executable
3. **memory/** — Recent context overrides stale information
4. **skills/** — Explicit skill instructions override default behaviors
5. **skills-index.json** — Used only for discovery, not execution

## Output Requirements

After loading all context files, respond with:

- Confirmation of which files were loaded
- Selected tool(s) and justification
- Any relevant context from memory files
- Execution command(s) ready to run