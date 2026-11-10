import os, sys
sys.path.insert(0, '/home/Hermes/repos/gepa')

# Load MINIMAX_API_KEY from hermes .env
env_file = os.path.expanduser('~/.hermes/.env')
if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            stripped = line.strip()
            key_start = stripped.startswith('MINIMAX_API_KEY=')
            is_comment = stripped.startswith('#')
            if key_start and not is_comment:
                os.environ['MINIMAX_API_KEY'] = stripped.split('=', 1)[1]
                break

print('Key:', os.environ.get('MINIMAX_API_KEY', 'NOT SET')[:15], '...')

from evolution.skills.evolve_skill import evolve
from evolution.core.config import EvolutionConfig

config = EvolutionConfig(iterations=3)
try:
    evolve(
        skill_name='notion',
        iterations=3,
        eval_source='golden',
        dataset_path='/home/Hermes/repos/gepa/datasets/skills/notion',
        eval_model='minimax/MiniMax-M2.7',
        hermes_repo='/home/Hermes/.hermes/hermes-agent',
        dry_run=False,
    )
    print('RESULT: SUCCESS')
except Exception as e:
    print(f'RESULT: FAILED -- {e}')
