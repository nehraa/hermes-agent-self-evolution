#!/usr/bin/env python3
"""Pre-generate evaluation datasets for all real Hermes skills in GEPA."""
import json, os, sys, time
from pathlib import Path

# Add GEPA to path
sys.path.insert(0, '/home/Hermes/repos/gepa')
os.environ.setdefault('MINIMAX_API_KEY', 'sk-cp-KjobHFSNe1A5LaEtTY0qrBV5l85bitrDDWkjO4VEtsGd6h8uTnRmbcuEQflj1FXbUwFX2L9S1Qt5_M-dqpFnX7qMGg7GUtGTfYp5EJJ05MVyuLN7N5WWoyA')
os.environ.setdefault('LITELLM_API_BASE', 'https://api.minimax.io/v1')

os.environ["MINIMAX_API_KEY"] = "sk-cp-...WoyA"
os.environ["LITELLM_API_BASE"] = "https://api.minimax.io/v1"

from evolution.core.config import EvolutionConfig
from evolution.core.dataset_builder import SyntheticDatasetBuilder

skills = [
    ('github-code-review', '/home/Hermes/.hermes/skills/github/github-code-review/SKILL.md'),
    ('notion', '/home/Hermes/.hermes/skills/productivity/notion/SKILL.md'),
    ('kaggle-sdxl-image-gen', '/home/Hermes/.hermes/skills/mlops/kaggle-sdxl-image-gen/SKILL.md'),
    ('arxiv', '/home/Hermes/.hermes/skills/research/arxiv/SKILL.md'),
    ('huggingface-hub', '/home/Hermes/.hermes/skills/mlops/huggingface-hub/SKILL.md'),
    ('codebase-inspection', '/home/Hermes/.hermes/skills/github/codebase-inspection/SKILL.md'),
    ('whatsapp-bulk-messaging', '/home/Hermes/.hermes/skills/messaging/whatsapp-bulk-messaging/SKILL.md'),
    ('llm-wiki', '/home/Hermes/.hermes/skills/research/llm-wiki/SKILL.md'),
    ('ai-video-production', '/home/Hermes/.hermes/skills/media/ai-video-production/SKILL.md'),
    ('comfyui', '/home/Hermes/.hermes/skills/creative/comfyui/SKILL.md'),
    ('p5js', '/home/Hermes/.hermes/skills/creative/p5js/SKILL.md'),
    ('claude-code', '/home/Hermes/.hermes/skills/autonomous-ai-agents/claude-code/SKILL.md'),
]

config = EvolutionConfig(iterations=3)
# Force MiniMax for dataset generation — judge_model defaults to openai/gpt-4.1 which has no key
config.judge_model = "minimax/MiniMax-M2.7"
config.eval_model = "minimax/MiniMax-M2.7"
results = []

for skill_name, skill_path in skills:
    print(f'\n{"="*60}')
    print(f'Generating dataset for: {skill_name}')
    print(f'{"="*60}')
    
    try:
        raw = Path(skill_path).read_text()
        
        # Parse frontmatter
        body = raw
        if raw.strip().startswith('---'):
            parts = raw.split('---', 2)
            if len(parts) >= 3:
                body = parts[2].strip()
        
        builder = SyntheticDatasetBuilder(config)
        dataset = builder.generate(
            artifact_text=body,
            artifact_type='skill',
        )
        
        save_path = Path('/home/Hermes/repos/gepa/datasets/skills') / skill_name
        dataset.save(save_path)
        
        print(f'  Generated {len(dataset.all_examples)} examples '
              f'(train={len(dataset.train)}, val={len(dataset.val)}, holdout={len(dataset.holdout)})')
        results.append({'skill': skill_name, 'status': 'ok', 'examples': len(dataset.all_examples)})
        
    except Exception as e:
        print(f'  ERROR: {e}')
        results.append({'skill': skill_name, 'status': 'error', 'error': str(e)})

print(f'\n\nDONE — {len([r for r in results if r["status"]=="ok"])}/{len(results)} datasets created')
for r in results:
    if r['status'] == 'ok':
        print(f"  {r['skill']}: {r['examples']} examples")
    else:
        print(f"  {r['skill']}: ERROR — {r.get('error')}")