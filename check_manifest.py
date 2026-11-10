import json
import os

with open('evolution_manifest.json') as f:
    m = json.load(f)

skills = m['skills']
print('Skills type:', type(skills))
print('Skills count:', len(skills))

# Get first few items
items = list(skills.items())[:2]
for k, v in items:
    print(f'Key: {k}, Value type: {type(v)}')
    if isinstance(v, dict):
        print(f'  Keys: {list(v.keys())}')

# Find failed
failed = {k: v for k, v in skills.items() if isinstance(v, dict) and v.get('status') == 'failed'}
print(f'FAILED_COUNT={len(failed)}')
if failed:
    for name, info in failed.items():
        print(f'FAILED_SKILL: {name} — {info.get("last_error_type")}: {str(info.get("last_error", ""))[:100]}')

print(f'Current round: {m.get("round")}')
print(f'Next index: {m.get("next_index")}')
print(f'Order length: {len(m.get("order", []))}')
