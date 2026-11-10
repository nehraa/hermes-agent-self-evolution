---
name: browser-use
description: "AI-powered web browser automation using browser-use — autonomously navigates, clicks, types, extracts from any website. Install once, use forever."
category: automation
---

# browser-use Skill

AI-powered web browser automation. An AI agent autonomously interacts with any website — navigating, clicking, filling forms, extracting content — driven by an LLM. Use this when you need JavaScript rendering, authentication flows, or multi-step interactions that static scraping cannot handle.

## Setup (already configured)

The environment is pre-installed at `~/.hermes/browser-use/`. Activate it with:

bash
cd ~/.hermes/browser-use
source .venv/bin/activate
## Quick Start

### Python API

python
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
### CLI

bash
cd ~/.hermes/browser-use && source .venv/bin/activate
uvx browser-use --agent-task "Find the top HN post" --llm-provider anthropic --llm-model claude-sonnet-4-0
## Recommended LLM: ChatBrowserUse

For browser automation, `ChatBrowserUse` provides 3-5x speed improvement and lower cost compared to general-purpose models.

python
from browser_use import Agent, ChatBrowserUse

async def main():
    agent = Agent(task="...", llm=ChatBrowserUse())
    await agent.run()
Get your API key at https://cloud.browser-use.com/new-api-key and set it in your `.env`:

bash
BROWSER_USE_API_KEY=your_key_here
## Cloud Browser Mode

For production use or stealthier operations, use the cloud browser:

python
from browser_use import Browser, BrowserConfig

browser = Browser(config=BrowserConfig(cloud=True))
Set `BROWSER_USE_API_KEY` in your environment before running.

## Common Use Cases

| Task | Example Task |
|------|--------------|
| Extract structured data | "Scrape all job listings from page 1 with title, company, salary" |
| Monitor prices | "Check if [product] price dropped below $50 and email me" |
| Fill forms | "Complete the contact form with name, email, and message" |
| Research pricing | "Find the pricing tiers for [service] including per-seat costs" |
| Extract behind login | "Navigate to pricing page, extract all plan details shown" |

## Research Pattern: Pricing Pages Behind Login

Many AI services (Kling, Runway, Midjourney, etc.) hide credit costs until logged in. Strategy:

1. Navigate to pricing page (`/app/membership/membership-plan`)
2. Check if login is required — often optional for reading prices
3. If needed, use `agent.add_history()` to pass login cookies from a previous run
4. Check the generation UI (`/app/generate/video`) — credit costs display before you confirm
5. If still blocked, check external sources: aitoolanalysis.com, magichour.ai, segmind.com — they often document credit costs

## Troubleshooting

- **Page not loading**: Add `max_steps=50` or higher to `Agent()` for complex sites
- **Wrong element clicked**: Include more context in task: "Click the blue 'Sign In' button in the top-right, not the green signup button"
- **Captcha blocking**: Use cloud browser mode for better stealth
- **Slow execution**: Switch to `ChatBrowserUse` LLM