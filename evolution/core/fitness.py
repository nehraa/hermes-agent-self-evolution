"""Fitness functions for evaluating evolved artifacts.

Uses LLM-as-judge with rubrics to score agent outputs.
Supports length penalties and multi-dimensional scoring.
"""

import dspy
from dataclasses import dataclass
from typing import Optional

from evolution.core.config import EvolutionConfig


@dataclass
class FitnessScore:
    """Multi-dimensional fitness score."""
    correctness: float = 0.0  # Did the agent produce correct output? (0-1)
    procedure_following: float = 0.0  # Did it follow the skill's procedure? (0-1)
    conciseness: float = 0.0  # Was it appropriately concise? (0-1)
    length_penalty: float = 0.0  # Penalty for being too verbose (0-1, 0 = no penalty)
    feedback: str = ""  # Textual feedback for GEPA's reflective analysis

    @property
    def composite(self) -> float:
        """Weighted composite score."""
        raw = (
            0.5 * self.correctness
            + 0.3 * self.procedure_following
            + 0.2 * self.conciseness
        )
        return max(0.0, raw - self.length_penalty)


class LLMJudge:
    """LLM-as-judge scorer with rubric-based evaluation.

    Scores agent outputs on multiple dimensions and provides
    textual feedback that GEPA can use for reflective mutation.
    """

    class JudgeSignature(dspy.Signature):
        """Evaluate an agent's response against an expected behavior rubric.

        Score the response on three dimensions (0.0 to 1.0 each):
        1. correctness: Did the response correctly address the task?
        2. procedure_following: Did it follow the expected approach/procedure?
        3. conciseness: Was it appropriately concise without omitting important info?

        Also provide specific, actionable feedback on what could be improved.
        """
        task_input: str = dspy.InputField(desc="The task the agent was given")
        expected_behavior: str = dspy.InputField(desc="Rubric describing what a good response looks like")
        agent_output: str = dspy.InputField(desc="The agent's actual response")
        skill_text: str = dspy.InputField(desc="The skill/instructions the agent was following")
        correctness: float = dspy.OutputField(desc="Score 0.0-1.0: Did the response correctly address the task?")
        procedure_following: float = dspy.OutputField(desc="Score 0.0-1.0: Did it follow the expected procedure?")
        conciseness: float = dspy.OutputField(desc="Score 0.0-1.0: Appropriately concise?")
        feedback: str = dspy.OutputField(desc="Specific, actionable feedback on what could be improved")

    def __init__(self, config: EvolutionConfig):
        self.config = config
        self.judge = dspy.ChainOfThought(self.JudgeSignature)

    def score(
        self,
        task_input: str,
        expected_behavior: str,
        agent_output: str,
        skill_text: str,
        artifact_size: Optional[int] = None,
        max_size: Optional[int] = None,
    ) -> FitnessScore:
        """Score an agent output using LLM-as-judge."""

        import os as _fitness_os
        _fitness_os.environ.setdefault("MINIMAX_API_KEY", "sk-cp-KjobHFSNe1A5LaEtTY0qrBV5l85bitrDDWkjO4VEtsGd6h8uTnRmbcuEQflj1FXbUwFX2L9S1Qt5_M-dqpFnX7qMGg7GUtGTfYp5EJJ05MVyuLN7N5WWoyA")
        _fitness_os.environ.setdefault("LITELLM_API_BASE", "https://api.minimax.io/v1")
        if "minimax" in self.config.eval_model.lower():
            lm = dspy.LM(self.config.eval_model, api_key=_fitness_os.environ["MINIMAX_API_KEY"], temperature=0.7, max_tokens=1024)
        else:
            lm = dspy.LM(self.config.eval_model)

        with dspy.context(lm=lm):
            result = self.judge(
                task_input=task_input,
                expected_behavior=expected_behavior,
                agent_output=agent_output,
                skill_text=skill_text,
            )

        # Parse scores (clamp to 0-1)
        correctness = _parse_score(result.correctness)
        procedure_following = _parse_score(result.procedure_following)
        conciseness = _parse_score(result.conciseness)

        # Length penalty
        length_penalty = 0.0
        if artifact_size is not None and max_size is not None:
            ratio = artifact_size / max_size
            if ratio > 0.9:
                # Penalty ramps from 0 at 90% to 0.3 at 100%+
                length_penalty = min(0.3, (ratio - 0.9) * 3.0)

        return FitnessScore(
            correctness=correctness,
            procedure_following=procedure_following,
            conciseness=conciseness,
            length_penalty=length_penalty,
            feedback=str(result.feedback),
        )


def skill_fitness_metric(example: dspy.Example, prediction: dspy.Prediction, trace=None) -> float:
    """DSPy-compatible metric function for GEPA's internal optimization loop.

    Uses a fast structural/semantic proxy — NOT keyword overlap.
    GEPA calls this hundreds of times per skill, so it MUST be fast (<10ms).
    The actual LLM-as-judge is only used for final holdout evaluation (see evolve_skill.py).
    """
    # The prediction should have an 'output' field with the agent's response
    agent_output = getattr(prediction, "output", "") or ""
    expected = getattr(example, "expected_behavior", "") or ""
    task = getattr(example, "task_input", "") or ""

    if not agent_output.strip():
        return 0.0

    # Fast structural scoring — captures task structure compliance without LLM calls
    # Heuristic: score based on presence of key structural elements
    score = 0.5  # Base score for non-empty output

    # Check procedure-following via structural markers
    # (e.g., "Step 1:", "##", code blocks, list items in expected_behavior)
    expected_lower = expected.lower()
    output_lower = agent_output.lower()

    # 1. Procedure markers: does output have expected section structure?
    proc_markers = ['step', '##', '```', '1.', '2.', '- ', '* ', ':']
    expected_has_proc = any(m in expected_lower for m in proc_markers)
    output_has_proc = any(m in output_lower for m in proc_markers)
    if expected_has_proc and not output_has_proc:
        score -= 0.15
    elif expected_has_proc and output_has_proc:
        score += 0.1

    # 2. Completeness: did output address the task scope?
    # Check if key nouns from task appear in output
    task_words = set(task.lower().split())
    output_words = set(output_lower.split())
    if task_words:
        task_coverage = len(task_words & output_words) / len(task_words)
        score = max(0.3, min(0.9, score + 0.2 * task_coverage))

    # 3. Non-empty structural content (not just one-liners)
    if len(agent_output) > 200:
        score += 0.1
    if len(agent_output) < 50:
        score -= 0.1

    # 4. Keyword presence from expected_behavior (soft check, not Jaccard)
    # Avoids double-penalizing when expected is short
    if len(expected) > 50:
        expected_words = set(expected_lower.split())
        output_words = set(output_lower.split())
        if expected_words:
            overlap = len(expected_words & output_words) / len(expected_words)
            score = score * 0.7 + (0.3 * (0.3 + 0.7 * overlap))

    return min(1.0, max(0.0, score))


def _parse_score(value) -> float:
    """Parse a score value, handling various LLM output formats."""
    if isinstance(value, (int, float)):
        return min(1.0, max(0.0, float(value)))
    try:
        return min(1.0, max(0.0, float(str(value).strip())))
    except (ValueError, TypeError):
        return 0.5  # Default to neutral on parse failure
