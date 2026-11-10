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

## 设计反模式（主动避免）

LLM 默认输出容易陷入这些陷阱：

| 反模式 | 问题 | 解决方案 |
|--------|------|----------|
| Inter + 紫色渐变 | 过度使用的默认值 | 选择个性字体 + 战略用色 |
| 卡片嵌套卡片 | 层次混乱 | 单一视觉层级原则 |
| 彩色背景 + 灰色文字 | 对比度不足 | 使用 OKLCH 色彩空间 |
| Bounce/弹性动画 | 显得廉价老气 | `cubic-bezier(0.16, 1, 0.3, 1)` |
| 纯黑/纯灰背景 | 过于生硬 | 始终带一点色调 (oklch) |

---

## 字体系统

### 推荐字体

**Display（标题）**
- Geist, Instrument Serif, Sora, Clash Display, Cabinet Grotesk

**Body（正文）**
- DM Sans, Geist, IBM Plex Sans, Satoshi

**代码**
- JetBrains Mono, Fira Code, Geist Mono

### 禁止使用

- ❌ Inter（过于通用，默认陷阱）
- ❌ Arial（过时无个性）
- ❌ system-ui（缺乏品牌感）
- ❌ 同一页面超过 2 种字体族

### 字体比例（Major Third 1.25）

css
:root {
  --text-xs:   clamp(0.694rem, 0.666rem + 0.14vw, 0.8rem);
  --text-sm:   clamp(0.833rem, 0.782rem + 0.25vw, 1rem);
  --text-base: clamp(1rem, 0.923rem + 0.39vw, 1.25rem);
  --text-lg:   clamp(1.2rem, 1.087rem + 0.57vw, 1.563rem);
  --text-xl:   clamp(1.44rem, 1.277rem + 0.81vw, 1.953rem);
  --text-2xl:  clamp(1.728rem, 1.503rem + 1.12vw, 2.441rem);
  --text-3xl:  clamp(2.074rem, 1.767rem + 1.53vw, 3.052rem);
}
---

## 色彩系统

### 使用 OKLCH（感知均匀）

OKLCH 比 HEX/HSL 更符合人眼感知，渐变更自然。

css
:root {
  /* 中性色（带微色调） */
  --gray-50:  oklch(0.98 0.005 240);
  --gray-100: oklch(0.96 0.01 240);
  --gray-200: oklch(0.92 0.015 240);
  --gray-300: oklch(0.87 0.02 240);
  --gray-400: oklch(0.70 0.02 240);
  --gray-500: oklch(0.55 0.02 240);
  --gray-600: oklch(0.40 0.02 240);
  --gray-700: oklch(0.28 0.02 240);
  --gray-800: oklch(0.18 0.015 240);
  --gray-900: oklch(0.14 0.01 240);

  /* 主色调示例 */
  --blue:      oklch(0.60 0.2 250);
  --blue-hover: oklch(0.55 0.22 250);

  /* 强调色 */
  --accent:    oklch(0.70 0.18 160);
}
### 暗色模式

css
:root {
  --bg-primary: oklch(0.12 0.01 240);  /* 不是纯 #000 */
  --bg-surface: oklch(0.16 0.01 240);
  --bg-elevated: oklch(0.20 0.01 240);
}
### 色彩禁止规则

- ❌ 彩色背景上使用灰色文字（对比度不足）
- ❌ 纯黑 `#000` 或纯灰 `#808080`
- ❌ 未验证的对比度（正文与背景必须满足 WCAG AA 4.5:1）

---

## 空间系统

### 基础间距（4px/8px 网格）

css
:root {
  --space-0: 0;
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;
  --space-12: 48px;
  --space-16: 64px;
  --space-20: 80px;
  --space-24: 96px;
}
### 内容宽度限制

- 正文内容：`max-width: 65ch`
- 宽容器：`max-width: 1280px`
- 侧边栏：`max-width: 320px`

### 布局原则

- 使用 `gap` 替代 `margin`（Flexbox/Grid）
- 用留白创造呼吸感，避免元素挤在一起

### 空间禁止规则

- ❌ 随意的 padding 值（13px、22px 等）
- ❌ 没有足够的留白
- ❌ 元素之间缺乏视觉分隔

---

## 动效系统

### Easing 曲线

css
:root {
  --ease-out:     cubic-bezier(0.16, 1, 0.3, 1);   /* 快入慢出，推荐 */
  --ease-in-out:  cubic-bezier(0.65, 0, 0.35, 1);   /* 平滑过渡 */
  --ease-spring:  cubic-bezier(0.34, 1.56, 0.64, 1); /* 轻微回弹 */
}
### 动画时长

| 类型 | 时长 |
|------|------|
| 微交互（hover, focus） | 100-200ms |
| 页面过渡 | 300-500ms |
| Loading 状态 | Skeleton > Spinner |

### 示例

css
.button {
  transition: 
    background-color var(--ease-out) 150ms,
    transform var(--ease-out) 150ms,
    box-shadow var(--ease-out) 150ms;
}

.button:hover {
  transform: translateY(-1px);
}

/* 无障碍：尊重用户偏好 */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    transition-duration: 0.01ms !important;
    animation-duration: 0.01ms !important;
  }
}
### 动效禁止规则

- ❌ `bounce` / `elastic` easing（廉价感）
- ❌ 动画时长超过 600ms
- ❌ 未处理 `prefers-reduced-motion`
- ❌ Loading 使用 spinner（改用 skeleton）

---

## 交互状态

### Focus 可见性

css
/* 全局 focus 样式 */
:focus-visible {
  outline: 2px solid var(--blue);
  outline-offset: 2px;
}

/* 组件级别 */
.button:focus-visible {
  box-shadow: 0 0 0 3px oklch(0.60 0.2 250 / 0.4);
}
### 组件悬停状态

css
.button {
  background: var(--gray-900);
  color: var(--gray-50);
}

.button:hover {
  background: var(--gray-800);
  transform: translateY(-1px);
}

.button:active {
  transform: translateY(0);
}
---

## 设计审查命令

当用户触发以下命令时，执行对应审查：

### `/audit` - 全面设计审计
检查：字体、色彩对比度、间距、动效、无障碍、组件一致性

### `/polish` - 优化打磨
对现有代码进行设计质量提升，应用本 skill 的规范

### `/critique` - 批判性审视
指出具体设计问题，提供改进建议

### `/colorize` - 色彩优化
检查并优化配色方案，确保对比度和视觉层次

### `/animate` - 动效审查
检查 easing、时长、无障碍处理

### `/bolder` - 增强视觉层级
增加对比度，让层次更分明

### `/quieter` - 降低视觉噪音
简化过度设计的部分

### `/distill` - 提炼精简
去除冗余元素，保留核心信息

---

## 检查清单

生成代码后，逐一核对：

- [ ] 字体是否超过 2 种
- [ ] 颜色是否使用 OKLCH
- [ ] 对比度是否满足 WCAG AA
- [ ] 间距是否为 4px 倍数
- [ ] 动效是否使用正确的 easing
- [ ] 是否尊重 `prefers-reduced-motion`
- [ ] Focus 状态是否可见
- [ ] 是否有足够的留白