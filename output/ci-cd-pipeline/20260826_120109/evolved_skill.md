---
category: software-development
name: ci-cd-pipeline
description: "Generate and configure CI/CD pipelines for GitHub Actions, GitLab CI, Jenkins, and Docker. Includes build, test, and deployment workflows for multiple programming languages."
---

# CI/CD Pipeline

Generate, configure, and optimize CI/CD pipelines across major platforms. This skill produces production-ready configurations for automated building, testing, and deployment workflows.

## Supported Platforms

| Platform | File | Description |
|----------|------|-------------|
| GitHub Actions | `.github/workflows/*.yml` | GitHub-hosted runners, matrix builds, artifacts |
| GitLab CI | `.gitlab-ci.yml` | GitLab runners, needs/stage pipelines, cache |
| Jenkins | `Jenkinsfile` | Declarative/coded pipelines, agents, stages |
| Docker | `Dockerfile`, docker-compose | Multi-stage builds, optimized images |

## Supported Languages & Runtimes

- **Python** — pytest, tox, coverage, pip caching
- **Java** — Maven, Gradle, JUnit, JaCoCo
- **Rust** — cargo test, clippy, cargo build with caching
- **Node.js** — npm/yarn/pnpm, Jest, ESLint

## Commands

### Platform Selection

| Command | Purpose |
|---------|---------|
| `github [lang]` | Generate GitHub Actions workflow |
| `gitlab [lang]` | Generate GitLab CI configuration |
| `jenkins [lang]` | Generate Jenkins pipeline |
| `docker [lang]` | Generate Dockerfile and compose |

### Workflow Stages

| Command | Purpose |
|---------|---------|
| `test [lang]` | Generate test stage configuration |
| `build [lang]` | Generate build stage configuration |
| `deploy [env]` | Generate deployment configuration |

### Utilities

| Command | Purpose |
|---------|---------|
| `matrix [lang]` | Generate matrix strategy for parallel jobs |
| `cache [lang]` | Generate dependency caching configuration |
| `notify` | Generate notification/alerting configuration |

## Usage Examples

### Generate a GitHub Actions workflow for Python

bash
ci-cd-pipeline github python
### Generate GitLab CI with testing and deployment

bash
ci-cd-pipeline gitlab java --stages test build deploy
### Generate Docker multi-stage build

bash
ci-cd-pipeline docker python --optimize
### Generate complete pipeline with all stages

bash
ci-cd-pipeline github rust --full --matrix
### Generate with custom deployment target

bash
ci-cd-pipeline jenkins python --deploy kubernetes
## Common Configurations

### Quick Start Templates

bash
# Minimal test + build
ci-cd-pipeline github python --minimal

# Full CI/CD with staging/production
ci-cd-pipeline gitlab java --full --env staging,production

# Docker-centric with registry push
ci-cd-pipeline docker node --push gcr.io/myapp
### Matrix Builds

bash
# Multiple Python versions
ci-cd-pipeline github python --matrix "3.9,3.10,3.11"

# Multiple OS combinations
ci-cd-pipeline github java --matrix "ubuntu-latest,windows-latest" --jdk "11,17"
## Features

- **Multi-platform output** — Generate configs for all major CI platforms
- **Language-specific optimizations** — Caching, testing, and building tailored to each language
- **Matrix strategies** — Parallel test/build matrices for multiple versions
- **Docker integration** — Multi-stage builds, layer caching, registry pushes
- **Deployment targets** — Kubernetes, AWS, Azure, GCP, VM, Heroku
- **Security scanning** — SAST, dependency scanning, secret detection
- **Notification hooks** — Slack, email, webhook integrations

## Flags

| Flag | Description |
|------|-------------|
| `--full` | Generate complete pipeline with all stages |
| `--minimal` | Generate minimal working pipeline |
| `--test` | Include only test stage |
| `--deploy <target>` | Specify deployment target |
| `--matrix` | Enable matrix strategy |
| `--optimize` | Optimize for build speed/caching |
| `--docker` | Include Docker build/push steps |

---
*CI/CD Pipeline by BytesAgain*
💬 Feedback: https://bytesagain.com/feedback