---
name: cron-pipeline-llm-credentials
description: "Probe auth pool with the script's actual max_tokens."
category: devops
---

# Cron Pipeline — LLM Credential Pool Diagnostics

When a cron-spawned LLM pipeline fails on the **first call** with HTTP 402 / 401 / 429, the root cause is almost always the **credential pool selection logic** combined with **credit headroom vs. request budget**. This skill documents the diagnostic recipe and the three canonical fixes.

## When This Skill Applies

- Cron pipeline that worked yesterday, fails today with `HTTP 402 Payment Required`, `HTTP 401 User not found`, or `HTTP 429 Token Plan usage limit reached`
- Script picks API key via the common "first non-empty wins" pattern: `next(e.get('access_token','') for e in pool if access_token not in ('***',''))`
- Same key works for tiny probes but fails on real payload

## The Probe Trap

A cheap probe with `max_tokens=5` returning 200 OK does **NOT** prove the same key can handle the script's real payload. Real failure mode (verified 2026-08-07):

json
{
  "error": {
    "message": "This request requires more credits, or fewer max_tokens. You requested up to 4000 tokens, but can only afford 2625. To increase, visit https://openrouter.ai/settings/credits..."
  }
}
**What happened:** The key has $0.2625 of credit left. A probe costs ~$0.0001 and succeeds. The real request with `max_tokens=4000` can cost up to ~$0.0008 — that still fits. But a different script with `max_tokens=4000` **and larger input** may exceed the per-request budget and trigger 402.

**Rule:** Always probe with the script's actual `max_tokens`, not a probe-friendly value.

## Diagnostic Recipe

Run this **before** attempting any fixes.

python
import json
import urllib.request
import urllib.error

# Load auth configuration
with open('/home/Hermes/.hermes/auth.json') as f:
    auth = json.load(f)

cp = auth.get('credential_pool', {})

# ============================================================
# STEP 1: Inspect pool state
# ============================================================
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

# ============================================================
# STEP 2: Probe each non-empty key with script's actual payload
# ============================================================
# Customize these to match your failing script
SCRIPT_MODEL = "anthropic/claude-3-haiku"
SCRIPT_MAX_TOKENS = 4000  # ← MUST match the failing script

print("\n" + "=" * 60)
print("PROBING CREDENTIALS")
print(f"Model: {SCRIPT_MODEL}")
print(f"max_tokens: {SCRIPT_MAX_TOKENS}")
print("=" * 60)

results = []

for provider, entries in cp.items():
    for i, e in enumerate(entries):
        token = e.get('access_token', '')
        if not token or token in ('***', ''):
            continue

        payload = json.dumps({
            "model": SCRIPT_MODEL,
            "messages": [{"role": "user", "content": "test"}],
            "max_tokens": SCRIPT_MAX_TOKENS
        }).encode()

        req = urllib.request.Request(
            "https://openrouter.ai/api/v1/chat/completions",
            data=payload,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                status = resp.status
                body = json.loads(resp.read())
                print(f"  [{provider}][{i}] ✅ {status} — Key viable")
                results.append((provider, i, True, status, None))
        except urllib.error.HTTPError as ex:
            body = json.loads(ex.read()) if ex.fp else {}
            error_msg = body.get('error', {}).get('message', str(ex))
            print(f"  [{provider}][{i}] ❌ HTTP {ex.code} — {error_msg}")
            results.append((provider, i, False, ex.code, error_msg))
        except Exception as ex:
            print(f"  [{provider}][{i}] ❌ ERROR — {ex}")
            results.append((provider, i, False, None, str(ex)))

# ============================================================
# STEP 3: Summary
# ============================================================
print("\n" + "=" * 60)
print("DIAGNOSTIC SUMMARY")
print("=" * 60)
viable = [r for r in results if r[2]]
failed = [r for r in results if not r[2]]

print(f"\nViable keys: {len(viable)}")
for provider, idx, _, status, _ in viable:
    print(f"  - [{provider}][{idx}] → HTTP {status}")

print(f"\nFailed keys: {len(failed)}")
for provider, idx, _, status, error in failed:
    reason = error[:80] + "..." if error and len(error) > 80 else error
    print(f"  - [{provider}][{idx}] → HTTP {status}: {reason}")
## The Three Canonical Fixes

### Fix 1: Use Round-Robin Selection Instead of "First Non-Empty"

The "first non-empty wins" pattern always picks the same key until it fails.

python
import itertools
import json

class CredentialPool:
    def __init__(self, pool_data):
        self._pool = pool_data
        self._cycler = itertools.cycle()

    def get_viable_key(self, model, max_tokens):
        """Iterate through pool until a key that can handle the request is found."""
        # Build flat list of all non-empty tokens
        all_tokens = [
            (provider, idx, entry['access_token'])
            for provider, entries in self._pool.items()
            for idx, entry in enumerate(entries)
            if entry.get('access_token', '') not in ('***', '')
        ]

        # Cycle through them fairly
        for provider, idx, token in itertools.cycle(all_tokens):
            if self._probe_token(token, model, max_tokens):
                return token
            # Token failed; will try next on next call

    def _probe_token(self, token, model, max_tokens):
        # ... probe logic from diagnostic recipe ...
        pass
### Fix 2: Add Per-Key Credit Budget Tracking

Track remaining credit per key and skip keys that cannot afford the request.

python
# In your auth.json, optionally annotate each key:
{
  "credential_pool": {
    "openrouter": [
      {
        "access_token": "sk-...",
        "estimated_credit_usd": 0.26,
        "last_probed": "2026-08-07T10:30:00Z"
      }
    ]
  }
}

def can_afford_request(entry, max_tokens, rate_per_token=0.0000002):
    """Check if key has sufficient estimated credit."""
    credit = entry.get('estimated_credit_usd', 0)
    cost_estimate = max_tokens * rate_per_token
    return credit >= cost_estimate

def select_key(pool, model, max_tokens):
    for provider, entries in pool.items():
        for entry in entries:
            if (entry.get('access_token', '') in ('***', '') or
                not can_afford_request(entry, max_tokens)):
                continue
            if probe_succeeds(entry['access_token'], model, max_tokens):
                return entry['access_token']
    raise RuntimeError("No viable credentials in pool")
### Fix 3: Retry with Reduced max_tokens on 402

If a key fails with 402, retry with a lower `max_tokens` to find the actual budget.

python
def call_with_fallback(token, model, original_max_tokens, messages):
    """Attempt request, retry with reduced tokens on 402."""
    for attempt, mt in enumerate(_reduce_max_tokens(original_max_tokens)):
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": mt
        }
        # ... make request ...
        if response.status == 200:
            return response
        if response.status != 402:
            raise RuntimeError(f"Unexpected error: {response.status}")

    raise RuntimeError(f"All token reductions failed for {model}")

def _reduce_max_tokens(original):
    """Yield decreasing max_tokens values."""
    yield original
    for reduction in [0.75, 0.5, 0.25, 64]:
        yield int(original * reduction) if reduction < 1 else int(reduction)
## Quick Troubleshooting Checklist

- [ ] **Verify cron environment**: Does cron have access to `/home/Hermes/.hermes/auth.json`?
- [ ] **Check key format**: No trailing whitespace, correct prefix (`sk-` vs `Bearer `)
- [ ] **Probe with real `max_tokens`**: Not a synthetic probe value
- [ ] **Inspect pool size**: Is the expected key even present?
- [ ] **Check `last_probed` timestamps**: Keys may be stale
- [ ] **Test outside cron**: Run the diagnostic script manually to isolate cron environment issues

## Related Commands

bash
# Quick pool inspection
python3 -c "
import json; cp=json.load(open('/home/Hermes/.hermes/auth.json'))['credential_pool']
for p,e in cp.items(): print(f'{p}: {len(e)} keys')
"

# Test specific key viability
curl -s -X POST https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"anthropic/claude-3-haiku","messages":[{"role":"user","content":"hi"}],"max_tokens":4000}'