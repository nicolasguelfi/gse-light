# gse-light — project management with generative AI

This page is the entry of the `gse-light` repository: a light method for running software
projects built with generative AI (Claude Code) as a working partner, with a **Project
Advisor** who gives feedback and advice in two hours of meeting and two hours of preparation
a week. It is for everyone on such a project: read the common part below, then the section
of your role — what you read first, what you install, what you write, what you never do.
The `gse-light` repository holds the method and its tools, **no project**: each project
lives in its own private repository, cloned next to this one — its code and, in a folder
`project/`, its shared record. Author: Nicolas Guelfi,
for [right-on-skill](https://rightonskill.odoo.com/). New to generative software engineering? Keep [GLOSSARY.md](GLOSSARY.md) open. Looking for what exists? [ARTEFACTS.md](ARTEFACTS.md) is the catalogue: every artefact by type, what it does, who uses it, where it lives.

**Words used here** (every other term: [GLOSSARY.md](GLOSSARY.md))

| Word | Meaning |
|---|---|
| **Project's repository** `<project-repo>` | the one private git repository of a project: its code, and its shared record in `project/`. Everyone works in it; nobody manages the project from anywhere else |
| **Project folder** `project/` | the shared record inside the project's repository — cockpit, registers, requirements, planning, meetings, journal, the roles record. Everyone reads it; each person writes their own part through the kit's skills |
| **Instance** | one project run with the method; its files are the project's repository |
| **Sandbox** | optional: a personal, private, throwaway repository `<project>-sandbox-<firstname>` for experiments outside the project; nothing of value stays there |
| **Placeholders** `<project-repo>`, `<project>`, `<firstname>` | stand for the project's real names: the repository, the project's short name (also the parent folder `~/dev/<project>`), a person's first name |
| **Kit** | the files that make every Claude Code session in the project's repository follow the method — `CLAUDE.md`, twelve skills, four agents, permissions, a start hook, a `gates.sh` stub, two CI workflows, the `project/` skeleton — installed with one command by the Project Advisor, committed with the code; everyone else gets it by cloning |
| **Skill, agent** | a skill is a procedure Claude runs when asked (`/name`) or by rule; an agent is a read-only helper Claude launches |
| **Register** | one document per kind of decision — project `PD`, requirements `DEC`, design `DD` — one numbered record per decision, a dashboard at the top |
| **Decision record and badges** | every `PD-NN`, `DEC-NNN` or `DD-NN` in these pages is one numbered decision record, with a status badge: 🔴 pending, 🟢 decided, 🟡 provisional; its *decider* is the person the roles record names for it, the only one who turns it 🟢 |
| **Design phase** | the step of W1 (the project's first week) where the project lead, with Claude, turns the project's facts and constraints into twelve technical decisions, `DD` records (the list is below, in "What the method fixes") |
| **Reference design** | the method's page of rules for building, testing, delivering and running a product |

<!-- who-is-who:start -->
**Who is who** — who decides what in a given project: its **roles record**, `project/governance/10-roles-and-go-aheads.md`.

| Role | Side | What they do | What they decide or write |
|---|---|---|---|
| **Client** | the organisation the product is built for | names the product owner and the data protection contact | — |
| **Product owner** | client | owns the need; accepts each delivered increment | the production and budget go-aheads |
| **Data protection contact** | client | — | how personal data may enter the product |
| **Project lead** (lead developer) | the team | runs the project: sprints, tickets, technical choices, code review; the developers' first contact | the sprints; the design decisions |
| **Developers** | the team | build the product with Claude Code, each in their own repository ("team member" = the project lead or a developer) | the implementation of their tickets; their own journal entries and pending records |
| **Project Advisor** | outside the team; the method's author | two hours of meeting and two hours of preparation a week; feedback and advice | nothing in the project — the method and the kits only |
| **Claude sessions** | in every repository | propose, measure, write, test | nothing; they act on a go-ahead |
<!-- who-is-who:end -->

One reading path for everyone: the [reference design](method/00-reference-design.md), chapters
0 (purpose and how to read it), 1 (principles), 2 (how people and AI share the decisions) and
13 (working with the AI day to day); the project lead adds chapter 15 (the start-of-project checklist).

## The repositories

Two clones, side by side in one parent folder, for every person who works on the project.

| Repository | What it is for | Who writes in it | Who reads it | Why it is separate |
|---|---|---|---|---|
| `gse-light` (this one, public) | the method: the rules every session follows, the templates, the scripts, the kit | the method's author only; every session reads it, none changes it | everyone | public and reusable by other projects, so nothing of a client may appear in it — the **leak guard** (the check `check_docs.py` that no private name of the client or project reaches `gse-light`, in files or commit messages) enforces it |
| `<project-repo>` — the project's repository (private, one per project) | the code, and the shared record in `project/`: cockpit, registers, requirements, planning, meetings, journal; the kit is committed in it | each person their own part: the developers their code by pull request, their journal entries and 🔴 records; the project lead the sprints and the design decisions; the Advisor the cockpit, the briefs and the draft minutes | everyone; the product owner on GitHub | one private repository per project: code and record together, so a decision and the code that follows it travel in the same pull request; the roles record says who hosts it and how `main` is protected |

A **sandbox** `<project>-sandbox-<firstname>` is optional: a personal, private, throwaway repository for experiments outside the project, created by its owner; nothing of value stays there.

## If you are the project lead

- **Read first**:
  - [the Project Advisor's page](method/15-project-advisor.md) — who is in the project, the weeks and where the Advisor steps in, the weekly meeting;
  - the [reference design](method/00-reference-design.md), its common chapters (above) plus chapter 15 (the start-of-project checklist);
  - [QUICKSTART.md](QUICKSTART.md), your section — what you add to a developer's path.
- **Install**: nothing — the Advisor installs the kit in the project's repository and refreshes it; you get it by cloning, like every developer ([QUICKSTART.md](QUICKSTART.md), the numbered path).
- **Write**: the sprints, `project/planning/sprints/`; the twelve `DD` records of the design phase (kit skill `design-phase`), in W1; `gates.sh`, the CI and the `<…>` fields of `CLAUDE.md`; the review of every pull request; the validation line of the minutes.
- **Never**: turn a record 🟢 unless the roles record names you its decider; let a decision live only in a chat or a ticket; edit `project/BRIEFING.md` (the Advisor's cockpit).

## If you are a developer

- **Read first**:
  - [QUICKSTART.md](QUICKSTART.md) — what gse-light does for you, **the numbered path from zero to your first session** (who does each step), what to use at each moment of the project, one page;
  - then [`kit/INSTALL.md`](kit/INSTALL.md) — prerequisites, what is shared or personal, Windows, troubleshooting;
  - then [`kit/ONBOARDING.md`](kit/ONBOARDING.md) — the words used, the method in one page, your first session step by step, the Day-0 and first-sprint checklists;
  - then the reference design's common chapters (above).
- **Install**: nothing — the kit comes with the clone; you copy `.env.example` to `.env` and run `../gse-light/kit/check.sh`.
- **Write**: the code, by pull request on a feature branch with its tests; your journal entry at the end of each session and your new 🔴 records — the kit's skills `session-close` and `decision-record` write them into `project/` for you.
- **Never**: edit `gse-light` from a project session; edit `project/BRIEFING.md`; push to `main` or to any branch that deploys without the go-ahead (the written yes of the person who holds that right, named in the roles record); commit a secret.

## If you are the product owner

- **Read**: `project/README.md` — the project, its phase, its people — and the dashboard at the top of each register (`project/governance/05-project-decisions.md`, `project/requirements/05-decisions.md`, `project/design/05-design-decisions.md`): the 🔴 records that await you.
- **Install**: nothing, and nothing to clone — you read on GitHub, with the read access the host of the project's repository gives you (roles record).
- **Write**: nothing by hand — your decisions and go-aheads are recorded by the team (skill `decision-record`) and in the meeting minutes; your tasks are in the minutes, per participant.
- **Never**: decide in a chat or a mail only — a decision that is not in a register does not exist for the project.

## If you are the Project Advisor

- **Read first**:
  - [`kit/README.md`](kit/README.md) — the kit: what it installs, the one command, the refresh;
  - then [the Project Advisor's page](method/15-project-advisor.md) — your week: the brief, the meeting, the minutes, what you do by default and do not;
  - your machine: [`scripts/README.md`](scripts/README.md).
- **Install**: the kit in the project's repository, once, with one command run at its root (`../gse-light/kit/install.sh`), then commit; the same command refreshes it after every change of the kit. Your sessions open in that repository, like everyone's; your personal `.claude/settings.local.json` allows you the cockpit.
- **Write**: the cockpit `project/BRIEFING.md` (your one-page dashboard — what awaits you, what awaits the team, what changed; written by your sessions only), the meeting briefs and the draft minutes with your feedback section (the project lead validates and sends them), `project/README.md` and the governance pages, your journal, the method in `gse-light`.
- **Never**: decide in the project (you give feedback and advice; the deciders are in the roles record); write a client or project name in `gse-light` (the leak guard refuses it); write in a team member's name.

## Layout

| Folder | What it holds |
|---|---|
| [`method/`](method/) | [Reference design](method/00-reference-design.md) (rules as invariants, "how to choose" drivers), [the Project Advisor's page](method/15-project-advisor.md), [upskilling](method/20-upskilling.md), [tool landscape — examples](method/40-tool-landscape-examples.md) (dated, non-normative) |
| [`GLOSSARY.md`](GLOSSARY.md) | Every term and acronym of the method in plain words, grouped by theme, for newcomers |
| [`ARTEFACTS.md`](ARTEFACTS.md) | The catalogue: every artefact by type — method pages, templates, scripts, the kit (skills, agents, installed files, pages, rehearsals), the claude.ai pages — with what it does, who uses it, where it lives and where it is installed; `check_docs` keeps it complete |
| [`templates/`](templates/) | Decision record, design drivers, example record, requirement record, journal entry, meeting agenda and minutes, skills grid, slide deck, artifact shortcut |
| [`scripts/`](scripts/) | `check_docs.py` (links, registers, kit copy, leak guard), `situation.py` and the session-start hook, `llm_call.py` (paid models, costs logged), `meeting/` (record, transcribe) — run from the project's repository; preparing a machine (environment outside synced folders, ffmpeg, transcription): [`scripts/README.md`](scripts/README.md) |
| [`kit/`](kit/README.md) | The kit, one for every role: skills `advisor` (the Advisor's single entry point), `meeting`, `slides`, `cockpit-update`, `method-lesson`, `genai-onboarding`, `decision-record`, `design-phase`, `review`, `session-close`, `upskilling`, `verify-claim`; agents `change-reviewer`, `delivery-auditor`, `minutes-verifier`, `design-reviewer`; the templates it installs (`CLAUDE.md`, settings, `gates.sh`, CI, the `project/` skeleton); its pages (install, onboarding, Day-0 rehearsal) |

## Rules that hold everywhere

1. **Every decision and every open question goes into a register** of the project, never
   scattered in a document. Registers share one format (see [`templates/decision-record.md`](templates/decision-record.md)).
2. **Plain words first, technical words second**, in every document.
3. **Evaluate is not execute**: a request to assess changes nothing; an action needs an
   explicit go-ahead.
4. **Measure before asserting**: a claim about the state of a system is backed by a
   command anyone can rerun.

## What the method fixes, what each project chooses

- **Design phase (first week)**: the team collects its drivers (facts and constraints) and decides its technology in `DD` records with the kit skill `design-phase` — twelve decisions, in order: repository layout, hosting, environments and promotion path, stack and language, data store, identity, infrastructure as code, continuous integration, test tools, secrets, dependency updates, monitoring; the method's rules name no tool.
- **One repository per project**: the project's repository exists from the kick-off, with the kit; each team member's Day 0 (clone, `.env`, `check.sh`, first session, `/upskilling`) happens in it, on a personal branch `day0-<firstname>`. The repository layout `DD` says how the code is organised inside it (components as folders) — or, if the project really needs several repositories, which one holds `project/`.
- **Tool landscape**: [`method/40-tool-landscape-examples.md`](method/40-tool-landscape-examples.md) lists options seen in past projects, dated and non-normative — illustrations, never defaults.
- **Firm rule**: end-to-end tests go through the real user interface and simulate the use cases, run by Claude, for verification and validation; the tool is the project's choice (Playwright is one example).
- **Prerequisite of the tooling**: GitHub (`gh`, pull requests, issues, CI workflows); another forge needs an adapted agent.
- **Where the repository lives and how `main` is protected** is the project's decision, in its roles record: on a private repository owned by a personal GitHub account, collaborators always have write access and branch protection is not available; an organisation gives read-only access (the product owner) and protected branches.

Status: v0.8 · 2026-10-09 · one repository per project (board r11): the code and `project/` together, one kit for every role, two clones per person; entry page by role (Who is who, the repositories, one section per role); rules as invariants, technology chosen per project

## Licence

© 2026 [right-on-skill](https://rightonskill.odoo.com/); author Nicolas Guelfi. Source-available for **non-commercial use**, with **attribution**:
documents under [CC BY-NC 4.0](LICENSES/CC-BY-NC-4.0.txt), code under the
[PolyForm Noncommercial License 1.0.0](LICENSES/LicenseRef-PolyForm-Noncommercial-1.0.0.md).
Cite *Nicolas Guelfi, gse-light, 2026, https://github.com/nicolasguelfi/gse-light*
([`CITATION.cff`](CITATION.cff)); commercial use needs a separate licence from right-on-skill.
Details: [`LICENSE.md`](LICENSE.md).
