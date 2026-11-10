---
name: mermaid-architect
description: Generate clean, well-structured Mermaid diagrams for flowcharts, sequence diagrams, class diagrams, and state diagrams. Use when users ask to "diagram this", "visualize this process", "draw a flowchart", or "show me how X connects to Y".
---

# Mermaid Architect

Generate beautiful, hand-drawn-style diagrams using Mermaid syntax with robust, error-free code.

## When to Use

**Trigger phrases:**
- "diagram this", "draw a diagram", "make a diagram"
- "visualize this process", "show the flow"
- "flowchart", "sequence diagram", "class diagram", "state diagram"
- "how does X connect to Y", "show the architecture"

**Output format:** Always provide a Mermaid code block (` ```mermaid `) followed by a brief explanation.

## Diagram Types

### 1. Flowcharts
Process mapping, decision trees, workflows, branching logic.
flowchart TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Process]
    B -->|No| D[End]
### 2. Sequence Diagrams
API calls, user interactions, request-response flows.
sequenceDiagram
    Client->>API: POST /orders
    API-->>Client: 201 Created
### 3. Class Diagrams
OOP structures, database schemas, entity relationships.
classDiagram
    class Order {
        +String id
        +DateTime createdAt
        +create()
    }
### 4. State Diagrams
Lifecycle management, status transitions, finite state machines.
stateDiagram-v2
    [*] --> Draft
    Draft --> Published
    Published --> Archived
## Syntax Rules

### Node Labels
- **Use double quotes** when labels contain special characters: `()`, `,`, `:`, `#`, or `|`
  ```mermaid
  flowchart LR
      A["User (Admin)"] --> B["Action: Create"]
  ```

### Node IDs
- **No spaces** allowed — use `camelCase`, `PascalCase`, or `snake_case`
- **Avoid reserved words:** `end`, `subgraph`, `graph`, `flowchart`, `state`, `class`

### Layout Direction
- `TD` or `TB` — Top-down (hierarchies, trees)
- `LR` — Left-right (timelines, processes, API flows)
- `BT` — Bottom-top (inverted hierarchies)

### Subgraphs
Always provide an explicit ID and a quoted label:
mermaid
flowchart LR
    subgraph Backend ["Backend Services"]
        A[API] --> B[Database]
    end
## Quick Reference

| Diagram Type | Best For | Direction |
|--------------|----------|-----------|
| Flowchart | Processes, decisions, workflows | TD or LR |
| Sequence | API calls, user interactions | Auto |
| Class | OOP, schemas, entities | TD |
| State | Transitions, lifecycles | TD |

## Examples

| File | Use Case |
|------|----------|
| `assets/examples/microservice-arch.mmd` | Microservices architecture |
| `assets/examples/sequence-api.mmd` | REST API sequence |
| `assets/examples/state-lifecycle.mmd` | Order/status lifecycle |

## Validation

Check your `.mmd` files for syntax errors:

bash
scripts/validate-mmd assets/examples/*.mmd
A successful validation produces no output. Errors display line numbers and descriptions.

## Tips

- **Start simple** — begin with the main nodes, then add details
- **Group logically** — use subgraphs to organize complex diagrams
- **Label transitions** — always include edge labels for clarity
- **Test early** — validate after writing complex syntax