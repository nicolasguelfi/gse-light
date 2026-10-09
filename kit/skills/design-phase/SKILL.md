---
name: design-phase
description: Run the project's design phase with the project lead in W1, time-boxed to one or two sessions - collect the project's drivers (users, data, the client's existing estate, team skills, budget, hosting, security, how well Claude works in a language, verification needs) by multiple-choice questions into project/design/10-design-drivers.md, open the twelve design decisions in order (repository layout, hosting, environments and promotion path, stack and language, data store, identity, infrastructure as code, continuous integration, test tools, secrets, dependency updates, monitoring) as DD records with options derived from the drivers, then, once decided, fill the kit's placeholders (gates, CI, CLAUDE.md). Use in W1 after the examples are gathered, or whenever a technology choice appears before the design decisions exist.
---

# design-phase — choose the technology from the project's drivers, not from a default

The method fixes **how** a project is run (tests at every step, green gates, registers,
journal); it does not fix **what** it is built with. The stack, the hosting, the
repositories and the tools are chosen in this phase, from the project's own facts (its
**drivers**), and written as design decisions (`DD` records) in `project/design/`. Until
they are decided, the kit's placeholders stay as installed (a `gates.sh`
that prints "no gates yet: design phase in progress").

**Who**: the project lead runs it with Claude (*Ask Claude*); developers join for their
area; the Project Advisor advises on drivers and options and **decides nothing**; the person
who holds each right decides (`project/governance/10-roles-and-go-aheads.md`).
**When**: W1, once the examples and data exports are gathered.
**Where**: in the project's repository, in the project lead's own session (the kit is
installed; everything is written under `project/`). Decision 1 (repository layout) says
whether the code lives as components of this repository (folders, each with its own
gates when needed) or in further repositories, which would then receive the kit too
(`../gse-light/kit/install.sh` run inside each clone).
**Time box**: one or two sessions. If a decision does not close in the box, it stays 🔴
with its options written, and the project moves on with what is decided.

`project/` is the project's shared record in this repository; the method is `../gse-light`.

## 0. Read first (Ask Claude)

`project/README.md` (project, phase, people), `project/requirements/00-vision.md`,
the examples and data exports gathered so far (`project/requirements/`, the dated
source reports), `project/governance/10-roles-and-go-aheads.md` (who decides what),
and the three registers' §0 dashboards (`PD`, `DEC`, `DD`). A driver or a decision that
already exists is amended, never duplicated (`decision-record` step 1).

## 1. Collect the drivers — one question at a time (Person answers, Ask Claude writes)

Write `project/design/10-design-drivers.md` from `../gse-light/templates/design-drivers.md`.
For each section, ask **one multiple-choice question at a time** (three or four options,
plus "other" and "unknown — to measure"); write each answer as a row *Fact · Source ·
Consequence for the design*. A fact with no source is marked "declared by <who>"; a fact
about an existing system is measured when possible (skill `verify-claim`).

| Section | What to ask | Why it matters |
|---|---|---|
| **Users and load** | who uses it, how many, when (peaks), on what devices, in which languages | sizing, interface, end-to-end test matrix |
| **Data and its regime** | what data, personal or not, volume, where it comes from, who may see it, retention | data store, hosting region, data regime record |
| **The client's existing estate and policies** | what the client already runs (identity, cloud, databases, platforms), what its policies allow or forbid | **constraints to weigh, never defaults**: an existing tool is an option with a driver, not the answer |
| **Team skills** | levels per technology from `project/governance/30-skills-and-responsibilities.md` (team profile, no names) | a stack nobody can review is a risk, whatever Claude can write |
| **Budget and timeline** | money per month for hosting and services, weeks to the first production, who pays after the project | managed services versus self-hosting, scope of the skeleton |
| **Hosting and operations capacity** | who operates it after hand-over, with how much time, which hours | monitoring, backups, the two hosting models (reference design ch. 4) |
| **Security and compliance** | identity provider required, data residency, audit, approvals the client's security demands | identity, secrets, hosting region |
| **How well Claude writes and tests in a language** | for each candidate language and framework: does Claude produce idiomatic code, tests and migrations without constant correction? | a stack Claude handles well is cheaper to build and to verify; measured on a small trial when unsure |
| **Verification needs** | which use cases must be simulated through the real user interface; which interfaces (web, mobile, API, batch) | **firm rule**: the end-to-end tests go through the real user interface and are drivable by Claude to simulate the use cases, for verification and validation; the tool is the instance's choice (for a web interface, Playwright is one example) |

End the page with the table "Decisions to open, in order" (§2), each with its future
`DD` id and status.

## 2. Open the decisions, in order (Ask Claude opens; the right-holder decides)

Each line below becomes one `DD` record through the `decision-record` skill, in this
order — a later decision depends on the earlier ones:

1. **Repository layout** — components inside this repository, or further repositories;
   their names. A further repository receives the kit too; `project/README.md` lists every
   repository of the project.
2. **Hosting** — managed cloud, the client's platform, or a self-hosted platform
   (reference design ch. 4).
3. **Environments and promotion path** — which environments exist (at least one
   rehearsal environment identical in shape to production), which branch deploys where,
   who gives each go-ahead.
4. **Stack and language** — language, framework, front end.
5. **Data store** — database, files, backups.
6. **Identity** — who signs in and how (the client's identity provider, or another).
7. **Infrastructure as code** — how environments are declared and recreated.
8. **Continuous integration** — where the gates run, on which events.
9. **Test tools** — unit, integration, and the end-to-end tool that drives the real user
   interface (the firm rule of §1, last row; for a web interface, Playwright is one example).
10. **Secrets** — where they live, how CI and developers reach them.
11. **Dependency updates** — how and how often.
12. **Monitoring** — probe, alerts, logs, who is called.

For each record: the problem in plain words; **2 to 4 options derived from the drivers,
with the driver named next to each option** (for example "B. managed database — driver:
no operator after hand-over, §Hosting and operations capacity"); advantages and
drawbacks; one recommendation with its reason; status 🔴 until the person who holds
the right decides (roles record) — the Project Advisor's advice is not a decision.
Decisions already forced by a driver (a client policy that imposes its identity provider)
are still written, with the driver as the reason, so the record shows why there was no
choice.

## 3. Once decided — fill the placeholders (Ask Claude, in the project's repository)

In this repository (and in each further repository the repository-layout record names):

- `gates.sh`: the real gates (install, lint, tests, coverage threshold, the end-to-end
  suite) — the stub is replaced, never kept next to the real one;
- the kit's CI workflow (`.github/workflows/gates.yml`, which runs `bash ./gates.sh` and
  nothing else): services the tests need, the branches and events that run the gates
  (continuous integration record), the branches that deploy (environments record);
- `CLAUDE.md`: the "Commands" table, the environments and the promotion path from the
  environments and promotion path record, the data regime in force;
- `.claude/settings.json`: nothing to add for safety. The kit's rules — Claude asks before
  any `git push`, the literal command `git push origin main` is denied, no edit under
  `../gse-light/` nor of the cockpit — are **conveniences, not a security boundary**. The
  boundary is **branch protection on GitHub** (recommended): the environments and promotion
  path record says whether `main` and the other branches that deploy are protected, and the
  roles record who enables it.

Then: further repositories, if any, are listed in `project/README.md` by the Project
Advisor — his page: ask him in the hand-over (§4); you update
`project/governance/30-skills-and-responsibilities.md` with the stack decided (the skill
`upskilling` reads it); run `python3 ../gse-light/scripts/check_docs.py`. Each change is
measured (the gates run once, output quoted) before it is called done.

## 4. Hand-over (Ask Claude)

A short journal entry "design phase done" (`session-close`): the records decided and
still 🔴, the repositories, the commands that proved the gates run, what the next sprint
inherits. The Project Advisor reads it in his next brief.

## Guardrails

- **Time box**: say when a session reaches it; close with what is decided and what stays 🔴.
- **Measure before asserting**: a fact about an existing system (versions, volumes,
  policies) is measured or marked "declared by <who>".
- **No vendor without a driver**: a product named in
  `../gse-light/method/40-tool-landscape-examples.md` enters an option only with the driver
  that calls for it; that page is a dated list of examples, not a recommendation.
- **Never propose an illustration project's stack as a default**: the projects the
  method cites as illustrations (Sumvadis, StreamTeX) show how a choice played out there;
  their stack is not this project's answer.
- The Project Advisor advises on drivers and options and decides nothing; the project
  lead decides what the roles record gives him, and no more.

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))
