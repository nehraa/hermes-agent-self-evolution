---
name: frontend-performance
description: Analyzes and improves frontend performance: LCP, FCP, CLS, bundle size, lazy loading, and runtime efficiency. Use when 性能优化, 首屏慢, 卡顿, 打包体积, performance optimization, or improving Core Web Vitals.
---

# 前端性能优化（Frontend Performance）

围绕 **Core Web Vitals** 与运行时效率，提供可落地的诊断思路与优化方案。

## 触发场景

| 触发词 | 说明 |
|--------|------|
| 性能优化、首屏慢、页面卡顿 | 通用性能问题 |
| 打包体积大、bundle 大 | 构建产物问题 |
| LCP/FCP/CLS 差 | Core Web Vitals 问题 |
| Lighthouse 报告、Performance 录屏 | 有诊断数据 |

## 诊断框架

### 维度一：加载性能（LCP / FCP / TTI）

| 指标 | 问题 | 根因 | 优化方向 |
|------|------|------|----------|
| **LCP** | 首屏内容加载慢 | 大图片、未优化、服务器慢 | 图片优化（WebP/AVIF）、CDN、SSR/预渲染、关键资源优先 |
| **FCP** | 白屏时间长 | JS/CSS 阻塞、渲染受阻 | 关键 CSS 内联、代码分割、defer/async 脚本 |
| **TTI** | 可交互慢 | 大 bundle、长任务 | 路由级代码分割、懒加载、减少主线程阻塞 |

### 维度二：体验稳定性（CLS / 卡顿）

| 问题 | 根因 | 优化方向 |
|------|------|----------|
| **CLS 高** | 图片/视频 无尺寸、字体切换、动态插入内容 | 固定宽高比、font-display:optional/swap、预留占位空间 |
| **滚动/操作卡顿** | 重排/重绘多、长任务阻塞、列表无虚拟化 | 防抖节流、requestAnimationFrame、虚拟滚动、减少 layout thrashing |

### 维度三：资源与打包

| 症状 | 诊断 | 优化方向 |
|------|------|----------|
| JS bundle 过大 | 分析工具定位大模块 | 按路由拆分、按需引入、tree-shaking、替换重型依赖 |
| 图片体积大 | 格式/尺寸问题 | WebP/AVIF 格式、响应式尺寸、CDN、懒加载 |
| 请求数过多 | 资源未合并/缓存 | 合并请求、HTTP 缓存、preload/prefetch、preconnect |

## 执行流程

### Step 1：量化现状

- **有 Lighthouse**：记录 LCP / FCP / CLS / TTI / Speed Index 数值
- **有慢操作**：记录操作步骤 + 主观耗时或 Performance 录制时长
- **有 bundle 问题**：记录主要 chunk 体积与数量

### Step 2：定位瓶颈

加载问题 → Network 瀑布图 → 阻塞资源 / 大文件 / 串行请求
运行时问题 → Performance 录制 → Long Task / 布局抖动 / 强制同步布局
打包问题 → bundle analyzer → 大模块 / 重复依赖 / 未 tree-shaking
### Step 3：方案评估

每个方案标注：

| 维度 | 说明 |
|------|------|
| **收益** | 预期影响的指标（Lighthouse 提升、体感改善） |
| **成本** | 改动量、风险、团队依赖 |
| **优先级** | 高/中/低（高收益低成本优先） |

### Step 4：落地顺序

1. **快速见效**（低成本高收益）
   - 图片添加尺寸/格式转换
   - font-display:swap
   - 关键 CSS 内联
   - 首屏资源 preload

2. **中等改动**（中等成本中等收益）
   - 路由级代码分割
   - 组件懒加载
   - 虚拟滚动列表
   - 缓存策略优化

3. **架构级改动**（高成本高收益）
   - SSR / Edge Rendering
   - 微前端拆分
   - 后端接口优化
   - CDN 架构调整

## 输出模板

markdown
## 性能优化报告

### 现状
- **指标**：LCP __ms / FCP __ms / CLS __ / TTI __ms
- **主要瓶颈**：…
- **慢操作**（如有）：…

### 优化方案（按优先级排序）

| # | 方案 | 收益 | 成本 | 优先级 |
|---|------|------|------|--------|
| 1 | … | … | … | 高 |
| 2 | … | … | … | 中 |

### 建议落地顺序
1. …
2. …
3. …

### 验证方式
- Lighthouse 复测对比
- Performance 录制确认长任务减少
- 关键操作耗时对比
## 框架特定建议

### Next.js

javascript
// 组件级懒加载
const HeavyComponent = dynamic(() => import('../components/Heavy'), { loading: () => <Skeleton /> })

// 图片优化
import Image from 'next/image'
<Image src="/hero.webp" width={800} height={400} alt="" />

// Bundle 分析
// npx @next/bundle-analyzer
### React

- 避免在 render 中创建新对象/函数 → 子组件不必要的重渲染
- 必要时使用 `React.memo` / `useMemo` / `useCallback`
- 长列表优先虚拟滚动（react-window、@tanstack/virtual）

### 通用

- 首屏图片务必设置 `width` + `height` 防止 CLS
- 第三方脚本用 `defer` 或动态 import
- 字体加载用 `font-display: swap` 或 `optional`