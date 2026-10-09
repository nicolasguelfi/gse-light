---
name: method-lesson
description: Turn something learned in a session (a gap between a request and the kit, an artefact that did not fit, a mistake, a rule the Project Advisor stated) into one dated lesson written at the right place - CLAUDE.md, a skill, a template, the reference design or the kit's CLAUDE.md template - then propagate and journal it (standing rule "Improve the project from every interaction"). Use as soon as a gap is named and the Project Advisor says yes to the fix, or whenever he states a way of working.
---

# method-lesson — one lesson, one place, dated

**Who runs this skill**: the Project Advisor's sessions only. First `git config user.name`; if that name is not in the holder cell of the "Project Advisor" row of `project/governance/10-roles-and-go-aheads.md` §1, say so and stop: this skill writes his pages.

The project improves iteratively and incrementally from the sessions (CLAUDE.md,
standing rule). A lesson that stays in the chat is lost at the next session; a lesson
written in four places drifts. This skill puts it in **one** place, dated, and makes the
rest point to it.

## 1. Name the lesson (one line each)

- **Trigger**: what happened — the request nobody could serve, the artefact that did
  not fit, the mistake, the sentence of the Project Advisor (Nicolas Guelfi, NG).
- **Rule**: what a session must do differently next time, in plain words, testable.
- **Why**: the reason, so a later reader can retire the rule when the reason is gone.

## 2. Choose the place — the narrowest that reaches every session concerned

| The lesson is about… | Write it in | Form |
|---|---|---|
| how every session of this project's repository behaves (this project only) | `CLAUDE.md` of this repository → "Lessons learned here" (newest first); promote to "Standing rules" when it holds everywhere | one bullet: rule — date — why |
| one step of one skill or agent | that `SKILL.md` or agent file | a sentence in the step, with the date in parentheses |
| what a document must contain | the template in `../gse-light/templates/` | a field or a comment line |
| how a product is built or run (binding for every instance's team) | `../gse-light/method/00-reference-design.md`, the chapter's "Rules" | a bullet; if it changes a decision, a register record first (`decision-record`) |
| how every session of a project's repository behaves, for every project | `../gse-light/kit/templates/CLAUDE.md` (the template) → "Lessons learned here", or the kit skill, and the project's own `CLAUDE.md` | same forms; then, after `git pull` in `gse-light`, each project's repository refreshes its skills and agents with `../gse-light/kit/install.sh`; a lesson written in the template is copied by hand into the `CLAUDE.md` of repositories that already have one (the installer creates it once, never overwrites it) |
| how NG wants to be asked or informed | `CLAUDE.md` lessons **and** the session memory | bullet + memory file |

A lesson that is really a **decision** (a choice between options, with consequences for
the team) is not a lesson: record it with `decision-record` and write only the pointer.

## 3. Write, propagate, verify

1. Write the lesson at the chosen place, dated `YYYY-MM-DD`, two lines at most.
2. **Propagate**: `grep -rn` this repository and `../gse-light` for the behaviour the lesson
   replaces (old wording, old file name, old rule) and fix every hit. A skill or agent is
   changed in `../gse-light/kit/`, committed there, then copied here with
   `../gse-light/kit/install.sh` — `check_docs.py` fails while `.claude/` differs from the kit.
   A lesson that holds for every project goes to `../gse-light` (never a client's name or
   data: the leak guard checks `project/private-terms.txt`).
3. If the lesson changes a script or a hook, run it once and quote the output.
4. `python3 ../gse-light/scripts/check_docs.py`.
5. Say in one line where the lesson now lives; add it to the session's journal entry
   under "Rules learned".

## 4. Keep the list alive

- Twenty lessons in `CLAUDE.md` is too many: at that point, group them, promote the
  general ones to standing rules, and move the historical ones to the journal (never
  delete the date and the why).
- A lesson whose reason has disappeared is retired with a dated line, not silently.

## Guardrails

- Never rewrite a journal entry to add a lesson; the journal cites, the rule lives
  elsewhere.
- Never add a rule NG did not state or confirm; a hypothesis is written as "to confirm
  with NG" and asked by one short multiple-choice question (QCM).
- Keep it light: a lesson takes two minutes to write and ten seconds to read.

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))
