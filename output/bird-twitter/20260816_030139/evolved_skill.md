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

- `bird` — Install from [github.com/rapalab/bird](https://github.com/rapalab/bird)

### Required Environment Variables

| Variable | Description | Source |
|----------|-------------|--------|
| `AUTH_TOKEN` | Twitter authentication token | Cookie `auth_token` from twitter.com |
| `CT0` | CSRF token | Cookie `ct0` from twitter.com |

bash
export AUTH_TOKEN=<your_twitter_auth_token>
export CT0=<your_twitter_ct0_cookie>
### Obtaining Tokens

1. Log in to [twitter.com](https://twitter.com) in your browser
2. Open Developer Tools (`F12` or `Cmd+Option+I` on Mac)
3. Navigate to **Application** → **Cookies** → **twitter.com**
4. Copy the following cookie values:
   - `auth_token` → set as `AUTH_TOKEN`
   - `ct0` → set as `CT0`

> **Security Note**: These tokens grant full account access. Keep them secure and never commit them to version control.

## Quick Reference

bash
# Authentication & Status
bird whoami              # Check current account
bird check               # Verify credentials are available

# Posting
bird tweet "Hello world" # Post a new tweet
bird reply <url> "text"  # Reply to a tweet
bird tweet "text" --media <path>  # Tweet with media (up to 4 images or 1 video)

# Reading
bird read <url>          # Read a single tweet
bird read <url> --json   # Read with JSON output
bird thread <url>        # Show full conversation thread
bird replies <url>       # List all replies to a tweet
bird user-tweets <handle> # Get user's recent tweets

# Timelines
bird home      # Home timeline (For You feed)
bird mentions  # Tweets mentioning you
bird likes     # Your liked tweets
bird bookmarks # Your bookmarked tweets

# Search & Discovery
bird search <query>  # Search tweets
bird news           # AI-curated news from Explore
bird trending       # Trending topics
bird news           # News topics

# Social Actions
bird follow <username>   # Follow a user
bird user-tweets <handle> # Get user's tweets
## Command Reference

### Authentication Commands

| Command | Description |
|---------|-------------|
| `bird whoami` | Display current logged-in account info |
| `bird check` | Verify `AUTH_TOKEN` and `CT0` are set and valid |

### Posting Commands

| Command | Description |
|---------|-------------|
| `bird tweet <text>` | Post a new tweet |
| `bird reply <url> <text>` | Reply to a tweet (use tweet URL or ID) |
| `bird tweet <text> --media <path>` | Post tweet with media attachment |

**Media Support:**
- Up to 4 images per tweet
- 1 video per tweet
- Supported formats: PNG, JPG, GIF, MP4

### Reading Commands

| Command | Description |
|---------|-------------|
| `bird read <url>` | Fetch and display a tweet |
| `bird read <url> --json` | Output tweet data as JSON |
| `bird thread <url>` | Display full conversation thread |
| `bird replies <url>` | List all replies to a tweet |
| `bird user-tweets <handle>` | Get recent tweets from a user |

**URL Formats for `read`, `reply`, `thread`, `replies`:**
- Full URL: `https://twitter.com/user/status/123456`
- Status ID only: `123456`

### Timeline Commands

| Command | Description |
|---------|-------------|
| `bird home` | Home timeline (For You feed) |
| `bird mentions` | Tweets that mention your account |
| `bird likes` | Your liked tweets |
| `bird bookmarks` | Your bookmarked tweets |

### Search & Discovery Commands

| Command | Description |
|---------|-------------|
| `bird search <query>` | Search tweets by keyword or phrase |
| `bird trending` | Current trending topics |
| `bird news` | AI-curated news stories from Explore |

### Social Commands

| Command | Description |
|---------|-------------|
| `bird follow <username>` | Follow a user (without @ symbol) |
| `bird user-tweets <handle>` | View tweets from a specific user |

## Examples

### Post a Tweet

bash
bird tweet "Hello from bird-twitter! 🐦"
### Reply to a Tweet

bash
# Using full URL
bird reply "https://twitter.com/user/status/123456789" "Great thread! 🔥"

# Using just the tweet ID
bird reply "123456789" "Thanks for sharing!"
### Search and Read

bash
# Search for tweets
bird search "open source AI"

# Read a specific tweet
bird read "https://twitter.com/openai/status/123456789"

# Get the full thread
bird thread "https://twitter.com/developer/status/123456789"
### View Timelines

bash
# Your home feed
bird home

# Who's talking about you
bird mentions

# Check what you've liked
bird likes
### Follow and View Users

bash
# Follow a user
bird follow "openai"

# View someone's recent tweets
bird user-tweets "openai"
## Troubleshooting

### "Auth token is missing" Error

Ensure `AUTH_TOKEN` and `CT0` environment variables are exported:

bash
echo $AUTH_TOKEN   # Should show a value
echo $CT0          # Should show a value
### "Invalid credentials" Error

Your tokens may have expired. Refresh them:
1. Log out of Twitter in your browser
2. Log back in
3. Copy fresh `auth_token` and `ct0` values from browser cookies

### Tweet Not Found

- Verify the URL is correct
- Check if the tweet or account has been deleted/suspended
- Ensure the account is not private (for reading others' tweets)

### Media Upload Fails

- Verify file exists at the specified path
- Check file size: images max 5MB, videos vary by type
- Supported formats: PNG, JPG, GIF, MP4, WebM

## Notes

- Uses Twitter's internal GraphQL API for optimal speed and reliability
- All commands return exit code `0` on success, non-zero on failure
- Rate limits may apply for intensive usage patterns
- Some features require a verified Twitter account