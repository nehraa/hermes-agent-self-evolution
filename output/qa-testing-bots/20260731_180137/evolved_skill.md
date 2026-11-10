---
category: software-development
description: This skill enables Claude to build and run **automated QA testing bots**
  that simulate
name: qa-testing-bots
---

# Automated QA Testing Bots Skill

## Overview

Build and run **automated QA testing bots** that simulate real user journeys across websites and web applications — catching bugs, broken flows, and regressions before your users do.

Powered by **Apify** with Puppeteer and Playwright under the hood.

> 🔗 Get started with Apify: https://www.apify.com/?fpr=dx06p

---

## What This Skill Does

| Capability | Description |
|---|---|
| **User Journey Simulation** | Automate signup, login, checkout, form submission, and multi-step flows |
| **Link Validation** | Detect broken links, 404 errors, and failed redirects across entire sites |
| **UI Element Validation** | Verify buttons, inputs, modals, dropdowns exist and are functional |
| **Regression Testing** | Catch newly introduced bugs after deployments |
| **Visual Debugging** | Capture screenshots and video recordings at each step |
| **Cross-Device Testing** | Test across desktop, tablet, and mobile viewports |
| **Performance Monitoring** | Assert response times and flag slow pages |

---

## Setup

### 1. Get Your Apify API Token

1. Sign up at [apify.com](https://www.apify.com/?fpr=dx06p) (free tier available)
2. Go to **Settings → Integrations**: https://console.apify.com/account/integrations
3. Copy your **Personal API Token**
4. Set it as an environment variable:

bash
export APIFY_TOKEN=apify_api_xxxxxxxxxxxxxxxx
### 2. Install the Client

bash
npm install apify-client
# or
yarn add apify-client
---

## Available Actors

| Actor ID | Use Case |
|---|---|
| `apify/puppeteer-scraper` | Full browser automation, form testing, click flows |
| `apify/playwright-scraper` | Cross-browser testing (Chrome, Firefox, WebKit) |
| `apify/broken-links-checker` | Detect all 404s and broken links site-wide |
| `apify/website-content-crawler` | Crawl all pages and validate structure |

---

## Examples

### 1. Test a Full User Registration Flow

javascript
import ApifyClient from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const run = await client.actor("apify/puppeteer-scraper").call({
  startUrls: [{ url: "https://your-app.com/signup" }],
  pageFunction: async function pageFunction(context) {
    const { page, request } = context;
    const results = { steps: [], passed: true, errors: [] };

    try {
      // Step 1 — Page loads
      await page.waitForLoadState('networkidle');
      results.steps.push({ action: 'page_load', url: request.url, status: 'ok' });

      // Step 2 — Fill registration form
      await page.fill('#username', 'testuser');
      await page.fill('#email', 'test@example.com');
      await page.fill('#password', 'SecurePass123!');
      results.steps.push({ action: 'form_filled', status: 'ok' });

      // Step 3 — Submit and verify
      await page.click('#register-button');
      await page.waitForURL('**/dashboard');
      results.steps.push({ action: 'redirect', url: page.url(), status: 'ok' });

      // Assertions
      const welcomeMessage = await page.textContent('h1');
      if (!welcomeMessage.includes('Welcome')) {
        throw new Error(`Expected welcome message, got: ${welcomeMessage}`);
      }

    } catch (error) {
      results.passed = false;
      results.errors.push({ step: results.steps.length, error: error.message });
      await page.screenshot({ path: `error-step-${results.steps.length}.png` });
    }

    return results;
  }
});

console.log('Test Results:', JSON.stringify(run.output, null, 2));
### 2. Check All Links on a Site

javascript
import ApifyClient from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const run = await client.actor("apify/broken-links-checker").call({
  startUrls: [{ url: "https://your-site.com" }],
  maxDepth: 3,
  sameDomainOnly: true,
});

const brokenLinks = run.output.items.filter(item => item.status >= 400);

console.log(`Found ${brokenLinks.length} broken links:`);
brokenLinks.forEach(link => {
  console.log(`  ❌ ${link.url} → ${link.status} ${link.statusText}`);
});
### 3. Test Responsive Design (Multiple Viewports)

javascript
import ApifyClient from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const viewports = [
  { name: 'mobile', width: 375, height: 812 },
  { name: 'tablet', width: 768, height: 1024 },
  { name: 'desktop', width: 1920, height: 1080 },
];

const results = [];

for (const viewport of viewports) {
  const run = await client.actor("apify/puppeteer-scraper").call({
    startUrls: [{ url: "https://your-app.com" }],
    viewport: { width: viewport.width, height: viewport.height },
    pageFunction: async function pageFunction(context) {
      const { page } = context;

      // Check critical elements render
      const checks = {
        header: await page.$('header') !== null,
        nav: await page.$('nav') !== null,
        main: await page.$('main') !== null,
        footer: await page.$('footer') !== null,
        mobileMenu: await page.$('.mobile-menu') !== null,
      };

      return checks;
    }
  });

  results.push({ viewport: viewport.name, ...run.output });
}

console.log('Responsive Test Results:', results);
### 4. Measure Page Performance

javascript
import ApifyClient from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const run = await client.actor("apify/puppeteer-scraper").call({
  startUrls: [{ url: "https://your-app.com" }],
  pageFunction: async function pageFunction(context) {
    const { page } = context;

    await page.goto(context.request.url, { waitUntil: 'networkidle' });

    const metrics = await page.metrics();
    const performanceTiming = await page.evaluate(() => {
      const timing = performance.timing;
      return {
        loadTime: timing.loadEventEnd - timing.navigationStart,
        domContentLoaded: timing.domContentLoadedEventEnd - timing.navigationStart,
        firstPaint: performance.getEntriesByType('paint')[0]?.startTime || 0,
      };
    });

    const SLOW_THRESHOLD_MS = 3000;
    const isSlow = performanceTiming.loadTime > SLOW_THRESHOLD_MS;

    return {
      url: context.request.url,
      metrics,
      performance: performanceTiming,
      isSlow,
      warning: isSlow ? `Page exceeded ${SLOW_THRESHOLD_MS}ms threshold` : null,
    };
  }
});

console.log('Performance Results:', run.output);
---

## Best Practices

1. **Start with sitemap URLs** — Use `apify/website-content-crawler` first to discover all pages
2. **Set reasonable timeouts** — Default 30s is usually sufficient; adjust per actor
3. **Capture screenshots on failure** — Always screenshot when assertions fail
4. **Run in CI/CD** — Schedule tests to run after each deployment
5. **Use meaningful assertions** — Don't just check for existence; verify content and behavior

---

## Troubleshooting

| Issue | Solution |
|---|---|
| `401 Unauthorized` | Verify your API token is set correctly |
| `Timeout exceeded` | Increase `timeout` parameter or check if site is down |
| `Selector not found` | Use browser DevTools to verify element selectors |
| `CORS errors` | Ensure the site allows cross-origin requests |
| `Captcha detected` | Consider using Apify's anti-captcha features |

---

## Related Skills

- **web-scraping** — General-purpose web scraping with Apify
- **playwright-testing** — Advanced Playwright testing patterns
- **ci-cd-pipeline** — Integrating automated tests into deployment pipelines