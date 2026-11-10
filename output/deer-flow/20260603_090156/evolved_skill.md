---
name: deer-flow
description: DeerFlow SuperAgent harness — ByteDance open-source deep research framework. Orchestrates sub-agents, memory, sandboxes, and extensible skills for long-horizon research and coding tasks. Backend on port 8001, frontend on port 2026.
category: agent-harnesses
---

# DeerFlow

ByteDance open-source SuperAgent harness (68k GitHub stars) for orchestrating sub-agents, memory, sandboxes, and extensible skills in long-horizon research and coding tasks.

## Prerequisites

- **No Docker available** — starts backend and frontend directly
- **Ports**: Backend (8001), Frontend (2026)
- **API key**: MiniMax `sk-cp-` format required (see Configuration below)

## Setup

### 1. Clone and Configure

bash
git clone https://github.com/bytedance/deer-flow.git ~/deer-flow
cd ~/deer-flow
make config   # generates config.yaml from examples
### 2. Configure Model — MiniMax M2.7

The `ntn_` key format fails with 1004 auth error. **Only `sk-cp-` keys work** for `api.minimax.io/v1/chat/completions`.

Set in `~/deer-flow/.env`:

env
MINIMAX_API_KEY=sk-cp-KjobHFSNe1A5LaEtTY0qrBV5l85bitrDDWkjO4VEtsGd6h8uTnRmbcuEQflj1FXbUwFX2L9S1Qt5_M-dqpFnX7qMGg7GUtGTfYp5EJJ05MVyuLN7N5WWoyA
Model config in `config.yaml`:

yaml
models:
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
## Running

**Backend** (port 8001):
bash
cd ~/deer-flow/backend
source .venv/bin/activate
PYTHONPATH=. uv run uvicorn app.gateway.app:app --host 0.0.0.0 --port 8001
**Frontend** (port 2026):
bash
cd ~/deer-flow/frontend
pnpm install  # first time only
pnpm exec next dev -p 2026
## Access Points

| Service | URL |
|---------|-----|
| Frontend | http://127.0.0.1:2026 |
| Backend API | http://127.0.0.1:8001 |
| API Docs (Swagger) | http://127.0.0.1:8001/docs |

## Important Notes

- **Always `cd ~/deer-flow/backend` before starting** — backend commands must run from that directory
- If the MiniMax API returns a 1004 auth error, verify you are using the `sk-cp-` key format, not `ntn_`