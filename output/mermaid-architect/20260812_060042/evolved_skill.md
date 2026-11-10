---
category: software-development
name: mermaid-architect
description: Generate beautiful, hand-drawn Mermaid diagrams with robust syntax (quoted labels, ELK layout). Use this skill when the user asks for "diagram", "flowchart", "sequence diagram", or "visualize this process".
---

# Mermaid Architect

Generate clean, visually appealing Mermaid diagrams with proper syntax, safe node IDs, and optimized layouts. This skill ensures diagrams are renderable, maintainable, and follow Mermaid best practices.

## When to Use

Invoke this skill when the user requests:

- **Diagrams**: Flowcharts, sequence diagrams, class diagrams, state diagrams
- **Visualizations**: Architecture diagrams, process maps, timelines
- **Chart requests**: "Draw this", "Make a diagram", "Visualize this process"

## Capabilities

| Type | Use Cases |
|------|-----------|
| **Flowcharts** | Process mapping, decision trees, workflows, system processes |
| **Sequence Diagrams** | API calls, user interactions, message passing, service communication |
| **Class Diagrams** | OOP structures, inheritance hierarchies, database schemas, entity relationships |
| **State Diagrams** | Lifecycle management, finite state machines, status transitions |
| **Entity Relationship** | Database schemas, data models, relationships |
| **Gantt Charts** | Project timelines, scheduling, milestones |
| **Pie Charts** | Proportional data visualization |

## Syntax Guidelines

### Node Labels

**Always quote labels** that contain special characters:

mermaid
graph LR
    A["Node with (parentheses)"] --> B["Colon: and comma,"]
> **Required** when labels contain: `(` `)` `[` `]` `{` `}` `<` `>` `:` `,` `#` `"` `'`

### Safe Node IDs

Use only alphanumeric characters, underscores, or hyphens. Never use spaces.

| Style | Example | Status |
|-------|---------|--------|
| camelCase | `userService` | ✅ Good |
| PascalCase | `UserService` | ✅ Good |
| Underscores | `user_service` | ✅ Good |
| Spaces | `user service` | ❌ Bad |
| Reserved words | `end`, `subgraph`, `graph`, `flowchart` | ❌ Bad |

### Layout Direction

| Direction | Use When |
|-----------|----------|
| `TD` or `TB` | Hierarchies, organizational charts, top-down flows |
| `LR` | Timelines, sequences, left-to-right processes |
| `RL` | Right-to-left flows (use sparingly) |

### Subgraphs

Always provide both an ID and a label:

mermaid
graph LR
    subgraph backend ["Backend Services"]
        A[API Gateway] --> B[Auth Service]
        B --> C[Database]
    end
### Styling

Use ELK layout for complex diagrams with automatic positioning. Apply classes for consistent styling:

mermaid
graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Process]
    B -->|No| D[End]
    class A,C,D success-node
    classDef success-node fill:#90EE90,stroke:#228B22
## Common Pitfalls to Avoid

1. **Unquoted special characters** — Labels with `()` or `:` break rendering
2. **Reserved ID words** — Never use `end`, `subgraph`, `graph`, `flowchart` as IDs
3. **Inconsistent spacing** — Maintain uniform formatting
4. **Missing arrows** — Every non-terminal node needs an outgoing edge
5. **Overcomplexity** — Break large diagrams into subgraphs

## Reference Materials

### Syntax & Best Practices
- [Syntax Guide](references/syntax-guide.md) — Complete syntax reference with examples

### Example Diagrams
- [Microservice Architecture](assets/examples/microservice-arch.mmd) — Multi-service system with ELK layout
- [API Sequence Diagram](assets/examples/sequence-api.mmd) — Request/response flow with auth
- [State Lifecycle](assets/examples/state-lifecycle.mmd) — State machine with transitions

## Validation

Before deploying, validate all `.mmd` files:

bash
scripts/validate-mmd assets/examples/*.mmd
Validate a single file:

bash
scripts/validate-mmd assets/examples/microservice-arch.mmd