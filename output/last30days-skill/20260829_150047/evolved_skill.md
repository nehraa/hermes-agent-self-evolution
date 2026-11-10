---
name: last30days
version: "2.9.5"
description: "Deep research engine covering the last 30 days across Reddit, X/Twitter, YouTube, TikTok, Instagram, Hacker News, Polymarket, Bluesky, Truth Social, and the web. AI synthesizes findings into grounded, cited reports. The most comprehensive recency research skill on ClawHub."
category: software-development
allowed-tools: Bash, Read, Write, AskUserQuestion, WebSearch
author: mvanhorn
license: MIT
user-invocable: true
homepage: https://github.com/mvanhorn/last30days-skill
repository: https://github.com/mvanhorn/last30days-skill
argument-hint: 'last30 AI video tools, last30 best project management tools'
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

Deep research engine for discovering what's happening **right now** across 10+ major platforms.

## What It Does

Research any topic and get a synthesized report covering discussions, trends, recommendations, debates, and predictions from the last 30 days. The AI pulls from:

- **Social Platforms:** Reddit, X/Twitter, Bluesky, Truth Social, Instagram
- **Video:** YouTube, TikTok
- **Tech News:** Hacker News
- **Prediction Markets:** Polymarket
- **General Web:** Search results and articles

## Usage

bash
last30 <your research topic>
**Examples:**

bash
last30 AI video generation tools 2024
last30 best open source project management tools
last30 consumer AI trends
last30 startup funding news
## Output

Returns a comprehensive, cited report with:

- Key findings synthesized from all sources
- Direct links and references to sources
- Sentiment analysis from discussions
- Betting odds and predictions (from Polymarket)
- Contrasting viewpoints and debates

## Permissions & Data Access

| Source | Access Method | Optional Credential |
|--------|--------------|---------------------|
| Reddit, YouTube, TikTok, Instagram, Web | Public API/Web scraping | None required |
| X/Twitter | Search API | `AUTH_TOKEN` + `CT0` (browser cookies) |
| Bluesky | AT Protocol API | `BSKY_HANDLE` + `BSKY_APP_PASSWORD` |
| Truth Social | Web scraping | `TRUTHSOCIAL_TOKEN` (bearer token) |

**Data Storage:** Optionally saves research briefings to `~/Documents/Last30Days/`

### Setting Up Optional Credentials

**X/Twitter tokens** (`AUTH_TOKEN`, `CT0`):
1. Log into x.com in your browser
2. Open DevTools (F12) → Application → Cookies
3. Copy `auth_token` and `ct0` values

**Bluesky app password** (`BSKY_APP_PASSWORD`):
1. Go to bsky.app/settings/app-passwords
2. Create a new app password
3. Set `BSKY_HANDLE` to your username (e.g., `yourname.bsky.social`)

**Truth Social token** (`TRUTHSOCIAL_TOKEN`):
1. Log into truthsocial.com
2. Open DevTools → Network tab
3. Find any API request → copy `Authorization: Bearer <token>`

## Required Environment Variables

| Variable | Required | Purpose |
|----------|----------|---------|
| `SCRAPECREATORS_API_KEY` | **Yes** | Core API key for platform access |

## Optional Environment Variables

| Variable | Purpose |
|----------|---------|
| `OPENAI_API_KEY` | AI model for synthesis |
| `XAI_API_KEY` | Alternative AI model |
| `OPENROUTER_API_KEY` | Alternative AI model |
| `PARALLEL_API_KEY` | Alternative AI model |
| `BRAVE_API_KEY` | Enhanced web search |
| `APIFY_API_TOKEN` | Alternative scraping backend |

## Requirements

- **Node.js** (for script execution)
- **Python 3** (for data processing)

## Repository

GitHub: https://github.com/mvanhorn/last30days-skill