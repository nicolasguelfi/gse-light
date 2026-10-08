# 20 — Upskilling: starting from the team's real levels

Status: draft · v0.3 · 2026-10-08 · author: Nicolas Guelfi, with Claude

> **Essentials** — A team's levels in generative AI, coding agents and development are
> unknown at the start and rarely even. The method does not assume them: it measures
> where each person starts, compares it with what their responsibilities need, and
> closes the gaps on real work, step by step. Each member runs the kit skill `upskilling`
> at their own pace; individual answers stay private; only an aggregated team profile is
> shared. Who does each action: *Person*, *Ask Claude*, *Automatic*
> ([the Project Advisor's page §0](15-project-advisor.md#0-who-does-an-action--three-marks)).

## 1. Where do we start — at the kick-off

A round table of about ten minutes (*Person*: each member, two minutes) on the
[skills grid](../templates/skills-grid.md): eight dimensions scored 0–3 and one free
question. It sets expectations and names the gaps; it is not an examination. The Project
Advisor notes the aggregated picture, never individual scores in public.

## 2. What each role needs

| Competence | Developer | Project lead | Product owner |
|---|---|---|---|
| Asking an agent for a task, reading its proposal, saying no | 2 | 2 | 1 |
| Reviewing AI-written code and tests before merging | 2 | 3 | — |
| Using the kit (`decision-record`, `design-phase`, `session-close`, `upskilling`, `verify-claim`, agent `change-reviewer`) | 2 | 3 | — |
| Git, pull requests, CI gates | 2 | 3 | — |
| Writing tests with Claude (unit, integration, end-to-end) | 2 | 2 | — |
| The project's technical skills — the stack decided in the design phase (instance list) | per responsibility | per responsibility | — |

Levels are the grid's scale (0–3). The instance lists its technical skills (from the
stack its `DD` records decided in the design phase) and each person's responsibilities
in `instances/<instance>/governance/30-skills-and-responsibilities.md`, in the project's
project-management repository.

## 3. The method, introduced in two steps

| When | What applies | Who |
|---|---|---|
| **First week** — the base | measure before asserting; evaluate ≠ execute (go-aheads); a journal entry per session; decisions in the registers; gates run before every merge | Automatic (Claude by the kit's rules) + Person |
| **Second week** — with the walking skeleton | tests at every step with Claude, coverage, the map of what is verified, end-to-end tests through the real user interface (tool decided in the design phase) | Ask Claude + Automatic (CI) |

The `upskilling` skill follows the same order: it does not train someone on coverage maps
before the base is in place.

## 4. Closing the gaps

- *Ask Claude* — `upskilling` (kit skill): assesses the person in conversation and with
  two or three small checks on real tasks (measured, not only declared), compares with
  what their responsibilities need, proposes a short plan of exercises (one hour at most
  each, on the real project or a practice repository), and follows progress at each run.
- *Person* — the project lead pairs a more experienced member with a less experienced
  one on the first tickets.
- *Person* — the Project Advisor runs a two-hour session only if the gap is large across
  the team (his time is four hours a week).
- The team's aggregated profile is read at the first weekly meeting, where the project
  lead and the product owner may resize the weeks (instance decision on the goal).

## 5. Privacy

Individual answers and plans live in the person's home folder, outside every repository,
one sub-folder per project (`~/.claude/upskilling/<instance>/record.md`; decided
2026-10-07) — where Claude Code keeps each user's own data. The skill is run from the
person's sandbox or product repository, never from the project-management repository.
The shared file holds only
counts per dimension and level, with no names, and the alignment tasks decided.

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))
