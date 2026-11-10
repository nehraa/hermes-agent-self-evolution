---
name: whatsapp-bulk-sender
description: Bulk WhatsApp messaging via WhatsApp Web using a controlled Chromium browser on a Linux server. Includes VNC setup, session management, and message sending via Playwright CDP.
category: messaging
---

# WhatsApp Bulk Sender

## Overview

This skill manages mass WhatsApp outreach campaigns using Playwright to control WhatsApp Web through Chrome DevTools Protocol (CDP). It operates on a dedicated Chromium browser with persistent session state.

**Important:** This skill is completely separate from the WhatsApp Agent Gateway (Baileys-based autonomous reply system).

## Architecture

| Component | Location | Purpose |
|-----------|----------|---------|
| Chrome Profile | `/home/Hermes/chrome-profile-persistent/` | Persistent login session (1300+ files) |
| Debug Port | 9222 | CDP connection for Playwright |
| Browser Mode | Headed (Xvfb + noVNC) | Visual browser control |
| Message Source | CSV file | Target contacts and message templates |

## Session Comparison

| Aspect | Bulk Sender | WhatsApp Agent Gateway |
|--------|-------------|------------------------|
| **Purpose** | Mass outreach campaigns | Autonomous reply handling |
| **Session Location** | `/home/Hermes/chrome-profile-persistent/` | `/home/Hermes/.hermes/whatsapp/session/` |
| **Browser** | Chrome via Xvfb/noVNC | None (Baileys protocol only) |
| **Debug Port** | 9222 | N/A |
| **Key File** | Playwright scripts | `bridge.js`, `logs/gateway.log` |

## Critical Path Locations

Bulk Sender Session
└── /home/Hermes/chrome-profile-persistent/
    ├── Default/
    │   ├── Local Storage/
    │   ├── Cookies
    │   └── WebData
    └── ...

Gateway Session (DO NOT confuse with bulk sender)
└── /home/Hermes/.hermes/whatsapp/session/
    └── creds.json          # Baileys authentication

Gateway Agent State
└── /home/Hermes/.hermes/profiles/whatsapp-agent/
    ├── gateway_state.json   # Connection status
    └── logs/
        ├── gateway.log      # Bridge activity
        └── agent.log        # Agent activity
## Diagnostic Checklist

Run these steps **in order** when troubleshooting issues:

### Step 1: Check Gateway State
bash
cat /home/Hermes/.hermes/profiles/whatsapp-agent/gateway_state.json
### Step 2: Check Last Activity
bash
tail -50 /home/Hermes/.hermes/profiles/whatsapp-agent/logs/gateway.log
### Step 3: Verify Chrome Process
bash
ps aux | grep -E "chrome|chromium" | grep -v grep
### Step 4: Check Debug Port Availability
bash
lsof -i :9222
### Step 5: If Session Expired
1. Stop any running Chrome instances
2. Clear corrupted cache files in `/home/Hermes/chrome-profile-persistent/`
3. Restart Chrome with debug port
4. Re-scan QR code via noVNC interface

## Common Issues

### "❌ Logged out" Despite Existing Session

**Symptom:** `bridge.log` reports logout while `creds.json` exists.

**Root Causes:**
1. Session mismatch - profile state corrupted or overwritten
2. QR code re-authentication required after server restart
3. WhatsApp account temporarily banned for mass messaging

**Resolution:**
bash
# Stop Chrome
pkill -f "chrome.*whatsapp"

# Backup corrupted profile
mv /home/Hermes/chrome-profile-persistent /home/Hermes/chrome-profile-$(date +%s)

# Restart with fresh profile directory
### Contact Search Returns "No Results Found"

**Cause:** WhatsApp Web phone search **only finds numbers saved in the logged-in account's contacts**.

**Numbers that will NEVER work:**
- Business landlines/switchboards (e.g., 0124-405XXXX)
- Toll-free numbers (e.g., 1800-XXX-XXXX)
- Unregistered mobile numbers

**Solution:** Pre-validate recipient numbers via WhatsApp API before sending.

## Message Sending via Playwright CDP

### Basic Send Flow
javascript
const { chromium } = require('playwright');

async function sendMessage(phoneNumber, message) {
  const browser = await chromium.connectOverCDP('ws://localhost:9222');
  const context = browser.contexts()[0];
  const page = context.pages()[0];
  
  // Navigate to WhatsApp Web with phone parameter
  await page.goto(`https://web.whatsapp.com/send?phone=${phoneNumber}`);
  await page.waitForSelector('[data-testid="conversation-compose-box"]', { timeout: 30000 });
  
  // Type and send message
  await page.fill('[data-testid="conversation-compose-box"]', message);
  await page.click('[data-testid="send"]');
  
  await browser.close();
}
### CSV Integration
javascript
const fs = require('fs');
const csv = require('csv-parse');

async function processCSV(filePath) {
  const records = [];
  fs.createReadStream(filePath)
    .pipe(csv.parse({ columns: true }))
    .on('data', (row) => records.push(row));
  
  for (const record of records) {
    await sendMessage(record.phone, record.message);
    await page.waitForTimeout(5000); // Rate limiting
  }
}
## VNC Setup

### Accessing noVNC
bash
# Via browser
http://your-server:6080/vnc.html

# With authentication
http://your-server:6080/vnc.html?password=your-vnc-password
### Local VNC Connection
bash
vncviewer localhost:5900
## Rate Limiting Recommendations

| Action | Minimum Delay | Reason |
|--------|---------------|--------|
| Message send | 5-10 seconds | Prevent spam detection |
| New chat open | 10-15 seconds | Allow message load |
| Batch size | 50-100 messages | Session stability |
| Daily limit | 500-1000 messages | Account safety |

## Security Notes

- Chrome profile contains sensitive authentication tokens
- Never share `/home/Hermes/chrome-profile-persistent/` directory
- Rotate session if unusual activity detected
- Monitor `gateway.log` for unauthorized access attempts