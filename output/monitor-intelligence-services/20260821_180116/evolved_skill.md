---
name: monitor-intelligence-services
description: Systematic approach to ensure World Monitor and Crucix intelligence platforms remain operational with automatic restart capabilities.
category: devops
---

# Monitor Intelligence Services

Ensure continuous operation of World Monitor and Crucix intelligence platforms with automatic failure detection and recovery.

## When to Use

- Deploy 24/7 monitoring for intelligence gathering platforms
- Automate recovery from service crashes or hangs
- Maintain uptime guarantees for OSINT infrastructure
- Proactively manage Hermes Agent services without manual intervention

## Prerequisites

| Service | Path | Port | Health Endpoint |
|---------|------|------|-----------------|
| World Monitor | `~/.hermes/hermes-agent/worldmonitor/` | 3000 | `http://localhost:3000/` |
| Crucix | `~/.hermes/hermes-agent/Crucix/` | 3117 | `http://localhost:3117/api/health` |

**Requirements:**
- Node.js and npm installed
- Shell access with execute permissions
- Hermes cronjob scheduler configured
- `~/.hermes/logs/` directory exists

## Service Health Checks

Verify service status before attempting restarts.

### World Monitor

bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/
# Returns: 200 (healthy) | Connection refused/timeout/other (unhealthy)
### Crucix

bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:3117/api/health
# Returns: 200 (healthy) | Connection refused/timeout/other (unhealthy)
## Restart Procedures

Execute only after confirming service failure via health check.

### Restart World Monitor

bash
cd ~/.hermes/hermes-agent/worldmonitor && \
nohup npm run dev > worldmonitor.log 2>&1 &
sleep 5 && \
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/
# Verify output is 200 before considering restart successful
### Restart Crucix

bash
cd ~/.hermes/hermes-agent/Crucix && \
nohup npm run dev > crucix.log 2>&1 &
sleep 5 && \
curl -s -o /dev/null -w "%{http_code}" http://localhost:3117/api/health
# Verify output is 200 before considering restart successful
## Log Files

| Service | Log Location |
|---------|--------------|
| Monitoring Script | `~/.hermes/logs/intelligence_monitor.log` |
| World Monitor | `~/.hermes/hermes-agent/worldmonitor/worldmonitor.log` |
| Crucix | `~/.hermes/hermes-agent/Crucix/crucix.log` |

## Automated Monitoring Script

### Step 1: Create the Monitoring Script

Save to `~/.hermes/scripts/monitor_intelligence_services.sh`:

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
    local status_code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$url")
    
    if [ "$status_code" = "200" ]; then
        echo "healthy"
    else
        echo "unhealthy"
    fi
}

restart_worldmonitor() {
    log "Restarting World Monitor..."
    pkill -f "worldmonitor" || true
    cd "$WORLDMONITOR_DIR" && \
    nohup npm run dev > worldmonitor.log 2>&1 &
    sleep 8
    if [ "$(check_service "World Monitor" "http://localhost:3000/")" = "healthy" ]; then
        log "World Monitor restarted successfully"
        return 0
    else
        log "ERROR: World Monitor restart failed"
        return 1
    fi
}

restart_crucix() {
    log "Restarting Crucix..."
    pkill -f "Crucix" || true
    cd "$CRUCIX_DIR" && \
    nohup npm run dev > crucix.log 2>&1 &
    sleep 8
    if [ "$(check_service "Crucix" "http://localhost:3117/api/health")" = "healthy" ]; then
        log "Crucix restarted successfully"
        return 0
    else
        log "ERROR: Crucix restart failed"
        return 1
    fi
}

# Main monitoring loop
log "=== Starting Intelligence Services Monitor ==="

# Check World Monitor
if [ "$(check_service "World Monitor" "http://localhost:3000/")" = "unhealthy" ]; then
    log "World Monitor is DOWN - initiating restart"
    restart_worldmonitor
else
    log "World Monitor is healthy"
fi

# Check Crucix
if [ "$(check_service "Crucix" "http://localhost:3117/api/health")" = "unhealthy" ]; then
    log "Crucix is DOWN - initiating restart"
    restart_crucix
else
    log "Crucix is healthy"
fi

log "=== Monitor cycle complete ==="
### Step 2: Make Executable

bash
chmod +x ~/.hermes/scripts/monitor_intelligence_services.sh
### Step 3: Schedule via Cron

Add to crontab (`crontab -e`):

bash
# Run every 5 minutes
*/5 * * * * ~/.hermes/scripts/monitor_intelligence_services.sh

# For faster response (every minute), use:
# * * * * * ~/.hermes/scripts/monitor_intelligence_services.sh
### Step 4: Ensure Log Directory Exists

bash
mkdir -p ~/.hermes/logs
touch ~/.hermes/logs/intelligence_monitor.log
## Troubleshooting

| Issue | Resolution |
|-------|------------|
| Script not running | Verify cron is active: `systemctl status cron` or `service cron status` |
| Services won't start | Check Node.js dependencies: `cd <service_dir> && npm install` |
| Logs show permission denied | Fix ownership: `chown -R $USER:$USER ~/.hermes` |
| Port already in use | Find conflicting process: `lsof -i :3000` or `lsof -i :3117` |
| Constant restart loop | Check application logs for crash root cause, not just monitor logs |

## Verification

Test the monitoring system manually:

bash
# Run the script directly
~/.hermes/scripts/monitor_intelligence_services.sh

# Check recent log entries
tail -20 ~/.hermes/logs/intelligence_monitor.log

# Verify both services respond
curl -s http://localhost:3000/ | head -1
curl -s http://localhost:3117/api/health