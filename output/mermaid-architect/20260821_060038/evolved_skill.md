---
category: software-development
description: Generate beautiful, hand-drawn Mermaid diagrams with robust syntax (quoted labels, ELK layout). Use this skill when the user asks for "diagram", "flowchart", "sequence diagram", or "visualize this process".
name: mermaid-architect
---

# Mermaid Architect

Generate clean, syntax-safe Mermaid diagrams from text descriptions. Handles flowcharts, sequence diagrams, class diagrams, state diagrams, and more.

## When to Use

Activate this skill when the user requests:

- "Draw a diagram for..."
- "Create a flowchart of..."
- "Visualize this process"
- "Make a sequence diagram"
- Any request involving diagram, flowchart, architecture, or visualization

## Output Format

Always return:

1. A `mermaid` code block containing the diagram code
2. A brief explanation of what the diagram represents

## Supported Diagram Types

| Type | Use Case | Key Syntax |
|------|----------|------------|
| **Flowchart** | Process mapping, decision trees | `graph TD/BT/LR/RL` |
| **Sequence** | API calls, user interactions | `sequenceDiagram` |
| **Class** | OOP structures, schemas | `classDiagram` |
| **State** | Lifecycle management | `stateDiagram-v2` |
| **ER** | Database relationships | `erDiagram` |
| **Gantt** | Project timelines | `gantt` |

## Syntax Rules

### Node Labels

Always quote labels that contain special characters:

✅ graph LR
    A["User (Admin)"] --> B["Server:3000"]

❌ graph LR
    A[User (Admin)] --> B[Server:3000]  "breaks parsing"
### Node IDs

- Use `camelCase`, `PascalCase`, or `underscores`
- Never use spaces
- Avoid reserved keywords: `end`, `subgraph`, `graph`, `flowchart`, `node`, `left`, `right`

✅ userLogin, UserLogin, user_login
❌ user login, graph, end, subgraph
### Layout Direction

| Directive | Direction | Best For |
|-----------|-----------|----------|
| `TD` or `TB` | Top → Down | Hierarchies, org charts |
| `BT` | Bottom → Top | Inverted hierarchies |
| `LR` | Left → Right | Timelines, sequences, APIs |
| `RL` | Right → Left | Reverse flows |

### Subgraphs

Always provide both an ID and a quoted label:

✅ subgraph backend ["Backend Services"]
❌ subgraph backend
❌ subgraph ["Backend Services"]
## Quick Reference

graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E
## Validation

Test diagrams against sample files:

bash
scripts/validate-mmd assets/examples/*.mmd
## Examples

| Example | File | Use Case |
|---------|------|----------|
| Microservices | `assets/examples/microservice-arch.mmd` | System architecture |
| API Sequence | `assets/examples/sequence-api.mmd` | Request/response flows |
| State Machine | `assets/examples/state-lifecycle.mmd` | Object lifecycles |

## Additional Resources

- [Syntax Guide](references/syntax-guide.md) — Full safe-syntax reference
- [Mermaid Live Editor](https://mermaid.live) — Preview diagrams interactively