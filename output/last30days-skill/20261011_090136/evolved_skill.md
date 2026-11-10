---
category: software-development
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

Deep research across Reddit, X/Twitter, YouTube, TikTok, Instagram, Hacker News, Polymarket, Bluesky, Truth Social, and the web — synthesizing the last 30 days into grounded, cited reports.

---

## What It Does

Queries 10+ platforms simultaneously to surface:

- **Discussions** — What people are debating on Reddit, X, Bluesky, Truth Social
- **Recommendations** — What tools, products, or content platforms are promoting
- **Market Signals** — What Polymarket bettors believe is most likely
- **Tech Sentiment** — Hacker News submissions and comments on emerging tech
- **Video Trends** — YouTube and TikTok content gaining traction
- **Web Coverage** — Latest articles, press releases, and news

AI synthesizes all findings into a structured report with citations.

---

## Usage

**Basic research query:**

/last30 AI video generation tools
**Research a product or service:**

/last30 best project management software 2024
**Track a trend or news story:**

/last30 OpenAI latest announcement
---

## Data Sources

| Source | Type | Notes |
|--------|------|-------|
| Reddit | Discussions, recommendations | Subreddit aggregation |
| X/Twitter | Real-time trends, opinions | Requires `AUTH_TOKEN`/`CT0` for extended access |
| YouTube | Video trends, reviews | Trending content |
| TikTok | Viral content | Platform trends |
| Instagram | Social buzz | Content engagement |
| Hacker News | Tech discussions | Startup/developer sentiment |
| Polymarket | Prediction markets | Crowd wisdom on outcomes |
| Bluesky | Emerging discourse | Requires `BSKY_APP_PASSWORD` |
| Truth Social | Alternative platform views | Requires `TRUTHSOCIAL_TOKEN` |
| Web | News, articles, press | Brave search fallback |

---

## Required Setup

### Required Environment Variables

| Variable | Purpose |
|----------|---------|
| `SCRAPECREATORS_API_KEY` | Primary API key for data collection |

### Optional Environment Variables

| Variable | Purpose | When Needed |
|----------|---------|-------------|
| `OPENAI_API_KEY` | AI synthesis model | Default synthesis |
| `XAI_API_KEY` | Alternative AI provider | No OpenAI key |
| `OPENROUTER_API_KEY` | Alternative AI provider | No OpenAI/XAI key |
| `PARALLEL_API_KEY` | Parallel data fetching | Faster collection |
| `BRAVE_API_KEY` | Web search fallback | Default web search |
| `APIFY_API_TOKEN` | Extended scraping | Advanced scraping needs |
| `AUTH_TOKEN` / `CT0` | X/Twitter auth tokens | Extended X search |
| `BSKY_HANDLE` / `BSKY_APP_PASSWORD` | Bluesky credentials | Bluesky search |
| `TRUTHSOCIAL_TOKEN` | Truth Social bearer token | Truth Social search |

---

## Security & Permissions

- **Data Access**: Reads public content only from listed platforms
- **X/Twitter Access**: Uses optional user-provided `AUTH_TOKEN`/`CT0` — token lifecycle managed by user
- **Bluesky Access**: Optional app password from bsky.app/settings/app-passwords — scoped to search only
- **Truth Social Access**: Optional bearer token extractable from browser dev tools
- **Data Writes**: Optional research briefings saved to `~/Documents/Last30Days/`
- **Credentials**: Never shared, stored locally, used only for respective platform APIs

---

## Output Format

The AI synthesizes all collected data into:

1. **Executive Summary** — Key findings in 3-5 bullet points
2. **Platform Breakdown** — What each source revealed
3. **Emerging Themes** — Cross-platform patterns
4. **Citations** — Direct links to sources
5. **Sentiment Analysis** — Positive, negative, neutral breakdown where applicable

---

## Requirements

- **Node.js** — For platform-specific scrapers
- **Python 3** — For data processing and AI synthesis
- **Bash** — For orchestration scripts