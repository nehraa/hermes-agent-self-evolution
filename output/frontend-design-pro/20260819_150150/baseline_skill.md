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

## 常见反模式（主动避免）

LLM 默认输出容易陷入这些陷阱：

| 反模式 | 问题 | 解决方案 |
|--------|------|----------|
| Inter + 紫色渐变 | 过度使用的默认值 | 选择个性字体 + 战略用色 |
| 卡片嵌套卡片 | 层次混乱 | 单一视觉层级原则 |
| 彩色背景 + 灰色文字 | 对比度不足 | OKLCH 色彩空间 |
| Bounce/弹性动画 | 显得廉价老气 | cubic-bezier(0.16, 1, 0.3, 1) |

---

## 设计规范

### 字体

**选用有个性的字体：**

- Display: Geist, Instrument Serif, Sora
- Body: DM Sans, Geist, IBM Plex Sans
- 代码: JetBrains Mono, Fira Code

**字体比例系统：**

css
:root {
  --text-xs: clamp(0.694rem, 0.666rem + 0.14vw, 0.8rem);
  --text-sm: clamp(0.833rem, 0.782rem + 0.25vw, 1rem);
  --text-base: clamp(1rem, 0.923rem + 0.39vw, 1.25rem);
  --text-lg: clamp(1.2rem, 1.087rem + 0.57vw, 1.563rem);
  --text-xl: clamp(1.44rem, 1.277rem + 0.81vw, 1.953rem);
  /* 比例 1.25 */
}
**禁止：**

- Arial、Inter（过于通用）
- system-ui（缺乏个性）
- 同一页面超过 2 种字体族

---

### 色彩

**使用 OKLCH（感知均匀）：**

css
:root {
  /* 有色调的中性色 */
  --gray-100: oklch(0.96 0.01 240);
  --gray-900: oklch(0.14 0.01 240);
  
  /* 主色调 */
  --blue: oklch(0.6 0.2 250);
  --blue-hover: oklch(0.5 0.22 250);
}
**暗色模式：**

css
:root {
  --bg-primary: #0f0f0f;    /* 不是 #000000 */
  --bg-surface: oklch(0.16 0.01 240);
}
**禁止：**

- 彩色背景上用灰色文字（对比度不足）
- 纯黑/纯灰（始终带一点色调）
- 未验证的对比度（文字与背景 WCAG AA 4.5:1）

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
  --space-12: 48px;
  --space-16: 64px;
}
**内容宽度限制：**

- 正文：max-width: 65ch
- 宽容器：max-width: 1280px
- 使用 gap 替代 margin（Flexbox/Grid）

**禁止：**

- 随意的 padding 值（13px、22px）
- 元素挤在一起（用留白创造呼吸感）

---

### 动效

**Easing 曲线：**

css
:root {
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);  /* 快入慢出 */
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);
}
**时长：**

- 微交互：100-200ms
- 页面过渡：300-500ms
- Loading：skeleton 优先于 spinner

css
.button {
  transition: all var(--ease-out) 150ms;
}

@media (prefers-reduced-motion: reduce) {
  .button {
    transition: none;
  }
}
**禁止：**

- bounce/elastic easing
- 超过 600ms 的动画
- 未尊重 prefers-reduced-motion

---

### 交互

**Focus 状态：**

css
.button:focus-visible {
  outline: 2px solid var(--blue);
  outline-offset: 2px;
}
**错误提示：**

js
// ❌ 差
"输入有误"

// ✅ 好
"邮箱格式不对，请检查（例如：user@example.com）"
**禁用状态：**

jsx
<Button disabled onClick={handleDelete}>
  删除
</Button>
// 需要同时提供 tooltip 或额外说明禁用原因
---

### UX 文案

**按钮文字：**

- ✅ "保存更改" / "删除文章" / "开始使用"
- ❌ "确认" / "提交" / "OK"

**空状态：**

jsx
<EmptyState
  title="还没有项目"
  description="创建你的第一个项目，开启高效协作之旅"
  action={<Button>创建项目</Button>}
/>
**禁止：**

- "请稍候..." → 说明具体在等什么
- 技术术语 → 用用户能理解的语言

---

## 命令

在 UI/前端相关对话中使用：

| 命令 | 功能 | 使用场景 |
|------|------|----------|
| `/audit [组件]` | 检查无障碍、性能、响应式 | 任何 UI 输出后 |
| `/critique [组件]` | UX 评审：信息层次、清晰度 | 设计方向不确定时 |
| `/polish [组件]` | 发布前最终打磨 | 准备交付时 |
| `/distill [组件]` | 化繁为简，去除冗余 | 界面过于复杂时 |
| `/colorize [组件]` | 引入战略性色彩 | 界面过于单调/灰暗 |
| `/animate [组件]` | 添加有意义的动效 | 需要交互动效时 |
| `/bolder [组件]` | 让平淡设计更有力 | 视觉冲击力不足 |
| `/quieter [组件]` | 让张扬设计沉稳 | 过于花哨时 |
| `/delight [组件]` | 添加精致微交互 | 提升体验惊喜感 |
| `/normalize [组件]` | 对齐设计系统 | 需要统一风格时 |
| `/harden [组件]` | 完善错误处理/边界/I18n | 准备生产环境 |

---

## 执行规则

### 生成代码时

1. **自动应用规范**：主动使用上述设计规则
2. **反模式提醒**：发现问题时立即指出（简短）
3. **落地到代码**：设计建议 → 具体 CSS/JS，不停留在概念

### 收到命令时

**`/audit`**：
- 输出 3-5 个具体问题（带组件名/行号）
- 格式：`问题描述 → 建议方案`

**`/polish`**：
- 输出修改后完整代码
- 用注释说明每个改动

**其他命令**：
- 先说明改动方向
- 再输出改后代码

---

## 示例

**输入：** 「帮我写一个登录表单」

**输出特征（自动应用规范）：**

jsx
function LoginForm() {
  return (
    <form className="login-form">
      <h1 className="login-form__title">登录账户</h1>
      
      <div className="login-form__field">
        <label htmlFor="email">邮箱地址</label>
        <input
          id="email"
          type="email"
          autoComplete="email"
          placeholder="you@example.com"
          className="login-form__input"
        />
      </div>
      
      <div className="login-form__field">
        <label htmlFor="password">密码</label>
        <input
          id="password"
          type="password"
          autoComplete="current-password"
          className="login-form__input"
        />
      </div>
      
      <button type="submit" className="login-form__submit">
        登录
      </button>
    </form>
  );
}
**规范应用点：**

| 规范 | 实现 |
|------|------|
| 字体 | 使用 Geist/DM Sans |
| Focus 状态 | 2px solid oklch(0.6 0.2 250) outline |
| 按钮文案 | "登录"（动词）而非"确认" |
| 空间 | 8px 倍数 spacing |
| 输入标签 | 显式 label（无障碍） |