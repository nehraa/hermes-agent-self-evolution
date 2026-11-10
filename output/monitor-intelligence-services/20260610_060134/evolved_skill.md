---
name: monitor-intelligence-services
description: Systematic approach to ensure World Monitor and Crucix intelligence platforms remain operational with automatic restart capabilities.
category: devops
---

# Monitor Intelligence Services

Systematic approach to ensure World Monitor and Crucix intelligence platforms remain operational with automatic restart capabilities.

## When to Use

Use this skill when you need to:

- Ensure continuous operation of World Monitor (port 3000) and Crucix (port 3117) intelligence platforms
- Automatically detect and recover from service failures
- Maintain 24/7 availability of global intelligence gathering systems
- Set up self-healing monitoring for critical OSINT infrastructure

## Prerequisites

- World Monitor installed at: `~/.hermes/hermes-agent/worldmonitor/`
- Crucix installed at: `~/.hermes/hermes-agent/Crucix/`
- Node.js and npm available
- Basic shell access
- `curl` installed for health checks

## Architecture Overview

| Service | Port | Health Endpoint | Log File |
|---------|------|-----------------|----------|
| World Monitor | 3000 | `http://localhost:3000/` | `worldmonitor.log` |
| Crucix | 3117 | `http://localhost:3117/api/health` | `crucix.log` |

## Steps

### 1. Service Verification

**Check World Monitor status:**
bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/
Expected response: `200`

**Check Crucix health endpoint:**
bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:3117/api/health
Expected response: `200`

**Combined verification script:**
bash
#!/bin/bash
WORLDMONITOR=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/)
CRUCIX=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3117/api/health)
echo "World Monitor: $WORLDMONITOR"
echo "Crucix: $CRUCIX"
### 2. Service Restart Procedures

**Restart World Monitor:**
bash
cd ~/.hermes/hermes-agent/worldmonitor && \
nohup npm run dev > worldmonitor.log 2>&1 &
echo "World Monitor restarting..."
sleep 5
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/
**Restart Crucix:**
bash
cd ~/.hermes/hermes-agent/Crucix && \
nohup npm run dev > crucix.log 2>&1 &
echo "Crucix restarting..."
sleep 5
curl -s -o /dev/null -w "%{http_code}" http://localhost:3117/api/health
**Force restart (kill existing process first):**
bash
# Kill existing processes
pkill -f "worldmonitor" || true
pkill -f "Crucix" || true

# Restart with small delay
sleep 2
cd ~/.hermes/hermes-agent/worldmonitor && nohup npm run dev > worldmonitor.log 2>&1 &
cd ~/.hermes/hermes-agent/Crucix && nohup npm run dev > crucix.log 2>&1 &
### 3. Logging and Monitoring

All service operations are logged to:

| Log Location | Description |
|--------------|-------------|
| `~/.hermes/logs/intelligence_monitor.log` | Monitoring script execution logs |
| `~/.hermes/hermes-agent/worldmonitor/worldmonitor.log` | World Monitor stdout/stderr |
| `~/.hermes/hermes-agent/Crucix/crucix.log` | Crucix stdout/stderr |

**View recent logs:**
bash
tail -f ~/.hermes/hermes-agent/worldmonitor/worldmonitor.log
tail -f ~/.hermes/hermes-agent/Crucix/crucix.log
tail -f ~/.hermes/logs/intelligence_monitor.log
### 4. Automated Monitoring Setup

#### Step 1: Create the monitoring script

bash
mkdir -p ~/.hermes/scripts ~/.hermes/logs
Save this script to `~/.hermes/scripts/monitor_intelligence_services.sh`:

bash
#!/bin/bash
# monitor_intelligence_services.sh
# Automated monitoring and restart for intelligence platforms
# Runs via cron every 5 minutes

LOG_FILE="$HOME/.hermes/logs/intelligence_monitor.log"
WORLDMONITOR_DIR="$HOME/.hermes/hermes-agent/worldmonitor"
CRUCIX_DIR="$HOME/.hermes/hermes-agent/Crucix"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

check_service() {
    local name="$1"
    local url="$2"
    local response
    response=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$url" 2>/dev/null)
    [ "$response" = "200" ]
}

restart_service() {
    local name="$1"
    local dir="$2"
    local port="$3"
    
    log "WARNING: $name is down, attempting restart..."
    
    # Kill existing process on port
    pkill -f "$name" 2>/dev/null || true
    sleep 2
    
    # Start service
    cd "$dir"
    nohup npm run dev > "${name,,}.log" 2>&1 &
    
    # Wait and verify
    sleep 10
    
    if check_service "$name" "http://localhost:$port/"; then
        log "SUCCESS: $name restarted successfully"
        return 0
    else
        log "ERROR: Failed to restart $name"
        return 1
    fi
}

# Main monitoring logic
log "Starting monitoring check..."

# Check World Monitor (port 3000)
if check_service "World Monitor" "http://localhost:3000/"; then
    log "OK: World Monitor is running"
else
    restart_service "World Monitor" "$WORLDMONITOR_DIR" "3000"
fi

# Check Crucix (port 3117)
if check_service "Crucix" "http://localhost:3117/api/health"; then
    log "OK: Crucix is running"
else
    restart_service "Crucix" "$CRUCIX_DIR" "3117"
fi

log "Monitoring check completed"
#### Step 2: Make executable

bash
chmod +x ~/.hermes/scripts/monitor_intelligence_services.sh
#### Step 3: Set up cron job

bash
# Edit crontab
crontab -e

# Add this line (runs every 5 minutes)
*/5 * * * * ~/.hermes/scripts/monitor_intelligence_services.sh >> ~/.hermes/logs/cron.log 2>&1

# Verify crontab
crontab -l
#### Step 4: Create log rotation (optional)

bash
# Add to /etc/logrotate.d/hermes or use daily rotation
sudo nano /etc/logrotate.d/hermes
conf
~/.hermes/logs/*.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
}
## Verification

After implementing, verify by running these checks:

bash
# 1. Test the monitoring script manually
~/.hermes/scripts/monitor_intelligence_services.sh

# 2. Check logs for successful startup
cat ~/.hermes/logs/intelligence_monitor.log

# 3. Verify both services respond
curl -s http://localhost:3000/ | head -5
curl -s http://localhost:3117/api/health

# 4. Confirm cron job is active
grep monitor_intelligence /var/log/syslog 2>/dev/null || \
  grep monitor_intelligence ~/.hermes/logs/cron.log

# 5. Test automatic restart by killing a service
pkill -f "worldmonitor"
# Wait 5-10 minutes, then check if it restarted automatically
cat ~/.hermes/logs/intelligence_monitor.log | grep -A1 "World Monitor is down"
## Troubleshooting

| Issue | Diagnosis | Solution |
|-------|-----------|----------|
| Port 3000 already in use | `lsof -i :3000` | Kill conflicting process or change port in config |
| Port 3117 already in use | `lsof -i :3117` | Kill conflicting process or change port in config |
| Service starts but crashes | Check `*.log` files | Look for Node.js errors, missing dependencies |
| Cron not running | `grep CRON /var/log/syslog` | Ensure cron daemon is running: `service cron start` |
| npm command not found | Check PATH | Add `export PATH="$PATH:$HOME/.nvm/versions/node/*/bin"` |
| Permission denied | `ls -la ~/.hermes/scripts/` | Run `chmod +x monitor_intelligence_services.sh` |
| Service starts but returns non-200 | Check health endpoint | Review app logs for startup errors |

**Debug steps:**

bash
# Check if process is running
ps aux | grep -E "(worldmonitor|Crucix)"

# Check port binding
netstat -tlnp | grep -E "(3000|3117)"

# View real-time logs
tail -f ~/.hermes/hermes-agent/worldmonitor/worldmonitor.log
tail -f ~/.hermes/hermes-agent/Crucix/crucix.log

# Check Node version
node --version
npm --version
## Quick Reference Commands

bash
# Check status
~/.hermes/scripts/monitor_intelligence_services.sh

# View monitor logs
tail -20 ~/.hermes/logs/intelligence_monitor.log

# Manual restart
pkill -f "worldmonitor" && pkill -f "Crucix"
sleep 2
cd ~/.hermes/hermes-agent/worldmonitor && nohup npm run dev > worldmonitor.log 2>&1 &
cd ~/.hermes/hermes-agent/Crucix && nohup npm run dev > crucix.log 2>&1 &