---
name: genai-onboarding
description: Prepare the arrival of one engineer or the project lead on the active instance - a personal cover note built on ../gse-light/claude-kit/ONBOARDING.md (who provides what, their sandbox repository and the one install command, their role's extras, the Day-0 checklist) and the Project Advisor's own to-do for that arrival (licence invitation, access), then verify the Day-0 checklist from the person's first journal entry. Use when the Project Advisor names a team member, before the kick-off, or when someone joins mid-project.
---

# genai-onboarding — one person, one page, one check

The manual is `../gse-light/claude-kit/ONBOARDING.md` (generic, maintained with the kit). This skill
does what the manual cannot: name the person, their repositories and role, list what the
Project Advisor (Nicolas Guelfi, NG) must do for them, and check later that Day 0 happened.

## 1. Before the arrival (10 minutes)

1. **Ask NG once** (one short multiple-choice question, QCM): name, role (project lead /
   engineer), start date, e-mail for the Claude invitation if he has not sent it, and
   whether the person's **sandbox repository** exists. Until the product repositories
   exist (repository layout, the first of the twelve decisions of `design-phase` §2, taken
   in the design phase of W1), every team member works in a personal sandbox:
   `<project>-sandbox-<first name>`, private, throwaway, created on GitHub by the project
   lead or by NG, cloned next to `gse-light` and this repository, the kit installed by
   **one command** run inside the clone: `../gse-light/claude-kit/install.sh <instance>`.
   There they do Day 0, `/upskilling` and their experiments; the project lead's sandbox is
   also where the design phase runs. The real product repositories and the gates command
   come later, from the `DD` records (repository layout, stack and language, test tools):
   while still 🔴, the note keeps those `<…>` fields and says the design phase fills them.
   **Nobody opens Claude Code in this project-management repository**: sessions here are
   the Project Advisor's.
2. **Write `instances/<instance>/governance/onboarding/<first-name>-<YYYY-MM-DD>.md`** (private repository;
   no personal data beyond name, role, e-mail domain):
   - a five-line welcome in the Project Advisor's voice: role, first meeting date, what the first
     week is about — examples and data, then the **design phase**: the stack, hosting and
     tools are chosen from the project's drivers in W1, not before (a project lead is told
     he runs it with the `design-phase` skill from his sandbox; an engineer that the kit's
     gates stay a stub until it is done);
   - "What you receive and from whom" filled for them (licence invitation sent on
     `<date>`, keys via the project lead, **their sandbox repository's URL and the one
     command**, the project-management repository's URL, product repository URLs once decided);
   - the link to `../gse-light/claude-kit/ONBOARDING.md` and the §5 extras if project lead;
   - their responsibilities (from `instances/<instance>/governance/30-skills-and-responsibilities.md`
     §2) and the skills they need, and a pointer to the kit skill `upskilling`, which they run
     on Day 0 in their sandbox (../gse-light/method/20-upskilling.md) — never their individual levels;
   - the Day-0 checklist copied, to be ticked in their first journal entry.
3. **Project Advisor's to-do for this arrival**, in the same note, each line measurable: Claude
   team invitation sent; sandbox repository created and access granted
   (`gh api repos/<owner>/<repo>/collaborators/<login>` once known); first meeting date confirmed.
4. Add a one-line task to `instances/<instance>/BRIEFING.md` §1 only for what NG himself must do (send the
   invitation, create the sandbox if the project lead is not yet named); the rest is the project lead's.

## 2. After the first session (5 minutes, at the next brief)

- Find the person's first journal entry in `instances/<instance>/journal/` (`grep -l "<name>"`).
- Check the Day-0 checklist lines against it: each ticked line has its command; the
  `.env` is not tracked (`git -C <repo> ls-files .env` → empty); `KIT_VERSION` present;
  the entry was pushed from the sandbox through `session-close` (its path is in this
  repository's `git log`).
- Report in the brief: done / missing, as facts. A missing line is a point for the
  Project Advisor's feedback, not a reproach in the minutes.

## Rules

- The manual stays generic: anything you find missing while onboarding someone goes
  into `../gse-light/claude-kit/ONBOARDING.md` through `method-lesson`, not into the personal note.
- Never send the invitation, create a repository or grant access yourself: NG and the
  project lead do; you prepare and verify.
- Keep the note to one page.

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))
