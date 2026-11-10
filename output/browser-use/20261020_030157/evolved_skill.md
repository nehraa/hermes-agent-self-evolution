---
name: browser-use
description: "AI-powered web browser automation using browser-use — autonomously navigates, clicks, types, extracts from any website. Install once, use forever."
category: automation
---

# browser-use Skill

AI-powered web browser automation that uses an LLM to autonomously interact with any website — navigating, clicking, filling forms, and extracting content. Use this when you need JavaScript rendering, authentication flows, or multi-step processes that static scraping cannot handle.

## When to Use

- Websites requiring login or authentication
- JavaScript-heavy Single Page Applications (SPAs)
- Multi-step form submissions
- Captcha-protected or bot-detection sites
- Interactive dashboards or dynamic content
- Price research behind login walls

## Setup (already completed)

The environment is pre-installed at `~/.hermes/browser-use/`:

bash
cd ~/.hermes/browser-use
source .venv/bin/activate
Required tools (Chromium, dependencies) are already installed.

## Running Tasks

### Python API

python
import asyncio
from browser_use import Agent
from langchain_anthropic import ChatAnthropic

async def main():
    agent = Agent(
        task="Find the current price of Claude Pro on anthropic.com pricing page",
        llm=ChatAnthropic(model="claude-sonnet-4-0")
    )
    result = await agent.run()
    print(result)

asyncio.run(main())
### CLI

bash
cd ~/.hermes/browser-use && source .venv/bin/activate
uvx browser-use \
  --agent-task "Navigate to GitHub and find the number of stars for the browser-use repository" \
  --llm-provider anthropic \
  --llm-model claude-sonnet-4-0
## LLM Options

### BrowserUse Cloud (Recommended)

Fastest option — 3-5x faster than standard providers. Get an API key at https://cloud.browser-use.com/new-api-key

python
import os
os.environ["BROWSER_USE_API_KEY"] = "your-key-here"

from browser_use import Agent, ChatBrowserUse

async def main():
    agent = Agent(task="...", llm=ChatBrowserUse())
    await agent.run()
### Cloud Browser (Stealth Mode)

Uses remote browsers — bypasses bot detection for production use:

python
from browser_use import Agent, Browser, BrowserConfig

browser = Browser(config=BrowserConfig(cloud=True))
agent = Agent(task="...", browser=browser)
### Standard Providers

python
# Anthropic
from browser_use import Agent
from langchain_anthropic import ChatAnthropic

agent = Agent(
    task="...",
    llm=ChatAnthropic(model="claude-sonnet-4-0")
)

# OpenAI
from langchain_openai import ChatOpenAI

agent = Agent(
    task="...",
    llm=ChatOpenAI(model="gpt-4o")
)
## Common Patterns

### Pattern 1: Extract Structured Data

python
async def extract_pricing(url: str) -> dict:
    agent = Agent(
        task=f"""Go to {url} and extract all pricing tiers in this format:
        - Plan name
        - Price per month
        - Key features
        Return as a clean list.""",
        llm=ChatAnthropic(model="claude-sonnet-4-0")
    )
    return await agent.run()
### Pattern 2: Multi-Step Research

python
async def research_ai_pricing():
    agent = Agent(
        task="""1. Go to kling.ai and check their pricing page (/app/membership/membership-plan)
        2. If prices require login, note which tier each credit pack belongs to
        3. Navigate to the video generation page (/app/generate/video) and note credit costs shown
        4. If still logged out, check aitoolanalysis.com for user-reported pricing tables
        5. Compile all findings into a comparison table""",
        llm=ChatAnthropic(model="claude-sonnet-4-0")
    )
    return await agent.run()
### Pattern 3: Form Automation

python
async def submit_form(url: str, form_data: dict):
    agent = Agent(
        task=f"""Navigate to {url}
        Fill in the following fields:
        {chr(10).join(f"- {k}: {v}" for k, v in form_data.items())}
        Click the submit button
        Confirm the submission was successful""",
        llm=ChatAnthropic(model="claude-sonnet-4-0")
    )
    return await agent.run()
### Pattern 4: Content Aggregation

python
async def aggregate_news(topic: str):
    agent = Agent(
        task=f"""Search for recent news about {topic}
        Visit the top 5 results
        For each article, extract: title, source, date, key points
        Return a summary with all sources cited""",
        llm=ChatAnthropic(model="claude-sonnet-4-0")
    )
    return await agent.run()
## Research: Paywalled Pricing Pages

Many AI service pricing pages don't display credit costs until logged in:

1. Navigate to the pricing page (often `/app/membership/membership-plan`)
2. Check if login is required or optional for viewing prices
3. For generation tools, navigate to the creation UI (often `/app/generate/video`) — credit costs typically display before generation
4. If paywalled, check external sources: `aitoolanalysis.com`, `magichour.ai`, `segmind.com`, or user forums for cached/user-reported pricing
5. Note any "free tier" credit allocations that are visible without login

## Troubleshooting

**Browser won't launch**: Run `uvx browser-use install` to reinstall Chromium

**Detection/blocked**: Use `BrowserConfig(cloud=True)` for remote browser sessions

**Task too vague**: Provide specific step-by-step instructions in the task description

**Missing elements**: Add wait times or specific element descriptions to your task

**API errors**: Verify `BROWSER_USE_API_KEY` is set correctly for cloud features