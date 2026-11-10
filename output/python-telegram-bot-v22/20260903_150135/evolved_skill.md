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
    related_skills: [subagent-driven-development, requesting-code-review, hermes-content]
---

# Python Telegram Bot v22+ Development

## Common Patterns

### v22 API Migration (`quote=` → `do_quote=`)

v22 renamed the `quote` parameter to `do_quote` across all reply methods:

python
# v20 (broken in v22)
await update.message.reply_text("text", quote=True)

# v22+ (correct)
await update.message.reply_text("text", do_quote=True)
This causes `TypeError: got an unexpected keyword argument 'quote'`.

### Persistent Claude Session Bridge Architecture

One chat = one long-running Claude subprocess with steering/checkpointing/JSONL logging:

Telegram User → Bot Handler → SteeringManager → Claude Code subprocess
                                   ↓
                              JSONL log file
                              Session cwd registry
**Key components:**

1. **Per-session CWD**: Each chat has its own working directory; `/cd`, `/ls`, `/tree` commands are session-scoped
2. **SteeringManager**: Maintains `user_prompts[]` array — beware of mutation pitfalls
3. **JSONL queue operations**: Parse `subagent/` prefixed lines carefully; buffer streaming output
4. **Watchdog trap**: External watchdog can kill subprocess mid-stream; implement graceful termination
5. **Session registry**: Maintain `session_id → cwd` mapping for `/resume` command

### safe_send Wrapper Pattern

Avoid the `do_quote` TypeError black-hole:

python
async def safe_send(context: CallbackContext, text: str, **kwargs):
    """Send with do_quote, guarding against early-failure surfacing issues."""
    try:
        await context.bot.send_message(
            chat_id=context._chat_id,
            text=text,
            do_quote=kwargs.get('do_quote', False),
            **kwargs
        )
    except TypeError as e:
        logger.error(f"safe_send failed: {e}")
        # Fallback: try without do_quote
        await context.bot.send_message(
            chat_id=context._chat_id,
            text=text,
            **kwargs
        )
### Interactive Command State Machine

5 silent failure modes to watch for:

1. **State flag not set**: `context.user_data['state']` not persisted correctly
2. **Mid-prompt interruption**: User sends new message before state resolves
3. **Cross-chat leak**: State persists across different chats using same user_data keys
4. **Restart state reset**: Bot restart clears `user_data` — implement persistence layer
5. **Handler priority conflict**: ConversationHandler vs callback handlers competing

python
# Chat-scoped state example
async def interactive_handler(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    
    if 'awaiting_input' not in context.user_data:
        context.user_data['awaiting_input'] = {}
    
    # Check if this chat is awaiting input
    if chat_id in context.user_data.get('awaiting_input', {}):
        # Process the input, then clear state
        del context.user_data['awaiting_input'][chat_id]
        return
    
    # Set state for next message
    if 'awaiting_input' not in context.user_data:
        context.user_data['awaiting_input'] = {}
    context.user_data['awaiting_input'][chat_id] = True
    
    await update.message.reply_text("Enter your input:")
### Buffered Event Summarization

python
class BufferedSummarizer:
    def __init__(self, count: int = None, idle: float = None, result: bool = None):
        self.count = count
        self.idle = idle  # seconds
        self.result = result  # callable returning bool
        self.buffer = []
        self.last_flush = time.time()
    
    async def add(self, event):
        self.buffer.append(event)
        
        if self.count and len(self.buffer) >= self.count:
            await self.flush()
        elif self.idle and (time.time() - self.last_flush) >= self.idle:
            await self.flush()
        elif self.result and self.result(self.buffer):
            await self.flush()
    
    async def flush(self):
        if not self.buffer:
            return
        # Summarize and send
        summary = "\n".join(str(e) for e in self.buffer)
        await self.send_summary(summary)
        self.buffer = []
        self.last_flush = time.time()
## Systemd User Service Setup

ini
[Unit]
Description=Telegram Bot
After=network.target

[Service]
Type=simple
WorkingDirectory=/path/to/bot
ExecStart=/usr/bin/python3 -m bot
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
**Critical pitfall**: `systemd-WorkingDirectory` sets initial CWD, but subprocess CWD resets independently. Use a session cwd registry for `/resume`.

## Five-Layer Logging Discipline

python
import logging

# Layer 1: Application
app_logger = logging.getLogger('bot.app')

# Layer 2: Handlers
handler_logger = logging.getLogger('bot.handlers')

# Layer 3: Subprocess/I/O
io_logger = logging.getLogger('bot.io')

# Layer 4: Telegram API
api_logger = logging.getLogger('bot.api')

# Layer 5: Debug (verbose)
debug_logger = logging.getLogger('bot.debug')

# Configure with different levels
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
## Silent Bot Debugging Checklist

When bot accepts messages but never replies:

1. **Verify long-polling**: Check logs for `Application.started()` and `update_queue` activity
2. **Check handler registration order**: More specific handlers must come before generic ones
3. **Inspect `context.user_data`**: Use `/debug` command to dump current state
4. **Test `do_quote`**: Ensure no TypeError silently swallowed by try/except
5. **Verify `_stdin_lock`**: If using per-runner locks, check for deadlock
6. **Check MIME sniffing**: For media, ensure `content_type` is correctly identified
7. **Enable debug logging**: `logging.getLogger('telegram').setLevel(logging.DEBUG)`

## Utility Helpers

### Image MIME Sniffing

python
from telegram.constants import ParseMode

async def get_mime_type(file_path: str) -> str:
    """Sniff MIME type from file bytes."""
    with open(file_path, 'rb') as f:
        header = f.read(8)
    
    if header[:3] == b'\xff\xd8\xff':
        return 'image/jpeg'
    elif header[:4] == b'\x89PNG':
        return 'image/png'
    elif header[:4] == b'GIF8':
        return 'image/gif'
    elif header[:4] == b'RIFF' and header[8:12] == b'WEBP':
        return 'image/webp'
    return 'application/octet-stream'
### Command Parsing

python
import shlex

def parse_command(text: str) -> tuple[str, list[str]]:
    """Safely parse command with arguments."""
    parts = shlex.split(text.strip())
    if not parts:
        return "", []
    return parts[0], parts[1:]
### MarkdownV2 Escaping

python
import re

def escape_markdownv2(text: str) -> str:
    """Escape special characters for MarkdownV2."""
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return ''.join('\\' + c if c in escape_chars else c for c in text)
## Quick Reference

| Issue | Solution |
|-------|----------|
| `quote=` TypeError | Replace with `do_quote=` (v22+) |
| Bot not responding | Run 7-step debugging checklist |
| State lost on restart | Implement user_data persistence layer |
| Cross-chat state leak | Use chat-scoped dictionaries |
| Watchdog kills subprocess | Implement graceful shutdown signal |
| `WorkingDirectory` cwd reset | Maintain session cwd registry |
| Silent failures | Enable debug logging; add try/except with surfacing |
| Handler not firing | Check registration order; verify filters |