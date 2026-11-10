---
name: linux-native-service-bringup
description: Install Linux services natively (apt/tarball) with systemd.
category: devops
---

# Native Linux Service Bring-Up on This Server

When you install a service natively (apt or GitHub tarball) instead of
Docker, the bring-up has four phases. Each has a trap.

## Phase 1 — Install

### Apt route
- For Servarr (Radarr/Sonarr/Prowlarr) projects: servarr.com is gone.
  Each project ships its own apt key + repo at its own domain now:
  - Radarr: `radarr.video`
  - Sonarr: `sonarr.tv`
  - Prowlarr: `prowlarr.com`
  - Jellyseerr: `jellyseerr.dev` (Docker-only, no apt)
- Generic pattern:
  ```bash
  curl -fsSL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x<SIG>" \
    | gpg --dearmor --yes -o /etc/apt/keyrings/<name>.gpg
  echo "deb [signed-by=/etc/apt/keyrings/<name>.gpg] https://<domain>/<repo> <suite> main" \
    > /etc/apt/sources.list.d/<name>.list
  apt-get update && apt-get install -y <package>
  ```
- If the upstream signing key is missing from Ubuntu keyserver, look
  for a keyring.gpg file on the project's apt repo domain. servarr's
  pattern was `https://servarr.com/linux/deb/keyring.gpg` — when
  servarr.com went down, every project split.

### Tarball route (most *arr projects post-2026)
- Get latest release metadata: `curl -fsSL
  "https://api.github.com/repos/<owner>/<repo>/releases/latest"`
- Asset name patterns:
  - Old: `<App>.main.<ver>.linux-x64.tar.gz` (Sonarr still uses this)
  - New: `<App>.master.<ver>.linux-core-x64.tar.gz` (Radarr, Prowlarr)
  - Variant: `<App>.master.<ver>.linux-musl-core-x64.tar.gz` (musl libc)
- Extract to `/opt/<App>/`. Create a service user (`useradd -r -s
  /usr/sbin/nologin -d /var/lib/<app> <app>`). chown the install.

## Phase 2 — Systemd unit (override.conf pattern)

Every native install on this server needs an override drop-in that:
1. Redirects data paths to `/mnt/ssd/<app>/`
2. Sets `WorkingDirectory` to a path that EXISTS
3. Inlines multi-word flags into `ExecStart`

The canonical shape (worked example: Jellyfin):

```ini
# /etc/systemd/system/<service>.service.d/override.conf
[Service]
WorkingDirectory=/mnt/ssd/<service>/config
Environment=KEY1=/mnt/ssd/<service>/sub   # single-value paths only
Environment=KEY2=/mnt/ssd/<service>/sub
ExecStart=
ExecStart=/usr/bin/<binary> --flag /path/with/spaces --service   # multi-word inline
```

**Three rules** (memorize these — they prevent 90% of failures):

1. **`WorkingDirectory` MUST exist** before the unit starts, owned
   by the service user. systemd chdirs before exec, so missing dirs
   cause silent `status=200/CHDIR` failures.
2. **`Environment=` for paths/ports/keys ONLY.** For `--flag value`
   pairs, inline them in `ExecStart`. systemd does NOT strip quotes
   from `EnvironmentFile=` values, and unquoted multi-word values
   get parsed as `KEY=first-word-only`.
3. **Override EVERY `-dir` flag the binary takes.** If you only
   override `--datadir` and forget `--logdir`, the binary starts
   then dies trying to create the log file.

Always sequence: write override → `daemon-reload` → `start` (don't
enable yet) → verify port → THEN `enable`. See service-verification
skill's `systemd-unit-pitfalls.md` Pitfall #7.

### Diagnostic gotchas

- `status=200/CHDIR` = missing WorkingDirectory. Check
  `journalctl -u <name>` for which path.
- `status=1/FAILURE` with `unknown flag` = wrong flag prefix
  (single vs double dash). Try `--webdir` instead of `-webdir`.
- App listens on port but 000 on `/` curl = bound to wrong interface
  (loopback vs 0.0.0.0).
- Container can't resolve host = docker daemon needs
  `sudo chmod 666 /var/run/docker.sock` after every daemon start.

## Phase 3 — SSD directory ownership

Native services run as their own user (`jellyfin`, `radarr`, etc.).
`/mnt/ssd` is owned by root, so the service user can't write there.

```bash
sudo mkdir -p /mnt/ssd/<app>/{config,cache,media,downloads}
sudo chown -R <app>:<app> /mnt/ssd/<app>
sudo chmod 755 /mnt/ssd/<app>
```

For Immich/Vaultwarden/etc. that bind-mount a host path into Docker
later, the bind-mount source must be readable by UID 999 or 1000
depending on the container's user.

## Phase 4 — Inter-app wiring (the *arr pattern)

When bringing up the *arr stack (Radarr/Sonarr/Prowlarr/qBittorrent/
Jellyseerr/Jellyfin), the wiring is consistent:

1. **API keys live in each app's `config.xml` first-run file.** The
   key is auto-generated on first start. Get it via:
   ```bash
   grep -oP '(?<=<ApiKey>)[^<]+' /mnt/ssd/<app>/config/config.xml
   ```
2. **Add download clients via `POST /api/v3/downloadclient`.**
   Gotchas:
   - `configContract` MUST be the implementation-specific string
     (e.g. `"QBittorrentSettings"`), NOT the generic
     `"DownloadClientSettings"`.
   - `removeCompletedDownloads` and `removeFailedDownloads` are
     TOP-LEVEL fields, not in `fields[]`.
   - Use `forceSave=true` query param to bypass validation that
     requires testing connections.
   - qBittorrent fields differ by app: Radarr uses `movieCategory`,
     Sonarr uses `tvCategory`.
3. **Add Prowlarr as the indexer sync target** via
   `POST /api/v1/applications` with `syncLevel=fullSync`. Sync
   categories: `[2000,...]` for Radarr, `[5000,...]` for Sonarr.
4. **Password masking on GET:** the password field returns `********`
   (8 chars) on GET even when stored correctly. Don't debug "pw_len
   is 8" — that's the mask, not the value.
5. **Jellyseerr is Docker-only.** No tarball releases, no source
   install. Pull `fallenbagel/jellyseerr:latest`, mount
   `/mnt/ssd/jellyseerr/config`, expose 5055.

## When to use this vs service-verification

- **Use this skill** when installing NEW native services, especially
  ones following the SSD migration + systemd override pattern.
- **Use service-verification** for verifying an EXISTING service's
  health, killing zombies, reading logs, or applying the watchdog
  cron pattern.

## See also

- `references/cardigann-indexer-api.md` — full Cardigann
  `/api/v1/indexer` POST recipe with all field defaults
- `references/jellyfin-ssd-override.md` — complete worked example of
  the override.conf pattern (the one that took 5 tries to get right)
- `service-verification/references/systemd-unit-pitfalls.md` —
  Pitfalls #1-#10 cover the broader systemd/Next.js pitfalls not
  specific to native services
