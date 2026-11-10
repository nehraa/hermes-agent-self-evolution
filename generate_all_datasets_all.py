#!/usr/bin/env python3
"""Generate evaluation datasets for ALL Hermes skills — runs in background."""
import json, os, sys, time
from pathlib import Path

# Load MINIMAX_API_KEY from hermes .env
hermes_env = Path.home() / '.hermes' / '.env'
if hermes_env.exists():
    with open(hermes_env) as f:
        for line in f:
            stripped = line.strip()
            key_start = stripped.startswith('MINIMAX_API_KEY=')
            is_comment = stripped.startswith('#')
            if key_start and not is_comment:
                os.environ['MINIMAX_API_KEY'] = stripped.split('=', 1)[1]
                break

sys.path.insert(0, '/home/Hermes/repos/gepa')
os.environ['LITELLM_API_BASE'] = 'https://api.minimax.io/v1'
from evolution.core.config import EvolutionConfig
from evolution.core.dataset_builder import SyntheticDatasetBuilder

config = EvolutionConfig(iterations=3)
config.judge_model = 'minimax/MiniMax-M2.7'
config.eval_model = 'minimax/MiniMax-M2.7'

skills_dir = Path('/home/Hermes/.hermes/skills')
skip_categories = {
    'agent', 'api', 'apple', 'convert_skill.py', 'dataset-metadata.json', 
    'feeds', 'inference-sh', 'diagramming', 'gifs', 'paperbanana',
    'pexoai-agent', 'pexoai-agent_temp', 'sulada-knowledge-base', 'tianshu-wan-video',
    'domain', 'elite-longterm-memory', 'last30days-skill', 'neural-memory',
    'operating-principles', 'personal', 'playbooks', 'self-improving-agent',
    'system-architect', 'cto', 'security-auditor', 'senior-architect', 
    'senior-security', 'test-master', 'use-tools', 'vision', 'x-research',
    'yuanbao', 'adhd-body-doubling', 'afrexai-qa-testing-engine', 
    'afrexai-qa-test-plan', 'deer-flow', 'dogfood', 'memory-setup',
    'memory-setup-openclaw', 'proactive-agent-lite', 'red-teaming',
    'monitor-intelligence-services',
}

skills = []
for cat in skills_dir.iterdir():
    if not cat.is_dir() or cat.name in skip_categories:
        continue
    for skill_path in cat.glob('*/SKILL.md'):
        if skill_path.stat().st_size > 1000:
            skills.append((skill_path.parent.name, str(skill_path)))

print(f'Found {len(skills)} skills to process')

results = {'ok': [], 'error': []}
for i, (skill_name, skill_path) in enumerate(skills):
    dataset_dir = Path('/home/Hermes/repos/gepa/datasets/skills') / skill_name
    if (dataset_dir / 'train.jsonl').exists():
        print(f'[{i+1}/{len(skills)}] {skill_name} — already has dataset, skipping')
        results['ok'].append(skill_name)
        continue
    
    print(f'[{i+1}/{len(skills)}] {skill_name}...')
    try:
        raw = Path(skill_path).read_text()
        body = raw.split('---', 2)[2].strip() if len(raw.split('---', 2)) >= 3 else raw
        
        builder = SyntheticDatasetBuilder(config)
        dataset = builder.generate(artifact_text=body[:6000], artifact_type='skill', num_cases=10)
        dataset.save(dataset_dir)
        
        print(f'  -> {len(dataset.all_examples)} examples')
        results['ok'].append(skill_name)
    except Exception as e:
        print(f'  -> ERROR: {str(e)[:80]}')
        results['error'].append({'skill': skill_name, 'error': str(e)[:100]})
    
    time.sleep(5)

with open('/tmp/dataset_generation_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print(f'\nDone: {len(results["ok"])}/{len(skills)} datasets created')
if results['error']:
    print(f'Failed: {[e["skill"] for e in results["error"]]}')