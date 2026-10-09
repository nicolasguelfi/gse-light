# `<project>` — <Project name>, the project folder

The shared record of <Project name>, run with the method
[`gse-light`](https://github.com/nicolasguelfi/gse-light/blob/main/README.md): this folder,
`project/`, in the project's repository `<project>`, next to the code. This page is the
project's entry page, for everyone on it: what the project is, who is who, the two
repositories and who writes where, the calendar, and where each role starts. Fields
written `<like this>` are filled by the Project Advisor when the folder is created.

**Words used here** (every other term: [glossary](https://github.com/nicolasguelfi/gse-light/blob/main/GLOSSARY.md))

| Word | Meaning |
|---|---|
| **Project's repository** `<project>` | one private repository per project, on GitHub: the code, and in `project/` the shared record (decisions, requirements, plans, minutes, journal); everyone opens Claude Code in it, each person writes their own part |
| **Project folder** `project/` | this folder: the shared record; everyone reads it, each person writes their own part in it through the kit's skills |
| **Go-ahead** | the written yes of the person who holds that right (roles record), before any state-changing action |
| **Kit** | the files that make every Claude Code session in the repository follow the method — `CLAUDE.md`, twelve skills, four agents, permissions, a `gates.sh` stub, two CI workflows — installed with one command by the Project Advisor, committed with the code |
| **Skill, agent** | a skill is a procedure Claude runs when asked (`/name`) or when the situation calls for it; an agent is a read-only helper Claude launches |
| **Decision record and badges** | every `PD-NN`, `DEC-NNN` or `DD-NN` in this folder is one numbered decision record in a *register* (project `PD`, requirements `DEC`, design `DD`), with a status badge: 🔴 pending, 🟢 decided, 🟡 provisional; its *decider* is the person the roles record names for it, the only one who turns it 🟢 |
| **Cockpit** | `BRIEFING.md`, the Project Advisor's one-page dashboard — what awaits him, what awaits the team, what changed; written by his sessions only |
| **Design phase** | the step of W1 where the project lead, with Claude, turns the project's facts and constraints into twelve technical decisions (`DD` records) |
| **Day 0** | each person's first hour — clone, `.env`, `check.sh`, first session, `/upskilling`, first journal entry — on a personal branch `day0-<firstname>` |

## People

**Who is who** — who decides what, and who hosts the project's repository: [roles and go-aheads](governance/10-roles-and-go-aheads.md).

| Role | Side | What they do | What they decide or write |
|---|---|---|---|
| **Client** — <client name> | the organisation the product is built for | names the product owner and the data protection contact | — |
| **Product owner** — <product owner> | client | owns the need; accepts each delivered increment | the production and budget go-aheads |
| **Data protection contact** — <data protection contact> | client | — | how personal data may enter the product |
| **Project lead** (lead developer) — <project lead> | the team | runs the project: sprints, tickets, technical choices, code review; the developers' first contact | the sprints; the design decisions |
| **Developers** — <developers> | the team | build the product with Claude Code ("team member" = the project lead or a developer) | the implementation of their tickets; their own journal entries and pending records |
| **Project Advisor** — <Project Advisor> | outside the team; the method's author | two hours of meeting and two hours of preparation a week; feedback and advice; installs and refreshes the kit | nothing in the project — the method and the kit only |
| **Claude sessions** | in the project's repository | propose, measure, write, test | nothing; they act on a go-ahead |

**Everyone opens Claude Code in the project's repository.** The kit's rules say what each
role's session does; the Project Advisor's six skills (`advisor`, `meeting`, `slides`,
`cockpit-update`, `method-lesson`, `genai-onboarding`) and the cockpit `BRIEFING.md` are his:
they check the git user and stop for anyone else. Your journal entries and your new 🔴
records go into this folder through the skills `session-close` and `decision-record`; the
project lead's sessions also write `planning/sprints/`.

## Repositories

| Repository | What it is for | Who writes in it | Who reads it |
|---|---|---|---|
| `gse-light` (public) | the method: the rules every session follows, the templates, the scripts, the kit — cloned next to `<project>` as `../gse-light` | the method's author only; every session reads it, none changes it | everyone |
| `<project>` (private, this one) | the project: the code, and in `project/` the shared record | each person their own part: the developers the code by pull request, their journal entries and new 🔴 records; the project lead the sprints, the design phase, the review of every pull request; the Project Advisor's sessions the cockpit, the briefs, the draft minutes, his journal entries, this page, and the kit | everyone — the product owner on GitHub |

<Once the repository layout is decided (the first `DD` record): components of this
repository, or further repositories — list each further repository here, one row each, with
the kit installed in it.> The `delivery-auditor` agent — the read-only helper that
measures, before each meeting, what the team delivered (tickets, pull requests, gates,
journal entries) — audits the repositories of this table only; a personal throwaway
repository a team member keeps for experiments is never audited.

**Access**: the host of the repository (roles record) grants it. On a repository owned by a
personal GitHub account, a collaborator always has write access (GitHub has no read-only
collaborator there); an organisation's repository has read-only roles. The product owner
needs to read `project/` on GitHub: where the repository lives, and what that means for
access, is a `PD` record of the roles record's host.

## The project

<Two or three lines: what the product does, for whom, what "done" means. The vision is
written in `requirements/00-vision.md`.>

**Calendar.** <n> **project weeks** W1–W<n>, one sprint each, from <YYYY-MM-DD>; the framing
week W-1 ends with the kick-off of <YYYY-MM-DD>. <One line on the team's rhythm: part time
or full time per period, and how many meetings with the Project Advisor in each.> The
project lead dates and sizes the weeks with the team; the meeting day with the Project
Advisor is fixed at each meeting for the next one.

| When | Week | Team | Meeting with the Project Advisor |
|---|---|---|---|
| <YYYY-MM-DD> | W-1 — the framing week before W1 (names, vision, kick-off) | — | **kick-off** |
| <YYYY-MM-DD> → <YYYY-MM-DD> | **W1** — the design phase | <part time / full time> | <date, day fixed at the kick-off> |
| <YYYY-MM-DD> → <YYYY-MM-DD> | **W2 … W<n>** | <part time / full time> | weekly, day fixed at each meeting |

## Phase

Framing (W-1), since <YYYY-MM-DD>: examples and data are being gathered; the team is
<named / being named>; every design choice is 🔴 pending in the
[design register](design/05-design-decisions.md) until the design phase of W1, which opens
twelve `DD` records in order, recorded by the project lead with the kit skill `design-phase`,
in this repository:

1. repository layout;
2. hosting;
3. environments and promotion path;
4. stack and language;
5. data store;
6. identity;
7. infrastructure as code;
8. continuous integration;
9. test tools;
10. secrets;
11. dependency updates;
12. monitoring.

## Start here

Common to every reader: the [glossary](https://github.com/nicolasguelfi/gse-light/blob/main/GLOSSARY.md)
and the [reference design](https://github.com/nicolasguelfi/gse-light/blob/main/method/00-reference-design.md)
(the method's rules for building, testing, delivering and running a product), chapters 0
(purpose and how to read it), 1 (principles), 2 (how people and AI share the decisions) and
13 (working with the AI day to day).

### If you are the project lead

- **Read first**:
  - [`QUICKSTART.md`](https://github.com/nicolasguelfi/gse-light/blob/main/QUICKSTART.md) — what gse-light does for you, the numbered path from zero to your first session, what to use at each moment of the project;
  - the reference design, chapter 15 — the start-of-project checklist;
  - the [roles record](governance/10-roles-and-go-aheads.md) — what you decide, which go-aheads you give;
  - the [design register](design/05-design-decisions.md) — the twelve decisions you open in W1.
- **Install**: nothing — the kit is in the repository, installed and refreshed by the
  Project Advisor; your Day 0 is a developer's (below).
- **Write**: `planning/sprints/` (one file per week, the tasks taken from the minutes), the
  drivers page `design/10-design-drivers.md` and the `DD` records of the design phase (kit
  skill `design-phase`, in this repository), your journal entries and new 🔴 records (kit
  skills `session-close`, `decision-record`); the `<…>` fields of `CLAUDE.md`, `gates.sh` and
  the CI once the design phase has decided them; the review of every pull request.
- **Never**: edit `BRIEFING.md`; turn 🟢 a record whose decider is someone else; promote to
  production or create cloud resources without the product owner's go-ahead.

### If you are a developer

- **Read first**:
  - [`QUICKSTART.md`](https://github.com/nicolasguelfi/gse-light/blob/main/QUICKSTART.md) — one page: what gse-light does for you, the numbered path from zero, what to use all project long;
  - [`kit/INSTALL.md`](https://github.com/nicolasguelfi/gse-light/blob/main/kit/INSTALL.md) — prerequisites, `.env`, `check.sh`, what is shared or personal;
  - [`kit/ONBOARDING.md`](https://github.com/nicolasguelfi/gse-light/blob/main/kit/ONBOARDING.md) — who provides what, the method in one page, your first session step by step, the week's rhythm;
  - the [roles record](governance/10-roles-and-go-aheads.md).
- **Install**: the numbered path of [`QUICKSTART.md`, "from zero to your first session"](https://github.com/nicolasguelfi/gse-light/blob/main/QUICKSTART.md#if-you-are-a-developer-from-zero-to-your-first-session)
  with this project's names — your seat and Claude Code, GitHub access to `<project>`, the
  two clones side by side, `.env`, `check.sh`, `claude`, `/upskilling`, your first journal
  entry, on a personal branch `day0-<firstname>`.
- **Write**: code by pull request on a feature branch with its tests; your journal entries
  and new 🔴 records, through the kit skills `session-close` and `decision-record`.
- **Never**: edit `BRIEFING.md` or anything under `../gse-light`; turn a record 🟢; push to
  a branch that deploys, or open a new flow of personal data, without the go-ahead the roles
  record names.

### If you are the product owner

- **Read**, on GitHub, in `project/`:
  - the vision `requirements/00-vision.md` — the need in five lines, yours to confirm;
  - the [requirements register](requirements/05-decisions.md) — the `DEC` records awaiting you;
  - the [roles record](governance/10-roles-and-go-aheads.md) §2 — the go-aheads you give: production, cloud resources, the budget;
  - the minutes of each meeting in [`meetings/`](meetings/README.md).
- **Install**: nothing — you read on GitHub, with the access the host of the repository gives you.
- **Write**: nothing here — your decisions and go-aheads are recorded in your name, with the
  date, by the project lead's or the Project Advisor's sessions; your tasks are in the minutes.

### If you are the Project Advisor

- **Read first**:
  - [`BRIEFING.md`](BRIEFING.md), your cockpit — §1 what awaits you, §1b what awaits the team, §2 what changed, §3 the state;
  - [the Project Advisor's page](https://github.com/nicolasguelfi/gse-light/blob/main/method/15-project-advisor.md) — where the Advisor steps in, the weekly meeting, what he does by default and does not.
- **Install**: the kit, once, at the root of the project's repository
  (`../gse-light/kit/install.sh`, then a commit — [`kit/README.md`](https://github.com/nicolasguelfi/gse-light/blob/main/kit/README.md));
  refresh it the same way after a change in `gse-light`; your machine for recording and
  transcription ([`scripts/README.md`](https://github.com/nicolasguelfi/gse-light/blob/main/scripts/README.md));
  your own rules, `cp .claude/roles/advisor.json .claude/settings.local.json` (never committed).
- **Write**: open Claude Code in the project's repository — the start hook says where the
  week stands — and say "go": your sessions write this page, `BRIEFING.md`, the meeting
  folders (brief, transcript, the draft minutes with your feedback section — the project
  lead validates and sends them), your journal entries, and the 🟢 of the records you decide
  (the method, the kit, your own spending).
- **Never**: write a sprint, a ticket or code; decide in the project (sprints, priorities,
  promotions, the client's budget); turn 🟢 a record whose decider is someone else.

## Folders

| Path | What it holds |
|---|---|
| [`BRIEFING.md`](BRIEFING.md) | Cockpit: §1 what awaits the Project Advisor, §1b the team, §2 changes, §3 state |
| [`governance/`](governance/) | Roles and go-aheads, project decisions (`PD-NN`), charter and risks once written |
| [`requirements/`](requirements/) | Vision, requirements decisions (`DEC-NNN`); `40-examples/` one file per real example (`EX-<AREA>-NNN-<short-name>.md`: `EX` example, `AREA` the short code of the part of the product, `NNN` its number — the identifier the requirements cite); `50-sources/<date>-<source>.md` one dated report per source — personal data stays out of git (the project's data-regime record) |
| [`design/`](design/) | Design decisions (`DD-NN`), the drivers page and the design choices once the design phase runs |
| `planning/` | Roadmap and one file per week in `sprints/` (project lead) |
| [`meetings/`](meetings/README.md) | One folder per meeting (agenda, transcript, minutes, slides, review boards); presentations registry |
| [`journal/`](journal/README.md) | One entry per working session, `metrics.csv` — never rewritten |
| `private-terms.txt` | Terms the leak guard refuses in the public `gse-light` (client name, project name) |

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))
