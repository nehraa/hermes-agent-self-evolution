---
name: cron-pipeline-llm-credentials
description: "Probe auth pool with the script's actual max_tokens."
category: devops
---

# Cron Pipeline — LLM Credential Pool Diagnostics

When a cron-spawned LLM pipeline fails on the **first call** with `HTTP 402`, `401`, or `429`, the root cause is almost always the **credential pool selection logic** combined with **credit headroom vs. request budget**. This skill documents the diagnostic recipe and the three canonical fixes.

## When This Skill Applies

- Cron pipeline fails with `HTTP 402 Payment Required`, `HTTP 401 User not found`, or `HTTP 429 Token Plan usage limit reached`
- Script selects API key using a "first non-empty wins" pattern (e.g., `next(e.get('access_token','') for e in pool if access_token not in ('***',''))`)
- A tiny probe with `max_tokens=5` succeeds, but the real payload fails

## The Probe Trap

A cheap probe returning `200 OK` does **NOT** prove the same key can handle your script's actual payload. Real failure mode (verified 2026-08-07):

json
{
  "error": {
    "message": "This request requires more credits, or fewer max_tokens. You requested up to 4000 tokens, but can only afford 2625. To increase, visit https://openrouter.ai/settings/credits ..."
  }
}
**What happened:** The key has $0.2625 of credit. A probe with `max_tokens=5` costs ~$0.0001 — succeeds. Your real request with `max_tokens=4000` may exceed the per-request budget and trigger 402.

**Rule:** Always probe with your script's **actual `max_tokens`**, not a tiny probe-friendly value.

## Diagnostic Recipe

Run this **before** attempting fixes.

python
import json
import urllib.request
import urllib.error

# Load auth config
with open('/home/Hermes/.hermes/auth.json') as f:
    auth = json.load(f)

cp = auth.get('credential_pool', {})

# 1. Show pool state
print("=== CREDENTIAL POOL STATE ===\n")
for provider, entries in cp.items():
    print(f"{provider}: {len(entries)} entries")
    for i, e in enumerate(entries):
        token = e.get('access_token', '')
        if not token or token in ('***', ''):
            status = 'EMPTY/MASKED'
        else:
            status = f"len={len(token)} tail=...{token[-4:]}"
        print(f"  [{i}] {status}")

# 2. Probe each non-empty key with ACTUAL payload size
#    Adjust these to match your failing script
SCRIPT_MODEL = "anthropic/claude-3-haiku"
SCRIPT_MAX_TOKENS = 4000  # ← MUST match the failing script

print("\n=== PROBING WITH REAL max_tokens ===\n")
for provider, entries in cp.items():
    for i, e in enumerate(entries):
        token = e.get('access_token', '')
        if not token or token in ('***', ''):
            continue

        # Probe with real max_tokens
        probe_payload = {
            "model": SCRIPT_MODEL,
            "messages": [{"role": "user", "content": "test"}],
            "max_tokens": SCRIPT_MAX_TOKENS
        }

        req = urllib.request.Request(
            "https://openrouter.ai/api/v1/chat/completions",
            data=json.dumps(probe_payload).encode(),
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read())
                print(f"[{provider}][{i}] ✓ 200 OK - Key viable")
        except urllib.error.HTTPError as ex:
            body = json.loads(ex.read())
            error_msg = body.get('error', {}).get('message', str(body))
            print(f"[{provider}][{i}] ✗ HTTP {ex.code} - {error_msg}")
        except Exception as ex:
            print(f"[{provider}][{i}] ✗ ERROR - {ex}")
## Three Canonical Fixes

### Fix 1: Filter by Credit Headroom (Recommended)

Add a pre-flight check that tests with actual `max_tokens`:

python
def select_viable_key(pool, model, max_tokens):
    """Return first key that can handle the request, or None."""
    test_payload = {
        "model": model,
        "messages": [{"role": "user", "content": "probe"}],
        "max_tokens": max_tokens
    }

    for entry in pool:
        token = entry.get('access_token', '')
        if not token or token in ('***', ''):
            continue

        req = urllib.request.Request(
            "https://openrouter.ai/api/v1/chat/completions",
            data=json.dumps(test_payload).encode(),
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.status == 200:
                    return token
        except urllib.error.HTTPError:
            continue

    return None  # No viable key found
### Fix 2: Reduce max_tokens to Fit Budget

If a key is nearly exhausted, reduce request size to fit within its headroom:

python
def get_max_affordable_tokens(token, model, target_tokens=4000):
    """Binary search for max tokens this key can afford."""
    lo, hi = 1, target_tokens
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if test_request_affordable(token, model, mid):
            lo = mid
        else:
            hi = mid - 1
    return lo

def test_request_affordable(token, model, max_tokens):
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps({
            "model": model,
            "messages": [{"role": "user", "content": "x"}],
            "max_tokens": max_tokens
        }).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=10):
            return True
    except urllib.error.HTTPError as ex:
        return ex.code != 402
### Fix 3: Rotate to Next Key in Pool

When a key fails, automatically try the next one:

python
def call_with_fallback(pool, model, messages, max_tokens):
    """Try each key in order until one succeeds."""
    for entry in pool:
        token = entry.get('access_token', '')
        if not token or token in ('***', ''):
            continue

        try:
            return call_llm(token, model, messages, max_tokens)
        except HTTPError as ex:
            if ex.code in (401, 402, 429):
                continue  # Try next key
            raise  # Re-raise unexpected errors

    raise RuntimeError("All credential keys exhausted")
## Quick Reference

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| `402` on first call | Key lacks credit for `max_tokens` | Fix 1 or Fix 2 |
| `401 User not found` | Key revoked/invalid | Replace key in pool |
| `429` immediately | Rate limit hit | Implement backoff + Fix 3 |
| Probe works, real fails | Probed with wrong `max_tokens` | Always probe with real value |