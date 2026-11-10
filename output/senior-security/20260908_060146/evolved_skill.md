---
category: software-development
name: senior-security
description: Security engineering toolkit for threat modeling, vulnerability analysis, secure architecture design, and penetration testing. Includes STRIDE methodology, OWASP guidance, cryptography patterns, and security scanning tools. Use when the user asks about security reviews, threat analysis, vulnerability assessments, secure coding practices, security audits, attack surface analysis, CVE remediation, or security best practices.
triggers:
  - security architecture
  - threat modeling
  - STRIDE analysis
  - penetration testing
  - vulnerability assessment
  - secure coding
  - OWASP
  - application security
  - cryptography implementation
  - secret scanning
  - security audit
  - zero trust
  - CVE remediation
  - security best practices
  - attack surface analysis
---

# Senior Security Engineer

Comprehensive security engineering toolkit for threat modeling, vulnerability analysis, secure architecture design, secure code review, and incident response.

---

## Table of Contents

- [Threat Modeling Workflow](#threat-modeling-workflow)
- [Security Architecture Workflow](#security-architecture-workflow)
- [Vulnerability Assessment Workflow](#vulnerability-assessment-workflow)
- [Secure Code Review Workflow](#secure-code-review-workflow)
- [Cryptography Patterns](#cryptography-patterns)
- [Incident Response Workflow](#incident-response-workflow)
- [Security Tools Reference](#security-tools-reference)
- [Common Vulnerabilities Reference](#common-vulnerabilities-reference)

---

## Threat Modeling Workflow

### When to Use

Conduct threat modeling when designing new systems, making significant architectural changes, or before major releases. Aim to complete during design phase—remediating threats post-deployment costs 30-100x more.

### Workflow: Conduct Threat Model

**Step 1: Define System Scope**

Identify and document:
├── Assets to protect (data, systems, reputation)
├── Trust boundaries (network zones, authentication checkpoints)
├── System boundaries (what's in scope vs. out of scope)
└── User roles and privilege levels
**Step 2: Create Data Flow Diagram (DFD)**

Model the system with these elements:

| Element | Symbol | Examples |
|---------|--------|----------|
| External Entity | Square | Users, third-party APIs, partner services |
| Process | Circle | Application services, microservices, daemons |
| Data Store | Open Rectangle | Databases, caches, file systems, message queues |
| Data Flow | Arrow | HTTP requests, API calls, database queries, events |

**Step 3: Apply STRIDE to Each DFD Element**

STRIDE categorizes threats by the security property they violate:

| Category | Threat | Security Property | Common Mitigations |
|----------|--------|-------------------|-------------------|
| **S**poofing | Impersonate legitimate user/component | Authentication | Strong auth, MFA, certificates, session management |
| **T**ampering | Modify data or code | Integrity | Digital signatures, HMAC, input validation, integrity checks |
| **R**epudiation | Deny performing an action | Non-repudiation | Audit logs, digital signatures, immutable logging |
| **I**nformation Disclosure | Expose sensitive data | Confidentiality | Encryption (TLS, at-rest), access controls, data masking |
| **D**enial of Service | Make system unavailable | Availability | Rate limiting, redundancy, load balancing, CDN |
| **E**levation of Privilege | Gain unauthorized capabilities | Authorization | Principle of least privilege, RBAC, input validation |

**STRIDE Per Element Matrix:**

| Element Type | Applicable STRIDE Categories |
|--------------|------------------------------|
| External Entity | Spoofing, Repudiation |
| Process | All STRIDE categories |
| Data Store | Tampering, Information Disclosure, Denial of Service |
| Data Flow | Tampering, Information Disclosure, Denial of Service |

**Step 4: Score Risks Using DREAD**

Quantify each threat's risk:

| Factor | Description | Scoring (1-10) |
|--------|-------------|-----------------|
| **D**amage | How severe is the impact if exploited? | 10 = catastrophic, 5 = minor, 1 = negligible |
| **R**eproducibility | How consistent is the exploit? | 10 = always, 5 = sometimes, 1 = theoretical |
| **E**xploitability | How hard to exploit? | 10 = trivial, 5 = moderate, 1 = requires nation-state resources |
| **A**ffected Users | What percentage of users are impacted? | 10 = all, 5 = many, 1 = single user |
| **D**iscoverability | How easy to find this vulnerability? | 10 = public exploit, 5 = requires research, 1 = unknown |

**Risk Score = (D + R + E + A + D) / 5**

| Score Range | Risk Level | Action |
|-------------|------------|--------|
| 8-10 | Critical | Immediate remediation required |
| 6-8 | High | Remediate within sprint/iteration |
| 4-6 | Medium | Schedule for next release |
| 1-4 | Low | Accept risk or defer |

**Step 5: Define and Document Mitigations**

For each threat, specify:

Threat: [Name]
STRIDE Category: [Category]
Risk Score: [X/10]
Affected Component: [Component name]
Mitigation:
  - Type: [Prevent/Detect/Respond]
  - Implementation: [Specific control]
  - Status: [Implemented/Planned/Accepted]
---

## Security Architecture Workflow

### Zero Trust Architecture Principles

Implement zero trust using the **Never Trust, Always Verify** principle:

┌─────────────────────────────────────────────────────────────────┐
│                    ZERO TRUST ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────────┤
│  1. Verify Explicitly                                            │
│     - Authenticate and authorize based on ALL available data     │
│     - Identity, location, device health, service, data, workload│
│                                                                  │
│  2. Use Least Privileged Access                                 │
│     - Limit user access with just-in-time and just-enough-access │
│     - Policy-based access decisions                              │
│                                                                  │
│  3. Assume Breach                                                │
│     - Minimize blast radius and segment access                  │
│     - Verify end-to-end encryption                               │
│     - Use analytics to get visibility and threat detection       │
└─────────────────────────────────────────────────────────────────┘
### Security Architecture Review Checklist

| Category | Checklist Item | Priority |
|----------|---------------|----------|
| Authentication | MFA implemented for all user access | Required |
| Authentication | Secure session management with proper timeouts | Required |
| Authorization | Role-based access control (RBAC) implemented | Required |
| Authorization | API uses OAuth 2.0 / OIDC for service auth | Required |
| Data | Encryption at rest for sensitive data | Required |
| Data | TLS 1.2+ for all network communication | Required |
| Data | Secrets managed via vault, not in code | Required |
| Logging | Security events logged with integrity protection | Required |
| Network | Defense in depth with network segmentation | Required |
| Network | WAF in front of public-facing applications | High |
| Infrastructure | Auto-scaling with DDoS protection | High |
| Compliance | Audit trail for access to sensitive resources | Required |

### Common Security Architecture Patterns

**Pattern 1: API Gateway Security**

Client → [TLS] → API Gateway → [mTLS] → Backend Services
                    ↓
              [Auth + Rate Limiting + WAF]
**Pattern 2: Microservices Security**

[Service Mesh with mTLS]
[Sidecar proxies for auth + encryption]
[Centralized policy enforcement point]
**Pattern 3: Database Security**

[Application] → [Connection Pool] → [Database]
                     ↓
              [Transparent Data Encryption]
              [Column-level encryption for PII]
              [Audit logging on all queries]
---

## Vulnerability Assessment Workflow

### OWASP Top 10 (2021)

| Rank | Category | Description | Common Fixes |
|------|----------|-------------|--------------|
| A01 | Broken Access Control | Unauthorized access to functionality/data | Implement proper authorization checks, deny by default |
| A02 | Cryptographic Failures | Data exposure due to weak crypto | Use strong algorithms, proper key management, encrypt sensitive data |
| A03 | Injection | SQL, NoSQL, OS command injection | Input validation, parameterized queries, context-aware escaping |
| A04 | Insecure Design | Missing or inadequate security controls | Threat modeling, secure design patterns, security testing |
| A05 | Security Misconfiguration | Improperly configured permissions, exposures | Hardening guides, automated configuration checks |
| A06 | Vulnerable Components | Using components with known vulnerabilities | Dependency scanning, inventory, timely patching |
| A07 | Auth Failures | Broken authentication mechanisms | Multi-factor auth, secure session management, password policies |
| A08 | Software/Data Integrity | Code/infrastructure integrity failures | Verify signatures, use secure CI/CD, code review |
| A09 | Security Logging Failures | Insufficient logging/monitoring | Log security events, centralized logging, alerting |
| A10 | SSRF | Server-side request forgery | Validate/sanitize user input, deny by default |

### Vulnerability Assessment Process

1. Reconnaissance
   ├── Passive: OSINT, DNS records, certificate transparency
   ├── Active: Port scanning, service enumeration
   └── Credentialed: Authenticated scans of internal systems

2. Vulnerability Identification
   ├── Automated: Nessus, Qualys, OpenVAS, Trivy
   ├── Manual: Code review, penetration testing
   └── Code analysis: Semgrep, SonarQube, Bandit

3. Vulnerability Analysis
   ├── Confirm exploitability
   ├── Assess impact
   ├── Identify compensating controls
   └── Assign CVSS score

4. Remediation Planning
   ├── Prioritize by risk
   ├── Define remediation steps
   ├── Assign ownership
   └── Set timeline

5. Verification
   ├── Confirm fix deployed
   └── Re-scan to verify closure
### CVSS Scoring Guide

| Base Score | Severity | Description |
|------------|----------|-------------|
| 0.0 | None | No vulnerability |
| 0.1-3.9 | Low | Minimal impact, unlikely to be exploited |
| 4.0-6.9 | Medium | Moderate impact, some exploitability |
| 7.0-8.9 | High | Significant impact, exploitable |
| 9.0-10.0 | Critical | Severe impact, trivial exploitation |

### CVE Remediation Process

When remediating a CVE:

1. Identify Scope
   - Determine affected components
   - Check dependencies for transitive exposure
   - Document attack surface

2. Assess Impact
   - CVSS score and vector
   - Availability of public exploit
   - Presence in your environment

3. Apply Fix (in priority order)
   - Upgrade to patched version
   - Apply vendor-provided workaround
   - Implement compensating control
   - Accept risk (with documentation)

4. Verify
   - Confirm fix applied
   - Re-scan
   - Test functionality
---

## Secure Code Review Workflow

### Code Review Focus Areas

| Category | What to Check | Red Flags |
|----------|--------------|-----------|
| **Input Validation** | All user inputs validated, sanitized | Raw SQL queries, unvalidated redirects, file uploads without checks |
| **Authentication** | Secure password storage, session handling | MD5/sha1 for passwords, predictable session IDs, no timeout |
| **Authorization** | Checked on every request, deny by default | IDOR vulnerabilities, missing role checks, horizontal privilege escalation |
| **Cryptography** | Proper algorithms, key management | Custom crypto, hardcoded keys, weak defaults |
| **Error Handling** | No information disclosure | Stack traces in responses, detailed error messages |
| **Logging** | Security events logged, PII protected | Logging credentials, sensitive data, or full request bodies |
| **Dependencies** | Known vulnerabilities, license compliance | Outdated libraries, malicious packages |

### Secure Coding Checklist by Language

**Python:**

python
# ❌ INSECURE: SQL Injection
query = f"SELECT * FROM users WHERE id = {user_id}"
cursor.execute(query)

# ✅ SECURE: Parameterized query
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))

# ❌ INSECURE: Hardcoded secret
api_key = "sk-1234567890abcdef"

# ✅ SECURE: Environment variable
import os
api_key = os.environ.get("API_KEY")

# ❌ INSECURE: Insecure random
import random
session_id = random.randint(1000000, 9999999)

# ✅ SECURE: Cryptographically secure
import secrets
session_id = secrets.token_urlsafe(32)
**JavaScript/Node.js:**

javascript
// ❌ INSECURE: Eval with user input
const userCode = req.body.code;
eval(userCode);

// ✅ SECURE: Avoid eval, use safe alternatives
const safeEval = (code) => {
  // Use sandboxed VM or whitelist approach
};

// ❌ INSECURE: Regex DoS (ReDoS)
const regex = /^([a-zA-Z]+)*$/; // Catastrophic backtracking

// ✅ SECURE: Safe regex patterns
const regex = /^[a-zA-Z]+$/;

// ❌ INSECURE: Timing attack vulnerable comparison
if (userPass === storedPass) { return true; }

// ✅ SECURE: Constant-time comparison
const crypto = require('crypto');
const isValid = crypto.timingSafeEqual(
  Buffer.from(userPass), 
  Buffer.from(storedPass)
);
### Secret Scanning Patterns

Detect secrets in code using these regex patterns:

| Secret Type | Pattern | Priority |
|-------------|---------|----------|
| AWS Access Key | `AKIA[0-9A-Z]{16}` | Critical |
| AWS Secret Key | `(?i)aws(.{0,20})?-?[0-9a-zA-Z\/+]{40}` | Critical |
| GitHub Token | `gh[pousr]_[A-Za-z0-9_]{36,255}` | Critical |
| Private Key | `-----BEGIN (RSA\|DSA\|EC\|OPENSSH) PRIVATE KEY-----` | Critical |
| API Key (Generic) | `(?i)(api[_-]?key\|apikey)\s*[:=]\s*['\"]?[a-zA-Z0-9]{16,}` | High |
| JWT Token | `eyJ[A-Za-z0-9_-]*\.eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*` | High |
| Database URL | `mysql://\|postgres://\|mongodb://` | High |
| Slack Token | `xox[baprs]-[0-9]{10,13}-[0-9]{10,13}[a-zA-Z0-9-]*` | High |

---

## Cryptography Patterns

### When to Use Cryptography

| Use Case | Algorithm | Notes |
|----------|-----------|-------|
| Data at rest encryption | AES-256-GCM | Use hardware security modules (HSM) for keys |
| Data in transit (TLS) | TLS 1.3 | TLS 1.2 as fallback only |
| Password storage | Argon2id | bcrypt as fallback; never MD5/sha1 |
| Message signing | Ed25519 or ECDSA (P-256) | Use established curves |
| Key exchange | X25519 or ECDH (P-256) | Never roll your own |
| Hashing (non-crypto) | SHA-256 | For checksums, integrity verification |
| Random number generation | OS CSPRNG | `secrets` module in Python, `crypto.getRandomValues()` in JS |

### Secure Password Storage

# ✅ SECURE: Argon2id (recommended)
import hashlib
import secrets

def hash_password(password: str) -> tuple[str, str, str]:
    salt = secrets.token_bytes(32)
    # Use a library like argon2-cffi in production
    hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 600000)
    return salt.hex(), hash.hex(), "sha256"

# ✅ SECURE: bcrypt (acceptable)
import bcrypt
salt = bcrypt.gensalt(rounds=12)
hash = bcrypt.hashpw(password.encode(), salt)

# ❌ NEVER: MD5
hash = hashlib.md5(password.encode())  # FAST = BAD for passwords

# ❌ NEVER: SHA-1
hash = hashlib.sha1(password.encode())  # Deprecated

# ❌ NEVER: SHA-256 without salt/iterations
hash = hashlib.sha256(password.encode())  # Too fast
### TLS Configuration

nginx
# ✅ SECURE: Modern TLS configuration
ssl_protocols TLSv1.3;
ssl_ciphers TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256;
ssl_prefer_server_ciphers off;
ssl_session_timeout 1d;
ssl_session_tickets off;
ssl_stapling on;
ssl_stapling_verify on;
add_header Strict-Transport-Security "max-age=63072000" always;
add_header X-Frame-Options DENY always;
add_header X-Content-Type-Options nosniff always;
---

## Incident Response Workflow

### Incident Classification

| Severity | Definition | Response Time | Examples |
|----------|------------|---------------|----------|
| P1 - Critical | Active breach, data exfiltration, ransomware | Immediate (<15 min) | Confirmed RCE, database breach |
| P2 - High | Significant vulnerability exploited, potential data access | 1 hour | Unauthenticated LFI, SSRF with data exposure |
| P3 - Medium | Vulnerability discovered, no evidence of exploitation | 24 hours | Stored XSS, IDOR without confirmed access |
| P4 - Low | Informational finding, hardening opportunity | 1 week | Missing security headers, weak cipher suites |

### Incident Response Phases

┌─────────────────────────────────────────────────────────────────┐
│                    INCIDENT RESPONSE LIFECYCLE                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │ PREPARE  │───▶│ DETECT   │───▶│ CONTAIN  │───▶│ ERADICATE│  │
│  │ & TRAIN  │    │ & ANALYZE│    │ & STABILIZE   │ & FIX   │  │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘  │
│                                              │                  │
│       ┌──────────────────────────────────────┘                  │
│       ▼                                                         │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                   │
│  │ LESSONS  │◀───│ RECOVER  │◀───│ RESTORE  │                   │
│  │ LEARNED  │    │ & RETURN │    │ SERVICES │                   │
│  └──────────┘    └──────────┘    └──────────┘                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
### Incident Response Checklist

**Containment (First Hour):**

□ Isolate affected systems (network segmentation, taking offline)
□ Preserve evidence (disk images, memory dumps, logs)
□ Block malicious IPs/accounts
□ Revoke compromised credentials
□ Enable enhanced logging/monitoring
□ Notify security team and stakeholders
□ Initiate communication plan
**Eradication (1-24 Hours):**

□ Identify root cause
□ Remove malware/backdoors
□ Patch vulnerabilities exploited
□ Reset compromised credentials
□ Update firewall/WAF rules
□ Verify no lateral movement
□ Document timeline
**Recovery (1-7 Days):**

□ Restore from clean backups
□ Gradually restore services (phased approach)
□ Monitor for re-exploitation
□ Validate integrity of restored systems
□ Continue enhanced monitoring
□ Coordinate with legal/PR if needed
**Post-Incident (1-4 Weeks):**

□ Conduct lessons learned review
□ Update incident response procedures
□ Implement preventive measures
□ Update detection rules
□ Schedule follow-up review
□ Close incident documentation
---

## Security Tools Reference

### Static Application Security Testing (SAST)

| Tool | Language | Cost | Notes |
|------|----------|------|-------|
| Semgrep | Multi | Free/Paid | Rule-based, great for custom patterns |
| SonarQube | Multi | Free/Paid | CI/CD integration, broad language support |
| Bandit | Python | Free | Python-specific security issues |
| CodeQL | Multi | Free | GitHub-native, query-based |
| Checkmarx | Multi | Paid | Enterprise-grade, comprehensive |

### Dynamic Application Security Testing (DAST)

| Tool | Type | Cost | Notes |
|------|------|------|-------|
| OWASP ZAP | Scanner | Free | Full-featured, CI/CD friendly |
| Burp Suite | Scanner/Proxy | Paid | Industry standard for pentesters |
| Nuclei | Scanner | Free | Template-based, fast scanning |
| sqlmap | SQL Injection | Free | Specialized for SQL injection |

### Dependency Scanning

| Tool | Language | Cost | Notes |
|------|----------|------|-------|
| Trivy | Multi | Free | Container and dependency scanning |
| Snyk | Multi | Free/Paid | Excellent integration, fix recommendations |
| Dependabot | Multi | Free | GitHub-native, automated PRs |
| Grype | Multi | Free | Fast, container-focused |
| npm audit | JavaScript | Free | Built into npm |

### Infrastructure Scanning

| Tool | Type | Cost | Notes |
|------|------|------|-------|
| Trivy | Containers | Free | Vulnerability scanner for containers |
| Clair | Containers | Free | Static analysis for container vulnerabilities |
| Anchore | Containers | Free/Paid | Deep image analysis |
| Terrascan | IaC | Free | Terraform, Kubernetes, Docker |
| Checkov | IaC | Free | Terraform, CloudFormation, Kubernetes |

### Secret Scanning

| Tool | Type | Cost | Notes |
|------|------|------|-------|
| Gitleaks | Repository | Free | Pre-commit and CI integration |
| TruffleHog | Repository | Free | Finds secrets in git history |
| GitGuardian | Repository | Paid | Real-time monitoring, high accuracy |
| Semgrep Supply Chain | Dependencies | Paid | Malware detection in packages |

---

## Common Vulnerabilities Reference

### Injection Vulnerabilities

**SQL Injection:**

# Blind SQL Injection Detection
' OR 1=1 --
' AND 1=1 --
' UNION SELECT NULL--

# Time-based Detection
' WAITFOR DELAY '00:00:05'--
' OR SLEEP(5)--
**Command Injection:**

# Linux
; whoami
| cat /etc/passwd
$(whoami)
`id`

# Windows
& dir
| type C:\Windows\win.ini
### Authentication Bypass Patterns

| Technique | Description | Test Case |
|-----------|-------------|-----------|
| IDOR | Insecure Direct Object Reference | Change ID parameter in request |
| Parameter Tampering | Modify hidden fields, cookies | Change role=user to role=admin |
| Session Hijacking | Steal/forge session tokens | Use another user's valid session |
| Brute Force | Automated credential guessing | 1000s of attempts with rate limiting bypass |
| Credential Stuffing | Use leaked credentials | Test credentials from other breaches |

### SSRF Exploitation

# Basic SSRF
?url=http://localhost/internal-api

# Cloud Metadata
?url=http://169.254.169.254/latest/meta-data/
?url=http://metadata.google.internal/

# File Access
?url=file:///etc/passwd
?url=file:///proc/self/environ
---

## Quick Reference Commands

### Git Security Audit

bash
# Find secrets in git history
gitleaks detect --source . --verbose

# Find API keys and tokens
git log --all -p -S "api_key" -- "*.py" "*.js"

# Check for sensitive files
git ls-files | grep -E "(secrets|credentials|\.env|\.key)"
### Docker Security Scan

bash
# Scan image for vulnerabilities
trivy image your-image:tag

# Scan running container
docker scan your-image:tag

# Check for secrets in image
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  wagoodman/dive:latest your-image:tag
### Dependency Audit

bash
# Python
pip-audit
safety check

# Node.js
npm audit --audit-level=moderate
yarn audit

# Go
go mod verify
nancy sleuth
---

## Output Templates

### Threat Model Report Template

markdown
# Threat Model: [System Name]

**Date:** [Date]
**Author:** [Name]
**Status:** [Draft/In Review/Approved]

## System Overview

### Purpose
[What the system does]

### Scope
[What's included/excluded]

### Trust Boundaries
[Define trust boundaries]

## Data Flow Diagram
[Include DFD diagram or description]

## Threat Analysis

### Identified Threats

| ID | Threat | STRIDE | Risk Score | Mitigation | Status |
|----|--------|--------|------------|------------|--------|
| T001 | [Threat] | [Category] | [X/10] | [Description] | [Open/Resolved] |

## Risk Summary

| Risk Level | Count |
|------------|-------|
| Critical | X |
| High | X |
| Medium | X |
| Low | X |

## Sign-off

| Role | Name | Date |
|------|------|------|
| Security Engineer | | |
| System Owner | | |
| Development Lead | | |
### Security Review Report Template

markdown
# Security Review Report: [Project Name]

**Review Date:** [Date]
**Reviewers:** [Names]
**Phase:** [Design/Implementation/Pre-Release]

## Executive Summary

## Scope

## Methodology

## Findings

### Critical Findings

| ID | Title | Description | Affected Component | Remediation | Priority |
|----|-------|-------------|-------------------|-------------|----------|
| C001 | | | | | |

### High Findings
[...]

### Medium Findings
[...]

### Low Findings / Recommendations
[...]

## Sign-off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Security Lead | | | |
| Project Lead | | | |
| CTO | | | |