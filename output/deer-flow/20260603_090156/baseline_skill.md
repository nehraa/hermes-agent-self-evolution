---
name: deer-flow
description: DeerFlow SuperAgent harness — ByteDance open-source deep research framework. Orchestrates sub-agents, memory, sandboxes, and extensible skills for long-horizon research and coding tasks. Backend on port 8001, frontend on port 2026.
category: agent-harnesses
---

# DeerFlow

ByteDance open-source SuperAgent harness (68k GitHub stars). Orchestrates sub-agents, memory, sandboxes, and extensible skills for long-horizon research and coding tasks.

## Setup (Complete Checklist)

### 1. Clone
```bash
git clone https://github.com/bytedance/deer-flow.git ~/deer-flow
cd ~/deer-flow
make config   # generates config.yaml from examples
```

### 2. Configure Model — MiniMax M2.7 (CORRECT KEY — May 2026)

Edit `~/deer-flow/.env` with the **working `sk-cp-` key** (NOT the `ntn_` key — that one returns 1004 auth error):

```yaml
models:
  # MiniMax M2.7 — international endpoint
  - name: minimax-m2.7
    display_name: MiniMax M2.7
    use: langchain_openai:ChatOpenAI
    model: MiniMax-M2.7
    api_key: $MINIMAX_API_KEY
    base_url: https://api.minimax.io/v1
    request_timeout: 600.0
    max_retries: 2
    max_tokens: 4096
    temperature: 1.0
    supports_vision: true
    supports_thinking: true
```

Edit `~/deer-flow/.env` — set the **working `sk-cp-` key**:
```env
MINIMAX_API_KEY=sk-cp-KjobHFSNe1A5LaEtTY0qrBV5l85bitrDDWkjO4VEtsGd6h8uTnRmbcuEQflj1FXbUwFX2L9S1Qt5_M-dqpFnX7qMGg7GUtGTfYp5EJJ05MVyuLN7N5WWoyA
```
⚠️ The `ntn_` key format fails with 1004 auth error. Only `sk-cp-` works for `api.minimax.io/v1/chat/completions`.

### 3. Install nginx

**sudo TTY rule**: `echo "pass" | sudo -S command` fails with "a password is required" when sudo needs a TTY. The `sudo -S` flag reads from stdin but the password prompt still needs an interactive TTY. Abhinav must run this himself:

```bash
sudo apt install -y nginx
```

### 4. Start — Docker-free (no Docker available)

Docker not available on this server. Start backend and frontend separately:

**Backend (uvicorn on port 8001):**
```bash
cd ~/deer-flow/backend
source .venv/bin/activate
PYTHONPATH=. uv run uvicorn app.gateway.app:app --host 0.0.0.0 --port 8001
```

**Frontend (Next.js on port 2026):**
```bash
cd ~/deer-flow/frontend
pnpm install  # first time only
pnpm exec next dev -p 2026
```

**Access:**
- Frontend: http://127.0.0.1:2026
- Backend API: http://127.0.0.1:8001
- Backend docs: http://127.0.0.1:8001/docs (Swagger UI)

**Critical path rules:**
- Always `cd` to `backend/` before starting uvicorn — `PYTHONPATH=.` only works from that directory
- Frontend requires `pnpm install` before first run (dependencies not in repo)
- Next.js binary must be called via `pnpm exec` (not directly — it's in `.pnpm` store)
- `make dev` (Docker-based) does NOT work — use manual startup above

- Gateway → `localhost:8001`
- Frontend → `localhost:3000`
- Nginx reverse proxy → `localhost:2026` (main entry point)

## Architecture

- **Gateway**: uvicorn on port 8001 — REST API + agent runtime
- **Frontend**: Next.js on port 2026 (Docker-free mode) or port 3000 (Docker mode)
- **Nginx**: reverse proxy on port 2026, routes `/api/langgraph/*` to gateway, `/api/*` to REST API
- **Sandbox**: Docker container (`deer-flow-sandbox`) for code execution (Docker mode only)

## Troubleshooting

## serve.sh Key Details

- Runs `nginx` with config at `$REPO_ROOT/docker/nginx/nginx.local.conf`
- Waits for ports with `scripts/wait-for-port.sh`
- Kills existing services on restart via `pkill` and `_kill_port`
- **No `sudo` inside serve.sh** — nginx must already be installed system-wide before `make dev`

## Initial Setup — Auth Reset (always needed on fresh install)

DeerFlow requires account creation via web UI. If the UI shows "Email already registered" or auth is broken:

### Step 1: Reset via CLI
```bash
cd /home/Hermes/deer-flow/backend && source .venv/bin/activate && PYTHONPATH=. python -m app.gateway.auth.reset_admin --email abhinav@devstudios.me
```
This writes a temp password to `.deer-flow/admin_initial_credentials.txt`.

### Step 2: Read the temp password
```bash
cat /home/Hermes/deer-flow/backend/.deer-flow/admin_initial_credentials.txt
```
Output format:
```
email: abhinav@devstudios.me
password: mqR3pN2nl2i-PvtAepjunA
```

### Step 3: Web UI setup
1. Navigate to http://localhost:2026 → Sign In → "Don't have an account? Sign up"
2. Enter email + temp password → Sign In
3. On first login, DeerFlow shows a "Complete Setup" form: enter email + current temp password + new password (twice) → "Complete Setup"
4. After setup, DeerFlow redirects to the workspace

**Critical:** The temp password from `reset_admin` is only valid for ONE login. The "Complete Setup" flow consumes it. If setup fails (wrong password, network issue), re-run `reset_admin` to get a fresh temp password.

**Testing that DeerFlow is working** — VERIFIED May 17, 2026:
Navigate to http://localhost:2026/workspace. Click "New chat". Type a query like "What is the current geopolitical situation in Myanmar? Give me a 3 sentence summary." Click Submit. DeerFlow will show live research progress (searching, browsing, generating) then return the final response.

**Status as of May 17, 2026:**
- Backend on port 8001: healthy ✅
- Frontend on port 2026: HTTP 200 ✅
- Auth: reset_admin flow → temp password → web UI "Complete Setup" → workspace ✅
- Full research query tested successfully ✅

## Docker-Free Startup (this server — May 2026)

Docker is not available on this server. Manual startup required:

**Backend (must cd to backend/ first):**
```bash
cd /home/Hermes/deer-flow/backend
source .venv/bin/activate
PYTHONPATH=. uv run uvicorn app.gateway.app:app --host 0.0.0.0 --port 8001
```

**Frontend (install deps first, use pnpm exec for next):**
```bash
cd /home/Hermes/deer-flow/frontend
pnpm install  # first time only
pnpm exec next dev -p 2026
```

**Daemon process tree:**
- `open-design tools-dev` — Open Design daemon + web (random ports from log)
- `Vane next dev` — Vane chat (port 3001 currently)
- `uvicorn deer-flow` — DeerFlow backend (port 8001)
- `next dev deer-flow` — DeerFlow frontend (port 2026)
- `whatsapp-bridge` — WhatsApp gateway (port 3000)

## Troubleshooting

**nginx not found / won't start**: Run `sudo apt install -y nginx` manually first.

**Gateway fails on 8001**: Check `logs/gateway.log`

**Frontend fails on 3000**: Check `logs/frontend.log`

**Model not found / LLM request fails with error 1004**: 
- Verify `MINIMAX_API_KEY` in `.env` uses `sk-cp-` prefix (NOT `ntn_` — the `ntn_` key returns 1004 auth error on this endpoint)
- Restart backend after updating `.env`

**Model not found / LLM request fails with error 1004**:
- Verify `MINIMAX_API_KEY` in `.env` uses `sk-cp-` prefix (NOT `ntn_` — the `ntn_` key returns 1004 on `api.minimax.io/v1/chat/completions`)
- The `sk-cp-` key works on `api.minimax.io/v1/chat/completions`
- The `ntn_` key works on `api.minimax.chat/v1/text/chatcompletion_v2` (different endpoint)
- Restart backend after updating `.env`

**"login fail: Please carry the API secret key" (error 1004)**:
- This is a key/endpoint mismatch. `sk-cp-` keys fail on `api.minimax.chat`, `ntn_` keys fail on `api.minimax.io`
- Fix: ensure the key format matches the endpoint in config.yaml
- The working combination (May 2026): `sk-cp-` key + `https://api.minimax.io/v1`

**401 Unauthorized on protected endpoints**:
- DeerFlow requires CSRF token on protected API calls. Login via browser UI (not curl) to get proper session cookies.
- Use the `reset_admin` flow for first-time setup: temp password → web UI → "Complete Setup" form.
- CSRF is handled automatically when using the browser UI.

**"Email already registered" during signup**:
- User already exists. Run `reset_admin` to get a fresh temp password, then sign in with it.

## Key Files

- `config.yaml` — main config (models, tools, tool_groups)
- `.env` — API keys and secrets
- `scripts/serve.sh` — service launcher (dev/prod/daemon modes)
- `scripts/deerflow_test.py` — health check + API test (run this to verify full stack)
- `docker/nginx/nginx.local.conf` — nginx reverse proxy config
- `references/minimax-api-auth-debugging.md` — key formats, auth flow, password reset
- `references/docker-free-startup.md` — manual startup sequence (no Docker)
- `references/docker-free-startup.md` — also contains auth reset flow (reset_admin CLI + temp password → web setup)
- `templates/minimax-m27-config.yaml` — copy-paste model block for MiniMax M2.7