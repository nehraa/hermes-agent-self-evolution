---
category: software-development
description: Analyzes and improves frontend performance: LCP, FCP, CLS, bundle size, lazy loading, and runtime efficiency. Use when 性能优化, 首屏慢, 卡顿, 打包体积, performance optimization, or improving Core Web Vitals.
name: frontend-performance
---

# 前端性能优化（Frontend Performance）

分析页面加载性能与运行时性能，识别瓶颈，提供可落地的优化方案与实施优先级。

## 触发场景

| 用户意图 | 触发条件 |
|----------|----------|
| 性能投诉 | 「首屏慢」「页面卡顿」「加载慢」「操作不流畅」 |
| 指标不达标 | LCP > 2.5s、FCP > 1.8s、CLS > 0.1、INP > 200ms |
| 打包优化 | 「bundle 太大」「首屏加载资源过多」「打包慢」 |
| 主动优化 | 提供 Lighthouse 报告、Performance 录屏、具体慢的操作步骤 |

## 分析维度

### 1. 加载性能（LCP / FCP / TBT）

| 指标 | 问题表现 | 常见根因 | 优化方向 |
|------|----------|----------|----------|
| **LCP** | 首屏大元素加载慢 | 大图未优化、服务器响应慢、资源优先级低 | 图片格式优化（WebP/AVIF）、CDN、preload 关键资源、SSR/ISR |
| **FCP** | 页面有内容但不可交互 | JS/CSS 阻塞渲染、首屏依赖第三方脚本 | 关键 CSS 内联、defer/async、非关键脚本延迟 |
| **TBT** | 页面可交互但响应慢 | 主线程被长任务占用 | 代码分割、减少第三方脚本、Web Worker |

### 2. 体验稳定性（CLS / INP）

| 指标 | 问题表现 | 常见根因 | 优化方向 |
|------|----------|----------|----------|
| **CLS** | 页面元素跳动、布局偏移 | 图片/广告/字体无尺寸、动态插入内容 | `width`/`height` 属性、aspect-ratio、font-display:optional/swap、骨架屏 |
| **INP** | 点击/输入响应延迟 | 长任务阻塞主线程、频繁重渲染 | 防抖节流、useCallback/useMemo、虚拟滚动、Web Worker |

### 3. 运行时性能（卡顿 / 内存）

| 问题 | 常见场景 | 优化方向 |
|------|----------|----------|
| 滚动卡顿 | 大列表、无虚拟化、频繁布局 | 虚拟滚动（react-window/tanstack-virtual）、will-change、transform |
| 操作响应慢 | 频繁重渲染、复杂计算 | React.memo、useMemo、useCallback、减少不必要的状态更新 |
| 内存泄漏 | 定时器未清理、闭包引用、事件监听未移除 | 组件卸载清理、useEffect cleanup、弱引用 |

### 4. 资源与打包

| 问题 | 诊断方法 | 优化方向 |
|------|----------|----------|
| JS 体积大 | bundle analyzer、webpack-bundle-analyzer | 按路由拆分、动态 import、tree-shaking、替换大依赖（moment→dayjs） |
| 图片未优化 | Network 瀑布图、 Lighthouse | 格式转换（WebP/AVIF）、响应式图片（srcset）、懒加载（loading="lazy"）、CDN |
| 请求过多 | 瀑布图分析 | 合并请求、缓存策略（Cache-Control/ETag）、preconnect/prefetch |
| 重复依赖 | bundle analyzer 重复包检测 | 提取公共依赖、monorepo 共享、别名配置 |

## 执行流程

### Step 1: 现状量化

**有 Lighthouse/PageSpeed Insights：**
- 记录 Core Web Vitals（LCP、FCP、CLS、INP）
- 记录 Speed Index、TBT、SI 分数
- 截图或导出 HTML 报告

**有 Performance 录屏：**
- 记录慢的操作路径 + 主观耗时 / Performance 面板时长
- 标记 Long Task 位置

**有打包诉求：**
- 记录当前首屏主要 chunk 体积
- 记录总 bundle 大小与模块数量

### Step 2: 找瓶颈

**加载问题：**
- Network 面板：瀑布图中哪些请求阻塞、过大、未缓存
- 关键路径：首屏渲染必需的 JS/CSS/字体/图片

**运行时问题：**
- Performance 面板：Long Task 分布、Main Thread 占用
- React DevTools Profiler：哪些组件频繁渲染、渲染耗时

**打包问题：**
- `@next/bundle-analyzer` / `webpack-bundle-analyzer`
- 定位大模块、重复依赖、tree-shaking 失效

### Step 3: 评估方案性价比

对每个方案标注：

| 维度 | 说明 |
|------|------|
| **收益** | 预期改善的指标（如 LCP -500ms）或体感提升 |
| **成本** | 改动范围、风险、是否需要设计/后端配合 |
| **优先级** | 高（高收益低风险）/ 中 / 低（收益有限或风险高） |

### Step 4: 给出落地顺序

| 阶段 | 特征 | 典型方案 |
|------|------|----------|
| **快速见效** | 成本低、风险小、改动范围小 | 图片尺寸/格式、font-display、关键 CSS 内联、懒加载非首屏组件 |
| **中等改动** | 需要规划、可能涉及架构 | 路由级拆包、虚拟列表、缓存策略、React 渲染优化 |
| **大改动** | 架构调整、跨团队协作 | SSR/ISR、边缘渲染、CDN 重构、数据库/接口优化 |

## 输出模板

markdown
## 性能优化报告

### 现状
- **Core Web Vitals / Lighthouse 分数**：LCP ___ms / FCP ___ms / CLS ___ / INP ___ms
- **主要瓶颈**：
  1. ___（如：大图未优化、bundle 体积过大、长任务阻塞）
  2. ___
  3. ___

### 优化方案

| # | 方案 | 预期收益 | 成本/风险 | 优先级 |
|---|------|----------|-----------|--------|
| 1 | ___ | ___ | 低/中/高 | 高/中/低 |
| 2 | ___ | ___ | 低/中/高 | 高/中/低 |
| 3 | ___ | ___ | 低/中/高 | 高/中/低 |

### 建议落地顺序
1. **（优先级1）**：___ — ___ 天完成
2. **（优先级2）**：___ — ___ 天完成
3. **（优先级3）**：___ — ___ 天完成

### 验证方式
- [ ] 优化后复测 Lighthouse / PageSpeed Insights
- [ ] Performance 录屏对比（Before/After）
- [ ] 关键操作耗时测量（如：首页加载、列表滚动、表单提交）
- [ ] 生产环境 Real User Monitoring（RUM）数据监控
## 框架/工具参考

### Next.js

| 场景 | 方案 |
|------|------|
| 图片优化 | `<Image>` 组件 + WebP/AVIF + `sizes` 属性 |
| 组件懒加载 | `dynamic(() => import('./Heavy'), { loading: () => <Skeleton /> })` |
| bundle 分析 | `next build && @next/bundle-analyzer` |
| 字体优化 | `next/font` 自动优化 + font-display 策略 |
| SSR/SSG | 静态生成或 ISR 优先，减少客户端数据获取 |

### React

| 场景 | 方案 |
|------|------|
| 避免无效重渲染 | React.memo + useMemo + useCallback（按需使用，避免过度优化） |
| 渲染时对象创建 | 避免在 JSX 或 useEffect 依赖中创建新对象/函数 |
| 长列表 | react-window / @tanstack/react-virtual 虚拟滚动 |
| 状态管理 | 状态粒度合理、避免全局状态频繁更新触发大量订阅 |

### 通用

| 场景 | 方案 |
|------|------|
| 懒加载 | 路由级：React.lazy + Suspense；组件级：Intersection Observer |
| 防抖节流 | lodash debounce/throttle，或自定义 useDebounce/useThrottle |
| 动画性能 | 优先 transform/opacity，启用 GPU 加速（will-change: transform） |
| 缓存 | Service Worker（Workbox）、HTTP 缓存头、localStorage/sessionStorage |