---
category: software-development
description: This skill enables Claude to build and run **automated QA testing bots** that simulate real user journeys across websites and web applications.
name: qa-testing-bots
---

# Automated QA Testing Bots

## Overview

Build and deploy automated QA testing bots that simulate real user journeys across websites and web applications — catching bugs, broken flows, and regressions before your users encounter them.

Powered by **Apify** with Puppeteer and Playwright under the hood.

> **Get started:** [Create a free Apify account](https://www.apify.com/?fpr=dx06p)

---

## What This Skill Does

| Capability | Description |
|---|---|
| **User Journey Simulation** | Automate signup, login, checkout, form submissions, and multi-step flows |
| **Link Validation** | Detect broken links, 404 errors, and failed redirects site-wide |
| **UI Element Verification** | Assert buttons, inputs, modals, and dropdowns are present and functional |
| **Regression Testing** | Validate functionality after deployments to catch regressions |
| **Visual Debugging** | Capture screenshots and video recordings at each step |
| **Cross-Device Testing** | Test across desktop, tablet, and mobile viewports |
| **Performance Monitoring** | Assert response times and flag slow pages |

---

## Setup

### 1. Get Your Apify API Token

1. Sign up at [apify.com](https://www.apify.com/?fpr=dx06p)
2. Go to **Settings → Integrations** ([direct link](https://console.apify.com/account/integrations))
3. Copy your **Personal API Token**
4. Set it as an environment variable:

bash
export APIFY_TOKEN=apify_api_xxxxxxxxxxxxxxxx
### 2. Install Dependencies

bash
npm install apify-client
---

## Available Actors

| Actor | Best For |
|---|---|
| `apify/puppeteer-scraper` | Full browser automation, form testing, click flows |
| `apify/playwright-scraper` | Cross-browser testing (Chrome, Firefox, WebKit) |
| `apify/broken-links-checker` | Detect all 404s and broken links site-wide |
| `apify/website-content-crawler` | Crawl all pages and validate structure |

---

## Examples

### Test a User Registration Flow

javascript
import ApifyClient from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const run = await client.actor("apify/puppeteer-scraper").call({
  startUrls: [{ url: "https://your-app.com/signup" }],
  pageFunction: async function pageFunction(context) {
    const { page, request } = context;
    const results = { steps: [], passed: true, errors: [] };

    // Step 1 — Verify page loads
    await page.waitForLoadState('networkidle');
    results.steps.push({ name: 'page_load', status: 'ok' });

    // Step 2 — Fill registration form
    await page.fill('#username', 'testuser_' + Date.now());
    await page.fill('#email', `test_${Date.now()}@example.com`);
    await page.fill('#password', 'SecurePass123!');
    results.steps.push({ name: 'form_fill', status: 'ok' });

    // Step 3 — Submit and verify
    await page.click('#signup-button');
    await page.waitForURL('**/dashboard');
    results.steps.push({ name: 'redirect', status: 'ok' });

    // Capture screenshot for debugging
    await page.screenshot({ path: 'signup-success.png' });

    return results;
  }
});

console.log('Test results:', run.output);
### Check for Broken Links Across a Site

javascript
import ApifyClient from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const run = await client.actor("apify/broken-links-checker").call({
  startUrls: [{ url: "https://your-app.com" }],
  maxConcurrency: 5,
  maxRequestRetries: 3
});

const brokenLinks = run.output?.items?.filter(item => item.status >= 400) || [];

if (brokenLinks.length > 0) {
  console.log('❌ Found broken links:');
  brokenLinks.forEach(link => {
    console.log(`  ${link.url} → ${link.status} ${link.statusText}`);
  });
} else {
  console.log('✅ No broken links found');
}
### Cross-Viewport UI Testing

javascript
import ApifyClient from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const viewports = [
  { name: 'mobile', width: 375, height: 667 },
  { name: 'tablet', width: 768, height: 1024 },
  { name: 'desktop', width: 1280, height: 720 }
];

for (const viewport of viewports) {
  const run = await client.actor("apify/puppeteer-scraper").call({
    startUrls: [{ url: "https://your-app.com/home" }],
    pageFunction: async function pageFunction(context) {
      const { page } = context;
      const results = { viewport: context.viewport, issues: [] };

      // Check navigation exists
      const nav = await page.$('nav');
      if (!nav) results.issues.push('Missing navigation');

      // Check CTA button is visible
      const cta = await page.$('#signup-cta');
      const isVisible = cta ? await cta.isVisible() : false;
      if (!isVisible) results.issues.push('CTA button not visible');

      await page.screenshot({ path: `home-${viewport.name}.png` });

      return results;
    },
    customData: { viewport: viewport.name }
  });

  console.log(`${viewport.name}: ${run.output?.issues?.length || 0} issues`);
}
### Regression Test After Deployment

javascript
import ApifyClient from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const criticalPaths = [
  '/',
  '/pricing',
  '/signup',
  '/login',
  '/docs/getting-started'
];

async function runRegressionTest() {
  const results = { passed: 0, failed: 0, issues: [] };

  for (const path of criticalPaths) {
    const run = await client.actor("apify/puppeteer-scraper").call({
      startUrls: [{ url: `https://your-app.com${path}` }],
      pageFunction: async function pageFunction(context) {
        const { page, request } = context;
        const result = { path, errors: [], warnings: [] };

        // Check page loads within 3 seconds
        const startTime = Date.now();
        await page.waitForLoadState('domcontentloaded');
        const loadTime = Date.now() - startTime;

        if (loadTime > 3000) {
          result.warnings.push(`Slow load: ${loadTime}ms`);
        }

        // Check no console errors
        page.on('console', msg => {
          if (msg.type() === 'error') {
            result.errors.push(msg.text());
          }
        });

        // Check page has content
        const bodyText = await page.textContent('body');
        if (bodyText.length < 100) {
          result.errors.push('Page appears to be empty');
        }

        await page.waitForTimeout(1000); // Let console errors fire
        return result;
      }
    });

    const output = run.output || {};

    if (output.errors?.length > 0) {
      results.failed++;
      results.issues.push({ path, errors: output.errors });
      console.log(`❌ ${path}: ${output.errors.length} errors`);
    } else {
      results.passed++;
      console.log(`✅ ${path}`);
    }
  }

  console.log(`\nRegression Results: ${results.passed}/${criticalPaths.length} passed`);

  if (results.issues.length > 0) {
    process.exit(1); // Fail CI/CD pipeline
  }
}

runRegressionTest();
---

## Best Practices

- **Start with critical paths** — Test your most important user journeys first
- **Use screenshots strategically** — Capture them only when debugging, not on every run
- **Set reasonable timeouts** — Account for slow networks and third-party scripts
- **Run in CI/CD** — Integrate regression tests into your deployment pipeline
- **Monitor performance** — Track response times over time to spot degradation

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `APIFY_TOKEN` | Yes | Your Apify API token |
| `APIFY_MAX_CONCURRENCY` | No | Max parallel browser instances (default: 1) |
| `APIFY_MEMORY_MBYTES` | No | Memory limit per actor (default: 256) |