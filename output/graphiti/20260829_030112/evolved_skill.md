---
category: software-development
name: graphiti
description: Knowledge graph operations via Graphiti API. Search facts, add episodes, and extract entities/relationships from your Neo4j-backed graph store.
homepage: https://github.com/getzep/graphiti
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
---

# Graphiti Knowledge Graph

Query and manage a Neo4j-backed knowledge graph using Graphiti's REST API with automatic service discovery.

## Prerequisites

| Service | Purpose | Default Port |
|---------|---------|--------------|
| Neo4j | Graph storage | 7474 |
| Qdrant | Vector search | 6333 |
| Graphiti | REST API | 8001 |

## Tools

### `graphiti_search`

Search the knowledge graph for facts matching a query.

**Parameters:**
- `query` (string, required) — Search query text
- `max_facts` (integer, optional) — Maximum results to return (default: 10)

**Example:**
bash
curl -s -X POST "${GRAPHITI_URL}/facts/search" \
  -H 'Content-Type: application/json' \
  -d '{"query": "Tell me about Essam Masoudy", "max_facts": 5}' | jq .
### `graphiti_add`

Add a new episode (memory) to the knowledge graph.

**Parameters:**
- `name` (string, required) — Episode identifier
- `content` (string, required) — Episode content/body

**Example:**
bash
curl -s -X POST "${GRAPHITI_URL}/messages" \
  -H 'Content-Type: application/json' \
  -d '{"name": "Project Update", "content": "Completed Phase 1 of Bot integration"}' | jq .
## Configuration

The skill discovers the Graphiti URL in this priority order:

1. **Bot config**: `skills.graphiti.baseUrl`
2. **Environment variable**: `$GRAPHITI_URL`
3. **Default fallback**: `http://localhost:8001`

**Set a custom URL:**

bash
# Via environment variable
export GRAPHITI_URL="http://10.0.0.10:8001"

# Via bot config
bot config set skills.graphiti.baseUrl "http://10.0.0.10:8001"
## Common Patterns

**Search for entity information:**
bash
curl -s -X POST "${GRAPHITI_URL}/facts/search" \
  -H 'Content-Type: application/json' \
  -d '{"query": "USER_QUERY_HERE", "max_facts": 10}' | jq .
**Store conversation or event:**
bash
curl -s -X POST "${GRAPHITI_URL}/messages" \
  -H 'Content-Type: application/json' \
  -d '{"name": "EPISODE_NAME", "content": "What happened..."}' | jq .