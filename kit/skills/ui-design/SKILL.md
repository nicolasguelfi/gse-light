---
name: ui-design
description: Before building or changing a screen of the project's product - write its screen sheet from the users' real tasks (who, the frequent task it serves, what must be seen at a glance, the actions in one step, what is left out), propose two or three mock-ups for the person to compare on a review board, then build the chosen one and have the agent ux-reviewer judge its screenshots before the pull request. Use whenever a change adds or alters a user interface - a page, a dashboard, a form, a view.
---

# ui-design — a screen starts from a task, and is judged on screenshots

A screen built quickly from the data tends to show everything the data holds and serve no task well
(the method's owner, 2026-10-29: the first prototype's screens were of very low quality). The method
keeps three steps: **the task first** (a screen sheet), **comparison before code** (mock-ups the
person chooses), **a review on evidence after** (the agent `ux-reviewer` on screenshots). Claude
prepares each step; the person decides.

## 1. The screen sheet — before any code

Copy [`screen-sheet.md`](screen-sheet.md) to `project/design/screens/<screen>.md` and fill it **from
sources**, never from guesses: the interviews and observations of the users (their recorded words,
with times), the requirements (`project/requirements/20-functional/`), the data dictionary. A field
with no source says `[unknown — to ask]`. The sheet names:

- **who** uses the screen, in the project's words (a role, never a name), and how expert they are;
- **the frequent task** it serves, step by step, and how often it happens (from the interviews);
- **what must be seen at a glance** to do that task — and what can wait one click;
- **the actions in one step** (the most frequent ones), and what must never happen by mistake;
- **what the screen leaves out**, and why;
- **how it will be measured**: the number of actions for the frequent task, the time to find the
  one thing the user looks for first, the widths it must work at.

The sheet is short (one page). It goes in the pull request with the screen, or before it.

## 2. Two or three mock-ups — the person chooses

From the sheet, Claude proposes **two or three** different designs (layout, density, what is first),
as static pages or images, each annotated with the frequent task's path (1 → 2 → 3) and its count
of actions. Show them on a **review board** (skill `review`): one subject, one proposal per mock-up,
with its advantages and drawbacks *for the task of the sheet*, a recommendation, a comment field. The
person (the developer, the project lead, or a user when one can be asked) ticks one. Never build
before the line comes back.

Use the project's interface rules when it has them (its design system decision, a `DD` record:
components, palette, density); never impose a library or a style the project has not chosen.

## 3. Build, then the review on screenshots

Build the chosen mock-up with its tests (the end-to-end test of the frequent task, through the real
interface). Then run the agent **`ux-reviewer`** with the pull request's number (or the branch) and
the path of the screen sheet: it takes the screenshots itself, at the widths of the sheet, and judges
them against the sheet and named criteria. Fix or answer each **critical** and **major** finding;
write its verdict on the pull request's line "`ux-reviewer`". `evidence_check.py` warns when a pull
request changes an interface file with no screen sheet or no `ux-reviewer` verdict.

## Never

Build a screen with no sheet; invent a user's task or a frequency (write `[unknown — to ask]`);
choose the mock-up for the person; present the agent's review as a test with users — it avoids the
worst defects, it does not replace watching a user do the task.

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))
