---
category: software-development
description: >-
  前端设计质量提升 skill。让 AI 生成的 UI/前端代码更专业，避免常见设计反模式。
  参考 impeccable 项目的设计语言规范，提供 audit/polish/critique 等设计审查命令。
  触发词：/audit /polish /critique /colorize /animate /bolder /quieter /distill
  以及：审查UI设计、优化界面、前端设计建议、让设计更好看、检查设计质量
name: frontend-design-pro
author: antonia-sz
version: 1.0.0
---

# Frontend Design Pro

让 AI 生成的前端代码摆脱「千篇一律的模板感」，生成专业、有辨识度的用户界面。

灵感来源：[impeccable](https://github.com/pbakaus/impeccable)

---

## 设计命令

| 命令 | 用途 |
|------|------|
| `/audit` | 审查当前设计的反模式和质量问题 |
| `/polish` | 润色优化现有代码的设计细节 |
| `/critique` | 深度分析设计的优缺点 |
| `/colorize` | 应用配色方案到组件 |
| `/animate` | 添加合适的动效 |
| `/bolder` | 增强视觉层次和对比度 |
| `/quieter` | 降低视觉噪音，简化界面 |
| `/distill` | 提炼核心内容，移除冗余 |

---

## 常见反模式（主动避免）

LLM 默认输出容易陷入这些陷阱，生成代码时必须主动规避：

| 反模式 | 问题 | 解决方案 |
|--------|------|----------|
| Inter + 紫色渐变 | 过度使用的默认值，毫无个性 | 选择有个性的字体 + 战略用色 |
| 卡片嵌套卡片 | 层次混乱，信息层级不清 | 单一视觉层级原则 |
| 彩色背景 + 灰色文字 | 对比度不足，可读性差 | 使用 OKLCH 色彩空间验证对比度 |
| Bounce/弹性动画 | 显得廉价老气 | 使用 cubic-bezier(0.16, 1, 0.3, 1) |

---

## 字体规范

### 推荐字体

**Display（标题）:**
- Geist, Instrument Serif, Sora, Playfair Display

**Body（正文）:**
- DM Sans, Geist, IBM Plex Sans, Source Sans 3

**代码:**
- JetBrains Mono, Fira Code, Source Code Pro

### 字体比例系统

css
:root {
  --text-xs:   clamp(0.694rem, 0.666rem + 0.14vw, 0.8rem);
  --text-sm:   clamp(0.833rem, 0.782rem + 0.25vw, 1rem);
  --text-base: clamp(1rem, 0.923rem + 0.39vw, 1.25rem);
  --text-lg:   clamp(1.2rem, 1.087rem + 0.57vw, 1.563rem);
  --text-xl:   clamp(1.44rem, 1.277rem + 0.81vw, 1.953rem);
  --text-2xl:  clamp(1.728rem, 1.503rem + 1.12vw, 2.441rem);
  --text-3xl:  clamp(2.074rem, 1.767rem + 1.53vw, 3.052rem);
  /* 比例: 1.25 (Major Third) */
}
### 禁止使用

- ❌ Arial、Helvetica（过于通用）
- ❌ Inter（被过度使用，缺乏个性）
- ❌ system-ui（缺乏品牌辨识度）
- ❌ 同一页面超过 2 种字体族

---

## 色彩规范

### 使用 OKLCH（感知均匀色彩空间）

OKLCH 比 HEX 和 RGB 更符合人类视觉感知，便于创建协调的配色。

css
:root {
  /* 有色调的中性色（避免纯灰） */
  --gray-50:  oklch(0.98 0.01 240);
  --gray-100: oklch(0.96 0.01 240);
  --gray-200: oklch(0.92 0.01 240);
  --gray-300: oklch(0.87 0.01 240);
  --gray-400: oklch(0.70 0.01 240);
  --gray-500: oklch(0.55 0.01 240);
  --gray-600: oklch(0.40 0.01 240);
  --gray-700: oklch(0.28 0.01 240);
  --gray-800: oklch(0.18 0.01 240);
  --gray-900: oklch(0.14 0.01 240);

  /* 主色调示例 */
  --blue:       oklch(0.60 0.20 250);
  --blue-hover: oklch(0.50 0.22 250);
  --blue-muted: oklch(0.70 0.10 250);

  /* 功能色 */
  --success: oklch(0.65 0.18 145);
  --warning: oklch(0.75 0.18 85);
  --error:   oklch(0.60 0.22 25);
}
### 暗色模式

css
@media (prefers-color-scheme: dark) {
  :root {
    --bg-primary: #0f0f0f;          /* 不要用纯黑 #000000 */
    --bg-surface: oklch(0.16 0.01 240);
    --bg-elevated: oklch(0.20 0.01 240);
  }
}
### 禁止做法

- ❌ 彩色背景上使用灰色文字（对比度不足）
- ❌ 纯黑/纯灰（始终带一点色调）
- ❌ 未验证的对比度（确保文字与背景 WCAG AA ≥ 4.5:1）

---

## 空间规范

### 基础间距系统（4px/8px 基准）

css
:root {
  --space-1:  4px;
  --space-2:  8px;
  --space-3:  12px;
  --space-4:  16px;
  --space-5:  20px;
  --space-6:  24px;
  --space-8:  32px;
  --space-10: 40px;
  --space-12: 48px;
  --space-16: 64px;
  --space-20: 80px;
  --space-24: 96px;
}
### 内容宽度限制

| 类型 | 最大宽度 |
|------|----------|
| 正文内容 | `max-width: 65ch` |
| 宽容器 | `max-width: 1280px` |
| 全宽媒体 | `max-width: 100%` |

### 布局原则

- 使用 `gap` 替代 `margin`（Flexbox/Grid 布局）
- 元素之间保持一致的间距
- 用留白创造呼吸感，不要让元素挤在一起

### 禁止做法

- ❌ 随意的 padding/margin 值（13px、22px、37px）
- ❌ 元素紧密排列无间距

---

## 动效规范

### Easing 曲线

css
:root {
  /* 快入慢出（默认） */
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);

  /* 慢入慢出（页面过渡） */
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);

  /* 强调效果 */
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
}
### 动画时长

| 类型 | 时长 |
|------|------|
| 微交互（hover、focus） | 100-200ms |
| 状态切换 | 200-300ms |
| 页面过渡 | 300-500ms |
| Loading 骨架屏 | skeleton 优先于 spinner |

### 示例

css
.button {
  transition: all var(--ease-out) 150ms;
}

.modal-enter {
  animation: fadeSlideIn 300ms var(--ease-out);
}

@keyframes fadeSlideIn {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 无障碍：尊重用户偏好 */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
### 禁止做法

- ❌ bounce/elastic easing（廉价感）
- ❌ 超过 600ms 的动画
- ❌ 未尊重 `prefers-reduced-motion`

---

## 交互规范

### Focus 状态（无障碍必需）

css
.button:focus-visible {
  outline: 2px solid var(--blue);
  outline-offset: 2px;
}

/* 不要移除 outline 而不提供替代方案 */
### 悬停状态

css
.button {
  background: var(--gray-100);
  transition: all var(--ease-out) 150ms;
}

.button:hover {
  background: var(--gray-200);
  transform: translateY(-1px);
}
### 点击反馈

- 微妙的缩放或颜色变化
- 避免过于夸张的按压效果
- 移动端考虑 `:active` 状态

### 禁止做法

- ❌ 移除 `outline` 不提供替代 focus 样式
- ❌ 悬停效果过于夸张
- ❌ 无点击反馈

---

## 代码质量标准

### CSS 架构

css
/* 使用 CSS 变量 */
:root {
  /* 颜色 */
  /* 间距 */
  /* 字体 */
  /* 动效 */
}

/* 组件化 */
.card {
  /* 组件变量 */
  --card-bg: var(--bg-surface);
  --card-padding: var(--space-6);

  background: var(--card-bg);
  padding: var(--card-padding);
}

/* 暗色模式覆盖 */
@media (prefers-color-scheme: dark) {
  .card {
    --card-bg: var(--bg-elevated);
  }
}
### 响应式断点

css
/* 移动优先 */
.container {
  width: 100%;
  padding: 0 var(--space-4);
}

@media (min-width: 640px) {
  .container {
    padding: 0 var(--space-6);
  }
}

@media (min-width: 1024px) {
  .container {
    padding: 0 var(--space-8);
  }
}
---

## 设计审查清单

生成或修改 UI 代码后，检查以下要点：

- [ ] 字体不超过 2 种，字重比例协调
- [ ] 色彩使用 OKLCH，带有细微色调
- [ ] 对比度符合 WCAG AA 标准
- [ ] 间距使用 4/8px 基准系统
- [ ] 正文宽度不超过 65ch
- [ ] 动画使用正确的 easing 曲线
- [ ] 动画时长在合理范围内
- [ ] 尊重 `prefers-reduced-motion`
- [ ] Focus 状态清晰可见
- [ ] 无卡片嵌套卡片等层次问题
- [ ] 无 Inter + 紫色渐变等默认反模式