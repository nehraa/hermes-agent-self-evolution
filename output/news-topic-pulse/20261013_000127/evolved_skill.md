---
name: news-topic-pulse
description: Live news pulse cron for any topic. Plain-link variant (titles + URLs) or LLM-summarized variant (single consolidated digest, no links, LLM reads the article body).
category: cron
---

# News Topic Pulse

Live news monitoring cron that sends updates on any topic at regular intervals.

## When to Use

Use this skill when the user says:

- "I want live updates on [topic]"
- "Set up a cron for [topic] news"
- "Track [topic] and DM me when it drops"
- "Alert me when [event] happens"
- "I want to know about [ongoing event] as it breaks"
- "Summarize the [topic] news for me" (→ LLM variant)
- "Just the key points, no links" (→ LLM variant)

**Do NOT use for:**

- One-time research → use `web_search` + `web_extract`
- Scraping a specific known URL → use `news-article-scraper`
- Email inbox monitoring → use `inbox_monitor.py`

## Variant Selection

Ask the user which variant they prefer if unclear. Default to LLM-summarized unless they explicitly want links.

| Variant | Output | LLM Cost | Use When |
|---------|--------|----------|----------|
| **Plain-links** | 3-10 bullets: title + source + URL | Zero | Titles are self-explanatory (court rulings, official statements, price changes) |
| **LLM-summarized** | One paragraph (4-6 sentences) of the overall situation | 2 calls/cycle (one per article, one to consolidate) | User wants context, not headlines (protests, breaking events, ongoing stories) |

**Rule of thumb:** If the topic is "what happened" → plain-links. If the topic is "what does this all mean" → LLM-summarized.

## Script Architecture

Three files, one cron entry.

scripts/
├── <topic>-pulse.sh      # Fetches, dedupes, formats
├── <topic>-pulse-runner.sh  # Wrapper: calls fetcher, sends to LLM if needed, posts to Discord
└── <topic>-state.json    # Tracks last-seen URLs (do not delete)
logs/
└── <topic>.log           # Execution log
---

### File 1: `<topic>-pulse.sh` — Fetcher

**Plain-links variant:**

bash
#!/usr/bin/env bash
# <topic>-pulse.sh — Live <topic> news monitor (plain-links)
# Scrape Google News RSS, dedupe against last-seen, output new items.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STATE_FILE="${SCRIPT_DIR}/<topic>-state.json"
LOG_DIR="/home/Hermes/.hermes/scripts/logs"
LOG_FILE="${LOG_DIR}/<topic>.log"

mkdir -p "$LOG_DIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

log "Starting <topic> pulse check"

# Initialize state file if missing
if [ ! -f "$STATE_FILE" ]; then
    echo '{}' > "$STATE_FILE"
fi

# Fetch latest news via Google News RSS
FEED_URL="https://news.google.com/rss/search?q=<topic>&hl=en-IN&gl=IN&ceid=IN:en"
CONTENT=$(curl -s --max-time 30 "$FEED_URL")

if [ -z "$CONTENT" ]; then
    log "ERROR: Empty feed response"
    exit 1
fi

# Parse items (title, link, pubDate)
ITEMS=$(echo "$CONTENT" | grep -oP '(?<=<item>).*?(?=</item>)' | head -20)

NEW_COUNT=0
NEW_ITEMS=""

while IFS= read -r item; do
    [ -z "$item" ] && continue

    TITLE=$(echo "$item" | grep -oP '(?<=<title>).*?(?=</title>)' | sed 's/<[^>]*>//g')
    LINK=$(echo "$item" | grep -oP '(?<=<link>).*?(?=</link>)' | head -1)
    PUB_DATE=$(echo "$item" | grep -oP '(?<=<pubDate>).*?(?=</pubDate>)' | head -1)

    # Skip if no link
    [ -z "$LINK" ] && continue

    # Dedupe against state
    if grep -q "\"$LINK\"" "$STATE_FILE" 2>/dev/null; then
        continue
    fi

    # Mark as seen
    jq --arg link "$LINK" --arg title "$TITLE" \
        '.seen[$link] = $title' "$STATE_FILE" > "${STATE_FILE}.tmp" && \
        mv "${STATE_FILE}.tmp" "$STATE_FILE"

    NEW_COUNT=$((NEW_COUNT + 1))
    NEW_ITEMS="${NEW_ITEMS}${TITLE}|${LINK}|${PUB_DATE}\n"
done <<< "$ITEMS"

log "Found $NEW_COUNT new items"

# Output for runner script
if [ "$NEW_COUNT" -gt 0 ]; then
    echo -e "$NEW_ITEMS" | head -10
fi
**LLM-summarized variant:**

Add article body extraction after fetching each link:

bash
# Inside the dedupe loop, after confirming link is new:
ARTICLE_BODY=$(curl -s --max-time 20 "$LINK" | \
    sed 's/<[^>]*>//g' | \
    tr -s ' ' '\n' | \
    tr '\n' ' ' | \
    sed 's/  */ /g' | \
    cut -c1-3000)

# Store for LLM consumption
echo "${TITLE}|${LINK}|${ARTICLE_BODY}" >> "${SCRIPT_DIR}/<topic>-articles-raw.txt"
---

### File 2: `<topic>-pulse-runner.sh` — Orchestrator

bash
#!/usr/bin/env bash
# <topic>-pulse-runner.sh — Wrapper script
# Calls fetcher, optionally summarizes via LLM, posts to Discord

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="/home/Hermes/.hermes/scripts/logs"
LOG_FILE="${LOG_DIR}/<topic>.log"
VARIANT="<plain-links|llm-summarized>"
DISCORD_WEBHOOK_URL_FILE="/home/Hermes/.hermes/scripts/discord-webhook-url.txt"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Run fetcher
OUTPUT=$("${SCRIPT_DIR}/<topic>-pulse.sh")
ITEM_COUNT=$(echo "$OUTPUT" | grep -c '|')

if [ -z "$ITEM_COUNT" ] || [ "$ITEM_COUNT" -eq 0 ]; then
    log "No new items"
    exit 0
fi

log "Processing $ITEM_COUNT new items"

if [ "$VARIANT" = "llm-summarized" ]; then
    # Read raw articles
    RAW_FILE="${SCRIPT_DIR}/<topic>-articles-raw.txt"
    if [ -f "$RAW_FILE" ]; then
        ARTICLES=$(cat "$RAW_FILE")
        rm -f "$RAW_FILE"
    else
        log "ERROR: No raw articles file found"
        exit 1
    fi

    # Summarize each article individually
    SUMMARIES=""
    while IFS= read -r line; do
        [ -z "$line" ] && continue
        TITLE=$(echo "$line" | cut -d'|' -f1)
        BODY=$(echo "$line" | cut -d'|' -f3)

        SUMMARY=$(python3 << EOF
import anthropic
client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=200,
    messages=[{
        "role": "user",
        "content": f"Summarize this news article in 2 sentences:\n\nTitle: {TITLE}\n\n{BODY}"
    }]
)
print(response.content[0].text)
EOF
)
        SUMMARIES="${SUMMARIES}${SUMMARY}\n\n"
    done <<< "$ARTICLES"

    # Consolidate into one digest
    DIGEST=$(python3 << EOF
import anthropic
client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=300,
    messages=[{
        "role": "user",
        "content": f"Write a 4-6 sentence paragraph summarizing this news topic based on these summaries:\n\n{SUMMARIES}"
    }]
)
print(response.content[0].text)
EOF
)

    PAYLOAD="{\"content\": \"📰 **<topic> Update**\n\n${DIGEST}\"}"

else
    # Plain-links variant
    MESSAGE="**📰 <topic> Update**\n\n"

    while IFS= read -r line; do
        [ -z "$line" ] && continue
        TITLE=$(echo "$line" | cut -d'|' -f1)
        LINK=$(echo "$line" | cut -d'|' -f2)

        # Convert Google News redirect URL to real URL
        REAL_LINK=$(echo "$LINK" | sed 's|.*news.google.com.*/articles/||; s|Ck0=||; s|CkQ=||')
        if [[ "$REAL_LINK" == *"/articles/"* ]]; then
            REAL_LINK=$(echo "$LINK" | grep -oP '(?<=url=).*?(?=&|$)' | head -1)
            [ -z "$REAL_LINK" ] && REAL_LINK="$LINK"
        else
            REAL_LINK="$LINK"
        fi

        MESSAGE="${MESSAGE}• ${TITLE}\n  ${REAL_LINK}\n\n"
    done <<< "$OUTPUT"

    # Truncate if too long
    if [ ${#MESSAGE} -gt 2000 ]; then
        MESSAGE="${MESSAGE:0:1950}...\n\n_(truncated)_"
    fi

    PAYLOAD="{\"content\": \"$MESSAGE\"}"
fi

# Post to Discord
DISCORD_WEBHOOK=$(cat "$DISCORD_WEBHOOK_URL_FILE" 2>/dev/null || echo "")

if [ -n "$DISCORD_WEBHOOK" ]; then
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" \
        -H "Content-Type: application/json" \
        -d "$PAYLOAD" \
        "$DISCORD_WEBHOOK")

    if [ "$HTTP_CODE" = "204" ] || [ "$HTTP_CODE" = "200" ]; then
        log "Posted to Discord successfully"
    else
        log "ERROR: Discord webhook returned HTTP $HTTP_CODE"
    fi
else
    # No Discord webhook — output to console/log
    log "No Discord webhook configured. Output:\n$PAYLOAD"
fi
---

### File 3: `<topic>-state.json` — State

Automatically created and maintained by the fetcher script. Do not delete.

json
{
  "seen": {
    "https://example.com/article1": "Article Title 1",
    "https://example.com/article2": "Article Title 2"
  }
}
**State cleanup:** Run monthly to prevent unbounded growth:
bash
# Keep only last 200 entries
jq '.seen |= to_entries | .[0:200] | from_entries' <topic>-state.json > <topic>-state.tmp && mv <topic>-state.tmp <topic>-state.json
---

## Cron Setup

bash
# Add to crontab: crontab -e

# Every 15 minutes (default for breaking news)
*/15 * * * * /home/Hermes/.hermes/scripts/<topic>-pulse-runner.sh >> /home/Hermes/.hermes/scripts/logs/<topic>-cron.log 2>&1

# Every hour (for slower-moving topics)
# 0 * * * * /home/Hermes/.hermes/scripts/<topic>-pulse-runner.sh >> /home/Hermes/.hermes/scripts/logs/<topic>-cron.log 2>&1

# Twice daily (for weekly digests)
# 0 9,21 * * * /home/Hermes/.hermes/scripts/<topic>-pulse-runner.sh >> /home/Hermes/.hermes/scripts/logs/<topic>-cron.log 2>&1
---

## Testing

Before adding to cron, test manually:

bash
cd /home/Hermes/.hermes/scripts
bash <topic>-pulse-runner.sh
Check the log file for errors:
bash
tail -50 /home/Hermes/.hermes/scripts/logs/<topic>.log
---

## Maintenance

| Task | Frequency | Command |
|------|-----------|---------|
| Check execution | Daily | `tail -20 /home/Hermes/.hermes/scripts/logs/<topic>.log` |
| Clean state file | Monthly | See state cleanup above |
| Verify Discord delivery | Weekly | Check Discord channel |
| Pause cron | Any time | `crontab -e` → comment out line |
| Remove completely | Any time | Delete 3 files, remove crontab entry |

---

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `Empty feed response` | Network timeout or RSS unavailable | Check network; RSS may be temporarily down |
| `No new items` | Normal — no news in last interval | No action needed |
| `Discord webhook returned HTTP 4xx` | Invalid webhook URL | Regenerate Discord webhook |
| `State file missing` | First run or file deleted | Script auto-recreates; normal on first run |