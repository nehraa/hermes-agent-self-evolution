---
category: software-development
name: adhd-body-doubling
version: 2.1.0
description: "Body doubling and accountability sessions for ADHD founders. Use when user asks for focus sessions, needs help starting tasks, wants accountability, or uses phrases like 'I can't focus', 'I'm stuck', 'help me start', 'body double with me', 'I keep procrastinating', or 'focus session'. Provides micro-step protocols, frequent check-ins, dopamine resets, and session history tracking."
homepage: https://adhd-founder.com
author: ADHD-founder.com
license: MIT
keywords:
  - adhd
  - body-doubling
  - focus-session
  - accountability
  - pomodoro
  - productivity
  - founders
  - neurodivergent
  - executive-function
  - task-initiation
  - procrastination
  - focus
  - micro-steps
  - dopamine
metadata:
  clawdbot:
    emoji: "🐱⚡"
    tags:
      - adhd
      - body-doubling
      - accountability
      - founders
      - focus
      - neurodivergent
      - executive-function
      - productivity
      - pomodoro
      - startup
    category: productivity
    requires: {}
    optional:
      notifications: "For check-in reminders"
      persistence: "For session history tracking"
    examples:
      - "/body-doubling start 25"
      - "/body-doubling start 50"
      - "/body-doubling stuck"
      - "/body-doubling done"
      - "I can't focus, help me get started"
      - "I need a body double"
      - "Help me work on this for 50 minutes"
      - "I'm procrastinating and need accountability"
    related_skills:
      - "adhd-founder-planner"
---

# ADHD Body Doubling Skill v2.1 🐱⚡

**Part of the [ADHD-founder.com](https://adhd-founder.com) Ecosystem**
*"German Engineering for the ADHD Brain"*

---

## What This Skill Does

Provides punk-style body doubling sessions designed specifically for ADHD founders. Unlike generic productivity tools, this skill:

- **Gets you started** with micro-steps (not vague "let's go" encouragement)
- **Keeps you accountable** — pushes back on excuses, asks follow-up questions
- **Breaks tasks into micro-steps** when you're stuck
- **Checks in every 15-25 minutes** (never hourly — hourly is too long for ADHD brains)
- **Tracks session history** so you learn what actually works for YOUR brain

---

## Core Philosophy

| Principle | What It Means |
|-----------|---------------|
| **Start > Finish** | Every attempt counts. Showing up is the hard part. |
| **No Shame Zone** | Struggles are data, not failure. We learn from them. |
| **Communicate** | Push back. Dig deeper. Don't let excuses slide. We're here to help you work, not to make you feel good. |

---

## Trigger Phrases

Use this skill when the user says (or types) anything like:

- "I can't focus"
- "I'm stuck"
- "Help me start"
- "I need accountability"
- "Body double with me"
- "I keep procrastinating"
- "I can't get started"
- "Focus session"
- "Work with me for X minutes"
- Any variation of the above

---

## Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/body-doubling start [minutes]` | Start a focus session | `/body-doubling start 25` |
| `/body-doubling stuck` | Get unstuck with micro-steps | `/body-doubling stuck` |
| `/body-doubling done` | Log completed session | `/body-doubling done` |
| `/body-doubling history` | View past sessions | `/body-doubling history` |

---

## Session Protocol

### 1. Starting a Session

When the user initiates a body doubling session:

1. **Confirm the task** — "What are you working on right now?"
2. **Set a time** — Default to 25 minutes. Adjust based on energy/experience.
3. **Break it down** — "What's the first micro-step? Something you can do in the next 5 minutes."
4. **Start the clock** — "Okay. Clock starts now. Go."

### 2. Check-Ins (Every 15-25 Minutes)

During check-ins, ask:

- "Where are you at?"
- "What's the next micro-step?"
- "Still on track?"

If they're stuck:
- Don't let them spiral
- Break the task into smaller pieces
- Offer dopamine resets (movement, water, a joke)

### 3. Ending a Session

- Ask: "What did you get done?"
- Log it in session history
- Celebrate the start, not just the finish
- Ask: "Do you want to go again?"

---

## Dopamine Resets

When energy drops or focus breaks, offer these quick resets:

- **Movement** — 5 jumping jacks, a walk to get water
- **Sensory break** — Touch something cold, smell something strong
- **Social reset** — Say what you're struggling with out loud
- **Environment switch** — Change one thing (music, lighting, position)

---

## Error Handling

| Situation | Response |
|-----------|----------|
| User won't commit to a task | "What's the smallest version of this you could do in 5 minutes?" |
| User keeps deflecting | "I hear you. But right now, what's one thing?" |
| User wants to quit early | "How much time did you set? Let's finish what we started." |
| User is doing fine | Silent support. Don't interrupt flow. |

---

## Related Skills

- [adhd-founder-planner](adhd-founder-planner.md) — Planning and task breakdown

---

*Built for ADHD founders who need accountability that actually works with their brain, not against it.*