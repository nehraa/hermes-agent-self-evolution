---
category: software-development
name: bird-twitter
description: Twitter/X CLI wrapper using bird — post tweets, reply, read, search, and manage your timeline. Fast GraphQL-based X CLI.
---

# Bird Twitter Skill 🐦

Fast Twitter/X CLI wrapper using `bird` — post tweets, reply, read, search, and manage your timeline via Twitter's GraphQL API.

## Prerequisites

- [bird](https://github.com/bird-team/bird) CLI tool installed
- Active Twitter/X account

## Required Environment Variables

Set these before using any `bird` command:

bash
export AUTH_TOKEN=<your_twitter_auth_token>
export CT0=<your_twitter_ct0_cookie>
### Obtaining Your Tokens

1. Log into [twitter.com](https://twitter.com) in your browser
2. Open Developer Tools (`F12` or right-click → Inspect)
3. Navigate to **Application** → **Cookies** → `twitter.com`
4. Copy the following values:
   - `auth_token` → `AUTH_TOKEN`
   - `ct0` → `CT0`

> **Note:** These tokens expire periodically. Re-authenticate and update them if commands start failing with authentication errors.

## Quick Reference

bash
# Authentication
bird whoami          # Verify logged-in account
bird check           # Verify credentials are valid

# Post content
bird tweet "Hello world!"                              # Post tweet
bird reply <tweet-id> "Great point!"                  # Reply to tweet
bird tweet "Check this out" --media ./image.jpg        # Tweet with media (up to 4 images or 1 video)

# Read content
bird read <tweet-id>           # View a single tweet
bird read <tweet-id> --json    # View tweet as JSON
bird thread <tweet-id>         # View full thread
bird replies <tweet-id>        # List all replies

# Timelines
bird home       # Your home feed ("For You")
bird mentions   # Tweets mentioning you
bird likes      # Your liked tweets
bird bookmarks  # Your bookmarked tweets

# Search & Discovery
bird search <query>   # Search tweets
bird news             # Trending news from Explore
bird trending         # Trending topics

# User Profiles
bird user <handle>           # View user profile
bird user-tweets <handle>    # View user's tweets
bird followers <handle>      # List user's followers
bird following <handle>      # List accounts user follows
bird follow <handle>         # Follow a user
bird unfollow <handle>       # Unfollow a user

# Notifications
bird notifications    # Your notification feed
## Commands Reference

### Posting

| Command | Description |
|---------|-------------|
| `bird tweet <text>` | Post a new tweet |
| `bird reply <id> <text>` | Reply to a tweet (ID or full URL) |
| `bird tweet <text> --media <path>` | Tweet with up to 4 images or 1 video |

### Reading

| Command | Description |
|---------|-------------|
| `bird read <id>` | Display a tweet's content |
| `bird read <id> --json` | Output tweet data as JSON |
| `bird thread <id>` | Show entire conversation thread |
| `bird replies <id>` | List all replies to a tweet |
| `bird user-tweets <handle>` | Fetch recent tweets from a user |

### Timelines

| Command | Description |
|---------|-------------|
| `bird home` | Home timeline (For You feed) |
| `bird mentions` | Tweets that mention you |
| `bird likes` | Your liked tweets collection |
| `bird bookmarks` | Your saved bookmarks |

### Search & Discovery

| Command | Description |
|---------|-------------|
| `bird search <query>` | Search for tweets matching query |
| `bird news` | AI-curated news from Explore tab |
| `bird trending` | Current trending topics |

### User Interactions

| Command | Description |
|---------|-------------|
| `bird user <handle>` | Display user profile info |
| `bird followers <handle>` | List user's followers |
| `bird following <handle>` | List accounts user follows |
| `bird follow <handle>` | Follow a user |
| `bird unfollow <handle>` | Unfollow a user |

### Notifications

| Command | Description |
|---------|-------------|
| `bird notifications` | Your notification feed |

### Utilities

| Command | Description |
|---------|-------------|
| `bird whoami` | Show current authenticated account |
| `bird check` | Validate credentials are present and valid |

## Tweet ID Extraction

You can use either:

- **Full URL**: `https://twitter.com/user/status/123456789`
- **Tweet ID only**: `123456789`

Both formats work with all read/reply commands.

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | Authentication error (check tokens) |
| `2` | Rate limited (wait before retrying) |
| `3` | Tweet not found or inaccessible |
| `4` | Network error |

## Rate Limits

Twitter imposes rate limits on most operations. If you encounter errors:

- Wait 15-60 minutes before retrying
- Reduce command frequency
- Check `bird check` to confirm your account status

---

**Version:** 1.0.0  
**Author:** cyzi  
**Tags:** twitter, x, tweet, social, timeline, search