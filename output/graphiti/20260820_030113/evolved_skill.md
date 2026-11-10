---
category: software-development
name: graphiti
description: Knowledge graph operations via Graphiti API. Search facts, add episodes, extract entities and relationships, and retrieve conversation context from your Neo4j-backed knowledge graph.
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

Query and manage your knowledge graph using Graphiti's REST API. Search for facts, add episodic memories, and extract entities and relationships from your Neo4j-backed graph with Qdrant vector search.

## Prerequisites

| Service | Purpose | Default |
|---------|---------|---------|
| Neo4j | Graph storage (nodes, relationships) | localhost:7474 |
| Qdrant | Vector similarity search | localhost:6333 |
| Graphiti | REST API server | localhost:8001 |

## Configuration

Graphiti URL is resolved in this order of priority:

1. **Bot config**: `bot config get skills.graphiti.baseUrl`
2. **Environment variable**: `$GRAPHITI_URL`
3. **Default fallback**: `http://localhost:8001`

Set a custom URL:

bash
# Environment variable
export GRAPHITI_URL="http://10.0.0.10:8001"

# Or persist via bot config
bot config set skills.graphiti.baseUrl "http://10.0.0.10:8001"
## Tools

### graphiti_search

Search the knowledge graph for facts matching a natural language query.

**Parameters:**

| Field | Type | Description |
|-------|------|-------------|
| `query` | string | Natural language search query |
| `max_facts` | integer | Maximum facts to return (default: 10) |
| `workspace_id` | string | Optional workspace filter |

**Request:**

bash
GRAPHITI_URL=$({baseDir}/references/env-check.sh)
curl -s -X POST "$GRAPHITI_URL/facts/search" \
  -H 'Content-Type: application/json' \
  -d '{"query": "YOUR_QUERY", "max_facts": 10}' | jq .
**Example:**

bash
GRAPHITI_URL=$({baseDir}/references/env-check.sh)
curl -s -X POST "$GRAPHITI_URL/facts/search" \
  -H 'Content-Type: application/json' \
  -d '{"query": "Tell me about Essam Masoudy", "max_facts": 5}'
---

### graphiti_add

Add a new episode (memory) to the knowledge graph. Graphiti automatically extracts entities and relationships and stores them in Neo4j with vector embeddings in Qdrant.

**Parameters:**

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Episode identifier/name |
| `content` | string | Text content to process and store |
| `workspace_id` | string | Optional workspace assignment |

**Request:**

bash
GRAPHITI_URL=$({baseDir}/references/env-check.sh)
curl -s -X POST "$GRAPHITI_URL/messages" \
  -H 'Content-Type: application/json' \
  -d '{"name": "EPISODE_NAME", "content": "EPISODE_CONTENT"}' | jq .
**Example:**

bash
GRAPHITI_URL=$({baseDir}/references/env-check.sh)
curl -s -X POST "$GRAPHITI_URL/messages" \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Project Update",
    "content": "Completed Phase 1 of Bot integration. Essam Masoudy reviewed the API endpoints and approved the architecture."
  }'
## API Endpoints Reference

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `POST` | `/facts/search` | Search for factual information |
| `POST` | `/messages` | Add a new episode/memory |
| `GET` | `/health` | Check service health |
| `GET` | `/workspaces` | List available workspaces |

## Workflow Example

1. **Add context**: When important information is shared, store it:
   ```bash
   graphiti_add "Customer Feedback" "User requested export to CSV format"
   ```

2. **Search context**: Later, retrieve relevant facts:
   ```bash
   graphiti_search "What export formats were requested?"
   ```

3. **Build conversation memory**: Chain episodes for context:
   ```bash
   graphiti_add "Meeting Notes" "Discussed CSV export feature with engineering team"
   graphiti_add "Design Review" "Approved CSV export UI mockup"