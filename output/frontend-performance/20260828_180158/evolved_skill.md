---
name: frontend-performance
description: Analyzes and improves frontend performance: LCP, FCP, CLS, bundle size, lazy loading, and runtime efficiency. Use when 性能优化, 首屏慢, 卡顿, 打包体积, performance optimization, or improving Core Web Vitals.
---

# 前端性能优化

围绕加载性能与运行时性能，给出可落地的优化方案与优先级排序。

## 触发场景

当用户提供以下信息时激活此技能：

- **关键词**：性能优化、首屏慢、页面卡顿、打包体积大、LCP/FCP 差
- **证据**：Lighthouse 报告、Performance 录屏、具体慢的操作或页面
- **指标诉求**：Core Web Vitals 不达标、Speed Index 过高

## 分析维度

### 1. 加载性能（LCP / FCP / TTI）

| 指标 | 目标值 | 常见原因 | 优化方向 |
|------|--------|----------|----------|
| **LCP** | < 2.5s | 大图未优化、服务器响应慢、渲染阻塞 | 图片优化（WebP/AVIF）、CDN、预加载关键资源、SSR |
| **FCP** | < 1.8s | JS/CSS 阻塞、关键路径过长 | 关键 CSS 内联、拆分非关键资源、延迟加载 |
| **TTI** | < 3.8s | 大 bundle、主线程阻塞 | 代码分割、懒加载、Web Worker 迁移重计算 |

### 2. 体验稳定性（CLS / 运行时卡顿）

| 指标 | 目标值 | 常见原因 | 优化方向 |
|------|--------|----------|----------|
| **CLS** | < 0.1 | 无尺寸图片/广告/iframe、字体跳动、动态内容插入 | 明确宽高、font-display:optional/swap、预留占位空间 |
| **卡顿** | FPS < 30 | 长任务（>50ms）、频繁重排重绘、大列表无虚拟化 | 防抖节流、requestAnimationFrame、虚拟滚动 |

### 3. 资源与打包

| 问题类型 | 优化方向 |
|----------|----------|
| **JS 体积大** | 按路由拆包、动态 import、tree-shaking、替换大依赖（moment → dayjs）、分析 bundle |
| **图片体积大** | 格式转换（WebP/AVIF）、响应式图片 srcset、懒加载、CDN 分发 |
| **请求过多** | 资源合并、HTTP/2 多路复用、缓存策略（Cache-Control/ETag）、preconnect/preload |

## 执行流程

### Step 1：现状量化

收集以下信息：

- **有 Lighthouse**：记录 LCP/FCP/CLS/TTI/Speed Index 原始值
- **有 Performance 录屏**：定位具体慢的操作及耗时
- **有打包诉求**：提供当前主要 chunk 体积分布

### Step 2：定位瓶颈

| 工具 | 用途 |
|------|------|
| Network 面板 | 看瀑布图：哪些请求阻塞、哪些资源过大 |
| Performance 面板 | 看长任务（Task）、重排重绘（Layout/Recalc Styles） |
| Bundle 分析器 | `@next/bundle-analyzer` / `webpack-bundle-analyzer` 定位大模块 |

### Step 3：方案评估

每个方案需标注：

- **收益**：预期提升的指标或体感改善
- **成本**：改动量、风险、依赖
- **优先级**：高（快速见效）/ 中（需测试）/ 低（架构改动）

### Step 4：落地顺序

第一梯队（快速见效，1-2天）
├── 图片压缩与格式转换（WebP/AVIF）
├── 关键 CSS 内联
├── font-display 调整
└── 首屏图片懒加载改为预加载

第二梯队（中等改动，3-5天）
├── 路由级代码分割
├── 虚拟列表实现
├── HTTP 缓存策略优化
└── 第三方脚本延迟加载

第三梯队（架构调整，长期规划）
├── SSR/SSG 改造
├── 边缘计算（Edge Functions）
└── 微前端或模块联邦
## 输出模板

markdown
## 性能优化报告

### 现状
- **核心指标**：LCP __ms / FCP __ms / CLS __ / TTI __ms
- **主要瓶颈**：
  1. LCP 慢：原因…
  2. 打包体积：main.js __KB，过大的依赖…

### 优化方案

| # | 方案 | 收益 | 成本 | 优先级 |
|---|------|------|------|--------|
| 1 | 图片切换 WebP + 响应式 | LCP ↓300ms | 低（工具自动化） | 高 |
| 2 | 路由懒加载 | TTI ↓800ms | 低（改 import） | 高 |
| 3 | 关键 CSS 内联 | FCP ↓200ms | 中（需构建配置） | 中 |
| 4 | 虚拟列表 | FPS 30→60 | 中（组件替换） | 中 |
| 5 | SSR 改造 | LCP/TTI 大幅提升 | 高（架构改动） | 低 |

### 落地顺序
1. 图片格式优化 + 响应式图片
2. 路由懒加载 + 关键 CSS
3. 虚拟列表（长列表场景）
4. 缓存策略优化
5. 评估 SSR 必要性

### 验证方式
- [ ] Lighthouse 重跑，对比核心指标
- [ ] Performance 录屏复验慢操作
- [ ] bundle 分析确认体积下降
## 框架专项

### Next.js

- **图片优化**：`next/image` 自动 WebP/AVIF、懒加载、srcset
- **代码分割**：使用 `next/dynamic` 懒加载组件/路由
- **分析打包**：`@next/bundle-analyzer` 可视化体积
- **SSR/SSG**：`getServerSideProps` / `getStaticProps` 按场景选用

### React

- **避免无效重渲染**：
  - 不在 render 中创建新对象/函数/数组
  - 合理使用 `React.memo`、`useMemo`、`useCallback`
- **长列表**：优先虚拟滚动（`react-window` / `@tanstack/react-virtual`），再考虑分页
- **状态管理**：避免全局 store 过大，按需加载

### Vue

- **组件懒加载**：`defineAsyncComponent` + `() => import()`
- **图片优化**：`v-lazy` 指令或 `vue3-lazy`
- **性能观测**：`Vue Performance Devtool`

## 关键阈值速查

| 指标 | 良好 | 需改进 | 差 |
|------|------|--------|-----|
| LCP | < 2.5s | 2.5s - 4s | > 4s |
| FCP | < 1.8s | 1.8s - 3s | > 3s |
| CLS | < 0.1 | 0.1 - 0.25 | > 0.25 |
| TTI | < 3.8s | 3.8s - 7s | > 7s |
| FID | < 100ms | 100ms - 300ms | > 300ms |