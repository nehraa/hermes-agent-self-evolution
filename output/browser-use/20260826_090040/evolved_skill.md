---
name: browser-use
description: "AI-powered web browser automation using browser-use — autonomously navigates, clicks, types, extracts from any website. Install once, use forever."
category: automation
---

# browser-use Skill

AI-powered web browser automation. An AI agent autonomously interacts with any website — navigates, clicks, fills forms, extracts content — driven by an LLM. Use whenever you need to interact with a website that requires JavaScript rendering, authentication, or multi-step flows that static scraping can't handle.

## Setup (One-Time, Already Completed)

The environment is pre-installed at `~/.hermes/browser-use/`. To activate:

bash
cd ~/.hermes/browser-use
source .venv/bin/activate
If dependencies are missing, run:

bash
uv sync
uvx browser-use install   # installs Chromium + dependencies
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
## Recommended LLM: BrowserUse Cloud

**`ChatBrowserUse`** is optimized for browser automation — 3-5x faster and more cost-effective than general-purpose models.

1. Get an API key at [https://cloud.browser-use.com/new-api-key](https://cloud.browser-use.com/new-api-key)
2. Set `BROWSER_USE_API_KEY` in your environment

python
from browser_use import Agent, ChatBrowserUse

async def main():
    agent = Agent(task="...", llm=ChatBrowserUse())
    await agent.run()
## Cloud Browser (Best for Production/Stealth)

python
from browser_use import Browser, BrowserConfig

browser = Browser(config=BrowserConfig(cloud=True))  # uses browser-use cloud
Set `BROWSER_USE_API_KEY` in environment for cloud browsers.

## Common Patterns

### Pricing Page Research (Sites Behind Login)

Many AI service pricing pages (Kling, Runway, etc.) hide credit costs until authenticated. Use this research sequence:

1. Navigate to pricing page (e.g., `/app/membership/membership-plan`)
2. Check if login is optional — often you can view prices without authenticating
3. If still denied, navigate to the generation UI (e.g., `/app/generate/video`) — credit costs often display before generation starts
4. As a fallback, search external review sites (aitoolanalysis, magichour, segmind) for cached pricing tables

### Multi-Step Form Automation

python
async def fill_complex_form():
    agent = Agent(
        task="Navigate to example.com/signup, fill in email 'user@test.com', "
             "select 'Pro' plan, and complete the checkout form with test data",
        llm=ChatAnthropic(model="claude-sonnet-4-0")
    )
    await agent.run()
### Content Extraction

python
async def extract_article():
    agent = Agent(
        task="Go to https://news.ycombinator.com, find the top post, "
             "and extract its title, author, and point count",
        llm=ChatBrowserUse()
    )
    await agent.run()
### Authentication Flows

python
async def authenticated_scrape():
    agent = Agent(
        task="Login to example.com with email 'user@test.com' and password 'testpass123'. "
             "Then navigate to /dashboard and extract all table data.",
        llm=ChatAnthropic(model="claude-sonnet-4-0")
    )
    await agent.run()
## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `BROWSER_USE_API_KEY` | API key for BrowserUse cloud services | For cloud browser only |
| `ANTHROPIC_API_KEY` | Anthropic API key for Claude models | For Anthropic LLM |

## Troubleshooting

**Browser doesn't launch**: Run `uvx browser-use install` to reinstall Chromium dependencies.

**Agent performs wrong actions**: Add more explicit steps to the task description. Example:

python
# Instead of:
task="Buy a laptop"

# Use:
task="1. Go to amazon.com 2. Search for 'ThinkPad X1 Carbon' 3. Click the first result 4. Add to cart 5. Proceed to checkout"
**Slow performance**: Use `ChatBrowserUse` instead of general-purpose LLMs for browser-specific tasks.