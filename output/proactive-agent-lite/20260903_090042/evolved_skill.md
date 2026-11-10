---
category: software-development
name: proactive-agent-lite
description: Transform AI agents from task-followers into proactive partners with memory architecture, reverse prompting, and self-healing patterns. Lightweight version focused on core proactive capabilities.
metadata:
  {
    "openclaw": {
      "requires": {},
      "install": []
    }
  }
---

# Proactive Agent Lite

Transform your AI agents from passive task-followers into proactive partners that anticipate needs and continuously improve.

## Overview

This skill provides lightweight proactive capabilities for OpenClaw agents:

- **Memory persistence** across context window boundaries
- **Context surfacing** to reveal relevant information the user hasn't explicitly requested
- **Self-diagnosis** to identify and recover from errors
- **Mission alignment** to maintain focus on core objectives

## Core Features

### Memory Architecture

Maintains working memory state across context compaction events. When the context window approaches capacity, the agent:

1. Identifies the most contextually relevant memories
2. Flushes them to a persistent memory store before compaction
3. Rehydrates these memories when the new context window initializes

This prevents loss of important context, user preferences, and ongoing project state.

### Context Surfacing (Reverse Prompting)

Instead of waiting for explicit questions, the agent:

1. Monitors conversation context for implicit needs
2. Surfaces relevant information proactively (e.g., "You mentioned X earlier — here's an update that might affect it")
3. Suggests actions based on patterns in the conversation

### Self-Healing Patterns

When the agent detects errors or inconsistencies, it:

1. Logs the diagnosis with root cause analysis
2. Attempts corrective action based on proven patterns
3. Falls back gracefully if self-healing fails
4. Notifies the user if manual intervention is required

### Security Hardening

- Validates all file system operations against allowlists
- Sanitizes command injection attempts
- Defaults to read-only mode for unknown operations
- Logs security-relevant actions for audit

## Usage

Activate by including this skill in your agent's skill configuration:

yaml
skills:
  - proactive-agent-lite
The agent will automatically begin:

- Preserving context across sessions
- Surfacing relevant information without prompting
- Attempting self-recovery on errors

## Configuration

Customize behavior via agent configuration:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `proactive_suggestions` | `true` | Enable unsolicited suggestions |
| `memory_flush_threshold` | `80%` | Context usage before flush |
| `self_heal_enabled` | `true` | Allow automatic error recovery |
| `security_mode` | `paranoid` | Security validation level |

## Limitations

- Memory persistence requires a compatible storage backend
- Self-healing cannot fix logic errors or hallucinated knowledge
- Suggestions may not always be relevant — use judgment before acting

## Requirements

- OpenClaw agent running v1.0 or higher
- Persistent storage for memory state (if memory features enabled)