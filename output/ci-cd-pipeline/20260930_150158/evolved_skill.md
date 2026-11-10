---
category: software-development
name: ci-cd-pipeline
description: "Generate and configure CI/CD pipelines for GitHub Actions, GitLab CI, Jenkins, and Docker. Includes build, test, and deployment workflows."
---

# CI/CD Pipeline

Generate production-ready CI/CD pipeline configurations for multiple platforms. Supports GitHub Actions, GitLab CI, Jenkins, and Docker-based workflows.

## Usage

ci-cd-pipeline <command> [options]
## Commands

| Command | Description |
|---------|-------------|
| `github` | Generate GitHub Actions workflow (`.github/workflows/`) |
| `gitlab` | Generate GitLab CI pipeline (`.gitlab-ci.yml`) |
| `jenkins` | Generate Jenkinsfile |
| `docker` | Generate Docker build and push workflows |
| `test` | Generate test automation configurations |
| `deploy` | Generate deployment configurations (K8s, AWS, etc.) |

## Examples

### Generate a GitHub Actions pipeline for a Node.js project

bash
ci-cd-pipeline github --language node --test npm test --deploy
### Generate a GitLab CI pipeline for a Python project

bash
ci-cd-pipeline gitlab --language python --test pytest
### Generate a Jenkins pipeline with Docker

bash
ci-cd-pipeline jenkins --docker --test maven
### Generate a complete Docker CI/CD workflow

bash
ci-cd-pipeline docker --build --push --registry ghcr.io
### Generate test configuration only

bash
ci-cd-pipeline test --framework jest --coverage
### Generate Kubernetes deployment configuration

bash
ci-cd-pipeline deploy --target kubernetes --registry docker.io/myapp
## Supported Languages

- Node.js / TypeScript
- Python
- Java
- Rust
- Go
- Ruby

## Supported Platforms

| Platform | Config File |
|----------|-------------|
| GitHub Actions | `.github/workflows/*.yml` |
| GitLab CI | `.gitlab-ci.yml` |
| Jenkins | `Jenkinsfile` |
| Docker | `Dockerfile`, `docker-compose.yml` |

## Options

| Option | Description |
|--------|-------------|
| `--language` | Project language (node, python, java, rust, go, ruby) |
| `--test` | Test command to run |
| `--deploy` | Enable deployment step |
| `--docker` | Include Docker build/push |
| `--registry` | Container registry URL |
| `--coverage` | Enable coverage reporting |
| `--output` | Output directory (default: current directory) |

## Common Workflows

### Node.js with GitHub Actions

yaml
name: Node.js CI

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
      - run: npm ci
      - run: npm test
      - run: npm run build
### Python with GitLab CI

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
    - pytest --cov

build:
  stage: build
  script:
    - docker build -t myapp:$CI_COMMIT_SHA .
  only:
    - main

deploy:
  stage: deploy
  script:
    - docker push myapp:$CI_COMMIT_SHA
  only:
    - main
---
*CI/CD Pipeline by BytesAgain*
*Feedback: https://bytesagain.com/feedback*