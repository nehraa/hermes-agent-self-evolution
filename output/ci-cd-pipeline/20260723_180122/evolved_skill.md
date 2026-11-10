---
category: software-development
name: ci-cd-pipeline
description: "CI/CD Pipeline Generator - Generate and configure CI/CD pipelines for GitHub Actions, GitLab CI, Jenkins, and Docker. Automate your build, test, and deployment workflows."
version: "2.0.0"
author: BytesAgain
---

# CI/CD Pipeline

自动化CI/CD流水线配置工具。支持GitHub Actions、GitLab CI、Jenkins和Docker镜像构建、测试、部署流程。

Automated CI/CD pipeline configuration tool. Generate pipelines for building, testing, and deploying your code.

## 触发条件 | Triggers

- 任何CI/CD相关需求 | Any CI/CD related request
- 关键词: `ci`, `cd`, `pipeline`, `github actions`, `gitlab`, `jenkins`, `docker`, `deploy`, `自动化部署`, `流水线配置`

## 命令 | Commands

| 命令 | 功能 | Description |
|------|------|-------------|
| `github` | GitHub Actions | GitHub Actions workflow配置 |
| `gitlab` | GitLab CI | GitLab CI/CD pipeline配置 |
| `jenkins` | Jenkins | Jenkinsfile和pipeline配置 |
| `docker` | Docker构建 | Docker镜像构建和推送 |
| `test` | 测试配置 | 自动化测试配置 |
| `deploy` | 部署配置 | 部署脚本和环境配置 |

## 使用方法 | Usage

### 基本流程 | Basic Flow

bash
# 1. 启动工具
ci-cd-pipeline

# 2. 选择需要的平台命令
ci-cd-pipeline github

# 3. 描述你的需求
# 例如: Node.js项目，主分支部署到AWS，测试通过后自动部署
### 快速示例 | Quick Examples

bash
# 生成GitHub Actions配置
ci-cd-pipeline github

# 生成Docker CI配置
ci-cd-pipeline docker

# 生成完整测试+部署流程
ci-cd-pipeline test && ci-cd-pipeline deploy
## 常用配置 | Common Configurations

### GitHub Actions

- **Node.js/Python/Go/Rust** 项目的构建和测试
- **多环境部署** (staging/production)
- **Docker镜像构建** 和容器化部署
- **定时任务** 和手动触发工作流

### GitLab CI

- **Auto DevOps** 快速配置
- **Docker镜像构建** 和Harbor推送
- **Kubernetes部署** 配置
- **多分支流水线** 配置

### Jenkins

- **Jenkinsfile** 声明式/脚本式流水线
- **Blue Ocean** 可视化配置
- **分布式构建** 节点配置
- **制品管理** 和版本控制

## 配置参数 | Parameters

| 参数 | 说明 |
|------|------|
| `--language` | 项目语言 (node, python, java, go, rust) |
| `--platform` | 目标平台 (aws, gcp, azure, k8s, vm) |
| `--registry` | 镜像仓库 (dockerhub, gcr, ecr, harbor) |
| `--env` | 环境变量配置 |

## 示例配置 | Example Configs

### Node.js项目 → GitHub Actions

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
    strategy:
      matrix:
        node-version: [16.x, 18.x, 20.x]

    steps:
      - uses: actions/checkout@v4
      - name: Use Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'
      - run: npm ci
      - run: npm test
---

💬 Feedback & Feature Requests: [https://bytesagain.com/feedback](https://bytesagain.com/feedback)

Powered by BytesAgain | [bytesagain.com](https://bytesagain.com)