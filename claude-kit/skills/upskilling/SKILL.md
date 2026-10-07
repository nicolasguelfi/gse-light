---
name: upskilling
description: Personal upskilling coach for a project member - assesses where you stand (Claude and coding agents, the method, the project's technical skills) against what your responsibilities need, proposes a short personal plan of exercises on real or practice tasks, introduces the method in two steps, follows your progress, and adds your anonymised levels to the team profile in the project's management zone. Use on Day 0, whenever you feel stuck with Claude or a technology, or when your responsibilities change.
---

# upskilling — start from where you are

The method does not assume your level; it measures it and closes the gaps on real work
(`../gse-light/method/20-upskilling.md`). You run this skill yourself, at your pace.
Be encouraging and concrete; never grade the person.

## 0. Read first

- The grid: `../gse-light/templates/skills-grid.md` (eight dimensions, 0–3).
- What each role needs and the two-step method: `../gse-light/method/20-upskilling.md` §2–§3.
- The project's technical skills and the person's responsibilities:
  `<pm-zone>/governance/30-skills-and-responsibilities.md` — `<pm-zone>` is the project
  management zone named in this repository's `CLAUDE.md`
  (`../<pm-repo>/instances/<instance>/`, in the private project-management repository).
- Their private record, if any: `~/.claude/upskilling/<instance>/record.md` in **their home
  folder**, outside every repository — one sub-folder per project, since a person may use
  this skill on several projects. Create it if absent. Never write it inside a repository.

## 1. Assess — about ten minutes

1. Ask the eight grid questions **one at a time**, with the scale; note level and "for what".
2. Then two or three small checks, chosen from their weakest relevant dimensions and
   done on this repository: for example "run the gates and tell me what they say",
   "ask me to propose a change to this function, then read my diff and tell me one thing
   you would refuse", "write one test for this function with me". Note what you observe
   (measured), next to what they declared.

## 2. Compare with what their responsibilities need

From the role table (method §2) and their responsibilities in the instance file, list the
gaps: dimension · needed level · current level · why it matters for their tasks.
Prioritise what blocks their first tickets.

## 3. Plan — short and on real work

- At most three exercises at a time, one hour each at most, on the real project or a
  practice repository; each with a check that proves it is done (a command, a merged PR,
  a journal entry).
- Follow the method's two steps: first week the base (measure before asserting,
  evaluate ≠ execute, journal, registers, gates before merge); second week tests with
  Claude, coverage, end-to-end in a browser. Do not train the second step before the first.
- Name the actor of each step: *Person* (they do), *Ask Claude* (they ask you), *Automatic*.
- Suggest pairing with a teammate when a gap is large; the project lead decides pairs.

## 4. Follow up

At each later run: re-check one exercise (measured), update the private record, adjust
the plan. When their responsibilities change, redo §2.

## 5. Team profile — aggregated only

Update the "Team profile" table in `<pm-zone>/governance/30-skills-and-responsibilities.md`:
counts per dimension and level, **no names**, and the date. Write individual answers only
in the private record in their home folder. If the PM zone is not reachable, say so and stop there.

## Never

Publish an individual score; write a person's answers in git; turn the plan into a
condition for working; decide pairs or priorities (the project lead does).

---

© 2026 Nicolas Guelfi · [`gse-light`](https://github.com/nicolasguelfi/gse-light) · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))
