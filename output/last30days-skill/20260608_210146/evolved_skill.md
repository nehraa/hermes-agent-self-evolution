---
category: software-development
description: "Deep research engine covering the last 30 days across 10+ sources - Reddit, X/Twitter, YouTube, TikTok, Instagram, Hacker News, Polymarket, Bluesky, Truth Social, web. AI synthesizes findings into grounded, cited reports. The most comprehensive recency research skill on ClawHub."
name: last30days-skill
---

---
name: last30days
version: "2.9.5"
description: "Deep research engine covering the last 30 days across 10+ sources - Reddit, X/Twitter, YouTube, TikTok, Instagram, Hacker News, Polymarket, Bluesky, Truth Social, web. AI synthesizes findings into grounded, cited reports. The most comprehensive recency research skill on ClawHub."
argument-hint: 'last30 AI video tools, last30 best project management tools'
allowed-tools: Bash, Read, Write, AskUserQuestion, WebSearch
homepage: https://github.com/mvanhorn/last30days-skill
repository: https://github.com/mvanhorn/last30days-skill
author: mvanhorn
license: MIT
user-invocable: true
metadata:
  openclaw:
    emoji: "📰"
    requires:
      env:
        - SCRAPECREATORS_API_KEY
      optionalEnv:
        - OPENAI_API_KEY
        - XAI_API_KEY
        - OPENROUTER_API_KEY
        - PARALLEL_API_KEY
        - BRAVE_API_KEY
        - APIFY_API_TOKEN
        - AUTH_TOKEN
        - CT0
        - BSKY_HANDLE
        - BSKY_APP_PASSWORD
        - TRUTHSOCIAL_TOKEN
      bins:
        - node
        - python3
    primaryEnv: SCRAPECREATORS_API_KEY
    files:
      - "scripts/*"
    homepage: https://github.com/mvanhorn/last30days-skill
    tags:
      - research
      - deep-research
      - reddit
      - x
      - twitter
      - youtube
      - tiktok
      - instagram
      - hackernews
      - polymarket
      - bluesky
      - truthsocial
      - trends
      - recency
      - news
      - citations
      - multi-source
      - social-media
      - analysis
      - web-search
      - ai-skill
      - clawhub
---

# last30days v2.9.5

## Deep Research Across the Last 30 Days

Research any topic across **10+ sources** — Reddit, X/Twitter, YouTube, TikTok, Instagram, Hacker News, Polymarket, Bluesky, Truth Social, and the broader web. Surface what people are discussing, recommending, betting on, and debating right now. AI synthesizes findings into grounded, cited reports.

---

## Overview

`last30days` is a comprehensive recency research engine designed to answer the question: **"What's happening with [topic] right now?"**

It searches multiple platforms simultaneously, aggregates results from the past 30 days, and uses AI to synthesize findings into a cohesive briefing with source citations.

### Use Cases

- **Product research:** Find the latest tools, trends, and discussions
- **Market intelligence:** Track what's being debated and adopted
- **Competitive analysis:** Monitor industry conversations across platforms
- **News tracking:** Go beyond traditional news to capture grassroots sentiment
- **Trend identification:** Discover emerging topics before they go mainstream

---

## Usage

### Basic Invocation

last30 <topic>
Prefix your query with `last30` to activate the skill:

last30 AI video tools
last30 best project management tools
last30 llama 4 release date
last30 open source llm trends
### What Happens

1. **Multi-source search:** Queries Reddit, X/Twitter, YouTube, TikTok, Instagram, Hacker News, Polymarket, Bluesky, Truth Social, and web sources simultaneously
2. **30-day window:** All results filtered to the last 30 days for recency
3. **AI synthesis:** Results are analyzed, deduplicated, and synthesized into a structured report
4. **Source citations:** Every finding links back to original sources

---

## Sources & Coverage

| Source | Coverage | Token Required |
|--------|----------|----------------|
| **Reddit** | Subreddit search, trending discussions | None |
| **X/Twitter** | Real-time posts, trends, hashtags | Optional (AUTH_TOKEN/CT0) |
| **YouTube** | Video titles, descriptions, comments | None |
| **TikTok** | Video titles, descriptions, trending | None |
| **Instagram** | Post captions, trending content | None |
| **Hacker News** | Discussion threads, comments | None |
| **Polymarket** | Prediction markets, sentiment data | None |
| **Bluesky** | Posts, trending topics | Optional (BSKY_APP_PASSWORD) |
| **Truth Social** | Posts, trending | Optional (TRUTHSOCIAL_TOKEN) |
| **Web** | News sites, blogs, forums | BRAVE_API_KEY |

---

## Environment Variables

### Required

| Variable | Description |
|----------|-------------|
| `SCRAPECREATORS_API_KEY` | Primary API key for multi-source scraping |

### Optional - AI Models

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | OpenAI GPT models for synthesis |
| `XAI_API_KEY` | xAI (Grok) models |
| `OPENROUTER_API_KEY` | Access to multiple AI providers |
| `PARALLEL_API_KEY` | Parallel proxy for AI calls |

### Optional - Search & Access

| Variable | Description |
|----------|-------------|
| `BRAVE_API_KEY` | Enhanced web search via Brave Search API |
| `APIFY_API_TOKEN` | Alternative scraping platform |

### Optional - Platform Authentication

| Variable | Description |
|----------|-------------|
| `AUTH_TOKEN` | X/Twitter session token (for enhanced search) |
| `CT0` | X/Twitter CSRF token |
| `BSKY_HANDLE` | Bluesky handle/username |
| `BSKY_APP_PASSWORD` | Bluesky app password (create at bsky.app/settings/app-passwords) |
| `TRUTHSOCIAL_TOKEN` | Truth Social bearer token (extract from browser dev tools) |

---

## Security & Permissions

### What the Skill Does

| Action | Data Accessed | Location |
|--------|---------------|----------|
| **Read** | Public posts, comments, videos, web pages | All listed platforms |
| **Write** | Research briefings (optional) | `~/Documents/Last30Days/` |

### Platform-Specific Notes

**X/Twitter Search:**
- Works without tokens using basic search
- Optional `AUTH_TOKEN` and `CT0` enable enhanced search capabilities
- Tokens are extracted from browser session (never shared or transmitted externally)

**Bluesky:**
- Optional `BSKY_APP_PASSWORD` enables Bluesky search
- Create app-specific password at bsky.app/settings/app-passwords (no 2FA required for this)
- Does not grant posting or message permissions

**Truth Social:**
- Optional `TRUTHSOCIAL_TOKEN` enables Truth Social search
- Extract bearer token from browser dev tools when logged into Truth Social
- Token is used only for authenticated API requests to Truth Social

### Data Handling

- All data stays local during processing
- Source URLs are preserved for citation and verification
- No data is shared with third parties
- Research briefings saved locally if output option is chosen

---

## Output Format

The skill generates a structured research report containing:

# [Topic] - Last 30 Days Research Report

## Executive Summary
[AI-synthesized overview of key findings]

## Key Discussions
[Aggregated themes from multiple sources]

## Platform Breakdown
### Reddit
[Top discussions, sentiment, key points]
### X/Twitter
[Trending posts, hashtags, key voices]
### Hacker News
[Technical discussions, debates]
### [Other platforms...]

## Predictions & Sentiment
[Polymarket data, community sentiment]

## Sources
[Hyperlinked citations to all referenced content]
---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No results from X/Twitter | Add `AUTH_TOKEN` and `CT0` to environment |
| Bluesky search failing | Verify `BSKY_APP_PASSWORD` is valid; regenerate at bsky.app |
| Truth Social not returning results | Check `TRUTHSOCIAL_TOKEN` is still valid; refresh from browser |
| Web search limited | Add `BRAVE_API_KEY` for enhanced web coverage |
| Rate limiting | Wait and retry; reduce query frequency |

---

## Examples

**Research emerging AI tools:**
last30 emerging AI coding tools 2024
**Track a product launch:**
last30 apple vision pro reception
**Monitor industry debate:**
last30 react vs vue 2024
**Find betting sentiment:**
last30 trump election odds
**Track alternative platform discussions:**
last30 bitcoin truth social
---

## Installation & Setup

1. Set required environment variable:
   ```bash
   export SCRAPECREATORS_API_KEY=your_api_key_here
   ```

2. Optionally configure AI providers:
   ```bash
   export OPENAI_API_KEY=your_openai_key  # or XAI_API_KEY, OPENROUTER_API_KEY, etc.
   ```

3. Optionally add platform tokens for enhanced search:
   ```bash
   export AUTH_TOKEN=your_x_token
   export CT0=your_ct0_token
   export BSKY_APP_PASSWORD=your_bluesky_password
   export TRUTHSOCIAL_TOKEN=your_truth_social_token
   ```

---

## Dependencies

- **node** - JavaScript runtime for scripts
- **python3** - Python runtime for processing

---

## License

MIT License - See [repository](https://github.com/mvanhorn/last30days-skill) for details.