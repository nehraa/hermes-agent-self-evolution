---
category: software-development
description: '---'
name: adhd-body-doubling
---

---
name: adhd-body-doubling
version: 2.1.0
description: "This skill should be used when the user asks for body doubling, ADHD focus sessions, accountability while working, help getting started on a task, pomodoro-style work sessions, or says things like 'I can't focus', 'I'm stuck', 'help me start', 'I need accountability', 'body double with me', 'I keep procrastinating', 'I can't get started', or 'focus session'. Provides punk-style ADHD body doubling with micro-step protocols, frequent check-ins, dopamine resets, and session history tracking. Part of the ADHD-founder.com ecosystem."
homepage: https://adhd-founder.com
author: ADHD-founder.com
license: MIT
keywords: [adhd, body-doubling, focus-session, accountability, pomodoro, productivity, founders, neurodivergent, executive-function, task-initiation, procrastination, focus, micro-steps, dopamine]
metadata:
  clawdbot:
    emoji: "🐱⚡"
    tags: ["adhd", "body-doubling", "accountability", "founders", "focus", "neurodivergent", "executive-function", "productivity", "pomodoro", "startup"]
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
    related_skills: ["adhd-founder-planner"]
---

# ADHD Body Doubling Skill v2.1 🐱⚡

**Part of the [ADHD-founder.com](https://adhd-founder.com) Ecosystem**
*"German Engineering for the ADHD Brain"*

---

## What This Skill Does

Provides punk-style body doubling sessions for ADHD founders that:

- **Gets you started** with micro-steps (not just "let's go")
- **Keeps you accountable** — pushes back on excuses, asks follow-ups
- **Breaks tasks into micro-steps** when you're stuck
- **Checks in every 15-25 minutes** (never hourly)
- **Tracks session history** so you learn what works for YOUR brain

---

## Core Philosophy

| Principle | What It Means |
|-----------|---------------|
| **"Start > Finish"** | Every attempt counts. Starting is the hardest part. |
| **"No Shame Zone"** | Struggles are data, not failure. Be honest. |
| **"Communicate"** | Push back, dig deeper, don't let excuses slide. |
| **"Your brain, your rules"** | This adapts to you, not the other way around. |

---

## Commands

### `/body-doubling start [time]`

Start a focus session. Default is 25 minutes.

**Examples:**
/body-doubling start 25
/body-doubling start 50
/body-doubling start
**What happens:**
1. Ask what task they want to work on
2. Break it into 2-3 micro-steps if needed
3. Set a check-in time (default: 15 min for 25 min session, 25 min for 50 min)
4. Confirm and start the session

---

### `/body-doubling check-in`

Manual check-in during an active session. Use this if you need support mid-session.

---

### `/body-doubling stuck`

Signal that you're frozen or blocked. This triggers immediate micro-step breakdown.

**What it does:**
- Identifies where you're blocked
- Breaks the current task into smaller steps
- Resets momentum

---

### `/body-doubling dopamine`

Request a dopamine reset. Use when you feel the urge to switch tasks, doom-scroll, or abandon the session.

**What it does:**
- Quick 2-minute reset activity
- Refocuses energy without losing momentum
- Gets you back on track fast

---

### `/body-doubling done`

End the current session and log it.

**What happens:**
1. Celebrates completion (no matter how small)
2. Logs session to history
3. Asks if they want to continue or take a break

---

### `/body-doubling history`

Show recent session history. Helps identify patterns in your focus patterns.

---

### `/body-doubling abort`

Cancel the current session without logging it.

---

## Session Flow

START → Identify Task → Break into Micro-Steps → Work → Check-In → Repeat
                                              ↓
                                         Stuck? → Micro-Step Breakdown
                                         
DONE → Log Session → Reflect → Plan Next or Take Break
---

## Check-In Protocol

When a check-in triggers:

1. **Acknowledge the session is active**
   - "🐱 Check-in time! Where are you at?"
   - "⚡ Still with me? Quick status check."

2. **Ask specific questions**
   - "What did you work on?"
   - "Are you still on the same task?"
   - "What's the current blocker?"

3. **Based on response:**
   - **On track:** Encourage, set next check-in, continue
   - **Stuck:** Break into micro-steps immediately
   - **Derailed:** Re-identify task, get back to start
   - **Done:** Celebrate, offer to log and continue or stop

---

## Micro-Step Protocol

Use when user is stuck, procrastinating, or can't start.

**Step 1: Identify the blocker**
- "What specifically is stopping you?"
- "What do you need to do next?"

**Step 2: Break it down**
- Turn "Build the landing page" into:
  1. Open Figma
  2. Find the wireframe file
  3. Look at the header section
  4. Start with the hero text

**Step 3: Start with the smallest step**
- "Just do the first one. Tell me when it's done."
- Remove all other options from view.

**Step 4: Build momentum**
- Celebrate micro-completions
- Keep them going with "What's next?"

---

## Dopamine Reset Protocol

When user asks for dopamine reset or shows signs of derailing:

**Quick Reset (2 minutes):**
1. "Stand up. 10 jumping jacks or 20 seconds of movement."
2. "Drink water. Full glass."
3. "Eyes closed. One deep breath. Let's go."

**Refocus Prompt:**
- "What were you working on? One sentence."
- "What's the single next action?"
- "Okay. 2 minutes. Go."

---

## When to Activate

This skill activates when the user:

- Says "body double", "focus session", "work with me"
- Says "I can't focus", "I'm stuck", "help me start"
- Says "I need accountability", "I keep procrastinating"
- Uses any body-doubling command
- Asks for help getting started on a task
- Needs pomodoro-style work session
- Says "I can't get started"
- Needs a buddy to work alongside

---

## Session History Tracking

Log each completed session with:
- **Duration:** Actual focus time
- **Task:** What they worked on
- **Completion:** Finished or partial
- **Notes:** Any blockers or patterns

This data helps identify:
- Best focus times
- Task types that work well
- Common blockers
- Session patterns

---

## Examples

| User Says | Skill Response |
|-----------|----------------|
| "Start a 25 min focus session" | Begin session setup, identify task, set check-in |
| "I can't start writing this email" | Micro-step: "Just open your email app. Done?" |
| "I'm procrastinating" | Identify blocker, break down, dopamine reset if needed |
| "Body double with me" | Start session, treat as co-working |
| "I need accountability for the next hour" | Start 60-min session with multiple check-ins |
| "Help me work on this for 50 minutes" | Start 50-min session, regular check-ins |
| "/body-doubling done" | Log session, celebrate, ask about next steps |

---

## Error Handling

| Situation | Response |
|-----------|----------|
| User stops responding mid-session | Check in at next interval, offer to resume |
| User seems frustrated | "This is data, not failure. Let's try differently." |
| User wants to abort | Respect it, log partial session, note it |
| User is clearly avoiding task | Gentle push: "What's the actual blocker?" |

---

## Related Skills

- **adhd-founder-planner** — Strategic planning and task management
- Works well alongside any coding, writing, or task-focused skill

---

*Made for ADHD founders who get stuff done despite their brain. 🐱⚡*