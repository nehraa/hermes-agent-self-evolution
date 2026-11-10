---
category: software-development
name: last30days-skill
---

---
name: last30days
version: "2.9.5"
description: "Deep research engine covering the last 30 days across 10+ sources — Reddit, X/Twitter, YouTube, TikTok, Instagram, Hacker News, Polymarket, Bluesky, Truth Social, and the web. AI synthesizes findings into grounded, cited reports. The most comprehensive recency research skill on ClawHub."
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

# last30days

Deep research for the last 30 days across Reddit, X/Twitter, Bluesky, Truth Social, YouTube, TikTok, Instagram, Hacker News, Polymarket, and the web.

This skill surfaces what people are actually discussing, recommending, betting on, and debating right now — synthesizing findings into grounded, cited reports.

## Usage

Provide any topic to research. The skill will:

1. Search multiple platforms simultaneously for recent discussions
2. Aggregate trends, opinions, and data points
3. Synthesize findings into a cohesive, cited report

**Examples:**

last30 AI video tools
last30 best project management tools
last30 electric vehicle news
last30 startup funding trends
## Supported Sources

| Platform | Data Retrieved |
|----------|----------------|
| Reddit | Trending posts, top comments, sentiment |
| X/Twitter | Hashtag trends, viral tweets, engagement |
| YouTube | Trending videos, comment discussions |
| TikTok | Viral content, trending sounds |
| Instagram | Popular posts, trending tags |
| Hacker News | Tech discussions, YC startup mentions |
| Polymarket | Prediction markets, betting volumes |
| Bluesky | Emerging trends, viral posts |
| Truth Social | Political/trending discussions |
| Web | News articles, blog posts, forums |

## Permissions

**What this skill accesses:**
- Public web data and platform content
- Optionally saves research briefings to `~/Documents/Last30Days/`

**Platform-specific tokens (all optional):**

| Platform | Environment Variables | Setup |
|----------|----------------------|-------|
| X/Twitter | `AUTH_TOKEN`, `CT0` | Browser dev tools |
| Bluesky | `BSKY_HANDLE`, `BSKY_APP_PASSWORD` | bsky.app/settings/app-passwords |
| Truth Social | `TRUTHSOCIAL_TOKEN` | Browser dev tools |

## Required Environment

| Variable | Required | Purpose |
|----------|----------|---------|
| `SCRAPECREATORS_API_KEY` | Yes | Core scraping API access |
| `OPENAI_API_KEY` | No | Enhanced synthesis |
| `BRAVE_API_KEY` | No | Web search augmentation |
| `APIFY_API_TOKEN` | No | Additional scraping |

## Output

Research reports include:
- Key findings organized by theme
- Direct citations with source links
- Sentiment analysis and trends
- Platform-specific insights
- Confidence indicators for claims