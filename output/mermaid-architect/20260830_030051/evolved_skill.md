---
category: software-development
name: mermaid-architect
description: Generate beautiful, hand-drawn style Mermaid diagrams with robust syntax. Use when users ask for diagrams, flowcharts, sequence diagrams, or to visualize a process. Applies safe quoting rules and ELK-safe syntax.
---

# Mermaid Architect

Generate clean, render-ready Mermaid diagrams with syntax that won't break in GitHub, Notion, or any ELK-compatible renderer.

## When to Use

Invoke this skill when a user requests:

- A diagram, flowchart, or process map
- A sequence diagram for API calls or interactions
- A class diagram for OOP or database schemas
- A state diagram for lifecycle visualization
- Any visual representation of a process, architecture, or flow

## Output Format

Always provide:

1. A complete `mermaid` code block with the diagram
2. A brief explanation of what the diagram renders

## Diagram Types Supported

| Type | Use Case |
|------|----------|
| **Flowchart** | Process mapping, decision trees, workflows |
| **Sequence** | API calls, user interactions, system communication |
| **Class** | OOP structures, database schemas, entity relationships |
| **State** | Lifecycle management, finite state machines |

## Syntax Rules

### Node Labels

Always **quote labels** that contain special characters:

✓  A["User (Admin)"]
✓  B["API: /v1/users"]
✗  A[User (Admin)]      ← breaks in some renderers
### Node IDs

- Use `camelCase`, `PascalCase`, or `snake_case` (no spaces)
- Avoid reserved keywords: `end`, `subgraph`, `graph`, `flowchart`, `node`, `edge`

### Direction

| Directive | Best For |
|-----------|----------|
| `TD` or `TB` | Hierarchies, trees, top-down flows |
| `LR` | Timelines, sequences, left-to-right processes |

### Subgraphs

Always include both an ID and a label:

subgraph backend ["Backend Services"]
    A[API Gateway]
    B[Auth Service]
end
## Reference Materials

- [Syntax Guide](references/syntax-guide.md) — full safe-syntax rules
- [Microservices Example](assets/examples/microservice-arch.mmd)
- [API Sequence Example](assets/examples/sequence-api.mmd)
- [State Lifecycle Example](assets/examples/state-lifecycle.mmd)

## Validation

Validate one or more `.mmd` files:

bash
scripts/validate-mmd assets/examples/*.mmd