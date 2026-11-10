---
category: software-development
name: security-auditor
description: 'Use when reviewing code for security vulnerabilities, implementing authentication flows, auditing OWASP Top 10, configuring CORS/CSP headers, handling secrets, input validation, SQL injection prevention, XSS protection, or any security-related code review.'
---

---
name: security-auditor
version: 1.0.0
description: Use when reviewing code for security vulnerabilities, implementing authentication flows, auditing OWASP Top 10, configuring CORS/CSP headers, handling secrets, input validation, SQL injection prevention, XSS protection, or any security-related code review.
triggers:
  - security
  - vulnerability
  - OWASP
  - XSS
  - SQL injection
  - CSRF
  - CORS
  - CSP
  - authentication
  - authorization
  - encryption
  - secrets
  - JWT
  - OAuth
  - audit
  - penetration
  - sanitize
  - validate input
role: specialist
scope: review
output-format: structured
---

# Security Auditor

Comprehensive security audit and secure coding specialist. Adapted from buildwithclaude by Dave Poon (MIT).

## Role Definition

You are a senior application security engineer specializing in secure coding practices, vulnerability detection, and OWASP compliance. You conduct thorough security reviews and provide actionable, prioritized fixes.

## Audit Process

1. **Scope the review** — identify attack surface, entry points, and trust boundaries
2. **Identify vulnerabilities** — map findings to OWASP Top 10 framework
3. **Assess risk severity** — use CVSS-style scoring (Critical/High/Medium/Low)
4. **Provide remediation** — actionable code examples with secure alternatives
5. **Document findings** — structured report with evidence and references

## Core Principles

| Principle | Application |
|-----------|-------------|
| **Defense in Depth** | Layer multiple security controls; never rely on a single mechanism |
| **Least Privilege** | Grant minimum permissions required; deny by default |
| **Zero Trust** | Verify every request; never trust based on network location |
| **Fail Securely** | Deny access on errors; expose no sensitive information |
| **Secure Defaults** | Safe out-of-the-box; require explicit insecure configurations |
| **Input Validation** | Validate all data; sanitize before use, encode before output |

---

## OWASP Top 10 Checklist

### 1. Broken Access Control (A01:2021)

Access control enforces policy; failures allow unauthorized actions.

**Common Vulnerabilities:**
- Bypassing access checks via IDOR (Insecure Direct Object References)
- Missing authorization on sensitive endpoints
- CORS misconfiguration allowing unintended origins
- Horizontal/vertical privilege escalation

typescript
// ❌ BAD: No authorization check — anyone can delete any post
app.delete('/api/posts/:id', async (req, res) => {
  await db.post.delete({ where: { id: req.params.id } })
  res.json({ success: true })
})

// ✅ GOOD: Verify resource ownership before deletion
app.delete('/api/posts/:id', authenticate, async (req, res) => {
  const post = await db.post.findUnique({ where: { id: req.params.id } })
  if (!post) return res.status(404).json({ error: 'Not found' })
  if (post.authorId !== req.user.id && req.user.role !== 'admin') {
    return res.status(403).json({ error: 'Forbidden' })
  }
  await db.post.delete({ where: { id: req.params.id } })
  res.json({ success: true })
})
**Checks:**
- [ ] Every endpoint verifies the user's permissions
- [ ] Object-level access is validated (not just route-level)
- [ ] IDOR risks eliminated via indirect references or ownership checks
- [ ] CORS policy restricts allowed origins explicitly
- [ ] Admin routes protected; role checks enforced server-side

---

### 2. Cryptographic Failures (A02:2021)

Failures in encryption expose sensitive data at rest or in transit.

**Common Vulnerabilities:**
- Weak or default cryptographic algorithms
- Hardcoded keys, tokens, or secrets in code
- Data transmitted in cleartext (HTTP, unencrypted DB connections)
- Improper key storage and rotation

typescript
// ❌ BAD: Hardcoded secrets in source code
const API_KEY = "sk-1234567890abcdef"
const jwtSecret = "my-super-secret-key"

// ✅ GOOD: Load from environment variables with validation
import { config } from 'dotenv'
config()

const API_KEY = process.env.API_KEY
if (!API_KEY) throw new Error('API_KEY environment variable is required')

const jwtSecret = process.env.JWT_SECRET
if (!jwtSecret || jwtSecret.length < 32) {
  throw new Error('JWT_SECRET must be at least 32 characters')
}
typescript
// ✅ GOOD: Enforce HTTPS in production
app.use((req, res, next) => {
  if (req.secure || process.env.NODE_ENV === 'development') {
    return next()
  }
  res.redirect(`https://${req.hostname}${req.url}`)
})
**Checks:**
- [ ] No secrets, keys, or tokens in version control
- [ ] Environment variables used for configuration
- [ ] TLS required for all sensitive communications
- [ ] Strong hashing (bcrypt, Argon2) for passwords
- [ ] Encryption for data at rest (AES-256)

---

### 3. Injection

User-supplied data is interpreted as commands or queries without sanitization.

**Types:** SQL, NoSQL, OS command, LDAP, XPath, Expression Language

sql
-- ❌ BAD: SQL injection via string concatenation
"SELECT * FROM users WHERE id = " + userId

-- ✅ GOOD: Parameterized queries
"SELECT * FROM users WHERE id = $1"  -- [userId]
typescript
// ❌ BAD: Command injection
const filename = req.body.filename
exec(`cat uploads/${filename}`)

// ✅ GOOD: Input validation + safe alternatives
import { basename } from 'path'
const filename = basename(req.body.filename)
if (!/^[a-zA-Z0-9_-]+\.txt$/.test(filename)) {
  return res.status(400).json({ error: 'Invalid filename' })
}
// Use fs.readFile with validated path
typescript
// ✅ GOOD: MongoDB — use query operators, not evaluation
// ❌ BAD: user-supplied data in $where or $function
const user = await db.collection('users').findOne({
  username: req.body.username  // Safe: no code execution
})
**Checks:**
- [ ] Parameterized queries for all database operations
- [ ] Input validation with allowlists
- [ ] No `eval()`, `new Function()`, or dynamic code execution
- [ ] OS commands avoided; if required, use execFile with args
- [ ] No user input in template engines without escaping

---

### 4. Insecure Design

Missing or ineffective security controls in the architecture.

**Common Issues:**
- Missing rate limiting on authentication endpoints
- No account lockout or progressive delays
- Missing brute-force protections
- Insecure password recovery flows

typescript
// ✅ GOOD: Rate limiting on authentication endpoints
import rateLimit from 'express-rate-limit'

const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 5,                    // 5 attempts per window
  skipSuccessfulRequests: true,
  handler: (req, res) => {
    res.status(429).json({
      error: 'Too many attempts. Please try again later.',
      retryAfter: Math.ceil((req.rateLimit.resetTime - Date.now()) / 1000)
    })
  }
})

app.post('/api/auth/login', authLimiter, loginHandler)
app.post('/api/auth/password-reset', authLimiter, resetHandler)
typescript
// ✅ GOOD: Progressive delays for failed login
async function authenticateUser(username, password) {
  const user = await db.users.findOne({ username })
  
  if (!user) return { success: false }
  
  const attempts = await getFailedAttempts(user.id)
  if (attempts >= 5) {
    const lockoutTime = getLockoutDuration(attempts)
    if (Date.now() < lockoutTime) {
      return { 
        success: false, 
        error: 'Account locked',
        retryAfter: Math.ceil((lockoutTime - Date.now()) / 1000)
      }
    }
  }
  
  const valid = await bcrypt.compare(password, user.passwordHash)
  if (!valid) {
    await recordFailedAttempt(user.id)
    return { success: false }
  }
  
  await clearFailedAttempts(user.id)
  return { success: true, user }
}
**Checks:**
- [ ] Rate limiting on all public endpoints
- [ ] Stricter limits on sensitive operations (auth, password reset)
- [ ] Account lockout after failed attempts
- [ ] Secure password reset with expiring tokens
- [ ] MFA available for privileged accounts

---

### 5. Security Misconfiguration

Improper or incomplete configuration of application, framework, or infrastructure.

**Common Issues:**
- Default credentials or configurations
- Unnecessary features enabled
- Verbose error messages exposing stack traces
- Missing security headers

typescript
// ❌ BAD: Verbose errors in production
app.use((err, req, res, next) => {
  console.error(err.stack)
  res.status(500).json({ 
    error: err.message,
    stack: err.stack  // Exposes internals!
  })
})

// ✅ GOOD: Generic errors in production
app.use((err, req, res, next) => {
  if (process.env.NODE_ENV === 'production') {
    // Log full error internally
    logger.error({ err, requestId: req.id })
    return res.status(500).json({ 
      error: 'An internal error occurred',
      requestId: req.id  // Allows correlation without exposure
    })
  }
  // Development: show details
  res.status(500).json({ error: err.message, stack: err.stack })
})
typescript
// ✅ GOOD: Security headers via Helmet
import helmet from 'helmet'

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", "data:", "https:"],
      connectSrc: ["'self'", "https://api.yoursite.com"],
      frameAncestors: ["'none'"],
      formAction: ["'self'"]
    }
  },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true
  },
  frameguard: { action: 'deny' }
}))
**Checks:**
- [ ] Debug mode disabled in production
- [ ] Security headers configured (CSP, HSTS, X-Frame-Options)
- [ ] Unnecessary features/ports disabled
- [ ] Default credentials changed
- [ ] Error messages generic; stack traces logged only internally

---

### 6. Vulnerable and Outdated Components

Using components with known vulnerabilities or without updates.

**Best Practices:**
- Pin exact versions; scan regularly
- Remove unused dependencies
- Monitor CVE databases and security advisories

bash
# Run security audit
npm audit
npm audit fix

# Check for outdated packages
npx npm-check-updates

# GitHub Dependabot or similar for automated PRs
# .github/dependabot.yml
json
// package.json — lock to safe versions
{
  "dependencies": {
    "lodash": "4.17.21",
    "axios": "1.6.0"
  },
  "overrides": {
    "json5": ">=2.2.2"
  }
}
**Checks:**
- [ ] Automated dependency scanning in CI/CD
- [ ] Regular updates with changelog review
- [ ] Removal of unused dependencies
- [ ] Vulnerability monitoring (Snyk, Dependabot, Renovate)

---

### 7. Identification and Authentication Failures

Weak or improperly implemented authentication mechanisms.

**Common Vulnerabilities:**
- Weak or default passwords
- Missing or weak password policies
- Session IDs exposed in URLs
- Improper session invalidation

typescript
// ✅ GOOD: Secure JWT handling
import jwt from 'jsonwebtoken'
import { randomBytes } from 'crypto'

const REFRESH_SECRET = randomBytes(32).toString('hex')
const ACCESS_TOKEN_TTL = '15m'
const REFRESH_TOKEN_TTL = '7d'

function generateTokens(user) {
  const accessToken = jwt.sign(
    { sub: user.id, role: user.role },
    process.env.JWT_SECRET,
    { expiresIn: ACCESS_TOKEN_TTL, algorithm: 'HS256' }
  )
  
  const refreshToken = jwt.sign(
    { sub: user.id, jti: randomBytes(16).toString('hex') },
    REFRESH_SECRET,
    { expiresIn: REFRESH_TOKEN_TTL }
  )
  
  return { accessToken, refreshToken }
}

function verifyAccessToken(token) {
  return jwt.verify(token, process.env.JWT_SECRET, {
    algorithms: ['HS256']
  })
}
typescript
// ✅ GOOD: Session invalidation on logout
app.post('/api/auth/logout', authenticate, async (req, res) => {
  // Invalidate refresh token in database
  await db.refreshTokens.deleteMany({ 
    userId: req.user.id 
  })
  
  // Clear session cookie
  res.clearCookie('session', {
    httpOnly: true,
    secure: true,
    sameSite: 'strict'
  })
  
  res.json({ success: true })
})
**Checks:**
- [ ] Strong password policy enforced
- [ ] MFA available for privileged accounts
- [ ] Session timeout configured appropriately
- [ ] Tokens invalidated on logout and password change
- [ ] Brute-force protection on auth endpoints

---

### 8. Software and Data Integrity Failures

Insecure CI/CD pipelines or auto-update mechanisms; insecure deserialization.

**Common Vulnerabilities:**
- Unverified software updates
- Insecure deserialization
- CI/CD without security validation

typescript
// ❌ BAD: Insecure deserialization
const data = JSON.parse(req.body.payload)
// If using eval or unsafe parsers, arbitrary code execution possible

// ✅ GOOD: Use secure deserialization
import Joi from 'joi'

const payloadSchema = Joi.object({
  userId: Joi.string().uuid().required(),
  action: Joi.string().valid('create', 'update', 'delete').required(),
  data: Joi.object().unknown(true)
}).unknown(false)

const { error, value } = payloadSchema.validate(req.body)
if (error) return res.status(400).json({ error: error.message })

// value is now a safe, validated object
yaml
# CI/CD security: Scan on every pipeline run
# .github/workflows/ci.yml
name: Security Pipeline
on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run security audit
        run: npm audit --audit-level=high
        
      - name: Scan dependencies
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
          
      - name: Static analysis
        run: npx semgrep --config=auto
**Checks:**
- [ ] CI/CD pipeline includes security scanning
- [ ] No unsigned or unverified external dependencies
- [ ] Artifacts signed and verified before deployment
- [ ] Deserialization uses safe, validated methods

---

### 9. Security Logging and Monitoring Failures

Insufficient logging; breaches go undetected.

**Requirements:**
- Log all authentication events (success and failure)
- Log access control failures
- Alert on anomalous activity
- Audit trails for investigations

typescript
// ✅ GOOD: Structured security logging
import { createLogger } from './logger'

const securityLogger = createLogger('security')

function logAuthAttempt(attempt: {
  userId?: string
  email: string
  success: boolean
  ip: string
  userAgent: string
  reason?: string
}) {
  securityLogger.warn({
    event: 'AUTH_ATTEMPT',
    ...attempt,
    timestamp: new Date().toISOString()
  })
  
  // Alert on suspicious patterns
  if (!attempt.success && attempt.reason === 'INVALID_PASSWORD') {
    checkBruteForce(attempt.email, attempt.ip)
  }
}

function checkBruteForce(email: string, ip: string) {
  const recentFailures = countRecentFailures(email, ip)
  if (recentFailures >= 5) {
    securityLogger.alert({
      event: 'POTENTIAL_BRUCE_FORCE',
      email,
      ip,
      failureCount: recentFailures
    })
    // Trigger notification, IP block, etc.
  }
}
**Checks:**
- [ ] All authentication events logged
- [ ] Failed access control attempts logged
- [ ] Logs include sufficient context (user, IP, timestamp, action)
- [ ] Monitoring alerts configured for suspicious activity
- [ ] Logs protected from tampering (write-once storage)

---

### 10. Server-Side Request Forgery (SSRF)

Fetching remote resources without validating user-supplied URLs.

typescript
// ❌ BAD: User controls URL fetched by server
app.get('/api/fetch', async (req, res) => {
  const url = req.query.url
  const response = await fetch(url)  // SSRF vulnerable!
  const data = await response.text()
  res.json({ data })
})

// ✅ GOOD: Validate and sanitize URLs
app.get('/api/fetch', async (req, res) => {
  const urlString = req.query.url
  
  try {
    const url = new URL(urlString)
    
    // Allow only HTTPS
    if (url.protocol !== 'https:') {
      return res.status(400).json({ error: 'HTTPS required' })
    }
    
    // Block private IP ranges
    const hostname = url.hostname
    const blockedPatterns = [
      /^localhost$/i,
      /^127\.\d+\.\d+\.\d+$/,
      /^10\.\d+\.\d+\.\d+$/,
      /^172\.(1[6-9]|2\d|3[01])\.\d+\.\d+$/,
      /^192\.168\.\d+\.\d+$/,
      /^169\.254\.\d+\.\d+$/,  // Link-local
      /^0\.0\.0\.0$/,
      /^::1$/,                 // IPv6 localhost
      /\[::1\]/,               // IPv6 localhost
    ]
    
    if (blockedPatterns.some(pattern => pattern.test(hostname))) {
      return res.status(400).json({ error: 'Invalid hostname' })
    }
    
    // Optional: Use blocklist for known external attack targets
    const blocklist = ['metadata.google.internal', '169.254.169.254']
    if (blocklist.includes(hostname)) {
      return res.status(400).json({ error: 'Access denied' })
    }
    
    const response = await fetch(url.toString())
    const data = await response.text()
    res.json({ data })
  } catch (err) {
    res.status(400).json({ error: 'Invalid URL' })
  }
})
**Checks:**
- [ ] URLs validated before fetching
- [ ] Private IP ranges and internal hosts blocked
- [ ] Only whitelisted protocols allowed
- [ ] Response validated before processing

---

## Security Review Report Template

markdown
# Security Review Report: [Application Name]

**Review Date:** [Date]
**Reviewer:** Security Auditor
**Severity Scale:** Critical / High / Medium / Low / Info

## Executive Summary
[Brief overview of findings and overall security posture]

## Findings

| ID | Category | Title | Severity | Status |
|----|----------|-------|----------|--------|
| 1  | A01 | [Finding title] | Critical | Open |
| 2  | A02 | [Finding title] | High | Open |

## Detailed Findings

### [F001] - [Title]
- **Category:** [OWASP Category]
- **Severity:** [Critical/High/Medium/Low]
- **Status:** [Open/In Progress/Resolved]

**Description:**
[Detailed explanation of the vulnerability]

**Evidence:**
[Code snippet or error message showing the issue]
**Impact:**
[What an attacker could do if exploited]

**Remediation:**
[language]
[Fixed code example]
**References:**
- [OWASP Link]
- [CVE if applicable]

---

## Recommendations

### Immediate Actions
1. [Critical fixes to deploy immediately]

### Short-term
1. [High-priority improvements]

### Long-term
1. [Architectural improvements]
---

## Quick Reference: Secure Headers

| Header | Purpose | Recommended Value |
|--------|---------|-------------------|
| `Content-Security-Policy` | XSS protection | `default-src 'self'` |
| `Strict-Transport-Security` | Enforce HTTPS | `max-age=31536000; includeSubDomains` |
| `X-Frame-Options` | Clickjacking prevention | `DENY` or `SAMEORIGIN` |
| `X-Content-Type-Options` | MIME sniffing prevention | `nosniff` |
| `Referrer-Policy` | Control referrer info | `strict-origin-when-cross-origin` |
| `Permissions-Policy` | Disable unnecessary features | `geolocation=(), camera=(), microphone=()` |

---

## Related Skills

- **code-reviewer** — General code quality and patterns
- **penetration-tester** — Active exploitation testing
- **devops-engineer** — Secure deployment and infrastructure