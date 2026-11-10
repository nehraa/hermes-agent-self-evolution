---
name: python-telegram-bot-v22
description: "Build Telegram bots on python-telegram-bot v22+ — v22 API breakages (quote= → do_quote=), handler organization, long-polling, systemd user service, persistent-claude-session pattern (one chat = one long-running claude subprocess with steering/checkpointing/JSONL log), per-session cwd for /cd//ls//tree, five-layer logging discipline, silent-bot debugging recipe (7-step checklist), chat-scoped interactive-command state machine with 5 silent failure modes, MarkdownV2 escaping, _stdin_lock per-runner, image MIME sniffing, shlex.split, restart state reset, early-failure surfacing, safe_send do_quote TypeError black-hole, Claude Code JSONL queue-operation + subagent/ parsing quirks, buffered-event summarization loop with count/idle/result triggers, systemd-WorkingDirectory cwd pitfall, Telegram→CLI subprocess bridge architecture (Claude-bot reference), watchdog trap, session cwd registry for /resume, SteeringManager user_prompts[] pitfall. Use when building a Telegram bot, porting v20, debugging the quote= TypeError, wrapping a long-running coding agent, designing an interactive multi-step command flow, or diagnosing a bot that accepts messages but never replies."
category: software-development
version: 1.5.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags:
      - telegram
      - bot
      - python-telegram-bot
      - ptb
      - asyncio
      - systemd
      - claude-code
      - streaming
      - cli-bridge
    triggers:
      - "build a Telegram bot"
      - "telegram bot not responding"
      - "got an unexpected keyword argument 'quote'"
      - "Message.reply_text() got an unexpected keyword argument"
      - "PTB v22"
      - "python-telegram-bot upgrade"
      - "telegram claude code bridge"
      - "persistent claude session telegram"
      - "steering manager bot"
      - "stream-json claude subprocess"
      - "telegram /cd navigation"
      - "filesystem navigation telegram bot"
      - "telegram bot logs for diagnosis"
      - "bot handler not firing"
      - "bot replies not arriving"
      - "silent bot debugging"
      - "interactive command pattern"
      - "context.user_data state flag"
      - "telegram bot eat messages restart"
      - "chat-scoped state bot"
      - "interactive command mid-prompt state"
      - "user_data cross-chat leak"
      - "telegram cli bridge"
      - "no conversation found with session ID"
      - "watchdog killed my work"
    related_skills:
      - subagent-driven-development
      - requesting-code-review
      - hermes-content-filtering
---

# python-telegram-bot v22+ Development

## Core Capabilities

- **Bot Architecture**: Handler organization, long-polling setup, systemd user service deployment
- **v22 Migration**: Fix `quote=` → `do_quote=` API breakage; resolve `Message.reply_text()` unexpected keyword argument errors
- **Persistent Claude Sessions**: One chat = one long-running Claude subprocess with steering/checkpointing and JSONL logging
- **Per-Session Filesystem**: `/cd`, `/ls`, `/tree` commands with isolated working directories per session

## Debugging & Diagnostics

- **Five-Layer Logging Discipline**: Structured logging for diagnosis
- **Silent-Bot Debugging**: 7-step checklist when bot accepts messages but never replies
- **Early-Failure Surfacing**: Catch and report failures before they vanish
- **Watchdog Trap**: Handle watchdog timeouts gracefully

## Interactive Command Patterns

- **Chat-Scoped State Machine**: Interactive multi-step commands with `context.user_data` state flags
- **5 Silent Failure Modes**: Identify why commands fail without errors:
  1. State not set or reset on restart
  2. Cross-chat `user_data` leakage
  3. Handler not firing due to update filter mismatch
  4. Silent `safe_send` `do_quote` TypeError swallowing errors
  5. Buffered events never triggering summarization

## Advanced Integration

- **Telegram→CLI Bridge**: Pipe Telegram messages to subprocess and relay responses back
- **Claude Code JSONL Queue**: Handle streaming JSON with `subagent/` parsing quirks
- **Buffered Event Summarization**: Configurable triggers on count, idle time, or result count
- **SteeringManager**: Avoid `user_prompts[]` pitfalls when steering Claude

## Common Pitfalls

- `systemd-WorkingDirectory` cwd reset breaking per-session navigation
- `_stdin_lock` race conditions across parallel runners
- Image MIME sniffing failures
- `shlex.split` parsing edge cases
- MarkdownV2 special character escaping requirements

## Use When

- Building a Telegram bot from scratch
- Porting from python-telegram-bot v20 to v22+
- Debugging "bot accepts messages but never replies"
- Wrapping a long-running coding agent in Telegram
- Designing interactive multi-step command flows
- Diagnosing silent failures in existing bot infrastructure
- Creating a Claude Code Telegram bridge