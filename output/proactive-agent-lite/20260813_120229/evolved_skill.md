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

Transform your AI agents from passive task-followers into proactive partners that anticipate needs, maintain context across sessions, and self-correct without intervention.

## Overview

This skill implements three core proactive capabilities:

1. **Memory Architecture** — Persists context beyond context window limits
2. **Reverse Prompting** — Surfaces relevant information proactively based on context
3. **Self-Healing** — Detects and resolves internal inconsistencies automatically

## Core Features

### Memory Architecture

Pre-compaction flush writes critical context to persistent storage before the context window fills. When the window resets, the agent retrieves this context and resumes seamlessly.

Memory flow:
  User Input → Working Context → [Pre-compaction Trigger]
              → Persistent Store ← Recovery on Context Reset
**What gets stored:**
- Current task state and progress
- Key decisions and their rationale
- Unresolved questions or pending follow-ups
- Relevant user preferences discovered during session

### Reverse Prompting

Instead of waiting for explicit requests, the agent monitors context and surfaces relevant information, suggestions, or warnings proactively.

**Triggers include:**
- Detecting potential security issues in user-provided code
- Identifying opportunities to complete related tasks
- Noticing missing information needed to complete current task
- Recognizing patterns from previous successful solutions

**Example behavior:**
Context: User is debugging an authentication flow
Agent action: "I notice you've fixed the token validation. 
Based on your recent pattern, you may also want to check 
the token refresh logic in token_service.py — it has a 
similar structure."
### Self-Healing Patterns

The agent monitors its own outputs and internal state for common failure modes:

| Issue | Detection | Resolution |
|-------|-----------|------------|
| Contradictory statements | Cross-reference recent outputs | Regenerate with corrected context |
| Hallucinated references | Validate against known facts | Acknowledge uncertainty, provide alternatives |
| Incomplete tool usage | Check tool response handling | Retry with corrected parameters or report failure |
| Context drift | Monitor alignment with original task | Redirect with reference to original objective |

## Configuration

Customize proactive behavior via `openclaw.yaml`:

yaml
proactive-agent-lite:
  memory:
    flush_threshold: 0.8  # Flush when 80% of context used
    priority_keys:
      - task_state
      - user_preferences
      - critical_decisions
  
  reverse_prompting:
    frequency: "moderate"  # "minimal" | "moderate" | "aggressive"
    silence_after_suggestion: 3  # Don't repeat for N interactions
  
  self_healing:
    enabled: true
    retry_attempts: 2
    escalate_on_failure: true
## Usage

Install the skill to enable proactive behaviors in all agent sessions. No explicit activation required.

bash
openclaw skill install proactive-agent-lite
## Requirements

- OpenClaw v1.0 or higher
- Persistent storage available for memory operations
- Standard agent configuration (no special permissions required)

## Best Practices

- **Start with defaults** — Use moderate settings initially, tune based on observed behavior
- **Monitor suggestions** — Review reverse prompt outputs to calibrate frequency
- **Review self-heals** — Check agent logs for self-healing events to understand behavior
- **Layer with domain skills** — Combine with domain-specific skills for targeted proactive assistance