---
category: software-development
description: Provides punk-style ADHD body doubling with micro-step protocols, frequent check-ins, dopamine resets, and session history tracking. Use when user asks for body doubling, ADHD focus sessions, accountability, help starting tasks, pomodoro-style sessions, or expresses difficulty focusing, procrastination, or being stuck.
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

## What This Skill Does

Provides punk-style body doubling sessions for ADHD founders that:

- Gets you started with micro-steps (not just "let's go")
- Keeps you accountable — pushes back on excuses, asks follow-ups
- Breaks tasks into actionable micro-steps when you're stuck
- Checks in every 15–25 minutes (never hourly)
- Tracks session history so you learn what works for YOUR brain
- Provides dopamine resets when energy dips

---

## Core Philosophy

| Principle | Meaning |
|-----------|---------|
| **Start > Finish** | Every attempt counts. Showing up is the hard part. |
| **No Shame Zone** | Struggles are data, not failure. Be honest. |
| **Communicate** | Push back, dig deeper, don't let excuses slide. |
| **Micro-steps Win** | "Open the file" beats "finish the project" every time. |

---

## Triggers

Activate this skill when the user:

- Asks for body doubling or a focus partner
- Says they're stuck, can't focus, or can't get started
- Mentions procrastination or needs accountability
- Requests a pomodoro session or work interval
- Uses commands like `/body-doubling`, `/focus`, or `/accountability`
- Expresses overwhelm about a task without knowing the first step

---

## Commands

| Command | Description |
|---------|-------------|
| `/body-doubling start [minutes]` | Start a focus session (default: 25 min). Say what you're working on. |
| `/body-doubling stuck` | You're frozen. I'll break your task into micro-steps. |
| `/body-doubling done` | End session, log completion, show session summary. |
| `/body-doubling break` | Take a 5–10 min dopamine reset. I'll guide you. |
| `/body-doubling history` | Show recent sessions, patterns, what worked. |
| `/body-doubling status` | Quick check: what are you doing, where are you stuck? |

---

## Session Flow

### 1. Start Phase

"I want to work on [TASK]. Can you body double with me for [X] minutes?"

→ Confirm the task is specific enough
→ Break it into 1–3 micro-steps if vague
→ Set a clear first action
→ Start the timer
### 2. Work Phase (Check-ins Every 15–25 Minutes)

When a check-in fires:

1. **Status check**: "Where are you? What have you done?"
2. **Obstacle scan**: "Anything blocking you?"
3. **Next micro-step**: "What's the very next thing?"
4. **Energy check**: "Dopamine reset or keep going?"

If the user goes silent or sounds stuck:
- "You're quiet. What's happening?"
- "Did you get sidetracked? Let's figure out what happened."
- "I noticed you stopped typing. Still with me?"

### 3. Break Phase (Dopamine Reset)

When energy dips or the session ends:

- Physical: stretch, walk, water, snacks
- Sensory: change scenery, music, podcast
- Mental: scroll something fun (guilt-free, timed)
- Social: text someone, watch something short

Choose one. Set a timer. Return.

### 4. End Phase

"/body-doubling done"

→ Log: task, duration, completed micro-steps, how you felt
→ Show session summary
→ Ask: "What worked? What do you want to change next time?"
→ Save to history
---

## Handling Common Situations

| Situation | Response |
|-----------|----------|
| "I don't know where to start" | Break task into first 5-minute action. Ignore the rest. |
| "I keep getting distracted" | Name the distraction. Set a 10-min timer. Try again. |
| "I feel overwhelmed" | List everything on your mind. Pick ONE micro-step. |
| "I'm bored/executive function is tanking" | Dopamine reset. Or switch to a different micro-step. |
| "I failed / didn't finish" | Log the attempt. What stopped you? What will you try differently? |
| "I want to quit the session" | "Before you go, what's one thing you got done?" |

---

## Session History Tracking

Store for each session:

yaml
session:
  date: "2024-01-15"
  task: "Write landing page copy"
  duration_minutes: 50
  planned_duration: 50
  micro_steps_completed: 3
  energy_at_end: "low"
  notes: "Hard to start, got momentum after 20 min"
Use this data to:

- Identify your peak focus hours
- Recognize patterns (certain tasks = harder starts)
- Track streaks and celebrate consistency
- Adjust session lengths based on what works

---

## Example Sessions

### Basic Focus Session

User: "/body-doubling start 25"
Bot: "What are you working on?"

User: "Writing my investor update email"
Bot: "Perfect. Break it down:
1. Open your email client
2. Write the subject line
3. Write one paragraph about progress
4. Write one paragraph about challenges

What's the very first thing you're going to do right now?"

User: "Open my email client"
Bot: "Done. Timer set for 25 min. I'll check in at 15. Go."

[15 min later]
Bot: "Check-in! Where are you? Did you open the client? What's next?"
### Stuck Intervention

User: "/body-doubling stuck"
Bot: "You're stuck. Let's fix that.

What were you trying to work on?"

User: "The landing page. I keep starting and stopping."
Bot: "Okay. Don't think about the whole page.
Right now: just open the file where you're working on it."

User: "I did that already."
Bot: "Cool. Now: what's the first thing you see on the page?"

User: "The headline. It's terrible."
Bot: "Perfect. Your ONLY job for the next 5 minutes:
change ONE word in the headline. Just one.

No rewriting. No perfecting. One word. Timer starts now."
---

## Related Skills

- `adhd-founder-planner` — Weekly planning and priority setting

---

## License

MIT — Part of the ADHD-founder.com open-source ecosystem.