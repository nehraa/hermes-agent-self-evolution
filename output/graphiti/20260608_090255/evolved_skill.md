---
category: software-development
name: graphiti
description: Query and manage a knowledge graph using Graphiti's REST API. Search facts, add episodes, and extract entities/relationships from stored graph data.
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

Interact with a knowledge graph via Graphiti's REST API. Store episodes, extract entities and relationships, and search for relevant facts using hybrid graph + vector search.

## Prerequisites

| Service | Purpose | Default Port |
|---------|---------|--------------|
| Neo4j | Graph storage (nodes, relationships) | 7687 |
| Qdrant | Vector search (embeddings) | 6333 |
| Graphiti | REST API gateway | 8001 |

## Base URL Configuration

Graphiti uses a three-tier discovery mechanism to locate the service:

1. **Bot config** (highest priority): `bot config get skills.graphiti.baseUrl`
2. **Environment variable**: `$GRAPHITI_URL`
3. **Default fallback**: `http://localhost:8001`

Set a custom URL:

bash
# Option 1: Environment variable (session-scoped)
export GRAPHITI_URL="http://10.0.0.10:8001"

# Option 2: Bot config (persistent)
bot config set skills.graphiti.baseUrl "http://10.0.0.10:8001"
## Tools

### graphiti_search

Search the knowledge graph for facts matching a query. Uses vector similarity + graph traversal to find relevant information.

**Parameters:**

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `query` | string | Yes | — | Natural language search query |
| `max_facts` | integer | No | 10 | Maximum number of facts to return |

**Request:**

bash
GRAPHITI_URL=$({baseDir}/references/env-check.sh)
curl -s -X POST "$GRAPHITI_URL/facts/search" \
  -H 'Content-Type: application/json' \
  -d '{"query": "YOUR_QUERY", "max_facts": 10}' | jq .
**Response format:**

json
{
  "facts": [
    {
      "subject": "string",
      "object": "string",
      "predicate": "string",
      "episode": "string",
      "confidence": 0.95,
      "source_date": "2024-01-15T10:30:00Z"
    }
  ]
}
---

### graphiti_add

Add a new episode (memory) to the knowledge graph. Graphiti automatically extracts entities, relationships, and facts from the content.

**Parameters:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Human-readable identifier for the episode |
| `content` | string | Yes | Text content to process and store |

**Request:**

bash
GRAPHITI_URL=$({baseDir}/references/env-check.sh)
curl -s -X POST "$GRAPHITI_URL/messages" \
  -H 'Content-Type: application/json' \
  -d '{"name": "EPISODE_NAME", "content": "EPISODE_CONTENT"}' | jq .
**Response format:**

json
{
  "episode_id": "uuid-string",
  "name": "Episode Name",
  "status": "processing",
  "entities_extracted": 5,
  "relationships_extracted": 3
}
## Examples

### Search for facts about a person

bash
GRAPHITI_URL=$({baseDir}/references/env-check.sh)
curl -s -X POST "$GRAPHITI_URL/facts/search" \
  -H 'Content-Type: application/json' \
  -d '{"query": "Tell me about Essam Masoudy", "max_facts": 5}'
### Store a project update

bash
GRAPHITI_URL=$({baseDir}/references/env-check.sh)
curl -s -X POST "$GRAPHITI_URL/messages" \
  -H 'Content-Type: application/json' \
  -d '{"name": "Project Update", "content": "Completed Phase 1 of Bot integration with Neo4j"}'
### Search with higher result count

bash
GRAPHITI_URL=$({baseDir}/references/env-check.sh)
curl -s -X POST "$GRAPHITI_URL/facts/search" \
  -H 'Content-Type: application/json' \
  -d '{"query": "What decisions were made about the API design?", "max_facts": 20}'
## Troubleshooting

**Connection refused:**

- Verify Graphiti is running: `curl http://localhost:8001/health`
- Check Docker containers: `docker ps | grep graphiti`

**Empty search results:**

- Ensure episodes have been added first via `graphiti_add`
- Try a broader query or lower `max_facts`

**Neo4j/Qdrant errors:**

- Verify both services are running and accessible
- Check connection strings in Graphiti configuration