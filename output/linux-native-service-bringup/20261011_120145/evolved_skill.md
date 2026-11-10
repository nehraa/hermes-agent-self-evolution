---
name: linux-native-service-bringup
description: Install Linux services natively (apt/tarball) with systemd.
category: devops
---

# Native Linux Service Bring-Up

Install services natively (apt or tarball) instead of Docker. Four phases, each with common traps.

## Phase 1 — Install

### Apt route

For **Servarr** projects (Radarr/Sonarr/Prowlarr): servarr.com is defunct. Each project now ships its own apt key and repo:

| Project | Domain |
|---------|--------|
| Radarr | `radarr.video` |
| Sonarr | `sonarr.tv` |
| Prowlarr | `prowlarr.com` |
| Jellyseerr | `jellyseerr.dev` (Docker-only — no apt) |

**Generic pattern:**

bash
# 1. Import the signing key
curl -fsSL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x<SIG>" \
  | gpg --dearmor --yes -o /etc/apt/keyrings/<name>.gpg

# 2. Add the repository
echo "deb [signed-by=/etc/apt/keyrings/<name>.gpg] https://<domain>/<repo> <suite> main" \
  > /etc/apt/sources.list.d/<name>.list

# 3. Install
apt-get update && apt-get install -y <package>
**Keyring fallback:** If the signing key is missing from Ubuntu keyserver, look for `keyring.gpg` on the project's apt repo domain (e.g., `https://radarr.video/linux/deb/keyring.gpg`).

### Tarball route

Use for *arr projects that don't offer apt packages (common post-2026).

**Step 1 — Get release info:**

bash
curl -fsSL "https://api.github.com/repos/<owner>/<repo>/releases/latest" \
  | jq -r '.assets[].browser_download_url'
**Step 2 — Asset naming patterns:**

| Pattern | Example | Used by |
|---------|---------|---------|
| Old | `<App>.main.<ver>.linux-x64.tar.gz` | Sonarr |
| New | `<App>.master.<ver>.linux-core-x64.tar.gz` | Radarr, Prowlarr |
| musl | `<App>.master.<ver>.linux-musl-core-x64.tar.gz` | Alpine-based systems |

**Step 3 — Install:**

bash
# Extract to /opt
tar -xzf <App>.*.linux-x64.tar.gz -C /opt/
mv /opt/<App> /opt/<App>-<version>   # optional: versioned dir
ln -s /opt/<App>-<version> /opt/<App> # symlink for easy updates

# Create service user
useradd -r -s /usr/sbin/nologin -d /var/lib/<app> <app>

# Fix ownership
chown -R <app>:<app> /opt/<App>
## Phase 2 — Systemd Unit (override.conf)

Every native install on this server needs a drop-in override at `/etc/systemd/system/<service>.service.d/override.conf`.

**Required overrides:**

ini
[Service]
WorkingDirectory=/mnt/ssd/<service>/config
Environment=CONFIGPATH=/mnt/ssd/<service>/config
ExecStart=
ExecStart=/usr/bin/<binary> --config /mnt/ssd/<service>/config
### Three rules (memorize — prevent 90% of failures)

1. **`WorkingDirectory` MUST exist before the unit starts.** Create it first:
   ```bash
   mkdir -p /mnt/ssd/<service>/config
   chown <service>:<service> /mnt/ssd/<service>/config
   ```

2. **Clear `ExecStart` before setting a new one.** systemd requires this explicit reset when overriding.

3. **Inline multi-word flags into `ExecStart`.** Don't use `Environment=` for paths with spaces or complex arguments.

### Worked example: Jellyfin

ini
[Service]
WorkingDirectory=/mnt/ssd/jellyfin/config
Environment=JELLYFIN_DATA_DIR=/mnt/ssd/jellyfin/data
Environment=JELLYFIN_CACHE_DIR=/mnt/ssd/jellyfin/cache
ExecStart=
ExecStart=/usr/bin/jellyfin --datadir /mnt/ssd/jellyfin/data --cachedir /mnt/ssd/jellyfin/cache
After creating the override:
bash
systemctl daemon-reload
systemctl enable --now <service>
## Phase 3 — Initial Configuration

**Check for startup failures:**

bash
systemctl status <service>
journalctl -u <service> -f --lines=50
**Common first-run issues:**

| Symptom | Cause | Fix |
|---------|-------|-----|
| "Connection refused" on port | Service not binding to expected interface | Check `bind_address` in config or logs |
| Permission denied on data dir | Wrong ownership | `chown -R <app>:<app> /mnt/ssd/<app>` |
| Database locked | Stale lock file | `rm /mnt/ssd/<app>/config/*.lock` |
| Port already in use | Another instance running | `lsof -i :<port>` to find conflict |

**Verify the service is reachable:**

bash
# Check it's listening
ss -tlnp | grep <port>

# Test local connectivity
curl -s http://127.0.0.1:<port>/api/health
## Phase 4 — Maintenance

**Backup paths to monitor:**

/mnt/ssd/<app>/config/     # configs
/mnt/ssd/<app>/data/       # databases
/opt/<app>/                # binaries
/etc/systemd/system/<app>.service.d/  # overrides
**Update procedure for tarball installs:**

bash
# 1. Stop the service
systemctl stop <app>

# 2. Backup current install
cp -a /opt/<app> /opt/<app>.bak

# 3. Download and extract new version
cd /opt
curl -fsSL https://github.com/<owner>/<repo>/releases/latest/download/<asset>.tar.gz \
  | tar -xz
ln -sfn /opt/<app>-<newversion> /opt/<app>

# 4. Restart
systemctl start <app>
**Rollback if needed:**

bash
systemctl stop <app>
ln -sfn /opt/<app>.bak /opt/<app>
systemctl start <app>
## Quick Reference

bash
# Full install checklist
mkdir -p /mnt/ssd/<app>/{config,data,cache}
useradd -r -s /usr/sbin/nologin -d /var/lib/<app> <app>
# (install binary)
chown -R <app>:<app> /mnt/ssd/<app>
chown -R <app>:<app> /opt/<app>

# Create override
mkdir -p /etc/systemd/system/<app>.service.d/
cat > /etc/systemd/system/<app>.service.d/override.conf << EOF
[Service]
WorkingDirectory=/mnt/ssd/<app>/config
ExecStart=
ExecStart=/opt/<app>/bin/<binary> --config /mnt/ssd/<app>/config
EOF

# Enable and start
systemctl daemon-reload
systemctl enable --now <app>