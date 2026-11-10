---
name: monitor-intelligence-services
description: Systematic approach to ensure World Monitor and Crucix intelligence platforms remain operational with automatic restart capabilities.
category: devops
---

# Monitor Intelligence Services

Systematic approach to ensure World Monitor and Crucix intelligence platforms remain operational with automatic restart capabilities.

## Overview

This skill provides automated health monitoring and self-healing capabilities for two critical intelligence gathering services:

| Service | Path | Port | Health Endpoint |
|---------|------|------|-----------------|
| World Monitor | `~/.hermes/hermes-agent/worldmonitor/` | 3000 | `http://localhost:3000/` |
| Crucix | `~/.hermes/hermes-agent/Crucix/` | 3117 | `http://localhost:3117/api/health` |

## Prerequisites

- Node.js and npm installed on the system
- Shell access with permissions to manage services
- Hermes cronjob scheduler configured
- Log directory created at `~/.hermes/logs/`

## Health Check Commands

### World Monitor

bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/
# Expected response: 200
# Failure indicators: Connection refused, timeout, or non-200 status
### Crucix

bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:3117/api/health
# Expected response: 200
# Failure indicators: Connection refused, timeout, or non-200 status
## Manual Restart Procedures

### Restart World Monitor

bash
cd ~/.hermes/hermes-agent/worldmonitor && \
nohup npm run dev > worldmonitor.log 2>&1 &
sleep 5 && \
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/
### Restart Crucix

bash
cd ~/.hermes/hermes-agent/Crucix && \
nohup npm run dev > crucix.log 2>&1 &
sleep 5 && \
curl -s -o /dev/null -w "%{http_code}" http://localhost:3117/api/health
## Log Locations

| Service | Log File |
|---------|----------|
| Monitoring Script | `~/.hermes/logs/intelligence_monitor.log` |
| World Monitor | `~/.hermes/hermes-agent/worldmonitor/worldmonitor.log` |
| Crucix | `~/.hermes/hermes-agent/Crucix/crucix.log` |

## Automated Monitoring Setup

### Step 1: Create the Monitoring Script

Save this script to `~/.hermes/scripts/monitor_intelligence_services.sh`:

bash
#!/bin/bash

# Monitor Intelligence Services
# Self-healing watchdog for World Monitor and Crucix
# Run via cron: */5 * * * * /home/user/.hermes/scripts/monitor_intelligence_services.sh

LOG_FILE="$HOME/.hermes/logs/intelligence_monitor.log"
WORLDMONITOR_DIR="$HOME/.hermes/hermes-agent/worldmonitor"
CRUCIX_DIR="$HOME/.hermes/hermes-agent/Crucix"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

check_service() {
    local name="$1"
    local port="$2"
    local endpoint="$3"
    
    local response
    response=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 --max-time 10 "http://localhost:${port}${endpoint}" 2>/dev/null)
    
    if [ "$response" = "200" ]; then
        log "[OK] ${name} is healthy (HTTP ${response})"
        return 0
    else
        log "[WARN] ${name} returned HTTP ${response} - service may be down"
        return 1
    fi
}

restart_service() {
    local name="$1"
    local dir="$2"
    local port="$3"
    local endpoint="$4"
    
    log "[INFO] Attempting to restart ${name}..."
    
    # Kill existing process on port
    pkill -f "node.*${name}" 2>/dev/null || true
    sleep 2
    
    # Restart service
    cd "$dir" && nohup npm run dev > "${name,,}.log" 2>&1 &
    sleep 8
    
    # Verify restart
    local response
    response=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 --max-time 10 "http://localhost:${port}${endpoint}" 2>/dev/null)
    
    if [ "$response" = "200" ]; then
        log "[SUCCESS] ${name} restarted successfully"
        return 0
    else
        log "[ERROR] Failed to restart ${name} - still returning HTTP ${response}"
        return 1
    fi
}

# Main monitoring logic
log "=== Starting intelligence services health check ==="

# Check World Monitor
if check_service "World Monitor" 3000 "/"; then
    :  # Service healthy, do nothing
else
    restart_service "World Monitor" "$WORLDMONITOR_DIR" 3000 "/"
fi

# Check Crucix
if check_service "Crucix" 3117 "/api/health"; then
    :  # Service healthy, do nothing
else
    restart_service "Crucix" "$CRUCIX_DIR" 3117 "/api/health"
fi

log "=== Health check complete ==="
### Step 2: Make Script Executable

bash
chmod +x ~/.hermes/scripts/monitor_intelligence_services.sh
### Step 3: Configure Cron Job

Add to crontab (`crontab -e`) to run every 5 minutes:

bash
*/5 * * * * /home/user/.hermes/scripts/monitor_intelligence_services.sh >> /home/user/.hermes/logs/cron_monitor.log 2>&1
For critical services, run more frequently:

bash
*/2 * * * * /home/user/.hermes/scripts/monitor_intelligence_services.sh
## Troubleshooting

### Service Won't Start

1. Check Node.js is installed: `node --version`
2. Verify dependencies: `cd <service_dir> && npm install`
3. Review service logs for errors: `tail -f <service_dir>/*.log`

### Port Already in Use

bash
# Find process using port
lsof -i :3000
lsof -i :3117

# Kill process if needed
kill -9 <PID>
### Monitoring Script Not Running

1. Verify cron is active: `service cron status` or `systemctl status cron`
2. Check script permissions: `ls -la ~/.hermes/scripts/monitor_intelligence_services.sh`
3. Test script manually: `~/.hermes/scripts/monitor_intelligence_services.sh`

## Alert Notifications (Optional)

To receive alerts on failures, add notification to the restart function:

bash
# Add after failed restart
if [ $? -ne 0 ]; then
    log "[ALERT] ${name} requires manual intervention"
    # Add your notification method here (email, Slack, etc.)
fi