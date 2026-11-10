---
name: mermaid-architect
description: Generate beautiful, hand-drawn Mermaid diagrams with robust syntax (quoted labels, ELK layout). Use this skill when the user asks for "diagram", "flowchart", "sequence diagram", or "visualize this process".
---

# Mermaid Architect

Generate Mermaid diagrams with proper syntax that renders correctly every time.

## When to Use

**Trigger phrases**: "draw", "diagram", "flowchart", "visualize", "create a chart", "show the process", "map out"

**Output format**: Always provide a Mermaid code block followed by a brief explanation of the diagram structure.

## Capabilities

| Diagram Type | Best For |
|--------------|----------|
| **Flowchart** | Decision trees, process flows, workflows |
| **Sequence** | API calls, user interactions, system exchanges |
| **Class** | OOP structures, database schemas, entity relationships |
| **State** | Lifecycle management, finite state machines |
| **ER** | Database entity relationships |
| **Gantt** | Project timelines |

## Core Syntax Rules

### Node Labels
Always use double quotes for labels containing special characters:
- Parentheses: `"User (admin)"`
- Commas: `"Error, try again"`
- Colons: `"Step 1: Initialize"`
- Hashes: `"## Header ##"`

mermaid
graph TD
    A["Node with (parentheses)"] --> B["Label with, commas"]
### Node IDs
- Use camelCase, PascalCase, or underscores: `startNode`, `process_step`, `UserLogin`
- Avoid reserved words: `end`, `subgraph`, `graph`, `flowchart`, `node`
- Never use spaces

### Direction
- `TD` (Top-Down): Hierarchies, levels, tree structures
- `LR` (Left-Right): Timelines, sequences, horizontal flows

mermaid
flowchart TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Process]
    B -->|No| D[End]
## Subgraph Syntax

Always include both ID and label:

mermaid
flowchart LR
    subgraph BACKEND ["Backend Services"]
        A[API] --> B[Database]
    end
    subgraph FRONTEND ["Frontend"]
        C[UI] --> A
    end
## Validation

Test your diagrams against the validator:

bash
scripts/validate-mmd assets/examples/*.mmd
## Reference Materials

- [Syntax Guide](references/syntax-guide.md) — Complete syntax rules and edge cases
- [Microservices Example](assets/examples/microservice-arch.mmd)
- [API Sequence Example](assets/examples/sequence-api.mmd)
- [State Lifecycle Example](assets/examples/state-lifecycle.mmd)

## Quick Checklist

Before outputting any diagram, verify:
- [ ] All labels with special chars are quoted
- [ ] IDs use safe naming (no reserved words)
- [ ] Direction is appropriate for the content type
- [ ] Subgraph IDs contain no spaces