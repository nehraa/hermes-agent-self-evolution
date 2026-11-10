---
name: browser-use
description: "AI-powered web browser automation using browser-use — autonomously navigates, clicks, types, extracts from any website. Install once, use forever."
category: automation
---

# browser-use Skill

AI-powered web browser automation. An AI agent autonomously interacts with any website — navigates, clicks, fills forms, extracts content, handles authentication — driven by an LLM. Use whenever you need to interact with a website that requires JavaScript rendering, login flows, or multi-step processes that static scraping cannot handle.

## Setup (already completed)

**Location**: `~/.hermes/browser-use/`

bash
cd ~/.hermes/browser-use
source .venv/bin/activate
## Usage

### Python API

python
import asyncio
from browser_use import Agent
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
## Recommended LLM

**`ChatBrowserUse`** — optimized for browser automation, 3-5x faster than general-purpose models.

python
from browser_use import Agent, ChatBrowserUse

async def main():
    agent = Agent(task="...", llm=ChatBrowserUse())
    await agent.run()
Get your API key at: https://cloud.browser-use.com/new-api-key

## Cloud Browser

For production use or when stealth is important (avoids local browser detection):

python
from browser_use import Browser, BrowserConfig

browser = Browser(config=BrowserConfig(cloud=True))
Set `BROWSER_USE_API_KEY` environment variable for cloud browsers.

## Common Patterns

### Research Behind Login Walls

Many AI service pricing pages (Kling, Runway, etc.) hide credit costs until authenticated. Use this sequence:

1. Navigate to pricing page (`/app/membership/membership-plan`)
2. Dismiss login interstitials if optional for viewing
3. Navigate to generation UI (`/app/generate/video`) — credit cost displayed before generation
4. If still authenticated out, search external review sites (aitoolanalysis, magichour, segmind) for plan comparisons

### Multi-Step Data Extraction

python
agent = Agent(
    task="Go to example.com/products, filter by 'electronics', extract all product names and prices, save to a JSON file",
    llm=ChatAnthropic(model="claude-sonnet-4-0")
)
await agent.run()
### Form Filling and Submission

python
agent = Agent(
    task="Navigate to example.com/contact, fill in name='John Doe', email='john@example.com', message='Hello', and click submit",
    llm=ChatAnthropic(model="claude-sonnet-4-0")
)
await agent.run()
## Tips

- **Be specific**: "Click the blue button labeled 'Submit'" works better than "Click submit"
- **Chain complex tasks**: For complex flows, break into smaller agent tasks if reliability drops
- **Check intermediate steps**: The agent prints actions to stdout — monitor for errors
- **Wait for dynamic content**: Let the agent wait for page loads; don't assume immediate rendering