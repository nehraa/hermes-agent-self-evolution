---
category: software-development
name: x-research
description: General-purpose X/Twitter research agent for finding real-time perspectives, dev discussions, product feedback, cultural takes, breaking news, and expert opinions.
version: 1.0.0
---

# X Research

Research agent for X/Twitter. Decompose research questions into targeted searches, iteratively refine results, follow threads, deep-dive linked content, and synthesize into a sourced briefing.

## When to Use

| Trigger | Examples |
|---------|----------|
| Explicit request | "x research", "search x for", "search twitter for", "/x-research" |
| Topic research | "what's twitter saying about...", "what are people saying about..." |
| Dev/product context | New library releases, API changes, product launches, industry drama |

## When NOT to Use

- Posting tweets or managing accounts
- Historical archive searches beyond 7 days
- General web research (use a web search agent instead)

For API details, endpoints, and operators: read `references/x-api.md`.

---

## Quick Start

bash
cd ~/clawd/skills/x-research
source ~/.config/env/global.env
---

## Search Command

bash
bun run x-search.ts search "<query>" [options]
### Filter Options

| Option | Description | Default |
|--------|-------------|---------|
| `--sort` | Sort by `likes`, `impressions`, `retweets`, or `recent` | `likes` |
| `--since` | Time filter: `1h`, `3h`, `12h`, `1d`, `7d`, `30m`, or ISO timestamp | `7d` |
| `--min-likes N` | Minimum likes required | none |
| `--min-impressions N` | Minimum impressions required | none |
| `--from <username>` | Filter by author (equivalent to `from:username` in query) | none |

### Pagination & Output

| Option | Description | Default |
|--------|-------------|---------|
| `--pages N` | Number of pages to fetch (1-5, 100 tweets/page) | `1` |
| `--limit N` | Maximum results to display | `15` |
| `--no-replies` | Exclude reply threads | false |
| `--save` | Save results to `~/clawd/drafts/x-research-{slug}-{date}.md` | false |
| `--json` | Output raw JSON | false |
| `--markdown` | Output markdown format for research docs | false |

### Quick Mode

bash
bun run x-search.ts search "<query>" --quick
Quick mode enables:
- 1 page fetch (100 tweets)
- Max 10 results displayed
- Auto noise filter (`-is:retweet -is:reply`)
- 1-hour cache
- API cost summary

### Quality Filter

bash
bun run x-search.ts search "<query>" --quality
Post-hoc filter that removes tweets with fewer than 10 likes.

### Notes

- Automatically adds `-is:retweet` unless the query already includes it
- All searches display estimated API cost
- Use `--markdown` when embedding results into research documents

---

## Examples

### Basic Searches

bash
# Find popular tweets mentioning a topic
bun run x-search.ts search "BNKR" --sort likes --limit 10

# Recent discussions only
bun run x-search.ts search "react server components" --sort recent --since 1d

# Tweets from a specific user
bun run x-search.ts search "from:frankdegods" --sort recent
### Research Workflows

bash
# Find expert opinions with high engagement
bun run x-search.ts search "typescript 5.0" --sort likes --min-likes 50 --quality

# Track a breaking topic over 12 hours
bun run x-search.ts search "api outage" --since 12h --sort recent --pages 2

# Build a research document
bun run x-search.ts search "ai coding tools" --sort likes --limit 20 --markdown --save
---

## Tips

1. **Iterate and refine** — Start broad, then add `--min-likes` or `--quality` to filter signal from noise
2. **Follow threads** — Use `--no-replies` to focus on top-level tweets, or remove it to see discussions
3. **Deep-dive** — Check linked content from high-engagement tweets for fuller context
4. **Save often** — Use `--save` to build a research archive over time
5. **Check costs** — Monitor API cost estimates, especially with `--pages 3` or higher