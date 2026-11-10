---
name: whatsapp-bulk-sender
description: Bulk WhatsApp messaging via WhatsApp Web using a controlled Chromium browser on a Linux server. Includes VNC setup, session management, and message sending via Playwright CDP.
category: messaging
---

# WhatsApp Bulk Sender

## WhatsApp Agent Gateway vs Bulk Sender — Two Completely Different Systems

**They share nothing. Know which one you're working with.**

### WhatsApp Agent Gateway (Baileys, autonomous reply)
- Profile: `/home/Hermes/.hermes/profiles/whatsapp-agent/`
- Session: `/home/Hermes/.hermes/whatsapp/session/` (1300+ Baileys credential files)
- **Does NOT use Chrome/Xvfb/noVNC** — those are for the bulk sender
- Bridge: `bridge.js` (Node.js, port 3000, started by gateway)
- Key file: `logs/gateway.log` + `logs/agent.log`
- Key config: `config.yaml` → `platforms.whatsapp.session_path` MUST be `/home/Hermes/.hermes/whatsapp/session`
- Typical symptom when broken: "❌ Logged out" in bridge.log despite creds.json existing
- See: `references/whatsapp-agent-gateway.md` (full reference)

### Bulk Sender (Playwright + Chrome CDP, mass outreach)
- Session: `/home/Hermes/chrome-profile-persistent/` (Chrome profile)
- **Requires Chrome/Xvfb/noVNC** to run headed browser
- Debug port: 9222
- Purpose: mass outreach from CSV, NOT autonomous reply

### Gateway Diagnostic Checklist (run FIRST when gateway issue is reported)

2. Check gateway_state.json for WhatsApp connection status:
   cat /home/Hermes/.hermes/profiles/whatsapp-agent/gateway_state.json

3. Check last activity in gateway log:
   tail -20 /home/Hermes/.hermes/profiles/whatsapp-agent/logs/gateway.log

4. Check if Chrome for whatsapp-agent is alive:
   ps aux | grep "whatsapp-agent.*chrome" | grep -v grep

5. If session expired: restart Chrome + re-scan QR via noVNC (see Setup section)
```

## Critical Lessons Learned (May 2026)

### This session's key finding: Contact search fails for business landlines
WhatsApp Web phone search only finds numbers **saved in the logged-in account's contacts**. Business landlines (switchboard numbers like 0124-405XXXX, 1800-XXX-XXXX, 828892XXXX) are NOT WhatsApp-registered — they will ALWAYS return "No results found". This is NOT a selector issue. The CSV contains mostly business landlines, not personal mobile numbers. Expected failure rate: 30-50%.

### The fundamental rule: NEVER mark [SENT] without confirmed delivery
CRITICAL BUG (May 2026 caught by user TWICE): Scripts marked entries as [SENT] BEFORE the send was confirmed. In this session, despite the existing rule, I again violated it — marking entries as sent based on optimistic assumptions rather than confirmed delivery. The user directly caught discrepancies by checking their WhatsApp chat history.

**Lesson (re-learned the hard way):** The ONLY valid [SENT] state is:
1. Send function returns 'SENT' or 'SENT_ENTER' (CDP-level confirmation)
2. OR a test message was successfully delivered to the contact
3. OR Abhinav confirmed via screenshot that the chat exists

**NOT valid:** script says "sent" in stdout, script didn't crash, chat opened, etc. These are all assumptions.

**The only valid [SENT] state is a confirmed delivery result ('SENT' or 'SENT_ENTER' from the send function).** Any other pattern — marking optimistically before send, accumulating in memory, marking after interrupt — produces false positives that waste follow-up effort and destroy CSV reliability.

### CSV parsing: strip \r before reading
The CSV has Windows-style line endings (\r\n) that break csv.reader row counts. Always normalize before parsing:

```python
with open(csv_path, encoding='utf-8-sig') as f:
    content = f.read()
content = content.replace('\r\n', '\n').replace('\r', '')
with open('/tmp/clean.csv', 'w') as f:
    f.write(content)
rows = list(csv.reader(content.splitlines()))
```

Use `/tmp/clean.csv` as the working copy — never the original.

### Bulk row-range tagging — user says "done, just tag them"
When user says "we've tried all up to row N" or "mark rows X-Y as [SENT]": tag them WITHOUT sending. User has independent tracking. They may then ask you to explicitly send to specific rows in that range — do exactly that, not the full range.

### CSV state management — keep it in sync or lose trust
Abhinav maintains his own mental record of what's sent. The CSV on server may lag. When he says "X is already done":
- Find the row by searching both name fragments AND phone number
- Update the CSV tag immediately
- Show the corrected next batch

**Before showing "next 10", ALWAYS scan all rows 0-50 at minimum.** The CSV has entries tagged throughout — don't assume rows 0-9 are always the first untagged. Tagging is scattered:
- Row 0-4: [SENT] cafes (early batch)
- Row 5-6: [NON-WHATSAPP]
- Row 7: [SENT] Diggin Cafe
- Row 8: [NON-WHATSAPP]
- Row 9: [SENT] ADDA Cafe
- Row 10-11: untagged
- Rows 12-50+: mixed [SENT]/[NON-WHATSAPP] scattered throughout

**BEFORE messaging any contact: scan rows on BOTH sides of the target.**
The CSV is NOT sequential in tagging. Rows 0-10 may be tagged, rows 10-20 may be mixed. A contact at row 50 may have been messaged before row 12 was ever touched. Always scan the full tag state of a range before assuming anything is untagged.

**Bulk row-range tagging (user confirmed):** When user says "rows X-Y are all done", just tag them immediately without sending. User knows their own tracking. The CSV is a running tally, not the source of truth for what was actually sent.

### NOTION messages are NOT the same as CSV messages
The Notion database has 930 pages with category-specific messages (gym, cafe, bakery, etc.). These are NOT the outreach messages used for WhatsApp. The CSV `outreach_message` field is what gets sent. Always use the CSV field, not the Notion field.

Exception: when a business has no CSV message (210 businesses were missing it), Notion messages were generated and written to Notion only — these have NOT been sent yet and need to be extracted from Notion if contacting those businesses.
CRITICAL BUG (May 2026 caught by user): The old pattern — accumulate results in lists, mark all after the loop — loses everything on interrupt. If script crashes after 3/5 sends, those 3 are never marked and the count is wrong.

**The ONLY correct pattern** — follow this exactly:
```python
for i, row in enumerate(batch):
    name_raw = row['business_name'].strip()
    phone_clean = normalize(row['phone'])
    print(f"[{i+1}/5] {name_raw}")
    result = await send_message(wa_page, phone_clean)
    print(f"  -> {result}")

    # MARK IMMEDIATELY after each result — no batching, no lists
    if 'SENT' in result:
        mark_row(rows, fieldnames, name_raw, 'SENT')
    else:
        mark_row(rows, fieldnames, name_raw, 'NON-WHATSAPP')

    # Re-read CSV after each write so state is never stale
    rows, fieldnames = read_csv()
    s, n, r = stats(rows)
    print(f"  Running: [SENT]: {s}, [NON-WHATSAPP]: {n}, Remaining: {r}")
    await asyncio.sleep(random.uniform(6, 10))
```

**mark_row must flush to disk immediately** — no in-memory buffering across iterations:
```python
def mark_row(rows, fieldnames, name_raw, tag):
    for row in rows:
        if row['business_name'].strip() == name_raw.strip():
            name = row['business_name']
            if f'[{tag}]' not in name:
                row['business_name'] = f'[{tag}] ' + name
            with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)  # Flush NOW
            return
```

**IMPORTANT: When user says "skip / already done / mark all as X" — respect it literally.**
If user says "mark rows 1-75 as [SENT]" it means mark them and move on. Do NOT send to them. If user then says "send to rows 75-80", send to 75-80 — the user may be testing or correcting. Never assume [SENT] = already messaged when user is explicitly asking you to send.

**BEFORE sending to any UNTAGED contact: screenshot first to check if already messaged.**
For contacts NOT yet tagged [SENT] in CSV:
1. Navigate to contact in WhatsApp
2. Screenshot the chat (`/tmp/wa_check.png`)
3. Send screenshot to Telegram for user review
4. Wait for "proceed" before sending
5. Only mark [SENT] after confirmed delivery

For contacts already tagged [SENT] when user explicitly asks to send: skip the screenshot check and send directly.

```python
# Screenshot check pattern
page.goto(f'https://web.whatsapp.com/send?phone={phone_clean}')
page.wait_for_timeout(5000)
page.screenshot(path='/tmp/wa_check.png', full_page=False)
# Send to Telegram for Abhinav to review, OR use vision if available
```

**Vision tools cannot read /tmp/ paths reliably.** If using a vision analyzer, save to a path the tool can access, or send via Telegram first.
WhatsApp loads messages dynamically via JavaScript. `page.inner_text()` on the chat area returns nothing. `page.content()` doesn't contain message bubbles. Screenshot verification via CDP is unreliable for confirming delivery. Screenshot analysis via vision tools cannot read `/tmp/` paths. The ONLY reliable confirmation is:
1. The send function returns 'SENT' or 'SENT_ENTER' (confirmed by CDP result)
2. A test message is successfully sent to the contact (and you see the test arrive in your WhatsApp sent folder)
3. If in doubt, send a "Test - please ignore" message — if it arrives, the number is valid

**Do NOT** try to navigate to a chat and look for the original message in the page — it won't be there as text. Use screenshots only for visual debugging, not programmatic verification.

**Report after each send — name + number + result.**
Never batch results and report at end. After each message:
```
print(f"  -> {result}: {name} | {phone}")
```
User needs to know in real time what went out.
**How false [SENT] entries get created:** The script marks entries as [SENT] in the CSV *before* actually sending, or the script crashes mid-loop. In this session (May 2026), Abhinav caught 5 cafes (Greenr Cafe, Guftagu Cafe, Love Over Coffee, Cafe De Flora, Cafe StayWoke) that were marked [SENT] from early test runs using a different send method (Ctrl+Alt+N approach) that never actually delivered messages. These 5 had valid WhatsApp numbers but were never actually messaged — confirmed when verification test messages were sent and Abhinav reported no conversation existed.

**Prevention:** Only mark [SENT] after confirmed delivery result. Never mark before send.

**Fix:** Run `scripts/csv_verify_sent.py` in batches — it sends test messages and auto-resets false [SENT] to [NON-WHATSAPP]. Or manually check screenshots Abhinav emails and cross-reference names against CSV.

### ALWAYS verify [SENT] after any session interruption
If the script was interrupted, the CSV may have false entries. Verify before continuing:
1. Run `scripts/csv_verify_sent.py` to check all [SENT] entries
2. Or manually check via WhatsApp Web: navigate to contact, look for Namaste message
3. If any [SENT] has no actual message → reset it to untagged

**csv_verify_sent.py** (reliable verification approach — send a test message):
- Navigate to each [SENT] contact via api.whatsapp.com → Continue to WhatsApp Web
- Send "Test - please ignore. This is ADAM verifying delivery."
- If NO_BOX → contact is NOT on WhatsApp, reset [SENT] to [NON-WHATSAPP]
- If chat opens and sends → contact is valid WhatsApp, original [SENT] was correct
- Delete the test message after confirming

### The working send pattern (simple, no dual-verification overhead):
```
Ctrl+Alt+N → fill(search_box, phone_10digits) → wait → 
if "No results": tag [NON-WHATSAPP]
else: click(first_contact) → fill(msg_box, message) → click(send)
```
No chat-history reading. No type-back verification. Just send and mark.

### Message = CSV outreach_message + 40% Hindi discount + devstudios.me/website (BOTH parts)
**NEVER send just the CSV message alone.** Abhinav wants BOTH parts every time:
1. The outreach_message from the CSV (business-specific original message)
2. The 40% Hindi discount block (see below)
3. devstudios.me/website link

**40% Hindi discount block (ALWAYS append after the CSV message):**
```
Chhote business ke liye hum flexible hain — kyunki aap hi desh ki raushni hain. Jo aap kar rahe ho, apni dukaan, apni mehnat — yehhi country ki taqat hai.

Isliye ab SIRF 1 MAHINE KE LIYE:
→ 40% OFF on website development

Baat karna ho toh phone pe reach karein. No pressure, sirf baat.

devstudios.me/website
```

**The full message sent = CSV outreach_message + "\n\n" + discount block above.**

**Important: The Notion database has DIFFERENT messages** (category-specific, longer) — do NOT use Notion messages. Always use the CSV outreach_message field + the discount block above.

### wa.me DOES NOT WORK from server IP
`page.goto("https://wa.me/...")` times out completely. WhatsApp blocks the request from a server datacenter IP. Do not attempt as fallback.

**Page index: pages[0] is WhatsApp Business in this session (May 2026 confirmed).**
pages[1] is the Service Worker. Always verify by title — don't assume:

```python
browser = await p.chromium.connect_over_cdp("http://localhost:9222")
for idx, pg in enumerate(browser.contexts[0].pages):
    print(f"Page {idx}: {await pg.title()} | {pg.url[:60]}")
# WhatsApp Business = pages[0] in current session
wa_page = browser.contexts[0].pages[0]
await wa_page.bring_to_front()
```

Early sessions used pages[1]. This session (May 2026) confirmed pages[0]. Always check at session start — never hardcode.

Send bulk WhatsApp messages via WhatsApp Web using Playwright to control a headed Chromium browser on a Linux server. Session persists across Playwright restarts as long as the Chrome process stays alive.

## Setup

### 1. Start Chrome with Xvfb (headless, no VNC needed)

On a headless server, use `xvfb-run` to provide a virtual display:

```bash
xvfb-run --auto-servernum \
  google-chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=/home/Hermes/chrome-profile-persistent/ \
  --no-first-run \
  --disable-dev-shm-usage \
  "https://web.whatsapp.com"
```

- `xvfb-run --auto-servernum` finds an available display automatically
- Chrome MUST stay running for CDP session to persist across script calls
- Verify with: `curl -s http://localhost:9222/json/version`
- If Chrome won't start (no `$DISPLAY` error), you're missing xvfb: `apt install xvfb`

### 2. (Optional) noVNC for manual login verification

Only needed if you want to watch the session in a browser:

```bash
# Start Xvfb virtual display
export DISPLAY=:99
Xvfb :99 -screen 0 1920x1080x24 &

# Start x11vnc (shares the display)
x11vnc -display :99 -nopw -listen localhost -xkb -ncache 10 -ncache_cr -forever -rfbport 5900 -bg

# Start noVNC web interface on port 6080
cd /usr/share/novnc && ./utils/novnc_proxy --vnc localhost:5900 --listen 6080 -bg
```

Then open `http://<server-ip>:6080/vnc_lite.html` to view.

### 3. noVNC over Tailscale for remote QR scan (RELOGIN)

When WhatsApp session expires (Chrome restarts = session lost), use noVNC to relogin:

```bash
# Start Xvfb + x11vnc + websockify
export DISPLAY=:99
Xvfb :99 -screen 0 1920x1080x24 &
x11vnc -display :99 -nopw -listen localhost -xkb -ncache 10 -ncache_cr -forever -rfbport 5900 -bg
cd /usr/share/novnc && ./utils/novnc_proxy --vnc localhost:5900 --listen 6080 -bg

# Expose via Tailscale (user ran: sudo tailscale serve --bg http://localhost:6080)
# Output: https://ip-172-31-42-231.taileXXXX.ts.net/
# User scans QR at: https://<tailnet-host>/vnc.html
```

```bash
# Start Xvfb + x11vnc + websockify (as before)
export DISPLAY=:99
Xvfb :99 -screen 0 1920x1080x24 &
x11vnc -display :99 -nopw -listen localhost -xkb -ncache 10 -ncache_cr -forever -rfbport 5900 -bg
cd /usr/share/novnc && ./utils/novnc_proxy --vnc localhost:5900 --listen 6080 -bg

# Expose noVNC via Tailscale (requires sudo on this machine)
sudo tailscale serve --bg http://localhost:6080
# Output: https://ip-172-31-42-231.taileXXXX.ts.net/
```

Open the Tailscale URL on your phone browser → scan WhatsApp QR code → session persists as long as Chrome process stays alive.

**Note:** `tailscale serve` requires sudo. If denied, run `sudo tailscale serve --bg http://localhost:6080` first, then proceed without sudo for subsequent runs.

### 4. Verify CDP connection

```bash
curl -s http://localhost:9222/json/version | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['webSocketDebuggerUrl'])"
```

Use `ws://localhost:9222/devtools/browser/<id>` as the CDP endpoint.

## Key WhatsApp Web Selectors

**Use data-tab attributes over CSS class names.** WhatsApp regenerates class names on every update — they are brittle and break without warning.

**Current verified selectors (May 2025):**

| Action | Selector |
|--------|----------|
| New chat shortcut | `Control+Alt+N` (keyboard) |
| Phone/name search input | `input[aria-label="Search name or number"]` |
| Contact search results | `[data-testid="cell-frame-container"]` (first = top match) |
| Message input | `div[contenteditable="true"][data-tab="10"]` |
| Send button | `button[aria-label="Send"]` |
| "No results found" text | `span:text("No results")` (use locator count > 0 to detect) |
| Close new-chat drawer | `Escape` key (use after failed "no results" to reset state) |

**Page index varies by session startup — ALWAYS verify by title.**

The CDP context may have pages[0] or pages[1] as WhatsApp Business. Before any action, verify:
```python
wa_page = browser.contexts[0].pages[0]  # or pages[1]
await wa_page.bring_to_front()
title = await wa_page.title()
assert "WhatsApp" in title, f"Wrong page: {title}"
```

This session (May 2026): `pages[0]` was the active WhatsApp page — `pages[1]` was the inert wa.me redirect. Previous sessions had the reverse. Never hardcode an index without verifying the page title first.
# CORRECT pattern:
wa_page = browser.contexts[0].pages[1]
await wa_page.bring_to_front()
title = await wa_page.title()  # Must be "(1) WhatsApp Business"
```

Hardcoding `pages[0]` will send to the wa.me redirect handler instead of WhatsApp Web. Always verify with `await wa_page.bring_to_front()` and check title is "(1) WhatsApp Business" before sending.

**Important corrections from live session (May 2025):**
- `locator.fill()` is FASTER and MORE RELIABLE than `page.keyboard.type()` for message input
- Phone search: use last 10 digits ONLY (no +91 prefix) — WhatsApp search strips it anyway
- `span:text("No results")` locator (count > 0) is the correct "no contact" detection
- After "No results", ALWAYS press `Escape` to close drawer before next attempt — drawer state leaks between iterations
- The `[data-testid="cell-frame-container"]` selector works reliably for clicking contacts
- Timeout errors during `fill()` usually mean WhatsApp lost focus or drawer state is wrong — `bring_to_front()` helps

**wa.me direct URL fallback:** When phone search returns "No results found", navigate directly to:
```
https://wa.me/<phone_clean>?text=<quote(message)>
```
WhatsApp will show a "Send message" button for any valid WhatsApp number, even if not saved in contacts.

## Verified Send Protocol (MANDATORY)

**NEVER send a message without first confirming the chat header shows the correct recipient.** This prevents messages going to the wrong person — the script must always verify before typing.

### Required Verification Steps (per message):
1. Open new chat → type phone number → click contact → wait for chat to load
2. **READ the chat header** — extract phone/name shown there with `span[dir="auto"][aria-hidden="false"]` (last)
3. **Compare**: header text must contain the target phone digits (normalized, both directions)
4. If mismatch → close chat (`Escape` key), skip the message, log failure
5. Only if verified → type message, send
6. **Post-send check**: read last message bubble, confirm it matches what was sent

### Report after each send — name + number + result
Never batch results and report at end. After each message:
```python
print(f"Row {row_idx}: {name} | {phone} -> SENT")
```
User needs to know in real time what went out.

### Why This Matters
- Empty phone field in CSV → message goes to whatever chat was last open (wrong person)
- Script showed "✓ Sent" for empty-phone rows even though no valid recipient existed
- Before this protocol: silent wrong-recipient sends. After: explicit verification with failure logging.

### Chat Header Extraction:
```python
async def get_chat_header_phone(page):
    """Read chat header to get the contact's phone or name shown by WhatsApp."""
    try:
        chat_title = page.locator('span[dir="auto"][aria-hidden="false"]').last
        return await chat_title.inner_text()
    except Exception:
        return ""
```

### Recipient Verification:
```python
def normalize_for_compare(p):
    """Strip all non-digit for phone comparison."""
    return re.sub(r'\D', '', p)

header_text = await get_chat_header_phone(page)
header_digits = normalize_for_compare(header_text)
phone_digits = normalize_for_compare(phone_clean)

# Must match in at least one direction (WhatsApp shows name or number)
if phone_digits and phone_digits not in header_digits and header_digits not in phone_digits:
    # Wrong chat — skip without sending
    await page.keyboard.press('Escape')
    return False, f"Wrong chat: {header_text}"
```

```python
import asyncio
from playwright.async_api import async_playwright

async def send_whatsapp_message(browser, page, phone, message):
    """
    phone: phone number as string, can be with or without +91
          e.g. "7404671623" or "+917404671623" or "917404671623"
    message: text message to send
    """
    try:
        # Open new chat
        await page.keyboard.press('Control+Alt+N')
        await asyncio.sleep(1.5)
        
        # Click Phone number button
        phone_btn = page.locator('[aria-label="Phone number"]')
        await phone_btn.click()
        await asyncio.sleep(1)
        
        # Type number in contenteditable div
        phone_div = page.locator(
            'div.x1hx0egp.x6ikm8r.x1odjw0f.x1k6rcq7.x1lkfr7t.x1whj5v'
        ).first
        await phone_div.click()
        await asyncio.sleep(0.3)
        await page.keyboard.type(phone)
        await asyncio.sleep(2)
        
        # Click first contact result if exists
        try:
            contact = page.locator('span[title]').first
            await contact.click()
            await asyncio.sleep(1)
        except:
            pass
        
        # Type message
        msg_div = page.locator('div[contenteditable="true"][data-tab="10"]').first
        await msg_div.click()
        await asyncio.sleep(0.3)
        await page.keyboard.type(message)
        await asyncio.sleep(0.5)
        
        # Send
        send_btn = page.locator('button[aria-label="Send"]').first
        await send_btn.click()
        await asyncio.sleep(0.5)
        
        return True, "Sent"
    except Exception as e:
        return False, str(e)
```

## Connect to Existing Chrome Session

```python
async with async_playwright() as p:
    browser = await p.chromium.connect_over_cdp("http://localhost:9222")
    # VERIFY page index each session — don't assume pages[0] or pages[1]
    for idx, pg in enumerate(browser.contexts[0].pages):
        title = await pg.title()
        url = pg.url[:60]
        print(f"Page {idx}: {title} | {url}")
        if 'WhatsApp Business' in title:
            wa_page = pg
    await wa_page.bring_to_front()
    # ... use send_whatsapp_message(browser, wa_page, phone, message)
```

## Bulk Send Script

```python
import asyncio
from playwright.async_api import async_playwright
import csv
import random

async def main():
    csv_path = "/home/Hermes/WebDev/output/haryana_with_outreach_v2.csv"
    
    rows = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        page = browser.contexts[0].pages[0]
        
        sent = failed = 0
        for i, row in enumerate(rows):
            phone = row.get('phone', '').strip()
            name = row.get('business_name', '').strip()
            message = row.get('outreach_message', '').strip()
            
            if not phone or not message:
                continue
            
            # Clean phone number
            phone_clean = phone.replace('+91', '').replace(' ', '').replace('-', '')
            while len(phone_clean) > 10 and phone_clean.startswith('0'):
                phone_clean = phone_clean[1:]
            if len(phone_clean) == 10:
                phone_clean = '91' + phone_clean
            
            print(f"[{i+1}/{len(rows)}] {phone_clean} | {name[:30]}")
            
            success, result = await send_whatsapp_message(browser, page, phone_clean, message)
            
            if success:
                sent += 1
            else:
                failed += 1
                print(f"  ✗ {result}")
            
            # Delay between messages (25-45s to avoid rate limits)
            if i < len(rows) - 1:
                await asyncio.sleep(random.randint(25, 45))
        
        print(f"\nDone: Sent={sent}, Failed={failed}")
        await browser.close()

asyncio.run(main())
```

## Phone Number Cleaning

```python
def clean_phone(phone):
    """Normalize phone number to Indian format (91XXXXXXXXXX)."""
    phone = phone.replace('+91', '').replace(' ', '').replace('-', '')
    # Strip leading zeros
    while len(phone) > 10 and phone.startswith('0'):
        phone = phone[1:]
    # Pad with 91 if needed
    if len(phone) == 10:
        phone = '91' + phone
    return phone
```

## CSV Handling

**Multiline fields break naive line-counting.** If a CSV row's field contains `\n` characters, writing with `csv.writer` without `lineterminator='\n'` produces a file with 12078 lines for 929 data rows — it's not corruption, just field-wrapped line breaks.

**Always read and write with `csv.DictReader`/`csv.DictWriter`.** Never count lines — count rows from the reader.

**Empty phone guard is mandatory.** Before any send attempt:
```python
if not phone.strip():
    print(f"[row {idx}] Skipping — empty phone: {name}")
    skipped += 1
    continue
```

## Important Notes

- **Session persists**: As long as Chrome process with `--user-data-dir=/home/Hermes/chrome-profile-persistent/` stays alive, WhatsApp stays logged in. Playwright reconnects via CDP each time.
- **Rate limiting**: WhatsApp may block after too many messages too fast. Use 60s fixed delay between messages. If blocked, stop and wait several hours. Never send more than 50-100 per session.
- **CDP vs new browser**: Always connect via `p.chromium.connect_over_cdp()` to reuse the existing authenticated session. Never launch a fresh browser — it would lose the WhatsApp login.
- **Phone login alternative**: If OTP works, use phone login at `web.whatsapp.com` → "Log in with phone number". If OTP times out, VNC + manual QR is more reliable.
- **xvfb-run**: If starting fresh with a headed browser, use `xvfb-run -a python3 script.py` instead of manually starting Xvfb.
- **Contact-not-found failures**: WhatsApp Web's phone search only finds numbers saved in the logged-in account's contacts. Business landlines and unstored numbers return "No results found" even when the number is valid. This is NOT a selector issue — the number genuinely isn't resolvable via search. Workaround: open `https://wa.me/<phone>` directly (see wa.me fallback below).

## wa.me Fallback (for numbers not in contacts)

When phone search returns "No results found", try the direct WhatsApp URL:

```python
# Open wa.me link — this works for any valid phone, even without contact saved
wa_url = f"https://wa.me/{phone_clean}?text={quote(message)}"
await page.goto(wa_url, timeout=30000)
await asyncio.sleep(4)

# Look for "Send message" button (WhatsApp may show it if number is valid)
send_btn = page.locator('a[href*="api.whatsapp.com"]')
if await send_btn.count() > 0:
    await send_btn.click()
    await asyncio.sleep(3)
    await page.locator('button[aria-label="Send"]').click()
```

The wa.me approach opens WhatsApp's web-start flow and can send to any number registered on WhatsApp, even if not in your contacts.
