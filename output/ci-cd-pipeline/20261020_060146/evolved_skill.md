---
category: software-development
name: ci-cd-pipeline
description: "CI/CD Pipeline Generator - Generate and configure CI/CD pipelines for GitHub Actions, GitLab CI, Jenkins, Docker build/test/deploy workflows."
---

# CI/CD Pipeline

Generate and configure CI/CD pipelines for major platforms. Supports GitHub Actions, GitLab CI, Jenkins, and Docker-based build/test/deploy workflows.

## When to Use

- Creating new CI/CD configurations from scratch
- Migrating pipelines between platforms
- Optimizing existing build and deployment workflows
- Setting up automated testing and deployment
- Configuring Docker-based CI/CD pipelines

## Supported Platforms

| Platform | Use Case |
|----------|----------|
| `github` | GitHub Actions workflows |
| `gitlab` | GitLab CI/CD pipelines |
| `jenkins` | Jenkins pipelines (Jenkinsfile) |
| `docker` | Docker build and containerization |

## Workflow Stages

| Stage | Description |
|-------|-------------|
| `build` | Compile code, build artifacts, create Docker images |
| `test` | Run unit tests, integration tests, code quality checks |
| `deploy` | Deploy to staging, production, or cloud platforms |

## Usage

ci-cd-pipeline <platform> <stage> [options]
### Examples

bash
# Generate a GitHub Actions workflow for a Node.js project
ci-cd-pipeline github build --language node --version 20

# Create GitLab CI pipeline with test and deploy stages
ci-cd-pipeline gitlab full --language python --framework fastapi

# Generate Jenkinsfile for Java Maven project
ci-cd-pipeline jenkins build --language java --build-tool maven

# Docker-based CI/CD setup
ci-cd-pipeline docker deploy --registry ghcr.io --image myapp

# Complete pipeline with all stages
ci-cd-pipeline github full --language node --deploy-to aws-ecs
## Common Configurations

### Node.js with GitHub Actions
yaml
name: Node.js CI
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npm test
### Docker Multi-stage Build Pipeline
yaml
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
## Best Practices

1. **Use caching** — Cache dependencies and build artifacts between runs
2. **Fail fast** — Run fastest tests first in your pipeline
3. **Environment isolation** — Use separate configs for staging/production
4. **Secret management** — Never commit secrets; use platform secret stores
5. **Parallel jobs** — Split independent tasks into parallel jobs

---

*CI/CD Pipeline Generator by BytesAgain*