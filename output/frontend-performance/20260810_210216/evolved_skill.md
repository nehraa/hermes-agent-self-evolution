---
category: software-development
description: Analyzes and improves frontend performance: LCP, FCP, CLS, bundle size, lazy loading, and runtime efficiency. Use when 性能优化, 首屏慢, 卡顿, 打包体积, performance optimization, or improving Core Web Vitals.
name: frontend-performance
---

# 前端性能优化（Frontend Performance）

围绕加载性能与运行时性能，提供可落地的诊断与优化方案。

## 触发场景

- 用户提及「性能优化」「首屏慢」「页面卡顿」「打包体积大」
- 提供 Lighthouse/PageSpeed Insights 报告、WebPageTest 截图
- 涉及 Core Web Vitals（LCP/FCP/CLS/INP）问题
- 提到具体慢的页面、操作或交互

## 核心指标与目标值

| 指标 | 含义 | 良好 | 需要优化 | 差 |
|------|------|------|----------|-----|
| LCP | 最大内容绘制 | < 2.5s | 2.5s - 4s | > 4s |
| FCP | 首次内容绘制 | < 1.8s | 1.8s - 3s | > 3s |
| CLS | 累积布局偏移 | < 0.1 | 0.1 - 0.25 | > 0.25 |
| INP | 交互到绘制（新版 FID） | < 200ms | 200ms - 500ms | > 500ms |
| TTI | 可交互时间 | < 3.8s | 3.8s - 7.3s | > 7.3s |

## 分析维度

### 1. 加载性能（LCP / FCP / TTI）

**LCP 慢（目标 < 2.5s）**

常见原因：
- 页面顶部大图未优化（尺寸、格式、延迟加载）
- 字体文件阻塞渲染
- 服务器响应慢（TTFB > 600ms）
- 首屏内容依赖 JS 执行后才渲染

优化方向：
- LCP 图片使用 `<link rel="preload">` 预加载
- 图片使用 WebP/AVIF 格式，尺寸匹配显示尺寸
- 关键 CSS 内联，延迟非关键 CSS
- 考虑 SSR/SSG 减少服务器等待时间
- 使用 CDN 减少网络延迟

**FCP 慢（目标 < 1.8s）**

常见原因：
- 大型 JS bundle 阻塞解析
- 渲染阻塞 CSS（字体、第三方样式）
- 大量第三方脚本

优化方向：
- 拆分 bundle，按路由代码分割
- `<script async>` 异步加载非关键脚本
- 关键 CSS 内联，其余延迟加载
- 预连接关键域名（字体、CDN）

**TTI 长（目标 < 3.8s）**

常见原因：
- 主线程被长任务阻塞
- 大型 bundle 未充分拆分
- 过多同步模块加载

优化方向：
- 代码分割，动态 import 懒加载
- 使用 Web Workers 处理计算密集任务
- 分析并替换大体积依赖
- 删除未使用代码（tree-shaking）

### 2. 体验稳定性（CLS / 卡顿）

**CLS 高（目标 < 0.1）**

常见原因：
- 图片/视频无固定尺寸
- 字体加载导致布局跳动（FOIT/FOUT）
- 动态插入内容（广告、banner）
- 异步加载的 CSS 导致样式突变

优化方向：
- 所有图片/视频设置 `width` 和 `height` 或 `aspect-ratio`
- 使用 `font-display: swap` 或 `optional`
- 字体文件使用 `preload` 减少加载时间
- 为动态内容预留空间或使用骨架屏
- 避免在 CLS 关键区域动态注入内容

**滚动/交互卡顿（INP 高）**

常见原因：
- 渲染周期中大量重排/重绘
- 长任务阻塞主线程
- 大列表无虚拟滚动
- 频繁触发样式计算的动画

优化方向：
- 避免在滚动时改变布局属性（用 transform/opacity）
- 使用 `will-change` 提示浏览器优化
- 虚拟化长列表（react-window、vue-virtual-scroller）
- 对高频事件（scroll、resize）节流/防抖
- 复杂计算移至 requestAnimationFrame 或 Web Worker

### 3. 资源与打包

**JS Bundle 体积**

| 优化手段 | 说明 |
|----------|------|
| 路由级分割 | 每个页面只加载必要代码 |
| 组件懒加载 | 非首屏组件用 `React.lazy()` / `defineAsyncComponent` |
| Tree-shaking | 确保使用 ESM，移除未引用代码 |
| 依赖分析 | 用 bundle analyzer 可视化各模块占比 |
| 替代方案 | 替换大体积库（如用 date-fns 替代 moment） |

**图片优化**

| 手段 | 说明 |
|------|------|
| 格式选择 | WebP（平均-30%体积）/ AVIF（更高压缩率） |
| 尺寸响应 | `srcset` 提供多尺寸，避免下载过大图片 |
| 懒加载 | `loading="lazy"` 或 Intersection Observer |
| CDN | 使用图片 CDN 自动优化（压缩、格式转换、裁剪） |
| 占位符 | LQIP 或骨架屏减少感知加载时间 |

**网络请求**

- 合并小请求（内联小资源、合并 API 请求）
- HTTP 缓存：`Cache-Control`、`ETag`、`Last-Modified`
- 预加载：`preconnect`、`dns-prefetch`、`prefetch`、`preload`
- 关键请求优先：`<link rel="preload">` 关键资源

## 执行流程

### 1. 现状量化

**量化指标：**
- Lighthouse/PageSpeed Insights 的核心指标数值
- WebPageTest 瀑布图中各请求时间
- 具体慢的操作描述 + 主观感受或 Performance API 记录

**Bundle 分析：**
- 当前主要 chunk 体积
- 最大的 5 个模块及来源

### 2. 找瓶颈

**加载瓶颈诊断：**
- Network 面板：瀑布图中哪些请求阻塞渲染、哪些过大
- Waterfall 分析：TTFB、下载时间、首字节到渲染的时间

**运行时瓶颈诊断：**
- Performance 面板：录制慢操作，查看长任务（> 50ms）、布局抖动
- 查找「强制同步布局」和「大量样式计算」

**Bundle 瓶颈诊断：**
- `webpack-bundle-analyzer` / `next/bundle-analyzer` / `rollup-plugin-visualizer`
- 定位大模块和无用依赖

### 3. 方案评估框架

每个方案标注：

| 维度 | 评估内容 |
|------|----------|
| **收益** | 预期提升的指标数值或体感改善 |
| **成本** | 改动范围、风险、测试工作量 |
| **依赖** | 是否依赖特定框架/架构 |
| **优先级** | 高（收益大/成本低）/ 中 / 低 |

### 4. 落地顺序建议

**第一阶段：快速见效（1-2天）**

- 图片添加尺寸/使用现代格式
- 字体 `font-display: swap` + 预加载
- 关键 CSS 内联
- 首屏图片懒加载改为预加载
- 移除阻塞渲染的第三方脚本

**第二阶段：中等投入（3-5天）**

- 路由级代码分割
- 非首屏组件懒加载
- 列表虚拟滚动
- 缓存策略优化（Service Worker、HTTP 缓存头）
- 高频事件节流防抖

**第三阶段：架构优化（1周+）**

- SSR/SSG 改造
- 边缘计算/边缘渲染
- 微前端按需加载
- 大型依赖替换或自研轻量方案

## 输出模板

markdown
## 性能优化报告

### 现状
- **Core Web Vitals**：[LCP] / [FCP] / [CLS] / [INP]
- **主要问题**：…
- **瓶颈位置**：…

### 优化方案

| # | 方案 | 预期收益 | 成本 | 优先级 |
|---|------|----------|------|--------|
| 1 | … | LCP 降低 500ms | 低 | 高 |
| 2 | … | CLS 降低 0.15 | 中 | 高 |
| 3 | … | TTI 降低 1s | 中 | 中 |

### 落地顺序
1. [快速见效项]
2. [中等改动项]
3. [架构优化项]

### 验证方式
- 工具：Lighthouse、PageSpeed Insights、WebPageTest、Performance 面板
- 方法：优化前后同环境对比，记录核心指标变化
- 用户感知：关键操作响应时间自测
## 框架/工具特定建议

### Next.js

- 路由级分割：默认行为，检查是否有过大 `page.js`
- 图片优化：`<Image>` 组件自动 WebP、懒加载、尺寸优化
- 动态导入：`next/dynamic` 懒加载组件和三方库
- Bundle 分析：`@next/bundle-analyzer`
- Font 优化：`next/font` 自动优化字体加载

### React

- 避免渲染时创建新对象/函数导致子组件无效重渲染
- 适当使用 `React.memo`、`useMemo`、`useCallback`
- 大量列表渲染优先虚拟滚动（react-window、react-virtualized）

### Vue

- 列表渲染使用 `v-virtual-scroller` 或 `vue-virtual-scroll-grid`
- 组件懒加载：`() => import('./Comp.vue')`
- 大列表避免响应式开销：使用 `Object.freeze()` 或非响应式数据

### 通用 Bundle 优化

- 依赖替代：moment → date-fns/dayjs；lodash → lodash-es/esbuild-plugin-lodash
- 图片 CDN：Cloudflare Images、Cloudinary、Vercel Image Optimization
- 压缩：Gzip/Brotli（服务器配置）
- 分析工具：webpack-bundle-analyzer、rollup-plugin-visualizer、esbuild-bundle-analyzer