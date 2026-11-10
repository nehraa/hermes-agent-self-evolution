---
category: software-development
name: proactive-agent-lite
description: Transform AI agents from task-followers into proactive partners with memory architecture, reverse prompting, and self-healing patterns. Lightweight version focused on core proactive capabilities.
metadata:
  {
    "openclaw":
      {
        "requires": {},
        "install": []
      }
  }
---

# Proactive Agent Lite

Transform your AI agents from passive task-followers into proactive partners that anticipate needs and continuously improve.

## Core Features

### Memory Architecture
Pre-compaction flush ensures context survives when the context window fills. When memory pressure exceeds threshold:
- Trigger checkpoint of working state before window resets
- Persist active context to long-term storage
- Restore seamlessly on next turn

### Reverse Prompting
Surfaces ideas and suggestions you didn't know to ask for by:
- Analyzing conversation patterns for unstated needs
- Identifying gaps in provided information
- Offering relevant context proactively

### Self-Healing Patterns
Automatically diagnoses and fixes issues:
- Detects inconsistencies in own responses
- Validates assumptions against provided context
- Recovers gracefully from errors without requiring user intervention

### Security Hardening
Built-in security considerations with safe defaults:
- Input sanitization before processing
- Rate limiting on repeated actions
- Audit trail for decision-making

### Alignment Systems
Stays on mission and remembers who it serves:
- Tracks primary objectives across session
- Validates actions against stated goals
- Maintains context of end-user identity

## Usage

yaml
# Enable proactive patterns in agent configuration
agent:
  proactive:
    enabled: true
    memory_flush_threshold: 0.85
    reverse_prompt_interval: 3
    self_heal: true
### Initialization
On agent startup, the skill injects:
1. Memory checkpoint handler
2. Proactive suggestion engine
3. Self-validation routines

### Runtime Behavior
- Every 3 interactions, evaluates whether to surface suggestions
- Monitors context utilization; triggers flush at 85% capacity
- Validates output consistency before responding

## Configuration Options

| Parameter | Default | Description |
|-----------|---------|-------------|
| `memory_flush_threshold` | 0.85 | Context utilization % to trigger memory flush |
| `reverse_prompt_interval` | 3 | Number of turns between reverse prompts |
| `self_heal_enabled` | true | Enable automatic error recovery |
| `initiative_level` | medium | `low` / `medium` / `high` — how often to suggest |
| `security_strict_mode` | false | Enable enhanced input validation |

## Integration

Combines with other skills:
- **Memory skills**: Extends context persistence beyond native limits
- **Reasoning skills**: Adds proactive suggestion layer to chain-of-thought
- **Security skills**: Multiplies validation checks

## Requirements

- OpenClaw v1.0 or higher
- Standard agent configuration

## Examples

**Before (passive):**
User: Fix the login bug
Agent: I'll investigate the login module...
**After (proactive):**
User: Fix the login bug
Agent: I'll investigate the login module. Also noticed the session token refresh logic in auth/service.ts might be related — I'll check both simultaneously.
## Limitations

- Does not persist memory across sessions (use persistent memory skills for that)
- Reverse prompts require minimum 3-turn conversation context
- Self-healing catches semantic inconsistencies, not syntax errors