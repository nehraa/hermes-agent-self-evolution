---
name: whatsapp-bulk-sender
description: Bulk WhatsApp messaging via WhatsApp Web using a controlled Chromium browser on a Linux server. Includes VNC setup, session management, and message sending via Playwright CDP.
category: messaging
---

# WhatsApp Bulk Sender

## Overview

This skill manages mass WhatsApp outreach campaigns using Playwright to control WhatsApp Web through Chrome DevTools Protocol (CDP). It operates with a persistent Chrome browser profile, enabling session persistence and automated message delivery from CSV contact lists.

> **Important:** This Bulk Sender is **completely separate** from the WhatsApp Agent Gateway, which uses Baileys for autonomous reply handling.

## System Architecture

┌─────────────────────────────────────────────────────────────────┐
│                     WhatsApp Bulk Sender                        │
├─────────────────────────────────────────────────────────────────┤
│  Chrome Browser ( headed mode )                                 │
│  └── Persistent Profile: /home/Hermes/chrome-profile-persistent │
│  └── Debug Port: 9222                                           │
│  └── VNC Access: noVNC (headless display)                       │
│                                                                  │
│  Playwright Scripts → CDP Commands → WhatsApp Web UI            │
│                                                                  │
│  Session Data: /home/Hermes/.hermes/whatsapp/session/           │
└─────────────────────────────────────────────────────────────────┘
## Path Reference

### Bulk Sender Paths

| Purpose | Path |
|---------|------|
| Chrome Profile (persistent) | `/home/Hermes/chrome-profile-persistent/` |
| Session Credentials | `/home/Hermes/.hermes/whatsapp/session/` |
| Playwright Scripts | `/home/Hermes/.hermes/scripts/` |
| VNC noVNC URL | `http://localhost:6080/` |

### WhatsApp Agent Gateway Paths (DO NOT confuse)

| Purpose | Path |
|---------|------|
| Baileys Session | `/home/Hermes/.hermes/whatsapp/session/` |
| Agent Profile | `/home/Hermes/.hermes/profiles/whatsapp-agent/` |
| Gateway State | `gateway_state.json` |
| Bridge Logs | `logs/gateway.log` |
| Agent Logs | `logs/agent.log` |

> ⚠️ **Warning:** The Gateway uses Baileys (no browser). The Bulk Sender uses Chrome. These are independent systems with separate session stores.

## Diagnostic Procedures

Run these steps **in order** when troubleshooting issues:

### Step 1: Verify Gateway State

bash
cat /home/Hermes/.hermes/profiles/whatsapp-agent/gateway_state.json
Expected output contains `"connected": true` when Gateway is active.

### Step 2: Check Bridge Logs

bash
tail -50 /home/Hermes/.hermes/profiles/whatsapp-agent/logs/gateway.log
Look for:
- `✅` messages indicate successful operations
- `❌` messages indicate failures
- `Logged out` indicates session expiration

### Step 3: Verify Chrome Process

bash
ps aux | grep "whatsapp-agent.*chrome" | grep -v grep
If no results, Chrome is not running → proceed to Step 4.

### Step 4: Restart Chrome Session (if expired)

bash
# Stop existing Chrome processes
pkill -f "chrome.*whatsapp"

# Start Chrome with debug port
google-chrome \
  --user-data-dir=/home/Hermes/chrome-profile-persistent \
  --remote-debugging-port=9222 \
  --no-first-run \
  --disable-infobars
Then re-authenticate via noVNC at `http://localhost:6080/`

## Common Issues

### Issue: "❌ Logged out" Despite Valid Credentials

**Symptoms:**
- `creds.json` exists in session directory
- `bridge.log` shows "Logged out" errors
- Cannot send messages

**Root Causes:**
1. Session mismatch (old profile vs new session)
2. QR code re-authentication required
3. WhatsApp account linked to different phone

**Resolution:**
1. Clear Chrome profile and re-scan QR code
2. Verify phone number matches the logged-in account
3. Check if WhatsApp Web session was terminated remotely

### Issue: Contact Search Returns "No Results Found"

**Cause:** WhatsApp Web search **only finds contacts saved in the logged-in account's address book**.

**Not WhatsApp-registered:**
- Business landlines (switchboard numbers: `0124-405XXXX`)
- Toll-free numbers (`1800-XXX-XXXX`)
- Generic business numbers (`828892XXXX`)

**Solution:**
- Verify recipient numbers are actual WhatsApp accounts
- Add recipients as contacts before sending
- Use phone numbers directly (without country code formatting issues)

## Sending Bulk Messages

### Prerequisites

1. Chrome browser running with debug port 9222
2. Active WhatsApp Web session (authenticated)
3. CSV file with phone numbers and message templates

### Basic Send Command

bash
cd /home/Hermes/.hermes/scripts

node send-bulk.js \
  --contacts /path/to/contacts.csv \
  --message "path/to/template.txt" \
  --delay 5000
### CSV Format

csv
phone,name,custom_var1
919876543210,Raj,order_123
919876543211,Priya,order_456
## Maintenance

### Weekly Tasks

1. Verify Chrome profile integrity
2. Clear old browser logs
3. Check disk space (profile can grow large)
4. Test send functionality with small batch

### Session Backup

bash
# Backup active session
cp -r /home/Hermes/.hermes/whatsapp/session /path/to/backup/session_$(date +%Y%m%d)