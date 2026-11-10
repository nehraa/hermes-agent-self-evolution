---
name: whatsapp-bulk-sender
description: Bulk WhatsApp messaging via WhatsApp Web using a controlled Chromium browser on a Linux server. Includes VNC setup, session management, and message sending via Playwright CDP.
category: messaging
---

# WhatsApp Bulk Sender

## Overview

This skill manages mass WhatsApp outreach campaigns using Playwright to control WhatsApp Web through Chrome DevTools Protocol (CDP). It runs Chrome in headed mode with VNC/noVNC access for session management.

> **Important:** This bulk sender is **completely separate** from the WhatsApp Agent Gateway, which uses Baileys for autonomous reply handling. Do not confuse their session directories or configuration files.

## Architecture

┌─────────────────────────────────────────────────────────────────┐
│                      WhatsApp Bulk Sender                        │
├─────────────────────────────────────────────────────────────────┤
│  Chrome Browser (headed mode)                                    │
│  ├── Profile: /home/Hermes/chrome-profile-persistent/           │
│  └── Debug Port: 9222                                           │
│        │                                                        │
│        ▼                                                        │
│  Playwright CDP Scripts                                          │
│  └── Reads: CSV contacts → Sends messages → Logs results       │
│                                                                  │
│  VNC Access Layer                                                │
│  └── noVNC → Xvfb → Display :1                                   │
└─────────────────────────────────────────────────────────────────┘
## System Comparison

| Aspect | Bulk Sender | WhatsApp Agent Gateway |
|--------|-------------|------------------------|
| **Purpose** | Mass outreach campaigns from CSV | Autonomous reply handling |
| **Session Location** | `/home/Hermes/chrome-profile-persistent/` | `/home/Hermes/.hermes/whatsapp/session/` |
| **Browser** | Chrome with Xvfb/noVNC (headed mode) | None (Baileys library only) |
| **Debug Port** | 9222 | N/A |
| **Core Files** | Playwright automation scripts | `bridge.js`, `logs/gateway.log` |
| **Contact Source** | CSV import | Incoming messages |

## Critical Path Locations

### Bulk Sender Session
/home/Hermes/chrome-profile-persistent/
├── Chrome profile data (~1300 files)
└── Session persists across restarts until QR re-auth required
### WhatsApp Agent Gateway Session (DO NOT confuse with bulk sender)
/home/Hermes/.hermes/whatsapp/session/
└── Baileys authentication credentials

/home/Hermes/.hermes/profiles/whatsapp-agent/
├── gateway_state.json          # Connection status
└── logs/
    ├── gateway.log             # Bridge activity logs
    └── agent.log               # Agent activity logs
## Diagnostic Checklist

Run these steps **in order** when issues are reported:

### Step 1: Check Gateway State
bash
cat /home/Hermes/.hermes/profiles/whatsapp-agent/gateway_state.json
**Expected:** `{"connected": true, "phone": "..."}`  
**Bad:** Session expired, phone number missing

### Step 2: Check Last Activity
bash
tail -30 /home/Hermes/.hermes/profiles/whatsapp-agent/logs/gateway.log
Look for:
- `❌ Logged out` → Session expired
- Connection errors → Network or QR timeout
- Message queue status → Pending vs sent counts

### Step 3: Verify Chrome Process
bash
ps aux | grep "whatsapp-agent.*chrome" | grep -v grep
**Expected:** Active Chrome process with `--remote-debugging-port=9222`  
**Missing:** Browser not running, needs restart

### Step 4: Check Playwright Script Status
bash
# Check if any Playwright processes are active
ps aux | grep -E "playwright|node.*whatsapp" | grep -v grep

# Check for hung browser instances
lsof -i :9222
### Step 5: Session Recovery (If Expired)

If session expired or logged out:

1. **Restart Chrome:**
   ```bash
   # Kill existing Chrome
   pkill -f "chrome.*whatsapp"
   
   # Restart with fresh session
   /home/Hermes/scripts/start-whatsapp-chrome.sh
   ```

2. **Re-scan QR via noVNC:**
   - Connect to: `http://server:6080/vnc.html`
   - Wait for WhatsApp Web QR prompt
   - Scan with phone (same as initial setup)

3. **Verify reconnection:**
   ```bash
   # Wait 10 seconds, then check
   curl -s http://localhost:9222/json/version | jq .browser
   ```

## Common Issues and Resolutions

| Symptom | Cause | Resolution |
|---------|-------|------------|
| `❌ Logged out` in logs despite `creds.json` existing | Session mismatch or token expiry | Re-scan QR code via noVNC |
| "No results found" for contact search | Number not saved in Chrome profile contacts | Add number to WhatsApp contacts first |
| Chrome crashes on startup | Corrupted profile | Delete profile, re-authenticate |
| Messages not sending | Rate limiting or browser freeze | Wait 60s, check `ps aux` for hung process |
| noVNC shows blank screen | Xvfb display not running | `export DISPLAY=:1; xdotool verify` |

## Contact Search Limitation

WhatsApp Web phone search **only finds numbers saved in the logged-in account's contacts**. This is a fundamental WhatsApp Web limitation.

**Numbers that will NOT work:**
- Business landlines / switchboard numbers (e.g., `0124-405XXXX`, `1800-XXX-XXXX`)
- Toll-free numbers (e.g., `1800-XXX-XXXX`)
- Unregistered mobile numbers

**Solution:** Before sending bulk messages:
1. Export contacts from your CSV to a temporary list
2. Add all recipient numbers to the phone's WhatsApp contact list
3. Sync contacts to the WhatsApp Web session
4. Verify searchability by testing with one number before bulk send

## Session Management Commands

bash
# Start Chrome session
/home/Hermes/scripts/start-whatsapp-chrome.sh

# Stop Chrome session
pkill -f "chrome.*remote-debugging-port=9222"

# Check session integrity
/home/Hermes/scripts/verify-whatsapp-session.sh

# View Chrome console logs
cat /tmp/chrome-console.log
## Best Practices

1. **Always verify session** before starting bulk campaigns
2. **Use contact lists** saved in the phone, not CSV-only numbers
3. **Monitor rate limits** — WhatsApp may temporarily block accounts sending to too many new contacts
4. **Keep profile backup** — Copy `/home/Hermes/chrome-profile-persistent/` before any major changes
5. **Separate sessions** — Don't run bulk sender and agent gateway simultaneously with same number