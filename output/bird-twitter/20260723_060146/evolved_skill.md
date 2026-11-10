---
category: software-development
name: bird-twitter
description: Twitter/X CLI wrapper using bird — post tweets, reply, read, search, and manage your timeline. Fast GraphQL-based X CLI.
version: 1.0.0
author: cyzi
tags: [twitter, x, tweet, social, timeline, search]
metadata:
  openclaw:
    emoji: "🐦"
    skillKey: "bird-twitter"
    primaryEnv: "AUTH_TOKEN"
    requires:
      bins: ["bird"]
      env: ["AUTH_TOKEN", "CT0"]
---

# Bird Twitter Skill 🐦

Fast Twitter/X CLI wrapper using `bird` — post tweets, reply, read, search, and manage your timeline via Twitter's GraphQL API.

## Prerequisites

### Required Tools

- [`bird`](https://github.com/nicholasbird/bird) — Install before using this skill

### Required Environment Variables

bash
export AUTH_TOKEN=<your_twitter_auth_token>
export CT0=<your_twitter_ct0_cookie>
> **Important:** Both `AUTH_TOKEN` and `CT0` are required for authentication.

## Getting Your Tokens

1. Log in to [twitter.com](https://twitter.com) in your browser
2. Open Developer Tools (`F12` or `Cmd+Option+I` on Mac)
3. Navigate to **Application** tab → **Cookies** → `twitter.com`
4. Copy the following values:
   - `auth_token` cookie → `AUTH_TOKEN`
   - `ct0` cookie → `CT0`

### Verify Your Setup

bash
# Check if you're logged in
bird whoami

# Check credential availability
bird check
## Core Commands

### Posting Tweets

| Command | Description |
|---------|-------------|
| `bird tweet "Your message"` | Post a new tweet |
| `bird reply <tweet-id-or-url> "Your reply"` | Reply to a specific tweet |
| `bird tweet "Text" --media /path/to/image.jpg` | Tweet with image (up to 4) |
| `bird tweet "Text" --video /path/to/video.mp4` | Tweet with video |

### Reading Tweets

| Command | Description |
|---------|-------------|
| `bird read <tweet-id-or-url>` | Fetch and display a tweet |
| `bird read <url> --json` | Output tweet data as JSON |
| `bird thread <url>` | Show full conversation thread |
| `bird replies <url>` | List all replies to a tweet |
| `bird user-tweets <handle>` | Get recent tweets from a user |

### Timeline & Notifications

| Command | Description |
|---------|-------------|
| `bird home` | Your home timeline ("For You" feed) |
| `bird mentions` | Tweets that mention you |
| `bird likes` | Your liked tweets |
| `bird bookmarks` | Your bookmarked tweets |

### Search & Discovery

| Command | Description |
|---------|-------------|
| `bird search "query"` | Search for tweets |
| `bird news` | AI-curated news from Explore tab |
| `bird trending` | Currently trending topics |

### Social Actions

| Command | Description |
|---------|-------------|
| `bird follow <username>` | Follow a user |
| `bird unfollow <username>` | Unfollow a user |
| `bird like <tweet-id-or-url>` | Like a tweet |
| `bird unlike <tweet-id-or-url>` | Unlike a tweet |
| `bird retweet <url>` | Retweet a tweet |
| `bird share <url>` | Share/bookmark a tweet |

## Quick Usage Examples

bash
# Post a simple tweet
bird tweet "Hello from bird-twitter skill! 🐦"

# Reply to someone
bird reply https://twitter.com/user/status/123456 "Great point!"

# Read a tweet
bird read 1234567890

# Search for tweets
bird search "open source"

# Check what's trending
bird trending

# Get news
bird news

# View a user's tweets
bird user-tweets elonmusk

# Follow someone
bird follow username
## Common Workflows

### Finding a Tweet ID

Many commands accept either a full URL or just the numeric tweet ID:

bash
# Both work:
bird read https://twitter.com/user/status/1234567890123456789
bird read 1234567890123456789
### Formatting Output

Some commands support JSON output for scripting:

bash
bird read 123456 --json | jq '.text'
## Troubleshooting

| Issue | Solution |
|-------|----------|
| `bird whoami` shows not logged in | Re-export your `AUTH_TOKEN` and `CT0` values |
| Missing CT0 error | Ensure both `AUTH_TOKEN` and `CT0` are set |
| Tweet fails to post | Check your internet connection and rate limits |
| Command not found | Ensure `bird` is installed and in your PATH |

## Notes

- Tokens expire periodically — re-authenticate if commands start failing
- Rate limits apply to certain operations
- Some features require a Twitter/X account with appropriate permissions