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
---

# Python Telegram Bot v22+ Skill

Comprehensive guide for building production Telegram bots using python-telegram-bot v22+, with emphasis on common pitfalls, async patterns, and Claude Code integration.

## v22 API Breaking Changes

### quote= → do_quote=

**Problem:** `Message.reply_text(quote=True)` raises `TypeError: got an unexpected keyword argument 'quote'`

**Cause:** PTB v22 renamed the parameter from `quote=` to `do_quote=`

**Fix:**
python
# v20 (broken in v22)
await message.reply_text("hello", quote=True)

# v22 (correct)
await message.reply_text("hello", do_quote=True)
**Global replacement pattern:**
bash
sed -i 's/\.reply_text(\([^)]*\)quote=/.reply_text(\1do_quote=/g' *.py
## Bot Architecture

### Long-Polling Setup

python
import logging
from telegram.ext import Application, CommandHandler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG  # Use DEBUG for diagnosis
)

app = Application.builder().token(os.getenv("BOT_TOKEN")).build()
app.add_handler(CommandHandler("start", start_handler))
app.run_polling(drop_pending_updates=True)
### Handler Organization

- **Use ConversationHandler** for multi-step flows
- **Register handlers early** — first match wins
- **Group related handlers** with HandlerGroup
- **Use filters** to narrow matches before processing

python
# Correct order: specific → general
app.add_handler(CommandHandler("cancel", cancel))  # First
app.add_handler(ConversationHandler(entry_points=[...], states={...}))  # Second
app.add_handler(MessageHandler(filters.TEXT, echo))  # Last resort
## Persistent Claude Session Pattern

### Architecture Overview

┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Telegram  │────▶│  Python Bot  │────▶│ Claude Code │
│    Chat     │◀────│  (steering)  │◀────│  Subprocess │
└─────────────┘     └──────────────┘     └─────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  JSONL Log   │
                    │ (session     │
                    │  history)    │
                    └──────────────┘
### Session Lifecycle

python
class SessionManager:
    def __init__(self, chat_id: int):
        self.chat_id = chat_id
        self.cwd = Path.home()
        self.process = None
        self.output_queue = asyncio.Queue()
        self._stdin_lock = asyncio.Lock()
        
    async def start_session(self):
        """Launch Claude Code subprocess for this chat."""
        self.process = await asyncio.create_subprocess_exec(
            *["claude", "--no-history"],
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(self.cwd)
        )
        # Start stream reader task
        
    async def send(self, prompt: str) -> str:
        """Send prompt to Claude, return response."""
        async with self._stdin_lock:  # Serialize writes
            self.process.stdin.write(f"{prompt}\n".encode())
            await self.process.stdin.drain()
        return await self._read_response()
### SteeringManager Pattern

**Pitfall:** `user_prompts[]` can grow unbounded, causing memory issues.

python
class SteeringManager:
    def __init__(self, max_history: int = 50):
        self.user_prompts: list[dict] = []
        self.max_history = max_history
        
    def add_prompt(self, role: str, content: str):
        self.user_prompts.append({"role": role, "content": content})
        # Prevent unbounded growth
        if len(self.user_prompts) > self.max_history:
            self.user_prompts = self.user_prompts[-self.max_history:]
## Per-Session Filesystem Navigation

### /cd, /ls, /tree Commands

python
from pathlib import Path
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

async def cmd_cd(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    session = get_session(chat_id)
    
    if not context.args:
        session.cwd = Path.home()
    else:
        new_path = session.cwd / context.args[0]
        if new_path.is_dir():
            session.cwd = new_path.resolve()
        else:
            await update.message.reply_text(f"❌ Not a directory: {new_path}")
            return
            
    await update.message.reply_text(f"📁 {session.cwd}")

# Register session cwd for resume
SESSION_CWD_REGISTRY[chat_id] = session.cwd
### /resume After Restart

python
def restore_sessions():
    """Called on bot startup to recover session state."""
    for chat_id, cwd_path in SESSION_CWD_REGISTRY.items():
        session = create_session(chat_id)
        session.cwd = cwd_path
        # Don't restart running processes — mark as "needs resume"
        session.needs_resume = True
## Five-Layer Logging Discipline

python
# Layer 1: Telegram API layer (DEBUG)
logging.getLogger("telegram.ext.Application").setLevel(logging.DEBUG)

# Layer 2: Bot handlers (DEBUG)
logging.getLogger("bot.handlers").setLevel(logging.DEBUG)

# Layer 3: Session/Claude bridge (DEBUG)
logging.getLogger("bot.session").setLevel(logging.DEBUG)

# Layer 4: Subprocess I/O (INFO for stdin/stdout, WARNING for errors)
logging.getLogger("bot.subprocess").setLevel(logging.INFO)

# Layer 5: Application state (INFO)
logging.getLogger("bot.state").setLevel(logging.INFO)

# Full config example
logging.basicConfig(
    format="%(asctime)s | %(name)-20s | %(levelname)-8s | %(message)s",
    level=logging.DEBUG,
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()
    ]
)
## Silent Bot Debugging Recipe

### 7-Step Checklist

1. **Verify bot token**
   ```python
   bot = Bot(token=os.getenv("BOT_TOKEN"))
   me = await bot.get_me()
   print(f"Bot username: @{me.username}")
   ```

2. **Check pending updates**
   ```python
   app.run_polling(drop_pending_updates=True)
   ```

3. **Enable DEBUG logging**
   ```python
   logging.getLogger("telegram").setLevel(logging.DEBUG)
   ```

4. **Verify handler registration**
   ```python
   print("Registered handlers:", app.handlers)
   ```

5. **Test single handler in isolation**
   ```python
   # Add only ONE handler, test, then add more
   ```

6. **Check user_data isolation**
   ```python
   # Clear per-user state on restart
   context.user_data.clear()
   ```

7. **Test with actual Telegram** (not test updates)
   - Delete and recreate bot chat
   - Send /start directly to bot

## Chat-Scoped Interactive Command State Machine

### Pattern with 5 Silent Failure Modes

python
from enum import Enum, auto

class InteractiveState(Enum):
    IDLE = auto()
    AWAITING_INPUT = auto()
    PROCESSING = auto()

async def interactive_command(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    
    # Set state using chat_id as key (NOT user_id alone)
    state_key = f"interactive_{chat_id}"
    context.chat_data[state_key] = InteractiveState.AWAITING_INPUT
    context.chat_data[f"{state_key}_step"] = 0
    
    await update.message.reply_text("Enter your input:")

async def handle_interactive_response(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    state_key = f"interactive_{chat_id}"
    
    current_state = context.chat_data.get(state_key)
    
    if current_state != InteractiveState.AWAITING_INPUT:
        return  # Silent failure: not in expected state
    
    # Process input...
### Failure Mode Reference

| Mode | Symptom | Cause | Fix |
|------|---------|-------|-----|
| 1 | Bot eats messages after restart | State reset, but user still in flow | Clear state on startup or use ConversationHandler |
| 2 | Cross-chat state leak | Using `context.user_data` shared across chats | Use `context.chat_data` for chat-scoped state |
| 3 | Mid-prompt state loss | Handler not matching after network blip | Persist state to disk, restore on startup |
| 4 | Double-processing | Handler firing twice | Use `filters.TEXT & ~filters.COMMAND` |
| 5 | Silent ignore | Handler returning without reply | Add logging, verify state transitions |

## MarkdownV2 Escaping

python
import re

def escape_markdown_v2(text: str) -> str:
    """Escape special characters for Telegram MarkdownV2."""
    # Order matters: escape backslash first
    escape_chars = r'\_*[]()~`>#+-=|{}.!'
    for char in escape_chars:
        text = text.replace(char, f'\\{char}')
    return text

# Usage
await update.message.reply_text(
    escape_markdown_v2("File: test.txt (exists)"),
    parse_mode="MarkdownV2"
)
## Systemd User Service

### Service File

ini
[Unit]
Description=Telegram Bot Service
After=network.target

[Service]
Type=simple
User=%u
WorkingDirectory=%h/bots/mybot
ExecStart=/usr/bin/python3 /home/user/bots/mybot/bot.py
Restart=on-failure
RestartSec=5
Environment=BOT_TOKEN=your_token_here

# CRITICAL: WorkingDirectory sets initial cwd
# Per-session cwd is managed in-app via SESSION_CWD_REGISTRY

[Install]
WantedBy=default.target
### Commands

bash
# Reload after code changes
systemctl --user daemon-reload
systemctl --user restart telegram-bot

# View logs
journalctl --user-unit telegram-bot -f

# Check status
systemctl --user status telegram-bot
## safe_send Pattern (do_quote TypeError Black-Hole)

python
async def safe_send(update: Update, text: str, **kwargs):
    """Safely send message, handling common errors."""
    try:
        # Use do_quote= explicitly (v22 compatibility)
        await update.message.reply_text(
            text,
            do_quote=False,  # or True based on need
            **kwargs
        )
    except TypeError as e:
        # Catch the quote= → do_quote= migration error
        logging.error(f"Safe send failed: {e}")
        # Retry with corrected parameters
        await update.message.reply_text(text, **kwargs)
## Claude Code JSONL Queue Operations

### Subagent Response Parsing

python
async def parse_claude_stream(stream_reader: asyncio.StreamReader):
    """Parse Claude Code streaming JSONL output."""
    buffer = ""
    async for line in stream_reader:
        buffer += line.decode()
        while "\n" in buffer:
            line, buffer = buffer.split("\n", 1)
            if not line.strip():
                continue
            try:
                data = json.loads(line)
                # Handle subagent / parsing
                if data.get("type") == "subagent":
                    yield parse_subagent_response(data)
                elif data.get("type") == "result":
                    yield parse_result(data)
            except json.JSONDecodeError:
                logging.warning(f"Malformed JSONL: {line}")
## Buffered Event Summarization

python
class EventBuffer:
    def __init__(self, count_trigger: int = 10, idle_seconds: int = 5):
        self.buffer: list[dict] = []
        self.count_trigger = count_trigger
        self.idle_seconds = idle_seconds
        self._idle_timer: asyncio.Task | None = None
        
    async def add(self, event: dict, result_callback):
        self.buffer.append(event)
        
        # Trigger 1: Count threshold
        if len(self.buffer) >= self.count_trigger:
            await self.flush(result_callback)
            return
            
        # Trigger 2: Idle timeout
        if self._idle_timer:
            self._idle_timer.cancel()
        self._idle_timer = asyncio.create_task(
            self._idle_wait(result_callback)
        )
        
    async def _idle_wait(self, callback):
        await asyncio.sleep(self.idle_seconds)
        if self.buffer:
            await self.flush(callback)
## Watchdog Trap

python
import signal

# WARNING: Watchdog may kill long-running Claude sessions
# Configure appropriately for your use case

# Option 1: Disable watchdog entirely
app.run_polling(drop_pending_updates=True, watchdog=None)

# Option 2: Increase watchdog timeout for Claude sessions
# (not directly supported; handle in subprocess instead)

# Option 3: Catch SIGALRM in subprocess
def no_alarm_handler(signum, frame):
    pass
signal.signal(signal.SIGALRM, no_alarm_handler)
## Image MIME Sniffing

python
from pathlib import Path

async def get_mime_type(file_path: Path) -> str:
    """Determine MIME type from file content, not extension."""
    with open(file_path, "rb") as f:
        header = f.read(8)
    
    # PNG: 89 50 4E 47
    if header[:4] == b"\x89PNG":
        return "image/png"
    # JPEG: FF D8 FF
    if header[:3] == b"\xFF\xD8\xFF":
        return "image/jpeg"
    # GIF: 47 49 46 38
    if header[:4] == b"GIF8":
        return "image/gif"
    # WebP: 52 49 46 46 ... 57 45 42 50
    if header[:4] == b"RIFF" and header[8:12] == b"WEBP":
        return "image/webp"
    
    return "application/octet-stream"
## shlex.split for Command Parsing

python
import shlex

async def parse_command(text: str) -> tuple[str, list[str]]:
    """Properly parse shell-like command syntax."""
    parts = shlex.split(text)
    if not parts:
        return "", []
    command = parts[0]
    args = parts[1:]
    return command, args

# Usage
# "/run find . -name '*.py'" → ("run", ["find", ".", "-name", "*.py"])
## Quick Reference

| Issue | Quick Fix |
|-------|-----------|
| `quote=` TypeError | Change to `do_quote=` |
| Bot not responding | Add `drop_pending_updates=True` |
| State lost on restart | Use `SESSION_CWD_REGISTRY` persistence |
| Cross-chat leak | Use `chat_data` not `user_data` |
| Markdown parse error | Use `escape_markdown_v2()` |
| Silent failures | Enable DEBUG logging |
| Watchdog kills work | Set `watchdog=None` in `run_polling` |