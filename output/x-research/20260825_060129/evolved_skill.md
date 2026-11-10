---
category: software-development
description: General-purpose X/Twitter research agent. Searches X for real-time perspectives, dev discussions, product feedback, cultural takes, breaking news, and expert opinions. Works like a web research agent but uses X as the source.
name: x-research
---

---
name: x-research
version: 1.0.0
description: >
  General-purpose X/Twitter research agent. Searches X for real-time perspectives,
  dev discussions, product feedback, cultural takes, breaking news, and expert opinions.
  Works like a web research agent but uses X as the source.

  Use when:
  - User says "x research", "search x for", "search twitter for", "what are people saying about",
    "what's twitter saying", "check x for", "x search", "/x-research"
  - User is working on something where recent X discourse would provide useful context
    (new library releases, API changes, product launches, cultural events, industry drama)
  - User wants to find what devs/experts/community thinks about a topic

  NOT for: posting tweets, account management, or historical archive searches beyond 7 days.
---

# X Research

General-purpose agentic research over X/Twitter. Decompose any research question into targeted searches, iteratively refine, follow threads, deep-dive linked content, and synthesize into a sourced briefing.

For X API details (endpoints, operators, response format): read `references/x-api.md`.

## CLI Tool

All commands run from the skill directory:

bash
cd ~/clawd/skills/x-research
source ~/.config/env/global.env
### Search

bash
bun run x-search.ts search "<query>" [options]
#### Options

| Flag | Description | Default |
|------|-------------|---------|
| `--sort` | Sort order: `likes`, `impressions`, `retweets`, `recent` | `likes` |
| `--since` | Time filter: `30m`, `1h`, `3h`, `12h`, `1d`, `7d` or ISO timestamp | `7d` |
| `--min-likes N` | Filter by minimum likes | — |
| `--min-impressions N` | Filter by minimum impressions | — |
| `--pages N` | Pages to fetch (1-5, 100 tweets/page) | `1` |
| `--limit N` | Max results to display | `15` |
| `--from <username>` | Filter by author (shorthand for `from:username`) | — |
| `--no-replies` | Exclude replies from results | `false` |
| `--save` | Save results to `~/clawd/drafts/x-research-{slug}-{date}.md` | `false` |
| `--json` | Raw JSON output | `false` |
| `--markdown` | Markdown output for research docs | `false` |
| `--quality` | Filter low-engagement tweets (≥10 likes, post-hoc) | `false` |
| `--quick` | Quick mode with noise filtering and 1hr cache | `false` |

#### Quick Mode

The `--quick` flag enables fast reconnaissance:
- Fetches 1 page (100 tweets max)
- Auto-applies noise filter (`-is:retweet -is:reply`)
- Limits output to top 10 results
- 1-hour cache for repeat queries
- Displays cost summary

#### Notes

- Automatically adds `-is:retweet` unless query already includes it
- All searches display estimated API cost
- Results can be saved directly to markdown for research documentation

#### Examples

bash
# Basic search for trending discussion
bun run x-search.ts search "BNKR" --sort likes --limit 10

# Find recent tweets from specific user
bun run x-search.ts search "from:frankdegods" --sort recent

# Quick mode for fast reconnaissance
bun run x-search.ts search "rust 2.0 release" --quick

# Research with time filter
bun run x-search.ts search "openai announcement" --since 1d --sort recent

# High-quality signal (engagement threshold)
bun run x-search.ts search "typescript tips" --quality --limit 20

# Save results for later reference
bun run x-search.ts search "vercel update" --since 7d --save

# Dev-focused research
bun run x-search.ts search "nextjs app router migration" --min-likes 50

# JSON for programmatic use
bun run x-search.ts search "bun runtime" --json --limit 50
## Workflow

1. **Decompose** — Break the research question into targeted search queries
2. **Search** — Run initial searches with appropriate filters (time range, engagement threshold)
3. **Refine** — Iterate based on results; follow interesting threads, adjust queries
4. **Synthesize** — Compile findings into a sourced briefing with links and key quotes