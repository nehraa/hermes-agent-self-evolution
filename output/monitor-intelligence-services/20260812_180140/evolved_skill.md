---
name: monitor-intelligence-services
description: Systematic approach to ensure World Monitor and Crucix intelligence platforms remain operational with automatic restart capabilities.
category: devops
---

# Monitor Intelligence Services

Systematic approach to ensure World Monitor and Crucix intelligence platforms remain operational with automatic restart capabilities.

## When to Use

- Ensure continuous operation of intelligence platforms
- Automatically detect and recover from service failures
- Maintain 24/7 availability of global intelligence gathering systems
- Set up self-healing monitoring for critical OSINT infrastructure

## Prerequisites

| Component | Location | Port |
|-----------|----------|------|
| World Monitor | `~/.hermes/hermes-agent/worldmonitor/` | 3000 |
| Crucix | `~/.hermes/hermes-agent/Crucix/` | 3117 |

Required:
- Node.js and npm installed
- Basic shell access
- Hermes cronjob scheduler configured

## Service Health Checks

### World Monitor (port 3000)

bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/
# Expected: 200
# Failure: Connection refused, timeout, or non-200 status
### Crucix (port 3117)

bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:3117/api/health
# Expected: 200
# Failure: Connection refused, timeout, or non-200 status
## Restart Procedures

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
| Hermes Monitor | `~/.hermes/logs/intelligence_monitor.log` |
| World Monitor | `~/.hermes/hermes-agent/worldmonitor/worldmonitor.log` |
| Crucix | `~/.hermes/hermes-agent/Crucix/crucis.log` |

## Automated Monitoring Setup

### Step 1: Create the Monitoring Script

Save this script to `~/.hermes/scripts/monitor_intelligence_services.sh`:

bash
#!/bin/bash

# Monitor Intelligence Services
# Self-healing watchdog for World Monitor and Crucix

LOG_FILE="$HOME/.hermes/logs/intelligence_monitor.log"
WORLDMONITOR_DIR="$HOME/.hermes/hermes-agent/worldmonitor"
CRUCIX_DIR="$HOME/.hermes/hermes-agent/Crucix"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

check_service() {
    local name="$1"
    local url="$2"
    local status=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$url" 2>/dev/null)
    [ "$status" = "200" ]
}

restart_service() {
    local name="$1"
    local dir="$2"
    local port="$3"
    local log_file="$4"

    log "Restarting $name (port $port)..."
    pkill -f "$name" 2>/dev/null
    sleep 2
    cd "$dir" && nohup npm run dev > "$log_file" 2>&1 &
    sleep 8

    if curl -s -o /dev/null --max-time 10 "http://localhost:$port/api/health" 2>/dev/null; then
        log "$name restarted successfully"
    else
        # Fallback health check for World Monitor (no /api/health endpoint)
        if curl -s -o /dev/null --max-time 10 "http://localhost:$port/" 2>/dev/null; then
            log "$name restarted successfully"
        else
            log "ERROR: $name failed to restart"
        fi
    fi
}

# Monitor World Monitor
if check_service "World Monitor" "http://localhost:3000/"; then
    log "World Monitor: OK"
else
    log "World Monitor: DOWN - initiating restart"
    restart_service "worldmonitor" "$WORLDMONITOR_DIR" "3000" "$WORLDMONITOR_DIR/worldmonitor.log"
fi

# Monitor Crucix
if check_service "Crucix" "http://localhost:3117/api/health"; then
    log "Crucix: OK"
else
    log "Crucix: DOWN - initiating restart"
    restart_service "crucix" "$CRUCIX_DIR" "3117" "$CRUCIX_DIR/crucix.log"
fi
### Step 2: Make Executable

bash
chmod +x ~/.hermes/scripts/monitor_intelligence_services.sh
### Step 3: Configure Cron Job

bash
cronjob(
    action='create',
    name='intelligence-services-watchdog',
    schedule='*/5 * * * *',
    script='monitor_intelligence_services.sh'
)
This runs the health check every 5 minutes and automatically restarts any down services.

## Common Issues and Resolutions

| Symptom | Likely Cause | Resolution |
|---------|--------------|------------|
| `curl: (7) Failed to connect` | Service not running | Run restart procedure |
| `curl: (28) Operation timed out` | Service hanging | `pkill -f <service>` then restart |
| Service restarts but fails immediately | Port already in use | `lsof -i :<port>` to check, kill conflicting process |
| Logs show `EADDRINUSE` | Another instance running | `pkill -f worldmonitor` or `pkill -f crucix` |

## Verify Monitoring is Active

bash
# Check last monitor run
tail -n 10 ~/.hermes/logs/intelligence_monitor.log

# Ensure cron job exists
cronjob(action='list') | grep intelligence-services-watchdog