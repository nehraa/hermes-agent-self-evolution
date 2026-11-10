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

让 AI 生成的前端代码摆脱「千篇一律的模板感」，输出专业级 UI。

灵感来源：[impeccable](https://github.com/pbakaus/impeccable)

---

## 触发命令

当用户输入以下内容时，激活此 skill：

| 命令 | 用途 | 示例 |
|------|------|------|
| `/audit` | 设计质量审查 | 检查整体设计规范符合度 |
| `/polish` | 打磨细节 | 微调间距、圆角、阴影 |
| `/critique` | 深度批评 | 指出具体设计问题及解决方案 |
| `/colorize` | 色彩诊断 | 修复对比度、调整配色 |
| `/animate` | 动效审查 | 优化 easing、时序 |
| `/bolder` | 增强视觉层次 | 加粗标题、强化对比 |
| `/quieter` | 降低视觉噪音 | 简化装饰、减少干扰 |
| `/distill` | 提炼精简 | 去除冗余元素 |

**自然语言触发：**

- 「审查 UI 设计」
- 「优化界面让它更好看」
- 「检查设计质量」
- 「前端设计建议」
- 「让这个按钮看起来更专业」

---

## 常见反模式（主动避免）

LLM 默认输出容易陷入这些陷阱：

| 反模式 | 问题 | 解决方案 |
|--------|------|----------|
| Inter + 紫色渐变 | 过度使用的默认值 | 选择个性字体 + 战略用色 |
| 卡片嵌套卡片 | 层次混乱 | 单一视觉层级原则 |
| 彩色背景 + 灰色文字 | 对比度不足 | 使用 OKLCH 色彩空间验证 |
| Bounce/弹性动画 | 显得廉价老气 | cubic-bezier(0.16, 1, 0.3, 1) |

---

## 设计规范

### 字体

**选用有个性的字体：**

| 用途 | 推荐字体 |
|------|----------|
| Display/标题 | Geist, Instrument Serif, Sora |
| Body/正文 | DM Sans, Geist, IBM Plex Sans |
| 代码 | JetBrains Mono, Fira Code |

**字体比例系统（比例 1.25）：**

css
:root {
  --text-xs: clamp(0.694rem, 0.666rem + 0.14vw, 0.8rem);
  --text-sm: clamp(0.833rem, 0.782rem + 0.25vw, 1rem);
  --text-base: clamp(1rem, 0.923rem + 0.39vw, 1.25rem);
  --text-lg: clamp(1.2rem, 1.087rem + 0.57vw, 1.563rem);
  --text-xl: clamp(1.44rem, 1.277rem + 0.81vw, 1.953rem);
  --text-2xl: clamp(1.728rem, 1.496rem + 1.16vw, 2.441rem);
  --text-3xl: clamp(2.074rem, 1.73rem + 1.72vw, 3.052rem);
}
**禁止使用：**

- ❌ Arial、Inter（过于通用，缺乏个性）
- ❌ system-ui（在不同系统表现不一致）
- ❌ 同一页面超过 2 种字体族

---

### 色彩

**使用 OKLCH（感知均匀的色彩空间）：**

css
:root {
  /* 有色调的中性色（避免纯灰） */
  --gray-50: oklch(0.98 0.01 240);
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
  --blue: oklch(0.60 0.20 250);
  --blue-hover: oklch(0.50 0.22 250);
  --blue-muted: oklch(0.70 0.10 250);
}
**暗色模式：**

css
:root {
  --bg-primary: #0f0f0f;    /* 避免纯黑 #000000 */
  --bg-surface: oklch(0.16 0.01 240);
  --bg-elevated: oklch(0.20 0.01 240);
}
**必须验证：**

- 文字与背景对比度 ≥ 4.5:1（WCAG AA）
- 使用 [contrastchecker.com](https://contrastchecker.com) 或浏览器 DevTools 验证

**禁止：**

- ❌ 彩色背景上用灰色文字
- ❌ 纯黑/纯灰（始终带一点色调）
- ❌ 未验证的对比度

---

### 空间

**4px/8px 基础系统：**

css
:root {
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;
  --space-12: 48px;
  --space-16: 64px;
  --space-20: 80px;
}
**内容宽度限制：**

| 类型 | 最大宽度 |
|------|----------|
| 正文/文章 | max-width: 65ch |
| 宽容器 | max-width: 1280px |
| 全宽图片 | width: 100% |

**布局原则：**

- 使用 `gap` 替代 `margin`（Flexbox/Grid）
- 移动端：`gap: 16px`
- 桌面端：`gap: 24px` 或 `gap: 32px`

**禁止：**

- ❌ 随意的 padding 值（13px、22px、37px）
- ❌ 元素挤在一起（用留白创造呼吸感）

---

### 动效

**Easing 曲线：**

css
:root {
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);    /* 快入慢出，主推动画 */
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1); /* 渐入渐出 */
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1); /* 弹性效果，仅必要时使用 */
}
**时长规范：**

| 类型 | 时长 | 示例 |
|------|------|------|
| 微交互 | 100-200ms | 按钮 hover、toggle |
| 页面过渡 | 300-500ms | 路由切换、模态框 |
| Loading | skeleton > spinner | 内容加载占位 |

**实现示例：**

css
.button {
  transition: all var(--ease-out) 150ms;
}

/* 尊重用户偏好 */
@media (prefers-reduced-motion: reduce) {
  .button {
    transition: none;
  }
}
**禁止：**

- ❌ bounce/elastic easing（除非刻意表现幼稚感）
- ❌ 超过 600ms 的动画
- ❌ 未尊重 `prefers-reduced-motion`

---

### 交互

**Focus 状态（无障碍必需）：**

css
.button:focus-visible {
  outline: 2px solid var(--blue);
  outline-offset: 2px;
}

/* 不要移除 outline 而不提供替代方案 */
**Hover 状态：**

css
.button {
  background: var(--gray-100);
  transition: background var(--ease-out) 150ms;
}

.button:hover {
  background: var(--gray-200);
}
**按钮层级：**

| 层级 | 样式 | 用途 |
|------|------|------|
| Primary | 实心背景，醒目颜色 | 主要操作 |
| Secondary | 边框或浅背景 | 次要操作 |
| Ghost | 无背景，仅文字 | 低优先级操作 |
| Destructive | 红色系 | 删除等危险操作 |

---

## 命令执行指南

### `/audit`

全面审查设计实现：

1. 检查字体选择是否符合规范
2. 验证色彩对比度（WCAG AA）
3. 检查空间系统一致性
4. 评估动效是否流畅
5. 检查交互状态是否完整

输出格式：

## Audit 报告

### ✅ 通过项
- 字体选择符合规范
- 对比度达标

### ⚠️ 需改进
- 按钮缺少 focus-visible
- 间距不统一

### ❌ 严重问题
- 动画超过 600ms
### `/polish`

细节打磨，提升精致度：

1. 统一间距值
2. 调整圆角大小
3. 优化阴影层级
4. 微调动画曲线
5. 修正字体粗细

### `/critique`

深度分析设计决策：

1. 识别反模式
2. 解释问题原因
3. 提供具体解决方案
4. 给出优化前后的代码对比

### `/colorize`

色彩专项优化：

1. 转换为 OKLCH
2. 调整饱和度
3. 确保对比度达标
4. 优化暗色模式配色

### `/animate`

动效专项审查：

1. 检查 easing 曲线
2. 验证时长合理性
3. 确保尊重 `prefers-reduced-motion`
4. 优化加载状态（优先 skeleton）

### `/bolder`

增强视觉层次：

1. 加粗标题字体
2. 增加主次对比
3. 强化 CTA 按钮
4. 增加区块对比

### `/quieter`

降低视觉噪音：

1. 移除多余装饰
2. 简化颜色使用
3. 减少边框使用
4. 降低次要元素对比度

### `/distill`

提炼精简设计：

1. 删除冗余元素
2. 合并相似组件
3. 简化层级结构
4. 保留核心功能

---

## 快速参考

**最容易出错的 5 个点：**

1. 使用 Inter 字体 → 替换为 DM Sans 或 Geist
2. 纯黑背景 → 使用 oklch(0.14 0.01 240)
3. bounce 动画 → 替换为 cubic-bezier(0.16, 1, 0.3, 1)
4. 随意 padding → 使用 4px/8px 系统
5. 缺少 focus-visible → 必须添加无障碍支持

**优质设计的标志：**

- ✅ 字体不超过 2 种
- ✅ 颜色有色调，不是纯灰
- ✅ 间距使用 4/8 倍数
- ✅ 动画使用 ease-out
- ✅ 所有交互状态完整