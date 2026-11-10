---
category: software-development
name: graphiti
description: Knowledge graph operations via Graphiti API. Search facts, add episodes, and extract entities/relationships.
homepage: https://github.com/getzep/graphiti
metadata:
  bot:
    emoji: "🕸️"
    requires:
      services: ["neo4j", "qdrant", "graphiti"]
    install:
      - id: docker
        kind: docker-compose
        label: Install Graphiti stack (Docker)
---

# Graphiti Knowledge Graph

Query and manage a knowledge graph using Graphiti's REST API with automatic service discovery.

## Prerequisites

- **Neo4j** — Graph database for storing entities and relationships
- **Qdrant** — Vector database for semantic search
- **Graphiti service** — REST API (default: `http://localhost:8001`)

## Tools

### `graphiti_search`

Search the knowledge graph for facts matching a natural language query.

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | string | Yes | — | Natural language search query |
| `max_facts` | integer | No | 10 | Maximum number of facts to return |

**Request:**
bash
curl -s -X POST "http://localhost:8001/facts/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "What are Essam Masoudy's key contributions?", "max_facts": 5}'
**Response:**
json
{
  "facts": [
    {
      "id": "fact_001",
      "content": "Essam Masoudy developed the Graphiti knowledge graph architecture",
      "entities": ["Essam Masoudy", "Graphiti"],
      "confidence": 0.95
    }
  ]
}
### `graphiti_add`

Add new episodes or memories to the knowledge graph.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `name` | string | Yes | Identifier for this episode |
| `content` | string | Yes | The memory content to store |
| `entities` | array | No | Specific entities to extract |
| `relationships` | array | No | Explicit relationships to create |

**Request:**
bash
curl -s -X POST "http://localhost:8001/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Team Meeting 2024-01-15",
    "content": "Discussed roadmap and assigned tasks to team members"
  }'
**Response:**
json
{
  "id": "msg_002",
  "name": "Team Meeting 2024-01-15",
  "extracted_entities": ["roadmap", "team members"],
  "created_at": "2024-01-15T10:30:00Z"
}
## Configuration

The Graphiti URL resolves in this priority order:

1. `GRAPHITI_URL` environment variable
2. `bot config get skills.graphiti.baseUrl`
3. `http://localhost:8001` (fallback)

**Override the URL:**

bash
# Via environment variable
export GRAPHITI_URL="http://10.0.0.10:8001"

# Via bot config
bot config set skills.graphiti.baseUrl "http://10.0.0.10:8001"
## Examples

### Search for facts about a specific entity

bash
curl -s -X POST "http://localhost:8001/facts/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "Essam Masoudy", "max_facts": 5}' | jq .
### Add a project milestone

bash
curl -s -X POST "http://localhost:8001/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Phase 1 Complete",
    "content": "Successfully integrated Neo4j and Qdrant with the Graphiti API"
  }' | jq .
### Add meeting notes with context

bash
curl -s -X POST "http://localhost:8001/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Q4 Planning Meeting",
    "content": "Team agreed to prioritize Graphiti integration in Q1 2024. Sarah will lead the implementation."
  }' | jq .