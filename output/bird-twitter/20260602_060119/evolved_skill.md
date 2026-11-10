---
name: bird-twitter
description: Twitter/X CLI wrapper using bird — post tweets, reply, read, search, and manage your timeline. Fast GraphQL-based X CLI.
category: software-development
version: 1.0.0
author: cyzi
tags: [twitter, x, tweet, social, timeline, search]
metadata: {"openclaw":{"emoji":"🐦","skillKey":"bird-twitter","primaryEnv":"AUTH_TOKEN","requires":{"bins":["bird"],"env":["AUTH_TOKEN","CT0"]}}}
---

# Bird Twitter Skill 🐦

A fast CLI wrapper for Twitter/X using the `bird` tool. Post tweets, reply to threads, read timelines, search content, and manage your social presence via Twitter's GraphQL API.

**Requires:** `bird` binary | **Auth:** `AUTH_TOKEN` + `CT0` cookies

---

## Setup

### 1. Install bird

bash
# Check if bird is available
which bird

# Install via your package manager (example)
go install github.com/your-bird-repo/cmd/bird@latest
### 2. Get Authentication Tokens

1. Log into [twitter.com](https://twitter.com) in your browser
2. Open DevTools (F12 or right-click → Inspect)
3. Navigate to **Application** tab → **Cookies** → `twitter.com`
4. Copy these values:

| Cookie | Environment Variable |
|--------|---------------------|
| `auth_token` | `AUTH_TOKEN` |
| `ct0` | `CT0` |

### 3. Configure Environment

bash
# Add to your shell profile (~/.bashrc, ~/.zshrc, etc.)
export AUTH_TOKEN="<your_auth_token_value>"
export CT0="<your_ct0_value>"
### 4. Verify Credentials

bash
# Check if you're logged in
bird whoami

# Check if tokens are available
bird check
---

## Quick Reference

### Posting Content

bash
# Post a text tweet
bird tweet "Hello world!"

# Post with images (up to 4)
bird tweet "Check out this photo" --media ./photo.jpg

# Post a reply to a tweet
bird reply https://twitter.com/user/status/123456789 "Great point!"

# Quote tweet
bird quote https://twitter.com/user/status/123456789 "My thoughts exactly"
### Reading Content

bash
# Read a single tweet
bird read https://twitter.com/user/status/123456789

# Read as JSON (useful for scripting)
bird read https://twitter.com/user/status/123456789 --json

# View full thread
bird thread https://twitter.com/user/status/123456789

# List all replies to a tweet
bird replies https://twitter.com/user/status/123456789

# Get user's recent tweets
bird user-tweets username

# Get user's likes
bird likes username
### Timelines & Notifications

bash
# Home timeline (For You feed)
bird home

# Mentions (replies to you)
bird mentions

# Your liked tweets
bird likes

# Your bookmarks
bird bookmarks
### Search & Discovery

bash
# Search for tweets
bird search "programming tips"

# Trending topics
bird trending

# News from Explore
bird news

# Search users
bird search-users "developer"
### Social Actions

bash
# Follow a user
bird follow username

# Unfollow a user
bird unfollow username

# Like a tweet
bird like https://twitter.com/user/status/123456789

# Unlike a tweet
bird unlike https://twitter.com/user/status/123456789

# Retweet
bird retweet https://twitter.com/user/status/123456789
---

## Command Reference

### Posting Commands

| Command | Description |
|---------|-------------|
| `bird tweet <text>` | Post a new text tweet |
| `bird tweet <text> --media <path>` | Post with media (max 4 images or 1 video) |
| `bird reply <url> <text>` | Reply to a specific tweet |
| `bird quote <url> <text>` | Quote tweet with comment |
| `bird delete <url>` | Delete your tweet |

### Reading Commands

| Command | Description |
|---------|-------------|
| `bird read <url>` | Display tweet content |
| `bird read <url> --json` | Output raw JSON data |
| `bird thread <url>` | Show complete conversation thread |
| `bird replies <url>` | List all replies to a tweet |
| `bird user-tweets <handle>` | Fetch recent tweets from a user |
| `bird user-info <handle>` | Get user profile information |

### Timeline Commands

| Command | Description |
|---------|-------------|
| `bird home` | Your "For You" home timeline |
| `bird mentions` | Tweets that mention you |
| `bird likes` | Tweets you've liked |
| `bird bookmarks` | Your saved tweets |

### Discovery Commands

| Command | Description |
|---------|-------------|
| `bird search <query>` | Search tweets by keyword |
| `bird search-users <query>` | Search for users |
| `bird trending` | Current trending topics |
| `bird news` | AI-curated news feed |

### Social Commands

| Command | Description |
|---------|-------------|
| `bird follow <username>` | Follow a user |
| `bird unfollow <username>` | Unfollow a user |
| `bird like <url>` | Like a tweet |
| `bird unlike <url>` | Unlike a tweet |
| `bird retweet <url>` | Retweet |
| `bird unretweet <url>` | Remove retweet |

---

## Tips & Troubleshooting

### Media Upload

- **Images:** Up to 4 images per tweet, JPEG/PNG/WebP supported
- **Video:** Single video up to 140 seconds (requires additional upload step)
- Use `--media` flag with file path(s)

### Rate Limiting

- Twitter's GraphQL API has rate limits
- Avoid rapid sequential commands
- If errors occur, wait a few minutes before retrying

### Common Issues

| Problem | Solution |
|---------|----------|
| `bird whoami` fails | Verify `AUTH_TOKEN` and `CT0` are set correctly |
| Media upload fails | Check file size limits and format support |
| Commands timeout | Check your internet connection |
| "Unauthorized" errors | Your session may have expired; re-authenticate |

### Session Maintenance

The `ct0` token expires periodically. If commands start failing:

1. Clear cookies in browser
2. Log into twitter.com fresh
3. Copy new `auth_token` and `ct0` values
4. Update environment variables and source your profile

---

## Automation Examples

### Post via Cron

bash
# Add to crontab: post daily status
0 9 * * * export AUTH_TOKEN="..." && export CT0="..." && bird tweet "Good morning! Time for coffee ☕"
### Scripted Thread

bash
# Post a thread programmatically
bird tweet "Here's a thread about coding:"
sleep 2
bird reply <first-tweet-url> "Let's start with basics..."
sleep 2
bird reply <second-tweet-url> "Now let's dive deeper..."
### Parse Tweet Data

bash
# Get tweet as JSON for processing
tweet_json=$(bird read https://twitter.com/user/status/123456789 --json)
echo "$tweet_json" | jq '.text'