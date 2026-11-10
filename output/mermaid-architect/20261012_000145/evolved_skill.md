---
name: mermaid-architect
description: Generate beautiful, hand-drawn Mermaid diagrams with robust syntax. Use this skill when the user asks for "diagram", "flowchart", "sequence diagram", "ER diagram", "Gantt chart", or "visualize this process".
---

# Mermaid Architect

## When to Use

**Trigger phrases**: "draw", "make a diagram", "visualize", "flowchart", "show the process", "create a sequence", "diagram this"

**Output**: A Mermaid code block (`mermaid`) with optional explanation.

## Diagram Types

| Type | Use Case |
|------|----------|
| **Flowchart** | Process maps, decision trees, workflows |
| **Sequence** | API calls, user interactions, system events |
| **Class** | OOP structures, database schemas |
| **State** | Lifecycle management, finite state machines |
| **ER** | Entity relationships, data models |
| **Gantt** | Project timelines, scheduling |

## Syntax Rules

### Node Labels
Always quote labels containing special characters:

✓ "User Authentication (OAuth2)"
✓ "Validate Input: email, password"
✓ "HTTP 500: Server Error"
✗ User Authentication (OAuth2)
### Node IDs
- No spaces allowed
- Use `camelCase`, `PascalCase`, or `snake_case`
- Avoid reserved keywords: `end`, `subgraph`, `graph`, `flowchart`, `node`, `edge`

✓ userAuth, ValidateInput, api_gateway
✗ user auth, validate input, node1
### Layout Direction
- `TD` (Top-Down): Hierarchies, trees, organizational charts
- `LR` (Left-Right): Timelines, sequences, processes flowing horizontally

### Subgraphs
Use explicit ID with quoted label:

subgraph backend ["Backend Services"]
## Quick Examples

**Flowchart**:
mermaid
flowchart TD
    A[Start] --> B{Is Valid?}
    B -->|Yes| C["Process Data (3 steps)"]
    B -->|No| D["Log Error: timeout, connection"]
    C --> E((End))
**Sequence**:
mermaid
sequenceDiagram
    Client->>+API: POST /users {"name": "Alice"}
    API->>+DB: INSERT INTO users
    DB-->>-API: 201 Created
    API-->>-Client: {"id": 42}
## Reference Materials

| File | Purpose |
|------|---------|
| [references/syntax-guide.md](references/syntax-guide.md) | Complete syntax reference with dos and don'ts |
| [assets/examples/microservice-arch.mmd](assets/examples/microservice-arch.mmd) | Full microservices architecture example |
| [assets/examples/sequence-api.mmd](assets/examples/sequence-api.mmd) | API sequence diagram example |
| [assets/examples/state-lifecycle.mmd](assets/examples/state-lifecycle.mmd) | State machine diagram example |

## Validation

Validate your diagrams before presenting:

bash
# Validate single file
scripts/validate-mmd assets/examples/microservice-arch.mmd

# Validate all examples
scripts/validate-mmd assets/examples/*.mmd