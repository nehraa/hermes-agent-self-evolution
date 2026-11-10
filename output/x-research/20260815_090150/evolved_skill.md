---
category: software-development
name: x-research
description: >
  General-purpose X/Twitter research agent. Searches X for real-time perspectives,
  dev discussions, product feedback, cultural takes, breaking news, and expert opinions.
  Works like a web research agent but uses X as the source.
---

# X Research

General-purpose agentic research over X/Twitter. Decompose any research question into targeted searches, iteratively refine, follow threads, deep-dive linked content, and synthesize into a sourced briefing.

For X API details (endpoints, operators, response format): read `references/x-api.md`.

## Quick Start

bash
cd ~/clawd/skills/x-research
source ~/.config/env/global.env
## Usage

### Basic Search

bash
bun run x-search.ts search "<query>" [options]
### Search Options

| Option | Description | Default |
|--------|-------------|---------|
| `--sort` | Sort by `likes`, `impressions`, `retweets`, or `recent` | `likes` |
| `--since` | Time filter: `30m`, `1h`, `3h`, `12h`, `1d`, `7d`, or ISO timestamp | `7d` |
| `--min-likes N` | Minimum likes to include | — |
| `--min-impressions N` | Minimum impressions to include | — |
| `--pages N` | Pages to fetch (1-5, 100 tweets/page) | `1` |
| `--limit N` | Max results to display | `15` |
| `--from <username>` | Filter by author (shorthand for `from:username`) | — |
| `--quality` | Filter tweets with ≥10 likes post-fetch | — |
| `--no-replies` | Exclude replies from results | — |
| `--save` | Save to `~/clawd/drafts/x-research-{slug}-{date}.md` | — |
| `--json` | Output raw JSON | — |
| `--markdown` | Output formatted markdown for research docs | — |
| `--quick` | Fast mode: 1 page, 10 results, auto noise filter, 1hr cache | — |

**Auto-filters:**
- `-is:retweet` added automatically unless already in query
- Estimated API cost displayed for every search

## Examples

**Search by keyword:**
bash
bun run x-search.ts search "BNKR" --sort likes --limit 10
**Search from specific user:**
bash
bun run x-search.ts search "from:frankdegods" --sort recent
**Quick research burst:**
bash
bun run x-search.ts search "swordship game" --quick
**Detailed research with quality filter:**
bash
bun run x-search.ts search "llama.cpp updates" --since 1d --quality --limit 30 --save
**Find recent discussions with minimum engagement:**
bash
bun run x-search.ts search "rust async" --since 3h --min-likes 5 --sort recent
## When to Use

**Activate when user says:**
- "x research", "search x for", "search twitter for"
- "what are people saying about", "what's twitter saying"
- "check x for", "x search", "/x-research"

**Activate when researching:**
- New library releases or API changes
- Product launches and feedback
- Industry drama or cultural events
- Developer discussions and expert opinions

## Limitations

- **NOT** for: posting tweets, account management, or historical archive searches beyond 7 days
- **NOT** for: bulk data export or archival research