---
category: software-development
name: frontend-performance
description: Analyzes and improves frontend performance: LCP, FCP, CLS, bundle size, lazy loading, and runtime efficiency. Use when 性能优化, 首屏慢, 卡顿, 打包体积, performance optimization, or improving Core Web Vitals.
---

# 前端性能优化（Frontend Performance）

分析并改进前端性能指标，提供可落地的优化方案与实施优先级。

## 触发场景

当用户提及以下关键词或场景时触发本技能：

- **关键词**：性能优化、首屏慢、页面卡顿、打包体积大、LCP/FCP/CLS 差
- **场景**：提供 Lighthouse 报告、Performance 录屏、具体慢的页面/操作
- **语言标签**：`performance optimization`、`Core Web Vitals`、`bundle size`

## 分析维度

### 1. 加载性能（LCP / FCP / TTI）

| 指标 | 含义 | 常见瓶颈 | 优化方向 |
|------|------|----------|----------|
| **LCP** | 最大内容绘制 | 大图未优化、服务器响应慢、渲染阻塞 | 图片优化（WebP/AVIF）、CDN、SSR/ISR、资源优先级 |
| **FCP** | 首次内容绘制 | JS/CSS 阻塞、关键路径过长 | 关键 CSS 内联、延迟非关键资源、Preload |
| **TTI** | 可交互时间 | 大 Bundle、主线程阻塞 | 代码分割、懒加载、Web Worker |

### 2. 体验稳定性（CLS / 运行时卡顿）

| 指标 | 常见原因 | 优化方案 |
|------|----------|----------|
| **CLS 高** | 图片/iframe 无尺寸、字体切换闪动、动态插入内容 | 明确宽高属性、`aspect-ratio`、CSS `font-display: optional/swap`、骨架屏占位 |
| **滚动/操作卡顿** | 大量重排重绘、长任务、大列表渲染 | 虚拟滚动、防抖节流、`will-change`、批量 DOM 操作 |

### 3. 资源与打包

| 问题类型 | 诊断方法 | 优化手段 |
|----------|----------|----------|
| **JS 体积大** | Bundle Analyzer 统计 | 路由级分割、按需引入、Tree Shaking、替换重型依赖 |
| **图片资源大** | Network 瀑布图 | 格式转换（WebP/AVIF）、响应式图片 `srcset`、`loading="lazy"` |
| **请求过多** | 请求合并分析 | 接口合并、HTTP/2 多路复用、缓存策略（Cache-Control/ETag） |

## 执行流程

### Step 1：现状量化

- Lighthouse 报告 → 记录 LCP/FCP/CLS/TTI/Speed Index 数值
- 慢操作 → 操作步骤 + 主观耗时 + Performance 面板时长
- Bundle 问题 → 主要 Chunk 体积 + 各模块占比
### Step 2：瓶颈定位

| 维度 | 工具/方法 | 关注点 |
|------|-----------|--------|
| 加载慢 | Network 瀑布图 | 阻塞资源、大文件、串行请求 |
| 运行慢 | Performance 面板 | Long Task、Layout Shift、Paint 耗时 |
| 打包大 | Bundle Analyzer | 体积占比、重复依赖、无效导出 |

### Step 3：方案评估

每个方案需标注：

- **收益**：预期提升的指标或体感改善
- **成本**：改动范围、风险等级、依赖条件
- **优先级**：高 / 中 / 低（高收益低风险优先）

### Step 4：落地顺序

快速见效（改动 < 1h）
  └── 图片压缩、font-display、关键 CSS 内联、静态资源缓存

中等改动（改动 1h - 1d）
  └── 路由级拆包、懒加载组件、接口合并、防抖节流

较大改动（改动 > 1d）
  └── SSR/ISR、虚拟列表、长任务拆分、Web Worker
## 输出模板

markdown
## 性能优化报告

### 现状分析
- **关键指标**：
  - LCP: Xms | FCP: Xms | CLS: X | TTI: Xms
  - Speed Index: Xms
- **主要瓶颈**：
  1. ...
  2. ...

### 优化方案

| # | 方案 | 预期收益 | 改动成本 | 优先级 |
|---|------|----------|----------|--------|
| 1 | ... | ... | 低/中/高 | 高/中/低 |
| 2 | ... | ... | 低/中/高 | ... |

### 实施路径
1. **立即执行**：...
2. **短期计划**：...
3. **长期规划**：...

### 验证方法
- [ ] 优化后 Lighthouse 复测
- [ ] Performance 面板对比
- [ ] 关键操作耗时对比（P75/P95）
## 框架特定建议

### Next.js

- **图片优化**：使用 `<Image>` 组件，自动格式转换与懒加载
- **Bundle 分析**：`npx @next/bundle-analyzer`
- **组件懒加载**：`next/dynamic` + `{ ssr: false }` 抑制首屏 SSR
- **Font 优化**：`next/font` 自动优化字体加载

### React

- **重渲染排查**：避免在渲染中创建新对象/函数，使用 `React.memo`/`useMemo`/`useCallback`
- **状态管理**：拆分大状态、避免全局状态触发无关组件重渲染
- **长列表**：优先虚拟滚动（`react-window`、`@tanstack/virtual`），再考虑分页

### Vue

- **组件懒加载**：动态导入 `() => import('./Comp.vue')`
- **图片**：使用 `v-lazy` 或 VueUse 的 `useImage`
- **重渲染**：`computed` 缓存、函数式组件减少开销

## 性能指标参考

| 指标 | 良好 | 需改进 | 差 |
|------|------|--------|-----|
| LCP | ≤ 2.5s | 2.5s - 4s | > 4s |
| FCP | ≤ 1.8s | 1.8s - 3s | > 3s |
| CLS | ≤ 0.1 | 0.1 - 0.25 | > 0.25 |
| TTI | ≤ 3.8s | 3.8s - 7.3s | > 7.3s |