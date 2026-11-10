---
name: proactive-agent-lite
description: Transform AI agents from task-followers into proactive partners using memory architecture, reverse prompting, and self-healing patterns. Lightweight implementation focused on core proactive capabilities.
category: software-development
metadata:
  {
    "openclaw":
      {
        "requires": {},
        "install": []
      }
  }
---

# Proactive Agent Lite

Transform your AI agents from passive task-followers into proactive partners that anticipate needs, maintain context, and self-correct.

## What This Does

- **Memory Architecture**: Implements a pre-compaction flush strategy that persists context before context window limits are reached
- **Reverse Prompting**: Generates implicit suggestions based on detected patterns in user interactions
- **Self-Healing**: Automatic detection and correction of conversation state inconsistencies
- **Mission Alignment**: Continuous verification that agent responses serve the stated objective

## Implementation Details

### Memory Architecture

The memory system flushes context summaries before context window exhaustion:

Context Window
├── [Active Conversation] ──→ Pre-compaction trigger (80% threshold)
├── [Working Memory]        ──→ Summarized and compacted
├── [Persistent Context]    ──→ Extracted to external store
└── [Recovery State]        ──→ Preserved for continuation
**Trigger Point**: Flush initiates at 80% context utilization to ensure safe extraction.

### Self-Healing Patterns

| Detection | Response |
|-----------|----------|
| Context gap detected | Reconstitute from persistent store |
| Response inconsistency | Flag and offer clarification |
| Mission drift identified | Redirect with context anchor |
| Error in previous output | Correct and acknowledge |

### Reverse Prompting

Analyzes conversation patterns to surface:

- Implicit assumptions that may need validation
- Related tasks that frequently follow current workflow
- Potential edge cases in current request
- Information gaps based on conversation history

## Usage

Install this skill to enable proactive behavior. The agent will automatically:

1. Monitor context utilization and trigger compaction before overflow
2. Surface relevant suggestions based on conversation patterns
3. Self-correct when inconsistencies are detected
4. Verify alignment with stated mission

## Configuration

yaml
proactive-agent-lite:
  memory:
    flush_threshold: 0.8      # Context percentage to trigger flush
    summary_style: structured  # structured | narrative | bullet
    preserve_recent: 3        # Last N messages kept verbatim

  self_healing:
    enabled: true
    auto_correct: true        # If false, only flags issues
    verify_alignment: true     # Check mission consistency

  reverse_prompting:
    enabled: true
    suggestion_frequency: contextual  # always | contextual | on_request
    max_suggestions: 3
## Behavior Examples

### Before (Passive)
User: "Generate a report"
Agent: *Generates report*
### After (Proactive)
User: "Generate a report"
Agent: *Detects this is part of recurring workflow*
       *Suggests: "Include the Q3 metrics comparison?"*
       *Offers: "Should I schedule this for weekly delivery?"*
       *Generates report with suggested additions*
### Self-Healing Example
Agent: "Based on the previous data, your conversion improved by 30%"

[System detects potential inconsistency in referenced data]

Agent: "Correction: The 30% figure requires verification against the 
       complete dataset. Running validation now..."
       *Confirms data or requests clarification*
## Requirements

- OpenClaw v1.0 or higher
- Context window with minimum 2,000 token capacity recommended

## Combining with Other Skills

This skill works synergistically with:

- `context-management` - Enhanced context handling
- `task-planner` - Proactive task decomposition
- `reflection-loop` - Deeper self-analysis capabilities

Add proactive-agent-lite first to establish the proactive foundation, then layer additional skills for specialized behavior.