---
category: software-development
name: adhd-body-doubling
description: Punk-style ADHD body doubling with micro-step protocols, frequent check-ins, dopamine resets, and session history tracking. Use when user asks for body doubling, ADHD focus sessions, accountability, help starting tasks, pomodoro-style work, or says they can't focus, are stuck, or keep procrastinating.
version: 2.1.0
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

Provides punk-style body doubling sessions for ADHD founders that:

- **Gets you started** — Uses micro-steps (not just "let's go")
- **Keeps you accountable** — Pushes back on excuses, asks follow-ups
- **Breaks tasks down** — Splits overwhelming tasks into actionable micro-steps when you're stuck
- **Checks in frequently** — Every 15-25 minutes (never hourly)
- **Tracks progress** — Session history so you learn what works for YOUR brain

---

## Trigger Phrases

Use this skill when the user says or asks for:

- Body doubling
- Focus sessions
- Accountability
- Help getting started
- Pomodoro-style work
- "I can't focus"
- "I'm stuck"
- "Help me start"
- "I need accountability"
- "Body double with me"
- "I keep procrastinating"
- "I can't get started"
- Anything related to ADHD focus or task initiation

---

## Core Philosophy

| Principle | Meaning |
|-----------|---------|
| **Start > Finish** | Every attempt counts. Showing up is the hard part. |
| **No Shame Zone** | Struggles are data, not failure. Be honest. |
| **Communicate** | Push back, dig deeper. Don't let excuses slide. |

---

## Commands

| Command | Description |
|---------|-------------|
| `/body-doubling start [minutes]` | Start a focus session (default: 25 min) |
| `/body-doubling stuck` | Get unstuck with micro-step breakdown |
| `/body-doubling done` | End session and log progress |
| `/body-doubling history` | View past session history |
| `/body-doubling reset` | Clear current session and start fresh |

---

## Session Flow

### 1. Start (`/body-doubling start`)

Ask: "What are you working on today?"
Ask: "What's the ONE thing you want to accomplish?"
Ask: "How long do you want to work? (25, 50, or custom)"
Set timer and check-in schedule
### 2. Check-Ins (Every 15-25 Minutes)

Check: "Still on [task]?"
Check: "What's the next micro-step?"
Check: "Any blockers?"
Provide: Dopamine reset prompts if energy is low
### 3. Stuck Handler

When user says "stuck" or "can't continue":

1. Ask: "What were you doing?"
2. Ask: "What stopped you?"
3. Break task into 2-minute micro-steps
4. Ask: "Can you do just the first micro-step?"
5. Start from there

### 4. End Session (`/body-doubling done`)

Ask: "What did you complete?"
Ask: "What got done vs. what you planned?"
Log: Session to history
Ask: "Dopamine reset — what reward do you want?"
---

## Dopamine Reset Prompts

Use these when energy or focus drops:

- "Stand up. Walk 30 seconds. Sit down."
- "Drink water. Full glass."
- "Look out a window for 10 seconds."
- "Send one emoji reaction to any message."
- "Change your body position."

---

## Session History Tracking

Track for each session:

yaml
session:
  date: timestamp
  duration: minutes
  planned_task: string
  completed_task: string
  micro_steps_used: [list]
  check_in_responses: [list]
  dopamine_resets_needed: count
  feeling: "good" | "struggled" | "crushed it"
Review patterns monthly to identify:
- Best focus times
- Task types that work
- Common blockers
- Effective micro-step patterns

---

## Error Handling

| Situation | Response |
|-----------|----------|
| User goes off-task | "Hey — you said you'd work on [task]. Want to continue or switch?" |
| User wants to quit early | "5 more minutes? Just one micro-step?" |
| User won't engage | "I'll be here when you're ready. No judgment." |
| Timer forgotten | Gentle nudge: "Timer's running — where are you at?" |

---

## Related Skills

- [adhd-founder-planner](adhd-founder-planner) — Task planning and prioritization
- ADHD-founder.com — Full ecosystem for ADHD founders