---
name: cron-pipeline-llm-credentials
description: "Probe auth pool with the script's actual max_tokens."
category: devops
---

# Cron Pipeline — LLM Credential Pool Diagnostics

When a cron-spawned LLM pipeline fails on the **first call** with `HTTP 402`, `401`, or `429`, the root cause is almost always the **credential pool selection logic** combined with **credit headroom vs. request budget**. This skill documents the diagnostic recipe and the three canonical fixes.

## When This Skill Applies

| Symptom | Likely Cause |
|---------|-------------|
| `HTTP 402 Payment Required` | Key lacks sufficient credits for the request size |
| `HTTP 401 User not found` | Expired or revoked access token |
| `HTTP 429 Token Plan usage limit reached` | Rate limit exceeded on the selected key |

**Precondition:** The script uses a "first non-empty wins" pattern to select a key:

python
# Common pool selection — picks the first non-masked key
selected_key = next(
    e.get('access_token', '') 
    for e in pool 
    if e.get('access_token', '') not in ('***', '')
)
## The Probe Trap

A probe with `max_tokens=5` returning `200 OK` does **NOT** prove the same key can handle your script's real payload.

**Verified failure mode (2026-08-07, OpenRouter):**

json
{
  "error": {
    "message": "This request requires more credits, or fewer max_tokens. "
               "You requested up to 4000 tokens, but can only afford 2625."
  }
}
| Scenario | `max_tokens` | Cost Estimate | Result |
|----------|--------------|---------------|--------|
| Cheap probe | 5 | ~$0.0001 | ✅ 200 OK |
| Real request | 4000 | ~$0.0008 | ✅ 200 OK (fits budget) |
| Larger prompt + 4000 | 4000 | ~$0.0012 | ❌ 402 (exceeds budget) |

**Rule:** Always probe with **your script's actual `max_tokens`** and a **representative input size**.

## Diagnostic Recipe

Run this **before** attempting any fixes.

python
#!/usr/bin/env python3
"""LLM Credential Pool Diagnostic Script"""

import json
import urllib.request
import urllib.error

# === CONFIGURATION ===
# Replace these to match your failing script
SCRIPT_MODEL = "anthropic/claude-3-haiku"
SCRIPT_MAX_TOKENS = 4000
PROBE_PROMPT = "Hello world, this is a diagnostic probe."  # Use typical input size

# === STEP 1: Inspect Pool State ===
auth = json.load(open('/home/Hermes/.hermes/auth.json'))
cp = auth.get('credential_pool', {})

print("=" * 60)
print("CREDENTIAL POOL STATE")
print("=" * 60)

for provider, entries in cp.items():
    print(f"\n{provider}: {len(entries)} entries")
    for i, e in enumerate(entries):
        token = e.get('access_token', '')
        if not token or token in ('***', ''):
            status = 'EMPTY/MASKED'
        else:
            status = f'len={len(token)} tail=...{token[-4:]}'
        print(f"  [{i}] {status}")

# === STEP 2: Probe Each Key with Actual Request Size ===
print("\n" + "=" * 60)
print("PROBING KEYS WITH REAL max_tokens")
print("=" * 60)

def probe_key(url: str, token: str, model: str, max_tokens: int, prompt: str) -> dict:
    """Send a minimal probe and return result."""
    payload = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens
    }).encode()

    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return {"status": resp.status, "body": resp.read().decode()}
    except urllib.error.HTTPError as e:
        return {"status": e.code, "body": e.read().decode()}
    except Exception as ex:
        return {"status": "ERROR", "body": str(ex)}

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

for provider, entries in cp.items():
    for i, e in enumerate(entries):
        token = e.get('access_token', '')
        if not token or token in ('***', ''):
            continue

        print(f"\nProbing [{provider}][{i}] with max_tokens={SCRIPT_MAX_TOKENS}...")
        result = probe_key(OPENROUTER_URL, token, SCRIPT_MODEL, SCRIPT_MAX_TOKENS, PROBE_PROMPT)

        if result["status"] == 200:
            print(f"  ✅ OK — key is viable for this request size")
        else:
            try:
                error_body = json.loads(result["body"])
                msg = error_body.get("error", {}).get("message", result["body"])
            except:
                msg = result["body"]
            print(f"  ❌ {result['status']} — {msg[:120]}")
**Expected output identifies which keys are viable for your script's actual request size.**

## Three Canonical Fixes

After diagnosis, apply the fix that matches your situation:

### Fix 1: Filter by Sufficient Credit Headroom

If keys exist but some lack budget, filter before selecting:

python
def select_key_with_credit(pool, required_tokens, required_credits_usd):
    """Select a key that can afford the request."""
    for e in pool:
        token = e.get('access_token', '')
        if not token or token in ('***', ''):
            continue
        
        # Probe this specific key (already validated above)
        if probe_key(...).get('status') == 200:
            return token
    return None
### Fix 2: Round-Robin Across Viable Keys

Distribute load to avoid exhausting single keys:

python
import itertools

class CredentialRotator:
    def __init__(self, pool):
        # Pre-filter to only viable keys
        self.viable = [e for e in pool if self._is_viable(e)]
        self.cycle = itertools.cycle(self.viable) if self.viable else iter([])

    def get_next(self):
        return next(self.cycle)

    def _is_viable(self, entry):
        token = entry.get('access_token', '')
        if not token or token in ('***', ''):
            return False
        # Quick viability check with script's actual params
        result = probe_key(token, SCRIPT_MAX_TOKENS, MINIMAL_PROMPT)
        return result.get('status') == 200
### Fix 3: Fallback Chain with Shrinking max_tokens

If credit is low, gracefully degrade:

python
def request_with_fallback(token, model, prompt, token_budgets):
    """Try progressively smaller token limits until one succeeds."""
    for max_tokens in sorted(token_budgets, reverse=True):
        result = probe_key(token, model, max_tokens, prompt)
        if result.get('status') == 200:
            return {"max_tokens": max_tokens, "result": result}
    
    # All failed — raise with details
    raise RuntimeError(f"No viable token budget for this key. Tried: {token_budgets}")
## Quick Reference

| Problem | Check | Fix |
|---------|-------|-----|
| 402 on first call | Probe with actual `max_tokens` | Filter by credit headroom |
| Key works for probe, fails for real | Input size difference | Use representative probe |
| Sporadic 429s | All keys using same provider | Round-robin across providers |
| 401 after days of success | Token expired | Implement expiration check |

## Verification Checklist

- [ ] Diagnostic script run against actual pool
- [ ] Probe used `max_tokens` matching the failing script
- [ ] Probe input size representative of real workload
- [ ] Fix applied (filter / round-robin / fallback) matches diagnosis
- [ ] Re-run diagnostic confirming fix works
- [ ] Monitor for 24h before marking resolved