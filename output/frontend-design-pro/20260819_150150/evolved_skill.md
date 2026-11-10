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

让 AI 生成的前端代码摆脱「千篇一律的模板感」。

灵感来源：[impeccable](https://github.com/pbakaus/impeccable)

---

## 设计审查命令

| 命令 | 用途 |
|------|------|
| `/audit` | 全面审查设计质量，输出改进清单 |
| `/polish` | 针对已有代码进行设计优化 |
| `/critique` | 指出具体设计问题与解决方案 |
| `/colorize` | 提供配色方案或改进建议 |
| `/animate` | 优化动画效果 |
| `/bolder` | 增强视觉层次和对比度 |
| `/quieter` | 降低视觉噪音，简化界面 |
| `/distill` | 精简组件，移除冗余元素 |

---

## 常见反模式（主动避免）

LLM 默认输出容易陷入这些陷阱，审查时优先检查：

| 反模式 | 问题 | 解决方案 |
|--------|------|----------|
| Inter + 紫色渐变 | 过度使用的默认值 | 选择个性字体 + 战略用色 |
| 卡片嵌套卡片 | 层次混乱 | 单一视觉层级原则 |
| 彩色背景 + 灰色文字 | 对比度不足 | OKLCH 色彩空间 |
| Bounce/弹性动画 | 显得廉价老气 | `cubic-bezier(0.16, 1, 0.3, 1)` |
| 纯黑背景 `#000` | 过度刺激 | `oklch(0.14 0.01 240)` |

---

## 字体规范

### 推荐字体

**Display / 标题字体：**
- Geist, Instrument Serif, Sora, Newsreader, Fraunces

**正文字体：**
- DM Sans, Geist, IBM Plex Sans, Source Sans 3

**代码字体：**
- JetBrains Mono, Fira Code, Berkeley Mono

### 字体比例系统

css
:root {
  --text-xs:   clamp(0.694rem, 0.666rem + 0.14vw, 0.8rem);
  --text-sm:   clamp(0.833rem, 0.782rem + 0.25vw, 1rem);
  --text-base: clamp(1rem,   0.923rem + 0.39vw, 1.25rem);
  --text-lg:   clamp(1.2rem, 1.087rem + 0.57vw, 1.563rem);
  --text-xl:   clamp(1.44rem, 1.277rem + 0.81vw, 1.953rem);
  --text-2xl:  clamp(1.728rem, 1.5rem + 1.14vw, 2.441rem);
  /* 比例系数 1.25 */
}
### 禁止使用

- **Arial、Inter** — 过于通用，缺乏个性
- **system-ui** — 依赖系统默认值，无法控制
- **同一页面超过 2 种字体族** — 保持视觉统一

---

## 色彩规范

### OKLCH 色彩空间

OKLCH 是感知均匀的色彩空间，比 HSL 更适合用于 UI 设计。

css
:root {
  /* 中性色 — 始终带色调 */
  --gray-50:  oklch(0.98 0.01 240);
  --gray-100: oklch(0.96 0.01 240);
  --gray-200: oklch(0.92 0.01 240);
  --gray-300: oklch(0.87 0.01 240);
  --gray-400: oklch(0.70 0.01 240);
  --gray-500: oklch(0.55 0.01 240);
  --gray-600: oklch(0.40 0.01 240);
  --gray-700: oklch(0.30 0.01 240);
  --gray-800: oklch(0.20 0.01 240);
  --gray-900: oklch(0.14 0.01 240);

  /* 主色调示例 */
  --blue:       oklch(0.60 0.20 250);
  --blue-hover: oklch(0.50 0.22 250);

  /* 功能色 */
  --success: oklch(0.65 0.18 145);
  --warning: oklch(0.75 0.18 85);
  --error:   oklch(0.60 0.22 25);
}
### 暗色模式

css
@media (prefers-color-scheme: dark) {
  :root {
    --bg-primary: #0f0f0f;           /* 不是纯黑 #000 */
    --bg-surface: oklch(0.16 0.01 240);
    --text-primary: oklch(0.95 0.01 240);
    --text-secondary: oklch(0.70 0.01 240);
  }
}
### 禁止事项

- ❌ 彩色背景上使用灰色文字
- ❌ 纯黑 `#000000` 或纯灰 `#808080`
- ❌ 未验证对比度（文字与背景需达到 WCAG AA 4.5:1）

---

## 空间规范

### 4px/8px 基础系统

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

| 场景 | 最大宽度 |
|------|----------|
| 正文内容 | `max-width: 65ch` |
| 宽容器 | `max-width: 1280px` |
| 全宽图片/视频 | `100%` |

### 布局原则

- 使用 `gap` 替代 `margin` 控制间距（Flexbox/Grid）
- 组件内部使用 padding，组件之间使用 gap
- 用留白创造呼吸感，避免元素拥挤

### 禁止事项

- ❌ 随意的 padding 值（13px、22px 等）
- ❌ 元素紧密排列无间距

---

## 动效规范

### Easing 曲线

css
:root {
  /* 标准缓出 — 快入慢出，适合大多数场景 */
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);

  /* 缓入缓出 — 适合页面过渡 */
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);

  /* 特殊场景 */
  --ease-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);
}
### 时长规范

| 类型 | 时长 |
|------|------|
| 微交互（hover、focus） | 100-200ms |
| 组件状态切换 | 200-300ms |
| 页面过渡 | 300-500ms |

### 组件示例

css
.button {
  transition: all var(--ease-out) 150ms;
}

/* Loading 状态优先使用 skeleton */
.skeleton {
  background: linear-gradient(
    90deg,
    var(--gray-100) 25%,
    var(--gray-200) 50%,
    var(--gray-100) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* 无障碍支持 */
@media (prefers-reduced-motion: reduce) {
  .button,
  .skeleton {
    transition: none;
    animation: none;
  }
}
### 禁止事项

- ❌ bounce/elastic easing（除非刻意营造俏皮感）
- ❌ 超过 600ms 的动画
- ❌ 未尊重 `prefers-reduced-motion`

---

## 交互规范

### Focus 状态

始终为可交互元素定义 focus-visible 样式：

css
.button:focus-visible {
  outline: 2px solid var(--blue);
  outline-offset: 2px;
  border-radius: 4px;
}

/* 不使用 outline: none 移除默认边框 */
### 点击区域

- 最小点击区域：`44 × 44px`（移动端）
- 可使用 `padding` 扩展实际点击区域

### 悬停状态

css
.button:hover {
  background: var(--blue-hover);
  transform: translateY(-1px);
}

.button:active {
  transform: translateY(0);
}
---

## 设计审查清单

执行 `/audit` 时检查以下项目：

### 字体
- [ ] 使用推荐字体而非 Inter/Arial
- [ ] 字体不超过 2 种字体族
- [ ] 使用 clamp() 实现响应式字体

### 色彩
- [ ] 使用 OKLCH 色彩空间
- [ ] 暗色模式不使用纯黑
- [ ] 所有文字对比度达到 WCAG AA

### 空间
- [ ] 使用 4/8px 基础网格
- [ ] 内容宽度有明确限制
- [ ] 元素间有适当呼吸空间

### 动效
- [ ] 使用标准 easing 曲线
- [ ] 微交互时长 100-200ms
- [ ] 支持 `prefers-reduced-motion`

### 交互
- [ ] 所有可交互元素有 focus 状态
- [ ] 点击区域足够大
- [ ] hover/active 状态明确

---

## 触发词

当用户输入以下内容时，激活此 skill：

**命令形式：**
- `/audit`、`/polish`、`/critique`
- `/colorize`、`/animate`、`/bolder`
- `/quieter`、`/distill`

**自然语言：**
- 审查 UI 设计、优化界面、前端设计建议
- 让设计更好看、检查设计质量
- 哪里可以改进、有什么设计问题