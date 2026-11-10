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
      - hermes-content-generation
---

# Python Telegram Bot (v22+) Development Skill

## Overview

This skill covers building production-grade Telegram bots using `python-telegram-bot` v22+, with emphasis on async patterns, persistent sessions, and CLI integration bridges.

---

## Core Topics

### API Breaking Changes (v20 → v22)

- **`quote=` → `do_quote=`**: The `Message.reply_text()` parameter renamed in v22. Causes `TypeError: got an unexpected keyword argument 'quote'`.
- **Early-failure surfacing**: v22 throws errors immediately on invalid parameters rather than silent failures.

### Handler Organization

- **Handler registration order**: More specific handlers must precede generic ones.
- **Handler not firing**: Check handler registration order and decorator placement.
- **Per-runner `_stdin_lock`**: Prevents stdin contention when multiple bot instances run.

### Long-Polling & Deployment

- **Long-polling**: Default polling mode; configure `allowed_updates` to control which updates the bot receives.
- **Systemd user service**: Deploy as user-level service for isolated runtime.
- **systemd `WorkingDirectory` cwd pitfall**: If set incorrectly, relative paths break on restart.

### Persistent Claude Session Pattern

One chat = one long-running Claude Code subprocess with:

- **Steering/checkpointing**: Send directives mid-session without restarting.
- **JSONL logging**: Structured audit trail of all interactions.
- **Per-session cwd**: Each session maintains its own working directory.
- **`/resume` command**: Session cwd registry maps chat IDs to their last working directories.
- **SteeringManager `user_prompts[]` pitfall**: Array accumulates prompts across calls; clear or manage explicitly.
- **Claude Code JSONL quirks**: `queue-operation` and `subagent/` output require special parsing.
- **Watchdog trap**: Timeout kills subprocesses mid-work; configure carefully.

### Chat-Scoped Interactive Command State Machine

- **State stored in `context.user_data`**: Key for per-user state flags.
- **5 silent failure modes**:
  1. State not set after command completes (can't enter next step).
  2. State persists after restart (stale state).
  3. State leaks between chats (`user_data` misconfiguration).
  4. Handler fires before state check (order issue).
  5. Mid-prompt interruption leaves incomplete state.

- **Restart state reset**: On bot restart, clear or validate all `user_data`.

### CLI Bridge Architecture

- **Telegram → CLI subprocess**: Messages forwarded to subprocess; responses streamed back.
- **`safe_send` do_quote TypeError**: Common black-hole failure where errors are swallowed.
- **Buffered event summarization loop**: Aggregates events with `count`/`idle`/`result` triggers.
- **Image MIME sniffing**: Detect image types before processing.

### Utilities & Edge Cases

- **`shlex.split`**: Safely parse user input with spaces/quotes.
- **MarkdownV2 escaping**: Telegram's strict markdown requires escaping special characters.
- **Five-layer logging discipline**: Implement DEBUG/INFO/WARNING/ERROR/CRITICAL separation.

---

## Silent Bot Debugging Recipe

When bot accepts messages but never replies:

1. **Check handler registration order** — specific handlers before generic.
2. **Verify `allowed_updates`** — includes `message` if using message handlers.
3. **Inspect `context.user_data`** — stale state from previous sessions.
4. **Check logging output** — set DEBUG level to see handler invocation.
5. **Test `do_quote` parameter** — v22 compatibility issue.
6. **Review `safe_send` error handling** — TypeErrors may be swallowed.
7. **Confirm subprocess alive** — watchdog or crash may have killed it.

---

## Common Error Patterns

| Error | Cause | Fix |
|-------|-------|-----|
| `unexpected keyword argument 'quote'` | v20 → v22 migration | Replace `quote=` with `do_quote=` |
| Bot accepts but never replies | Handler order or `allowed_updates` | Reorder handlers; verify update types |
| `no conversation found with session ID` | Session not initialized | Ensure session created before state commands |
| State leaks between chats | `user_data` scope | Use chat_id as prefix for all state keys |
| `watchdog killed my work` | Timeout too aggressive | Increase or disable watchdog timeout |

---

## When to Use This Skill

Use this skill when:

- Building a new Telegram bot with PTB v22+
- Porting a v20 bot to v22
- Debugging `quote=` TypeErrors
- Wrapping Claude Code in a Telegram interface
- Designing multi-step interactive commands
- Diagnosing silent bot failures (receives but doesn't reply)
- Implementing persistent session with per-chat working directories
- Setting up systemd deployment for long-running bots