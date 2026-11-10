---
category: software-development
name: x-research
description: 'General-purpose X/Twitter research agent. Searches X for real-time perspectives, dev discussions, product feedback, cultural takes, breaking news, and expert opinions. Works like a web research agent but uses X as the source.'
version: 1.0.0
---

# X Research

Agentic research over X/Twitter. Decompose research questions into targeted searches, iteratively refine, follow threads, deep-dive linked content, and synthesize into a sourced briefing.

## When to Use

**Direct triggers:**
- "x research", "search x for", "search twitter for"
- "what are people saying about", "what's twitter saying"
- "check x for", "x search", "/x-research"

**Implicit triggers** (X discourse would provide useful context):
- New library releases, API changes, product launches
- Cultural events, industry drama, breaking news
- Finding what devs/experts/community thinks about a topic

**NOT for:** posting tweets, account management, or historical archive searches beyond 7 days.

## Setup

All commands run from the skill directory:

bash
cd ~/clawd/skills/x-research
source ~/.config/env/global.env
For API details (endpoints, operators, response format): see `references/x-api.md`.

## Search Command

bash
bun run x-search.ts search "<query>" [options]
### Filtering Options

| Option | Description | Default |
|--------|-------------|---------|
| `--sort` | Sort by `likes`, `impressions`, `retweets`, or `recent` | likes |
| `--since` | Time range: `30m`, `1h`, `3h`, `12h`, `1d`, `7d`, or ISO timestamp | 7d |
| `--min-likes N` | Minimum likes required | none |
| `--min-impressions N` | Minimum impressions required | none |
| `--from <username>` | Filter by author (shorthand for `from:username`) | none |
| `--no-replies` | Exclude reply threads | include replies |

### Output Options

| Option | Description |
|--------|-------------|
| `--pages N` | Pages to fetch (1-5, default: 1, 100 tweets/page) |
| `--limit N` | Max results to display (default: 15) |
| `--json` | Raw JSON output |
| `--markdown` | Markdown format for research docs |
| `--save` | Save results to `~/clawd/drafts/x-research-{slug}-{date}.md` |

### Quick Mode

bash
bun run x-search.ts search "<query>" --quick
Applies automatically: 1 page, max 10 results, noise filter (`-is:retweet -is:reply`), 1hr cache, shows API cost.

### Quality Mode

bash
bun run x-search.ts search "<query>" --quality
Post-hoc filter for ≥10 likes (removes low-engagement tweets).

### Notes

- Auto-adds `-is:retweet` unless query already includes it
- All searches display estimated API cost

## Examples

**Basic searches:**
bash
bun run x-search.ts search "BNKR" --sort likes --limit 10
bun run x-search.ts search "from:frankdegods" --sort recent
**Time-filtered:**
bash
bun run x-search.ts search "React 19" --since 3h --limit 20
bun run x-search.ts search "open source drama" --since 12h --quality
**Deep research:**
bash
bun run x-search.ts search "Claude API" --since 7d --pages 3 --limit 50 --save