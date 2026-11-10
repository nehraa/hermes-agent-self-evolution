---
name: python-telegram-bot-v22
description: "Build Telegram bots on python-telegram-bot v22+ — v22 API breakages (quote= → do_quote=), handler organization, long-polling, systemd user service, persistent-claude-session pattern (one chat = one long-running claude subprocess with steering/checkpointing/JSONL log), per-session cwd for /cd//ls//tree, five-layer logging discipline, silent-bot debugging recipe (7-step checklist), chat-scoped interactive-command state machine with 5 silent failure modes, MarkdownV2 escaping, _stdin_lock per-runner, image MIME sniffing, shlex.split, restart state reset, early-failure surfacing, safe_send do_quote TypeError black-hole, Claude Code JSONL queue-operation + subagent/ parsing quirks, buffered-event summarization loop with count/idle/result triggers, systemd-WorkingDirectory cwd pitfall, Telegram→CLI subprocess bridge architecture (Claude-bot reference), watchdog trap, session cwd registry for /resume, SteeringManager user_prompts[] pitfall. Use when building a Telegram bot, porting v20, debugging the quote= TypeError, wrapping a long-running coding agent, designing an interactive multi-step command flow, or diagnosing a bot that accepts messages but never replies."
category: software-development
version: 1.5.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [telegram, bot, python-telegram-bot, ptb, asyncio, systemd, claude-code, streaming, cli-bridge]
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
    related_skills: [subagent-driven-development, requesting-code-review, hermes-content-generation]
---

# python-telegram-bot v22+ Skill

## Overview

This skill covers building production Telegram bots using `python-telegram-bot` v22+, with emphasis on:

- **API migration** from v20 (breaking changes)
- **Persistent session architectures** for long-running agents
- **Interactive command flows** with chat-scoped state
- **Silent failure debugging** when bots accept messages but never reply
- **Systemd deployment** with proper working directory handling

## When to Use This Skill

Use this skill when:

1. Building a new Telegram bot with python-telegram-bot
2. Porting a bot from v20 to v22+
3. Debugging `got an unexpected keyword argument 'quote'` errors
4. Implementing persistent Claude Code sessions via Telegram
5. Designing multi-step interactive command flows
6. Diagnosing a bot that silently fails to respond
7. Setting up a Telegram→CLI subprocess bridge

---

## API Migration: v20 → v22 Breaking Changes

### The `quote=` Parameter Renamed

**Error:** `Message.reply_text() got an unexpected keyword argument 'quote'`

**Fix:** Rename all `quote=` to `do_quote=`

python
# v20
await message.reply_text("Hello", quote=True)

# v22+
await message.reply_text("Hello", do_quote=True)
### Safe Send Pattern

When wrapping `reply_text` in try/catch, the `quote`→`do_quote` rename can cause silent failures:

python
async def safe_send(context, chat_id, text, **kwargs):
    """Safely send message, surfacing do_quote TypeErrors."""
    try:
        await context.bot.send_message(chat_id, text, **kwargs)
    except TypeError as e:
        if "do_quote" in str(e):
            # Black hole trap: remove the offending param and retry
            kwargs.pop("do_quote", None)
            await context.bot.send_message(chat_id, text, **kwargs)
        else:
            raise
---

## Handler Organization

### Recommended Pattern: Command + Callback Router

python
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

async def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("Option A", callback_data="opt_a")],
        [InlineKeyboardButton("Option B", callback_data="opt_b")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose:", reply_markup=reply_markup)

async def button_handler(update: Update, context):
    query = update.callback_query
    await query.answer()
    
    if query.data == "opt_a":
        await query.edit_message_text("You chose A")
    elif query.data == "opt_b":
        await query.edit_message_text("You chose B")

app = Application.builder().token("BOT_TOKEN").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
### Handler Not Firing? Checklist

1. Handler registered **before** other handlers that might consume updates
2. `app.add_handler()` called **after** `app.initialize()`, not before `build()`
3. Conversation handler groups: lower group = higher priority
4. Check if `MessageHandler` with filters is overriding specific handlers

---

## Persistent Claude Session Architecture

### Core Pattern: One Chat = One Long-Running Subprocess

┌─────────────────────────────────────────────────────────┐
│                      Telegram Chat                       │
│  [User] ────────► [Bot] ────────► [Claude Subprocess]   │
│                    │                     │               │
│              /restart              stdin/stdout          │
│              /resume               JSONL logging         │
│              /cancel               checkpoint files      │
└─────────────────────────────────────────────────────────┘
### Session Registry

python
import asyncio
from pathlib import Path

class SessionRegistry:
    """Tracks active Claude Code sessions per chat."""
    
    def __init__(self, base_dir: Path = Path("~/.claude-sessions")):
        self.base_dir = base_dir.expanduser()
        self.sessions: dict[int, dict] = {}  # chat_id -> session info
        self._lock = asyncio.Lock()
    
    async def get_cwd(self, chat_id: int) -> Path:
        """Get or create per-session working directory."""
        async with self._lock:
            if chat_id not in self.sessions:
                session_dir = self.base_dir / f"chat_{chat_id}"
                session_dir.mkdir(parents=True, exist_ok=True)
                self.sessions[chat_id] = {
                    "cwd": session_dir,
                    "process": None,
                    "last_activity": None,
                }
            return self.sessions[chat_id]["cwd"]
    
    async def cleanup(self, chat_id: int):
        """Kill subprocess and cleanup on restart."""
        async with self._lock:
            if chat_id in self.sessions:
                proc = self.sessions[chat_id]["process"]
                if proc and proc.poll() is None:
                    proc.terminate()
                    try:
                        proc.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        proc.kill()
                del self.sessions[chat_id]
### JSONL Logging

python
import json
from datetime import datetime

def log_event(chat_id: int, event_type: str, data: dict):
    log_path = f"/tmp/claude-session-{chat_id}.jsonl"
    with open(log_path, "a") as f:
        f.write(json.dumps({
            "timestamp": datetime.utcnow().isoformat(),
            "chat_id": chat_id,
            "type": event_type,
            **data
        }) + "\n")
---

## Chat-Scoped Interactive Command State Machine

### State Flag Pattern

python
from telegram.ext import ContextTypes

# Define states as an enum or constants
class CommandState:
    NONE = "none"
    AWAITING_CONFIRMATION = "awaiting_confirmation"
    AWAITING_INPUT = "awaiting_input"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = context.user_data.get("command_state", CommandState.NONE)
    
    if state == CommandState.AWAITING_CONFIRMATION:
        await handle_confirmation(update, context)
        return
    
    if state == CommandState.AWAITING_INPUT:
        await handle_input(update, context)
        return
    
    # Normal command routing
    text = update.message.text.strip().lower()
    
    if text == "/confirm":
        await update.message.reply_text("Are you sure? Reply yes/no")
        context.user_data["command_state"] = CommandState.AWAITING_CONFIRMATION
        context.user_data["pending_action"] = "delete_files"
        return
    
    await update.message.reply_text("Send /confirm to proceed")
### Five Silent Failure Modes

| Failure Mode | Symptom | Cause | Fix |
|--------------|---------|-------|-----|
| **Missing `return`** | Handler continues to process | No `return` after state transition | Add `return` after setting state |
| **Cross-chat leak** | Bot responds in wrong chat | `user_data` not scoped by chat | Use `context.chat_data` instead |
| **State not reset on error** | Bot stuck in wrong state after exception | Missing try/finally | Reset state in finally block |
| **Race condition** | Duplicate state transitions | Concurrent handlers | Add `asyncio.Lock` per chat |
| **Restart state leak** | Old state persists after `/restart` | Session cleanup incomplete | Explicitly reset all `user_data` keys |

python
async def handle_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()
    
    try:
        if text in ("yes", "y"):
            action = context.user_data.get("pending_action")
            await execute_action(action, update, context)
        else:
            await update.message.reply_text("Cancelled.")
    finally:
        # Always reset state, even on error
        context.user_data["command_state"] = CommandState.NONE
        context.user_data.pop("pending_action", None)
---

## Filesystem Navigation Commands

### Per-Session Working Directory

python
async def cmd_cd(update: Update, context):
    """Change session's working directory."""
    if not context.args:
        cwd = await session_registry.get_cwd(update.effective_chat.id)
        await update.message.reply_text(f"Current: `{cwd}`", parse_mode="MarkdownV2")
        return
    
    target = " ".join(context.args)
    cwd = await session_registry.get_cwd(update.effective_chat.id)
    new_path = (cwd / target).resolve()
    
    if not new_path.exists():
        await update.message.reply_text(f"Directory not found: {target}")
        return
    
    if new_path.is_file():
        await update.message.reply_text(f"Not a directory: {target}")
        return
    
    session_registry.sessions[update.effective_chat.id]["cwd"] = new_path
    await update.message.reply_text(f"Changed to: `{new_path}`", parse_mode="MarkdownV2")

async def cmd_ls(update: Update, context):
    """List files in session's working directory."""
    cwd = await session_registry.get_cwd(update.effective_chat.id)
    
    try:
        entries = sorted(cwd.iterdir())
        lines = [f"`{p.name}`" + ("/" if p.is_dir() else "") for p in entries]
        text = "\n".join(lines) if lines else "(empty)"
        await update.message.reply_text(text, parse_mode="MarkdownV2")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def cmd_tree(update: Update, context):
    """Display directory tree."""
    cwd = await session_registry.get_cwd(update.effective_chat.id)
    lines = ["."]
    _build_tree(cwd, lines, prefix="", max_depth=3)
    await update.message.reply_text("\n".join(lines), parse_mode="MarkdownV2")
### Parsing User Input

Use `shlex.split` for safe command parsing with quoted arguments:

python
import shlex

def parse_command(text: str) -> tuple[str, list[str]]:
    """Safely parse command with shlex."""
    try:
        parts = shlex.split(text.strip())
    except ValueError:
        return "", []
    
    if not parts:
        return "", []
    
    command = parts[0].lstrip("/")
    args = parts[1:]
    return command, args
---

## Long-Running Claude Subprocess Integration

### Claude Code JSONL Parsing

python
import asyncio
import json
import re
from typing import Optional

async def stream_claude_output(process: asyncio.subprocess.Process, chat_id: int):
    """Parse streaming JSON from Claude Code subprocess."""
    buffer = ""
    
    while True:
        try:
            line = await asyncio.wait_for(process.stdout.readline(), timeout=60)
        except asyncio.TimeoutError:
            await log_event(chat_id, "timeout", {})
            continue
        
        if not line:
            break  # Process ended
        
        buffer += line.decode("utf-8")
        
        # Claude Code streams JSON objects that may be incomplete
        while "\n" in buffer:
            line_end = buffer.index("\n")
            json_str = buffer[:line_end]
            buffer = buffer[line_end + 1:]
            
            try:
                obj = json.loads(json_str)
                await handle_claude_event(chat_id, obj)
            except json.JSONDecodeError:
                # Incomplete JSON, continue buffering
                buffer = json_str + buffer
                break

async def handle_claude_event(chat_id: int, event: dict):
    """Route Claude Code events to appropriate handlers."""
    subtype = event.get("type") or event.get("subtype")
    
    if subtype == "subagent":
        # Parse subagent delegation
        match = re.search(r"subagent[/\s]+(\w+)", event.get("text", ""))
        if match:
            await log_event(chat_id, "subagent_delegation", {"target": match.group(1)})
    
    elif subtype == "result":
        await log_event(chat_id, "task_complete", {"result": event.get("text", "")})
### SteeringManager with user_prompts[]

**Pitfall:** SteeringManager accumulates `user_prompts[]` indefinitely, causing context overflow.

python
class BoundedSteeringManager:
    """SteeringManager that limits prompt history."""
    
    MAX_PROMPTS = 50
    
    def __init__(self, steering: SteeringManager):
        self.steering = steering
        self._prompt_count = 0
    
    async def add_prompt(self, prompt: str):
        self.steering.user_prompts.append(prompt)
        self._prompt_count += 1
        
        # Rotate oldest prompts when limit exceeded
        if self._prompt_count > self.MAX_PROMPTS:
            excess = self._prompt_count - self.MAX_PROMPTS
            self.steering.user_prompts = self.steering.user_prompts[excess:]
            self._prompt_count = self.MAX_PROMPTS
---

## Buffered Event Summarization Loop

Avoid sending every token update; batch with triggers:

python
from telegram.ext import ContextTypes

class BufferedSummarizer:
    """Buffer events and send summary when triggers fire."""
    
    def __init__(
        self,
        chat_id: int,
        send_func: callable,
        count_trigger: int = 10,
        idle_trigger: float = 5.0,
        result_trigger: bool = True,
    ):
        self.chat_id = chat_id
        self.send_func = send_func
        self.count_trigger = count_trigger
        self.idle_trigger = idle_trigger
        self.result_trigger = result_trigger
        
        self.buffer: list[dict] = []
        self.last_send = asyncio.get_event_loop().time()
        self._task: Optional[asyncio.Task] = None
    
    def add_event(self, event: dict):
        self.buffer.append(event)
        
        # Check triggers
        should_send = (
            len(self.buffer) >= self.count_trigger or
            self.result_trigger and event.get("type") == "result"
        )
        
        if should_send:
            asyncio.create_task(self.flush())
        else:
            # Start idle timer if not running
            if self._task is None:
                self._task = asyncio.create_task(self._idle_flush())
    
    async def _idle_flush(self):
        await asyncio.sleep(self.idle_trigger)
        await self.flush()
        self._task = None
    
    async def flush(self):
        if not self.buffer:
            return
        
        summary = self._summarize(self.buffer)
        await self.send_func(summary)
        self.buffer = []
        self.last_send = asyncio.get_event_loop().time()
    
    def _summarize(self, events: list[dict]) -> str:
        types = set(e.get("type", "unknown") for e in events)
        return f"📊 Update: {len(events)} events [{', '.join(types)}]"
---

## Five-Layer Logging Discipline

For production debugging, log at five levels:

python
import logging

# Layer 1: Core application events
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s APP %(levelname)s %(message)s",
    handlers=[logging.FileHandler("/var/log/bot/app.log")]
)

# Layer 2: Telegram API interactions
telegram_logger = logging.getLogger("telegram")
telegram_logger.setLevel(logging.DEBUG)

# Layer 3: User command processing
command_logger = logging.getLogger("commands")
command_logger.propagate = False
command_logger.addHandler(logging.FileHandler("/var/log/bot/commands.log"))

# Layer 4: Subprocess I/O (Claude Code bridge)
subprocess_logger = logging.getLogger("subprocess")
subprocess_logger.setLevel(logging.DEBUG)

# Layer 5: State transitions
state_logger = logging.getLogger("state")
state_logger.info(f"chat_id={chat_id} transition: {old} -> {new}")

# Structured logging helper
def log_command(chat_id: int, command: str, args: list, result: str):
    logging.getLogger("commands").info(json.dumps({
        "chat_id": chat_id,
        "command": command,
        "args": args,
        "result": result,
        "ts": datetime.utcnow().isoformat()
    }))
---

## Silent Bot Debugging: 7-Step Checklist

When a bot accepts messages but never replies:

### Step 1: Verify Token and Network
bash
curl -s https://api.telegram.org/bot<TOKEN>/getMe
### Step 2: Check Webhook vs Polling
python
# If using polling:
app.run_polling(allowed_updates=Update.ALL_TYPES)
# NOT just run_webhooks
### Step 3: Enable Debug Logging
python
logging.basicConfig(level=logging.DEBUG)
# Check for: "No handlers matched" warnings
### Step 4: Verify Handler Registration Order
python
# More specific handlers FIRST
app.add_handler(CallbackQueryHandler(...))  # Before CommandHandler
app.add_handler(CommandHandler("start", ...))
app.add_handler(MessageHandler(filters.TEXT, ...))  # Catch-all LAST
### Step 5: Check ConversationHandler Group
python
# Lower group = higher priority
app.add_handler(conv_handler, group=0)  # Runs before group=1 handlers
### Step 6: Verify Update Types
python
# Explicitly request MESSAGE updates
app.run_polling(allowed_updates=["message", "callback_query"])
# By default, some update types may be excluded
### Step 7: Test with Echo Command
python
async def echo(update: Update, context):
    await update.message.reply_text(update.message.text)

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
If echo fails, the issue is in handler infrastructure, not business logic.

---

## Systemd User Service Deployment

### Service File: `~/.config/systemd/user/telegram-bot.service`

ini
[Unit]
Description=Telegram Bot Service
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
# CRITICAL: Set WorkingDirectory to session base
WorkingDirectory=/home/user/.claude-sessions
ExecStart=/usr/bin/python3 /opt/bot/bot.py
Restart=always
RestartSec=10
Environment=PYTHONUNBUFFERED=1

# Logging
StandardOutput=journal
StandardError=journal
SyslogIdentifier=telegram-bot

[Install]
WantedBy=default.target
### WorkingDirectory Pitfall

**Symptom:** Bot works when run manually, fails when started via systemd.

**Cause:** `WorkingDirectory` defaults to `/`, so relative paths break.

**Fix:** Explicitly set `WorkingDirectory` to your session base directory, or use absolute paths everywhere.

bash
systemctl --user daemon-reload
systemctl --user enable --now telegram-bot
journalctl --user -u telegram-bot -f
---

## Watchdog Pattern

Protect long-running operations from being killed:

python
import signal
from telegram.ext import ContextTypes

class WatchdogManager:
    """Watchdog that kills work after timeout."""
    
    def __init__(self, timeout: int = 300):
        self.timeout = timeout
        self._watchdog_task: Optional[asyncio.Task] = None
        self._interrupted = False
    
    async def run_with_watchdog(self, coro, chat_id: int):
        """Run coroutine with watchdog protection."""
        
        async def watchdog():
            await asyncio.sleep(self.timeout)
            if not self._interrupted:
                await log_event(chat_id, "watchdog_kill", {"timeout": self.timeout})
                # Could send interrupt signal to subprocess here
                raise asyncio.CancelledError("Watchdog triggered")
        
        self._watchdog_task = asyncio.create_task(watchdog())
        try:
            result = await coro
            self._watchdog_task.cancel()
            return result
        except asyncio.CancelledError:
            await log_event(chat_id, "task_cancelled", {"reason": "watchdog"})
            raise
        finally:
            self._watchdog_task = None
            self._interrupted = False
---

## Image MIME Sniffing

When receiving photos, detect actual MIME type:

python
import imghdr

async def get_image_type(file_path: str) -> str:
    """Detect image MIME type from file content."""
    mime = imghdr.what(file_path)
    mime_map = {
        "jpeg": "image/jpeg",
        "png": "image/png",
        "gif": "image/gif",
        "webp": "image/webp",
    }
    return mime_map.get(mime, "application/octet-stream")

# Usage with Telegram file
file = await context.bot.get_file(update.message.photo[-1].file_id)
await file.download_to_drive("/tmp/photo.jpg")
mime = await get_image_type("/tmp/photo.jpg")
---

## MarkdownV2 Escaping

Telegram's `MarkdownV2` requires escaping special characters:

python
import re

MARKDOWN_V2_ESCAPE = re.compile(r'([_*\[\]()~`>#+\-=|{}.!\\])')

def escape_markdown_v2(text: str) -> str:
    """Escape special characters for MarkdownV2 parse mode."""
    return MARKDOWN_V2_ESCAPE.sub(r'\\\1', text)

# Usage
await update.message.reply_text(
    escape_markdown_v2("File: /path/to/file.txt (created 2024-01-15)"),
    parse_mode="MarkdownV2"
)
---

## Early Failure Surfacing

Log failures immediately, don't let them silently propagate:

python
async def command_handler(update: Update, context):
    try:
        await process_command(update, context)
    except Exception as e:
        logging.exception(f"Command failed for chat_id={update.effective_chat.id}")
        try:
            await update.message.reply_text(
                f"❌ Error: {escape_markdown_v2(str(e))}",
                parse_mode="MarkdownV2"
            )
        except Exception as send_error:
            logging.error(f"Failed to send error message: {send_error}")
---

## Related Skills

- **subagent-driven-development** — Orchestrating Claude Code subagents
- **requesting-code-review** — Getting code reviews via Telegram bot
- **hermes-content-generation** — AI-powered content generation patterns