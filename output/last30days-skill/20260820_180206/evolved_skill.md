---
category: software-development
name: last30days-skill
description: 'Deep research engine covering the last 30 days across 10+ sources - Reddit, X/Twitter, YouTube, TikTok, Instagram, Hacker News, Polymarket, Bluesky, Truth Social, web. AI synthesizes findings into grounded, cited reports. The most comprehensive recency research skill on ClawHub.'
---

---
name: last30days
version: "2.9.5"
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

Deep research engine for discovering what's happening, trending, and discussed across the internet in the last 30 days.

## What It Does

Scans 10+ platforms simultaneously and uses AI to synthesize findings into cited, grounded reports:

| Source | Content Type | Notes |
|--------|--------------|-------|
| **Reddit** | Discussions, recommendations, debates | Communities, threads, upvotes |
| **X/Twitter** | Trending topics, opinions, news | Requires optional AUTH_TOKEN/CT0 |
| **YouTube** | Video trends, commentary, reviews | Thumbnails, view counts |
| **TikTok** | Viral content, trends | Requires APIFY_API_TOKEN |
| **Instagram** | Visual trends, influencer activity | Requires APIFY_API_TOKEN |
| **Hacker News** | Tech discussions, startup news | Commentary, points |
| **Polymarket** | Prediction markets, betting sentiment | Real-money forecasting data |
| **Bluesky** | Fediverse discussions | Requires BSKY_HANDLE/BSKY_APP_PASSWORD |
| **Truth Social** | Alternative social discourse | Requires TRUTHSOCIAL_TOKEN |
| **Web** | News, blogs, general coverage | Via Brave/Parallel search APIs |

## Usage

**Argument format:** `last30 <topic>`

**Examples:**
last30 AI video tools
last30 best project management tools
last30 climate tech investments
last30 SpaceX launch controversy
last30 keto diet科学研究
The skill extracts the topic after "last30" and searches all configured sources.

## Output

Delivers structured reports with:

- **Key findings** organized by platform
- **Source citations** with direct links to posts, threads, and articles
- **Sentiment analysis** showing what people think vs. what's being bet on
- **Trend indicators** comparing engagement, predictions, and web volume
- **Research briefing file** saved to `~/Documents/Last30Days/` (optional)

## Security & Permissions

| Capability | Scope | Data Handling |
|------------|-------|---------------|
| Read public web content | Any publicly accessible URL | Not stored beyond session |
| Read platform data | Via official APIs or Scrapecreators | Processed in-memory for synthesis |
| Save briefings | `~/Documents/Last30Days/` | Optional; user-controlled |
| X/Twitter search | Optional user tokens (AUTH_TOKEN/CT0) | Scopes to read-only search |
| Bluesky access | Optional app password (bsky.app/settings/app-passwords) | Read-only |
| Truth Social access | Optional bearer token (extract from browser dev tools) | Read-only |

No data is exfiltrated. All credential storage and usage is transparent in source code.

## Required Setup

### Required Environment Variables

| Variable | Purpose |
|----------|---------|
| `SCRAPECREATORS_API_KEY` | Primary scraping API (get key at scrapecreators.com) |

### Optional Environment Variables

| Variable | Enables | Setup |
|----------|---------|-------|
| `OPENAI_API_KEY` | Better AI synthesis | platform.openai.com |
| `XAI_API_KEY` | Grok-powered analysis | x.ai |
| `OPENROUTER_API_KEY` | Alternative model routing | openrouter.ai |
| `PARALLEL_API_KEY` | Web search | parallel.ai |
| `BRAVE_API_KEY` | Web search | api.search.brave.com |
| `APIFY_API_TOKEN` | TikTok/Instagram scraping | apify.com |
| `AUTH_TOKEN` + `CT0` | X/Twitter organic search | Browser dev tools |
| `BSKY_HANDLE` + `BSKY_APP_PASSWORD` | Bluesky access | bsky.app/settings/app-passwords |
| `TRUTHSOCIAL_TOKEN` | Truth Social access | Browser dev tools (Bearer token) |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No results from a source | Check if that source requires optional env vars |
| Generic/anonymous results | Set AUTH_TOKEN/CT0 for X, or BSKY credentials for Bluesky |
| Web search returns stale results | Configure BRAVE_API_KEY or PARALLEL_API_KEY |
| Missing TikTok/Instagram content | Add APIFY_API_TOKEN |

---

**Repository:** https://github.com/mvanhorn/last30days-skill