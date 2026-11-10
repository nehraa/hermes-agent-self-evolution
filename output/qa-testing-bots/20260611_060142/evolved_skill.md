---
category: software-development
description: This skill enables Claude to build and run automated QA testing bots that simulate real user journeys across websites and web applications.
name: qa-testing-bots
---

# Automated QA Testing Bots

Build and run automated QA testing bots that simulate real user journeys — catching bugs, broken flows, and regressions before your users do.

Powered by **Apify** with Puppeteer and Playwright under the hood.

> Get started: [Sign up for free](https://www.apify.com/?fpr=dx06p)

---

## Setup

### 1. Get Your Apify API Token

1. Create a free account at [apify.com](https://www.apify.com/?fpr=dx06p)
2. Go to **Settings → Integrations**: [console.apify.com/account/integrations](https://console.apify.com/account/integrations)
3. Copy your **Personal API Token**
4. Set it as an environment variable:

bash
export APIFY_TOKEN=apify_api_xxxxxxxxxxxxxxxx
### 2. Install the Client

bash
npm install apify-client
---

## Available Actors

| Actor | Use Case |
|-------|----------|
| `apify/puppeteer-scraper` | Full browser automation, form testing, click flows |
| `apify/playwright-scraper` | Cross-browser testing (Chrome, Firefox, WebKit) |
| `apify/broken-links-checker` | Find all 404s and broken links site-wide |
| `apify/website-content-crawler` | Crawl all pages and validate structure |

---

## Usage Examples

### Test User Registration Flow

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
    results.steps.push({ action: 'page_load', status: 'ok' });

    // Step 2 — Fill registration form
    await page.fill('#email', 'test@example.com');
    await page.fill('#password', 'SecurePass123!');
    await page.fill('#confirm-password', 'SecurePass123!');
    results.steps.push({ action: 'form_filled', status: 'ok' });

    // Step 3 — Submit and verify redirect
    await Promise.all([
      page.waitForNavigation({ waitUntil: 'networkidle' }),
      page.click('#register-button')
    ]);

    const finalUrl = page.url();
    if (finalUrl.includes('/welcome') || finalUrl.includes('/dashboard')) {
      results.steps.push({ action: 'redirect', status: 'ok', url: finalUrl });
    } else {
      results.passed = false;
      results.errors.push(`Unexpected redirect to: ${finalUrl}`);
    }

    return results;
  }
});

console.log('Test results:', run.output);
### Check for Broken Links Across Your Site

javascript
const run = await client.actor("apify/broken-links-checker").call({
  startUrls: [{ url: "https://your-app.com" }],
  maxConcurrency: 5,
  maxDepth: 3
});

console.log('Broken links found:', run.output.brokenLinks);
### Validate UI Elements

javascript
const run = await client.actor("apify/puppeteer-scraper").call({
  startUrls: [{ url: "https://your-app.com/checkout" }],
  pageFunction: async function pageFunction(context) {
    const { page } = context;
    const checks = [];

    // Verify critical elements exist
    const elements = [
      { selector: '#cart-items', name: 'Cart items container' },
      { selector: '#promo-code-input', name: 'Promo code input' },
      { selector: '#checkout-button', name: 'Checkout button' },
      { selector: '#terms-checkbox', name: 'Terms checkbox' }
    ];

    for (const el of elements) {
      const exists = await page.locator(el.selector).count() > 0;
      checks.push({ element: el.name, present: exists });
    }

    // Verify button is clickable
    const button = page.locator('#checkout-button');
    const isEnabled = await button.isEnabled();
    checks.push({ element: 'Checkout button enabled', present: isEnabled });

    return { checks, timestamp: new Date().toISOString() };
  }
});

console.log('UI validation:', run.output.checks);
### Test Responsive Design (Multiple Viewports)

javascript
const viewports = [
  { name: 'Mobile', width: 375, height: 812 },
  { name: 'Tablet', width: 768, height: 1024 },
  { name: 'Desktop', width: 1920, height: 1080 }
];

for (const vp of viewports) {
  const run = await client.actor("apify/puppeteer-scraper").call({
    startUrls: [{ url: "https://your-app.com/" }],
    pageFunction: async function pageFunction(context) {
      const { page } = context;
      await page.setViewportSize({ width: vp.width, height: vp.height });
      await page.waitForLoadState('networkidle');

      // Check for horizontal scroll (layout breakage)
      const scrollWidth = await page.evaluate(() => document.body.scrollWidth);
      const viewportWidth = await page.evaluate(() => window.innerWidth);
      const hasHorizontalScroll = scrollWidth > viewportWidth;

      return {
        viewport: context.viewport,
        hasHorizontalScroll,
        layoutBreak: hasHorizontalScroll ? 'FAIL' : 'PASS'
      };
    }
  });
}
---

## Best Practices

- **Use `waitForLoadState('networkidle')`** instead of arbitrary timeouts
- **Set reasonable concurrency limits** to avoid overwhelming target servers
- **Store test results** in a structured format for CI/CD integration
- **Add retry logic** for flaky network conditions
- **Screenshot on failure** for faster debugging

---

## Running in CI/CD

Add QA tests to your deployment pipeline:

yaml
# Example: GitHub Actions
- name: Run QA Tests
  env:
    APIFY_TOKEN: ${{ secrets.APIFY_TOKEN }}
  run: |
    node test/user-flows.js
    node test/broken-links.js
```yaml
---
category: software-development
description: Build and run automated QA testing bots that simulate real user journeys across websites and web applications — catching bugs, broken flows, and regressions before your users do.
name: qa-testing-bots
---

# Automated QA Testing Bots

Build and run automated QA testing bots that simulate real user journeys across websites and web applications — catching bugs, broken flows, and regressions before your users do.

Powered by **Apify** with Puppeteer and Playwright under the hood.

> 🔗 Sign up for free: [apify.com](https://www.apify.com/?fpr=dx06p)

---

## What This Skill Does

- Simulate complete **user journeys** (signup, login, checkout, form submission)
- Detect **broken links**, **404 errors**, and **failed redirects** across an entire site
- Validate **UI elements** — buttons, inputs, modals, dropdowns — are present and functional
- Run **regression tests** after deployments to catch newly introduced bugs
- Take **screenshots and video recordings** at each step for visual debugging
- Test across multiple **viewports** (desktop, tablet, mobile)
- Assert **response times** and flag pages that are too slow

---

## Setup

### 1. Get Your Apify API Token

1. Sign up for free at [apify.com](https://www.apify.com/?fpr=dx06p)
2. Navigate to **Settings → Integrations**
   - Direct link: [console.apify.com/account/integrations](https://console.apify.com/account/integrations)
3. Copy your **Personal API Token** (starts with `apify_api_`)
4. Set it as an environment variable:

bash
export APIFY_TOKEN=apify_api_xxxxxxxxxxxxxxxx
### 2. Install the Client

bash
npm install apify-client
---

## Available Actors

| Actor | Best For |
|-------|----------|
| `apify/puppeteer-scraper` | Full browser automation, form testing, click flows |
| `apify/playwright-scraper` | Cross-browser testing (Chrome, Firefox, WebKit) |
| `apify/broken-links-checker` | Detect all 404s and broken links site-wide |
| `apify/website-content-crawler` | Crawl all pages and validate structure |

---

## Usage Examples

### Test a Full User Registration Flow

javascript
import ApifyClient from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const run = await client.actor("apify/puppeteer-scraper").call({
  startUrls: [{ url: "https://your-app.com/signup" }],
  pageFunction: async function pageFunction(context) {
    const { page } = context;
    const results = { steps: [], passed: true, errors: [] };

    try {
      // Step 1 — Page loads
      await page.waitForLoadState('networkidle');
      results.steps.push({ action: 'page_load', status: 'ok' });

      // Step 2 — Fill registration form
      await page.fill('#email', 'test@example.com');
      await page.fill('#password', 'TestPass123!');
      await page.fill('#confirm-password', 'TestPass123!');
      results.steps.push({ action: 'form_filled', status: 'ok' });

      // Step 3 — Submit and verify
      await Promise.all([
        page.waitForNavigation({ waitUntil: 'networkidle' }),
        page.click('#register-button')
      ]);

      // Verify success
      const url = page.url();
      if (url.includes('/welcome') || url.includes('/dashboard')) {
        results.steps.push({ action: 'registration_success', status: 'ok' });
      } else {
        results.passed = false;
        results.errors.push(`Unexpected redirect: ${url}`);
      }

      // Capture screenshot on completion
      await page.screenshot({ path: 'registration-complete.png' });

    } catch (err) {
      results.passed = false;
      results.errors.push(err.message);
    }

    return results;
  }
});

console.log('Test passed:', run.output.passed);
console.log('Steps:', run.output.steps);
### Check for Broken Links Across Your Site

javascript
const run = await client.actor("apify/broken-links-checker").call({
  startUrls: [{ url: "https://your-app.com" }],
  maxConcurrency: 5,
  maxDepth: 3  // Crawl up to 3 levels deep
});

console.log('Broken links:', run.output.brokenLinks);
console.log('Total pages checked:', run.output.totalPages);
### Validate UI Elements Are Present

javascript
const run = await client.actor("apify/puppeteer-scraper").call({
  startUrls: [{ url: "https://your-app.com/checkout" }],
  pageFunction: async function pageFunction(context) {
    const { page } = context;
    const checks = [];

    // Define critical elements to validate
    const elements = [
      { selector: '#cart-items', name: 'Cart items' },
      { selector: '#promo-input', name: 'Promo code input' },
      { selector: '#checkout-btn', name: 'Checkout button' },
      { selector: '#payment-form', name: 'Payment form' }
    ];

    for (const el of elements) {
      const exists = await page.locator(el.selector).count() > 0;
      checks.push({ element: el.name, present: exists });
      
      if (!exists) {
        console.error(`Missing element: ${el.name} (${el.selector})`);
      }
    }

    // Verify checkout button is enabled
    const btnEnabled = await page.locator('#checkout-btn').isEnabled();
    checks.push({ element: 'Checkout button enabled', present: btnEnabled });

    return { checks, allPresent: checks.every(c => c.present) };
  }
});

console.log('All elements present:', run.output.allPresent);
### Test Across Multiple Viewports

javascript
const viewports = [
  { name: 'Mobile', width: 375, height: 812 },
  { name: 'Tablet', width: 768, height: 1024 },
  { name: 'Desktop', width: 1280, height: 720 },
  { name: 'Wide', width: 1920, height: 1080 }
];

for (const vp of viewports) {
  const run = await client.actor("apify/puppeteer-scraper").call({
    startUrls: [{ url: "https://your-app.com/" }],
    pageFunction: async function pageFunction(context) {
      const { page } = context;
      
      // Set viewport size
      await page.setViewportSize({ width: vp.width, height: vp.height });
      await page.waitForLoadState('networkidle');

      // Check for horizontal scroll (layout breakage)
      const hasHorizontalScroll = await page.evaluate(() => {
        return document.body.scrollWidth > window.innerWidth;
      });

      return {
        viewport: vp.name,
        passed: !hasHorizontalScroll,
        hasHorizontalScroll
      };
    }
  });

  console.log(`${vp.name}: ${run.output.passed ? 'PASS' : 'FAIL'}`);
}
---

## Best Practices

- **Wait for network idle** — Use `waitForLoadState('networkidle')` instead of arbitrary delays
- **Set concurrency limits** — Avoid overwhelming target servers with `maxConcurrency`
- **Screenshot on failure** — Capture debugging evidence when tests fail
- **Validate with assertions** — Don't just check existence; verify correct behavior
- **Test realistic flows** — Simulate actual user behavior, not just element presence

---

## CI/CD Integration

Run QA tests in your deployment pipeline:

bash
# Example: Run tests after deployment
node --experimental-vm-modules qa-tests/user-flows.js
node qa-tests/broken-links.js
javascript
// Exit with proper code for CI
if (!testResults.passed) {
  console.error('QA tests failed');
  process.exit(1);
}