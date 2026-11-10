---
name: whatsapp-bulk-sender
description: Bulk WhatsApp messaging via WhatsApp Web using a controlled Chromium browser on a Linux server. Includes VNC setup, session management, and message sending via Playwright CDP.
category: messaging
---

# WhatsApp Bulk Sender

Bulk WhatsApp messaging via WhatsApp Web using Playwright-controlled Chromium. Handles CSV-based mass outreach through Chrome DevTools Protocol (CDP).

> **Note:** This is completely separate from the WhatsApp Agent Gateway (Baileys-based autonomous reply system).

---

## Architecture Overview

| Component | Bulk Sender | WhatsApp Agent Gateway |
|-----------|-------------|------------------------|
| **Purpose** | Mass outreach from CSV | Autonomous reply handling |
| **Session Location** | `/home/Hermes/chrome-profile-persistent/` | `/home/Hermes/.hermes/whatsapp/session/` |
| **Browser** | Chrome/Xvfb/noVNC (headed mode) | None (Baileys only) |
| **Debug Port** | 9222 | N/A |
| **Key File** | Playwright scripts | `bridge.js`, `logs/gateway.log` |

---

## Directory Structure

Bulk Sender Session
└── /home/Hermes/chrome-profile-persistent/
    └── Chrome profile data (~1300 files)

Gateway Session (Separate - Do Not Confuse)
└── /home/Hermes/.hermes/whatsapp/session/
    └── Baileys credentials

└── /home/Hermes/.hermes/profiles/whatsapp-agent/
    ├── gateway_state.json          # Connection status
    └── logs/
        ├── gateway.log             # Bridge activity
        └── agent.log               # Agent activity
---

## Setup Instructions

### Prerequisites

1. **Chrome installed** on the Linux server
2. **Xvfb** for virtual display (headless-friendly)
3. **noVNC** for visual access to scan QR codes
4. **Playwright** with Chromium browser installed

### Initial Setup

bash
# 1. Start virtual display
export DISPLAY=:99
Xvfb :99 -screen 0 1920x1080x24 &

# 2. Start Chrome with remote debugging
google-chrome \
  --user-data-dir=/home/Hermes/chrome-profile-persistent \
  --remote-debugging-port=9222 \
  --no-first-run \
  --no-default-browser-check &

# 3. Access noVNC in browser
# Navigate to: http://<server>:6080/vnc.html
### QR Code Scanning

1. Connect via noVNC at `http://<server>:6080/vnc.html`
2. Navigate to `https://web.whatsapp.com/`
3. Scan the QR code with your WhatsApp mobile app
4. Wait for sync to complete

---

## Diagnostic Procedures

Run these steps **in order** when issues are reported.

### Step 1: Check Gateway State

bash
cat /home/Hermes/.hermes/profiles/whatsapp-agent/gateway_state.json
Expected output should show `"connected": true`. If missing or false, proceed to Step 4.

### Step 2: Check Last Activity

bash
tail -50 /home/Hermes/.hermes/profiles/whatsapp-agent/logs/gateway.log
Look for:
- `✅ Connected` - Normal operation
- `❌ Logged out` - Session expired
- `QR Code detected` - Re-authentication needed
- `Message sent successfully` - Recent activity

### Step 3: Verify Chrome Process

bash
ps aux | grep "whatsapp-agent.*chrome" | grep -v grep
If no results, Chrome is not running. Proceed to Step 4.

### Step 4: Restart Chrome Session

bash
# Kill existing Chrome processes
pkill -f "chrome.*whatsapp" || true

# Restart with fresh instance
export DISPLAY=:99
google-chrome \
  --user-data-dir=/home/Hermes/chrome-profile-persistent \
  --remote-debugging-port=9222 \
  --no-first-run &

# Wait 10 seconds, then re-scan QR via noVNC
---

## Common Issues

### "Logged out" Despite `creds.json` Existing

**Cause:** Session mismatch or expired authentication.

**Resolution:**
1. Clear browser data in the profile directory
2. Re-scan QR code via noVNC
3. Verify phone has WhatsApp Web access enabled

### Contact Search Returns No Results

**Cause:** WhatsApp Web phone search only finds numbers saved in the logged-in account's contacts.

**Important limitations:**
- Business landlines (switchboard numbers like `0124-405XXXX`, `1800-XXX-XXXX`) are **NOT** WhatsApp-registered
- Toll-free numbers and switchboards will always return "No results found"
- Numbers must be saved as contacts in the phone linked to WhatsApp Web

**Resolution:**
1. Add target numbers to phone contacts
2. Re-sync WhatsApp Web
3. Verify contact has an active WhatsApp account via mobile app first

### Message Sending Fails

**Possible causes:**
- Target number not in WhatsApp contacts
- Rate limiting (too many messages too fast)
- Session expired
- Network connectivity issues

**Checklist:**
bash
# Verify WhatsApp Web is accessible
curl -s http://localhost:9222/json | head

# Check Playwright script logs
tail -100 /path/to/playwright/script.log

# Test manual send via WhatsApp Web
# Use noVNC to manually send a test message
---

## Maintenance

### Regular Tasks

- **Daily:** Monitor `gateway.log` for errors
- **Weekly:** Clear old browser logs
- **Monthly:** Backup `chrome-profile-persistent/` directory

### Backup Command

bash
tar -czf whatsapp-profile-backup-$(date +%Y%m%d).tar.gz \
  /home/Hermes/chrome-profile-persistent/