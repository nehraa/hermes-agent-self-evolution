---
category: software-development
name: frontend-performance
description: Analyzes and improves frontend performance: LCP, FCP, CLS, bundle size, lazy loading, and runtime efficiency. Use when 性能优化, 首屏慢, 卡顿, 打包体积, performance optimization, or improving Core Web Vitals.
---

# 前端性能优化（Frontend Performance）

分析并优化前端性能，提供可落地的方案与优先级建议。

## 触发场景

- 用户提到：性能优化、首屏慢、页面卡顿、打包体积大、LCP/FCP 差
- 提供 Lighthouse 报告、Performance 录屏、具体慢的页面/操作
- 新项目需要预防性优化建议

## 核心指标

| 指标 | 含义 | 目标值 |
|------|------|--------|
| LCP | 最大内容绘制（加载速度） | < 2.5s |
| FCP | 首次内容绘制 | < 1.8s |
| CLS | 累计布局偏移（稳定性） | < 0.1 |
| TTI | 可交互时间 | < 3.8s |
| FID/INP | 交互延迟（响应性） | < 100ms |

## 分析维度

### 1. 加载性能

| 问题 | 常见原因 | 优化方向 |
|------|----------|----------|
| LCP 慢 (>2.5s) | 未压缩大图、LCP 元素加载晚、服务器响应慢 | 图片优化（WebP/AVIF + 正确尺寸）、预加载关键资源、CDN、SSR/ISR |
| FCP 慢 (>1.8s) | JS/CSS 阻塞渲染、首屏依赖过多同步资源 | 关键 CSS 内联、JS 延迟/拆分、preconnect/prefetch |
| TTI 长 (>3.8s) | 大 bundle 阻塞主线程、长任务 | 代码分割、懒加载、Web Workers、减少主线程工作 |

### 2. 运行时性能

| 问题 | 常见原因 | 优化方向 |
|------|----------|----------|
| CLS 高 (>0.1) | 图片/iframe 无尺寸、字体加载闪烁、动态内容插入 | 明确宽高比、font-display: optional/swap、CSS aspect-ratio、占位符 |
| 滚动卡顿 | 重排/重绘过多、长任务阻塞、大列表无虚拟化 | 虚拟滚动、防抖节流、requestAnimationFrame、will-change、批量 DOM 操作 |
| 点击/输入延迟 | 复杂事件处理、主线程阻塞 | 事件委托、Web Worker、useMemo/useCallback、减少 re-render |

### 3. 资源与打包

| 问题 | 优化方向 |
|------|----------|
| JS bundle 大 | 按路由/组件拆包、tree-shaking、动态导入、分析并替换大依赖（lodash-es、moment.js） |
| 图片未优化 | 格式转换（WebP/AVIF）、响应式尺寸、懒加载、CDN 加速 |
| 请求过多 | 资源合并、HTTP/2、缓存策略（Cache-Control/ETag）、预连接/preload |

## 执行流程

### 1. 现状量化

**有数据时：**
- 记录 Lighthouse 各项分数与具体指标（LCP/FCP/CLS/TTI/Speed Index）
- 标注 Lighthouse 的优化建议

**无数据时：**
- 描述慢的操作 + 主观感受或 Performance 录制时长
- 记录网络环境（4G/宽带）+ 设备类型（低端机/旗舰机）

### 2. 定位瓶颈

**加载问题：**
- Network 面板：分析瀑布图，找出阻塞请求、大资源、慢响应
- 重点关注：首屏关键路径资源

**运行时问题：**
- Performance 面板：查看长任务（>50ms）、强制同步布局（Layout Thrashing）
- 重点关注：Main 线程时间线

**打包问题：**
- `@next/bundle-analyzer` / `webpack-bundle-analyzer`
- 识别大模块、重复依赖、无用导出

### 3. 制定方案

每项方案标注：

- **收益**：具体影响的指标（如 LCP 预期降低 Xms）或体感改善
- **成本**：改动量（新增文件/改配置/重构）、风险、团队学习成本
- **优先级**：高（收益大+成本低）/ 中 / 低（收益小或成本高）

### 4. 落地顺序

**第一梯队（快速见效，1-2天）：**
- 图片格式转换 + 懒加载
- 关键 CSS 内联
- font-display 优化
- 简单路由级代码分割

**第二梯队（中等改动，3-5天）：**
- 组件级懒加载
- 虚拟列表实现
- 缓存策略配置
- 大依赖替换（如 moment → dayjs）

**第三梯队（架构调整，按需）：**
- SSR/ISR 改造
- 边缘渲染
- 微前端拆分
- 构建流程优化

## 输出模板

markdown
## 性能优化报告

### 现状
- **核心指标**：LCP Xs / FCP Xs / CLS X / TTI Xs
- **主要瓶颈**：…
- **触发场景**：…

### 优化方案

| # | 方案 | 收益 | 成本 | 优先级 |
|---|------|------|------|--------|
| 1 | … | … | … | 高 |
| 2 | … | … | … | 中 |

### 建议落地顺序
1. [高] …（预计收益：…）
2. [高] …（预计收益：…）
3. [中] …（预计收益：…）

### 验证方式
- 工具：Lighthouse CI / WebPageTest / Performance 录制
- 指标：优化前后对比 LCP/FCP/CLS/TTI
- 体感：关键操作耗时实测

### 风险与注意事项
- …
## 框架专项

### Next.js

- **图片**：`next/image`（自动 WebP + 懒加载 + 尺寸优化）
- **组件懒加载**：`dynamic(() => import(...), { ssr: false })`
- **分析**：`@next/bundle-analyzer` 插件
- **Font**：`next/font`（自动优化字体加载）

### React

- **避免无效重渲染**：render 中不创建新对象/函数、适当使用 memo/useMemo/useCallback
- **列表**：虚拟滚动优先（react-window / tanstack-virtual）
- **状态**：用 useDeferredValue/useTransition 标记非紧急更新

### Vue

- **图片**：`v-lazy` / `vue3-lazy`
- **组件**：`defineAsyncComponent`
- **列表**：vue-virtual-scroller
- **分析**：`rollup-plugin-visualizer`

## 推荐工具

| 用途 | 工具 |
|------|------|
| 性能测试 | Lighthouse, WebPageTest, Chrome DevTools |
| Bundle 分析 | webpack-bundle-analyzer, @next/bundle-analyzer, source-map-explorer |
| 运行时分析 | Performance 面板, React DevTools Profiler, Vue DevTools |
| 监控 | Web Vitals, Sentry Performance, Datadog |
| 图片优化 | Squoosh, Sharp, Cloudinary |