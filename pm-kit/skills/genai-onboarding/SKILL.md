---
name: genai-onboarding
description: Prepare the arrival of one engineer or the project lead on the active instance - a personal cover note built on ../gse-light/claude-kit/ONBOARDING.md (who provides what, their repositories, their role's extras, the Day-0 checklist) and the Project Advisor's own to-do for that arrival (licence invitation, access), then verify the Day-0 checklist from the person's first journal entry. Use when NG names a team member, before the kick-off, or when someone joins mid-project.
---

# genai-onboarding — one person, one page, one check

The manual is `../gse-light/claude-kit/ONBOARDING.md` (generic, maintained with the kit). This skill
does what the manual cannot: name the person, their repositories and role, list what the
Project Advisor must do for them, and check later that Day 0 happened.

## 1. Before the arrival (10 minutes)

1. **Ask NG once** (QCM, short): name, role (project lead / engineer), start date,
   e-mail for the Claude invitation if he has not sent it. Repositories and the gates
   command come from the registers (repositories, stack) — if still 🔴, the note keeps the
   `<…>` fields and says so.
2. **Write `instances/<instance>/governance/onboarding/<first-name>-<YYYY-MM-DD>.md`** (private repository;
   no personal data beyond name, role, e-mail domain):
   - a five-line welcome in the Project Advisor's voice: role, first meeting date, what the first
     week is about;
   - "What you receive and from whom" filled for them (licence invitation sent on
     `<date>`, keys via the project lead, repository URLs);
   - the link to `../gse-light/claude-kit/ONBOARDING.md` and the §5 extras if project lead;
   - their responsibilities (from `instances/<instance>/governance/30-skills-and-responsibilities.md`
     §2) and the skills they need, and a pointer to the kit skill `upskilling`, which they run
     on Day 0 (../gse-light/method/20-upskilling.md) — never their individual levels;
   - the Day-0 checklist copied, to be ticked in their first journal entry.
3. **Project Advisor's to-do for this arrival**, in the same note, each line measurable: Claude
   team invitation sent; repository access granted (`gh api repos/<owner>/<repo>/collaborators/<login>` once known); first meeting date confirmed.
4. Add a one-line task to `instances/<instance>/BRIEFING.md` §1 only for what NG himself must do (send the
   invitation); the rest is the project lead's.

## 2. After the first session (5 minutes, at the next brief)

- Find the person's first journal entry in `instances/<instance>/journal/` (`grep -l "<name>"`).
- Check the Day-0 checklist lines against it: each ticked line has its command; the
  `.env` is not tracked (`git -C <repo> ls-files .env` → empty); `KIT_VERSION` present.
- Report in the brief: done / missing, as facts. A missing line is a point for the
  Project Advisor's feedback, not a reproach in the minutes.

## Rules

- The manual stays generic: anything you find missing while onboarding someone goes
  into `../gse-light/claude-kit/ONBOARDING.md` through `method-lesson`, not into the personal note.
- Never send the invitation or grant access yourself: NG and the project lead do;
  you prepare and verify.
- Keep the note to one page.
