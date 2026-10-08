# Instance `<instance>` — <Project name>

The project-management folder of <Project name>, run with the method
[`gse-light`](https://github.com/nicolasguelfi/gse-light/blob/main/README.md), cloned next to
`<pm-repo>`. This page is the instance's entry page, for everyone on the project: what the
project is, who is who, which repositories exist and who writes where, the calendar, and
where each role starts. **No product code here.** Fields written `<like this>` are filled by
the Project Advisor when the instance is created; `<instance>` is the folder name under
`instances/` (`ls instances` shows it).

**Words used here** (every other term: [glossary](https://github.com/nicolasguelfi/gse-light/blob/main/GLOSSARY.md))

| Word | Meaning |
|---|---|
| **Instance** | one project run with the method, and its folder `instances/<instance>/` in the project-management repository `<pm-repo>` |
| **Project-management repository** `<pm-repo>` | the project's shared record (decisions, requirements, plans, minutes, journal), private, one per project; everyone reads it, each person writes their own part in it through the kit's skills; nobody manages the project from it |
| **Go-ahead** | the written yes of the person who holds that right (roles record), before any state-changing action |
| **Kit** | the files that make every Claude Code session in a repository follow the method — `CLAUDE.md`, five skills, one agent, permissions, a `gates.sh` stub, a CI workflow — installed with one command, committed with the code |
| **Skill, agent** | a skill is a procedure Claude runs when asked (`/name`) or when the situation calls for it; an agent is a read-only helper Claude launches |
| **Decision record and badges** | every `PD-NN`, `DEC-NNN` or `DD-NN` in this folder is one numbered decision record in a *register* (project `PD`, requirements `DEC`, design `DD`), with a status badge: 🔴 pending, 🟢 decided, 🟡 provisional; its *decider* is the person the roles record names for it, the only one who turns it 🟢 |
| **Cockpit** | `BRIEFING.md`, the Project Advisor's one-page dashboard — what awaits him, what awaits the team, what changed; written by his sessions only |
| **Sandbox** | a personal, private, throwaway repository `<project>-sandbox-<firstname>` with the kit, for Day 0 and experiments until the product repositories exist; the project lead's sandbox hosts the design phase |
| **Design phase** | the step of W1 where the project lead, with Claude, turns the project's facts and constraints into twelve technical decisions (`DD` records) |
| **Day 0** | each person's first hour — clone, kit, `.env`, `check.sh`, first session |

## People

**Who is who** — who decides what, and who hosts `<pm-repo>`: [roles and go-aheads](governance/10-roles-and-go-aheads.md).

| Role | Side | What they do | What they decide or write |
|---|---|---|---|
| **Client** — <client name> | the organisation the product is built for | names the product owner and the data protection contact | — |
| **Product owner** — <product owner> | client | owns the need; accepts each delivered increment | the production and budget go-aheads |
| **Data protection contact** — <data protection contact> | client | — | how personal data may enter the product |
| **Project lead** (lead developer) — <project lead> | the team | runs the project: sprints, tickets, technical choices, code review; the developers' first contact | the sprints; the design decisions |
| **Developers** — <developers> | the team | build the product with Claude Code, each in their own repository ("team member" = the project lead or a developer) | the implementation of their tickets; their own journal entries and pending records |
| **Project Advisor** — <Project Advisor> | outside the team; the method's author | two hours of meeting and two hours of preparation a week; feedback and advice | nothing in the project — the method and the kits only |
| **Claude sessions** | in every repository | propose, measure, write, test | nothing; they act on a go-ahead |

**Never open Claude Code in `<pm-repo>`.** A session opened here loads the Project Advisor's
kit and acts in his name (it writes his cockpit, it closes decisions). Your own kit, with
its guard rails, is in your sandbox or in a product repository; from there its skills
`session-close` and `decision-record` push your journal entries and your new 🔴 records into
`<pm-repo>`; the project lead's sessions also push `planning/sprints/`.

## Repositories

| Repository | What it is for | Who writes in it | Who reads it | Why it is separate |
|---|---|---|---|---|
| `gse-light` (public) | the method: the rules every session follows, the templates, the scripts, the two kits — cloned next to `<pm-repo>` as `../gse-light` | the method's author only; every session reads it, none changes it | everyone | public and reusable by other projects, so nothing of <Project name> or <client name> may appear in it — the leak guard (`check_docs.py`, with `private-terms.txt`) enforces it |
| `<pm-repo>` (private, this one) | the project's shared record: this instance in `instances/<instance>/` | each person their own part, through the kit's skills: the Project Advisor's sessions the cockpit, the minutes and his journal entries; the project lead the sprints; every team member their journal entries and new 🔴 records | everyone (the product owner on GitHub) | nobody manages the project from it; its sessions are the Project Advisor's; it is the project's **overall view** |
| `<project>-sandbox-<firstname>` (private, one per team member) | Day 0, `/upskilling` and experiments with the kit until the product repositories exist; the project lead's hosts the design phase | its owner | its owner, the project lead | throwaway — **not** a product repository, never audited, never listed below |
| product repositories (private, one or several) | the product's code, data jobs, infrastructure code, each with the kit — **to decide**: repository layout, the first decision of the design phase (W1); then listed here, one row each | the developers by pull request, the project lead reviews | the team | code is separate from project management: a session in a product repository writes into `<pm-repo>` only through the kit's skills |

This table is the project's **overall view**: once the repository layout is decided, list
each product repository here. The `delivery-auditor` agent — the read-only helper that
measures, before each meeting, what the team delivered (tickets, pull requests, gates,
journal entries) — audits those rows only; sandboxes are never audited.

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
from his sandbox:

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
  - [`QUICKSTART.md`](https://github.com/nicolasguelfi/gse-light/blob/main/QUICKSTART.md) — what gse-light does for you, which repositories you clone, the one install command of the kit, what to use at each moment of the project;
  - the reference design, chapter 15 — the start-of-project checklist;
  - the [roles record](governance/10-roles-and-go-aheads.md) — what you decide, which go-aheads you give;
  - the [design register](design/05-design-decisions.md) — the twelve decisions you open in W1.
- **Install**: your sandbox `<project>-sandbox-<firstname>` with the kit (created on GitHub
  by you or the Project Advisor; the one command, inside the clone:
  `../gse-light/claude-kit/install.sh <instance>`); in W1, the kit in each product
  repository named by the repository-layout decision.
- **Write**: `planning/sprints/` (one file per week, the tasks taken from the minutes), the
  drivers page `design/10-design-drivers.md` and the `DD` records of the design phase (kit
  skill `design-phase`, from your sandbox), your journal entries and new 🔴 records (kit
  skills `session-close`, `decision-record`); `CLAUDE.md`, gates and CI of each product
  repository.
- **Never**: open Claude Code in `<pm-repo>`; edit `BRIEFING.md`; turn 🟢 a record whose
  decider is someone else; promote to production or create cloud resources without the
  product owner's go-ahead.

### If you are a developer

- **Read first**:
  - [`QUICKSTART.md`](https://github.com/nicolasguelfi/gse-light/blob/main/QUICKSTART.md) — one page: what gse-light does for you, your sandbox, the one install command;
  - [`claude-kit/INSTALL.md`](https://github.com/nicolasguelfi/gse-light/blob/main/claude-kit/INSTALL.md) — clone the repositories side by side, `.env`, `check.sh`;
  - [`claude-kit/ONBOARDING.md`](https://github.com/nicolasguelfi/gse-light/blob/main/claude-kit/ONBOARDING.md) — who provides what, the method in one page, your first session step by step, the week's rhythm;
  - the [roles record](governance/10-roles-and-go-aheads.md).
- **Install**: your sandbox `<project>-sandbox-<firstname>` with the kit (the one command
  above), then `/upskilling` in your first session; later, clone the product repositories
  (the kit is already in them).
- **Write**: code by pull request in the product repositories; your journal entries and new
  🔴 records, through the kit skills `session-close` and `decision-record`, from your sandbox
  or a product repository.
- **Never**: open Claude Code in `<pm-repo>`; write directly in `instances/<instance>/`; push
  to a branch that deploys, or open a new flow of personal data, without the go-ahead the
  roles record names.

### If you are the product owner

- **Read**:
  - the vision `requirements/00-vision.md` — the need in five lines, yours to confirm;
  - the [requirements register](requirements/05-decisions.md) — the `DEC` records awaiting you;
  - the [roles record](governance/10-roles-and-go-aheads.md) §2 — the go-aheads you give: production, cloud resources, the budget;
  - the minutes of each meeting in [`meetings/`](meetings/README.md).
- **Install**: nothing — you read on GitHub.
- **Write**: nothing here — your decisions and go-aheads are recorded in your name, with the
  date, by the project lead's or the Project Advisor's sessions.

### If you are the Project Advisor

- **Read first**:
  - [`BRIEFING.md`](BRIEFING.md), your cockpit — §1 what awaits you, §1b what awaits the team, §2 what changed, §3 the state;
  - [the Project Advisor's page](https://github.com/nicolasguelfi/gse-light/blob/main/method/15-project-advisor.md) — where the Advisor steps in, the weekly meeting, what he does by default and does not.
- **Install**: the pm-kit in `<pm-repo>` ([`pm-kit/README.md`](https://github.com/nicolasguelfi/gse-light/blob/main/pm-kit/README.md))
  — done if you are reading this page in a created instance; the machine for recording and
  transcription ([`scripts/README.md`](https://github.com/nicolasguelfi/gse-light/blob/main/scripts/README.md)).
- **Write**: open Claude Code in `<pm-repo>` — the start hook says where the week stands —
  and say "go": your sessions write this page, `BRIEFING.md`, the meeting folders (brief,
  transcript, minutes validated by you), your journal entries, and the 🟢 of the records you
  decide (the method, the kits, your own spending).
- **Never**: write a sprint, a ticket or code; decide in the project (sprints, priorities,
  promotions, the client's budget); turn 🟢 a record whose decider is someone else.

## Folders

| Path | What it holds |
|---|---|
| [`BRIEFING.md`](BRIEFING.md) | Cockpit: §1 what awaits the Project Advisor, §1b the team, §2 changes, §3 state |
| [`governance/`](governance/) | Roles and go-aheads, project decisions (`PD-NN`), charter and risks once written |
| [`requirements/`](requirements/) | Vision, requirements decisions (`DEC-NNN`); `40-examples/` one file per real example (`EX-<AREA>-NNN-<short-name>.md`: `EX` example, `AREA` the short code of the part of the product, `NNN` its number — the identifier the requirements cite); `50-sources/<date>-<source>.md` one dated report per source — personal data stays out of git (the instance's data-regime record) |
| [`design/`](design/) | Design decisions (`DD-NN`), the drivers page and the design choices once the design phase runs |
| `planning/` | Roadmap and one file per week in `sprints/` (project lead) |
| [`meetings/`](meetings/README.md) | One folder per meeting (agenda, transcript, minutes, slides); presentations registry |
| [`journal/`](journal/README.md) | One entry per working session, `metrics.csv` — never rewritten |
| `private-terms.txt` | Terms the leak guard refuses in the public `gse-light` (client name, project name) |

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))
