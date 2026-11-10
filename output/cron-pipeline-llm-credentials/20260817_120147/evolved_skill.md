---
name: cron-pipeline-llm-credentials
description: "Probe auth pool with the script's actual max_tokens."
category: devops
---

# Cron Pipeline — LLM Credential Pool Diagnostics

When a cron-spawned LLM pipeline fails on the **FIRST call** with `HTTP 402`, `401`, or `429`, the root cause is almost always **credential pool selection logic** combined with **credit headroom vs. request budget mismatch**. This skill provides the diagnostic recipe and three canonical fixes.

## When This Skill Applies

- Cron pipeline that worked yesterday, fails today with:
  - `HTTP 402 Payment Required`
  - `HTTP 401 User not found`
  - `HTTP 429 Token Plan usage limit reached`
- Script selects API keys via a "first non-empty wins" pattern:
  ```python
  next(e.get('access_token', '') for e in pool if access_token not in ('***', ''))
  ```
- A tiny probe (`max_tokens=5`) succeeds, but the real payload fails

## The Probe Trap

A cheap probe with `max_tokens=5` returning `200 OK` does **NOT** prove the key can handle your script's real payload.

**Real failure mode (verified 2026-08-07):**

json
{
  "error": {
    "message": "This request requires more credits, or fewer max_tokens. You requested up to 4000 tokens, but can only afford 2625. To increase, visit https://openrouter.ai/settings/credits..."
  }
}
**What happened:** The key has $0.2625 of credit. The probe (~$0.0001) succeeds. A request with `max_tokens=4000` costs up to ~$0.0008 — still fits. But a different script with `max_tokens=4000` **and** larger input exceeds the per-request budget → HTTP 402.

**Rule:** Always probe with the **script's actual `max_tokens`**, not a probe-friendly value.

## Diagnostic Recipe

Run this **before** attempting any fixes.

python
import json
import urllib.request
import urllib.error

# Load credentials
auth = json.load(open('/home/Hermes/.hermes/auth.json'))
cp = auth.get('credential_pool', {})

# === 1. Inspect pool state ===
print("\n=== Credential Pool State ===")
for provider, entries in cp.items():
    print(f"\n{provider}: {len(entries)} entries")
    for i, e in enumerate(entries):
        t = e.get('access_token', '')
        if not t or t in ('***', ''):
            marker = 'EMPTY/MASKED'
        else:
            marker = f'len={len(t)} tail=...{t[-4:]}'
        print(f"  [{i}] {marker}")

# === 2. Probe each key with YOUR script's actual parameters ===
# Adjust these to match your failing script
SCRIPT_MODEL = "anthropic/claude-3-haiku"
SCRIPT_MAX_TOKENS = 4000  # ← MUST match the failing script
SCRIPT_PROMPT = "What is 2+2? Answer briefly."  # Or use real input sample

for provider, entries in cp.items():
    for i, e in enumerate(entries):
        t = e.get('access_token', '')
        if not t or t in ('***', ''):
            continue

        print(f"\n--- Probing [{provider}][{i}] with max_tokens={SCRIPT_MAX_TOKENS} ---")

        payload = json.dumps({
            "model": SCRIPT_MODEL,
            "messages": [{"role": "user", "content": SCRIPT_PROMPT}],
            "max_tokens": SCRIPT_MAX_TOKENS
        }).encode()

        req = urllib.request.Request(
            "https://openrouter.ai/api/v1/chat/completions",
            data=payload,
            headers={
                "Authorization": f"Bearer {t}",
                "Content-Type": "application/json"
            },
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read())
                print(f"  ✓ SUCCESS: {result.get('usage', {})}")
        except urllib.error.HTTPError as ex:
            body = json.loads(ex.read())
            print(f"  ✗ FAILED: {ex.code} - {body}")
        except Exception as ex:
            print(f"  ✗ ERROR: {ex}")
**Expected output pattern when you find the bad key:**

--- Probing [openrouter][0] with max_tokens=4000 ---
  ✗ FAILED: 402 - {'error': {'message': 'This request requires more credits...'}}
## The Three Canonical Fixes

### Fix 1: Round-Robin Selection (Preferred for Equal-Use Teams)

Replace "first non-empty wins" with rotating through available keys:

python
import itertools
import json

# Load pool
auth = json.load(open('/home/Hermes/.hermes/auth.json'))
pool = auth.get('credential_pool', {}).get('openrouter', [])

# Filter to valid keys
valid_keys = [e['access_token'] for e in pool if e.get('access_token') not in ('***', '')]

# Round-robin across pipeline runs
def get_next_key():
    return next(itertools.cycle(valid_keys))

# Usage in your LLM call:
# api_key = get_next_key()
### Fix 2: Pre-flight Check Per-Request (Safest for Variable Workloads)

Before each LLM call, probe with the actual `max_tokens` budget:

python
def get_usable_key(model: str, required_max_tokens: int) -> str | None:
    """Return first key that can satisfy the request, or None."""
    pool = json.load(open('/home/Hermes/.hermes/auth.json'))
                      .get('credential_pool', {}).get('openrouter', [])

    for entry in pool:
        token = entry.get('access_token', '')
        if not token or token in ('***', ''):
            continue

        if probe_key(token, model, required_max_tokens):
            return token

    return None  # No usable key found

def probe_key(token: str, model: str, max_tokens: int) -> bool:
    """Return True if key can handle the request."""
    # Use actual prompt or a representative sample
    payload = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": "ping"}],
        "max_tokens": max_tokens
    }).encode()

    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=payload,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="POST"
    )
    try:
        urllib.request.urlopen(req, timeout=10)
        return True
    except urllib.error.HTTPError as e:
        return e.code in (200, 201)  # Only these are "usable"
    except Exception:
        return False
### Fix 3: Budget-Aware Selection (Best for Cost Control)

Track credit estimates and select based on available headroom:

python
def select_key_by_budget(pool_entries: list, required_max_tokens: int, model: str) -> str | None:
    """
    Select the best key based on known credit estimates.
    Requires `credit_estimate` field in pool entries, e.g.:
      {"access_token": "sk-...", "credit_estimate": 0.50}
    """
    MIN_CREDIT_BUFFER = 0.01  # Keep $0.01 reserve

    for entry in pool_entries:
        token = entry.get('access_token', '')
        estimate = entry.get('credit_estimate', 999.0)

        if not token or token in ('***', ''):
            continue

        # Rough cost: max_tokens * $0.00000025 per token (adjust per model)
        estimated_cost = required_max_tokens * 0.00000025

        if estimate - estimated_cost >= MIN_CREDIT_BUFFER:
            return token

    return None
## Quick Reference: HTTP Error Codes

| Code | Meaning | Typical Fix |
|------|---------|-------------|
| `401` | Invalid/missing API key | Check for `***` masking or expired key |
| `402` | Insufficient credits for request | Key lacks budget for `max_tokens` |
| `429` | Rate limit or plan limit | Add delay, use different key, or wait |

## Prevention Checklist

- [ ] Replace "first non-empty wins" with round-robin or budget-aware selection
- [ ] Add pre-flight probe with script's actual `max_tokens` (not a test value)
- [ ] Monitor key credit levels and rotate before exhaustion
- [ ] Log which key was selected for each pipeline run
- [ ] Set alerts on `HTTP 402` spikes