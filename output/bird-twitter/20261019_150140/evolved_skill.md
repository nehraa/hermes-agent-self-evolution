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

A fast, lightweight Twitter/X CLI wrapper using `bird`. Post tweets, reply to threads, read conversations, search content, and manage your entire timeline — all through Twitter's GraphQL API.

## Prerequisites

### Required Binaries

- **`bird`** — Install from [github.com/nicoco007/bird](https://github.com/nicoco007/bird) or via your package manager

### Required Environment Variables

| Variable | Source | Description |
|----------|--------|-------------|
| `AUTH_TOKEN` | Cookie `auth_token` | Main authentication token |
| `CT0` | Cookie `ct0` | CSRF protection token |

bash
export AUTH_TOKEN=<your_twitter_auth_token>
export CT0=<your_twitter_ct0_cookie>
### Obtaining Your Tokens

1. Open [twitter.com](https://twitter.com) in your browser and log in
2. Press **F12** to open Developer Tools
3. Navigate to **Application** tab → **Cookies** → `twitter.com`
4. Copy the following values:
   - `auth_token` → set as `AUTH_TOKEN`
   - `ct0` → set as `CT0`

> **Note:** These tokens expire periodically. Re-extract them if commands start returning authentication errors.

---

## Quick Reference

bash
# Verify setup
bird whoami              # Check logged-in account
bird check              # Validate credentials

# Posting
bird tweet "Hello!"     # Post a new tweet
bird reply <url> "Text" # Reply to a tweet
bird tweet "..." --media /path/to/image.jpg

# Reading
bird read <url>         # Fetch a tweet
bird thread <url>       # View full conversation thread
bird replies <url>      # List replies to a tweet

# Content Discovery
bird home               # Home timeline (For You feed)
bird mentions           # Tweets mentioning you
bird likes              # Your liked tweets
bird bookmarks          # Your saved bookmarks
bird search "query"     # Search tweets
bird user-tweets <handle>  # User's recent tweets
bird news               # Trending news from Explore
bird trending           # Trending topics

# Social Actions
bird follow <username>  # Follow a user
---

## Commands Reference

### Account & Status

| Command | Description |
|---------|-------------|
| `bird whoami` | Display logged-in account info |
| `bird check` | Verify `AUTH_TOKEN` and `CT0` are valid |

### Posting Content

| Command | Description |
|---------|-------------|
| `bird tweet <text>` | Post a new tweet |
| `bird reply <url> <text>` | Reply to a tweet (use tweet URL or ID) |
| `bird tweet <text> --media <path>` | Tweet with image(s) or video (max 4 images or 1 video) |

**Examples:**

bash
# Simple tweet
bird tweet "Just shipped a new feature!"

# Reply with context
bird reply https://twitter.com/user/status/123 "Great insights, thanks for sharing!"

# Tweet with image
bird tweet "Check out this screenshot!" --media ./screenshot.png
### Reading & Viewing

| Command | Description |
|---------|-------------|
| `bird read <url>` | Fetch and display a single tweet |
| `bird read <url> --json` | Output tweet data as JSON |
| `bird thread <url>` | Display full conversation/thread |
| `bird replies <url>` | List all replies to a tweet |
| `bird user-tweets <handle>` | View recent tweets from a user |

**Examples:**

bash
# Read a tweet
bird read 1234567890

# Get full thread
bird thread https://twitter.com/user/status/123

# Output as JSON for scripting
bird read 1234567890 --json

# View someone's tweets
bird user-tweets @username
### Timelines & Notifications

| Command | Description |
|---------|-------------|
| `bird home` | Home timeline (For You feed) |
| `bird mentions` | Tweets that mention or reply to you |
| `bird likes` | Tweets you've liked |
| `bird bookmarks` | Your saved bookmarks |

### Search & Discovery

| Command | Description |
|---------|-------------|
| `bird search <query>` | Search tweets by keyword or phrase |
| `bird news` | AI-curated trending news from Explore |
| `bird trending` | Current trending topics worldwide |
| `bird follow <username>` | Follow a user by handle (without @) |

**Examples:**

bash
# Search for tweets
bird search "open source cli tools"

# Follow a user
bird follow username

# Check what's trending
bird trending
---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `Error: not authenticated` | Re-extract `AUTH_TOKEN` and `CT0` from browser cookies |
| `Error: rate limited` | Wait a few minutes and retry; avoid rapid successive requests |
| Media upload fails | Ensure file is ≤ 5MB for images or ≤ 15MB for video |
| Empty timeline results | Your account may be set to "Protect your tweets" |

---

## Tips

- **Use tweet URLs or numeric IDs** — Both work with `read`, `reply`, `thread`, and `replies`
- **JSON output for automation** — Pipe `--json` output to `jq` for powerful scripting
- **Protect your tokens** — Never commit `AUTH_TOKEN` or `CT0` to version control