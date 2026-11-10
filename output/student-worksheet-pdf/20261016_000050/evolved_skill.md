---
name: student-worksheet-pdf
description: Generate printable ESL/IELTS worksheets as PDFs.
---

# Student Worksheet / Handout PDF Generator

## Class of Work

Printable ESL/IELTS materials: sentence drills, vocabulary sheets, grammar worksheets, cloze tests, listening transcripts. Output is always a PDF the teacher prints and gives to a student. Multi-version layouts (Version A vs Version B side by side) are common.

## Hard Rules

These are non-negotiable user preferences.

### 1. No Identifying Information

**Never include the student's name, teacher's name, or any framing language that singles out the recipient.** Avoid titles like "Get back your attention", "For [Name]'s recovery", "Dopamine detox sheet", or any text that implies the student has a problem.

The material should look generic — a worksheet any student could pick up and use. If it has a heading at all, use a neutral description like "6-Word Sentence Worksheet" or "Past Simple Drill".

**Reason:** The worksheet gets handed to the student. Anything that reads as "we know what's wrong with you" turns them off before they even start.

### 2. Fix Manually First, Then Script

When the user reports that output is wrong, work manually one step at a time FIRST. Only encode the solution as a script after manual iteration produces verified-good output.

**Trigger:** User says output is incorrect or "it doesn't work."

**Correct approach:**
1. Write one sentence, verify it by eye, fix it if needed
2. Write the next sentence, verify by eye, fix if needed
3. Repeat until all items are correct
4. Only then write a script that reproduces the verified-good output

**Wrong approach:** "Let me rewrite the auto-expander and run again." This assumes the script will generate correct output without human verification — it won't.

**Concrete example:** When building a 15-word corpus, the user kept saying "worse" because each automated attempt drifted from the target. The right move was hand-writing, hand-counting, and visually verifying each sentence one at a time. Only after 100 verified-good sentences existed did a build script make sense. The script is a downstream artifact of a manually-verified corpus, not a generator that produces good output by hope.

### 3. Plain Means Plain

When the user asks for "black and white, no color, no marking, nothing," deliver exactly that — no embellishments, no decorative elements, no styling that wasn't explicitly requested.