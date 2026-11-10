---
name: graphiti
description: Knowledge graph operations via Graphiti API. Search facts, add episodes, and extract entities/relationships.
category: software-development
metadata:
  bot:
    emoji: "🕸️"
    requires:
      services:
        - neo4j
        - qdrant
        - graphiti
    install:
      - id: docker
        kind: docker-compose
        label: Install Graphiti stack (Docker)
homepage: https://github.com/getzep/graphiti
---

# Graphiti Knowledge Graph

Query and manage a Neo4j-backed knowledge graph with Qdrant vector search via Graphiti's REST API.

## Prerequisites

| Service | Purpose | Default Port |
|---------|---------|--------------|
| Neo4j | Graph storage (nodes, relationships) | 7474 |
| Qdrant | Vector similarity search | 6333 |
| Graphiti | REST API layer | 8001 |

Ensure all services are running before use. Graphiti must be accessible at the configured URL.

## Tools

### `graphiti_search`

Search the knowledge graph for facts matching a natural language query.

**Endpoint:** `POST /facts/search`

**Parameters:**

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `query` | string | Yes | — | Natural language search query |
| `max_facts` | integer | No | 10 | Maximum number of facts to return |

**Response:** Returns an array of fact objects with source episodes, confidence scores, and extracted entities.

**Example:**
bash
GRAPHITI_URL="${GRAPHITI_URL:-http://localhost:8001}"
curl -s -X POST "${GRAPHITI_URL}/facts/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "Tell me about Essam Masoudy", "max_facts": 5}' | jq .
---

### `graphiti_add`

Add a new episode (memory) to the knowledge graph. Graphiti will automatically extract entities and relationships.

**Endpoint:** `POST /messages`

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Identifier/title for the episode |
| `content` | string | Yes | Text content to process and store |

**Response:** Returns the created episode with extracted metadata.

**Example:**
bash
GRAPHITI_URL="${GRAPHITI_URL:-http://localhost:8001}"
curl -s -X POST "${GRAPHITI_URL}/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Project Update",
    "content": "Completed Phase 1 of Bot integration with Graphiti. User confirmed the entity extraction is working correctly."
  }' | jq .
---

## Configuration

Graphiti URL resolution (in priority order):

1. **Bot config:** `bot config get skills.graphiti.baseUrl`
2. **Environment variable:** `$GRAPHITI_URL`
3. **Default fallback:** `http://localhost:8001`

**Set a custom URL:**

bash
# Via environment variable (session-scoped)
export GRAPHITI_URL="http://10.0.0.10:8001"

# Via bot config (persistent)
bot config set skills.graphiti.baseUrl "http://10.0.0.10:8001"
---

## Workflow Example

1. Add episode → graphiti_add
   └── Stores raw content, triggers entity extraction

2. Search facts → graphiti_search
   └── Queries extracted facts with vector similarity
**Use case:** After a conversation, store key information with `graphiti_add`. Later, retrieve relevant context with `graphiti_search` to maintain continuity across sessions.

---

## Common Patterns

**Bulk add from log entries:**
bash
for entry in "Task A completed" "Task B started" "Bug fixed in module X"; do
  curl -s -X POST "${GRAPHITI_URL}/messages" \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"log-$(date +%s)\", \"content\": \"$entry\"}"
done
**Semantic search with relaxed results:**
bash
curl -s -X POST "${GRAPHITI_URL}/facts/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "anything related to project deadlines", "max_facts": 20}'