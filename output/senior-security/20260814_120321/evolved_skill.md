---
name: "senior-security"
description: Security engineering toolkit for threat modeling, vulnerability analysis, secure architecture, and penetration testing. Includes STRIDE analysis, OWASP guidance, cryptography patterns, and security scanning tools. Use when the user asks about security reviews, threat analysis, vulnerability assessments, secure coding practices, security audits, attack surface analysis, CVE remediation, or security best practices.
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
---

# Senior Security Engineer

Comprehensive security engineering toolkit for threat modeling, vulnerability analysis, secure architecture design, penetration testing, and incident response.

---

## Table of Contents

1. [Threat Modeling Workflow](#1-threat-modeling-workflow)
2. [Security Architecture Workflow](#2-security-architecture-workflow)
3. [Vulnerability Assessment Workflow](#3-vulnerability-assessment-workflow)
4. [Secure Code Review Workflow](#4-secure-code-review-workflow)
5. [Incident Response Workflow](#5-incident-response-workflow)
6. [Security Tools Reference](#6-security-tools-reference)
7. [Cryptography Patterns](#7-cryptography-patterns)
8. [OWASP Reference](#8-owasp-reference)
9. [CVE Remediation Guide](#9-cve-remediation-guide)

---

## 1. Threat Modeling Workflow

Systematic approach to identifying, analyzing, and prioritizing security threats using STRIDE methodology.

### Step 1: Define System Scope

Document the system boundaries and collect key information:

markdown
## System Scope Document

### System Name: [System/Application Name]
### Version: [Version/Release]
### Owner: [Team/Individual Responsible]
### Review Date: [Date]

### Assets to Protect
- [List critical assets: data, systems, credentials, keys]

### Trust Boundaries
- [Define internal vs external boundaries]
- [Identify authentication/authorization boundaries]

### Data Flows
- [Document data inputs/outputs]
- [Identify data sensitivity levels]
### Step 2: Create Data Flow Diagram (DFD)

Map all system components using standard DFD notation:

| Element | Symbol | Security Considerations |
|---------|--------|------------------------|
| External Entity | Square | User trust level, authentication method |
| Process | Circle | Privileges, attack surface, dependencies |
| Data Store | Open Rectangle | Encryption at rest, access controls |
| Data Flow | Arrow | Encryption in transit, integrity checks |
| Trust Boundary | Dashed Line | Authentication requirements |

### Step 3: Apply STRIDE Analysis

Apply each STRIDE category to every DFD element:

| Threat Category | Security Property | Common Attack Vectors | Recommended Mitigations |
|-----------------|-------------------|------------------------|-------------------------|
| **S**poofing | Authentication | Session hijacking, credential theft, JWT forgery | Strong auth, MFA, certificate pinning, secure session management |
| **T**ampering | Integrity | SQL injection, XSS, MITM, supply chain poisoning | Input validation, integrity checks, code signing, WAF |
| **R**epudiation | Non-repudiation | Log manipulation, transaction否认 | Audit logging, digital signatures, immutable logs |
| **I**nformation Disclosure | Confidentiality | Data leaks, misconfigured S3, API exposure | Encryption, access controls, DLP, data masking |
| **D**enial of Service | Availability | DDoS, resource exhaustion, algorithmic complexity | Rate limiting, CDN, autoscaling, circuit breakers |
| **E**levation of Privilege | Authorization | IDOR, privilege escalation, insecure defaults | Role-based access, principle of least privilege, zero trust |

### Step 4: Risk Scoring with DREAD

Score each identified threat:

| Score | 1 | 2 | 3 | 4 | 5 |
|-------|---|---|---|---|---|
| **Damage** | No impact | Minor non-sensitive | Sensitive data affected | Critical system compromised | Full system compromise |
| **Reproducibility** | Unlikely | Hard to reproduce | Requires specific conditions | Easily reproducible | Always reproducible |
| **Exploitability** | Requires physical access | Requires local access | Requires network access | Script kiddie level | Automated tools available |
| **Affected Users** | Single user | Few users | Department | Entire organization | All users/customers |
| **Discoverability** | Very hard | Hard | Moderate | Easy | Public/exploits known |

**Risk Score = (Damage + Reproducibility + Exploitability + Affected Users + Discoverability) / 5**

| Score Range | Risk Level | Action |
|-------------|------------|--------|
| 8-10 | Critical | Immediate remediation |
| 6-8 | High | Within 1 week |
| 4-6 | Medium | Within 1 month |
| <4 | Low | Document and monitor |

### Step 5: Document and Validate

**Validation Checklist:**
- [ ] All DFD elements analyzed
- [ ] STRIDE applied to each element
- [ ] Threats documented with descriptions
- [ ] DREAD scores calculated
- [ ] Mitigations defined for each threat
- [ ] Priority established based on risk score
- [ ] Findings reviewed with stakeholders
- [ ] Threat model approved and signed off

---

## 2. Security Architecture Workflow

Design and evaluate secure system architectures.

### Step 1: Define Security Requirements

## Security Requirements

### Functional Requirements
- [ ] Authentication mechanism (SAML, OAuth2, OIDC)
- [ ] Authorization model (RBAC, ABAC, zero-trust)
- [ ] Data protection requirements
- [ ] Compliance requirements (SOC2, GDPR, HIPAA, PCI-DSS)

### Non-Functional Requirements
- [ ] Confidentiality requirements
- [ ] Integrity requirements
- [ ] Availability targets (99.99% SLA?)
- [ ] Recovery time objective (RTO)
- [ ] Recovery point objective (RPO)
### Step 2: Architecture Review Checklist

| Category | Review Item | Status |
|----------|-------------|--------|
| **Authentication** | MFA implemented | ☐ |
| | Password policy enforced | ☐ |
| | Session management secure | ☐ |
| | Token-based auth uses short expiry | ☐ |
| **Authorization** | Least privilege enforced | ☐ |
| | Separation of duties defined | ☐ |
| | Role hierarchy documented | ☐ |
| **Network** | Network segmentation implemented | ☐ |
| | Firewalls/configured correctly | ☐ |
| | Encryption in transit (TLS 1.2+) | ☐ |
| **Data** | Encryption at rest | ☐ |
| | Data classification applied | ☐ |
| | Backup strategy documented | ☐ |
| **Infrastructure** | Secrets management (HashiCorp Vault, AWS Secrets Manager) | ☐ |
| | Patch management process | ☐ |
| | Logging and monitoring | ☐ |

### Step 3: Zero Trust Architecture Principles

┌─────────────────────────────────────────────────────────┐
│                    Zero Trust Model                      │
├─────────────────────────────────────────────────────────┤
│  1. VERIFY EXPLICITLY                                    │
│     Always authenticate and authorize based on all      │
│     available data points (identity, location, device,  │
│     service, workload, data classification, anomalies)  │
│                                                          │
│  2. USE LEAST PRIVILEGE ACCESS                           │
│     Limit user access with just-in-time and             │
│     just-enough-access, risk-based adaptive policies    │
│                                                          │
│  3. ASSUME BREACH                                        │
│     Minimize blast radius, segment access. Verify        │
│     end-to-end encryption. Use analytics to get          │
│     visibility, detect threats, improve defenses        │
└─────────────────────────────────────────────────────────┘
---

## 3. Vulnerability Assessment Workflow

### Step 1: Reconnaissance

bash
# Passive reconnaissance
amass enum -passive -d example.com
subfinder -d example.com
assetfinder example.com

# Active reconnaissance
nmap -sV -sC -O target-ips.txt
nikto -h https://target.com
dirb https://target.com /usr/share/wordlists/dirb/common.txt
### Step 2: Vulnerability Scanning

| Scanner | Use Case | Command Example |
|---------|----------|------------------|
| **OWASP ZAP** | Web application scanning | `zap-cli quick-scan https://target.com` |
| **Burp Suite** | Manual + automated testing | Pro version recommended |
| **Nuclei** | Template-based scanning | `nuclei -u https://target.com` |
| **OpenVAS** | Network vulnerability scanning | `omp -u admin -w password -h localhost -T tasks` |
| **Trivy** | Container/image scanning | `trivy image myapp:latest` |
| **Semgrep** | Static code analysis | `semgrep --config=auto .` |

### Step 3: Vulnerability Prioritization

Use CVSS scoring for prioritization:

| CVSS Score | Severity | Response Time |
|------------|----------|---------------|
| 9.0-10.0 | Critical | 24 hours |
| 7.0-8.9 | High | 7 days |
| 4.0-6.9 | Medium | 30 days |
| 0.1-3.9 | Low | 90 days |

### Step 4: Reporting Template

markdown
## Vulnerability Assessment Report

### Executive Summary
[High-level overview of findings]

### Methodology
- Scope
- Tools used
- Testing period

### Findings Summary
| ID | Vulnerability | Severity | Status |
|----|---------------|----------|--------|
| V001 | SQL Injection in /api/users | Critical | Open |
| V002 | Missing X-Frame-Options | Medium | Open |

### Detailed Findings
### V001: SQL Injection
**Severity:** Critical (CVSS 9.8)
**Location:** /api/users?id=*
**Description:** [Detailed description]
**Impact:** [Business impact]
**Proof of Concept:** [Steps to reproduce]
**Remediation:** [Specific fix with code example]
**References:** CWE-89, OWASP A1
---

## 4. Secure Code Review Workflow

### Step 1: Quick Wins Checklist

markdown
## Quick Security Checks

### Authentication
- [ ] No hardcoded credentials
- [ ] Passwords hashed with bcrypt/argon2
- [ ] Sessions expire appropriately
- [ ] MFA available for sensitive operations

### Input Validation
- [ ] All user input validated
- [ ] Parameterized queries used
- [ ] Output encoding applied

### Access Control
- [ ] Authorization checks on every endpoint
- [ ] Direct object references validated
- [ ] Admin routes protected

### Data Protection
- [ ] Sensitive data encrypted
- [ ] No secrets in code/version control
- [ ] Logging sanitized (no PII)
### Step 2: Common Vulnerability Patterns

#### SQL Injection

❌ **Vulnerable:**
sql
-- Never do this
query = "SELECT * FROM users WHERE id = " + userId
✅ **Secure:**
python
# Use parameterized queries
cursor.execute("SELECT * FROM users WHERE id = ?", (userId,))
#### Cross-Site Scripting (XSS)

❌ **Vulnerable:**
javascript
// Never render untrusted input directly
element.innerHTML = userInput;
✅ **Secure:**
javascript
// Use textContent or context-aware encoding
element.textContent = userInput;
// Or use framework's built-in escaping
<div>{userInput}</div>  // React auto-escapes
#### Command Injection

❌ **Vulnerable:**
python
# Never pass unsanitized input to shell
os.system(f"ls {user_directory}")
✅ **Secure:**
python
# Use subprocess with explicit arguments
subprocess.run(["ls", user_directory], shell=False)
### Step 3: Security Code Review Tools

| Language | Static Analysis Tool | Secret Scanner |
|----------|---------------------|----------------|
| Python | Bandit, Semgrep, Pylint-security | Gitleaks, TruffleHog, detect-secrets |
| JavaScript | ESLint-security, Semgrep | Gitleaks, secrets-scanner |
| Go | Gosec, Semgrep | Gitleaks, detect-secrets |
| Java | SpotBugs, Semgrep | Gitleaks, TruffleHog |
| All | Semgrep (multi-language) | Gitleaks, GitGuardian |

### Step 4: Secret Scanning Commands

bash
# Scan for secrets in repository
gitleaks detect --source . --report-path gitleaks-report.json

# Scan Docker images for vulnerabilities
trivy image --severity HIGH,CRITICAL myapp:latest

# Scan infrastructure as code
checkov -f terraform/main.tf
tfsec terraform/
---

## 5. Incident Response Workflow

### Incident Response Phases

┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   PREPARE    │───▶│   DETECT     │───▶│  CONTAIN     │
│              │    │   & ANALYZE  │    │              │
└──────────────┘    └──────────────┘    └──────────────┘
                                                │
       ┌────────────────────────────────────────┘
       │
       ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   ERADICATE  │───▶│   RECOVER    │───▶│ LESSONS      │
│              │    │              │    │ LEARNED      │
└──────────────┘    └──────────────┘    └──────────────┘
### Step 1: Detection & Analysis

markdown
## Incident Classification

| Severity | Definition | Response Time | Example |
|----------|------------|---------------|---------|
| SEV1 | Active breach, data exfiltration | Immediate | Ransomware, unauthorized access |
| SEV2 | Potential breach, significant risk | 1 hour | Suspicious activity, failed attacks |
| SEV3 | Vulnerability exploited, contained | 4 hours | Low-impact vulnerability found |
| SEV4 | Potential vulnerability, no impact | 24 hours | Security misconfiguration found |
### Step 2: Containment

**Immediate Containment:**
- Isolate affected systems
- Block malicious IPs
- Revoke compromised credentials
- Enable enhanced logging

**Evidence Preservation:**
bash
# Create forensic image
dd if=/dev/sda of=/mnt/evidence/disk-image.raw bs=4M status=progress

# Collect volatile data
memdump > memory.raw
netstat -tulpn > network-connections.txt
ps aux > process-list.txt
lsof > open-files.txt
### Step 3: Eradication & Recovery

1. Remove malware/backdoors
2. Patch vulnerabilities exploited
3. Reset compromised credentials
4. Verify system integrity
5. Gradual service restoration
6. Monitoring for re-infection

### Step 4: Post-Incident Report Template

markdown
## Incident Report

### Incident Details
- **Incident ID:** [ID]
- **Date/Time:** [When detected]
- **Severity:** [SEV1-4]
- **Status:** [Closed]

### Summary
[What happened]

### Timeline
| Time | Action |
|------|--------|
| YYYY-MM-DD HH:MM | [Event description] |

### Root Cause
[Why it happened]

### Impact
- Systems affected:
- Data exposed:
- Business impact:

### Remediation
- [ ] Action 1
- [ ] Action 2

### Lessons Learned
[What could be improved]

### Follow-up Actions
| Action | Owner | Due Date |
|--------|-------|----------|
| Action 1 | @person | YYYY-MM-DD |
---

## 6. Security Tools Reference

### Web Application Security

| Tool | Purpose | Install |
|------|---------|---------|
| OWASP ZAP | Web vulnerability scanner | `brew install owasp-zap` |
| Burp Suite | Web proxy/testing | Download from PortSwigger |
| SQLMap | SQL injection exploitation | `pip install sqlmap` |
| XSStrike | XSS detection | `pip install xsstrike` |

### Network Security

| Tool | Purpose | Command |
|------|---------|---------|
| Nmap | Network discovery | `nmap -sV -sC -p- target` |
| Wireshark | Packet analysis | GUI tool |
| Metasploit | Penetration testing | `msfconsole` |
| CrackMapExec | Active Directory testing | `cme smb target-list` |

### Code Security

| Tool | Purpose | Command |
|------|---------|---------|
| Semgrep | Static analysis | `semgrep --config=auto .` |
| SonarQube | Code quality + security | Docker部署 |
| Snyk | Dependency scanning | `snyk test` |
| Grype | Container scanning | `grype myapp:latest` |

### Secrets Detection

| Tool | Purpose | Command |
|------|---------|---------|
| Gitleaks | Git history scanning | `gitleaks detect --source .` |
| TruffleHog | Secret scanning | `trufflehog filesystem .` |
| GitGuardian | CI/CD integration | API-based |

---

## 7. Cryptography Patterns

### Password Hashing

python
# Python - Using argon2-cffi (recommended)
from argon2 import PasswordHasher

ph = PasswordHasher(
    time_cost=3,      # Number of iterations
    memory_cost=65536, # 64 MB
    parallelism=4     # Number of parallel threads
)

# Hash password
hashed = ph.hash("user_password")
# Verify password
ph.verify(hashed, "user_password")
javascript
// Node.js - Using argon2
const argon2 = require('argon2');

const hash = await argon2.hash(password, {
  type: argon2.argon2id,
  memoryCost: 65536, // 64 MB
  timeCost: 3,
  parallelism: 4
});

const isValid = await argon2.verify(hash, password);
### Secure Random Generation

python
# Use secrets module (not random)
import secrets

# Generate secure token
token = secrets.token_urlsafe(32)

# Generate random bytes
random_bytes = secrets.token_bytes(32)

# Generate secure password
password = secrets.token_urlsafe(16)
### Encryption at Rest (AES-256-GCM)

python
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

def encrypt_data(key: bytes, plaintext: bytes) -> bytes:
    """Encrypt data using AES-256-GCM with random nonce."""
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)  # 96-bit nonce for GCM
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    return nonce + ciphertext  # Prepend nonce for storage

def decrypt_data(key: bytes, encrypted_data: bytes) -> bytes:
    """Decrypt AES-256-GCM encrypted data."""
    aesgcm = AESGCM(key)
    nonce = encrypted_data[:12]
    ciphertext = encrypted_data[12:]
    return aesgcm.decrypt(nonce, ciphertext, None)
### Key Derivation

python
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def derive_key(password: str, salt: bytes, iterations: int = 480000) -> bytes:
    """Derive key using PBKDF2-HMAC-SHA256 (consider Argon2 for passwords)."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
    )
    return kdf.derive(password.encode())
### Secure Token Generation (JWT)

python
import jwt
from datetime import datetime, timedelta

# Token generation
payload = {
    "sub": "user_id",
    "exp": datetime.utcnow() + timedelta(minutes=30),
    "iat": datetime.utcnow(),
    "scope": ["read", "write"]
}
token = jwt.encode(payload, SECRET_KEY, algorithm="RS256")

# Token verification
try:
    decoded = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"])
except jwt.ExpiredSignatureError:
    raise AuthError("Token expired")
except jwt.InvalidTokenError:
    raise AuthError("Invalid token")
---

## 8. OWASP Reference

### OWASP Top 10 (2021)

| Rank | Vulnerability | Key Mitigations |
|------|---------------|-----------------|
| A01 | Broken Access Control | Implement proper authorization, audit access logs |
| A02 | Cryptographic Failures | Encrypt sensitive data, use modern cryptography |
| A03 | Injection | Input validation, parameterized queries |
| A04 | Insecure Design | Threat modeling, secure design patterns |
| A05 | Security Misconfiguration | Hardened configurations, automated scanning |
| A06 | Vulnerable Components | Dependency scanning, regular updates |
| A07 | Auth Failures | Strong passwords, MFA, session management |
| A08 | Data Integrity Failures | Digital signatures, integrity checks |
| A09 | Logging Failures | Centralized logging, alerting |
| A10 | SSRF | URL validation, blocklist/allowlist |

### OWASP API Security Top 10

| Rank | Issue | Prevention |
|------|-------|------------|
| API1 | Broken Object Level Authorization | Implement authorization checks for each resource |
| API2 | Broken Auth | Strong token validation, MFA |
| API3 | Excessive Data Exposure | Response filtering, minimal data exposure |
| API4 | Lack of Resources | Rate limiting, pagination |
| API5 | Broken Function Level Authorization | Verify access control on each endpoint |
| API6 | Mass Assignment | Explicit object binding, input validation |
| API7 | Security Misconfiguration | Hardened configurations, penetration testing |
| API8 | Injection | Input validation, output encoding |
| API9 | Improper Assets Management | API inventory, versioning |
| API10 | Insufficient Logging | Comprehensive logging, alerting |

---

## 9. CVE Remediation Guide

### CVE Analysis Process

┌─────────────────────────────────────────────────────────┐
│  1. IDENTIFY                                            │
│     Monitor CVE feeds (NVD, MITRE, vendor advisories)  │
├─────────────────────────────────────────────────────────┤
│  2. ASSESS                                              │
│     Determine applicability to your environment         │
├─────────────────────────────────────────────────────────┤
│  3. PRIORITIZE                                          │
│     CVSS score + exploit availability + asset criticality│
├─────────────────────────────────────────────────────────┤
│  4. REMEDIATE                                           │
│     Apply patch, implement mitigation, or accept risk   │
├─────────────────────────────────────────────────────────┤
│  5. VERIFY                                              │
│     Confirm remediation effective                       │
└─────────────────────────────────────────────────────────┘
### Remediation Strategies

| Strategy | When to Use | Example |
|----------|-------------|---------|
| **Patch** | Fix available and tested | Apply vendor security patch |
| **Upgrade** | Major version change needed | Upgrade to newer major release |
| **Mitigate** | Patch not yet available | Implement WAF rules, network segmentation |
| **Accept** | Low risk, high cost to fix | Document justification, monitor |
| **Compensate** | Permanent control in place | Alternative security measure |

### CVE Notification Sources

bash
# Subscribe to security advisories
# - NVD: https://nvd.nist.gov/
# - MITRE CVE: https://cve.mitre.org/
# - Vendor-specific mailing lists

# CLI tools for CVE monitoring
# Nix: nixpkgs-nixos-security-advisories
# GitHub: Dependabot alerts
# Docker: trivy vulnerability database updates
### Patch Priority Matrix

| CVSS | Exploitable | Patched | Priority |
|------|-------------|---------|----------|
| 9.0-10.0 | Yes | Available | **P1 - Immediate** |
| 9.0-10.0 | No | Available | **P2 - 48 hours** |
| 7.0-8.9 | Yes | Available | **P2 - 72 hours** |
| 7.0-8.9 | No | Available | **P3 - 7 days** |
| 4.0-6.9 | Any | Available | **P4 - 30 days** |
| <4.0 | Any | Available | **P5 - Next maintenance window** |

---

## Quick Reference Card

### Security Checklist for Code Reviews

┌────────────────────────────────────────────────────────┐
│  □ No hardcoded credentials or secrets                 │
│  □ Input validation on all endpoints                   │
│  □ Output encoding appropriate for context             │
│  □ Authentication required for sensitive operations     │
│  □ Authorization checked on every request              │
│  □ Error messages don't leak sensitive info            │
│  □ Logging doesn't capture PII                         │
│  □ Encryption used for sensitive data                  │
│  □ Dependencies are up to date                        │
│  □ Security headers configured                         │
│  □ Rate limiting implemented                           │
│  □ Third-party code audited                            │
└────────────────────────────────────────────────────────┘
### Essential Security Headers

| Header | Value | Purpose |
|--------|-------|---------|
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` | Force HTTPS |
| `X-Content-Type-Options` | `nosniff` | Prevent MIME sniffing |
| `X-Frame-Options` | `DENY` or `SAMEORIGIN` | Prevent clickjacking |
| `X-XSS-Protection` | `1; mode=block` | XSS filter (legacy browsers) |
| `Content-Security-Policy` | `default-src 'self'` | Prevent XSS/injection |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | Control referrer info |
| `Permissions-Policy` | `camera=(), microphone=()` | Restrict browser features |

---

*Last updated: 2024 | For internal security engineering use*