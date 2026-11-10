---
name: browser-use
description: "AI-powered web browser automation using browser-use — autonomously navigates, clicks, types, extracts from any website. Install once, use forever."
category: automation
---

# browser-use Skill

AI-powered web browser automation. An AI agent autonomously interacts with any website — navigates, clicks, fills forms, extracts content — driven by an LLM. Use whenever you need to interact with a website that requires JavaScript rendering, authentication, or multi-step flows that static scraping can't handle.

## Setup (one-time, already done on this machine)

```bash
cd ~/.hermes/browser-use
uv venv --python 3.11 .venv
source .venv/bin/activate
uv sync
uvx browser-use install   # installs Chromium + dependencies
```

**Location**: `~/.hermes/browser-use/` — already cloned and installed.

## Quick Start

```python
import asyncio
from browser_use import Agent, ChatAnthropic
from dotenv import load_dotenv

load_dotenv()

async def main():
    agent = Agent(
        task="Your instruction here",
        llm=ChatAnthropic(model="claude-sonnet-4-0")
    )
    await agent.run()

asyncio.run(main())
```

Or via CLI:
```bash
cd ~/.hermes/browser-use && source .venv/bin/activate
uvx browser-use --agent-task "Find the top HN post" --llm-provider anthropic --llm-model claude-sonnet-4-0
```

## Preferred LLM

**`ChatBrowserUse`** — fastest and most cost-effective for browser automation (3-5x faster). Get key at https://cloud.browser-use.com/new-api-key

```python
from browser_use import Agent, ChatBrowserUse

async def main():
    agent = Agent(task="...", llm=ChatBrowserUse())
    await agent.run()
```

## Cloud Browser (best for production / stealth)

```python
from browser_use import Browser, BrowserConfig

browser = Browser(config=BrowserConfig(cloud=True))  # uses browser-use cloud
```

Set `BROWSER_USE_API_KEY` in environment for cloud browsers.

## Research Pattern: Pricing Pages Behind Login

Many AI service pricing pages (Kling, Runway, etc.) don't show credit costs until logged in. The generation UI shows credit cost when you select video settings. Use this research sequence:

1. Navigate to pricing page (`/app/membership/membership-plan`)
2. Click through any login interstitial (it's often optional for reading prices)
3. Navigate to generation UI (`/app/generate/video`) — credit cost shown before generation
4. If still logged out, look for plan comparison tables on external review sites (aitoolanalysis, magichour, segmind) which publish credit costs per video type
5. Check `references/kling-ai-pricing.md` in this skill for pre-researched Kling credit costs (May 2026 verified)

### WorldMonitor.app — JS SPA that ScrapeGraph can't handle

`https://www.worldmonitor.app` — live country-level geopolitical intelligence (212KB JSON feed). ScrapeGraphAI only sees landing page marketing copy. browser-use handles the JS-rendered SPA natively.

**PREFERRED approach — async Playwright interceptor (no LLM needed):**
```python
import asyncio
from playwright.async_api import async_playwright

async def fetch_worldmonitor():
    OUTPUT = "/tmp/wm_news_feed.json"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=[
            '--disable-blink-features=AutomationControlled',
            '--no-sandbox', '--disable-dev-shm-usage',
        ])
        page = await browser.new_page()
        async def on_resp(r):
            if 'list-feed-digest' in r.url:
                body = await r.body()  # ← await r.body() captures FULL 212KB without truncation
                with open(OUTPUT, 'wb') as f: f.write(body)
        page.on('response', on_resp)
        await page.goto('https://www.worldmonitor.app', timeout=30000, wait_until='domcontentloaded')
        await asyncio.sleep(10)
        await browser.close()
    # Then parse /tmp/wm_news_feed.json — categories: politics, middleeast, europe, us, etc.
```

⚠️ **Sync Playwright fails** — `response.text()` truncates at ~100KB, causing `json.JSONDecodeError`. Use async + `await r.body()`.

**Alternative (LLM-powered, more expensive):**
```python
from browser_use import Agent, ChatOpenAI

agent = Agent(
    task="Navigate to https://www.worldmonitor.app and extract all news stories with "
         "title, snippet, riskLevel, importance score, source, link.",
    llm=ChatOpenAI(model="gpt-4o")
)
```

User confirmed (May 17, 2026): "this is the best source" for international news.

## noVNC + CDP Pattern: User-Auth-Then-Automate

Many sites (Google, Gemini, banking sites) detect and block CDP/browser automation. The pattern:

1. Start Xvfb + x11vnc + noVNC on the server
2. Launch browser in Xvfb
3. User connects via noVNC (`http://<server>:6080/vnc_lite.html`) and manually authenticates
4. After auth, use Playwright's CDP to connect to the authenticated session and automate

**Setup:**
```bash
# Xvfb virtual display
Xvfb :99 -screen 0 1920x1080x24 &

# VNC server sharing the display
export DISPLAY=:99
x11vnc -display :99 -nopw -listen localhost -xkb -ncache 10 -ncache_cr -forever -rfbport 5900 -bg

# noVNC web proxy
websockify --web=/usr/share/novnc 0.0.0.0:6080 localhost:5900 &
```

**Then launch browser and let user authenticate via noVNC URL.**

**Tailscale access:** Server at `100.118.48.109`, noVNC at **`http://100.118.48.109:6080/vnc.html`** (not `vnc_lite.html`)

**Common issues:**
- Port 5900 already in use → `sudo lsof -i :5900` to find old x11vnc
- Chrome CDP on wrong port → check `ps aux | grep chrome`
- Mac Tailscale offline → user must reconnect to reach noVNC

## Useful Patterns

### Extract structured data from a website
```python
agent = Agent(
    task="Go to example.com, extract all product names and prices, return as JSON",
    llm=ChatAnthropic(model="claude-sonnet-4-0")
)
```

### Multi-step authenticated flow
```python
agent = Agent(
    task="Login to gmail.com with email user@example.com and password mypass, then send an email to test@example.com with subject 'Hello'",
    llm=ChatAnthropic(model="claude-sonnet-4-0")
)
```

### Scrape dynamic content (JS-rendered)
```python
agent = Agent(
    task="Find all job listings on linkedin.com/jobs/search/?keywords=python",
    llm=ChatAnthropic(model="claude-sonnet-4-0")
)
```

## Environment Variables

```bash
BROWSER_USE_API_KEY=        # cloud.browser-use.com API key (for cloud browsers)
ANTHROPIC_API_KEY=          # for ChatAnthropic
OPENAI_API_KEY=             # for ChatOpenAI
GOOGLE_API_KEY=             # for ChatGoogle
```

## Tips

- Be specific in tasks: "Click the login button, wait 2s, enter 'myuser' in the username field"
- Use `ChatBrowserUse` for fastest/cheapest browser tasks
- Use `Browser(use_cloud=True)` to bypass bot detection, CAPTCHAs, geo-restrictions
- browser-use supports persistent contexts (cookies/profiles) for authenticated sessions
