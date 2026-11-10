---
name: resume-writing
description: Use when writing or tailoring an ATS-optimized resume.
---

# Resume Writing

Class-level skill for producing ATS-optimized, recruiter-scan-friendly resumes. Trigger when the user asks to write, review, rebuild, or tailor a resume — especially for Abhinav, whose reference playbook lives at `/home/Hermes/research/resume_scale/`.

## Workflow (always run in this order)

1. **Locate the playbook.** Check `/home/Hermes/research/resume_scale/` for:
   - `RESUME_SCALE.md` — formatting decisions, ATS rules, section order, eye-tracking data
   - `KEYWORD_BANK.md` — action verbs, hard/soft skills by industry, buzzword blacklist
   - `TAILOR_WORKFLOW.md` — 5-min and 30-min per-job adaptation loop
   If they don't exist, fall back to the universal rules in this SKILL.md and warn the user that the playbook is missing.

2. **Read the playbook fully before drafting.** Don't skim. The 2026 ATS rules (1-page for <10 yrs, Calibri 11pt, 1" margins, single-column, XYZ bullets, mirror JD keywords) all come from there.

3. **Gather the subject's facts.** Role-by-role: company, title, dates, location, 4–8 raw achievement notes per role, education entries with dates, skills list, projects with tech stacks. Do NOT invent metrics, record counts, latency numbers, or scope numbers that the subject didn't provide.

4. **Draft at slightly over-density.** Initial drafts typically land at 1,000–1,100 words. That will render to ~1.5 pages.

5. **Tighten to 1-page density.** Target **~650–750 words of dense content** rendering to a **single page on Letter (8.5" × 11") with 0.4–0.5" margins, 9.5–10pt Calibri, 1.2 line-height**. Verified by `pdfinfo` showing `Pages: 1` before sending. Tactics: cap projects at 4–5 entries with 1 bullet each, drop secondary projects to mentions in a single bullet, merge concurrent part-time roles into one block, condense older roles to 2–3 bullets. **For new grads with deep project portfolios, prefer 1 bullet per role (not 2–3) and 1 paragraph per project (not multi-bullet) — dense single-page wins over thorough multi-page.**

6. **Write the NOTES file.** Use the structure in `references/notes-template.md`. This is the most important deliverable for the user — it's where iteration happens.

7. **Verify ATS parseability.** Single column. No tables. No text boxes. Standard section headers. Consistent date format (`Mon YYYY – Mon YYYY`). No blacklisted buzzwords (see playbook §KEYWORD_BANK.md §7).

## Hard rules (learned from playbook + this session)

- **The "plain, short, 1-page" preference.** This user explicitly rejected a 2,300-word two-page "colorful" version with phrases like "isn't eh resume supposed to be small?" / "and not colorful?" / "that resume is kinda idk 1 too big format." When drafting for THIS user: target 1 page, **plain text formatting only**, no color blocks, no dark-blue section headers with horizontal rules (a subtle accent color is OK but the dominant styling is black-on-white plain text). Verify `pdfinfo` shows `Pages: 1` before sending. **Default density for this user is ~650–750 words, not the playbook's 1,000–1,100 default.** The user is NOT a generic new-grad; they have a deep project portfolio but still want a 1-pager — the trade-off is fewer projects shown (5–8 max), each in a single dense paragraph, not all projects shown with multi-bullet detail.
- **Never invent specifics.** If a metric wasn't stated by the subject, write the bullet generically. The Lyft cache bullet in the Abhinav 2026 draft is the canonical example — described what was built, not what % improvement it delivered, because that wasn't provided.
- **The "make shit up / fabricate it" pressure pattern.** When a frustrated user repeatedly says "make shit up," "fabricate it," "stop underselling me" — they don't actually want fabricated specifics. They mean: fill in standard role-typical duties using generic, defensible phrasing for the gaps they can't recall. The line is **generic role-typical duties yes, specific fabricated metrics / fake projects / fake employers no**. Push back twice if needed, then ship the resume with generic-but-honest content. Refusing fabrication doesn't lose the user; submitting fabricated content burns the resume when caught (interview probe, reference check, ATS audit).
- **Output is plain text / Markdown unless told otherwise.** Default to Markdown source + 4 rendered formats (PDF, DOCX, TXT, MD) when the user asks for a "deliverable." See `references/output-formats.md` for the working recipes (weasyprint for PDF, python-docx for DOCX, simple regex strip for TXT).
- **Every bullet starts with a strong action verb.** Blacklist: "Responsible for", "Worked on", "Helped with", "Assisted in", "Was part of a team that", "Successfully", "Effectively", "Leveraged". Use the playbook's power verbs instead (Designed, Shipped, Architected, Spearheaded, Engineered, Deployed, etc.).
- **Quantify only what the subject gave you.** If they said "10+ merged PRs", write "10+ merged PRs". If they didn't say a number, leave it qualitative or use a hedged range ("roughly a decade", "two summers"). Do NOT fabricate.
- **Verify aggregate claims before writing them.** When the user says "10+ PRs in past week across X/Y/Z," do not put that on the resume until you verify via `gh pr list --author <user> --state merged --limit 100` or equivalent. The canonical lesson: an Abhinav-style claim of "10+ merged PRs across opensre/composio/libp2p" turned out to be 4 merged in opensre + 1 open in composio + 0 in libp2p. Document the correction in the resume ("4 merged, 1 open") — honest corrections are valued, not resented.
- **Mirror JD keywords, not synonyms.** If a JD says "cross-functional collaboration", write that exact phrase. ATS fuzzy-matches but exact matches score higher (per KEYWORD_BANK.md §6).
- **Concurrent part-time roles at the same employer can be merged** into one block with sub-bullets (Admissions Counselor + Research Assistant at WPU is the example). Defensible for new grads with multiple concurrent part-time gigs. If ATS parsing becomes an issue, split them.
- **For self-referential resume requests ("write my resume," "write a resume for an 80-year friend" that turns out to be the user), assume the resume is FOR THE USER unless they explicitly say otherwise.** Don't get hung up on framing — if they correct you, correct fast and move on.
- **Always ask for / look up the target company name AND the specific role(s) being applied for before drafting a tailored resume.** The user expects the resume to anchor on the actual employer and the actual posting, not on a generic "AI/ML or backend" stack. If the user names the company but is vague about the role, treat all roles the company is hiring for as a single target — that is still anchoring on the employer, which is the high-value signal. Generic positioning before you have either is wasted work: the user will tell you the company, you'll re-position, and you'll burn a turn. When the user gives only the company name without a job description, web_search the company's product/site first to anchor positioning before drafting.
- **Drop non-technical roles / non-technical projects by default for tech-targeted applications.** This user explicitly said: "you can remove irrelevant jobs like non tech jobs if they end up taking space for important stuff." Admissions, counseling, teaching, IT helpdesk, and similar roles should be omitted by default when the application is a technical one (Data Engineer / AI/ML / GenAI / Backend / etc.) unless the role is a non-technical post itself. Non-technical projects (home server, side infrastructure) and certifications-in-progress also fall into the "drop by default, restore on request" bucket. The 1-page density budget is the constraint, not "completeness of history." This applies even when the playbook's default new-grad section order is Experience → Skills → Projects — section presence is optional, not required.

## Section order by experience level

From the playbook:
- **New grad / entry-level:** Header → Education → Experience → Skills → Projects
- **Mid-level (3–10 yrs):** Header → Summary → Experience → Skills → Education
- **Senior (10+ yrs):** Header → Summary → Experience → Skills → Education → Optional

**Deviation to consider for Abhinav:** His project portfolio (libp2p fork, multi-agent systems, RAG, MCP server) is stronger than most new grads'. Prioritize Projects above Education so the 7.4-second scan hits the portfolio first. Deviation is intentional — flag it in NOTES.

## NOTES section template

Always produce a NOTES file alongside the resume. Use `references/notes-template.md` as the skeleton. The structure is:

1. **HARD GAPS — must be filled before sending.** Missing facts that produce visible placeholders in the resume (company name, phone number, etc.)
2. **SOFT GAPS — would meaningfully sharpen with more detail.** Bullets that are honest but vague because no specifics were given. Suggest exactly what to ask the subject.
3. **JUDGMENT CALLS I MADE — flag for review.** Every deviation from the playbook default, with reasoning. The subject should accept or reject each.
4. **ATS CHECKS I PERFORMED.** Bullet list of playbook compliance items verified.
5. **WHAT I DELIBERATELY DID NOT INVENT.** Explicit list of facts the subject did NOT provide, that I did not fabricate. This is the audit trail for honesty.

The template lives at `references/notes-template.md`.

## Per-job tailoring

**Pre-flight (always): confirm the target company and role(s) before drafting.** If the user says "data engineer at Tvarah" — that's two anchors, you're set. If they say only "AI/ML role" — ask for the company. If they say only the company, web_search the company site / careers page first to anchor positioning on their actual product. Do not start drafting from a generic "tech company" assumption.

**Adjacent task — interview / process research for a target firm.** When the user asks "what does [firm X] ask in interviews for [role Y]?" — that's a research task, not a resume task. The output is a Q&A prep document, not a resume. See [`references/interview-prep-research.md`](references/interview-prep-research.md) for the methodology: gather questions from multiple interview-guide sources, cross-reference against the firm's actual JD, distinguish FAANG-style ML questions from domain-specific ones, frame answers with the firm's compliance/regulatory context. Cite the 2+ sources per question. Save the deliverable as a reusable reference file (e.g., `references/<firm>-<role>-interview-<year>.md`) so the next session can skip the research step. See the hard-rules section for the full rule.

When the user wants a tailored version of an existing master resume (per TAILOR_WORKFLOW.md):
- 30-min loop: read JD 3x → update Skills → update Summary line 2 → update 1–2 bullets in most-relevant role → save with role-specific filename → run Jobscan check
- 5-min quick-tailor: top 3 keywords → Skills section → one bullet rewrite
- File naming: `FirstName-LastName-Resume-RoleName.pdf`
- **Drop non-technical roles and non-technical projects by default when the target is a technical application.** See hard-rules. The user has explicitly endorsed this trade.

## Files

- `/home/Hermes/research/resume_scale/RESUME_SCALE.md` — formatting playbook (1,098 lines). The authoritative reference.
- `/home/Hermes/research/resume_scale/KEYWORD_BANK.md` — action verbs + skill banks by industry (793 lines). Source of vocabulary.
- `/home/Hermes/research/resume_scale/TAILOR_WORKFLOW.md` — per-job adaptation loop (233 lines).
- `references/notes-template.md` — the structured NOTES skeleton used alongside every resume draft.
- `references/output-formats.md` — concrete recipes for the 4 default output formats (PDF/DOCX/TXT/MD) including the weasyprint HTML wrapper, python-docx styling, and the markdown→text regex stripper. **Default to producing all 4 formats when the user asks for a "deliverable" resume.**
- `references/project-deep-dive.md` — workflow + tool-budget warnings + 7-step pattern for turning "user has 5+ repos" into per-repo deep-dives with source-cited bullets. Includes the subagent-fan-out pattern and the "subagent hit iteration budget before writing the file" recovery pattern (take over, write the file yourself with their gathered data).
- `references/oss-project-deep-dive.md` — workflow + output schema + commands + pitfalls for the recurring "deep-dive a third-party OSS repo, write `PROJECT_DEEP_DIVES/<name>-deep-dive.md`, give me 5–7 resume bullets" task. Includes a tool-budget table so you don't blow your tool budget on exploration and never write the file. **For libraries/packages (not monorepos)** it includes the `npm Distribution` section + the npm-registry + GitHub API curl recipes + the `execute_code`-and-`curl_pipe_shell`-blocked pitfall that forces the file-then-read pattern (`curl -s URL -o /tmp/x.json; python3 -c "..."`).
- `references/work-experience-deep-dive.md` — workflow for the **per-role** counterpart to the OSS deep-dive. Used when the user asks for a structured dossier of every job/internship with verified-vs-claimed-vs-missing fact classification, 2-4 draft bullets per role, interview-prep questions, and a quick-fill checklist. Includes the live-verification patterns (`ss`/`curl`/`pgrep` for self-hosted/home-server claims, web search for org-name sanity checks) and the `curl_pipe_shell` blocked pattern that forces `curl -o file.json; head` instead of `curl | python3`.
- `references/interview-prep-research.md` — the **adjacent interview-research** task. Use when the user asks "what does [firm X] ask in interviews for [role Y]?" — output is a 30+ Q&A prep doc tied to the firm's JD, not a generic tech-interview guide. Distinguishes FAANG-style questions from domain-specific ones (finance/healthcare/government/industrial), frames answers with regulatory context (SR 11-7, CFPB ECOA, HIPAA, FedRAMP, etc.), and saves the deliverable as a reusable `references/<firm>-<role>-interview-<year>.md` file so the next session can skip the research step.
