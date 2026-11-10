---
category: software-development
name: ci-cd-pipeline
description: "CI/CD Pipeline Generator - Generates and configures CI/CD pipelines for GitHub Actions, GitLab CI, Jenkins, and Docker. Supports automated testing, building, and deployment workflows."
version: "2.1.0"
author: BytesAgain
tags: [ci-cd, devops, github-actions, gitlab-ci, jenkins, docker, deployment, automation]
---

# CI/CD Pipeline

Generate, configure, and optimize CI/CD pipelines for your projects. Supports multiple platforms and deployment targets.

## Triggers

- "ci cd pipeline"
- "github actions workflow"
- "gitlab ci config"
- "jenkins pipeline"
- "docker build and deploy"
- "automated testing and deployment"
- "CI/CD setup"

## Commands

| Command | Description | Use Case |
|---------|-------------|----------|
| `github` | Generate GitHub Actions workflow files | YAML-based workflows in `.github/workflows/` |
| `gitlab` | Generate GitLab CI configuration | `.gitlab-ci.yml` for GitLab repositories |
| `jenkins` | Generate Jenkinsfile pipelines | Declarative or scripted Jenkins pipelines |
| `docker` | Generate Docker build and push workflows | Multi-stage builds, multi-platform images |
| `test` | Generate test automation configs | Unit, integration, E2E testing stages |
| `deploy` | Generate deployment configurations | Staging, production, blue-green, canary |
| `multi` | Generate multi-platform configs | Simultaneous GitHub + GitLab + Jenkins |

## Supported Technologies

### Languages & Frameworks
- Node.js / TypeScript
- Python / Django / FastAPI
- Java / Spring Boot
- Go
- Rust
- Ruby / Rails
- .NET / C#

### Deployment Targets
- AWS (EC2, ECS, EKS, Lambda, S3, CloudFront)
- GCP (Cloud Run, GKE, Cloud Functions)
- Azure (App Service, AKS, Functions)
- Kubernetes (Helm, Kustomize)
- Docker Hub, AWS ECR, GCP Artifact Registry
- VPS / Self-hosted servers

### Testing Tools
- Jest, Mocha, Cypress
- PyTest, unittest
- JUnit, TestNG
- Cargo test
- RSpec

## Usage

### Basic Workflow

bash
# Generate a GitHub Actions workflow
ci-cd-pipeline github --name "Build and Test" --language "node" --test "jest"

# Generate GitLab CI configuration
ci-cd-pipeline gitlab --language "python" --deploy "aws-ecs"

# Generate Jenkins pipeline
ci-cd-pipeline jenkins --framework "spring-boot" --deploy "kubernetes"

# Generate Docker build workflow
ci-cd-pipeline docker --multi-stage --platforms "linux/amd64,linux/arm64"
### Interactive Mode

bash
ci-cd-pipeline run
# Select platform → Select language → Configure stages → Generate
### Full Pipeline Example

bash
# Generate complete pipeline with testing, building, and deployment
ci-cd-pipeline github --name "Production Deploy" \
  --language "node" \
  --test "jest --coverage" \
  --build "docker build" \
  --deploy "aws-ecs" \
  --env "staging,production" \
  --notifications "slack"
## Configuration Options

### Build Stage
- Caching strategies (npm cache, pip cache, Docker layers)
- Multi-platform builds
- Matrix builds for multiple versions
- Artifact retention

### Test Stage
- Coverage thresholds
- Parallel execution
- Test reporting (JUnit, Cobertura)
- Security scanning (Snyk, Trivy)

### Deploy Stage
- Environment promotion
- Rollback strategies
- Blue-green deployments
- Canary releases
- Notification integrations

## Examples

### GitHub Actions - Node.js with Docker

yaml
name: Build and Deploy
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm test
      - run: npm run build
      - uses: docker/build-push-action@v5
        with:
          push: ${{ github.ref == 'refs/heads/main' }}
          tags: ghcr.io/${{ github.repository }}:${{ github.sha }}
### GitLab CI - Python with K8s Deploy

yaml
stages:
  - test
  - build
  - deploy

test:
  stage: test
  image: python:3.12
  script:
    - pip install -r requirements.txt
    - pytest --junitxml=report.xml
  artifacts:
    reports:
      junit: report.xml

build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

deploy:
  stage: deploy
  image: bitnami/kubectl
  script:
    - kubectl set image deployment/app app=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  only:
    - main
---

💬 Feedback & Feature Requests: https://bytesagain.com/feedback
Powered by BytesAgain | bytesagain.com