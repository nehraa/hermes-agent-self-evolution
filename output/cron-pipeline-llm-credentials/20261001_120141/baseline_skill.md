---
name: cron-pipeline-llm-credentials
description: "Probe auth pool with the script's actual max_tokens."
category: devops
---

# Cron Pipeline — LLM Credential Pool Diagnostics

When a cron-spawned LLM pipeline fails on the FIRST call with HTTP 402 / 401 / 429, the root cause is almost always the **credential pool selection logic** combined with **credit headroom vs request budget**. This skill documents the diagnostic recipe and the three canonical fixes.

## When this skill applies

- Cron pipeline that worked yesterday, fails today with `HTTP 402 Payment Required` or `HTTP 401 User not found` or `HTTP 429 Token Plan usage limit reached`
- Script picks API key via `next(e.get('access_token','') for e in pool if access_token not in ('***',''))` (the common "first non-empty wins" pattern)
- Same key works for tiny probes but fails on real payload

## The probe trap

A cheap probe (`max_tokens=5`) returning 200 OK does NOT prove the same key can handle the script's real payload. Real OpenRouter failure mode (verified 2026-08-07):

```json
{"error":{"message":"This request requires more credits, or fewer max_tokens. You requested up to 4000 tokens, but can only afford 2625. To increase, visit https://openrouter.ai/settings/credits ..."}}
```

The key has $0.2625 of credit left. Probe costs ~$0.0001, succeeds. Real request with `max_tokens=4000` can cost up to ~$0.0008 — fits. But a different script with `max_tokens=4000` AND larger input may exceed the per-request budget and 402.

**Always probe with the SCRIPT'S actual `max_tokens`, not a tiny value.**

## Diagnostic recipe (run BEFORE attempting fixes)

```python
import json, urllib.request, urllib.error
auth = json.load(open('/home/Hermes/.hermes/auth.json'))
cp = auth.get('credential_pool', {})

# 1. Show the pool state
for provider, entries in cp.items():
    print(f'\n{provider}: {len(entries)} entries')
    for i, e in enumerate(entries):
        t = e.get('access_token', '')
        marker = 'EMPTY/MASKED' if not t or t in ('***','') else f'len={len(t)} tail=...{t[-4:]}'
        print(f'  [{i}] {marker}')

# 2. Probe each non-empty key with the script's ACTUAL payload size
#    (substitute the script's model + max_tokens)
SCRIPT_MODEL = "anthropic/claude-3-haiku"
SCRIPT_MAX_TOKENS = 4000  # ← match the failing script, not a probe-friendly value

for provider, entries in cp.items():
    for i, e in enumerate(entries):
        t = e.get('access_token', '')
        if not t or t in ('***', ''):
            continue
        payload = json.dumps({"model": SCRIPT_MODEL,
                              "messages": [{"role":"user","content":"hi"}],
                              "max_tokens": SCRIPT_MAX_TOKENS}).encode()
        req = urllib.request.Request(
            f"https://openrouter.ai/api/v1/chat/completions",
            data=payload,
            headers={"Authorization": f"Bearer {t}", "Content-Type":"application/json"},
            method="POST")
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                print(f'{provider}[{i}]: OK ({r.status})')
        except urllib.error.HTTPError as exc:
            body = exc.read().decode()[:120]
            print(f'{provider}[{i}]: HTTP {exc.code} — {body}')
        except Exception as exc:
            print(f'{provider}[{i}]: {type(exc).__name__}: {str(exc)[:80]}')
```

The script's likely-failing key will show `HTTP 402` here even though the user might swear "I just topped it up yesterday." Credits deplete fast on multi-call pipelines.

## Three canonical fixes (least-modification first)

### Fix 1: Lower `max_tokens` in the script (one-line patch)

Many scripts over-budget their `max_tokens`. Real responses are usually much smaller:

- `claude-3-haiku` for 4-slide JSON output → 500–600 tokens actual, 2000 ceiling is safe
- `gpt-4o-mini` for short Q&A → 100-300 tokens actual, 1000 ceiling is safe

```python
# Before:
"max_tokens": 4000,
# After:
"max_tokens": 2000,
```

This brings the call under a $0.20-balance key's budget without touching credentials.

**When to use:** The script is yours to edit AND the actual output is well under the new cap.

### Fix 2: Top up the key at the provider's billing page

- OpenRouter: https://openrouter.ai/settings/credits
- Anthropic: https://console.anthropic.com/settings/billing
- MiniMax: https://platform.minimax.io/subscribe/token-plan

**When to use:** No code change allowed (user said "don't modify it"), and the user's wallet supports it.

### Fix 3: Swap the failing first-pool entry with a working one

The script may be hardcoded to pick the first non-empty token via `next(...)`. If only slot 0 has a key (and slot 0 is failing), the script dies. The fix is a temporary `auth.json` swap:

```bash
# Backup
cp /home/Hermes/.hermes/auth.json /home/Hermes/.hermes/auth.json.bak.$(date +%s)

# Swap (Python is easier than sed for nested JSON)
python3 -c "
import json
p = '/home/Hermes/.hermes/auth.json'
auth = json.load(open(p))
or_list = auth['credential_pool']['openrouter']
first = next((e['access_token'] for e in or_list if e.get('access_token','') not in ('','***')), None)
working = 'sk-or-v1-WORKING_KEY_HERE'  # from probe above
for e in or_list:
    if e['access_token'] == first:
        e['access_token'] = working
json.dump(auth, open(p,'w'), indent=2)
print(f'swapped {first[-4:]} -> {working[-4:]}')
"

# Run the pipeline
python3 /home/Hermes/protocol-papers/scripts/protocol_daily_remotion.py

# ALWAYS restore — even on failure
cp /home/Hermes/.hermes/auth.json.bak.* /home/Hermes/.hermes/auth.json
rm /home/Hermes/.hermes/auth.json.bak.*
```

**Critical:** Restore `auth.json` from backup before reporting back. A missed restore corrupts the next cron run silently.

## When the script is locked (user said "don't modify")

Prefer fix 2 (top up) or fix 3 (swap+restore). If neither is acceptable, the only remaining option is to abort the cron and report the failure honestly:

```
Topic: <protocol>
Output: <empty directory path>
Telegram: NOT SENT (HTTP 402 on script's first LLM call)
Fix: Top up openrouter.ai/settings/credits OR patch max_tokens to 2000 in the script.
```

No fake "success" report. No fabricated video path. The file is on disk only when the script got far enough to write one.

## Reference cases

- **2026-08-07 protocol_daily_remotion.py** — `max_tokens=4000` on `anthropic/claude-3-haiku` via openrouter.ai 402'd because first key had $0.2625 credit. Five of nine pool entries were healthy. Fix: lower max_tokens to 2000 (or top up first key).
- **2026-07-19 OpenMAIC** — `MINIMAX_API_KEY=*** ` was old format `ntn_…` key that 401'd. New `sk-cp-…` key in `~/.hermes/.env` worked. Diagnostic: probe with the actual model before assuming key state.
- **2026-08-05 newspaper-pipeline** — OpenRouter Token Plan hit 2056 rate limit. Lesson: don't cascade to OpenRouter as MiniMax fallback (see `cron-pipeline-minimax-provider`).

## See also

- `cron-pipeline-minimax-provider` — the user-mandated rule that cron pipelines use MiniMax, not OpenRouter. If your pipeline is on OpenRouter, this is the second-order reason it failed.
- `devops/cron-video-delivery-telegram` — the existing skill that already documents the auth-pool probe pattern. The skill here extends that with the credit-headroom vs max_tokens insight specifically.
- `devops/service-verification` — the broader "verify before restart" methodology.
- `hermes-content-filter-quirks` — when API keys get rewritten to `***` and your pool appears empty.
