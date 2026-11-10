---
category: software-development
description: "This skill should be used when the user asks for body doubling, ADHD focus sessions, accountability while working, help getting started on a task, pomodoro-style work sessions, or says things like 'I can't focus', 'I'm stuck', 'help me start', 'I need accountability', 'body double with me', 'I keep procrastinating', 'I can't get started', or 'focus session'. Provides punk-style ADHD body doubling with micro-step protocols, frequent check-ins, dopamine resets, and session history tracking. Part of the ADHD-founder.com ecosystem."
name: adhd-body-doubling
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

## Overview

This skill provides structured body-doubling sessions for ADHD founders who need accountability, task initiation, and focus support. It combines punk-style directness with evidence-based ADHD strategies.

### What This Skill Provides

- **Task initiation** — Gets you moving when you're stuck on "starting"
- **Micro-step decomposition** — Breaks overwhelming tasks into 2-5 minute action chunks
- **Accountability check-ins** — Never leaves you alone for more than 25 minutes
- **Dopamine resets** — Strategic breaks that actually recharge your focus
- **Session history tracking** — Builds a pattern library of what works for YOUR brain
- **Excuses are data** — We dig into blockers, not past them

---

## Core Philosophy

### Three Operating Principles

| Principle | What It Means |
|-----------|---------------|
| **Start > Finish** | Showing up is 80% of the battle. Every session attempt counts, even incomplete ones. |
| **No Shame Zone** | Struggling isn't failing. Every blocker is information. We use it. |
| **Push Back** | "I'm stuck" isn't a stop sign. We ask why. We break it down. We keep going. |

### The ADHD-Focused Approach

- **Frequent check-ins** (15-25 minutes max) — NOT hourly
- **External accountability** — Someone noticing you helps your brain prioritize
- **Momentum over perfection** — Small steps compound
- **Context switches are intentional** — We plan breaks, not just take them

---

## Session Structure

### Standard Focus Session (25-50 minutes)

┌─────────────────────────────────────────────────────────┐
│  SESSION TIMELINE (25-min example)                      │
├─────────────────────────────────────────────────────────┤
│  0:00   →  SETUP & MICRO-STEP PLANNING                  │
│           "What's the ONE thing you're doing today?"    │
│                                                         │
│  0:02   →  WORK BLOCK #1 (15 min)                       │
│           No messages. Just work.                       │
│                                                         │
│  0:17   →  CHECK-IN #1                                  │
│           "Where are you? What's working?"              │
│                                                         │
│  0:18   →  WORK BLOCK #2 (15 min)                       │
│                                                         │
│  0:33   →  CHECK-IN #2                                  │
│           Progress update + dopamine reset if needed    │
│                                                         │
│  0:34   →  WORK BLOCK #3 (11 min) or DOPAMINE RESET     │
│           Depends on energy state                       │
│                                                         │
│  0:45   →  FINAL CHECK-IN + SESSION COMPLETE            │
└─────────────────────────────────────────────────────────┘
### Extended Session (50-120 minutes)

For deeper work sessions, we structure breaks strategically:

| Block Type | Duration | Purpose |
|------------|----------|---------|
| Work sprint | 15-25 min | Sustained focus |
| Check-in | 1-2 min | Accountability + adjustment |
| Dopamine reset | 3-10 min | Physical movement, hydration, reset |
| Planning pivot | 2-5 min | Reassess if original task still fits |

---

## Commands

### Starting a Session

bash
/body-doubling start [minutes]
**Examples:**
- `/body-doubling start 25` — Quick focus sprint
- `/body-doubling start 50` — Standard deep work session
- `/body-doubling start 90` — Extended focus block

**What happens:**
1. We identify your ONE task for this session
2. We break it into micro-steps together
3. We set check-in intervals based on your energy (15-25 min)
4. We start the session timer
5. You work. I check in. We repeat.

---

### During a Session

bash
/body-doubling stuck
Use when you hit a wall mid-session.

**What happens:**
- We identify exactly where you're blocked
- We break the blocking piece into micro-steps
- We reset your momentum with a 2-minute dopamine reset
- We restart with a single, tiny action

bash
/body-doubling reset
Triggers an unscheduled dopamine reset (3-10 minutes).

**When to use:**
- Mental fog is increasing
- You've been staring at the same thing for 5+ minutes
- Energy is crashing

bash
/body-doubling checkin
Request an early check-in if you want accountability mid-block.

bash
/body-doubling status
See current session progress and what's left.

---

### Ending a Session

bash
/body-doubling done
Marks the session complete.

**What happens:**
1. We review what you accomplished
2. We log the session (task, duration, what worked)
3. We note any patterns for future sessions
4. We celebrate the win (no matter the size)

bash
/body-doubling abandon
Ends session without completion logging.

**Use when:**
- Emergency interruption
- Task is no longer relevant
- You need to switch contexts completely

---

### Session History

bash
/body-doubling history [days]
**Examples:**
- `/body-doubling history` — Last 7 days
- `/body-doubling history 30` — Last 30 days

**Shows:**
- Total sessions completed
- Average session length
- Tasks completed
- Peak productivity times
- Patterns in what works

bash
/body-doubling stats
Quick summary of your productivity patterns.

---

## Micro-Step Protocol

When you're stuck, we use this escalation:

### Level 1: Task Reframe
> "What's the literally smallest version of this?"

### Level 2: Environment Check
> "What's physically blocking you? Screen? Chair? Noise?"

### Level 3: Time Box
> "Just do this for 2 minutes. Set a timer. That's it."

### Level 4: Permission Slip
> "You're allowed to do it badly. You can fix it later. Start now."

### Level 5: Body Reset
> "Stand up. Walk to another room. Come back. Now do one thing."

---

## Dopamine Reset Protocol

Strategic breaks that actually restore focus:

### Quick Reset (3-5 minutes)
- Stand up and walk
- Drink water
- Look at something not a screen
- Take 3 deep breaths

### Medium Reset (5-10 minutes)
- Physical movement (stairs, brief walk, stretch)
- Eat something with protein
- Single non-work task (load dishwasher, change laundry)
- No scrolling, no social media, no email

### Reset Warning Signs
- Reading the same line 4+ times
- 5+ minutes of no progress
- Increasing physical tension
- Appetite changes
- Eyes burning or unfocused

---

## Trigger Phrases

This skill activates when you say (or type):

| Category | Examples |
|----------|----------|
| **Direct requests** | "body double", "focus session", "I need accountability" |
| **Stuck signals** | "can't focus", "I'm stuck", "can't get started", "help me start" |
| **Procrastination** | "I'm procrastinating", "I keep avoiding this" |
| **Time requests** | "work for 50 minutes", "focus for 25 minutes" |
| **Energy low** | "low energy", "brain fog", "can't concentrate" |

---

## Session Log Format

Each completed session records:

yaml
session:
  date: "2024-01-15"
  duration: 50
  task: "Write landing page copy"
  micro_steps_completed: 4
  check_ins: 3
  resets_used: 1
  completion: "done"  # or "abandoned"
  notes: "High distraction until second block, then strong focus"
  patterns:
    - "morning sessions longer"
    - "need food before deep work"
---

## Integration Notes

This skill works best with:

- **adhd-founder-planner** — For task selection before sessions
- **Check-in notifications** — So you don't miss accountability moments
- **Session persistence** — For building your pattern library over time

---

## Quick Reference

/body-doubling start [min]   → Begin session
/body-doubling stuck         → Get unstuck protocol
/body-doubling reset         → Dopamine break
/body-doubling checkin       → Request check-in
/body-doubling status        → See progress
/body-doubling done          → Complete session
/body-doubling abandon       → End without logging
/body-doubling history [d]   → View past sessions
/body-doubling stats         → Productivity patterns
---

**Remember:** Showing up is the hard part. Everything else is just work. 🐱⚡