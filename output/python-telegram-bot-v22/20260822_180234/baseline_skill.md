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
    related_skills: [subagent-driven-development, requesting-code-review, hermes-content-filter-quirks]
---

# python-telegram-bot v22 Patterns

python-telegram-bot (PTB) v22 is the actively maintained release as of 2026. v21+ broke
several v20-era APIs. This skill captures the patterns that work and the bugs that bite
when wiring a bot end-to-end on this server.

## When to load

- "Build a Telegram bot that does X"
- Porting an old PTB v20 bot to current
- Hitting `TypeError: Message.reply_text() got an unexpected keyword argument 'quote'`
  in production logs
- Debugging `RuntimeError: This object has no bot associated with it`
- Wiring a bot as a systemd user-mode service (`.config/systemd/user/<name>.service`)
- Setting up long-polling vs webhook
- Adding custom slash commands, voice message handling, photo analysis

## v20 → v22 API breakage (the big ones)

### `quote=` → `do_quote=`

PTB v21 renamed the `quote` parameter across `reply_text`, `reply_photo`, `reply_audio`,
`reply_video`, `reply_document`, `reply_voice`, `reply_location`, etc. v22 keeps the rename.

**Old (v20):**
```python
await update.message.reply_text("hello", quote=True)
```

**New (v22):**
```python
await update.message.reply_text("hello", do_quote=True)
```

This applies to every `reply_*` shortcut. v20 code that runs under v22 crashes with
`TypeError: Message.reply_text() got an unexpected keyword argument 'quote'` on EVERY
incoming message — no warning, no deprecation, just hard failure.

**Migration: one-shot sed replacement:**
```bash
# Inside the bot file only — not other files that may legitimately use quote=
sed -i 's/\breply_text(\(.*\), quote=/reply_text(\1, do_quote=/g' bot.py
sed -i 's/\breply_text(\(.*\), quote=False/reply_text(\1, do_quote=False/g' bot.py
sed -i 's/\breply_photo(\(.*\), quote=/reply_photo(\1, do_quote=/g' bot.py
sed -i 's/\breply_audio(\(.*\), quote=/reply_audio(\1, do_quote=/g' bot.py
# etc. for every reply_* variant you use
```

Then grep for any `quote=True` / `quote=False` left:
```bash
grep -nE 'quote=(True|False)' bot.py
```

### Message objects need an attached bot for shortcuts

In v22, `Message.reply_text()` etc. internally call `self.get_bot().send_message(...)`.
If you build a Message in a test or migration script without attaching it to a `Bot`
instance, you get:

```
RuntimeError: This object has no bot associated with it. Shortcuts cannot be used.
```

**Fix for production:** always construct via the bot's `update_queue` or pass a real
`Update` from the dispatcher. Don't try to build Update/Message manually for real sends.

**Fix for tests:** skip Message shortcuts entirely — define a stub class with the
methods you need:

```python
class FakeMessage:
    def __init__(self, text="", chat_id=0):
        self.text = text
        self.chat_id = chat_id
        self.chat = type('FakeChat', (), {'id': chat_id})()
    async def reply_text(self, text, quote=None, do_quote=None, parse_mode=None, **kw):
        print(f"[reply_text] {text}")
    async def reply_photo(self, photo=None, do_quote=None, **kw):
        print(f"[reply_photo] {getattr(photo, 'name', '?')}")
    async def reply_audio(self, audio=None, do_quote=None, **kw):
        print(f"[reply_audio] {getattr(audio, 'name', '?')}")
```

Building a real `telegram.Message` for tests requires `Message._bot` to be set, which
needs a `Bot` instance, which needs an `Application` — too much ceremony for a unit test.
The stub approach is the standard pattern in PTB's own test suite.

### Other v22 behavior changes

- `filters.Regex(r"^/")` and `filters.COMMAND` are still valid but `~filters.COMMAND`
  filter composition syntax changed in v22 — use `filters.TEXT & ~filters.COMMAND`
  (explicit `&` instead of chained `~`).
- `application.run_polling()` now defaults to `drop_pending_updates=True`; pass
  `drop_pending_updates=False` if you want to reprocess messages from before the
  service started (rare; usually you DON'T want this).
- `JobQueue` is now in a separate package `python-telegram-bot[job-queue]` — install
  with the extra or `JobQueue` import fails.

## Minimum-viable bot template (v22)

```python
#!/usr/bin/env python3
import os
import logging
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    ContextTypes, filters,
)
from telegram.constants import ParseMode

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! Send me anything.",
        do_quote=True,                # NOT quote=True — v22
        parse_mode=ParseMode.MARKDOWN,
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text, do_quote=True)

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    voice_file = await context.bot.get_file(update.message.voice.file_id)
    ogg = await voice_file.download_as_bytearray()
    # ... process bytes ...
    await update.message.reply_text("Got voice", do_quote=True)

def main():
    logging.basicConfig(level=logging.INFO)
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler(["start", "help"], start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
```

## Handler organization

For non-trivial bots, structure handlers around `MessageHandler` filters:

| Filter | Handler |
|---|---|
| `filters.TEXT & ~filters.COMMAND` | Plain text → claude / echo / etc. |
| `filters.COMMAND` | Slash commands → `CommandHandler([...], ...)` |
| `filters.PHOTO` | Photos → vision model |
| `filters.VOICE` | Voice notes → STT |
| `filters.VIDEO` | Videos → description + analysis |
| `filters.Document.ALL` | Files → save / parse |
| `filters.Regex(r"^/")` | Catch-all for malformed commands |

**Pitfall:** the order of `app.add_handler(...)` calls DOES NOT determine priority.
PTB picks the first handler whose filter matches the update, based on registration
order. If a generic `filters.TEXT` is registered before `filters.COMMAND`, the
generic one catches `/start` first. Always register specific filters first.

## Multipart messages (text + image, etc.)

`update.message` is always a single Message, but `update.message.caption` + media
fields can appear together (a photo with caption). The pattern:

```python
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Photo (largest size)
    photo = update.message.photo[-1]   # -1 = highest resolution
    photo_file = await context.bot.get_file(photo.file_id)
    bytes_ = await photo_file.download_as_bytearray()
    # Optional caption
    caption = update.message.caption or ""
    # ... do stuff ...
    await update.message.reply_text(f"Got photo, caption: {caption}", do_quote=True)
```

## Long-polling on a server with systemd

The simplest production deployment on Linux is long-polling + systemd user unit.
Don't bother with webhooks unless you need fan-out scaling — they require HTTPS
+ a public URL.

```ini
# ~/.config/systemd/user/claude-bot.service (template)
[Unit]
Description=<bot name>
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=/home/Hermes/<repo>
EnvironmentFile=/home/Hermes/<repo>/.env
Environment=PYTHONUNBUFFERED=1
ExecStart=/home/Hermes/<repo>/venv/bin/python3 -u /home/Hermes/<repo>/bot.py
Restart=always
RestartSec=10
TimeoutStartSec=60
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=default.target
```

```bash
systemctl --user daemon-reload
systemctl --user start <name>
systemctl --user status <name>
journalctl --user -u <name> -f
```

For reboot survival: `loginctl enable-linger $(whoami)` (one-time). User services
otherwise die at logout. See `service-verification` skill for the full bring-up
sequence including the "test before enable" rule.

## Token + secrets handling

Two layers:

1. **`.env` file (mode 0600) with `EnvironmentFile=` in the unit** — service reads at boot.
2. **Code reads via `os.environ["TELEGRAM_BOT_TOKEN"]`** — never hardcode, never commit.

```bash
# .env (gitignored)
TELEGRAM_BOT_TOKEN=...
# Optional: anything else the bot needs at runtime
MINIMAX_API_KEY=...
DATABASE_URL=...
```

**Testing the token validity from CLI (before wiring systemd):**

```python
import requests, os
token = os.environ["TELEGRAM_BOT_TOKEN"]
r = requests.get(f"https://api.telegram.org/bot{token}/getMe", timeout=10)
print(r.json())   # {ok: True, result: {id: ..., username: 'YourBot', ...}}
```

If `ok: False`, token is wrong. If `ok: True` but you don't see the bot in your
Telegram search, the username is wrong (token can be valid for a different bot).

## Common bugs that look like setup bugs but aren't

| Symptom | Real cause |
|---|---|
| Bot accepts messages but never replies | `quote=True` was the culprit (v22 broke it). Look for TypeError in journal. |
| Bot replies with empty message body | The handler ran but the reply body is empty (e.g., `mx_chat()` returned "" because the model was thinking-block-truncated). |
| Bot replies with raw Markdown | `parse_mode=ParseMode.MARKDOWN` rejected by Telegram (parse error → empty reply). Switch to `ParseMode.MARKDOWN_V2` or HTML. |
| Bot replies once and stops | Async handler raised but error swallowed. Add explicit `try/except` and `logger.exception(e)`. |
| `telegram.error.Conflict: terminated by other getUpdates` | Two bot instances running. Check `systemctl --user status` + `ps aux | grep bot.py`. |
| `telegram.error.NetworkError` after hours of working | Telegram long-poll dropped. `RestartSec=10` will recover automatically. |

## Conversation logging (SQLite)

The simplest useful log table:

```python
import sqlite3
from pathlib import Path

DB = Path(__file__).parent / "conversations.db"

def init_db():
    conn = sqlite3.connect(DB)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER,
            role TEXT,        -- 'user' | 'bot' | 'claude'
            content TEXT,
            media TEXT DEFAULT 'text',
            ts DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS idx_msg_chat ON messages(chat_id, id);
    """)
    conn.commit()
    conn.close()

def log(chat_id, role, content, media="text"):
    conn = sqlite3.connect(DB)
    conn.execute(
        "INSERT INTO messages (chat_id, role, content, media) VALUES (?, ?, ?, ?)",
        (chat_id, role, content[:8000], media),   # truncate to avoid SQLite pain
    )
    conn.commit()
    conn.close()
```

For a richer schema with sessions, tool calls, attachments, etc., see the
Claude-bot reference at `/home/Hermes/Claude-bot/telegram-claude-channel.py`.

## References

- `references/persistent-session-architecture.md` — full architecture for one-Telegram-chat-one-claude-session pattern: stream-json invocation, event types, mid-run steering, restart-on-config-change, steering manager, JSONL training log, DB schema + migration, anti-patterns, verification commands, performance numbers. Verified at `/home/Hermes/Claude-bot/` (v3, July 22 2026).
- `references/silent-bot-debugging-transcript.md` — worked transcript of a ~20-minute "silent bot" debugging session (Claude-bot v3.1, July 22 2026). Shows the actual failure modes (sendMessage-from-bot doesn't generate getUpdates; drop_pending_updates eats messages on every restart) and the 7-step diagnostic recipe that would have caught both in 30 seconds.

(Older placeholder references in this list — `v20-to-v22-migration.md`, `handler-testing-patterns.md`, `systemd-user-units.md` — are NOT yet created. The v20→v22 breakage section in this SKILL.md already covers migration; the systemd bring-up sequence is in the `service-verification` skill; handler testing patterns are in the `Persistent chat-as-session pattern` section below.)

## Persistent chat-as-session pattern (July 22 2026)

For a bot where **one Telegram chat = one ongoing session** (rather than fresh subprocess per message), see `references/persistent-session-architecture.md` for the full design: stream-json invocation, event types, mid-run steering, restart-on-config-change, steering manager, JSONL training log, DB schema + migration, anti-patterns, and verification commands.

Verified at `/home/Hermes/Claude-bot/telegram-claude-channel.py` (v3). Key abstractions:

- `ClaudeRunner(chat_id, steer_manager)` — owns one long-lived `claude` subprocess per chat
- `runner.start(goal, send_fn, user_chat)` — spawn subprocess, send initial goal, start streaming
- `runner.inject_prompt(text)` — queue prompt for next assistant-turn flush (the steering path)
- `runner.restart_with_config(new_config, send_fn)` — stop + apply new flags + restart (used by /model, /agent, /add-dir, /effort)
- `SteeringManager` — separate class with persistent JSON state per chat_id, fires checkpoint every N responses, calls M3 to summarize + decide if steering needed, asks user via Telegram (debounced 5 min)
- `log_event(type, chat_id, data)` — append to `data/training_log/YYYY-MM-DD.jsonl` for future training data

Minimal skeleton:

```python
class ClaudeRunner:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self._pending_inject: list = []
        self.process = None

    async def start(self, goal: str, send_fn):
        cmd = ["claude", "--print",
               "--input-format", "stream-json",
               "--output-format", "stream-json",
               "--verbose",
               "--session-id", str(uuid.uuid4()),
               "--model", "claude-sonnet-4-5-20250929",
               "--bare", "--dangerously-skip-permissions"]
        self.process = await asyncio.create_subprocess_exec(
            *cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE,
        )
        await self._send({"type":"user","message":{"role":"user","content":goal}})
        asyncio.create_task(self._read_stdout(send_fn))

    async def inject_prompt(self, prompt):
        self._pending_inject.append(prompt)

    async def _send(self, msg):
        line = json.dumps(msg) + "\n"
        self.process.stdin.write(line.encode())
        await self.process.stdin.drain()

    async def _read_stdout(self, send_fn):
        buf = ""
        while self.process and self.process.returncode is None:
            chunk = await self.process.stdout.read(4096)
            if not chunk: break
            buf += chunk.decode() + "\n"
            for line in buf.split("\n"):
                if not line.strip(): continue
                ev = json.loads(line)
                if ev["type"] == "assistant":
                    for block in ev["message"]["content"]:
                        if block.get("type") == "text":
                            await send_fn(block["text"])
                    # Flush pending user injects after each assistant turn
                    while self._pending_inject:
                        await self._send({"type":"user","message":{"role":"user","content":self._pending_inject.pop(0)}})
```

**Key insight:** `--input-format stream-json --output-format stream-json` requires `--verbose` (else: `Error: When using --print, --output-format=stream-json requires --verbose`). Session ID must be a valid UUID (`uuid.uuid4()`), not an arbitrary string. `--bare` skips hooks/plugins/MCP for cleaner behavior in bots. `--dangerously-skip-permissions` is needed for unattended operation.

**Asyncio gotcha:** `process.stdout.readline()` returns a coroutine — DO NOT double-await it. `asyncio.create_task(process.stdout.readline().__await__())` raises `TypeError`. Correct: `asyncio.create_task(process.stdout.readline())`. Bug found in Claude-bot v1, silently crashes on first stream read. (See pitfall #9.)

## Pitfalls (verified July 2026)

1. **`quote=` works on PTB v20, fails on v22.** Every `reply_*` shortcut.
   One-shot sed fix per shortcut method.
2. **Real `Message` objects need `Message._bot` set** for shortcuts to work.
   In tests, use stub classes — building a real one is too much ceremony.
3. **Handler registration order matters.** PTB picks the first matching filter,
   not the most specific. Register specific (PHOTO, VOICE, COMMAND) before
   generic (TEXT).
4. **`drop_pending_updates=True` (PTB v22 default) eats messages on every restart, not just first.**
   See pitfall #20 for the full picture and fix. Short version: set
   `app.run_polling(drop_pending_updates=False)` for any dev bot you bounce during testing.
5. **`filters.Regex(r"^/")` matches commands BEFORE they reach `CommandHandler`** if
   you register the regex handler first. Use `filters.COMMAND` for slash commands.
6. **`ParseMode.MARKDOWN` (v1) is deprecated** — Telegram returns parse errors for
   half of what you'd write. Use `ParseMode.MARKDOWN_V2` (escape `*`, `_`, `[`, etc.)
   or HTML.
7. **Long-poll uses HTTP keepalive; aggressive firewalls cut it.** If bot dies
   every few hours, add `RestartSec=10` to the unit and let systemd recover.
8. **`max_tokens` on whatever LLM you wrap matters more than you think** — if it
   emits long thinking blocks before text, set max_tokens ≥ 8000 or you'll see
   empty replies. See `minimax-tts-video` skill for the M2.7 case.
9. **`asyncio.subprocess.Process.stdout.readline()` returns a coroutine — DO NOT
   double-await it.** The pattern `asyncio.create_task(process.stdout.readline().__await__())`
   raises `TypeError: a coroutine was expected, got <coroutine_wrapper>`. Correct:
   `asyncio.create_task(process.stdout.readline())`. Bug found in Claude-bot v1, will
   silently crash on the first stream read. (July 22 2026)
10. **MiniMax TTS response field is `data.audio`, NOT `data.audio_url`.** The OpenAI-
    compatible `/v1/t2a_v2` endpoint returns `{"data": {"audio": "<url>", "status": 2, ...}}`.
    Bots written assuming the original docs (which said `audio_url`) will fail with
    `No audio_url in TTS response: {...}`. Fix: `data.get("audio") or data.get("audio_url")`
    with both as fallback. (July 22 2026)
11. **Concurrent bot instances → 409 Conflict on every poll.** If you see
    `telegram.error.Conflict: terminated by other getUpdates request; make sure that only
    one bot instance is running`, you have a duplicate bot. Check `systemctl --user status`
    + `ps aux | grep bot.py`. Also happens if you manually call `getUpdates` while the
    service is polling. The error is recoverable (Telegram recovers in seconds) but
    kills messages during the conflict window. (July 22 2026)
12. **`claude --print --output-format=stream-json` requires `--verbose`.** Without it,
    you get `Error: When using --print, --output-format=stream-json requires --verbose`.
    Add `--verbose` to the bot's claude command. (July 22 2026)
13. **Telegram command names cannot contain hyphens.** The PTB dispatcher rejects
    `CommandHandler(["add-dir"], ...)` with `ValueError: Command 'add-dir' is not a
    valid bot command`. Allowed charset is `[a-z0-9_]{1,32}`. Use `adddir` /
    `adddirs` / similar (or document the deviation). Always register multiple aliases
    for convenience: `CommandHandler(["model", "m"], handle_set_model)`. (July 22 2026)
14. **Never trust memory for LLM model names — always query the model's own listing
    endpoint first.** Example: claimed `MiniMax-M3 doesn't exist` from memory when it
    did, and the actual provider's response was an empty content body from a
    truncated-thinking block. The fix: `GET /v1/models` (Bearer auth) returns the full
    catalog — use that as source of truth. Memory decays; the API is always right.
    Verified at api.minimax.io: MiniMax-M3 exists, has no thinking block, ~2s response
    vs M2.7's ~10-15s. (July 22 2026)
15. **`CREATE TABLE IF NOT EXISTS` does NOT migrate existing tables.** If you change
    your DB schema between bot versions, the old table persists unchanged. `init_db()`
    needs explicit migration: check `PRAGMA table_info(<table>)`, if a new column
    is missing, `ALTER TABLE x RENAME TO x_old`, recreate with new schema, copy
    old data with `INSERT OR IGNORE`, drop the old. See the schema-migration snippet
    in `persistent-session-architecture.md` § "DB schema for sessions". (July 22 2026)
16. **`_pending_inject: list[str]` typed too narrowly for image content.** Photo input
    flows through `_pending_inject` and items are either str (text prompt) OR list of
    Anthropic-format content blocks (text + image). Type it as `list` (untyped) or
    `list[Union[str, list[dict]]]` and let `_send_prompt` decide format. (July 22 2026)
17. **Restart-on-config-change requires both `await stop()` AND a new `--session-id`.**
    `/model`, `/agent`, `/add-dir`, `/effort` all need the subprocess restarted with
    different CLI flags. If you reuse the old `--session-id`, claude may try to
    resume a session that doesn't match the new config and fail. Generate fresh
    `uuid.uuid4()` for each restart unless `--resume` is explicitly set. The pattern
    lives in `ClaudeRunner.restart_with_config()`. (July 22 2026)
18. **Per-session `cwd` requires passing `cwd=` to `create_subprocess_exec`.** The
    bot's process cwd and claude's process cwd are independent. For directory navigation
    commands (`/cd <path>`) to actually change where claude's bash tool reads/writes,
    the subprocess MUST be spawned with `cwd=runner.config["cwd"]`. Default = bot's
    cwd at runner init time. `restart_with_config({"cwd": target})` handles the
    restart — new session_id + new cwd both get applied atomically. (July 22 2026)
19. **Five-layer logging discipline for bot diagnosis.** When user reports
    "the bot is doing X wrong", your debug path needs ALL of these to be queryable:
    (1) systemd journal (`journalctl -u <svc> -p err`),
    (2) structured event log (JSONL per-day with `chat_id`, `ts`, `event_type`, payload),
    (3) per-session state file (JSON with goal/intent/decisions/checkpoints),
    (4) claude CLI's own session JSONL (`~/.claude/projects/<cwd-key>/<uuid>.jsonl`),
    (5) SQLite conversation DB. Skip a layer and you'll waste time chasing ghosts.
    The Claude-bot v3 pattern lives at `data/training_log/`, `data/sessions/<chat_id>.json`,
    `~/.claude/projects/`, and `conversations.db` respectively. User explicit rule
    (July 22 2026): "logs are important — if I tell you about an issue you can read
    them to diagnose." (July 22 2026)
20. **`drop_pending_updates=True` is set on EVERY restart, not just first start.**
    PTB's `app.run_polling(drop_pending_updates=True)` does what it says on every call —
    if you restart the bot while messages are queued, those messages are silently dropped
    before any handler can see them. The default `True` is wrong for any dev / iter / dev-server
    workflow where you bounce the service while testing. Set `drop_pending_updates=False`
    for dev bots. The "good for first start" note in pitfall #4 above is misleading — first
    start eats the messages you sent during the previous restart, which is the whole point of
    the messages. For long-lived prod bots where duplicate-on-restart is genuinely a problem,
    flip it back to True. (July 22 2026, Claude-bot v3.1)
21. **The "silent bot" debugging recipe — when handler doesn't fire and the journal is quiet.**
    If you `send /foo` to your bot and nothing happens, work this list top-to-bottom
    before assuming a code bug (Claude-bot v3.1 burned ~20 min on this):
    (a) **`getWebhookInfo` should return empty URL.** A stale webhook from a prior
        deploy will silently bypass polling — Telegram routes messages to the webhook URL
        and your bot never sees them. Fix: `curl -X POST "https://api.telegram.org/bot<TOKEN>/deleteWebhook?drop_pending_updates=true"`.
    (b) **You can't test handlers by `bot.sendMessage` from the same bot.** Telegram's
        `sendMessage` API call from the bot's own token delivers the message to the chat
        but does NOT generate a `message` update in `getUpdates`. Only messages from a
        REAL user (or a different bot's sendMessage) produce updates. To test, the user
        must actually send the message from their Telegram app, OR you need to spoof a
        user via a second bot. Don't waste time wondering why your Python test "succeeded"
        but the bot doesn't react.
    (c) **Don't manually `getUpdates` while the bot is polling.** Doing so triggers
        `telegram.error.Conflict: terminated by other getUpdates request` and the bot is
        killed (systemd will restart it, but messages in that window are dropped). Stop
        the service first, query manually, then start.
    (d) **`context.user_data` is per-chat, not per-user.** If you set a state flag in
        one chat's `user_data`, it doesn't affect other chats. Use chat_id-scoped state.
    (e) **`update.message` can be `None` for edited messages / channel posts.** PTB
        typing reflects this; `update.message.text` access without a guard will crash on
        edits. Filter on `filters.TEXT` if you only want fresh user text.
    (f) **Bump logging to DEBUG to see handler firing.** `logging.basicConfig(level=logging.DEBUG)`
        shows every PTB `getUpdates` call, every "Process Update" event, every "No new
        updates found." Without DEBUG you can't distinguish "Telegram returned nothing"
        from "Telegram returned something and my handler ignored it."
    (g) **Check Telegram's `pending_update_count`** via `getWebhookInfo` even in polling
        mode — it's a proxy for "messages are queued." 0 pending + bot polling + no
        replies = messages are arriving at the user-to-bot endpoint but the bot's
        offset is past them (because previous bot instance ack'd them, or `drop_pending_updates`
        ate them). The fix is `deleteWebhook + drop_pending_updates=false` + restart.
    (July 22 2026, Claude-bot v3.1 — full transcript burned 6 turns chasing a non-bug)
22. **Interactive multi-step command pattern via chat-scoped state.** When a
    command needs more than one message to gather input (e.g. `/new` with no goal,
    then reply with the goal), the natural instinct is `context.user_data["flag"] = True`,
    but that pattern has 5 silent failure modes. The correct version:
    ```python
    # Module-level (chat-scoped, not user-scoped — see note below)
    _pending_goals: dict[int, bool] = {}
    _pending_lock = asyncio.Lock()

    async def _set_pending_goal(chat_id): ...
    async def _consume_pending_goal(chat_id) -> bool: ...   # atomic pop
    async def _clear_pending_goal(chat_id) -> None: ...    # non-consuming clear

    async def handle_new(update, context):
        chat_id = update.message.chat_id
        await _clear_pending_goal(chat_id)  # supersede any prior pending state
        if not update.message.text.split(maxsplit=1)[1:]:
            await update.message.reply_text(HELP_TEXT + "\n\nReply with your goal…")
            await _set_pending_goal(chat_id)
            return
        # ... or process inline ...

    async def handle_text(update, context):
        if await _consume_pending_goal(update.message.chat_id):
            # next-text-becomes-goal path
            ...
    ```
    **The 5 silent failure modes of the naive `context.user_data` version** (all
    caught by a subagent critical review of Claude-bot v3.1, fixed in v3.2):

    (a) **`context.user_data` is per-USER, not per-chat.** If the same user has
        `/new` armed in chat A and sends a normal text in chat B, chat B consumes
        the flag and starts an unexpected new session. Use a chat-scoped dict at
        module scope (matching `_active_runs`).

    (b) **`/cancel` doesn't clear the pending flag.** Naive version: user runs
        `/new`, decides not to, runs `/cancel` → flag stays armed → next text
        message silently starts a new session. Fix: `handle_cancel` must call
        `_clear_pending_goal(chat_id)` BEFORE checking the runner.

    (c) **Any slash command during the prompt leaves the flag armed.** Same
        problem as (b) but for `/status`, `/ls`, `/help`, etc. Fix: register a
        `MessageHandler(filters.COMMAND, _pre_clear_pending) **in group=-1**`
        BEFORE all `CommandHandler`s. In group=-1 it runs first but doesn't
        block the command handler. Skip `/new` itself (which sets the flag).

    (d) **Photo and voice ignore the flag.** Naive version: user runs `/new`,
        sends a photo intending it as the goal → photo handler injects to old
        session, flag stays armed, next text starts new session. Fix: call
        `_consume_pending_goal(chat_id)` at the top of `handle_photo` and
        `handle_voice`.

    (e) **Markdown injection in the goal acknowledgement.** Naive version:
        `reply_text(f"..._{prompt}_", parse_mode=ParseMode.MARKDOWN)` — goal
        containing `_`, `*`, `[`, `]` from user input crashes the reply.
        Fix: render the goal as plain text (`do_quote=True`, no `parse_mode`)
        since user input is untrusted.

    Plus three supporting rules:

    (f) **Always `pop`, never `peek`** — `pop` is atomic, prevents re-entry bugs
        if the user sends a command while in awaiting state.

    (g) **Extract the prompt as a constant** (`HELP_TEXT = "..."`) so the
        command and `/help` stay in sync — single source of truth beats two
        hand-maintained strings.

    (h) **When `/new` wipes state, also wipe persisted state.** Database
        `ON CONFLICT ... COALESCE(sessions.goal, excluded.goal)` and steering
        manager `st["goal"] = st.get("goal") or runner.goal` both preserve the
        OLD goal across `/new`, so `/status` and steering checkpoints report
        stale context. Fix: `runner.start()` should call
        `steer_manager.reset_for_new_session(chat_id, new_goal)` to wipe
        goal/responses/checkpoint/steer_history atomically. And `upsert_session`
        should use `goal = excluded.goal` (no COALESCE) so the new goal wins.

    **Subagent critical-review pattern (recommended for any non-trivial bot
    state machine).** After implementing the interactive command flow, delegate
    to a subagent with the goal "find the P1 bugs in this state machine — be
    tough, don't be polite." The subagent caught all 5 of these issues in one
    pass when the author thought the code was done. See
    `subagent-driven-development` skill for the workflow. (Claude-bot v3.1
    → v3.2, July 22 2026 — 5 P1s caught by subagent critical review after
    shipping v3.1 thinking it was done.)

23. **`_consume` vs `_clear` matters for photo/voice during interactive prompts.**
    Photo and voice handlers can't act as a "goal" for an awaiting `/new`
    interactive state — they don't carry typed text. So they should
    `_clear_pending_goal()` (non-consuming clear), NOT `_consume_pending_goal()`
    (which would atomically pop and the user's typed goal that follows
    wouldn't fire). The reverse — using `_clear` from the text handler — would
    let a stray typed message remain armed. The correct asymmetry: text path
    consumes (atomic pop), media paths clear (don't consume). Both call sites
    use the same `_clear_pending_goal` helper, but the text handler in
    `handle_text` is the only one that uses the consuming variant. (July 22 2026,
    Claude-bot v3.3 — caught on second subagent review.)

24. **MarkdownV2 escaping is required for any user-content-bearing message.**
    `parse_mode=ParseMode.MARKDOWN` in PTB v22 maps to MarkdownV2, which has
    reserved chars `_*[]()~`>#+-=|{}.!\`. A tool_result preview containing
    `file_path_with_underscore` or `function(args)` from claude CLI will fail
    to parse → empty reply → user thinks the bot is silent. Three patterns:

    (a) **Inside a code block** (` ``` ... ``` `): use `md_code_escape(text)`
        which only escapes backticks and backslashes, and replaces ``` with
        `ʼʼʼ` so the outer block never closes prematurely.

    (b) **Inline user content** (e.g. goal text in a confirmation message):
        render as plain text (`do_quote=True`, NO `parse_mode`). User input
        is untrusted.

    (c) **Wrapped safe-send helper** for when you don't know if the content
        might have reserved chars: try Markdown first, on parse error fall
        back to escaped-Markdown, then plain text. The helper signature:
        `async def safe_send(update, text, parse_mode=ParseMode.MARKDOWN, **kw): ...`
        — built for the claude-bot but applies to any bot that echoes
        user-generated content.

    Avoid: rendering user content in MarkdownV2 without escaping (silent empty
    replies), or using PTB's `ParseMode.MARKDOWN` legacy mode (deprecated and
    also rejects half of what you write). (July 22 2026, Claude-bot v3.3 —
    caught on second subagent review.)

25. **`_stdin_lock` per-runner — concurrent inject_prompt() corrupts the JSON
    stream.** `asyncio.subprocess.Process.stdin` writes are NOT serialized by
    the event loop. If the bot receives two updates while claude is mid-turn
    (e.g. user types "stop" + sends a photo within 100ms), both call sites
    race into `process.stdin.write(...)` and the resulting byte stream is two
    JSON objects concatenated mid-line — claude CLI then either hangs or
    crashes with a stream-parse error. Fix: add `self._stdin_lock = asyncio.Lock()`
    in `__init__` and wrap every `_send_prompt` body in `async with self._stdin_lock:`.
    Verify with a test that fires 20 concurrent `_send_prompt` calls and asserts
    `max_concurrent_writers == 1` (use a FakeStdin that checks `_stdin_lock.locked()`
    on every `write`). (July 22 2026, Claude-bot v3.3.)

26. **`shlex.split` for CLI args built from env vars.** Anywhere you split an
    env-var-supplied string into argv tokens (`CLAUDE_EXTRA_ARGS`, model names
    with paths, system prompts with spaces), use `shlex.split()` not `.split()`.
    `CLAUDE_EXTRA_ARGS="--system-prompt 'my prompt.md'"` becomes
    `["--system-prompt", "my prompt.md"]` under shlex, but
    `["--system-prompt", "'my", "prompt.md'"]` under naive `.split()`. The
    latter is silently accepted by `create_subprocess_exec` and fails inside
    the CLI. Pattern: `cmd += shlex.split(CLAUDE_EXTRA_ARGS)`. (July 22 2026,
    Claude-bot v3.3.)

27. **Sniff image MIME from magic bytes, don't hardcode `image/jpeg`.** Telegram
    delivers photos as JPEG by default but screenshots, PNG stickers, animated
    GIFs, and WebP images come through with their actual format. If your
    Anthropic-API wrapper hardcodes `"media_type": "image/jpeg"` for everything,
    the model rejects mismatched base64 → silent injection failure → user
    sees "↪️ image injected into session" but the model never processes it.
    Magic-byte sniffer:
    ```python
    _IMAGE_MAGIC = (
        (b"\xff\xd8\xff", "image/jpeg"),
        (b"\x89PNG\r\n\x1a\n", "image/png"),
        (b"GIF87a", "image/gif"),
        (b"GIF89a", "image/gif"),
        (b"RIFF", "image/webp"),  # verify WEBP at offset 8
        (b"BM", "image/bmp"),
    )
    def sniff_image_mime(b: bytes) -> str:
        for magic, mime in _IMAGE_MAGIC:
            if b.startswith(magic):
                if mime == "image/webp" and b[8:12] != b"WEBP":
                    continue
                return mime
        return "image/jpeg"  # safe fallback
    ```
    Always log the detected MIME in `log_event` so debugging cross-format
    issues is one grep away. (July 22 2026, Claude-bot v3.3.)

28. **`restart_with_config` must drain `_pending_inject` AND reset
    `response_count` and `session_id`.** Three things carry over from the old
    subprocess and break the new one if not reset:

    (a) **`_pending_inject`** — steering messages queued during the restart
        window get sent as the first user message of the new session, polluting
        its history. Drain to a log entry before stopping:
        `dropped = self._pending_inject; self._pending_inject = []; log_event("runner_restart", ..., {"dropped": dropped})`.

    (b) **`response_count`** — used by `response_count % CHECKPOINT_EVERY == 0`
        to decide when to checkpoint. If the old counter was at 9, the new
        session's first response fires a checkpoint against zero context. Reset
        to 0 in `restart_with_config`.

    (c) **`session_id`** — already handled by existing pattern (`if not
        config.get("resume"): self.session_id = uuid.uuid4()`), but worth
        flagging since it's the same fix family. Don't reset if `--resume`
        is set — that's the whole point of resume. (July 22 2026, Claude-bot v3.3.)

29. **`runner.start()` should surface early claude CLI failures within 2s.**
    Bad model name, missing flag, auth error, missing binary — claude CLI
    exits in <1s with a stderr message that nobody sees. The bot happily
    shows "starting…" and then sits silent forever. Fix: after spawning,
    `await asyncio.wait_for(process.wait(), timeout=2.0)`. If it exits,
    read stderr and send it to the user via `_send_to_user_fn` with a
    `❌ claude exited immediately (code N)\n<stderr>` prefix. Log
    `runner_early_exit` event with returncode + stderr for diagnosis.
    After the 2s timeout, the process is presumed healthy and the function
    returns. (July 22 2026, Claude-bot v3.3.)

30. **`safe_send` must NOT pass `do_quote` to `bot.send_message()`.** The
    `do_quote` parameter belongs to `update.message.reply_text()` and its
    siblings — NOT to the low-level `bot.send_message()`. If your safe_send
    helper is written as `await bot.send_message(chat_id=chat_id, text=text,
    parse_mode=parse_mode, do_quote=do_quote)`, **every** call raises
    `TypeError: ExtBot.send_message() got an unexpected keyword argument
    'do_quote'`. The exception is caught by safe_send's own try/except, but
    the fallback re-runs the SAME broken call with escaped text → TypeError
    again → falls through to plain text → TypeError again → message lost.
    End user sees the bot accept their command and never reply.

    **Diagnosis:** grep journal for `TypeError: ExtBot.send_message() got an
    unexpected keyword argument 'do_quote'`. The 3-5 retry chain (Markdown →
    escaped Markdown → plain text) shows up as a single 100ms burst. The
    message itself never gets to Telegram.

    **Fix:** `safe_send` must use ONLY `bot.send_message()` (no `do_quote`),
    fetch the bot via `update.get_bot()` (canonical) instead of
    `update.effective_message.get_bot()` (fragile), and prefer
    `update.effective_chat.id` for chat_id resolution. (Claude-bot v3.8.3,
    July 23 2026 — `/sessions` silently dropped every reply for one bot
    iteration; user reported "it does nothing" until journal was checked.)

31. **Claude Code JSONL session files have a `queue-operation` line BEFORE
    the first `user` message.** A `/sessions` handler that does
    `f.readline()` and checks `if type=="user"` skips every session — the
    first line is always `{"type":"queue-operation","operation":"enqueue",...}`.
    Then the same handler using `rglob("*.jsonl")` picks up files under
    `*/subagents/*.jsonl` which all share the parent's sessionId — same
    session appears 6+ times in the list.

    **Correct parser:**
    ```python
    sid, preview = None, ""
    with open(jsonl) as f:
        for line in f:
            if not line.strip(): continue
            try: ev = json.loads(line)
            except json.JSONDecodeError: continue
            if sid is None:
                sid = ev.get("sessionId") or jsonl.stem
            if not preview and ev.get("type") == "user":
                msg = ev.get("message", {})
                content = msg.get("content", "")
                if isinstance(content, list):
                    content = "\n".join(b.get("text","") for b in content if b.get("type") == "text")
                preview = (content or "").strip()
    # Skip subagent files entirely
    if "/subagents/" in str(jsonl): continue
    ```
    Verified: before fix, `/sessions` showed 2 stale sessions from a different
    project; after fix, 46 unique sessions including all bot's own sessions.
    (Claude-bot v3.8.1, July 23 2026.)

32. **Steering manager anti-pattern: LLM summary buried under raw counts.**
    The summary class calls M3 to produce a beautiful structured output
    (`🎯 What you want: ...`, `📍 Claude is doing: ...`, etc.) — then the
    formatter prepends raw `f"📊 Last Activity: {text}\n🔢 Activities:
    {len(recent)}\n🔧 Decisions: {len(recent_decisions)}..."` on top. User
    sees the LLM summary PLUS a redundant dump. **The user wants ONLY the
    summary, nothing else.**

    **Fix:** the formatter is purely a function of the LLM output. Raw event
    counts go to `log_event()`, never into the user-facing message. The
    formatter function (`_format_checkpoint_summary`) should accept ONLY the
    parsed LLM dict, not the raw event list. If you find yourself wanting to
    embed `len(recent_tools)` or "last activity description" — log it, don't
    show it.

    **Architectural invariant:** the summary loop buffers events and emits
    ONLY the structured LLM-curated summary. `_handle_event` writes to the
    buffer; it does NOT call `send_fn` for routine events after the first
    turn. The first turn streams raw so the user knows claude is alive; from
    then on, only summaries reach the user.

    **Three triggers for the summary loop, none alone is correct:**
    - **Count:** every N events buffered (default 10). Cheap checkpoint.
    - **Idle:** N seconds since last event (default 3). Catches mid-turn pauses.
    - **Result:** when a turn-completion event arrives. Natural break point.

    Use `time.time()` (wall clock) for idle detection, NOT `time.monotonic()`
    (which can return 0 at boot and trigger an immediate false summary).

    Also: `stop()` should flush the remaining buffer as a FINAL summary so
    the user knows what claude accomplished before shutdown. (Claude-bot
    v3.7 → v3.8, July 23 2026 — lost 2 hours debugging "the steering manager
    isn't working" before realizing the formatter was dumping raw counts on
    top of the LLM output. The LLM summary was fine; the UI was the bug.)

33. **`os.getcwd()` in a systemd bot service returns the service's
    `WorkingDirectory`, not the user's home.** A bot launched via systemd
    with `WorkingDirectory=/home/Hermes/Claude-bot` has `os.getcwd() ==
    /home/Hermes/Claude-bot` for every Python call. Any handler that falls
    back to `os.getcwd()` for "no active session" cwd will show the bot's
    internals — `/ls` shows `venv/`, `data/`, `.env`, etc. instead of the
    user's projects.

    **Default the runner's cwd to `Path.home()`, not `os.getcwd()`:**
    ```python
    self.config = {"cwd": str(Path.home())}  # NOT os.getcwd()
    ```

    **AND audit every other handler that uses `os.getcwd()` as a fallback.**
    In Claude-bot v3.8.4, the runner was fixed but `/ls`, `/tree`, `/adddir`,
    `/cd <no-arg>` still fell back to `os.getcwd()`. User typed `/ls` and
    saw Claude-bot's internals. The audit + sed fix:
    ```bash
    grep -n 'if runner else None) or os.getcwd()' bot.py
    # for each hit, replace os.getcwd() with str(Path.home())
    ```

    The user can still override per-session with `/cd ~/repos/Foo` which
    calls `runner.restart_with_config({"cwd": target})`. Persisting cwd
    across restarts requires writing it to a per-chat state file.
    (Claude-bot v3.8.4, July 23 2026.)

---

## Telegram → CLI Subprocess Bridge Architecture (Claude-bot pattern)

When the goal is **full Claude Code parity over Telegram** — one chat = one
long-running Claude subprocess with steering, checkpointing, and slash commands —
the architecture is a `python-telegram-bot` PTB v22 application that owns a
persistent subprocess, streams stream-json events from stdout, writes user
messages back to stdin, and exposes slash commands to inspect / steer / fork
the session.

Reference implementation: **Claude-bot** at `/home/Hermes/Claude-bot/` (Telegram
`@Claude2203bot`, ~2,400 LoC). All pitfalls below were hit during that build.

### When to apply

- Building a chat bot that exposes a CLI agent as a conversational interface
- Debugging "bot responds to first message then nothing" or "Cannot continue a session ID" or "watchdog killed my work"
- Wiring `claude --print --input-format stream-json` to a chat transport
- Setting up a user-mode systemd service for a personal bot

### Telegram API pitfalls (bridge-specific)

**`bot.send_message()` does NOT accept `do_quote`** — `do_quote` is for
`update.message.reply_text()`, NOT `bot.send_message()`. A `safe_send` wrapper
that passes `do_quote=do_quote` to `bot.send_message` raises `TypeError` on every
call — the bot appears alive but the user sees nothing. Diagnose:
`journalctl --user -u <bot>.service | grep "got an unexpected keyword argument"`.

**Fix:** `safe_send` always uses `bot.send_message(chat_id, text, **kwargs)`. Use
`update.message.reply_text(..., do_quote=True)` for actual quoted replies.

**ParseMode.MARKDOWN vs MARKDOWN_V2 escape rules** — V1 escapes only `[`, `]`, `` ` ``, `\`. V2
escapes `_*[]()~`>#+-=|{}.!`. A handler that builds a V1-style string and sends
with V2 (the default) hits "Can't find end of entity" and black-holes the message.

**Fix:** every user-content message must be sent with V2 + `md_escape()`-escaped
content, OR plain text. Catch-all `except Exception` is mandatory — different
bugs raise different exception types, and re-raising a specific type is a
recipe for silent black holes.

**Command names — hyphens vs underscores** — PTB v22 only accepts alphanumeric +
underscore for `CommandHandler` names. Hyphens work as Bot Menu commands (set
via @BotFather) but NOT as text commands in chat. Use underscores in code.

### CLI subprocess plumbing

`claude --print --input-format stream-json` accepts multiple user messages on
stdin and emits multiple `result` events. You do NOT need `--resume` for a
multi-turn session in this mode; just keep writing to stdin.

```python
async def _send_prompt(self, content):
    if isinstance(content, str):
        content = [{"type": "text", "text": content}]
    msg = {"type": "user", "message": {"role": "user", "content": content}}
    line = json.dumps(msg) + "\n"
    self._last_prompt_sent_at = time.monotonic()
    async with self._stdin_lock:
        try:
            self.process.stdin.write(line.encode("utf-8"))
            await self.process.stdin.drain()
        except Exception as e:
            log_event("inject_error", self.chat_id, {"error": str(e)})
```

The `+ "\n"` is critical — stream-json is newline-delimited, atomic line writes
are safe. The `_stdin_lock` serializes concurrent injects from multiple chat
handlers.

### The watchdog trap (can kill its own session)

**Symptom:** Bot restarts the session mid-work. Journal shows
`stuck_session_kill: silent_seconds=95, last_prompt_sent_at=1140834.54,
last_event_ts=1140806.24` — i.e. `last_prompt_sent_at > last_event_ts` by 28s.

**Root cause:** `_last_prompt_sent_at` gets bumped by code paths that aren't
real user prompts: `_flush_pending_injects()` calls `_send_prompt()` for each
queued image-inject; internal `_send_prompt` calls bump it too. Compounding:
`last_event_ts` is often only updated on `assistant/text` blocks, leaving it
frozen during long `thinking` + `tool_use` chains.

**Fixes (apply both):**

1. Update `last_event_ts` on **every** event from claude (system, assistant,
   user, result). If claude is producing any events, the watchdog is silent.
2. Track `_pending_prompt_queued_at` separately from `_last_prompt_sent_at`.
   Only set the former from `inject_prompt()` (real user input). Watchdog only
   fires if `silent > timeout AND _pending_prompt_queued_at > 0` — idle claude
   doing long thinking without user input is NOT stuck.

**Last-resort:** if you can't find the phantom-prompt source, comment out the
watchdog task and trust `/cancel` for manual session termination. Keep the
function in place. Re-enable when the underlying bug is identified.

### Session cwd registry (the /resume trap)

**Symptom:** "I enter the session id, it says it cannot continue a session."
Error from claude: `No conversation found with session ID: <id>`.

**Root cause:** Claude Code looks up sessions by `(project, session_id)` where
`project` is derived from the current cwd. The bot spawns the resumed claude in
the bot's current cwd, but the session was originally created in a different cwd.

**Fix:** capture the `cwd` from claude's `system/init` event and register
`(claude_session_id → cwd)` in a JSON file. On `/resume`, look up the cwd and
override the runner's `config["cwd"]` before spawning.

**Backfill on startup:** scan `~/.claude/projects/` and recover cwd for sessions
not in the registry. The directory name encodes the cwd: `~/.claude/projects/-home-Hermes/`
→ `/home/Hermes`. Strip leading `-`, replace the rest of the `-`s with `/`,
prepend `/`. Claude-bot recovered 61 sessions on the first install.

### `claude --session-id` + `--resume` are mutually exclusive

**Symptom:** `/resume` exits immediately with
`Error: --session-id can only be used with --continue or --resume if --fork-session is also specified.`
(exit code 1).

**Root cause:** Claude CLI has THREE command shapes:

| Mode | Required flags |
|---|---|
| New session | `--session-id <id>` (sets the id) |
| Resume existing | `--resume <id>` (uses the id from the on-disk JSONL; do NOT pass `--session-id`) |
| Resume + fork | `--resume <id> --fork-session --session-id <new-id>` |

If you always include `--session-id` in `_build_cmd` and add `--resume` when the
user asks to resume, you produce the forbidden combination.

**Fix:** branch the build — omit `--session-id` for plain resume, add
`--fork-session --session-id` for resume+forks. Verify each shape with a unit
test (FakeRunner subclass, assert command list) before shipping.

### Steering state — track ALL user prompts, not just the first

**Symptom:** LLM keeps asking "what does the user actually want?" for the
entire session, despite many specific prompts.

**Root cause:** SteeringManager only stored the FIRST user prompt. Every
subsequent `inject_prompt()` was invisible to the summarizer.

**Fix:** add a `user_prompts[]` list to the state file. Update it on every
`inject_prompt()`. Feed the full list to the summarizer LLM with an explicit
instruction to reason about the FULL history, especially the latest prompt.
`_load_state` must merge defaults with on-disk data so a state file from an
older bot version loads cleanly with the new field initialized to `[]`.

### User-mode systemd deployment

```ini
[Unit]
Description=Claude Telegram Bridge
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=/home/Hermes/Claude-bot
EnvironmentFile=/home/Hermes/Claude-bot/.env
Environment=PYTHONUNBUFFERED=1
ExecStart=/home/Hermes/Claude-bot/venv/bin/python3 /home/Hermes/Claude-bot/telegram-claude-channel.py
Restart=always
RestartSec=10
TimeoutStartSec=60
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=default.target
```

**Two gotchas:**

1. `loginctl enable-linger <user>` is required for user services to survive
   logout. Check: `loginctl show-user <user> | grep Linger` should be `Linger=yes`.
2. Avoid `pkill -f` against the unit's binary — pkill matches against full
   command line and will also match the terminal running pkill. Use
   `systemctl --user restart <name>.service` instead.

### Watchdog-then-cron-watchdog pattern

A bot can hang; the systemd unit restarts it after 10s. But the underlying
problem (claude hang, network outage) may still be there. Layer a `cronjob`
watchdog on top:

```bash
#!/bin/bash
# ~/.hermes/scripts/<bot>-watchdog.sh
set -e
if ! pgrep -f '<bot-script.py>' > /dev/null; then
    systemctl --user start <bot>.service
    echo "<bot> restarted"
fi
curl -s -m 3 "https://api.telegram.org/bot<TOKEN>/getMe" -o /dev/null
echo "ok"
```

```python
cronjob(action='create',
         name='<bot>-watchdog',
         schedule='every 5m',
         script='<bot>-watchdog.sh',   # MUST end in .sh
         no_agent=True)
```

**Filename MUST end in `.sh`** — Hermes scheduler runs `.sh`/`.bash` as bash
and everything else as Python. A bash script with no extension silently fails
every tick with `SyntaxError`. Diagnose:
`cat /home/Hermes/.hermes/cron/output/<job_id>/<timestamp>.md | tail -20`.

### Bridge pitfalls (consolidated)

- Don't raw-stream every event to Telegram. Buffer + summarize.
- Don't trust `bot.send_message` to surface errors. Wrap in `safe_send`.
- Don't trust `os.getcwd()` as a session default. Use `Path.home()`.
- Don't update `last_event_ts` only on text events. Update on every event.
- Don't trust the watchdog. Gate it on real pending input, not timestamp comparisons.
- Don't assume `claude --resume` finds the session. Spawn in the original cwd.
- Don't pass `--session-id` alongside `--resume` unless `--fork-session` is also set.
- Don't store only the first user prompt in steering state. Store full `user_prompts[]`.
- Don't `pkill -f` from a terminal that itself matches the pattern. Use `systemctl --user restart`.
- Don't use `pkill -KILL -f` then `systemctl start` in the same shell.

### Reference implementation

`/home/Hermes/Claude-bot/` — `@Claude2203bot`, ~2,400 LoC,
github.com/nehraa/Claude-bot. Runs MiniMax-M3 via
`claude --print --input-format stream-json` with
`ANTHROPIC_BASE_URL=https://api.minimax.io/anthropic`. 21 slash commands.
Voice notes via local whisper-tiny. Photos + voice → Anthropic content blocks.
