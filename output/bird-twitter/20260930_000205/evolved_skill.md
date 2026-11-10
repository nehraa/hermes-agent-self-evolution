---
name: bird-twitter
description: Twitter/X CLI wrapper using bird — post tweets, reply, read, search, and manage your timeline. Fast GraphQL-based X CLI.
version: 1.0.0
author: cyzi
tags: [twitter, x, tweet, social, timeline, search]
metadata: {"openclaw":{"emoji":"🐦","skillKey":"bird-twitter","primaryEnv":"AUTH_TOKEN","requires":{"bins":["bird"],"env":["AUTH_TOKEN","CT0"]}}}
---

# Bird Twitter 🐦

A fast CLI wrapper for Twitter/X using `bird` — post tweets, reply to threads, read content, search, and manage your timeline via Twitter's GraphQL API.

## Prerequisites

### Required Environment Variables

bash
export AUTH_TOKEN=<your_twitter_auth_token>
export CT0=<your_twitter_ct0_cookie>
**Without these variables, `bird` commands will fail.**

### Obtaining Your Tokens

1. Open Twitter/X in your browser and log in
2. Press `F12` to open Developer Tools
3. Navigate to **Application** → **Cookies** → `twitter.com`
4. Copy the following values:
   - `auth_token` → set as `AUTH_TOKEN`
   - `ct0` → set as `CT0`

> **Note:** These tokens expire periodically. If you encounter authentication errors, refresh your cookies and update the environment variables.

## Quick Start

bash
# Verify your login status
bird whoami

# Check if credentials are properly configured
bird check

# Post your first tweet
bird tweet "Hello from bird-twitter!"

# Read any tweet by URL or ID
bird read https://twitter.com/user/status/1234567890

# Search for tweets
bird search "OpenAI GPT-5"

# View your home timeline
bird home
## Core Commands

### Posting Content

| Command | Description |
|---------|-------------|
| `bird tweet <text>` | Post a new text tweet |
| `bird tweet <text> --media <path>` | Tweet with up to 4 images or 1 video |
| `bird reply <url> <text>` | Reply to a specific tweet |
| `bird reply <url> <text> --media <path>` | Reply with media attachment |

**Examples:**
bash
bird tweet "Just shipped a new feature! 🚀"
bird tweet "Check out this screenshot" --media ./screenshot.png
bird reply https://twitter.com/user/status/123 "Great insight! 💯"
### Reading Content

| Command | Description |
|---------|-------------|
| `bird read <url>` | Fetch and display a single tweet |
| `bird read <url> --json` | Output tweet data as JSON |
| `bird thread <url>` | Display full conversation thread |
| `bird replies <url>` | List all replies to a tweet |
| `bird user-tweets <handle>` | Get recent tweets from a user |

**Examples:**
bash
bird read 1234567890
bird read https://twitter.com/elonmusk/status/1234567890 --json
bird thread https://twitter.com/user/status/1234567890
bird user-tweets openai
### Timelines & Notifications

| Command | Description |
|---------|-------------|
| `bird home` | Your home timeline ("For You" feed) |
| `bird mentions` | Tweets that mention you |
| `bird likes` | Tweets you've liked |
| `bird bookmarks` | Your saved bookmarks |

### Search & Discovery

| Command | Description |
|---------|-------------|
| `bird search <query>` | Search for tweets matching query |
| `bird news` | AI-curated trending news from Explore |
| `bird trending` | Current trending topics |

**Examples:**
bash
bird search "#rustlang"
bird search "from:github announced"
bird news
bird trending
### Social Actions

| Command | Description |
|---------|-------------|
| `bird follow <username>` | Follow a user (without @ symbol) |
| `bird follow <username> --list <list-name>` | Follow and add to a list |
| `bird unfollow <username>` | Unfollow a user |

**Examples:**
bash
bird follow satyanadella
bird unfollow unwanted_account
## Common Workflows

### Thread Creation
bash
# Post the opening tweet
THREAD_START=$(bird tweet "Here's a thread on building CLI tools:")

# Extract the tweet ID and reply with subsequent tweets
bird reply $THREAD_START "1/ Research the problem space first"
bird reply $THREAD_START "2/ Design the interface before coding"
bird reply $THREAD_START "3/ Use established patterns (CLI framework, config formats)"
bird reply $THREAD_START "4/ Test with real users early and often"
### Engagement Tracking
bash
# Check who's mentioning you
bird mentions

# View recent likes to track engagement
bird likes

# Read replies to your tweets
bird replies https://twitter.com/your_handle/status/YOUR_TWEET_ID
## Troubleshooting

| Issue | Solution |
|-------|----------|
| `Error: Authentication failed` | Refresh `AUTH_TOKEN` and `CT0` cookies in your browser |
| `Error: Rate limit exceeded` | Wait a few minutes; Twitter imposes rate limits per endpoint |
| `Error: Media upload failed` | Ensure file is under 15MB (images) or 140MB (video) |
| `No output from command` | Verify `bird` is installed: `which bird` |

## Technical Notes

- All API calls go directly to Twitter's GraphQL endpoints (no third-party API)
- Responses are optimized for terminal display; use `--json` for programmatic access
- Rate limits vary by endpoint (typically 15-180 requests per 15-minute window)