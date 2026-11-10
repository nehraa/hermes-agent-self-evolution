---
category: software-development
description: When the user prompt contains "use tools", this skill activates. It forces deep context loading before execution.
name: use-tools
---

# Use Tools Trigger Skill

## Purpose

When a user includes **"use tools"** in their request, this skill activates to perform mandatory deep context loading before executing any task. This ensures the agent has full awareness of available capabilities, recent context, and optimal tool selection.

## Trigger

**Activation phrase:** `"use tools"` (case-insensitive, anywhere in the user message)

Example triggers:
- "use tools to analyze this code"
- "I need to use tools for this deployment"
- "use tools, then summarize what you found"

## Pre-Execution Context Loading

**MANDATORY** — Read ALL files in order before responding to any "use tools" prompt:

### 1. TOOLS.md
**Path:** `~/.openclaw/workspace/TOOLS.md`

Purpose: Discover available services, bridges, cron jobs, models, and tool capabilities including:
- Hermes bridge capabilities (Docker/SSH execution)
- DeerFlow bridge capabilities (sandbox, research, planning, subagent)
- Scrapling bridge capabilities (web scraping, stealth mode)
- Any OpenClaw native tools

### 2. Skills Directory
**Path:** `~/.openclaw/workspace/skills/`

Purpose: Find relevant skills for the user's task
- List all available skills
- Match user's intent to one or more relevant skills
- Note skill file paths for potential inclusion

### 3. SOUL.md
**Path:** `~/.openclaw/workspace/SOUL.md`

Purpose: Understand agent identity and boundaries
- Agent personality and behavior patterns
- Operational boundaries and limitations
- Response style guidelines

### 4. Memory Files
**Path:** `~/.openclaw/workspace/memory/`

Purpose: Load recent context
- Today's daily log
- Yesterday's daily log
- Any files relevant to the current task

### 5. Skills Index
**Path:** `~/ai-agents/awesome-agent-skills/skills-index.json`

Purpose: Access extended skill library
- 700+ indexed skills from VoltAgent's awesome-agent-skills repository
- Match user's domain to available skill categories
- Consider for complex or specialized tasks

## Execution Flow

User Input: "use tools" + task description
    │
    ▼
┌─────────────────────────────────────┐
│ MANDATORY CONTEXT LOADING           │
│                                     │
│ 1. Read TOOLS.md                    │
│ 2. Read skills/ directory           │
│ 3. Read SOUL.md                     │
│ 4. Read memory/ files               │
│ 5. Read skills-index.json           │
└─────────────────────────────────────┘
    │
    ▼
Analyze task type and requirements
    │
    ▼
┌─────────────────────────────────────┐
│ TOOL/BRIDGE SELECTION               │
│                                     │
│ Match task → optimal tool/bridge    │
│ Consider: efficiency, capability,   │
│           context window usage      │
└─────────────────────────────────────┘
    │
    ▼
EXECUTE with full context awareness
    │
    ▼
Return results to user
## Tool Selection Reference

### Terminal & System Operations

| Task | Tool | Command Syntax |
|------|------|----------------|
| Shell command | OpenClaw exec | `exec` — direct execution |
| Docker container | Hermes | `hermes.sh exec '<cmd>' docker` |
| SSH remote | Hermes | `hermes.sh exec '<cmd>' ssh '<host>'` |

### Code & Development

| Task | Tool | Command Syntax |
|------|------|----------------|
| Code execution | DeerFlow sandbox | `deerflow.sh sandbox '<code>' python` |
| Multi-file project | DeerFlow sandbox | `deerflow.sh sandbox '<code>' <lang>` |
| Code review | DeerFlow | `deerflow.sh call planning '{"goal":"review code"}'` |

### Research & Information

| Task | Tool | Command Syntax |
|------|------|----------------|
| Deep research | DeerFlow | `deerflow.sh research '<query>' deep` |
| Quick lookup | DeerFlow | `deerflow.sh research '<query>' quick` |
| Web page extraction | Scrapling | `scrapling.sh get '<url>'` |
| Bypassing protection | Scrapling stealth | `scrapling.sh stealthy '<url>' '' true` |

### Planning & Orchestration

| Task | Tool | Command Syntax |
|------|------|----------------|
| Task planning | DeerFlow | `deerflow.sh call planning '{"goal":"..."}'` |
| Subagent delegation | DeerFlow | `deerflow.sh call subagent_run '{"task":"..."}'` |

### Automation & Scheduling

| Task | Tool | Command Syntax |
|------|------|----------------|
| Schedule task | OpenClaw cron | `cron add '<schedule>' '<command>'` |
| List schedules | OpenClaw cron | `cron list` |
| Remove schedule | OpenClaw cron | `cron remove <id>` |

### Memory & Persistence

| Task | Tool | Command Syntax |
|------|------|----------------|
| Store information | OpenClaw memory | `memory_store '<key>' '<value>'` |
| Retrieve information | OpenClaw memory | `memory_get '<key>'` |

### File Operations

| Task | Tool | Command Syntax |
|------|------|----------------|
| Read file | OpenClaw read | `read` tool with file path |
| Write file | OpenClaw write | `write` tool with path and content |
| Edit file | OpenClaw edit | `edit` tool with path, old/new content |

## Domain Matching

When the user's task maps to a domain in the skills index:

1. Load the relevant skill file from `~/.openclaw/workspace/skills/`
2. Check `~/ai-agents/awesome-agent-skills/` for specialized implementations
3. If a specialized skill exists and is better suited than direct tool use, present both options to the user

### Common Domain Mappings

| User Intent | Domain | Primary Skill | Fallback Tool |
|-------------|--------|---------------|---------------|
| API development | backend, api | `api-development.md` | DeerFlow sandbox |
| Testing | testing, qa | `testing-skill.md` | DeerFlow sandbox |
| Documentation | docs, writing | `documentation.md` | Direct write |
| Deployment | devops, deploy | `deployment-skill.md` | Hermes exec |
| Data analysis | data, analytics | `data-analysis.md` | DeerFlow sandbox |
| Security audit | security | `security-audit.md` | DeerFlow sandbox |

## Error Handling

If a tool or bridge fails:

1. **Log the failure** in the current session memory
2. **Attempt fallback** — try the next best option from the selection matrix
3. **Report to user** — explain what failed and what alternatives were attempted
4. **Suggest** — recommend manual intervention if all tools fail

## Example Usage

### Example 1: Research Task
User: "use tools to research the latest React performance techniques"

Execution:
1. Load TOOLS.md → DeerFlow research available
2. Load skills/ → Check for React/web skills
3. Load memory/ → Check for any recent React context
4. Select: deerflow.sh research "React performance 2024" deep
5. Execute and return findings
### Example 2: Multi-Step Task
User: "use tools to deploy my app to staging and run the test suite"

Execution:
1. Load TOOLS.md → Hermes (deployment), DeerFlow (testing)
2. Load SOUL.md → Understand execution boundaries
3. Select: hermes.sh exec 'deploy.sh staging' docker
4. Then: deerflow.sh sandbox 'pytest' python
5. Return combined results
### Example 3: Ambiguous Task
User: "use tools to analyze this data"

Execution:
1. Load TOOLS.md → Multiple options available
2. Load skills/ → data-analysis skill exists
3. Present: "I found a data-analysis skill. Would you like me to:
   a) Use the data-analysis skill
   b) Use DeerFlow sandbox directly
   c) Use Scrapling to fetch data first?"
4. Execute based on user choice