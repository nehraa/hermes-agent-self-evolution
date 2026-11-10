#!/usr/bin/env python3
"""
GEPA Runner — Evolve a Hermes skill using DSPy + GEPA with MiniMax LM
"""
import os, sys, json
from pathlib import Path

# ── Config ──────────────────────────────────────────────────────────────────
MINIMAX_KEY = "sk-cp-KjobHFSNe1A5LaEtTY0qrBV5l85bitrDDWkjO4VEtsGd6h8uTnRmbcuEQflj1FXbUwFX2L9S1Qt5_M-dqpFnX7qMGg7GUtGTfYp5EJJ05MVyuLN7N5WWoyA"
HERMES_AGENT_REPO = Path.home() / ".hermes"  # find_skill searches .skills/ here
SKILL_NAME = "github-code-review"  # Built-in skill in hermes-agent/skills/github/
ITERATIONS = 5  # Quick test run

os.environ["MINIMAX_API_KEY"] = MINIMAX_KEY
os.environ["HERMES_AGENT_REPO"] = str(HERMES_AGENT_REPO)

# ── Setup DSPy with MiniMax ────────────────────────────────────────────────
import dspy

lm = dspy.LM(
    "minimax/MiniMax-M2.7",
    api_key=MINIMAX_KEY,
    api_base="https://api.minimax.io/v1",
    temperature=0.7,
    max_tokens=2048,
    system_prompt="You are a helpful assistant. Give clear, direct answers. No excessive reasoning."
)
dspy.configure(lm=lm)
print(f"✓ DSPy configured with MiniMax LM")
print(f"  GEPA: {hasattr(dspy, 'GEPA')}")
print(f"  MIPROv2: {hasattr(dspy, 'MIPROv2')}")

# ── Import evolution modules ────────────────────────────────────────────────
sys.path.insert(0, "/tmp/hermes-agent-self-evolution")

from evolution.core.config import EvolutionConfig
from evolution.core.dataset_builder import SyntheticDatasetBuilder, EvalDataset, GoldenDatasetLoader
from evolution.core.fitness import skill_fitness_metric, LLMJudge, FitnessScore
from evolution.core.constraints import ConstraintValidator
from evolution.skills.skill_module import load_skill, find_skill, reassemble_skill

# ── Load target skill ──────────────────────────────────────────────────────
skill_path = find_skill(SKILL_NAME, HERMES_AGENT_REPO / "skills")
if not skill_path:
    # Try user skills dir
    skill_path = find_skill(SKILL_NAME, Path.home() / ".hermes/skills")

if not skill_path:
    print(f"✗ Skill '{SKILL_NAME}' not found")
    sys.exit(1)

skill_data = load_skill(skill_path)
print(f"✓ Loaded skill: {skill_data['name']}")
print(f"  Path: {skill_path}")
print(f"  Size: {len(skill_data['content'])} chars")

# ── Build evaluation dataset ───────────────────────────────────────────────
print(f"\n[2] Building synthetic evaluation dataset...")
dataset_builder = SyntheticDatasetBuilder(
    judge_model="minimax/MiniMax-M2.7",  # Use same model as judge
    config=EvolutionConfig()
)

# Generate test cases for the coderag skill
eval_dataset = dataset_builder.build(
    skill_content=skill_data["content"],
    skill_name=SKILL_NAME,
    num_examples=10,  # Small for test run
    source="synthetic"
)

print(f"  Generated {len(eval_dataset.examples)} eval examples")
if eval_dataset.examples:
    ex = eval_dataset.examples[0]
    print(f"  Example: Q={ex.get('input', ex.get('question', '?'))[:60]} A={ex.get('output', ex.get('answer', '?'))[:60]}")

# ── Initialize GEPA optimizer ──────────────────────────────────────────────
print(f"\n[3] Setting up GEPA optimizer...")
config = EvolutionConfig(
    iterations=ITERATIONS,
    hermes_agent_path=HERMES_AGENT_REPO,
    eval_dataset_size=len(eval_dataset.examples),
    run_pytest=False,  # No pytest for this skill
    create_pr=False,   # Dry run
)

# ── Run GEPA optimization ───────────────────────────────────────────────────
print(f"\n[4] Running GEPA ({ITERATIONS} iterations)...")

try:
    from evolution.skills.evolve_skill import evolve as run_gepa

    result = run_gepa(
        skill_name=SKILL_NAME,
        iterations=ITERATIONS,
        eval_source="synthetic",
        dataset_path=None,
        optimizer_model="minimax/MiniMax-M2.7",
        eval_model="minimax/MiniMax-M2.7",
        hermes_repo=str(HERMES_AGENT_REPO),
        run_tests=False,
        dry_run=False,
    )

    print(f"\n✓ GEPA completed!")
    print(f"  Best fitness: {result.get('best_fitness', 'N/A')}")
    print(f"  Improvements: {result.get('num_improvements', 0)}")
    print(f"  Output: {result.get('output_path', 'N/A')}")

except Exception as e:
    print(f"\n✗ GEPA error: {e}")
    import traceback
    traceback.print_exc()

print("\nDone.")