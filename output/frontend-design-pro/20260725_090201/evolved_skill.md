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

让 AI 生成的前端代码摆脱「千篇一律的模板感」，输出专业级设计。

灵感来源：[impeccable](https://github.com/pbakaus/impeccable)

---

## 核心原则

**先做对，再做美。** 每个设计决策都应有据可依。

| 原则 | 说明 |
|------|------|
| 克制 | 不堆砌装饰，用留白创造层次 |
| 统一 | 字体、色彩、间距系统化 |
| 可达 | WCAG AA 对比度，支持无障碍 |
| 流畅 | 动效服务于交互，不喧宾夺主 |

---

## 常见反模式（主动避免）

LLM 默认输出容易陷入这些陷阱，发现即修复：

| 反模式 | 问题 | 解决方案 |
|--------|------|----------|
| Inter + 紫色渐变 | 过度使用的默认值 | 选择个性字体 + 战略用色 |
| 卡片嵌套卡片 | 层次混乱 | 单一视觉层级原则 |
| 彩色背景 + 灰色文字 | 对比度不足 | OKLCH 色彩空间 + WCAG 验证 |
| Bounce/弹性动画 | 显得廉价老气 | `cubic-bezier(0.16, 1, 0.3, 1)` |
| 随意 padding 值 | 13px、22px 等零散数值 | 基于 4/8px 系统 |
| 纯黑/纯灰背景 | 缺乏温度感 | 始终带一点色调 |

---

## 字体规范

### 推荐字体栈

css
/* Display（标题） */
font-family: 'Geist', 'Instrument Serif', 'Sora', Georgia, serif;

/* Body（正文） */
font-family: 'DM Sans', 'Geist', 'IBM Plex Sans', system-ui, sans-serif;

/* Code（代码） */
font-family: 'JetBrains Mono', 'Fira Code', 'SF Mono', monospace;
### 比例系统（基于 1.25 比例）

css
:root {
  --text-xs:   clamp(0.694rem, 0.666rem + 0.14vw, 0.8rem);   /* 11-13px */
  --text-sm:   clamp(0.833rem, 0.782rem + 0.25vw, 1rem);     /* 13-16px */
  --text-base: clamp(1rem, 0.923rem + 0.39vw, 1.25rem);      /* 16-20px */
  --text-lg:   clamp(1.2rem, 1.087rem + 0.57vw, 1.563rem);   /* 19-25px */
  --text-xl:   clamp(1.44rem, 1.277rem + 0.81vw, 1.953rem);  /* 23-31px */
  --text-2xl:  clamp(1.728rem, 1.504rem + 1.12vw, 2.441rem); /* 28-39px */
  --text-3xl:  clamp(2.074rem, 1.767rem + 1.53vw, 3.052rem); /* 33-49px */
}
### 禁止

- ❌ Arial、Inter（过于通用）
- ❌ `system-ui`（缺乏个性）
- ❌ 同一页面超过 2 种字体族

---

## 色彩规范

### 使用 OKLCH（感知均匀）

OKLCH 比 HSL/HSLA 更符合人眼感知，渐变更自然。

css
:root {
  /* 有色调的中性色（不是纯灰） */
  --gray-50:  oklch(0.98 0 0);
  --gray-100: oklch(0.96 0.01 240);
  --gray-200: oklch(0.92 0.01 240);
  --gray-300: oklch(0.87 0.01 240);
  --gray-500: oklch(0.55 0.02 240);
  --gray-700: oklch(0.37 0.02 240);
  --gray-900: oklch(0.14 0.01 240);

  /* 主色调示例（蓝） */
  --blue-500: oklch(0.6 0.2 250);
  --blue-600: oklch(0.5 0.22 250);

  /* 语义色 */
  --success: oklch(0.65 0.18 145);
  --warning: oklch(0.75 0.18 85);
  --error:   oklch(0.6 0.2 25);
}
### 暗色模式

css
:root {
  --bg-primary: #0f0f0f;                    /* 不是 #000000 */
  --bg-surface: oklch(0.16 0.01 240);
  --bg-elevated: oklch(0.2 0.01 240);
}
### 禁止

- ❌ 彩色背景上用灰色文字
- ❌ 纯黑/纯灰（始终带一点色调）
- ❌ 未验证的对比度（文字与背景 WCAG AA ≥ 4.5:1）

---

## 空间规范

### 4/8px 基础系统

css
:root {
  --space-0:  0;
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

| 场景 | max-width |
|------|-----------|
| 正文 | `65ch` |
| 宽容器 | `1280px` |
| 窄容器（登录页等） | `400px` |

### 布局建议

- 使用 `gap` 替代 `margin`（Flexbox/Grid）
- 元素间至少 `16px` 间距
- 区块间至少 `48px` 间距

### 禁止

- ❌ 随意 padding 值（13px、22px）
- ❌ 元素挤在一起（用留白创造呼吸感）

---

## 动效规范

### Easing 曲线

css
:root {
  --ease-out:     cubic-bezier(0.16, 1, 0.3, 1);   /* 快入慢出（默认） */
  --ease-in-out:  cubic-bezier(0.65, 0, 0.35, 1);   /* 对称过渡 */
  --ease-spring:  cubic-bezier(0.34, 1.56, 0.64, 1); /* 轻微回弹（慎用） */
}
### 时长

| 类型 | 时长 |
|------|------|
| 微交互（hover、active） | 100-200ms |
| 展开/收起 | 200-300ms |
| 页面过渡 | 300-500ms |
| Loading | Skeleton 优先于 Spinner |

### 示例

css
.button {
  transition: all var(--ease-out) 150ms;
}

/* 无障碍：尊重用户偏好 */
@media (prefers-reduced-motion: reduce) {
  .button {
    transition: none;
  }
}
### 禁止

- ❌ bounce/elastic easing（除非刻意追求复古感）
- ❌ 超过 600ms 的动画
- ❌ 未尊重 `prefers-reduced-motion`

---

## 交互规范

### Focus 状态（无障碍必需）

css
.button:focus-visible {
  outline: 2px solid var(--blue-500);
  outline-offset: 2px;
}

/* 不要移除 outline 而不提供替代方案 */
### 悬停状态

css
.button {
  background: var(--blue-500);
}

.button:hover {
  background: var(--blue-600);
  transform: translateY(-1px);  /* 可选：轻微抬升 */
}

.button:active {
  transform: translateY(0);
}
### 禁用状态

css
.button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
---

## 常用命令

### /audit

对当前代码进行全面设计审查，输出问题清单和修复建议。

### /polish

在现有设计基础上进行精细化调整，提升整体质感。

### /critique

指出设计问题，给出改进方向（更直接的反馈）。

### /colorize

提供完整的色彩系统方案（基于 OKLCH）。

### /animate

设计动效方案，包括 easing、时长、触发条件。

### /bolder

增加视觉权重（字体粗细、色调饱和度、对比度）。

### /quieter

降低视觉权重，营造更克制的设计。

### /distill

提炼核心信息，移除冗余装饰。

---

## 检查清单

生成代码后，逐项核对：

- [ ] 字体是否超过 2 种？
- [ ] 颜色是否使用 OKLCH？是否有足够对比度？
- [ ] 间距是否基于 4/8px 系统？
- [ ] 动画是否使用正确的 easing 和时长？
- [ ] focus-visible 是否正确实现？
- [ ] 是否尊重 `prefers-reduced-motion`？