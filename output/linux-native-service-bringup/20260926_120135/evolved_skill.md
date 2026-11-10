---
name: linux-native-service-bringup
description: Install Linux services natively (apt/tarball) with systemd.
category: devops
---

# Native Linux Service Bring-Up

When installing a service natively (apt or GitHub tarball) instead of Docker, follow these four phases. Each has specific pitfalls.

---

## Phase 1 — Install

### Apt route

#### Servarr projects (Radarr/Sonarr/Prowlarr)

> **Note:** servarr.com is defunct. Each project now ships its own apt key and repo from its own domain.

| Project | Repository Domain | Package Name |
|---------|-------------------|--------------|
| Radarr | `radarr.video` | `radarr` |
| Sonarr | `sonarr.tv` | `sonarr` |
| Prowlarr | `prowlarr.com` | `prowlarr` |

Jellyseerr is Docker-only — no apt package available.

#### Generic apt pattern

bash
# 1. Import the signing key
curl -fsSL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x<SIG>" \
  | gpg --dearmor --yes -o /etc/apt/keyrings/<name>.gpg

# 2. Add the repository
echo "deb [signed-by=/etc/apt/keyrings/<name>.gpg] https://<domain>/<repo> <suite> main" \
  > /etc/apt/sources.list.d/<name>.list

# 3. Install
apt-get update && apt-get install -y <package>
#### When the keyserver is missing the signing key

Many projects host their own keyring file directly:

bash
# Example: servarr-style pattern (now defunct but projects migrated here)
curl -fsSL "https://<project-domain>/linux/deb/keyring.gpg" \
  -o /etc/apt/keyrings/<name>.gpg
Check the project's official documentation for the correct keyring URL.

---

### Tarball route

Use this for *arr projects that don't offer apt repos (common post-2026).

#### Step 1: Get release metadata

bash
curl -fsSL "https://api.github.com/repos/<owner>/<repo>/releases/latest" | jq -r '.assets[] | "\(.name) -> \(.browser_download_url)"'
#### Step 2: Identify the correct asset

| Pattern | libc | Example filename |
|---------|------|------------------|
| `*.main.*.linux-x64.tar.gz` | glibc | `Sonarr.main.4.0.2.1234.linux-x64.tar.gz` |
| `*.master.*.linux-core-x64.tar.gz` | glibc | `Radarr.master.10.1.2.3456.linux-core-x64.tar.gz` |
| `*.master.*.linux-musl-core-x64.tar.gz` | musl | `Prowlarr.master.1.5.6.7890.linux-musl-core-x64.tar.gz` |

**Choose `musl` only if** your system uses Alpine Linux. Debian/Ubuntu use glibc.

#### Step 3: Extract and configure

bash
# Extract to /opt
mkdir -p /opt/<App>
tar -xzf /path/to/release.tar.gz -C /opt/<App> --strip-components=1

# Create dedicated service user
useradd -r -s /usr/sbin/nologin -d /var/lib/<app> <app>

# Fix ownership
chown -R <app>:<app> /opt/<App>
chown -R <app>:<app> /var/lib/<app>

# Create data directory
mkdir -p /mnt/ssd/<app>
chown <app>:<app> /mnt/ssd/<app>
---

## Phase 2 — Systemd Unit

### Override drop-in pattern

Create a drop-in file at `/etc/systemd/system/<service>.service.d/override.conf`.

This overrides the upstream unit to redirect data paths and fix common issues.

ini
[Service]
WorkingDirectory=/mnt/ssd/<service>/config
Environment="DATA_DIR=/mnt/ssd/<service>/data"
Environment="CONFIG_DIR=/mnt/ssd/<service>/config"
ExecStart=
ExecStart=/usr/bin/<binary> --data-dir "/mnt/ssd/<service>/data"
### The three rules (prevent 90% of failures)

#### Rule 1: `WorkingDirectory` MUST exist before reload

bash
mkdir -p /mnt/ssd/<service>/config
systemctl daemon-reload
systemctl start <service>
If the directory doesn't exist, the service fails to start with a misleading error.

#### Rule 2: Blank `ExecStart=` before setting new value

The second `ExecStart=` line **must** be preceded by `ExecStart=` (empty) to reset the array.

**Wrong:**
ini
ExecStart=/usr/bin/binary --flag value  # Appends to existing, causes error
**Correct:**
ini
ExecStart=
ExecStart=/usr/bin/binary --flag value  # Replaces existing
#### Rule 3: Inline multi-word flags into `ExecStart`

Quotes or escaping may be needed for paths with spaces:

ini
ExecStart=
ExecStart=/usr/bin/binary --config "/path/with spaces/config.yml"
### Common override examples

#### Jellyfin

ini
[Service]
WorkingDirectory=/mnt/ssd/jellyfin/config
Environment="JELLYFIN_DATA_DIR=/mnt/ssd/jellyfin/data"
Environment="JELLYFIN_CACHE_DIR=/mnt/ssd/jellyfin/cache"
ExecStart=
ExecStart=/usr/bin/jellyfin --datadir "/mnt/ssd/jellyfin/data" --cachedir "/mnt/ssd/jellyfin/cache"
#### Radarr (tarball install)

ini
[Service]
WorkingDirectory=/mnt/ssd/radarr/config
ExecStart=
ExecStart=/opt/Radarr/Radarr -nobrowser -data=/mnt/ssd/radarr/config
---

## Phase 3 — Initial Configuration

### Pre-flight checks before starting

bash
# Verify the binary is executable
ls -la /opt/<App>/<binary>

# Check the unit file exists
systemctl status <service> --no-pager

# Check for port conflicts
ss -tlnp | grep ':<port>'
### First-start behavior

Most services (Radarr, Sonarr, Prowlarr, Jellyfin) open a web UI on their default port:

| Service | Default Port |
|---------|-------------|
| Radarr | 7878 |
| Sonarr | 8989 |
| Prowlarr | 9696 |
| Jellyfin | 8096 |

Access the web UI to complete first-run setup (create admin user, set data directories).

---

## Phase 4 — Verification

### Health checks

bash
# Check service status
systemctl status <service> --no-pager -l

# View recent logs
journalctl -u <service> --no-pager -n 50

# Check for errors
journalctl -u <service> --no-pager -p err

# Verify the process is running
ps aux | grep <service>
### Enable on boot

bash
systemctl enable <service>
### Common failure modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Starting failed: Unit not found` | Unit file missing | Run `systemctl daemon-reload` |
| `Starting failed: WorkingDirectory missing` | Data dir doesn't exist | `mkdir -p /mnt/ssd/<app>/config` |
| `Starting failed: Exec Start line not valid` | Missing `ExecStart=` reset | Add `ExecStart=` before new `ExecStart=` |
| `Process exited with code X` | Config error or missing permissions | Check logs: `journalctl -u <service>` |
| Port already in use | Another service on same port | `ss -tlnp \| grep :<port>` then stop/conflict service |