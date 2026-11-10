---
name: news-topic-pulse
description: Live news pulse cron for any topic. Plain-link variant (titles + URLs) or LLM-summarized variant (single consolidated digest, no links, LLM reads the article body).
category: cron
---

# News Topic Pulse — Live Cron for Any Topic

## When to use

Use this skill when Abhinav says any of:
- "I want live updates on X"
- "Set up a cron for Y news"
- "Alert me when Z happens"
- "Track [topic] and DM me when it drops"
- "I want to know about [ongoing event] as it breaks"
- "Summarize the [topic] news for me" (LLM-summarized variant)
- "Just the key points, no links" (LLM-summarized variant)

NOT for:
- One-time research (use web_search + web_extract)
- Scraping a specific site (use news-article-scraper)
- Email inbox digests (different pattern — see inbox_monitor.py in cron jobs)

## Two variants

There are TWO output styles for news-topic-pulse crons. **Ask which one Abhinav wants if he doesn't say** — but the default signal is "no links" or "summarize" → LLM variant; otherwise → plain-links variant.

| Variant | Output | LLM cost | Best for |
|---|---|---|---|
| **Plain-links** | 3-10 bullet items, each with title + source + URL | Zero | Topics where the title itself is informative (CJI rulings, court orders) |
| **LLM-summarized** | ONE consolidated paragraph (4-6 sentences) of the overall situation. No links, no per-article breakdown | 2 LLM calls per cycle (one per article to summarize, one final to consolidate) | Topics where Abhinav wants the *gist* not the *headlines* (protests, ongoing events, breaking stories) |

LLM-summarized is the higher-value variant because the LLM is doing the work of "what does this all mean" that Abhinav would otherwise do himself. For ongoing event topics (protests, court hearings, disasters), it's the right default.

## The working script pattern (canonical, do not deviate)

Three files, three responsibilities, one cron entry.

### 1. `scripts/<topic>-pulse.sh` — fetcher + dedupe + formatter

#### Plain-links variant (no LLM)

Standard structure that worked for Delhi Protest News Pulse (Oct 8 2026):

```bash
#!/usr/bin/env bash
# <topic>-pulse.sh — Live <topic> news monitor
# Runs every N min. Scrapes Google News RSS, dedupes against last-seen, posts only NEW items.

set -e

LOG_DIR="/home/Hermes/.hermes/scripts/logs"
STATE_FILE="/home/Hermes/.hermes/scripts/<topic>_state.json"   # one file per topic
LOG_FILE="${LOG_DIR}/<topic>.log"

mkdir -p "$LOG_DIR"
if [ ! -f "$STATE_FILE" ]; then
    echo '{"last_seen_ids":[],"last_run":""}' > "$STATE_FILE"
fi

# Build search queries — 5-20 is the right band. Less = misses angles, more = duplicate noise.
# Tip: include both narrow and broad phrasings. Mix exact terms with paraphrases.
QUERIES=(
    "<topic exact>"
    "<topic paraphrased>"
    "<actor or event>"
    "<location if relevant>"
    # ... 5-20 entries
)

# Fetch from Google News RSS (no auth, fast, India-aware with ?gl=IN&hl=en-IN)
ALL_ITEMS=""
for q in "${QUERIES[@]}"; do
    encoded=$(echo "$q" | sed 's/ /+/g')
    rss=$(curl -sL --max-time 15 "https://news.google.com/rss/search?q=${encoded}&hl=en-IN&gl=IN&ceid=IN:en" 2>/dev/null || true)
    [ -z "$rss" ] && continue
    items=$(echo "$rss" | python3 -c "
import sys, re, html
data = sys.stdin.read()
items = re.findall(r'<item>(.*?)</item>', data, re.DOTALL)
out = []
for it in items:
    title_m = re.search(r'<title>(.*?)</title>', it, re.DOTALL)
    link_m  = re.search(r'<link>(.*?)</link>', it)
    date_m  = re.search(r'<pubDate>(.*?)</pubDate>', it)
    if title_m and link_m:
        t = html.unescape(title_m.group(1).strip())
        l = link_m.group(1).strip()
        d = date_m.group(1).strip() if date_m else ''
        src = ''
        if ' - ' in t:
            parts = t.rsplit(' - ', 1)
            t = parts[0]
            src = parts[1]
        out.append({'title': t, 'link': l, 'date': d, 'source': src})
seen = set()
deduped = []
for it in out:
    if it['link'] not in seen:
        seen.add(it['link'])
        deduped.append(it)
for it in deduped:
    print(f\"{it['title']}||{it['link']}||{it['date']}||{it['source']}\")
")
    ALL_ITEMS="${ALL_ITEMS}${items}"$'\n'
done

# Python dedupe pass: hash each link, emit only unseen, sort by date desc, cap to top-N
python3 <<EOF > /tmp/<topic>_new.txt
import json, hashlib, datetime
state_file = "$STATE_FILE"
items_raw = """$ALL_ITEMS"""
with open(state_file) as f:
    state = json.load(f)
seen = set(state.get("last_seen_ids", []))
new_items = []
for line in items_raw.splitlines():
    line = line.strip()
    if not line or "||" not in line:
        continue
    parts = line.split("||")
    if len(parts) < 4:
        continue
    title, link, date, source = parts[0], parts[1], parts[2], parts[3]
    h = hashlib.sha256(link.encode()).hexdigest()[:16]
    if h not in seen:
        new_items.append({"h": h, "title": title, "link": link, "date": date, "source": source})

# De-dupe new_items by link too (queries can overlap)
seen_links = set()
unique_new = []
for it in new_items:
    if it['link'] not in seen_links:
        seen_links.add(it['link'])
        unique_new.append(it)

unique_new.sort(key=lambda x: x.get("date", ""), reverse=True)
unique_new = unique_new[:3]   # DEFAULT TOP-N = 3, see pitfall 1

all_seen = list(seen) + [it["h"] for it in unique_new]
all_seen = all_seen[-1000:]
state["last_seen_ids"] = all_seen
state["last_run"] = datetime.datetime.utcnow().isoformat() + "Z"
with open(state_file, "w") as f:
    json.dump(state, f)

if unique_new:
    print("**<Topic> — fresh items**")
    print("")
    for it in unique_new:
        src = f" — _{it['source']}_" if it.get('source') else ""
        print(f"• [{it['title']}]({it['link']}){src}")
EOF
cat /tmp/<topic>_new.txt
```

#### LLM-summarized variant (consolidated digest, no links)

Built for the Delhi Protest News Pulse (Oct 10 2026). Two-stage LLM:
1. **Per-article summarize** — fetch each article body, call LLM to produce a 2-3 sentence summary
2. **Consolidate** — call LLM a second time with all per-article summaries, ask for ONE 4-6 sentence consolidated paragraph

Key script structure:

```bash
#!/usr/bin/env bash
# <topic>-summary.sh — Live <topic> news with LLM-summarized consolidated digest
# Fetches articles, summarizes each, consolidates into one paragraph. No links.

set -e

# ... (same RSS fetching + dedupe as plain-links variant, but cap = 6 items not 3) ...

# Two STAGES happen in the Python block:
# STAGE 1: fetch_text() for each new article (curl + <p> extraction, 3500 char cap)
# STAGE 2: summarize() — single LLM call per article, 2-3 sentence plain-text output
# STAGE 3: ONE FINAL LLM call that takes all per-article summaries and consolidates
#   into a 4-6 sentence paragraph. The system prompt MUST say "no links, no bullets,
#   no per-article breakdown, just one flowing paragraph of key facts".

python3 <<'PYEOF' > /tmp/<topic>_summary.txt
import json, hashlib, datetime, os, subprocess, sys, re, urllib.request, time

# ... (load state, fetch, dedupe, cap to 6 fresh items) ...

def fetch_text(url):
    """Best-effort article body via curl + <p> extraction. Returns "" on failure."""
    try:
        out = subprocess.run(
            ["curl", "-sL", "--max-time", "12",
             "-H", "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
             url],
            capture_output=True, text=True, timeout=15
        )
        html = out.stdout[:200_000]
        html = re.sub(r"<script[^>]*>.*?</script>", " ", html, flags=re.DOTALL|re.IGNORECASE)
        html = re.sub(r"<style[^>]*>.*?</style>", " ", html, flags=re.DOTALL|re.IGNORECASE)
        paras = re.findall(r"<p[^>]*>(.*?)</p>", html, re.DOTALL|re.IGNORECASE)
        body = " ".join(re.sub(r"<[^>]+>", "", p) for p in paras)
        body = re.sub(r"\s+", " ", body).strip()
        import html as htmlmod
        body = htmlmod.unescape(body)[:3500]
        return body
    except Exception:
        return ""

def summarize(title, body, api_key):
    """Single per-article summary. System prompt forbids thinking blocks + thinking tags."""
    if not body or len(body) < 200:
        body = "(article body could not be fetched)"
    payload = json.dumps({
        "model": "MiniMax-M2.7-highspeed",
        "max_tokens": 350,
        "messages": [
            {"role": "system", "content": "You are a news summarizer. Output ONLY a 2-3 sentence plain-text summary. No thinking, no preamble, no labels. Just the facts: who, what, where, when, why. Use specific names, places, numbers."},
            {"role": "user", "content": f"TITLE: {title}\n\nBODY: {body}\n\nSUMMARY:"}
        ]
    }).encode()
    req = urllib.request.Request(
        "https://api.minimax.io/v1/chat/completions",
        data=payload,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
        s = data["choices"][0]["message"]["content"].strip()
        # Defensive: strip any leaked <think>...</think> blocks
        s = re.sub(r"<think>.*?</think>", "", s, flags=re.DOTALL).strip()
        return s
    except Exception as e:
        return f"(summary failed: {e})"

# ... (loop over unique_new[:6], fetch + summarize each, sleep 0.4s between API calls) ...

# STAGE 3: consolidation
combined_prompt = f"""Below are several recent {topic} stories. Produce ONE consolidated 4-6 sentence summary covering the overall situation: who, what, where, when, any police/official response. No links, no bullet points, no article-by-article breakdown. Just one flowing paragraph of the key facts.

TITLES: {' | '.join(titles)}

SUMMARIES:
{chr(10).join('- ' + b for b in bodies)}

CONSOLIDATED DIGEST:"""
final = json.dumps({
    "model": "MiniMax-M2.7-highspeed",
    "max_tokens": 500,
    "messages": [
        {"role": "system", "content": "You are a news editor. Output ONLY a single 4-6 sentence plain-text paragraph. No thinking, no preamble, no labels, no links, no bullet points."},
        {"role": "user", "content": combined_prompt}
    ]
}).encode()
# ... (call API, strip <think>, print) ...

if results:
    print(f"**{topic} — latest digest**")
    print("")
    print(digest)  # ONE paragraph, no bullets, no links
PYEOF

cat /tmp/<topic>_summary.txt
```

**Why this LLM-summarized pattern works:**
- Stage 1 is bounded (one API call per article, 6 max = 6 calls)
- Stage 2 is one final call to consolidate
- Total runtime ~90s for 6 articles (each LLM call ~10-15s)
- The LLM gets the actual article body, not just the title — much higher signal than RSS titles alone
- When the body fetch fails, the LLM is told "(article body could not be fetched)" — it will honestly say so rather than fabricate. Don't ask it to summarize from title alone unless you want the hallucination risk.

### 2. Create the cron

```bash
hermes cron create "*/30 * * * *" --name "<Topic> News Pulse" --script <topic>-pulse.sh --no-agent --deliver origin
```

The cron contract is:
- `--no-agent`: script's stdout IS the message (no LLM in the loop, no tokens wasted)
- `--deliver origin`: lands in the current Telegram chat
- Empty stdout = silent (no "no news" spam) — verified cron-pipeline-no-agent pattern

For the LLM-summarized variant, runtime is ~90s per cycle. The default cron timeout (960s) handles this fine, but if you see a clamp at 60s, that's `process(wait)` not the cron itself — use `process(poll)` to check status, or `process(wait, timeout=60)` in a loop.

### 3. Stop: `hermes cron remove <id>` (user uses remove, not pause)

User uses `remove` (verified Oct 8 2026 — he said "delete that cron job" not "pause"). The system supports both `hermes cron pause <id>` (preserves job) and `hermes cron remove <id>` (deletes). User defaults to remove.

## Pitfalls (verified Oct 8 + Oct 10 2026)

1. **Default top-N = 3 for plain-links variant, 6 for LLM-summarized variant.** For plain-links: Abhinav said "I ain't reading all that i just want the most latest shit." Cap at 3. For LLM-summarized: cap at 6 because the LLM collapses 6 articles into one paragraph anyway — the user reads the paragraph, not the underlying articles. Going higher than 6 in the LLM variant wastes LLM tokens without adding signal.

2. **Clarify ambiguous acronyms BEFORE building the script.** Abhinav said "CJI" — I built a Chief Justice of India monitor. He meant CJP (Citizens for Justice and Peace) protest, then expanded to "any protest happening in Delhi." Two pivots = two wrong builds. The right move: when the user says "track X" with an ambiguous acronym, `clarify` BEFORE writing the script. Cost of clarify: 1 turn. Cost of building wrong: 1 script write + 1 remove + 1 rewrite. Always clarify first if you would otherwise have to delete and rebuild.

3. **When user corrects scope, REMOVE the wrong cron and BUILD the corrected one in the same turn.** Pattern: `hermes cron remove <wrong-id>` → write new script → `hermes cron create <new>`. Don't preserve the wrong one. Don't ask "do you want me to update it?" — they already said the scope changed.

4. **State file is keyed by topic — one state file per topic.** Filename: `<topic>_state.json` in `~/.hermes/scripts/`. Do NOT share state files across topics. Each topic's seen-IDs are independent.

5. **Dedupe by SHA256(link)[:16], not by title or pubDate.** Links are stable; titles and pubDates can shift slightly between scrapes. The 16-char prefix gives ~64-bit hash space which is more than enough for 1000+ items per topic.

6. **Cap the seen-IDs list at 1000 most recent.** Otherwise the state file grows unbounded. `all_seen = all_seen[-1000:]` after every run.

7. **Google News RSS URL parameters matter.** Use `?q=...&hl=en-IN&gl=IN&ceid=IN:en` for India-relevant results. Without these, the RSS serves US-localized results.

8. **No-agent cron fails loud on script error.** If the script `set -e` and Python raises, the cron output is just the error trace — user gets a Telegram message of the traceback. This is the right behavior (no silent failure) but make sure the script is tested BEFORE creating the cron. Smoke test = run the script manually first, confirm it produces clean output, THEN `hermes cron create`.

9. **`text_to_speech` voice replies are NOT the same as news pulse output.** A voice message is a one-shot summary, not a recurring digest. Don't conflate "respond in voice message" with "set up a voice cron." If Abhinav says "respond in voice" in chat, use `text_to_speech` directly to the chat, not a cron. If he says "live voice updates on X", that's a different pattern (TTS the script output) — defer to the user, don't assume.

10. **The script writes markdown to stdout. Telegram renders it.** Plain markdown bullets + links are the right format. Don't pre-format with `MEDIA:` tags or HTML.

11. **For LLM-summarized variant, the system prompt MUST forbid thinking blocks and force plain text output.** Default MiniMax behavior leaks `<think>...</think>` blocks into the response. Use a system prompt that explicitly says "Output ONLY plain text. No thinking, no preamble, no labels." AND apply a defensive `re.sub(r"<think>.*?</think>", "", s, flags=re.DOTALL)` to strip any leaked blocks. Belt and suspenders.

12. **Don't ask the LLM to summarize from title alone — give it the article body.** When the curl body fetch fails (paywall, JS-rendered, 404), pass the literal string "(article body could not be fetched)" to the LLM. The LLM will honestly say "could not summarize" rather than fabricate from the title. Hallucination from title-only summaries is a real risk and looks worse than admitting failure.

13. **Pass large data via mktemp files, not env vars.** Bash argv has a hard limit (visible as `Argument list too long` when exceeded). For the LLM-summarized variant, the ALL_ITEMS string can be 100KB+. Write to `mktemp` and pass path via env var, not the data itself. Env vars are fine for small things (API keys, single URLs) but break for bulk data.

14. **For LLM-summarized variant, the user wants ONE consolidated paragraph, not per-article summaries.** When asked "summarize the X news," Abhinav means one paragraph that captures the overall situation, not N bullet points with one summary each. The second LLM call is the consolidation — don't skip it. (Verified Oct 10 2026: "No not seperate 3 articles just combine rhem all into one summary and then u can bump up the number too if u want of articles i just want one summary not one per article and no links either i dont want any")

15. **"No links" in LLM-summarized variant is literal — strip the URL from the final output.** The system prompt for the consolidation call must say "no links, no URLs, no markdown link syntax." The 2-3-sentence per-article summaries may include URLs (they're internal, not in the final digest), but the final consolidated paragraph must be pure prose. Telegram renders markdown links even in plain text, so the URLs would show as `[link](url)` cruft if not stripped.

## Working example (Oct 8 2026, Delhi protest monitor, plain-links)

Three pivots in this session alone:
1. Built for CJI (Chief Justice). User: "I meant CJP protest."
2. Built for CJP. User: "I meant protest happening in delhi."
3. Final build: `delhi-protest-pulse.sh`, 20 broad queries covering lawyers, students, farmers, gig workers, political, bandh, sit-in, etc. Cron `Delhi Protest News Pulse` every 30 min, top 3, deliver origin.

Three wrong builds before the right one. The lesson in pitfall 2 is real.

## Working example (Oct 10 2026, Delhi protest monitor, LLM-summarized)

User came back the next day and said "I dont want article links I want u to read those articles generate a summary fo the key points and just deliver that summary to me in cron job." I extended the same script with the LLM-summarized two-stage pattern: fetch article body, summarize each, consolidate into one paragraph, no links.

Then user said: "No not seperate 3 articles just combine rhem all into one summary and then u can bump up the number too if u want of articles i just want one summary not one per article and no links either i dont want any."

Final: `delhi-protest-summary.sh`, top 6 articles fetched, two LLM calls per cycle (one per article + one consolidation), runtime ~90s, one consolidated 4-6 sentence digest, no links, no bullets.

This is the new default for ongoing-event topics.

## Reference

- `references/delhi-protest-pulse-2026-10-08.md` — the canonical plain-links working example: full script + the 3-pivot history + the cron-creation commands + the user's explicit "delete that cron job" / "I meant X" / "I want the most latest shit" corrections, all preserved as the durable reference for this class of task.
- `references/delhi-protest-summary-2026-10-10.md` — the LLM-summarized variant: two-stage LLM pattern, the "no links / one consolidated paragraph" user feedback, the mktemp workaround for argv limits, the LLM thinking-block leakage fix, all preserved as the durable reference for the LLM variant.
