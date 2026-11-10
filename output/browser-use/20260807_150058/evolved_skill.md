---
name: browser-use
description: "AI-powered web browser automation using browser-use — autonomously navigates, clicks, types, extracts from any website. Install once, use forever."
category: automation
---

# browser-use Skill

AI-powered web browser automation that lets an AI agent autonomously interact with any website — navigating, clicking, filling forms, and extracting content. Ideal for sites requiring JavaScript rendering, authentication, or multi-step flows that static scraping cannot handle.

## Setup

**Already installed** at `~/.hermes/browser-use/`. Activate the environment before use:

bash
cd ~/.hermes/browser-use && source .venv/bin/activate
## Usage

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
    result = await agent.run()
    print(result)

asyncio.run(main())
### CLI

bash
cd ~/.hermes/browser-use && source .venv/bin/activate

uvx browser-use \
  --agent-task "Find the top HN post" \
  --llm-provider anthropic \
  --llm-model claude-sonnet-4-0
## Recommended LLM

**ChatBrowserUse** — optimized for browser automation, typically 3-5x faster and more cost-effective.

python
from browser_use import Agent, ChatBrowserUse

async def main():
    agent = Agent(task="...", llm=ChatBrowserUse())
    await agent.run()
Get your API key at: https://cloud.browser-use.com/new-api-key

## Cloud Browser (Production / Stealth Mode)

Uses browser-use's cloud infrastructure for better stealth and reliability:

python
from browser_use import Browser, BrowserConfig

browser = Browser(config=BrowserConfig(cloud=True))
Set your API key in the environment:

bash
export BROWSER_USE_API_KEY="your-key-here"
## Common Patterns

### Research: Pricing Pages Behind Login

Many AI services (Kling, Runway, etc.) hide credit costs until logged in. The generation UI typically shows credit cost before creation.

python
agent = Agent(
    task="""Research pricing for [SERVICE]:
    1. Navigate to pricing page (/app/membership/membership-plan)
    2. Check if prices visible without login — sometimes login interstitial is optional
    3. If not visible, navigate to generation UI (/app/generate/video) — credit cost shown before generation
    4. If still logged out, check external review sites (aitoolanalysis, magichour, segmind) for plan comparison tables
    5. Extract and document all credit/cost information found""",
    llm=ChatAnthropic(model="claude-sonnet-4-0")
)
await agent.run()
### Content Extraction

python
agent = Agent(
    task="Extract all job listings from the page including: title, company, location, salary range, and job description",
    llm=ChatAnthropic(model="claude-sonnet-4-0")
)
### Form Filling & Multi-Step Flows

python
agent = Agent(
    task="""Complete the registration form:
    1. Navigate to example.com/signup
    2. Fill email with 'test@example.com'
    3. Fill password with a secure password
    4. Select 'Marketing' from industry dropdown
    5. Click the submit button
    6. Report any errors or confirmation received""",
    llm=ChatAnthropic(model="claude-sonnet-4-0")
)
## Troubleshooting

| Issue | Solution |
|-------|----------|
| Page doesn't load | Try `cloud=True` in BrowserConfig for stealth mode |
| Authentication fails | Pass credentials via task prompt or use session cookies |
| Element not found | Add wait steps in task description: "Wait 2 seconds after clicking" |
| Rate limiting | Add delays between actions in your task description |