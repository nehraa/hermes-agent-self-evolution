---
category: software-development
name: x-research
description: General-purpose X/Twitter research agent. Searches X for real-time perspectives, dev discussions, product feedback, cultural takes, breaking news, and expert opinions. Works like a web research agent but uses X as the source.
version: 1.0.0
---

# X Research

Agentic research over X/Twitter. Decompose any research question into targeted searches, iteratively refine, follow threads, deep-dive linked content, and synthesize into a sourced briefing.

## When to Use

**Trigger phrases:**
- "x research", "search x for", "search twitter for"
- "what are people saying about", "what's twitter saying"
- "check x for", "x search", "/x-research"

**Use cases:**
- Recent X discourse would provide useful context (new library releases, API changes, product launches, cultural events, industry drama)
- Finding what devs/experts/community thinks about a topic
- Real-time perspectives, breaking news, expert opinions

**NOT for:** posting tweets, account management, or historical archive searches beyond 7 days.

## CLI Tool

All commands run from the skill directory:

bash
cd ~/clawd/skills/x-research
source ~/.config/env/global.env
### Search Command

bash
bun run x-search.ts search "<query>" [options]
**Sort options:**
| Flag | Values | Default |
|------|--------|---------|
| `--sort` | `likes`, `impressions`, `retweets`, `recent` | `likes` |

**Time filters:**
| Flag | Values | Default |
|------|--------|---------|
| `--since` | `30m`, `1h`, `3h`, `12h`, `1d`, `7d`, or ISO timestamp | `7d` |

**Result filters:**
| Flag | Description |
|------|-------------|
| `--min-likes N` | Filter by minimum likes |
| `--min-impressions N` | Filter by minimum impressions |
| `--quality` | Post-hoc filter for ≥10 likes |
| `--no-replies` | Exclude replies |

**Output controls:**
| Flag | Description |
|------|-------------|
| `--pages N` | Pages to fetch (1-5, default: 1, 100 tweets/page) |
| `--limit N` | Max results to display (default: 15) |
| `--json` | Raw JSON output |
| `--markdown` | Markdown output for research docs |
| `--save` | Save results to `~/clawd/drafts/x-research-{slug}-{date}.md` |

**Query helpers:**
| Flag | Description |
|------|-------------|
| `--from <username>` | Shorthand for `from:username` |

**Quick mode:**
bash
bun run x-search.ts search "<query>" --quick
- 1 page, max 10 results
- Auto noise filter (`-is:retweet -is:reply`)
- 1hr cache
- Cost summary

### Behavior

- Auto-adds `-is:retweet` unless query already includes it
- All searches display estimated API cost

### Examples

bash
# Search for a term, top liked
bun run x-search.ts search "BNKR" --sort likes --limit 10

# Search from specific user
bun run x-search.ts search "from:frankdegods" --sort recent

# Recent posts only (last hour)
bun run x-search.ts search "rust wasm" --since 1h --sort recent

# High-engagement tweets only
bun run x-search.ts search "react server components" --quality --min-likes 50

# Save to file for later
bun run x-search.ts search "openai gpt-5" --limit 25 --save

# Quick research pulse
bun run x-search.ts search "vercel deployment" --quick
## API Reference

For X API details (endpoints, operators, response format), see `references/x-api.md`.