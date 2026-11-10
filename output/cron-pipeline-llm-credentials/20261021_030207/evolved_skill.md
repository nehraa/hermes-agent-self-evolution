---
name: cron-pipeline-llm-credentials
description: "Probe auth pool with the script's actual max_tokens."
category: devops
---

# Cron Pipeline — LLM Credential Pool Diagnostics

When a cron-spawned LLM pipeline fails on the **first call** with HTTP 402 / 401 / 429, the root cause is almost always the **credential pool selection logic** combined with **credit headroom vs request budget**. This skill documents the diagnostic recipe and the three canonical fixes.

## When This Skill Applies

- Cron pipeline that worked yesterday, fails today with:
  - `HTTP 402 Payment Required`
  - `HTTP 401 User not found`
  - `HTTP 429 Token Plan usage limit reached`
- Script selects API key via `next(e.get('access_token', '') for e in pool if access_token not in ('***', ''))` (the common "first non-empty wins" pattern)
- Same key works for small probes but fails on real payload

## The Probe Trap

A cheap probe (`max_tokens=5`) returning 200 OK does **NOT** prove the same key can handle the script's real payload. Real OpenRouter failure mode (verified 2026-08-07):

json
{
  "error": {
    "message": "This request requires more credits, or fewer max_tokens. You requested up to 4000 tokens, but can only afford 2625. To increase, visit https://openrouter.ai/settings/credits ..."
  }
}
**What happened:** The key has $0.2625 of credit left.

| Request Type | max_tokens | Estimated Cost | Result |
|-------------|-----------|----------------|--------|
| Tiny probe | 5 | ~$0.0001 | ✓ 200 OK |
| Real request | 4000 | ~$0.0008 | ✗ 402 |

**Root cause:** A different script with `max_tokens=4000` AND larger input exceeded the per-request budget.

> **Rule:** Always probe with the **script's actual `max_tokens`**, not a tiny arbitrary value.

## Diagnostic Recipe

Run this **before** attempting any fixes.

### Step 1: Inspect the Credential Pool

python
#!/usr/bin/env python3
"""Inspect credential pool state — run this first."""

import json
import sys

AUTH_FILE = '/home/Hermes/.hermes/auth.json'

def inspect_pool():
    try:
        auth = json.load(open(AUTH_FILE))
    except FileNotFoundError:
        print(f"ERROR: Auth file not found at {AUTH_FILE}")
        sys.exit(1)

    cp = auth.get('credential_pool', {})

    if not cp:
        print("ERROR: No 'credential_pool' key in auth.json")
        sys.exit(1)

    print(f"\n{'Provider':<20} {'Entries':<8} {'Status'}")
    print("-" * 50)

    for provider, entries in cp.items():
        if not isinstance(entries, list):
            print(f"{provider:<20} INVALID FORMAT (expected list)")
            continue

        print(f"\n{provider} ({len(entries)} entries):")
        for i, e in enumerate(entries):
            t = e.get('access_token', '') if isinstance(e, dict) else ''
            if not t or t in ('***', ''):
                status = 'EMPTY/MASKED'
            else:
                status = f"valid (len={len(t)}, tail=...{t[-4:]})"
            print(f"  [{i}] {status}")

if __name__ == '__main__':
    inspect_pool()
### Step 2: Probe Each Key with Script's Actual Parameters

python
#!/usr/bin/env python3
"""Probe credential pool with the script's actual max_tokens.

Replace SCRIPT_MODEL and SCRIPT_MAX_TOKENS with the values
from the failing script.
"""

import json
import urllib.request
import urllib.error

AUTH_FILE = '/home/Hermes/.hermes/auth.json'

# ← SUBSTITUTE THESE VALUES from the failing script
SCRIPT_MODEL = "anthropic/claude-3-haiku"
SCRIPT_MAX_TOKENS = 4000  # Must match the failing script

def probe_key(access_token: str, model: str, max_tokens: int) -> dict:
    """Send a minimal probe with the script's actual parameters."""
    payload = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": "hi"}],
        "max_tokens": max_tokens
    }).encode('utf-8')

    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        method="POST'
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return {"status": "OK", "code": resp.status}
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='replace')
        try:
            err = json.loads(body)
            msg = err.get('error', {}).get('message', body)
        except json.JSONDecodeError:
            msg = body[:200]
        return {"status": "FAIL", "code": e.code, "message": msg}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

def probe_pool():
    auth = json.load(open(AUTH_FILE))
    cp = auth.get('credential_pool', {})

    print(f"\nProbing with model={SCRIPT_MODEL}, max_tokens={SCRIPT_MAX_TOKENS}")
    print("=" * 60)

    for provider, entries in cp.items():
        for i, e in enumerate(entries):
            if not isinstance(e, dict):
                continue

            token = e.get('access_token', '')
            if not token or token in ('***', ''):
                continue

            result = probe_key(token, SCRIPT_MODEL, SCRIPT_MAX_TOKENS)

            if result["status"] == "OK":
                print(f"✓ [{provider}][{i}] {result['code']} — USABLE")
            else:
                code = result.get('code', 'N/A')
                msg = result.get('message', result.get('msg', ''))[:80]
                print(f"✗ [{provider}][{i}] {code} — {msg}")

if __name__ == '__main__':
    probe_pool()
### Step 3: Interpret Results

| Probe Result | HTTP Code | Meaning | Action |
|-------------|-----------|---------|--------|
| `{"id": "...", "choices": [...]}` | 200 | Key is fully functional | Use this key |
| `"requires more credits"` | 402 | Insufficient balance for this request size | See Fix #1 or #2 |
| `"User not found"` | 401 | Invalid/expired key | See Fix #3 |
| `"usage limit reached"` | 429 | Rate limited | Wait and retry, or see Fix #1 |

---

## The Three Canonical Fixes

### Fix #1: Filter by Credit Headroom (Recommended)

Modify pool selection to only consider keys that can afford the request:

python
def select_usable_key(pool_entries: list, required_max_tokens: int) -> str | None:
    """
    Select the first key that can handle the required max_tokens.
    Skips keys that would fail with 402 due to insufficient credits.
    """
    for entry in pool_entries:
        if not isinstance(entry, dict):
            continue

        token = entry.get('access_token', '')
        if not token or token in ('***', ''):
            continue

        # Probe with required size (not a tiny probe)
        result = probe_key(token, SCRIPT_MODEL, required_max_tokens)

        if result["status"] == "OK":
            return token  # Found a usable key

    return None  # No usable key found
### Fix #2: Sort Pool by Credit Priority

Ensure the pool orders keys by credit balance (highest first):

python
def sort_pool_by_credit(cp: dict, model: str, max_tokens: int) -> dict:
    """Reorder each provider's pool by usable credit (descending)."""
    sorted_cp = {}

    for provider, entries in cp.items():
        usable = []
        for entry in entries:
            if not isinstance(entry, dict):
                usable.append((float('inf'), entry))  # Keep invalid at end
                continue

            token = entry.get('access_token', '')
            if not token or token in ('***', ''):
                usable.append((float('inf'), entry))
                continue

            result = probe_key(token, model, max_tokens)
            # Lower score = more credits available
            score = 0 if result["status"] == "OK" else 1
            usable.append((score, entry))

        # Sort: usable keys first (score=0), then failed keys (score=1)
        usable.sort(key=lambda x: x[0])
        sorted_cp[provider] = [e for _, e in usable]

    return sorted_cp
### Fix #3: Mark Expired Keys and Rotate

Track and skip keys that return 401:

python
def mark_expired_keys(auth_file: str, cp: dict) -> dict:
    """Probe all keys, mark failures, save updated auth file."""
    auth = json.load(open(auth_file))
    cp = auth.get('credential_pool', {})

    for provider, entries in cp.items():
        for i, entry in enumerate(entries):
            if not isinstance(entry, dict):
                continue

            token = entry.get('access_token', '')
            if not token or token in ('***', ''):
                continue

            result = probe_key(token, SCRIPT_MODEL, SCRIPT_MAX_TOKENS)

            if result.get('code') in (401, 403):
                print(f"[!] [{provider}][{i}] Marking as expired")
                entry['status'] = 'expired'
                entry['expired_at'] = str(datetime.now())

    # Save updated auth file
    with open(auth_file, 'w') as f:
        json.dump(auth, f, indent=2)

    return cp
---

## Quick Reference

┌─────────────────────────────────────────────────────────────┐
│ BEFORE RUNNING CRON PIPELINE                                │
│                                                             │
│ 1. Run inspect_pool.py  → Know what's in the pool          │
│ 2. Run probe_pool.py    → Find which keys actually work    │
│ 3. Apply Fix #1, #2, or #3 based on diagnosis               │
│                                                             │
│ NEVER trust a probe with max_tokens < script's max_tokens  │
└─────────────────────────────────────────────────────────────┘
## Common Mistakes

| Mistake | Why It Fails |
|---------|--------------|
| Probing with `max_tokens=5` | Cheap probe passes, real request 402s |
| Not checking 402 before first real call | First LLM call fails cron job |
| Assuming pool order = credit order | Pool may be FIFO, but credits aren't |
| Reusing a 402'd key | Repeated 402s don't fix credit shortage |