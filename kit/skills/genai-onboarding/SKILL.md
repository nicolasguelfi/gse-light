---
name: genai-onboarding
description: Prepare the arrival of one developer or the project lead on the project - a personal cover note built on ../gse-light/kit/ONBOARDING.md (who provides what, the project's repository and the numbered path of QUICKSTART.md, their role's extras, the Day-0 checklist) and the Project Advisor's own to-do for that arrival (licence invitation, access), then verify the Day-0 checklist from the person's first journal entry. Use when the Project Advisor names a team member, before the kick-off, or when someone joins mid-project.
---

# genai-onboarding — one person, one page, one check

**Who runs this skill**: the Project Advisor's sessions only. First `git config user.name`; if that name is not in the holder cell of the "Project Advisor" row of `project/governance/10-roles-and-go-aheads.md` §1, say so and stop: this skill writes his pages.

The manual is `../gse-light/kit/ONBOARDING.md` (generic, maintained with the kit). This skill
does what the manual cannot: name the person, their repositories and role, list what the
Project Advisor (Nicolas Guelfi, NG) must do for them, and check later that Day 0 happened.

## 1. Before the arrival (10 minutes)

1. **Ask NG once** (one short multiple-choice question, QCM): name, role (project lead /
   developer), start date, e-mail for the Claude invitation if he has not sent it, and
   whether the person's **write access to the project's repository** is granted. Day 0 is
   the numbered path of `../gse-light/QUICKSTART.md`, in the project's repository: clone it
   next to `gse-light`, `.env`, `check.sh`, `claude`, `/upskilling`, the first journal
   entry — on a personal branch `day0-<firstname>`, merged or deleted afterwards. A
   personal throwaway repository is optional, for whoever wants to experiment outside the
   project; nothing of value stays there. The stack and the gates command come later, from
   the `DD` records of the design phase (repository layout, stack and language, test tools),
   run by the project lead in the same repository: while still 🔴, the note keeps those
   `<…>` fields and says the design phase fills them.
2. **Write `project/governance/onboarding/<first-name>-<YYYY-MM-DD>.md`** (private repository;
   no personal data beyond name, role, e-mail domain):
   - a five-line welcome in the Project Advisor's voice: role, first meeting date, what the first
     week is about — examples and data, then the **design phase**: the stack, hosting and
     tools are chosen from the project's drivers in W1, not before (a project lead is told
     he runs it with the `design-phase` skill in the project's repository; a developer that
     the kit's gates stay a stub until it is done);
   - "What you receive and from whom" filled for them (licence invitation sent on
     `<date>`, keys via the project lead, **the project's repository URL and the numbered
     path of `QUICKSTART.md`**, further repository URLs once the repository layout is decided);
   - the link to `../gse-light/kit/ONBOARDING.md` and the project lead's section (§2) if project lead;
   - their responsibilities (from `project/governance/30-skills-and-responsibilities.md`
     §2) and the skills they need, and a pointer to the kit skill `upskilling`, which they run
     on Day 0 (../gse-light/method/20-upskilling.md) — never their individual levels;
   - the Day-0 checklist copied, to be ticked in their first journal entry.
3. **Project Advisor's to-do for this arrival**, in the same note, each line measurable: Claude
   team invitation sent; write access to the project's repository granted
   (`gh api repos/<owner>/<repo>/collaborators/<login>` once known); first meeting date confirmed.
4. Add a one-line task to `project/BRIEFING.md` §1 only for what NG himself must do (send the
   invitation, grant the access if the host of the repository is not the project lead); the rest
   is the project lead's.

## 2. After the first session (5 minutes, at the next brief)

- Find the person's first journal entry in `project/journal/` (`grep -l "<name>"`).
- Check the Day-0 checklist lines against it: each ticked line has its command; the
  `.env` is not tracked (`git ls-files .env` → empty); `KIT_VERSION` present; the entry was
  committed through `session-close` (its path is in `git log`).
- Report in the brief: done / missing, as facts. A missing line is a point for the
  Project Advisor's feedback, not a reproach in the minutes.

## Rules

- The manual stays generic: anything you find missing while onboarding someone goes
  into `../gse-light/kit/ONBOARDING.md` through `method-lesson`, not into the personal note.
- Never send the invitation or grant access yourself: NG and the project lead do; you
  prepare and verify.
- Keep the note to one page.

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))
