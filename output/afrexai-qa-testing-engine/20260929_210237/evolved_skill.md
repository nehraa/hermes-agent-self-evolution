---
category: software-development
description: "The definitive testing methodology for AI agents. From test strategy to execution, coverage to reporting — everything you need to ship quality software."
name: afrexai-qa-testing-engine
---

# QA & Testing Engine — Complete Software Quality System

> The definitive testing methodology for AI agents. From test strategy to execution, coverage to reporting — everything you need to ship quality software.

---

## Phase 1: Test Strategy Design

Before writing a single test, design the strategy. A well-defined strategy prevents wasted effort and ensures you're testing what matters.

### Strategy Brief Template

yaml
project:
  name: ""
  type: web-app | api | mobile | library | cli | data-pipeline
  languages: [typescript, python, go, java]
  frameworks: [react, express, django, spring]
  
risk_profile:
  data_sensitivity: low | medium | high | critical  # PII, financial, health
  user_impact: internal | b2b | b2c | life-safety
  deployment_frequency: daily | weekly | monthly
  regulatory: [none, SOC2, HIPAA, PCI-DSS, GDPR]

test_scope:
  in_scope: []      # Features, services, components to test
  out_of_scope: []  # Explicitly excluded (with business justification)
  
environments:
  dev: { url: "", db: "local" }
  staging: { url: "", db: "seeded" }
  prod: { url: "", smoke_only: true }
### Test Type Decision Matrix

| Risk Profile | Unit | Integration | E2E | Performance | Security | Accessibility |
|--------------|------|-------------|-----|-------------|----------|---------------|
| Internal tool | ✅ Core logic | ✅ API calls | ⚠️ Happy path | ❌ | ⚠️ Basic checks | ❌ |
| B2B SaaS | ✅ Full suite | ✅ Full suite | ✅ Critical flows | ✅ Load testing | ✅ OWASP Top 10 | ✅ WCAG AA |
| B2C high-traffic | ✅ Full suite | ✅ Full suite | ✅ Comprehensive | ✅ Stress + soak | ✅ Full suite | ✅ WCAG AA |
| Financial/Health | ✅ Full + mutation | ✅ Full + contract | ✅ Full + chaos | ✅ Full suite | ✅ Pen test required | ✅ WCAG AAA |

### Test Pyramid Architecture

/  E2E  \          5-10% — Critical user journeys only
        / Integration \     20-30% — API contracts, service boundaries
       /    Unit Tests   \  60-70% — Business logic, pure functions
**Anti-pattern: Ice cream cone** — More E2E than unit tests. Results: slow execution, flaky results, expensive maintenance. **Fix:** Push coverage DOWN the pyramid.

**Anti-pattern: Hourglass** — Lots of unit + E2E, no integration. Results: contract bugs between services slip through. **Fix:** Add integration tests at service boundaries.

---

## Phase 2: Unit Testing Mastery

### The AAA Pattern (Arrange-Act-Assert)

Every unit test follows this three-part structure:

typescript
describe('PricingCalculator', () => {
  // Group by behavior, not by method name
  describe('when customer has volume discount eligibility', () => {
    it('applies 15% discount for orders over 1000 units', () => {
      // Arrange
      const calculator = new PricingCalculator();
      const order = { units: 1500, basePrice: 10 };
      
      // Act
      const result = calculator.calculatePrice(order);
      
      // Assert
      expect(result.finalPrice).toBe(12750); // 1500 * 10 * 0.85
      expect(result.discountApplied).toBe(true);
    });
  });
});
### Naming Conventions

Use the format: `describe('[unit]')` → `it('[expected behavior] when [condition]')`

❌ testCalculate()
❌ testCalculatePriceDiscount()
✅ describe('PricingCalculator') → it('returns discounted price when order exceeds 1000 units')
### Test Doubles

| Type | Purpose | When to Use |
|------|---------|-------------|
| **Mock** | Verify interactions | Checking method calls, argument values |
| **Stub** | Provide canned responses | Controlling external dependencies |
| **Spy** | Wrap real objects | Partial mocking, call tracking |
| **Fake** | Simplified implementation | In-memory DB, mock HTTP clients |

typescript
// Mock — verify interactions
const paymentService = { charge: jest.fn() };
userService.upgradePlan(userId, paymentService);
expect(paymentService.charge).toHaveBeenCalledWith(userId, 99);

// Stub — control responses
userRepo.findById = jest.fn().mockResolvedValue(mockUser);

// Spy — wrap real object with tracking
const realMailer = new Mailer();
const spy = jest.spyOn(realMailer, 'send');
### Boundary Testing

Test the edges — this is where bugs hide:

typescript
describe('AgeValidator', () => {
  it('rejects ages below 0', () => { /* ... */ });
  it('accepts age 0', () => { /* ... */ });
  it('accepts age 18', () => { /* ... */ });
  it('accepts age 120', () => { /* ... */ });
  it('rejects ages above 120', () => { /* ... */ });
});
### Coverage Targets

| Component Type | Target | Minimum |
|----------------|--------|---------|
| Business logic | 90%+ | 80% |
| Utilities/helpers | 80%+ | 70% |
| UI components | 70%+ | 60% |
| Trivial getters/setters | Skip | Skip |

---

## Phase 3: Integration Testing

### API Contract Testing

typescript
describe('POST /api/orders', () => {
  it('validates request body against OpenAPI schema', async () => {
    const response = await request(app)
      .post('/api/orders')
      .send({ customerId: 1 }); // Missing required fields
    
    expect(response.status).toBe(400);
    expect(response.body.errors).toContainEqual({
      field: 'items',
      message: 'items is required'
    });
  });
});
### Database Integration

typescript
describe('OrderRepository', () => {
  beforeEach(async () => {
    await db.seed('test-data.json');
  });
  
  afterEach(async () => {
    await db.reset();
  });
  
  it('persists order and returns with generated ID', async () => {
    const order = { customerId: 1, items: [...] };
    const saved = await repo.create(order);
    
    expect(saved.id).toBeDefined();
    expect(await repo.findById(saved.id)).toEqual(saved);
  });
});
---

## Phase 4: End-to-End Testing

### Critical User Journeys

Only automate journeys that are:
1. **High business value** — Revenue-affecting
2. **High failure impact** — Cannot easily recover
3. **Frequently executed** — Worth investment

Examples for e-commerce:
✅ User registration + first purchase
✅ Login + checkout + payment
✅ Password reset + account recovery

❌ Password change (low frequency, easy manual)
❌ Account deletion (rare, high risk manual)
❌ Admin panel features (separate suite)
### Page Object Pattern

typescript
// page-objects/LoginPage.ts
class LoginPage {
  constructor(private page: Page) {}
  
  async goto() {
    await this.page.goto('/login');
  }
  
  async login(email: string, password: string) {
    await this.page.fill('[data-testid="email"]', email);
    await this.page.fill('[data-testid="password"]', password);
    await this.page.click('[data-testid="submit"]');
  }
}

// tests/login.spec.ts
test('user can login', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.goto();
  await loginPage.login('user@test.com', 'password123');
  await expect(page).toHaveURL('/dashboard');
});
### Handling Flakiness

typescript
// Wait for specific conditions, not arbitrary delays
await expect(page.locator('[data-testid="success-message"]')).toBeVisible();

// Retry failed assertions
test.retry(2);

// Run in isolated contexts
test.describe.configure({ mode: 'parallel' });

// Use test artifacts for debugging
await test.info().attach('screenshot', {
  body: await page.screenshot(),
  contentType: 'image/png'
});
---

## Phase 5: Performance Testing

### Load Testing with k6

javascript
// load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 100 },   // Ramp up
    { duration: '5m', target: 100 },    // Steady state
    { duration: '2m', target: 200 },   // Stress
    { duration: '5m', target: 0 },     // Cool down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% under 500ms
    http_req_failed: ['rate<0.01'],     // <1% failure rate
  },
};

export default function() {
  const res = http.get('https://api.example.com/products');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 1s': (r) => r.timings.duration < 1000,
  });
  sleep(1);
}
### Performance Budget

| Metric | Target | Critical |
|--------|--------|----------|
| First Contentful Paint | < 1.8s | < 3s |
| Time to Interactive | < 3.5s | < 5s |
| Largest Contentful Paint | < 2.5s | < 4s |
| API p95 latency | < 300ms | < 500ms |
| API p99 latency | < 500ms | < 1s |

---

## Phase 6: Security Testing

### OWASP Top 10 Quick Checks

typescript
describe('Security: Injection Prevention', () => {
  it('prevents SQL injection in user input', async () => {
    const maliciousInput = "'; DROP TABLE users; --";
    const response = await request(app)
      .get(`/api/users?search=${encodeURIComponent(maliciousInput)}`);
    
    expect(response.status).toBe(200);
    expect(response.body).not.toContain('DROP TABLE');
    // Verify table still exists
    const tables = await db.query("SHOW TABLES");
    expect(tables).toContain('users');
  });
  
  it('sanitizes XSS payloads in user-generated content', async () => {
    const xssPayload = '<script>alert("xss")</script>';
    const response = await request(app)
      .post('/api/comments')
      .send({ content: xssPayload });
    
    // Script tag should be escaped or stripped
    expect(response.body.content).not.toContain('<script>');
  });
});
### Authentication & Authorization Tests

typescript
describe('Authorization', () => {
  it('prevents user from accessing admin endpoints', async () => {
    const userToken = await getUserToken();
    const response = await request(app)
      .get('/api/admin/users')
      .set('Authorization', `Bearer ${userToken}`);
    
    expect(response.status).toBe(403);
  });
  
  it('prevents IDOR on user resources', async () => {
    const userToken = await getUserToken(1); // User 1's token
    const otherUserResponse = await request(app)
      .get('/api/users/999') // User 999's data
      .set('Authorization', `Bearer ${userToken}`);
    
    expect(otherUserResponse.status).toBe(403);
  });
});
---

## Phase 7: Test Execution & CI/CD

### CI Pipeline Integration

yaml
# .github/workflows/test.yml
name: Test Suite

on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm ci
      - run: npm run test:unit -- --coverage
      - uses: codecov/codecov-action@v3

  integration-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
    steps:
      - uses: actions/checkout@v4
      - run: npm run test:integration

  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm run test:e2e -- --parallel
### Quality Gates

| Gate | Criteria | Blocking |
|------|----------|----------|
| Unit coverage | ≥ 80% | Yes |
| Unit pass rate | 100% | Yes |
| Integration pass | 100% | Yes |
| E2E pass | ≥ 95% | Yes |
| Performance | Meets budget | Yes |
| Security scan | 0 critical | Yes |

---

## Phase 8: Test Reporting & Metrics

### Key Metrics Dashboard

Track these metrics to understand test health:

| Metric | What It Measures | Target |
|--------|------------------|--------|
| **Pass Rate** | Overall test health | > 98% |
| **Flake Rate** | Test reliability | < 2% |
| **Coverage %** | Code exercised | > 80% |
| **MTTD** | Mean time to detect | < 1 day |
| **MTTR** | Mean time to repair | < 3 days |
| **Test Duration** | CI pipeline speed | < 15 min |

### Test Execution Report Structure

Test Execution Report — v2.4.1
Date: 2024-01-15
Duration: 8m 32s

┌─────────────────────────────────────────────┐
│ Summary          │ Passed │ Failed │ Skipped│
├───────────────────�┼────────┼────────┼────────┤
│ Unit Tests        │   847  │    2   │    0   │
│ Integration Tests │   124  │    0   │    3   │
│ E2E Tests         │    89  │    1   │    0   │
└───────────────────┴────────┴────────┴────────┘

Failed Tests:
✗ CheckoutFlow.completePurchase — Timeout waiting for payment confirmation

Coverage: 84.2% (↑ 1.3% from main)
---

## Quick Reference: Test Selection Guide

Need to test a...       Use this...                  Examples

Pure function           Unit test                    calculateTax(), formatDate()
Business rule            Unit test + boundary cases   discount tiers, validation
Database operation       Integration test             CRUD operations, migrations
API endpoint             Integration test             REST endpoints, GraphQL resolvers
User login flow          E2E test                     Auth, sessions, redirects
Payment processing       E2E + contract test          Stripe, PayPal integrations
Concurrent requests      Performance test             Race conditions, deadlocks
Security vulnerability   Security test                Auth bypass, injection, XSS
Browser rendering        E2E visual test              React components, CSS layouts
---

## Anti-Patterns Quick Reference

| Anti-Pattern | Symptom | Solution |
|--------------|---------|----------|
| **Asserting everything** | Fragile tests, constant maintenance | Assert outcomes, not implementation |
| **Testing private methods** | Brittle tests, over-specification | Test public behavior only |
| **Shared mutable state** | Flaky tests, order dependencies | Use fresh instances per test |
| **Testing external services** | Slow, unreliable, rate limits | Mock external APIs |
| **Manual test data setup** | Reproducibility issues | Use factories, fixtures, seeds |
| **One test to rule them all** | Unclear failures, slow | One assertion concept per test |

---

*Last updated: 2024 | Use this as a living document. Adjust thresholds and strategies based on your project's specific needs and risk profile.*