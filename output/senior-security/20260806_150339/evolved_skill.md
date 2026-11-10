---
category: software-development
name: senior-security
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

Comprehensive security engineering toolkit for threat modeling, vulnerability analysis, secure architecture design, and penetration testing.

---

## Table of Contents

- [Quick Reference](#quick-reference)
- [Threat Modeling Workflow](#threat-modeling-workflow)
- [Security Architecture Review](#security-architecture-review)
- [Vulnerability Assessment Workflow](#vulnerability-assessment-workflow)
- [Secure Code Review Workflow](#secure-code-review-workflow)
- [Cryptography Implementation Guide](#cryptography-implementation-guide)
- [Incident Response Workflow](#incident-response-workflow)
- [Security Tools Reference](#security-tools-reference)
- [OWASP Top 10 Checklist](#owasp-top-10-checklist)
- [Common Vulnerability Mitigations](#common-vulnerability-mitigations)

---

## Quick Reference

### STRIDE Threat Categories

| Category | Threat | Security Property | Common Mitigations |
|----------|--------|-------------------|-------------------|
| **S**poofing | Impersonate legitimate users/systems | Authentication | MFA, certificates, session tokens |
| **T**ampering | Modify data/code | Integrity | Hash verification, digital signatures, HMAC |
| **R**epudiation | Deny actions without proof | Non-repudiation | Audit logs, digital signatures, immutable logging |
| **I**nformation Disclosure | Expose sensitive data | Confidentiality | Encryption, access controls, data masking |
| **D**enial of Service | Disrupt availability | Availability | Rate limiting, redundancy, DDoS protection |
| **E**levation of Privilege | Gain unauthorized access | Authorization | Role-based access control, principle of least privilege |

### Risk Scoring (DREAD)

| Rating | 1-3 (Low) | 4-6 (Medium) | 7-10 (High) |
|--------|-----------|--------------|-------------|
| Damage | Minimal | Moderate | Severe/Catastrophic |
| Reproducibility | Complex/rare | Uncommon | Simple/immediate |
| Exploitability | Requires advanced tools | Requires some skill | Trivial script available |
| Affected Users | Single user | Some users | All users |
| Discoverability | Hidden/logs only | Can be found | Public/exploits known |

**Risk Score = (Damage + Reproducibility + Exploitability + Affected Users + Discoverability) / 5**

---

## Threat Modeling Workflow

### Step 1: Scope Definition

Document before analyzing:
- System purpose and boundaries
- Data assets requiring protection
- User roles and trust levels
- Integration points with external systems
- Regulatory requirements (GDPR, HIPAA, PCI-DSS)
### Step 2: Create Data Flow Diagram (DFD)

Identify these elements:

| Element | Description | Examples |
|---------|-------------|----------|
| External Entities | Users, external services | End users, third-party APIs, SSO providers |
| Processes | Application components | Web server, microservices, background workers |
| Data Stores | Persistence layer | Databases, caches, file storage, message queues |
| Data Flows | Information transfer | REST APIs, gRPC, WebSocket, file transfers |

### Step 3: Identify Trust Boundaries

Mark locations where:

- Untrusted input enters the system
- Privilege levels change
- Network zones intersect
- Encryption starts/ends
- Authentication occurs

### Step 4: Apply STRIDE per Element

**STRIDE per Element Matrix:**

| DFD Element | Spoofing | Tampering | Repudiation | Information Disclosure | DoS | Elevation of Privilege |
|-------------|----------|-----------|-------------|------------------------|-----|------------------------|
| External Entity | ✓ | ✓ | ✓ | ✓ | ✓ | |
| Process | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Data Store | | ✓ | ✓ | ✓ | ✓ | ✓ |
| Data Flow | | ✓ | | ✓ | ✓ | |

### Step 5: Risk Assessment with DREAD

For each identified threat:

1. Rate each factor 1-10
2. Calculate average score
3. Classify: Low (<4), Medium (4-7), High (>7)
4. Prioritize remediation by score
### Step 6: Document Mitigations

| Threat | Risk Score | Mitigation Strategy | Implementation Notes |
|--------|------------|--------------------|--------------------|
| SQL Injection | 8.5 | Parameterized queries | ORM with prepared statements |
| Session Hijacking | 7.2 | Secure cookie flags | HttpOnly, Secure, SameSite |
| Data Exposure | 8.0 | Encryption at rest | AES-256 with key rotation |

### Step 7: Validation Checklist

- [ ] All DFD elements have STRIDE analysis
- [ ] Trust boundaries clearly marked
- [ ] Every threat has risk score
- [ ] Mitigations mapped to threats
- [ ] Residual risk documented
- [ ] Review completed with security team
- [ ] Threat model version controlled and dated

---

## Security Architecture Review

### Architecture Security Checklist

#### Authentication

- [ ] Multi-factor authentication implemented
- [ ] Password policy enforced (12+ chars, complexity, rotation)
- [ ] Secure session management (timeouts, invalidation)
- [ ] OAuth 2.0 / OIDC properly configured
- [ ] Token storage follows security best practices

#### Authorization

- [ ] Principle of least privilege applied
- [ ] Role-based access control (RBAC) implemented
- [ ] API permissions validated server-side
- [ ] Resource ownership verified
- [ ] Horizontal privilege escalation prevented

#### Data Protection

- [ ] Encryption at rest (AES-256 or equivalent)
- [ ] Encryption in transit (TLS 1.2+)
- [ ] Key management follows best practices
- [ ] Secrets management (no hardcoded credentials)
- [ ] Sensitive data minimized and masked

#### Network Security

- [ ] Zero-trust architecture principles applied
- [ ] Network segmentation implemented
- [ ] Firewall rules follow deny-by-default
- [ ] DNS security (DNSSEC, DoH/DoT)
- [ ] API gateway rate limiting active

### Security Patterns

#### Defense in Depth

Layer 1: Perimeter (WAF, DDoS protection)
Layer 2: Network (Firewall, segmentation, IDS/IPS)
Layer 3: Host (Hardening, vulnerability management)
Layer 4: Application (Secure coding, input validation)
Layer 5: Data (Encryption, access controls)
Layer 6: User (MFA, security awareness)
#### Zero Trust Principles

Never trust, always verify
Least privilege access
Assume breach
Verify explicitly (location, device health, identity)
---

## Vulnerability Assessment Workflow

### Phase 1: Reconnaissance

bash
# Passive reconnaissance
amass enum -passive -d example.com
subfinder -d example.com
waybackurls example.com | tee wayback.txt

# Active scanning
nmap -sV -sC -O target.com
nikto -h https://target.com
### Phase 2: Vulnerability Discovery

#### Automated Scanning

| Tool | Focus | Use Case |
|------|-------|----------|
| **OWASP ZAP** | Web application | Dynamic testing |
| **Burp Suite** | Web application | Manual + automated |
| **Nessus** | Infrastructure | Network scanning |
| **OpenVAS** | Infrastructure | Vulnerability assessment |
| **Nuclei** | Templates | CVE detection |
| **Semgrep** | Static analysis | Code scanning |

#### Manual Testing Checklist

- [ ] Authentication bypass attempts
- [ ] Authorization flaw testing
- [ ] Injection vulnerabilities (SQL, NoSQL, Command, LDAP, XSS, XXE)
- [ ] Business logic flaws
- [ ] API security testing
- [ ] Cryptographic weakness analysis
- [ ] Race condition testing
- [ ] Race condition testing

### Phase 3: Vulnerability Classification

Use CVSS v3.1 for severity scoring:

| Rating | CVSS Score | Action Timeline |
|--------|------------|-----------------|
| Critical | 9.0-10.0 | Immediate (<24h) |
| High | 7.0-8.9 | Within 7 days |
| Medium | 4.0-6.9 | Within 30 days |
| Low | 0.1-3.9 | Within 90 days |

### Phase 4: Remediation Verification

- [ ] Proof of concept exploit documented
- [ ] Fix implemented and tested
- [ ] Vulnerability re-scanned
- [ ] False positive ruled out
- [ ] Remediation verified in staging
- [ ] Monitoring for regression

---

## Secure Code Review Workflow

### Quick Wins (First Pass)

Scan for these patterns with `grep` or Semgrep:

bash
# Hardcoded credentials
grep -r "password\s*=" --include="*.py" .
grep -r "api[_-]?key\s*=" --include="*.js" .

# SQL Injection patterns
grep -r "execute\s*(" --include="*.py" .
grep -r "query\s*\+" --include="*.js" .

# Insecure deserialization
grep -r "pickle.loads" --include="*.py" .
grep -r "yaml.load" --include="*.py" .
### Secure Code Review Checklist

#### Input Validation

- [ ] All input validated before processing
- [ ] Whitelist validation preferred over blacklist
- [ ] File type validation uses magic bytes, not extensions
- [ ] URL validation checks scheme and destination
- [ ] Email validation follows RFC standards
- [ ] Length limits enforced

#### Authentication

- [ ] Passwords hashed with bcrypt/scrypt/Argon2
- [ ] Session tokens are cryptographically random
- [ ] Session timeout implemented
- [ ] Password reset tokens are single-use and time-limited
- [ ] MFA available for sensitive operations

#### Data Handling

- [ ] No sensitive data in logs
- [ ] No sensitive data in error messages
- [ ] PII properly classified and handled
- [ ] Data retention policies enforced
- [ ] Secure deletion implemented

#### Cryptography

- [ ] Strong algorithms (AES-256, RSA-2048+, Ed25519)
- [ ] Proper IV/randomness generation
- [ ] No custom crypto implementations
- [ ] Key rotation implemented
- [ ] Secrets never in version control

#### Error Handling

- [ ] Generic error messages to users
- [ ] Detailed errors logged server-side only
- [ ] No stack traces in production
- [ ] Fail-secure defaults

---

## Cryptography Implementation Guide

### Algorithm Selection

| Use Case | Recommended | Avoid |
|----------|-------------|-------|
| Symmetric encryption | AES-256-GCM | DES, 3DES, AES-ECB |
| Asymmetric encryption | RSA-2048+, ECIES | RSA-1024, textbook RSA |
| Digital signatures | ECDSA (P-256+), Ed25519 | MD5, SHA1 signatures |
| Hashing (passwords) | Argon2id, bcrypt, scrypt | MD5, SHA256 alone |
| Hashing (integrity) | SHA-256, SHA-3 | MD5, SHA1 |
| HMAC | HMAC-SHA256 | MD5-based HMAC |
| Key derivation | HKDF, PBKDF2 (high iterations) | Single iteration |
| Random generation | CSPRNG (os.urandom, SecureRandom) | Math.random() |

### Secure Implementation Examples

#### Password Hashing (Python)

python
import argon2
from argon2 import PasswordHasher

ph = PasswordHasher(
    time_cost=3,      # Number of iterations
    memory_cost=65536, # 64 MiB
    parallelism=4,    # Number of parallel threads
    hash_len=32,      # Length of the hash in bytes
    salt_len=16       # Length of the random salt
)

# Hashing
hashed = ph.hash("user_password")
# Verification
try:
    ph.verify(hashed, "user_password")
except argon2.exceptions.VerifyMismatchError:
    print("Invalid password")
#### Secure Random Generation

python
import secrets
import os

# Cryptographically secure random bytes
token = secrets.token_urlsafe(32)  # 256-bit token
salt = secrets.token_bytes(32)     # 256-bit salt

# For AES-GCM
nonce = secrets.token_bytes(12)  # 96-bit nonce for GCM
#### Encryption at Rest (Python)

python
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def encrypt(plaintext: bytes, key: bytes) -> tuple[bytes, bytes]:
    """Encrypt using AES-256-GCM with random nonce."""
    aesgcm = AESGCM(key)
    nonce = secrets.token_bytes(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    return nonce, ciphertext

def decrypt(ciphertext: bytes, key: bytes, nonce: bytes) -> bytes:
    """Decrypt AES-256-GCM ciphertext."""
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ciphertext, None)
#### Key Derivation

python
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

def derive_key(master_key: bytes, context: str) -> bytes:
    """Derive a key using HKDF."""
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=context.encode(),
    )
    return hkdf.derive(master_key)
### Common Crypto Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| Using ECB mode | Patterns visible in ciphertext | Use GCM, CBC with HMAC |
| Reusing nonces | Confidentiality broken (GCM) | Random nonce per encryption |
| MD5/SHA1 for passwords | Fast hashing enables brute force | Use bcrypt/Argon2/scrypt |
| Hardcoded keys | Key exposure in source | Use KMS or environment variables |
| ECB mode for files | Patterns visible | Use CBC or XTS mode |
| RSA without padding | Vulnerable to attacks | Use OAEP/PSS padding |

---

## Incident Response Workflow

### Incident Classification

| Severity | Definition | Response Time | Examples |
|----------|------------|---------------|----------|
| P1 - Critical | Active breach, data exfiltration | Immediate | Ransomware, unauthorized access to sensitive data |
| P2 - High | Potential breach, severe vulnerability exploited | Within 1 hour | Malware detected, credential compromise suspected |
| P3 - Medium | Security event, investigation needed | Within 4 hours | Failed intrusion attempts, policy violation |
| P4 - Low | Minor event, no immediate threat | Within 24 hours | Suspicious activity, phishing attempt |

### Incident Response Phases

#### 1. Preparation

- [ ] Incident response plan documented
- [ ] Contact list current (security team, legal, PR)
- [ ] Communication channels established
- [ ] Forensic tools ready
- [ ] Team trained on procedures

#### 2. Detection & Analysis

Collect evidence:
- Logs (application, system, network)
- Memory dumps (if applicable)
- Disk images (for forensic analysis)
- Network traffic captures
- Timeline of events
#### 3. Containment

**Immediate (Short-term):**
- Isolate affected systems
- Block malicious IPs/domains
- Revoke compromised credentials
- Enable additional logging

**Long-term:**
- Deploy patches
- Strengthen controls
- Monitor for recurrence

#### 4. Eradication & Recovery

- Remove malware/backdoors
- Close exploited vulnerabilities
- Restore from clean backups
- Verify system integrity
- Gradual return to operations

#### 5. Post-Incident

- [ ] Document lessons learned
- [ ] Update incident response plan
- [ ] Implement preventive measures
- [ ] Brief relevant stakeholders
- [ ] Regulatory notification if required

---

## Security Tools Reference

### Static Application Security Testing (SAST)

| Tool | Languages | Best For |
|------|-----------|----------|
| Semgrep | Multi | Custom rules, speed |
| SonarQube | Multi | CI/CD integration |
| Bandit | Python | Quick Python analysis |
| CodeQL | Multi | Deep analysis |
| Checkmarx | Multi | Enterprise scale |

### Dynamic Application Security Testing (DAST)

| Tool | Type | Best For |
|------|------|----------|
| OWASP ZAP | Open source | Web apps |
| Burp Suite | Commercial | Manual testing |
| Nuclei | Templates | CVE scanning |
| sqlmap | SQL injection | Database assessment |

### Secret Scanning

bash
# GitLeaks
gitleaks detect --source . --report report.json

# TruffleHog
trufflehog filesystem .

# Gitleaks (pre-commit hook)
gitleaks protect --pre-commit --source .

# Detect-secrets
detect-secrets scan > .secrets.baseline
### Dependency Scanning

bash
# npm audit
npm audit --audit-level=moderate

# Snyk
snyk test

# Dependabot (GitHub)
# Enable in repository settings

# Grype
grype dir:.

# Trivy
trivy fs --severity HIGH,CRITICAL .
### Infrastructure Scanning

bash
# Network enumeration
nmap -sV -sC -O -p- target.com

# Vulnerability scanning
openvas -T pdf -o report.pdf

# Container scanning
trivy image image:tag

# Cloud security (AWS)
aws config credential-check
---

## OWASP Top 10 Checklist

### A01:2021 - Broken Access Control

- [ ] Direct object references validated
- [ ] Access controls enforced server-side
- [ ] Deny by default policy
- [ ] Rate limiting on API endpoints
- [ ] CORS properly configured
- [ ] Access logs maintained

### A02:2021 - Cryptographic Failures

- [ ] Data classified by sensitivity
- [ ] Encryption for data at rest
- [ ] TLS 1.2+ for data in transit
- [ ] No sensitive data in URLs
- [ ] Secrets in secure vaults
- [ ] Strong crypto algorithms used

### A03:2021 - Injection

- [ ] Input validation on server
- [ ] Parameterized queries used
- [ ] ORMs with safe defaults
- [ ] Shell commands avoided
- [ ] Context-aware output encoding
- [ ] Content Security Policy set

### A04:2021 - Insecure Design

- [ ] Threat model completed
- [ ] Secure design patterns used
- [ ] Security requirements defined
- [ ] Abuse cases documented
- [ ] Rate limiting implemented
- [ ] Limits on resource consumption

### A05:2021 - Security Misconfiguration

- [ ] Hardened configurations
- [ ] Unnecessary features disabled
- [ ] Error handling configured
- [ ] Security headers set
- [ ] Configuration regularly reviewed
- [ ] Automated configuration checks

### A06:2021 - Vulnerable Components

- [ ] Bill of materials maintained
- [ ] Dependency scanning automated
- [ ] Components from trusted sources
- [ ] Monitoring for CVE announcements
- [ ] Removal of unused dependencies
- [ ] Patching policy defined

### A07:2021 - Authentication Failures

- [ ] MFA implemented
- [ ] Weak passwords rejected
- [ ] Session timeout enforced
- [ ] Secure session tokens
- [ ] Password reset secured
- [ ] Failed login rate limited

### A08:2021 - Software and Data Integrity

- [ ] Code signed and verified
- [ ] CI/CD with security controls
- [ ] Dependencies pinned
- [ ] No untrusted deserialization
- [ ] Update verification implemented

### A09:2021 - Security Logging and Monitoring

- [ ] Logs contain necessary context
- [ ] Logs protected from tampering
- [ ] Monitoring configured
- [ ] Alerts for suspicious activity
- [ ] Incident response plan exists
- [ ] Regular log review

### A10:2021 - Server-Side Request Forgery (SSRF)

- [ ] URL validation implemented
- [ ] Allowlist for internal services
- [ ] Deny by default firewall rules
- [ ] Network segmentation applied
- [ ] Response validation

---

## Common Vulnerability Mitigations

### SQL Injection

**Vulnerable Pattern:**
python
# NEVER DO THIS
query = f"SELECT * FROM users WHERE id = {user_id}"
**Secure Patterns:**
python
# Parameterized query
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))

# ORM with safe defaults
user = User.query.filter_by(id=user_id).first()
### Cross-Site Scripting (XSS)

**Mitigations:**
- Output encoding (HTML, JavaScript, URL, CSS)
- Content Security Policy headers
- HTTPOnly cookie flag
- Template auto-escaping (Jinja2, React JSX)
- Input validation (whitelist approach)

### Cross-Site Request Forgery (CSRF)

**Mitigations:**
- CSRF tokens for state-changing operations
- SameSite cookie attribute
- Origin/Referer header validation
- Custom request headers

### Insecure Deserialization

**Vulnerable:**
python
import pickle
data = pickle.loads(untrusted_data)
**Secure Alternatives:**
python
import json
data = json.loads(untrusted_data)
# Or use marshmallow/pydantic for validation
### Path Traversal

**Vulnerable:**
python
# NEVER
with open(f"/var/files/{filename}") as f:
    return f.read()
**Secure:**
python
import os
safe_path = os.path.realpath(f"/var/files/{filename}")
if not safe_path.startswith("/var/files/"):
    raise ValueError("Invalid path")
with open(safe_path) as f:
    return f.read()
### Command Injection

**Vulnerable:**
python
import os
os.system(f"echo {user_input}")
**Secure:**
python
import subprocess
result = subprocess.run(
    ["echo", user_input],  # Pass as argument, not shell
    capture_output=True,
    text=True
)
### Server-Side Request Forgery (SSRF)

**Mitigations:**
python
import ipaddress

def is_safe_url(url: str) -> bool:
    parsed = urlparse(url)
    
    # Check for localhost/private IP ranges
    try:
        host = resolve_hostname(parsed.hostname)
        ip = ipaddress.ip_address(host)
        
        # RFC 1918 private, loopback, link-local
        if ip.is_private or ip.is_loopback or ip.is_reserved:
            return False
    except:
        return False
    
    # Check scheme
    if parsed.scheme not in ('http', 'https'):
        return False
    
    return True
### XML External Entity (XXE)

**Vulnerable (Python):**
python
# NEVER use defusedxml or disable entity expansion
from xml.etree import ElementTree as ET
ET.parse(untrusted_xml)  # Vulnerable by default
**Secure:**
python
from defusedxml import ElementTree
tree = ElementTree.parse(untrusted_xml)  # Safe by default
---

## Quick Response Templates

### Security Review Request

Subject: Security Review Request - [Component Name]

Component: [Name and version]
Owner: [Team/Person]
Review Scope: [What's in scope]
Data Classification: [Public/Internal/Confidential/Restricted]
External Dependencies: [List third-party services]

Threat Model: [Attached/Link]
Previous Security Issues: [Links to prior findings]

Timeline: [Requested completion date]
### Vulnerability Disclosure

Vulnerability: [Title]
Severity: [Critical/High/Medium/Low]
CVSS Score: [X.X]
Affected Component: [Version range]
Discovery Date: [Date]
Reporter: [Name/Organization]

Description:
[Detailed description of the vulnerability]

Impact:
[What an attacker could achieve]

Proof of Concept:
[Steps to reproduce / code snippets]

Recommended Fix:
[Suggested remediation]

References:
[CVE if applicable / related CVEs]