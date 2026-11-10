---
category: software-development
description: "> The definitive testing methodology for AI agents. From test strategy to execution, coverage to reporting — everything you need to ship quality software."
name: afrexai-qa-testing-engine
---

# QA & Testing Engine — Complete Software Quality System

> The definitive testing methodology for AI agents. From test strategy to execution, coverage to reporting — everything you need to ship quality software.

## Phase 1: Test Strategy Design

Before writing a single test, design the strategy. A clear strategy prevents wasted effort on low-value tests while ensuring critical paths are covered.

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
  in_scope: []    # Features, services, components
  out_of_scope: [] # Explicitly excluded (with reason)

environments:
  dev: { url: "", db: "local" }
  staging: { url: "", db: "seeded" }
  prod: { url: "", smoke_only: true }
### Test Type Decision Matrix

| Risk Profile | Unit | Integration | E2E | Performance | Security | Accessibility |
|---|---|---|---|---|---|---|
| Internal tool | ✅ Core | ✅ API | ⚠️ Happy path | ❌ | ⚠️ Basic | ❌ |
| B2B SaaS | ✅ Full | ✅ Full | ✅ Critical flows | ✅ Load | ✅ OWASP Top 10 | ✅ WCAG AA |
| B2C high-traffic | ✅ Full | ✅ Full | ✅ Full | ✅ Stress + soak | ✅ Full | ✅ WCAG AA |
| Financial/Health | ✅ Full + mutation | ✅ Full + contract | ✅ Full + chaos | ✅ Full suite | ✅ Pen test | ✅ WCAG AAA |

### Test Pyramid Architecture

/  E2E  \          5-10% — Critical user journeys only
        / Integration \     20-30% — API contracts, service boundaries
       /    Unit Tests   \  60-70% — Business logic, pure functions
**Anti-pattern: Ice cream cone** — More E2E than unit tests. Slow, flaky, expensive. Fix by pushing test coverage DOWN the pyramid.

**Anti-pattern: Hourglass** — Lots of unit + E2E, no integration. Misses contract bugs between services.

---

## Phase 2: Unit Testing Mastery

### The AAA Pattern (Arrange-Act-Assert)

Every unit test follows this structure:

typescript
describe('PricingCalculator', () => {
  // Group by behavior, not by method
  describe('when customer has volume discount', () => {
    it('applies correct percentage to base price', () => {
      // Arrange
      const calculator = new PricingCalculator();
      const customer = { basePrice: 100, tier: 'gold', discountPercent: 15 };

      // Act
      const result = calculator.calculate(customer);

      // Assert
      expect(result).toBe(85);
    });

    it('never returns negative price', () => {
      // Arrange
      const calculator = new PricingCalculator();
      const customer = { basePrice: 10, tier: 'vip', discountPercent: 150 };

      // Act
      const result = calculator.calculate(customer);

      // Assert
      expect(result).toBeGreaterThanOrEqual(0);
    });
  });
});
### Naming Conventions

**Pattern:** `describe('[Unit]')` → `describe('[scenario]')` → `it('[expected behavior]')`

| ❌ Bad | ✅ Good |
|--------|---------|
| `test('test1')` | `describe('calculateTotal')` |
| `test('should work')` | `it('returns 0 for empty cart')` |
| `test('pricing test')` | `it('applies tier discount correctly')` |

### What to Test in Unit Tests

**✅ Always test:**
- Business logic and calculations
- Data transformations
- Input validation and edge cases
- Error handling paths
- State transitions

**❌ Never test (delegate to integration/E2E):**
- Framework behavior (React renders, Express routing)
- Database operations
- External API calls
- File system operations

### Test Edge Cases First

python
# Example in Python
class TestFibonacci:
    def test_returns_0_for_position_0(self):
        assert fibonacci(0) == 0

    def test_returns_1_for_position_1(self):
        assert fibonacci(1) == 1

    def test_returns_55_for_position_10(self):
        assert fibonacci(10) == 55

    def test_raises_for_negative_input(self):
        with pytest.raises(ValueError):
            fibonacci(-1)

    def test_raises_for_non_integer(self):
        with pytest.raises(TypeError):
            fibonacci(3.14)
---

## Phase 3: Integration Testing

### Scope and Purpose

Integration tests verify that components work correctly together — databases, APIs, message queues, and external services.

### Database Testing Patterns

typescript
describe('UserRepository', () => {
  let db: TestDatabase;
  let repo: UserRepository;

  beforeEach(async () => {
    db = await TestDatabase.create();
    repo = new UserRepository(db.connection);
  });

  afterEach(async () => {
    await db.cleanup();
  });

  describe('findById', () => {
    it('returns user with all relations loaded', async () => {
      // Arrange
      const userId = await repo.create({
        email: 'test@example.com',
        role: 'admin'
      });

      // Act
      const user = await repo.findById(userId);

      // Assert
      expect(user).toMatchObject({
        id: userId,
        email: 'test@example.com',
        role: 'admin',
        createdAt: expect.any(Date)
      });
    });

    it('returns null for non-existent id', async () => {
      const user = await repo.findById(99999);
      expect(user).toBeNull();
    });
  });
});
### API Contract Testing

typescript
describe('Orders API', () => {
  describe('POST /api/orders', () => {
    it('validates required fields', async () => {
      const response = await request(app)
        .post('/api/orders')
        .send({});

      expect(response.status).toBe(400);
      expect(response.body.errors).toContainEqual({
        field: 'customerId',
        message: 'Customer ID is required'
      });
    });

    it('creates order and returns 201', async () => {
      const response = await request(app)
        .post('/api/orders')
        .send({
          customerId: 'cust_123',
          items: [{ productId: 'prod_456', quantity: 2 }]
        });

      expect(response.status).toBe(201);
      expect(response.body).toMatchObject({
        id: expect.any(String),
        status: 'pending'
      });
    });
  });
});
---

## Phase 4: End-to-End Testing

### When to Use E2E

E2E tests simulate real user scenarios from start to finish. Use sparingly for:

- Critical user journeys (login, checkout, signup)
- High-value business processes
- Regression protection for key features

### E2E Best Practices

typescript
// Use page objects for maintainability
class LoginPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.page.fill('[data-testid="email-input"]', email);
    await this.page.fill('[data-testid="password-input"]', password);
    await this.page.click('[data-testid="login-button"]');
  }

  async expectError(message: string) {
    await expect(
      this.page.locator('[data-testid="error-message"]')
    ).toHaveText(message);
  }
}

// Test file
describe('Authentication Flow', () => {
  test('user can login with valid credentials', async ({ page }) => {
    const loginPage = new LoginPage(page);
    
    await loginPage.goto();
    await loginPage.login('user@example.com', 'validpassword');
    
    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('[data-testid="welcome-message"]'))
      .toContainText('Welcome back');
  });

  test('shows error for invalid credentials', async ({ page }) => {
    const loginPage = new LoginPage(page);
    
    await loginPage.goto();
    await loginPage.login('user@example.com', 'wrongpassword');
    
    await loginPage.expectError('Invalid email or password');
  });
});
---

## Phase 5: Performance Testing

### Types of Performance Tests

| Type | Purpose | Metrics |
|------|---------|---------|
| Load | Verify system under expected load | Response time, throughput |
| Stress | Find breaking point | Max users, failure mode |
| Soak | Detect memory leaks | Resource usage over time |
| Spike | Test sudden traffic changes | Recovery time |

### Load Testing Example

yaml
# k6 script configuration
scenarios:
  smoke:
    executor: constant-vus
    vus: 10
    duration: 30s
    tags:
      test_type: smoke

  load:
    executor: ramping-vus
    start_vus: 0
    stages:
      - duration: 2m, target: 100   # Ramp up
      - duration: 5m, target: 100   # Steady state
      - duration: 2m, target: 0     # Ramp down
    thresholds:
      http_req_duration: ['p(95)<500']
      http_req_failed: ['rate<0.01']
### Performance Benchmarks

typescript
describe('API Performance', () => {
  describe('GET /api/products', () => {
    it('responds within 200ms for cached requests', async () => {
      const start = performance.now();
      
      await request(app).get('/api/products?page=1&limit=20');
      
      const duration = performance.now() - start;
      expect(duration).toBeLessThan(200);
    });

    it('handles 100 concurrent requests', async () => {
      const promises = Array(100).fill(null).map(() =>
        request(app).get('/api/products')
      );
      
      const responses = await Promise.all(promises);
      const allSuccessful = responses.every(r => r.status === 200);
      
      expect(allSuccessful).toBe(true);
    });
  });
});
---

## Phase 6: Security Testing

### Security Test Checklist

- [ ] **Authentication** — Login, logout, session timeout, password requirements
- [ ] **Authorization** — Role-based access, privilege escalation attempts
- [ ] **Input Validation** — SQL injection, XSS, command injection
- [ ] **Data Exposure** — API responses, error messages, logs
- [ ] **Cryptography** — Sensitive data in transit and at rest

### Security Test Examples

typescript
describe('Security: Authentication', () => {
  it('locks account after 5 failed attempts', async () => {
    for (let i = 0; i < 5; i++) {
      await request(app)
        .post('/api/auth/login')
        .send({ email: 'locked@example.com', password: 'wrong' });
    }

    const response = await request(app)
      .post('/api/auth/login')
      .send({ email: 'locked@example.com', password: 'correct' });

    expect(response.status).toBe(423);
    expect(response.body.message).toContain('locked');
  });

  it('rejects weak passwords during registration', async () => {
    const response = await request(app)
      .post('/api/auth/register')
      .send({ email: 'new@example.com', password: '123' });

    expect(response.status).toBe(400);
    expect(response.body.errors).toContainEqual(
      expect.objectContaining({ field: 'password' })
    );
  });
});

describe('Security: Injection Prevention', () => {
  it('prevents SQL injection in search', async () => {
    const response = await request(app)
      .get("/api/users?search=' OR '1'='1");

    // Should not return all users
    expect(response.body.users).toHaveLength(0);
    expect(response.status).toBe(200);
  });

  it('sanitizes XSS payloads', async () => {
    const response = await request(app)
      .post('/api/posts')
      .send({ 
        title: '<script>alert("xss")</script>',
        content: 'Normal content'
      });

    const post = response.body;
    expect(post.title).not.toContain('<script>');
    expect(post.title).toContain('&lt;script&gt;');
  });
});
---

## Phase 7: Test Coverage & Reporting

### Coverage Metrics

| Metric | Target | Purpose |
|--------|--------|---------|
| Line Coverage | >80% | Basic indicator |
| Branch Coverage | >75% | Decision points |
| Function Coverage | 100% | All functions tested |
| Statement Coverage | >85% | Executable statements |

### Coverage Configuration

json
{
  "coverageThreshold": {
    "global": {
      "branches": 75,
      "functions": 90,
      "lines": 80,
      "statements": 80
    },
    "./src/domain/**/*.ts": {
      "branches": 90,
      "functions": 100,
      "lines": 95
    }
  }
}
### Test Reports

Generate comprehensive reports for stakeholders:

bash
# Generate HTML coverage report
npx jest --coverage --coverageReporters=html --coverageReporters=lcov

# Generate CI-friendly summary
npx jest --coverage --coverageReporters=text-summary

# Generate badge data for README
npx jest --coverage --coverageReporters=json-summary
### Coverage Anti-Patterns

**❌ Don't chase 100% coverage — it's a vanity metric.**

**✅ Focus on:**
- Critical business logic (100% coverage required)
- Edge cases and error handling
- Security-sensitive code paths
- Data validation and transformation

---

## Phase 8: Test Execution & CI/CD

### Running Tests Strategically

yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
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
      redis:
        image: redis:7
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run test:integration

  e2e-tests:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run build
      - run: npm run test:e2e
### Test Selection Strategy

| Trigger | Tests Run |
|---------|-----------|
| Every push | Unit tests |
| PR opened | Unit + Integration |
| Main branch | Full suite + E2E |
| Pre-deploy | Smoke tests |
| Scheduled (nightly) | Full suite with coverage |

### Test Execution Tips

bash
# Run tests in parallel (Jest)
npm test -- --maxWorkers=4

# Run only changed tests (affected)
npx jest --changedSince=origin/main

# Run tests with specific tags
npm test -- --grep="integration"

# Debug a single test
npm test -- --testNamePattern="specific test" --runInBand

# Generate test report
npm test -- --json --outputFile=test-results.json
---

## Quick Reference

### Test Type Selection

Q: Is it business logic?           → Unit Test
Q: Does it involve data storage?   → Integration Test
Q: Does it span multiple systems?  → E2E Test
Q: Does it need to be fast?        → Unit Test
Q: Is it a critical user journey? → E2E Test
### When to Debug vs. Write a Test

| Situation | Action |
|-----------|--------|
| Bug in business logic | Write a failing unit test, then fix |
| Bug in integration | Write a failing integration test, then fix |
| UI rendering issue | Write E2E test, debug manually |
| Flaky test | Isolate dependencies, mock external calls |
| Test runs >5min | Split into parallel jobs |

---

## Testing Philosophy

**The best tests are:**

1. **Fast** — Run in milliseconds, enable TDD
2. **Isolated** — No dependencies between tests
3. **Deterministic** — Same result every time
4. **Self-contained** — No external services required
5. **Maintainable** — Clear intent, easy to update

**Remember:**
- Tests are documentation — they describe expected behavior
- A passing test proves nothing; a failing test proves the test works
- If it's hard to test, the design may need improvement
- Perfect coverage doesn't mean perfect code — it means nothing is missed intentionally