---
name: monitor-intelligence-services
description: Systematic approach to ensure World Monitor and Crucix intelligence platforms remain operational with automatic restart capabilities.
category: devops
---

# Monitor Intelligence Services

Ensure continuous operation of World Monitor and Crucix intelligence platforms with automatic failure detection and restart capabilities.

## Overview

| Service | Port | Location | Health Endpoint |
|---------|------|----------|-----------------|
| World Monitor | 3000 | `~/.hermes/hermes-agent/worldmonitor/` | `http://localhost:3000/` |
| Crucix | 3117 | `~/.hermes/hermes-agent/Crucix/` | `http://localhost:3117/api/health` |

## Prerequisites

- World Monitor installed at `~/.hermes/hermes-agent/worldmonitor/`
- Crucix installed at `~/.hermes/hermes-agent/Crucix/`
- Node.js and npm available
- Shell access with execute permissions

## Health Check Commands

### Check World Monitor
bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/
# Expected: 200
### Check Crucix
bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:3117/api/health
# Expected: 200
If either returns a non-200 status or connection is refused, the service is down and requires restart.

## Service Restart Procedures

### Restart World Monitor

bash
cd ~/.hermes/hermes-agent/worldmonitor && \
pkill -f "node.*worldmonitor" 2>/dev/null || true && \
nohup npm run dev > worldmonitor.log 2>&1 &

# Verify
sleep 5 && curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/
# Should return: 200
### Restart Crucix

bash
cd ~/.hermes/hermes-agent/Crucix && \
pkill -f "node.*crucix" 2>/dev/null || true && \
nohup npm run dev > crucix.log 2>&1 &

# Verify
sleep 5 && curl -s -o /dev/null -w "%{http_code}" http://localhost:3117/api/health
# Should return: 200
## Log Locations

| Log | Path |
|-----|------|
| Monitoring activity | `~/.hermes/logs/intelligence_monitor.log` |
| World Monitor output | `~/.hermes/hermes-agent/worldmonitor/worldmonitor.log` |
| Crucix output | `~/.hermes/hermes-agent/Crucix/crucix.log` |

## Automated Monitoring Setup

### Step 1: Create Monitoring Script

Save this script to `~/.hermes/scripts/monitor_intelligence_services.sh`

> **Important:** Filename must end in `.sh` — Hermes cronjob scheduler auto-runs `.sh`/`.bash` files as Bash. A bash script with no extension silently fails with `SyntaxError` on every tick. (See `service-verification` skill, "Pitfalls".)

bash
#!/bin/bash

LOG_DIR="$HOME/.hermes/logs"
LOG_FILE="$LOG_DIR/intelligence_monitor.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

check_service() {
    local name="$1"
    local url="$2"
    local response
    response=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$url" 2>/dev/null)
    
    if [ "$response" = "200" ]; then
        log "[OK] $name is running"
        return 0
    else
        log "[WARN] $name returned HTTP $response — needs restart"
        return 1
    fi
}

restart_worldmonitor() {
    log "[INFO] Restarting World Monitor..."
    cd "$HOME/.hermes/hermes-agent/worldmonitor" || exit 1
    pkill -f "node.*worldmonitor" 2>/dev/null || true
    sleep 2
    nohup npm run dev > worldmonitor.log 2>&1 &
    sleep 5
    
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/ | grep -q "200"; then
        log "[OK] World Monitor restarted successfully"
    else
        log "[ERROR] World Monitor restart failed"
    fi
}

restart_crucix() {
    log "[INFO] Restarting Crucix..."
    cd "$HOME/.hermes/hermes-agent/Crucix" || exit 1
    pkill -f "node.*crucix" 2>/dev/null || true
    sleep 2
    nohup npm run dev > crucix.log 2>&1 &
    sleep 5
    
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:3117/api/health | grep -q "200"; then
        log "[OK] Crucix restarted successfully"
    else
        log "[ERROR] Crucix restart failed"
    fi
}

# Main execution
log "=== Starting intelligence services check ==="

check_service "World Monitor" "http://localhost:3000/" || restart_worldmonitor
check_service "Crucix" "http://localhost:3117/api/health" || restart_crucix

log "=== Intelligence services check complete ==="
### Step 2: Make Executable

bash
chmod +x ~/.hermes/scripts/monitor_intelligence_services.sh
### Step 3: Create Cron Job

bash
cronjob(
    action='create',
    name='intelligence-services-watchdog',
    schedule='*/5 * * * *',
    script='monitor_intelligence_services.sh'
)
This runs the health check every 5 minutes.

## Troubleshooting

| Issue | Diagnosis | Resolution |
|-------|-----------|------------|
| Connection refused | Service not running | Run restart procedure |
| HTTP 502/503 | Service crashed or port conflict | Check logs, restart service |
| Process exists but not responding | Port blocked or OOM | Kill process, clear port, restart |
| Restart fails repeatedly | Dependency issue or port in use | Check `netstat -tlnp | grep <port>`, resolve conflict |

## Quick Reference

bash
# One-liner health check
curl -s http://localhost:3000/ && echo " World Monitor OK" || echo " World Monitor DOWN"; \
curl -s http://localhost:3117/api/health && echo " Crucix OK" || echo " Crucix DOWN"