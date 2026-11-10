---
name: whatsapp-bulk-sender
description: Bulk WhatsApp messaging via WhatsApp Web using a controlled Chromium browser on a Linux server. Includes VNC setup, session management, and message sending via Playwright CDP.
category: messaging
---

# WhatsApp Bulk Sender

## Overview

This skill manages mass WhatsApp outreach using Playwright to control WhatsApp Web through Chrome DevTools Protocol (CDP). It is **completely separate** from the WhatsApp Agent Gateway (Baileys-based autonomous reply system).

## System Comparison

| Aspect | Bulk Sender | WhatsApp Agent Gateway |
|--------|-------------|------------------------|
| **Purpose** | Mass outreach from CSV | Autonomous reply handling |
| **Session Location** | `/home/Hermes/chrome-profile-persistent/` | `/home/Hermes/.hermes/whatsapp/session/` |
| **Browser** | Chrome/Xvfb/noVNC (headed) | None (Baileys only) |
| **Debug Port** | 9222 | N/A |
| **Key File** | Playwright scripts | `bridge.js`, `logs/gateway.log` |

## Critical Path Locations

Bulk Sender Session
└── /home/Hermes/chrome-profile-persistent/    # Chrome profile (1300+ files)

Gateway Session (DO NOT confuse with bulk sender)
└── /home/Hermes/.hermes/whatsapp/session/     # Baileys credentials
└── /home/Hermes/.hermes/profiles/whatsapp-agent/
    ├── gateway_state.json                      # Connection status
    └── logs/
        ├── gateway.log                         # Bridge activity
        └── agent.log                           # Agent activity
## Diagnostic Checklist

Run these steps **in order** when issues are reported:

1. **Check gateway state:**
   ```bash
   cat /home/Hermes/.hermes/profiles/whatsapp-agent/gateway_state.json
   ```

2. **Check last activity:**
   ```bash
   tail -20 /home/Hermes/.hermes/profiles/whatsapp-agent/logs/gateway.log
   ```

3. **Verify Chrome process:**
   ```bash
   ps aux | grep "whatsapp-agent.*chrome" | grep -v grep
   ```

4. **If session expired:** Restart Chrome and re-scan QR via noVNC (see Setup section)

### Common Symptom

- **"❌ Logged out"** in `bridge.log` despite `creds.json` existing → usually indicates session mismatch or QR code re-authentication required.

---

## Critical Lessons Learned

### Contact Search Limitation

WhatsApp Web phone search **only finds numbers saved in the logged-in account's contacts**. Business landlines (switchboard numbers like 0124-405XXXX, 1800-XXX-XXXX, 828892XXXX) are **NOT WhatsApp-registered** and will always return "No results found".

- This is **NOT** a selector issue
- The CSV typically contains mostly business landlines, not personal mobile numbers
- **Expected failure rate: 30–50%**

### Message Status Rule

> **NEVER mark [SENT] without confirmed delivery.**

**Known bug (May 2026):** Scripts previously marked entries as `[SENT]` *before* the send was confirmed. This caused false positives in reporting. Ensure your script marks status only after the API/browser confirms the message was sent.

---

## Setup Reference

For full setup instructions including:
- VNC configuration
- Browser profile initialization
- Playwright script deployment
- QR code scanning via noVNC

See: `references/whatsapp-agent-gateway.md`