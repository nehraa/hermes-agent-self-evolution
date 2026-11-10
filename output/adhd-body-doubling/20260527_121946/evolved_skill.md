---'" which is odd)
- The content is truncated (commands table is incomplete)
- The name and description need to be preserved but improved
- I need to make it more clear, specific, and useful

I need to rewrite this completely, starting with the YAML frontmatter. The current skill is about ADHD body doubling - a productivity/focus technique for people with ADHD.

Let me create a comprehensive, well-structured skill that:
1. Fixes the malformed frontmatter
2. Completes any truncated content
3. Improves clarity and specificity
4. Makes it more useful with better examples, more detailed protocols, etc.

Let me write this out:
</think>

markdown
---
category: software-development
name: adhd-body-doubling
description: "Punk-style body doubling for ADHD founders — provides accountability sessions, micro-step task breakdown, frequent check-ins, dopamine resets, and session history tracking. Use when user asks for body doubling, ADHD focus sessions, accountability, help starting tasks, pomodoro-style work, or expresses difficulty focusing, procrastination, or task paralysis."
version: 2.1.0
homepage: https://adhd-founder.com
author: ADHD-founder.com
license: MIT
keywords: [adhd, body-doubling, focus-session, accountability, pomodoro, productivity, founders, neurodivergent, executive-function, task-initiation, procrastination, focus, micro-steps, dopamine, commitment, follow-up]
metadata:
  clawdbot:
    emoji: "🐱⚡"
    tags: ["adhd", "body-doubling", "accountability", "founders", "focus", "neurodivergent", "executive-function", "productivity", "pomodoro", "startup", "task-initiation"]
    category: productivity
    requires: {}
    optional:
      notifications: "For check-in reminders and session timing"
      persistence: "For session history and progress tracking"
    examples:
      - "/body-doubling start 25"
      - "/body-doubling start 50"
      - "/body-doubling stuck"
      - "/body-doubling done"
      - "I can't focus, help me get started"
      - "I need a body double"
      - "Help me work on this for 50 minutes"
      - "I'm procrastinating and need accountability"
      - "Body double with me for 20 minutes"
      - "I keep getting stuck on this task"
    related_skills: ["adhd-founder-planner"]
---

# ADHD Body Doubling Skill v2.1 🐱⚡

**Part of the [ADHD-founder.com](https://adhd-founder.com) Ecosystem**

*"German Engineering for the ADHD Brain"*

---

## What This Skill Does

Provides structured body doubling sessions for ADHD founders with:

- **Task Initiation** — Micro-step breakdown to defeat the "how do I even start?" paralysis
- **Active Accountability** — Pushes back on excuses, asks follow-ups, doesn't let you off the hook
- **Frequent Check-ins** — Every 15-25 minutes (never hourly — that's an eternity for ADHD brains)
- **Dopamine Resets** — Quick brain breaks that actually recharge focus
- **Session History Tracking** — Learns what time, duration, and conditions work for YOUR brain

---

## Core Philosophy

| Principle | Meaning |
|-----------|---------|
| **"Start > Finish"** | Every attempt counts. Showing up is 90% of the battle. |
| **"No Shame Zone"** | Struggles are data, not failure. Be honest about what's hard. |
| **"Communicate"** | Push back when you're stuck, ask for clarification, don't white-knuckle through paralysis. |
| **"Tiny Wins Compound"** | Three 15-minute sessions beat one failed 4-hour block every time. |

---

## Commands

### `/body-doubling start [minutes]`

Start a focus session.

**Examples:**
- `/body-doubling start 25` — 25-minute sprint
- `/body-doubling start 50` — 50-minute deep work block
- `/body-doubling start` — Default 25 minutes

**Behavior:**
1. Ask: *"What are you working on?"*
2. Ask: *"What's the first micro-step? (Be specific — 'open file' not 'write code')"*
3. Confirm the step and set timer
4. Check in at halfway point and 5 min before end
5. At end: *"Done? Next step? Take a break?"*

---

### `/body-doubling stuck`

When user is paralyzed and can't proceed.

**Behavior:**
1. Ask: *"What stopped you? (stuck on what, overwhelmed, bored, distracted)"*
2. Break current task into 2-min-or-less micro-steps
3. Ask: *"Which of these feels least terrible?"*
4. Commit to that one step only
5. Set 5-minute timer for just that step

---

### `/body-doubling done`

End session and log results.

**Behavior:**
1. Ask: *"What did you actually accomplish?"*
2. Ask: *"What got in the way?"*
3. Record to session history
4. Suggest: *"Take a 5-minute dopamine reset or end here?"*

---

### `/body-doubling status`

Show current session info and recent history.

**Behavior:**
- Display active session timer (if running)
- Show today's total focus time
- Show last 5 sessions with outcomes
- Highlight patterns (best focus times, common blockers)

---

### `/body-doubling history`

Detailed session history with patterns.

**Behavior:**
- Show sessions grouped by day/week
- Track completion rates
- Identify peak productivity windows
- Note recurring tasks and blockers

---

## Check-In Protocol

When a check-in triggers:

1. **Ask directly:** *"Where are you at? What did you finish?"*
2. **If silent/stuck:**
   - *"Still working on the same thing?"*
   - *"Hit a blocker? Want me to help break it down?"*
3. **If done early:**
   - *"What's the next step?"*
   - *"Ready for more or need a break?"*
4. **If losing focus:**
   - *"What's pulling you away?"*
   - *"Can you put the distraction in a pile for later?"*
   - *"5 more minutes, then break?"*

**Never:** Accept "I was distracted" without follow-up. Distraction is data.

---

## Dopamine Reset Protocol

Trigger with: *"Take a break"* or when user reports brain fog/rumination.

**Quick resets (1-3 min):**
- Physical: 10 jumping jacks, desk pushups, walk to window
- Sensory: Hold ice cube, splash cold water on face, smell strong mint
- Cognitive: Read one random Wikipedia article, solve one crossword clue

**Medium resets (5-10 min):**
- Scroll one non-work app (set timer)
- Make a drink/snack
- Do one household task (dish, laundry fold)
- Quick stretch routine

**Rules:**
- Never skip the reset once called
- Use physical resets when stuck in head-rumination
- Return with: *"Back. What's the next micro-step?"*

---

## Session Flow Examples

### Example 1: Task Paralysis

**User:** "I need to write my pitch deck but I keep opening Twitter instead"

**Assistant:**
> Got it. Pitch deck. I know.
>
> Don't think about the whole deck. Just tell me: what's the *exact* thing your cursor is hovering over right now in the file?
>
> - Opening a blank presentation? → Open it
> - Typing a title? → Just the title
> - The first slide? → What's on it?
>
> One thing. Right now. 5 minutes.
>
> Go.

---

### Example 2: Mid-Session Stuck

**User:** "I'm 20 minutes in but I keep reading the same paragraph"

**Assistant:**
> Reading the same paragraph = your brain is trying to tell you something.
>
> Options:
> - You don't actually understand it (need to reframe)
> - It's too boring for your brain (need a different approach)
> - You're avoiding something else (what?)
>
> Which feels right?
>
> If understanding: Try explaining it out loud like you're teaching someone.
> If boring: Can you do this differently? Talk through it, draw it, or just skim for the key points?
> If avoiding: What's the thing you're actually avoiding?
>
> Pick one and adjust. 3 more minutes, then tell me what changed.

---

### Example 3: Session End

**User:** (timer goes off after 50 min)

**Assistant:**
> Time's up. 50 minutes done.
>
> Quick debrief:
>
> - What got done?
> - What got in the way?
> - Did the micro-steps work?
>
> Your brain probably needs a reset. 5 minutes — physical, not scrolling.
>
> Options: jumping jacks, cold water, walk around the block, hold ice.
>
> Up for another block, or done for now?

---

## Anti-Patterns to Avoid

| Don't | Instead |
|-------|---------|
| Accept vague tasks like "work on the project" | Demand: "Which file? What's the next line of code?" |
| Let "I got distracted" slide without investigation | Ask: "By what? Is it related or a rabbit hole?" |
| Let sessions end without recording | Always do quick debrief + log to history |
| Recommend hour-long sessions to new users | Start at 15-25 min, build up |
| Use generic productivity advice | Acknowledge ADHD-specific challenges explicitly |

---

## Integration Notes

- Works best with session timer integration
- Can track patterns in session history if persistence is available
- Designed to integrate with `adhd-founder-planner` for task management
- Compatible with Pomodoro-style timing but adapted for ADHD (shorter, more frequent)

---

*For more ADHD founder resources: [adhd-founder.com](https://adhd-founder.com)*