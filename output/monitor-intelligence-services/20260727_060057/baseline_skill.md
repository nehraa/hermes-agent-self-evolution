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

## Automated Monitoring Setup
To create a self-healing monitor:
1. Save the monitoring script to `~/.hermes/scripts/monitor_intelligence_services.sh`
   (**must end in `.sh`** — Hermes cronjob scheduler auto-runs `.sh`/`.bash` as bash,
   everything else as Python; a bash script with no extension silently fails with
   `SyntaxError` on every tick. See `service-verification` skill, "Pitfalls".)
2. Make it executable: `chmod +x ~/.hermes/scripts/monitor_intelligence_services.sh`
3. Set up cron job: `cronjob(action='create', name='intelligence-services-watchdog',
   schedule='*/5 * * * *', script='monitor_intelligence_services.sh', no_agent=True,
   deliver='local')`

**The 3-state loud-alert contract (user requirement, June 24 2026):**

User explicitly stated: *ping only when the service is broken AND I could not
fix it myself.* The cron must enforce this via exit code + stdout, NOT by
swapping `deliver` per failure:

| State | Exit code | stdout | User pings? |
|-------|-----------|--------|-------------|
| All healthy | 0 | empty | no |
| Auto-recovered within run | 0 | empty | no (recovery logged only) |
| Could not fix after N attempts | **non-zero** | `❌ ... Manual intervention required` | **yes** |

- Threshold: 2 consecutive cron ticks down before alerting (one transient blip
  should not wake the user).
- `deliver='local'` is the right baseline; the script decides loud vs silent.
- Loud message must include: service label + port, fail count, last restart
  time, cooldown status, and the literal phrase `Manual intervention required`
  so it's greppable.

**For multi-PID stacks** (Next.js, pnpm/npm wrappers), the watchdog must:
- Collect ALL PIDs on the port, not just the first: `ss -tlnp | grep "(:PORT[[:space:]]|:PORT$)" | grep -oE 'pid=[0-9]+'`
- Track last-restart epoch and enforce a cooldown (10 min) to prevent restart loops
- Wait a startup grace (15s) and re-probe health before claiming success
- Capture child PID inside the `( ... & )` subshell: `$!` is empty after `setsid`
- Use `<label>.fails=N` counter in state file to track consecutive failures across
  ticks; clear when service comes back healthy

See the OpenMAIC watchdog at `~/.hermes/scripts/openmaic-watchdog.sh` for the
worked reference implementation (also at
`~/.hermes/skills/devops/openmaic-self-host/scripts/openmaic-watchdog`).

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