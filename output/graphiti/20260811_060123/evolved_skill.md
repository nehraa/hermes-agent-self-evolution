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
      - id: "docker"
        kind: "docker-compose"
        label: "Install Graphiti stack (Docker)"
---

# Graphiti Knowledge Graph

Query and manage a Neo4j-backed knowledge graph using Graphiti's REST API. Search for facts, add episodic memories, and retrieve extracted entities and relationships.

## Prerequisites

| Service | Purpose | Default Port |
|---------|---------|--------------|
| Neo4j | Graph storage (nodes, relationships) | 7687 (Bolt), 7474 (HTTP) |
| Qdrant | Vector similarity search | 6333 |
| Graphiti | REST API service | 8001 |

## Tools

### `graphiti_search`

Search the knowledge graph for facts matching a natural language query. Uses vector similarity to find relevant episodes and their extracted facts.

**Parameters:**
| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `query` | string | Yes | - | Natural language search query |
| `max_facts` | integer | No | 10 | Maximum facts to return |

**Request Example:**
bash
curl -s -X POST "${GRAPHITI_URL}/facts/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "Tell me about Essam Masoudy", "max_facts": 5}' | jq .
**Response Format:**
json
{
  "results": [
    {
      "fact": "Essam Masoudy is a software architect",
      "episode_name": "Meeting Notes 2024-01-15",
      "confidence": 0.92,
      "entities": ["Essam Masoudy", "Software Architect"]
    }
  ]
}
---

### `graphiti_add`

Add a new episodic memory to the knowledge graph. The content is automatically processed to extract entities, relationships, and facts.

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Unique identifier/title for the episode |
| `content` | string | Yes | The memory content to process |

**Request Example:**
bash
curl -s -X POST "${GRAPHITI_URL}/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Project Update 2024-01-15",
    "content": "Completed Phase 1 of Bot integration. Team lead is Essam Masoudy."
  }' | jq .
**Response Format:**
json
{
  "episode_id": "abc123",
  "name": "Project Update 2024-01-15",
  "facts_extracted": 3,
  "entities_found": ["Bot", "Phase 1", "Essam Masoudy", "Team Lead"]
}
---

## Dynamic Service Discovery

The skill automatically locates the Graphiti service using this priority chain:

1. **Bot config** — `bot config get skills.graphiti.baseUrl`
2. **Environment variable** — `$GRAPHITI_URL`
3. **Default fallback** — `http://localhost:8001`

### Viewing Current Configuration

bash
# Check environment variable
echo $GRAPHITI_URL

# Check bot config
bot config get skills.graphiti.baseUrl

# Verify service is reachable
curl -s http://localhost:8001/health | jq .
### Updating the Graphiti URL

bash
# Set via environment variable (session-scoped)
export GRAPHITI_URL="http://10.0.0.10:8001"

# Set via bot config (persistent)
bot config set skills.graphiti.baseUrl "http://10.0.0.10:8001"
---

## Common Workflows

### Search Before Adding

Always search for existing facts to avoid duplicate episodes:

bash
curl -s -X POST "${GRAPHITI_URL}/facts/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "Essam Masoudy", "max_facts": 5}'
### Add Meeting Notes

bash
curl -s -X POST "${GRAPHITI_URL}/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Standup 2024-01-15",
    "content": "Discussed Q1 roadmap. Key decision: adopt Graphiti for memory management."
  }' | jq .
### Query Recent Facts

bash
curl -s -X POST "${GRAPHITI_URL}/facts/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "What decisions were made in January?", "max_facts": 10}' | jq .
---

## Error Handling

| Error Code | Meaning | Resolution |
|------------|---------|------------|
| `ECONNREFUSED` | Graphiti not running | Check Docker containers: `docker ps` |
| `404` | Endpoint not found | Verify Graphiti version supports the endpoint |
| `400` | Invalid request body | Check JSON syntax and required fields |
| `500` | Internal error | Check Graphiti logs: `docker logs graphiti` |