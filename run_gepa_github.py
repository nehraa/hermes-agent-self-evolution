#!/usr/bin/env python3
"""
GEPA Runner for github-code-review skill
"""
import os, sys
from pathlib import Path

MINIMAX_KEY = "sk-cp-KjobHFSNe1A5LaEtTY0qrBV5l85bitrDDWkjO4VEtsGd6h8uTnRmbcuEQflj1FXbUwFX2L9S1Qt5_M-dqpFnX7qMGg7GUtGTfYp5EJJ05MVyuLN7N5WWoyA"
HERMES_AGENT_REPO = str(Path.home() / ".hermes")
SKILL_NAME = "github-code-review"

os.environ["MINIMAX_API_KEY"] = MINIMAX_KEY
os.environ["HERMES_AGENT_REPO"] = HERMES_AGENT_REPO

# Configure DSPy with MiniMax BEFORE importing evolution modules
import dspy
lm = dspy.LM(
    "minimax/MiniMax-M2.7",
    api_key=MINIMAX_KEY,
    api_base="https://api.minimax.io/v1",
    temperature=0.7,
    max_tokens=2048,
    system_prompt="You are a helpful coding assistant. Give clear, direct answers. No excessive reasoning."
)
dspy.configure(lm=lm)
print(f"✓ DSPy configured with MiniMax")

sys.path.insert(0, "/tmp/hermes-agent-self-evolution")

# Now run the evolution
from evolution.skills.evolve_skill import evolve

print(f"\n🧬 GEPA Evolution — {SKILL_NAME} — 3 iterations\n")

result = evolve(
    skill_name=SKILL_NAME,
    iterations=3,
    eval_source="synthetic",
    dataset_path=None,
    optimizer_model="minimax/MiniMax-M2.7",
    eval_model="minimax/MiniMax-M2.7",
    hermes_repo=HERMES_AGENT_REPO,
    run_tests=False,
    dry_run=False,
)

print(f"\n{'='*60}")
if result:
    print(f"✓ GEPA completed!")
    print(f"  Best fitness: {result.get('best_fitness', 'N/A')}")
    print(f"  Num improvements: {result.get('num_improvements', 0)}")
else:
    print(f"✗ GEPA returned no result")