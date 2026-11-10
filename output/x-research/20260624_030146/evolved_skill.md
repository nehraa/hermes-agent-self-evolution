---
category: software-development
name: x-research
description: >
  General-purpose X/Twitter research agent. Searches X for real-time perspectives,
  dev discussions, product feedback, cultural takes, breaking news, and expert opinions.
  Works like a web research agent but uses X as the source.
  Use when: (1) user says "x research", "search x for", "search twitter for",
  "what are people saying about", "what's twitter saying", "check x for", "x search",
  "/x-research", (2) user is working on something where recent X discourse would provide
  useful context (new library releases, API changes, product launches, cultural events,
  industry drama), (3) user wants to find what devs/experts/community thinks about a topic.
  NOT for: posting tweets, account management, or historical archive searches beyond 7 days.
---
# X Research

General-purpose agentic research over X/Twitter. Decompose any research question into targeted searches, iteratively refine, follow threads, deep-dive linked content, and synthesize into a sourced briefing.

For X API details (endpoints, operators, response format): read `references/x-api.md`.

## Setup

All commands run from this skill directory:

bash
cd ~/clawd/skills/x-research
source ~/.config/env/global.env
## CLI Tool

### Search

bash
bun run x-search.ts search "<query>" [options]
**Arguments:**
- `<query>` — Search query string (supports X operators like `from:username`, `lang:en`, etc.)

**Options:**

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--sort` | `likes`, `impressions`, `retweets`, `recent` | `likes` | Sort order |
| `--since` | `30m`, `1h`, `3h`, `12h`, `1d`, `7d` or ISO timestamp | `7d` | Time filter |
| `--min-likes` | number | — | Minimum likes threshold |
| `--min-impressions` | number | — | Minimum impressions threshold |
| `--pages` | 1-5 | `1` | Pages to fetch (100 tweets/page) |
| `--limit` | number | `15` | Max results to display |
| `--from` | username | — | Shorthand for `from:username` |
| `--quality` | — | — | Filter low-engagement tweets (≥10 likes, post-hoc) |
| `--no-replies` | — | — | Exclude reply tweets |
| `--save` | — | — | Save results to `~/clawd/drafts/x-research-{slug}-{date}.md` |
| `--json` | — | — | Raw JSON output |
| `--markdown` | — | — | Markdown output for research docs |

**Quick Mode (`--quick`):**
- Fetches 1 page, max 10 results
- Auto noise filter: `-is:retweet -is:reply`
- 1-hour cache
- Cost summary displayed

**Auto-behavior:**
- Adds `-is:retweet` unless already included in query
- Displays estimated API cost for all searches

## Examples

bash
# Find popular tweets about BNKR
bun run x-search.ts search "BNKR" --sort likes --limit 10

# Search a specific user's tweets
bun run x-search.ts search "from:frankdegods" --sort recent --limit 20

# Recent dev discussions with quality filter
bun run x-search.ts search "Next.js 15" --since 3h --quality --limit 25

# Quick research with time constraint
bun run x-search.ts search "API breaking change" --quick --since 1d

# Find tweets with high engagement
bun run x-search.ts search "typescript" --min-likes 50 --min-impressions 1000

# Save results for documentation
bun run x-search.ts search "claude agent" --sort likes --limit 30 --save

# JSON output for scripting
bun run x-search.ts search "open source" --json --pages 2
## X Search Operators

Use these in your query for precise filtering:

- `from:username` — Tweets from specific user
- `to:username` — Tweets replying to user
- `@username` — Tweets mentioning user
- `"exact phrase"` — Exact match
- `lang:en` — Language filter
- `-filter:retweets` — Exclude retweets
- `-filter:replies` — Exclude replies

## Limitations

- **NOT for:** posting tweets, account management, or historical archive searches beyond 7 days
- Results limited to X's 7-day search index
- High-volume searches may hit rate limits