---
category: software-development
name: proactive-agent-lite
description: Transform AI agents from passive task-followers into proactive partners using memory architecture, reverse prompting, and self-healing patterns. Lightweight version focused on core proactive capabilities.
metadata:
  {
    "openclaw": {
      "requires": {},
      "install": []
    }
  }
---

# Proactive Agent Lite

Transform your AI agents from passive task-followers into proactive partners that anticipate needs and continuously improve.

## Architecture Overview

┌─────────────────────────────────────────────────────────────┐
│                    Agent Core                               │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Memory    │  │   Intent    │  │   Self-Healing      │  │
│  │  Manager    │  │  Tracker    │  │   Monitor           │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐│
│  │              Proactive Suggestion Engine                ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
## Core Features

### 1. Memory Architecture

Pre-compaction flush ensures context survives when the context window fills.

**Pattern**: Detect when context reaches 80% capacity and proactively summarize older context into compressed memory tokens.

python
class MemoryManager:
    def __init__(self, max_context_ratio=0.8):
        self.max_context_ratio = max_context_ratio
        self.compressed_memory = []

    def pre_compaction_flush(self, current_context, full_history):
        """Called before context window compaction."""
        # Extract key facts, decisions, and pending items
        critical_info = self.extract_critical_info(
            full_history,
            priority_keys=["decision", "fact", "commitment", "preference"]
        )
        # Store in compressed form for retrieval
        self.compressed_memory.extend(critical_info)
        return self.generate_summary(current_context)
### 2. Reverse Prompting

Surfaces ideas you didn't know to ask for by analyzing patterns and inferring unstated needs.

**Pattern**: Maintain an "unasked questions" queue based on context patterns.

python
class ReversePromptEngine:
    def __init__(self):
        self.unasked_needs = []
        self.pattern_triggers = [
            "repeated_approach",
            "implied_constraint",
            "missing_prerequisite",
            "opportunity_identified"
        ]

    def analyze_context(self, user_input, agent_history):
        """Identify what user needs but hasn't expressed."""
        needs = []

        # Detect repeated patterns suggesting inefficiency
        if self.detect_repeated_patterns(agent_history):
            needs.append({
                "type": "optimization",
                "suggestion": "I notice you're doing X repeatedly. "
                            "Would you like me to automate this?"
            })

        # Detect implied constraints
        constraints = self.extract_implied_constraints(user_input)
        if constraints:
            needs.append({
                "type": "constraint",
                "suggestion": f"I understand you need {constraints}. "
                            "I can also suggest alternatives you might consider."
            })

        return needs
### 3. Self-Healing Patterns

Diagnoses and fixes issues automatically through structured recovery protocols.

python
class SelfHealingMonitor:
    def __init__(self):
        self.error_patterns = {}
        self.recovery_strategies = {
            "context_drift": self.realign_context,
            "contradiction": self.resolve_contradiction,
            "incomplete_task": self.continue_task,
            "hallucination_risk": self.verify_with_grounding
        }

    def diagnose_and_recover(self, issue_type, context):
        """Automated diagnosis and recovery."""
        strategy = self.recovery_strategies.get(issue_type)

        if issue_type == "context_drift":
            return self.realign_context(context)
        elif issue_type == "hallucination_risk":
            return self.verify_with_grounding(context)

    def realign_context(self, context):
        """Realign when conversation has drifted from core objective."""
        return {
            "action": "reframe",
            "message": "Let me refocus on your core request: "
                     f"{self.extract_primary_goal(context)}"
        }

    def verify_with_grounding(self, context):
        """Reduce hallucination risk by adding verification steps."""
        return {
            "action": "add_verification",
            "checks": ["verify_facts", "cross_reference", "express_uncertainty"]
        }
### 4. Alignment Systems

Keeps the agent on mission and remembers who it serves.

python
class AlignmentSystem:
    def __init__(self, mission_statement):
        self.mission = mission_statement
        self.stakeholder_context = {}
        self.goal_hierarchy = []

    def validate_action(self, proposed_action, full_context):
        """Ensure proposed action aligns with mission."""
        alignment_score = self.calculate_alignment(
            proposed_action,
            self.mission,
            self.stakeholder_context
        )

        if alignment_score < 0.7:
            return {
                "approved": False,
                "reason": "Action may deviate from core mission",
                "suggestion": self.suggest_aligned_alternative(proposed_action)
            }
        return {"approved": True, "alignment_score": alignment_score}

    def calculate_alignment(self, action, mission, context):
        """Score how well an action aligns with stated mission."""
        # Implementation considers:
        # - Direct mission alignment
        # - Stakeholder priorities
        # - Long-term vs short-term impact
        return 0.85  # Placeholder - implement semantic similarity
## Usage

### Basic Integration

python
from openclaw import Agent
from proactive_agent_lite import (
    MemoryManager,
    ReversePromptEngine,
    SelfHealingMonitor,
    AlignmentSystem
)

agent = Agent(
    name="assistant",
    skills=["proactive-agent-lite"]
)

# Agent now automatically:
# - Manages context memory
# - Surfaces unasked needs
# - Self-heals from errors
# - Stays aligned with mission
### Initialization

python
# Configure proactive behaviors
agent.configure(
    proactive={
        "memory_flush_threshold": 0.8,      # When to compact context
        "suggestion_frequency": "moderate", # low/moderate/high
        "self_healing_enabled": True,
        "reverse_prompt_enabled": True,
        "alignment_checks": True
    }
)
## Configuration Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `memory_flush_threshold` | float | 0.8 | Context ratio triggering memory flush |
| `suggestion_frequency` | string | "moderate" | How often to surface proactive suggestions |
| `self_healing_enabled` | bool | true | Enable automatic error recovery |
| `reverse_prompt_enabled` | bool | true | Enable reverse prompting engine |
| `alignment_checks` | bool | true | Validate actions against mission |
| `max_compressed_memories` | int | 50 | Maximum memories to retain |

## Proactive Suggestion Examples

The agent will surface suggestions like:

- **"I notice you've described the same error 3 times. Shall I help diagnose the root cause?"**
- **"You mentioned you're on a deadline. I can prioritize the critical path if you'd like."**
- **"Based on your recent work, you might need [related tool/approach]. Should I prepare it?"**
- **"Your context is getting full. I've summarized the key points for continuity."**

## Requirements

- OpenClaw v1.0 or higher
- Python 3.9+ (for pattern implementations)
- Standard agent configuration

## Combining with Other Skills

python
agent = Agent(
    name="assistant",
    skills=[
        "proactive-agent-lite",
        "code-analysis",
        "security-scan"
    ]
)
# Proactive behaviors enhance other skill capabilities
## Extending the Framework

Add custom proactive behaviors:

python
from proactive_agent_lite import ProactiveMixin

class MyCustomProactive(ProactiveMixin):
    def custom_trigger(self, context):
        """Define custom proactive trigger."""
        return context.get("custom_condition", False)

    def custom_action(self, context):
        """Define response to trigger."""
        return {"suggestion": "Custom proactive response"}