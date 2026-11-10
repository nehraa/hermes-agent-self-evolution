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

## Steps

### 1. Service Verification
**Check World Monitor (port 3000):**
```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/
```
Expected response: `200`

**Check Crucix health endpoint (port 3117):**
```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:3117/api/health
```
Expected response: `200`

### 2. Service Restart Procedures

**Restart World Monitor:**
```bash
cd ~/.hermes/hermes-agent/worldmonitor && \
nohup npm run dev > worldmonitor.log 2>&1 &
```
Wait 5-10 seconds, then verify with health check.

**Restart Crucix:**
```bash
cd ~/.hermes/hermes-agent/Crucix && \
nohup npm run dev > crucix.log 2>&1 &
```
Wait 5-10 seconds, then verify with health check.

### 3. Logging and Monitoring
All service operations are logged to:
- `~/.hermes/logs/intelligence_monitor.log`
- World Monitor output: `~/.hermes/hermes-agent/worldmonitor/worldmonitor.log`
- Crucix output: `~/.hermes/hermes-agent/Crucix/crucix.log`

### 4. Automated Monitoring Setup
To create a self-healing monitor:
1. Save the monitoring script to `~/.hermes/scripts/monitor_intelligence_services.sh`
2. Make it executable: `chmod +x ~/.hermes/scripts/monitor_intelligence_services.sh`
3. Set up cron job: `*/5 * * * * ~/.hermes/scripts/monitor_intelligence_services.sh`

## Verification
After implementing, verify by:
1. Checking both services respond to HTTP requests
2. Reviewing logs for startup confirmation
3. Confirming automatic restart works by temporarily stopping a service
4. Checking that the cron job runs every 5 minutes

## Troubleshooting
- **Port conflicts**: Check what's running on ports 3000/3117 with `ss -tlnp | grep :300`
- **Permission issues**: Ensure you have write access to log directories
- **NPM problems**: Try `npm install` in service directories if dependencies missing
- **Log rotation**: Monitor log file sizes in production deployments
- **Cron job issues**: If monitoring isn't running, check job status with `hermes cronjob list` and resume paused jobs with `hermes cronjob resume <job_id>`
- **Path errors**: Use absolute paths in scripts (~/.hermes/...) rather than relative paths to avoid "file not found" errors in cron environments
- **Timezone considerations**: Remember that Hermes cron jobs use UTC internally; convert to local time (IST = UTC+5:30) when scheduling

## Safety Notes
- Services are started with `nohup` to survive terminal disconnections
- Output is redirected to log files for debugging
- Health checks use lightweight HTTP requests to minimize overhead
- Restart attempts include appropriate wait times for service initialization