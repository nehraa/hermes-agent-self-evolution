---
name: bird-twitter
description: Twitter/X CLI wrapper using bird — post tweets, reply, read, search, and manage your timeline. Fast GraphQL-based X CLI.
version: 1.0.0
author: cyzi
tags: [twitter, x, tweet, social, timeline, search]
metadata: {"openclaw":{"emoji":"🐦","skillKey":"bird-twitter","primaryEnv":"AUTH_TOKEN","requires":{"bins":["bird"],"env":["AUTH_TOKEN","CT0"]}}}
---

# Bird Twitter Skill 🐦

Fast Twitter/X CLI wrapper using `bird` — post tweets, reply, read, search, and manage your timeline via Twitter's GraphQL API.

## Prerequisites

### Required Environment Variables

bash
export AUTH_TOKEN=<your_twitter_auth_token>
export CT0=<your_twitter_ct0_cookie>
**Important:** Both `AUTH_TOKEN` and `CT0` are required for authentication.

### Obtaining Your Tokens

1. Log in to [twitter.com](https://twitter.com) in your browser
2. Open Developer Tools (`F12` or right-click → Inspect)
3. Navigate to **Application** (Chrome) or **Storage** (Firefox) → **Cookies** → `twitter.com`
4. Copy the following values:
   - `auth_token` → set as `AUTH_TOKEN`
   - `ct0` → set as `CT0`

> **Security Note:** These tokens grant full account access. Store them securely and never commit them to version control.

---

## Quick Start

bash
# Verify authentication is working
bird whoami

# Check if credentials are properly set
bird check

# Post your first tweet
bird tweet "Hello from bird-twitter!"

# Read a tweet by URL or ID
bird read https://twitter.com/user/status/1234567890

# Search for tweets
bird search "open source"

# View your home timeline
bird home
---

## Commands Reference

### Authentication & Status

| Command | Description |
|---------|-------------|
| `bird whoami` | Display authenticated user info |
| `bird check` | Verify `AUTH_TOKEN` and `CT0` are set correctly |

### Posting Content

| Command | Description |
|---------|-------------|
| `bird tweet <text>` | Post a new tweet (max 280 chars) |
| `bird reply <url-or-id> <text>` | Reply to a specific tweet |
| `bird tweet <text> --media <path>` | Tweet with up to 4 images or 1 video |

**Examples:**
bash
bird tweet "Just shipped a new feature! 🚀"
bird reply 1234567890 "Great point, thanks for sharing!"
bird tweet "Check out this screenshot" --media ./screenshot.png
### Reading & Viewing

| Command | Description |
|---------|-------------|
| `bird read <url-or-id>` | Fetch and display a single tweet |
| `bird read <url-or-id> --json` | Output tweet data as JSON |
| `bird thread <url-or-id>` | Display full conversation thread |
| `bird replies <url-or-id>` | List all replies to a tweet |
| `bird user-tweets <handle>` | Get recent tweets from a user |
| `bird user <handle>` | Get user profile information |

**Examples:**
bash
bird read 1234567890
bird read https://twitter.com/elonmusk/status/1234567890 --json
bird thread 1234567890
bird user-tweets openai
### Timelines & Feeds

| Command | Description |
|---------|-------------|
| `bird home` | Home timeline ("For You" feed) |
| `bird mentions` | Tweets mentioning you (@username) |
| `bird likes` | Your liked/saved tweets |
| `bird bookmarks` | Your bookmarked tweets |

### Search & Discovery

| Command | Description |
|---------|-------------|
| `bird search <query>` | Search tweets by keyword or phrase |
| `bird news` | AI-curated news from Explore tab |
| `bird trending` | Currently trending topics worldwide |

**Examples:**
bash
bird search "rust programming"
bird search "from:github since:2024-01-01"
bird search "#OpenSource" --limit 50
### Social Actions

| Command | Description |
|---------|-------------|
| `bird follow <username>` | Follow a user |
| `bird unfollow <username>` | Unfollow a user |
| `bird like <url-or-id>` | Like/favorite a tweet |
| `bird unlike <url-or-id>` | Unlike a tweet |
| `bird retweet <url-or-id>` | Retweet a tweet |
| `bird quote <url-or-id> <text>` | Quote tweet with comment |

---

## Common Workflows

### Posting a Thread

bash
bird tweet "🧵 Here's a thread about best practices..."
bird reply <first-tweet-id> "1/ Let's start with the basics"
bird reply <second-tweet-id> "2/ Now let's dive deeper"
### Engaging with Content

bash
# Like multiple tweets from search results
bird search "tech news" | xargs -I {} bird like {}

# Quote tweet with your thoughts
bird quote 1234567890 "Agreed! Adding my take on this..."
### Monitoring Your Account

bash
# Check mentions regularly
bird mentions

# Review your liked tweets
bird likes

# View who's talking about you
bird search "to:yourusername"
---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `Error: Not authenticated` | Run `bird check` to verify tokens are set |
| `Error: Token expired` | Refresh cookies in browser and update `AUTH_TOKEN` and `CT0` |
| `Error: Rate limited` | Wait a few minutes; Twitter limits API calls |
| `Empty results` | Try different search terms or check if account is private |

### Debug Mode

bash
# Enable verbose output
DEBUG=bird bird tweet "test"

# Check the underlying API calls
DEBUG=api bird home