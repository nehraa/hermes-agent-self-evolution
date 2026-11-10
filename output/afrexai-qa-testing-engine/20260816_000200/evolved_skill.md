---
category: software-development
description: "> The definitive testing methodology for AI agents. From test strategy to execution, coverage to reporting — everything you need to ship quality software."
name: afrexai-qa-testing-engine
---

# QA & Testing Engine — Complete Software Quality System

> The definitive testing methodology for AI agents. From test strategy to execution, coverage to reporting — everything you need to ship quality software.

## Phase 1: Test Strategy Design

Before writing a single test, establish your testing philosophy and scope.

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
  in_scope: []    # Features, services, components to test
  out_of_scope: [] # Explicitly excluded (with justification)
  
environments:
  dev: { url: "", db: "local" }
  staging: { url: "", db: "seeded" }
  prod: { url: "", smoke_only: true }
  
success_criteria:
  coverage_target: 80%      # Line, branch, or statement
  performance_baseline:     # e.g., p95 < 200ms
  uptime_slo: 99.9%         # Service Level Objective
### Test Type Decision Matrix

| Risk Profile | Unit | Integration | E2E | Performance | Security | Accessibility |
|---|---|---|---|---|---|---|
| Internal tool | ✅ Core logic | ✅ API | ⚠️ Happy path | ❌ | ⚠️ Basic auth | ❌ |
| B2B SaaS | ✅ Full coverage | ✅ Full coverage | ✅ Critical flows | ✅ Load testing | ✅ OWASP Top 10 | ✅ WCAG AA |
| B2C high-traffic | ✅ Full coverage | ✅ Full coverage | ✅ Full suite | ✅ Stress + soak | ✅ Full suite | ✅ WCAG AA |
| Financial/Health | ✅ Full + mutation | ✅ Full + contract | ✅ Full + chaos | ✅ Full suite | ✅ Pen test | ✅ WCAG AAA |

### Test Pyramid Architecture

/  E2E  \          5-10% — Critical user journeys only
        / Integration \     20-30% — API contracts, service boundaries
       /    Unit Tests   \  60-70% — Business logic, pure functions
**Anti-pattern: Ice cream cone** — More E2E than unit tests. Results in slow, flaky, expensive test suites. Fix by pushing coverage DOWN the pyramid.

**Anti-pattern: Hourglass** — Lots of unit + E2E, no integration layer. Misses contract bugs between services.

---

## Phase 2: Unit Testing Mastery

### The AAA Pattern (Arrange-Act-Assert)

Every unit test follows this strict structure:

typescript
describe('PricingCalculator', () => {
  // Group by behavior, not by method name
  describe('when customer has volume discount', () => {
    
    // Arrange: Set up all dependencies and inputs
    const customer = { tier: 'gold', totalSpend: 50000 };
    const calculator = new PricingCalculator();
    
    // Act: Execute the single behavior under test
    const discount = calculator.getVolumeDiscount(customer);
    
    // Assert: Verify the expected outcome
    expect(discount).toBe(0.15);
  });
});
### Test Naming Convention

Use the format: `should [expected behavior] when [condition]`

| ❌ Bad | ✅ Good |
|--------|---------|
| `test1()` | `should return 15% discount when customer is Gold tier` |
| `testCalculate()` | `should throw ValidationError when price is negative` |
| `pricingTest()` | `should apply compound discounts when volume threshold exceeded` |

### Test Data Builders

Eliminate test setup noise with builder pattern:

typescript
// Before: Messy, repetitive setup
const user = {
  id: 'user-123',
  email: 'test@example.com',
  role: 'admin',
  preferences: { theme: 'dark', notifications: true },
  createdAt: new Date('2024-01-01')
};

// After: Intentional, readable builder
const user = new UserBuilder()
  .withRole('admin')
  .withEmail('test@example.com')
  .build();
---

## Phase 3: Integration Testing

### API Contract Testing

Validate API contracts before integration breaks production:

typescript
describe('POST /api/orders', () => {
  it('should return 201 with orderId when valid order submitted', async () => {
    const response = await request(app)
      .post('/api/orders')
      .send({ productId: 'prod-123', quantity: 2 })
      .expect(201);
    
    expect(response.body).toMatchSchema({
      type: 'object',
      required: ['orderId', 'status', 'createdAt'],
      properties: {
        orderId: { type: 'string', format: 'uuid' },
        status: { type: 'string', enum: ['pending', 'confirmed'] }
      }
    });
  });
});
### Database Integration

Test data access with transactional isolation:

typescript
describe('OrderRepository', () => {
  beforeEach(async () => {
    await db.query('BEGIN');
  });
  
  afterEach(async () => {
    await db.query('ROLLBACK'); // Clean state for each test
  });
  
  it('should persist order and return with generated ID', async () => {
    const order = new Order({ productId: 'prod-123', quantity: 1 });
    const saved = await repo.save(order);
    
    expect(saved.id).toBeDefined();
    expect(await repo.findById(saved.id)).toEqual(saved);
  });
});
---

## Phase 4: End-to-End Testing

### Critical User Flows Only

E2E tests are expensive and flaky. Test only the paths that matter:

**Always test:**
- User signup/login (authentication flow)
- Core business transaction (what users pay for)
- Checkout/payment flow
- Critical error recovery

**Never test (these belong in unit/integration):**
- Email formatting
- Date calculations
- API response parsing
- Individual component rendering

### Playwright Example

typescript
import { test, expect } from '@playwright/test';

test.describe('Checkout Flow', () => {
  test('should complete purchase with valid card', async ({ page }) => {
    await page.goto('/products/premium-plan');
    
    await page.click('[data-testid="add-to-cart"]');
    await page.click('[data-testid="checkout-button"]');
    await page.fill('[data-testid="card-number"]', '4242424242424242');
    await page.fill('[data-testid="expiry"]', '12/26');
    await page.fill('[data-testid="cvc"]', '123');
    
    await page.click('[data-testid="pay-now"]');
    
    await expect(page.locator('[data-testid="confirmation"]'))
      .toContainText('Order confirmed');
  });
});
---

## Phase 5: Performance Testing

### Load Test with k6

typescript
// k6/scenarios/checkout.ts
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 100 },  // Ramp up
    { duration: '5m', target: 100 },  // Steady state
    { duration: '2m', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% under 500ms
    http_req_failed: ['rate<0.01'],   // Error rate < 1%
  },
};

export default function () {
  const res = http.post(
    `${__ENV.BASE_URL}/api/checkout`,
    JSON.stringify({ productId: 'prod-123', quantity: 1 }),
    { headers: { 'Content-Type': 'application/json' } }
  );
  
  check(res, {
    'status is 201': (r) => r.status === 201,
    'response has orderId': (r) => !!JSON.parse(r.body).orderId,
  });
  
  sleep(1);
}
### Key Performance Indicators

| Metric | Target | Critical Threshold |
|--------|--------|-------------------|
| Response time (p95) | < 200ms | > 500ms |
| Response time (p99) | < 500ms | > 1s |
| Error rate | < 0.1% | > 1% |
| Throughput | Meets SLA | Degraded by > 20% |

---

## Phase 6: Test Coverage Analysis

### Coverage Requirements by Tier

yaml
coverage:
  # Minimum thresholds (fail build if not met)
  minimum:
    statements: 70
    branches: 65
    functions: 70
    lines: 70
    
  # Target thresholds (code review metric)
  target:
    statements: 85
    branches: 80
    functions: 90
    lines: 85
    
  # Critical paths (100% required)
  critical:
    - payment processing
    - authentication/authorization
    - data validation
### Coverage Reports in CI

yaml
# .github/workflows/test.yml
- name: Run tests with coverage
  run: npm test -- --coverage --coverageReporters=lcov
  
- name: Upload coverage
  uses: codecov/codecov-action@v4
  with:
    fail_ci_if_error: true
    thresholds: '80 85'  # Flag if below 80%, warn if below 85%
---

## Phase 7: Test Automation & CI/CD

### Pre-commit Hooks

Block bad code before it reaches version control:

bash
# .husky/pre-commit
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

npx lint-staged
npm test -- --coverage
### CI Pipeline Stages

yaml
stages:
  - name: lint
    script: eslint src --max-warnings 0
    
  - name: test:unit
    script: jest --coverage --ci
    coverage_gate: 80%
    
  - name: test:integration
    script: jest --testPathPattern=integration
    services: [postgres, redis]
    
  - name: test:e2e
    script: playwright test
    parallel: 3
    
  - name: test:performance
    script: k6 run k6/scenarios/*.ts
    trigger: manual  # Or on deploy to staging
---

## Phase 8: Test Maintenance

### Flaky Test Handling

typescript
// Mark flaky tests with retry configuration
test.describe('Flaky Network Tests', () => {
  test.use({ 
    retries: process.env.CI ? 2 : 0,
    timeout: 30000 
  });
  
  test('should fetch user profile', async ({ page }) => {
    // Test implementation
  });
});
### Test Review Checklist

Before merging, verify:

- [ ] Test names describe behavior, not implementation
- [ ] Each test has exactly one assertion focus
- [ ] Test data is realistic and deterministic
- [ ] Tests are isolated (no shared mutable state)
- [ ] Coverage meets minimum thresholds
- [ ] No commented-out tests or `todo()` items
- [ ] Performance baselines are documented

---

## Quick Reference: Testing Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Testing implementation | Breaks on refactor | Test behavior, not methods |
| Shared mutable state | Tests affect each other | Use fresh instances per test |
| Overly specific assertions | Brittle tests | Assert outcomes, not exact formats |
| Network calls in unit tests | Slow, unreliable | Mock external dependencies |
| Tests without assertions | False positives | Every test must assert something |
| Fixture abuse | Unreadable tests | Use builder pattern |
| Magic numbers | Unclear intent | Use named constants |

---

## Testing Checklist by Phase

### Before Writing Code
- [ ] Define test strategy and scope
- [ ] Identify critical user flows
- [ ] Set coverage thresholds
- [ ] Choose testing tools and frameworks

### During Development
- [ ] Write unit tests for all business logic
- [ ] Add integration tests for data access
- [ ] Maintain 80%+ coverage on new code
- [ ] Use TDD for complex algorithms

### Before Deployment
- [ ] Run full unit test suite
- [ ] Execute integration tests with real services
- [ ] Run E2E on critical paths
- [ ] Verify performance baselines
- [ ] Check accessibility compliance

### Production Monitoring
- [ ] Set up synthetic transaction monitoring
- [ ] Track error rates and latency
- [ ] Alert on coverage regression
- [ ] Review flaky tests weekly