---
category: software-development
name: last30days-skill
description: "Deep research engine covering the last 30 days across 10+ sources - Reddit, X/Twitter, YouTube, TikTok, Instagram, Hacker News, Polymarket, Bluesky, Truth Social, web. AI synthesizes findings into grounded, cited reports. The most comprehensive recency research skill on ClawHub."
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

Research any topic from the last 30 days across 10+ sources.

## Overview

**last30days** is a deep research engine that aggregates trending discussions, news, and insights from multiple platforms into a single, cited synthesis report.

### Supported Sources

| Platform | Content Type | Auth Required |
|----------|--------------|---------------|
| Reddit | Discussions, recommendations, AMAs | No |
| X/Twitter | Trends, opinions, viral posts | Optional |
| YouTube | Commentary, reviews, tutorials | No |
| TikTok | Viral content, trends | No |
| Instagram | Trends, influencer content | No |
| Hacker News | Tech discussions, startup news | No |
| Polymarket | Market predictions, betting trends | No |
| Bluesky | Emerging discussions | Optional |
| Truth Social | Alternative perspectives | Optional |
| Web | News, articles, blogs | No |

### Features

- **Multi-source aggregation** — Simultaneous search across all platforms
- **AI synthesis** — Combines findings into a coherent, cited report
- **30-day recency filter** — Focuses on the latest discussions and trends
- **Source attribution** — Every claim linked to original posts/sources
- **Platform-specific insights** — Tailored analysis per source type

## Usage

### Basic Invocation

last30 <topic>
**Examples:**

bash
last30 AI video generation tools
last30 best project management software 2024
last30 react framework trends
last30 customer service automation
### Output Format

The research report includes:

1. **Executive Summary** — Key findings at a glance
2. **Platform Breakdown** — What each source is saying
3. **Consensus Points** — Where platforms agree
4. **Diverging Opinions** — Contradicting viewpoints
5. **Trending Sentiment** — Overall community mood
6. **Citations** — Direct links to all referenced posts

## Security & Permissions

### Required Environment

| Variable | Purpose | Required |
|----------|---------|----------|
| `SCRAPECREATORS_API_KEY` | Core API for content aggregation | **Yes** |

### Optional Environment Variables

| Variable | Platform | Purpose |
|----------|----------|---------|
| `OPENAI_API_KEY` | AI synthesis | Better language generation |
| `XAI_API_KEY` | X/Twitter search | Enhanced Twitter queries |
| `OPENROUTER_API_KEY` | Model routing | Alternative AI provider |
| `PARALLEL_API_KEY` | Parallel processing | Faster results |
| `BRAVE_API_KEY` | Web search | Additional web coverage |
| `APIFY_API_TOKEN` | Data extraction | Backup scraping |

### Platform-Specific Authentication

#### X/Twitter

bash
AUTH_TOKEN=<your_token>
CT0=<your_ct0_token>
Extract these from browser cookies when logged into Twitter/X.

#### Bluesky

bash
BSKY_HANDLE=<your_handle.bsky.social>
BSKY_APP_PASSWORD=<app_password>
Generate at [bsky.app/settings/app-passwords](https://bsky.app/settings/app-passwords).

#### Truth Social

bash
TRUTHSOCIAL_TOKEN=<bearer_token>
Extract from browser DevTools network tab.

### Data Access & Storage

| Action | Scope | Location |
|--------|-------|----------|
| Read | Public platform data | Via API/scraping |
| Read | Public web content | Via search APIs |
| Write | Research briefings (optional) | `~/Documents/Last30Days/` |

All writes require explicit user confirmation. No personal data is collected or stored.

## Installation

bash
# Clone the repository
git clone https://github.com/mvanhorn/last30days-skill.git

# Install dependencies
cd last30days-skill/scripts
npm install  # or python3 -m pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys
## Troubleshooting

| Issue | Solution |
|-------|----------|
| No results from X/Twitter | Ensure `AUTH_TOKEN` and `CT0` are set |
| Bluesky auth fails | Verify handle format (must end in `.bsky.social`) |
| Empty Polymarket results | Check if event trading volume is low |
| Rate limiting | Add `BRAVE_API_KEY` for backup web search |

## Contributing

Contributions welcome! See [GitHub repository](https://github.com/mvanhorn/last30days-skill) for guidelines.