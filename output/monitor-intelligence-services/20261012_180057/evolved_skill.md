---
name: monitor-intelligence-services
description: Systematic approach to ensure World Monitor and Crucix intelligence platforms remain operational with automatic restart capabilities.
category: devops
---

# Monitor Intelligence Services

Systematic approach to ensure World Monitor and Crucix intelligence platforms remain operational with automatic restart capabilities.

## Overview

This skill provides automated health monitoring and self-healing restart capabilities for two critical intelligence platforms:

- **World Monitor** — Primary intelligence gathering service
- **Crucix** — Secondary intelligence processing service

The monitoring system detects service failures and automatically restarts the affected service, ensuring minimal downtime for critical OSINT infrastructure.

## Service Configuration

| Service | Directory | Port | Health Endpoint |
|---------|-----------|------|-----------------|
| World Monitor | `~/.hermes/hermes-agent/worldmonitor/` | 3000 | `http://localhost:3000/` |
| Crucix | `~/.hermes/hermes-agent/Crucix/` | 3117 | `http://localhost:3117/api/health` |

### Prerequisites

- Node.js and npm installed
- Bash-compatible shell
- Hermes cronjob scheduler configured
- Write access to `~/.hermes/logs/` directory

## Health Check Procedures

### World Monitor

bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/
# Success: 200
# Failure: Connection refused, timeout, or non-200 response
### Crucix

bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:3117/api/health
# Success: 200
# Failure: Connection refused, timeout, or non-200 response
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
## Log Files

| Service | Log Location |
|---------|--------------|
| Monitor Script | `~/.hermes/logs/intelligence_monitor.log` |
| World Monitor | `~/.hermes/hermes-agent/worldmonitor/worldmonitor.log` |
| Crucix | `~/.hermes/hermes-agent/Crucix/crucix.log` |

## Automated Monitoring Setup

### Step 1: Create the Monitoring Directory

bash
mkdir -p ~/.hermes/scripts ~/.hermes/logs
### Step 2: Create the Monitoring Script

Save the following script to `~/.hermes/scripts/monitor_intelligence_services.sh`:

bash
#!/bin/bash

# Monitor Intelligence Services
# Self-healing watchdog for World Monitor and Crucix

set -euo pipefail

# Configuration
LOG_FILE="$HOME/.hermes/logs/intelligence_monitor.log"
WORLDMONITOR_DIR="$HOME/.hermes/hermes-agent/worldmonitor"
CRUCIX_DIR="$HOME/.hermes/hermes-agent/Crucix"
WORLDMONITOR_PORT=3000
CRUCIX_PORT=3117

# Ensure log directory exists
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

check_service() {
    local name="$1"
    local port="$2"
    local endpoint="$3"
    
    if [ "$name" = "World Monitor" ]; then
        status=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "http://localhost:${port}/" 2>/dev/null || echo "000")
    else
        status=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "http://localhost:${port}${endpoint}" 2>/dev/null || echo "000")
    fi
    
    [ "$status" = "200" ]
}

restart_service() {
    local name="$1"
    local dir="$2"
    local port="$3"
    local log_suffix="$4"
    
    log "WARNING: $name not responding on port $port. Initiating restart..."
    
    # Kill existing process on port
    pkill -f "node.*$name" 2>/dev/null || true
    sleep 2
    
    # Start service
    cd "$dir"
    nohup npm run dev > "$HOME/.hermes/hermes-agent/${log_suffix}/${log_suffix}.log" 2>&1 &
    sleep 8
    
    # Verify restart
    if check_service "$name" "$port" "/api/health"; then
        log "SUCCESS: $name restarted successfully"
    else
        log "ERROR: Failed to restart $name after maximum attempts"
        return 1
    fi
}

# Main monitoring loop
main() {
    log "=== Starting intelligence services health check ==="
    
    # Check World Monitor
    if check_service "World Monitor" "$WORLDMONITOR_PORT" "/api/health"; then
        log "OK: World Monitor responding on port $WORLDMONITOR_PORT"
    else
        restart_service "World Monitor" "$WORLDMONITOR_DIR" "$WORLDMONITOR_PORT" "worldmonitor"
    fi
    
    # Check Crucix
    if check_service "Crucix" "$CRUCIX_PORT" "/api/health"; then
        log "OK: Crucix responding on port $CRUCIX_PORT"
    else
        restart_service "Crucix" "$CRUCIX_DIR" "$CRUCIX_PORT" "Crucix"
    fi
    
    log "=== Health check complete ==="
}

main "$@"
### Step 3: Make Script Executable

bash
chmod +x ~/.hermes/scripts/monitor_intelligence_services.sh
### Step 4: Configure Cronjob

Open the crontab editor:

bash
crontab -e
Add the following entry to run health checks every 5 minutes:

cron
*/5 * * * * /home/USER/.hermes/scripts/monitor_intelligence_services.sh >> /home/USER/.hermes/logs/intelligence_monitor.log 2>&1
Replace `USER` with your actual username, or use `$HOME` path.

### Alternative: Run Hourly

For less frequent checks, use:

cron
0 * * * * /home/USER/.hermes/scripts/monitor_intelligence_services.sh >> /home/USER/.hermes/logs/intelligence_monitor.log 2>&1
## Verification

### Test the Monitoring Script Manually

bash
~/.hermes/scripts/monitor_intelligence_services.sh
Expected output in log file:
[2024-01-15 10:00:00] === Starting intelligence services health check ===
[2024-01-15 10:00:01] OK: World Monitor responding on port 3000
[2024-01-15 10:00:02] OK: Crucix responding on port 3117
[2024-01-15 10:00:03] === Health check complete ===
### Check Cronjob is Running

bash
crontab -l
### View Recent Logs

bash
tail -f ~/.hermes/logs/intelligence_monitor.log
## Troubleshooting

| Issue | Solution |
|-------|----------|
| Script not executable | Run `chmod +x ~/.hermes/scripts/monitor_intelligence_services.sh` |
| Cronjob not running | Verify with `crontab -l` and check cron status |
| Port already in use | Kill existing process: `pkill -f "node.*3000"` |
| Permission denied | Ensure user owns the hermes directory |
| Service keeps restarting | Check application logs for underlying errors |

### View Service Logs for Errors

bash
# World Monitor
tail -50 ~/.hermes/hermes-agent/worldmonitor/worldmonitor.log

# Crucix
tail -50 ~/.hermes/hermes-agent/Crucix/crucix.log
## Quick Reference

bash
# Manual health check
~/.hermes/scripts/monitor_intelligence_services.sh

# View monitoring logs
tail -f ~/.hermes/logs/intelligence_monitor.log

# View World Monitor logs
tail -f ~/.hermes/hermes-agent/worldmonitor/worldmonitor.log

# View Crucix logs
tail -f ~/.hermes/hermes-agent/Crucix/crucix.log

# Manual restart
cd ~/.hermes/hermes-agent/worldmonitor && nohup npm run dev &
cd ~/.hermes/hermes-agent/Crucix && nohup npm run dev &