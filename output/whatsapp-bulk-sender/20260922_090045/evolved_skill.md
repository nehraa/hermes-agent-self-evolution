---
name: whatsapp-bulk-sender
description: Bulk WhatsApp messaging via WhatsApp Web using a controlled Chromium browser on a Linux server. Includes VNC setup, session management, and message sending via Playwright CDP.
category: messaging
---

# WhatsApp Bulk Sender

Bulk messaging via WhatsApp Web using a headless Chromium browser controlled through Playwright and Chrome DevTools Protocol (CDP).

> **Important:** This skill operates completely independently from the WhatsApp Agent Gateway (Baileys-based autonomous reply system). Do not confuse the session files or processes between the two.

## System Comparison

| Aspect | Bulk Sender | WhatsApp Agent Gateway |
|--------|-------------|------------------------|
| **Purpose** | Mass outreach from CSV | Autonomous reply handling |
| **Session Location** | `/home/Hermes/chrome-profile-persistent/` | `/home/Hermes/.hermes/whatsapp/session/` |
| **Browser** | Chrome/Xvfb/noVNC (headed) | None (Baileys only) |
| **Debug Port** | 9222 | N/A |
| **Entry Point** | Playwright scripts | `bridge.js`, `gateway.log` |

## Directory Structure

### Bulk Sender Session

/home/Hermes/chrome-profile-persistent/
Chrome profile directory containing 1300+ files. This profile stores the authenticated WhatsApp Web session cookies and local storage.

### Gateway Session (Do Not Confuse)

/home/Hermes/.hermes/whatsapp/session/     # Baileys credentials
/home/Hermes/.hermes/profiles/whatsapp-agent/
├── gateway_state.json                      # Connection status
└── logs/
    ├── gateway.log                         # Bridge activity
    └── agent.log                           # Agent activity
## Setup

### Starting the Browser Environment

bash
# Start Xvfb (virtual framebuffer) if not running
Xvfb :99 -screen 0 1920x1080x24 &

# Launch Chrome with remote debugging enabled
google-chrome \
  --user-data-dir=/home/Hermes/chrome-profile-persistent \
  --remote-debugging-port=9222 \
  --no-first-run \
  --no-default-browser-check \
  --display=:99
### Accessing via noVNC

Connect to the noVNC interface to scan the QR code and authenticate the session when first setting up or after session expiration.

### Key Playwright Commands

javascript
// Connect to existing Chrome session via CDP
const browser = await playwright.chromium.connectOverCDP('http://localhost:9222');

// Send a message (example pattern)
const page = await browser.newPage();
await page.goto('https://web.whatsapp.com');
// ... navigate and send message logic
## Diagnostic Checklist

Run these steps **in order** when issues are reported:

### 1. Check Gateway State

bash
cat /home/Hermes/.hermes/profiles/whatsapp-agent/gateway_state.json
### 2. Check Last Bridge Activity

bash
tail -20 /home/Hermes/.hermes/profiles/whatsapp-agent/logs/gateway.log
### 3. Verify Chrome Process

bash
ps aux | grep "whatsapp-agent.*chrome" | grep -v grep
### 4. Check Session Expiration

If the session has expired:
1. Stop the current Chrome process
2. Clear the old profile directory
3. Restart Chrome with fresh debugging port
4. Re-scan QR code via noVNC

## Common Issues

### "Logged Out" Despite Valid Credentials

**Symptom:** `bridge.log` shows "❌ Logged out" even though `creds.json` exists in the session directory.

**Likely Causes:**
- Session mismatch between browser profile and Baileys session files
- QR code re-authentication required (session expired)
- Corrupted Chrome profile data

**Resolution:**
1. Verify Chrome is using the correct `--user-data-dir`
2. Re-authenticate via noVNC QR scan
3. If persistent, delete profile directory and start fresh

### Contact Search Returns No Results

**Symptom:** WhatsApp Web phone search returns "No results found" for valid phone numbers.

**Root Cause:** WhatsApp Web phone search **only finds numbers saved in the logged-in account's contacts**. This is a WhatsApp Web limitation, not a bug.

**Affected Numbers:**
- Business landlines (switchboard numbers like 0124-405XXXX)
- Toll-free numbers (1800-XXX-XXXX)
- Generic business numbers (828892XXXX)

**Workaround:** Numbers must be saved as contacts in the WhatsApp account before they can be searched and messaged via the web interface.

## Operational Notes

- The Chrome profile persists between sessions, but WhatsApp Web sessions may expire after several weeks
- Monitor `gateway.log` for authentication status during automated campaigns
- When sending bulk messages, respect WhatsApp rate limits to avoid temporary blocks