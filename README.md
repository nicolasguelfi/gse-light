# gse-light — project management with generative AI

This page is the entry of the `gse-light` repository: a light method for running software
projects built with generative AI (Claude Code) as a working partner, with a **Project
Advisor** who gives feedback and advice in two hours of meeting and two hours of preparation
a week. It is for everyone on such a project: read the common part below, then the section
of your role — what you read first, what you install, what you write, what you never do.
The `gse-light` repository holds the method and its tools, **no project**: each project
keeps its own management in a private repository cloned next to it. Author: Nicolas Guelfi,
for [right-on-skill](https://rightonskill.odoo.com/). New to generative software engineering? Keep [GLOSSARY.md](GLOSSARY.md) open. Looking for what exists? [ARTEFACTS.md](ARTEFACTS.md) is the catalogue: every artefact by type, what it does, who uses it, where it lives.

**Words used here** (every other term: [GLOSSARY.md](GLOSSARY.md))

| Word | Meaning |
|---|---|
| **Project-management repository** `<pm-repo>` | the project's shared record — decisions, requirements, plans, minutes, journal — private, one per project. Everyone reads it; each person writes their own part in it through the kit's skills; nobody manages the project from it |
| **Instance** | one project run with the method, and its folder `instances/<instance>/` in `<pm-repo>` |
| **Product repository** `<product-repo>` | the code, private, one or several (repository layout, the first design decision); the kit is committed in it |
| **Sandbox** | a personal, private, throwaway repository `<project>-sandbox-<firstname>` with the kit, for Day 0 (each person's first hour on the project) and experiments until the product repositories exist; the project lead's sandbox hosts the design phase |
| **Placeholders** `<instance>`, `<pm-repo>`, `<product-repo>`, `<project>`, `<firstname>` | stand for the project's real names; `<instance>` is the folder name under `instances/` (`ls ../<pm-repo>/instances` shows it; the project lead gives it) |
| **Kit** | the files that make every Claude Code session in a repository follow the method — `CLAUDE.md`, five skills, one agent, permissions, a `gates.sh` stub, a CI workflow — installed with one command, committed with the code. Two kits: `claude-kit` for product and sandbox repositories, `pm-kit` for the Project Advisor in `<pm-repo>` |
| **Skill, agent** | a skill is a procedure Claude runs when asked (`/name`); an agent is a read-only helper Claude launches |
| **Register** | one document per kind of decision — project `PD`, requirements `DEC`, design `DD` — one numbered record per decision, a dashboard at the top |
| **Decision record and badges** | every `PD-NN`, `DEC-NNN` or `DD-NN` in these pages is one numbered decision record, with a status badge: 🔴 pending, 🟢 decided, 🟡 provisional; its *decider* is the person the roles record names for it, the only one who turns it 🟢 |
| **Design phase** | the step of W1 (the project's first week) where the project lead, with Claude, turns the project's facts and constraints into twelve technical decisions, `DD` records (the list is below, in "What the method fixes") |
| **Reference design** | the method's page of rules for building, testing, delivering and running a product |

<!-- who-is-who:start -->
**Who is who** — who decides what in a given project: its **roles record**, `<pm-repo>/instances/<instance>/governance/10-roles-and-go-aheads.md`.

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

| Repository | What it is for | Who writes in it | Who reads it | Why it is separate |
|---|---|---|---|---|
| `gse-light` (this one, public) | the method: the rules every session follows, the templates, the scripts, the two kits | the method's author only; every session reads it, none changes it | everyone | public and reusable by other projects, so nothing of a client may appear in it — the **leak guard** (the check `check_docs.py` that no private name of the client or project reaches `gse-light`, in files or commit messages) enforces it |
| `<pm-repo>` — the project-management repository (private, one per project) | the project's shared record, in `instances/<instance>/`: cockpit, registers, requirements, planning, meetings, journal | each person their own part, through the kit's skills: the developers their journal entries and 🔴 records, the project lead the sprints, the Advisor the cockpit and the minutes | everyone | one private record per project, apart from the public method and from the code; nobody manages the project from it — the Advisor's sessions run there, nobody else's |
| a sandbox `<project>-sandbox-<firstname>` (private, throwaway) | Day 0, `/upskilling` and experiments with the kit until the product repositories exist; the project lead's sandbox hosts the design phase | its owner, one per team member | its owner; the Advisor on request | personal and throwaway: nothing in it is the product; it stands in for a product repository until one exists |
| the product repositories `<product-repo>` (private, one or several) | the code, data jobs, infrastructure code, each with the kit | the developers by pull request, the project lead reviews | the team | code is separate from project management: a session in a product repository writes into `<pm-repo>` only through the kit's skills |

## If you are the project lead

- **Read first**:
  - [the Project Advisor's page](method/15-project-advisor.md) — who is in the project, the weeks and where the Advisor steps in, the weekly meeting;
  - the [reference design](method/00-reference-design.md), its common chapters (above) plus chapter 15 (the start-of-project checklist);
  - [`claude-kit/INSTALL.md`](claude-kit/INSTALL.md), its project-lead section — the kit in a product repository.
- **Install**: the kit in your sandbox, then once in each product repository, one command each time — [QUICKSTART.md](QUICKSTART.md), your section.
- **Write**: the sprints, `<pm-repo>/instances/<instance>/planning/sprints/`; the twelve `DD` records of the design phase, from your sandbox (kit skill `design-phase`); `gates.sh`, the CI and `CLAUDE.md` of each product repository; the review of every pull request.
- **Never**: open Claude Code in `<pm-repo>` (a session opened there acts in the Advisor's name); turn a record 🟢 unless the roles record names you its decider; let a decision live only in a chat or a ticket.

## If you are a developer

- **Read first**:
  - [QUICKSTART.md](QUICKSTART.md) — what gse-light does for you, your Day 0, what to use at each moment of the project, one page;
  - then [`claude-kit/INSTALL.md`](claude-kit/INSTALL.md) — prerequisites, clone, `.env`, `check.sh`, Windows, troubleshooting;
  - then [`claude-kit/ONBOARDING.md`](claude-kit/ONBOARDING.md) — the words used, the method in one page, your first session step by step, the Day-0 and first-sprint checklists;
  - then the reference design's common chapters (above).
- **Install**: the kit in your sandbox, one command; in a product repository nothing — the kit is already there, you copy `.env.example` to `.env` and run `check.sh`.
- **Write**: the code, by pull request on a feature branch with its tests; your journal entry at the end of each session and your new 🔴 records — the kit's skills `session-close` and `decision-record` push them into `<pm-repo>` for you.
- **Never**: open Claude Code in `<pm-repo>`; edit `gse-light` from a project session; push to `main` or to any branch that deploys without the go-ahead (the written yes of the person who holds that right, named in the roles record); commit a secret.

## If you are the product owner

- **Read**: `<pm-repo>/instances/<instance>/README.md` — the project, its phase, its people — and the dashboard at the top of each register (`governance/05-project-decisions.md`, `requirements/05-decisions.md`, `design/05-design-decisions.md`): the 🔴 records that await you.
- **Install**: nothing, and nothing to clone — you read on GitHub.
- **Write**: nothing by hand — your decisions and go-aheads are recorded by the team (skill `decision-record`) and in the meeting minutes.
- **Never**: decide in a chat or a mail only — a decision that is not in a register does not exist for the project.

## If you are the Project Advisor

- **Read first**:
  - [`pm-kit/README.md`](pm-kit/README.md) — create `<pm-repo>` and install the pm-kit, one command;
  - then [the Project Advisor's page](method/15-project-advisor.md) — your week: the brief, the meeting, the minutes, what you do by default and do not;
  - your machine: [`scripts/README.md`](scripts/README.md).
- **Install**: the pm-kit in `<pm-repo>`; your sessions run there, with the product repositories as additional directories for the overall view.
- **Write**: the cockpit `BRIEFING.md` (your one-page dashboard in the instance — what awaits you, what awaits the team, what changed; written by your sessions only), the meeting briefs and the draft minutes with your feedback section (the project lead validates and sends them), your journal, the method in `gse-light`.
- **Never**: decide in the project (you give feedback and advice; the deciders are in the roles record); write a client or project name in `gse-light` (the leak guard refuses it); write in a team member's name.

## Layout

| Folder | What it holds |
|---|---|
| [`method/`](method/) | [Reference design](method/00-reference-design.md) (rules as invariants, "how to choose" drivers), [the Project Advisor's page](method/15-project-advisor.md), [upskilling](method/20-upskilling.md), [tool landscape — examples](method/40-tool-landscape-examples.md) (dated, non-normative) |
| [`GLOSSARY.md`](GLOSSARY.md) | Every term and acronym of the method in plain words, grouped by theme, for newcomers |
| [`ARTEFACTS.md`](ARTEFACTS.md) | The catalogue: every artefact by type — method pages, templates, scripts, the two kits (skills, agents, installed files, tests), the claude.ai artefacts — with what it does, who uses it, where it lives and where it is installed; `check_docs` keeps it complete |
| [`templates/`](templates/) | Decision record, design drivers, example record, requirement record, journal entry, meeting agenda and minutes, skills grid, slide deck, artifact shortcut |
| [`scripts/`](scripts/) | `check_docs.py` (links, registers, kit copies, leak guard), `situation.py` and the session-start hook, `llm_call.py` (paid models, costs logged), `meeting/` (record, transcribe) — run from a project-management repository; preparing a machine (environment outside synced folders, ffmpeg, transcription): [`scripts/README.md`](scripts/README.md) |
| [`pm-kit/`](pm-kit/README.md) | The Project Advisor's Claude artefacts for a project-management repository: skills `advisor` (single entry point), `meeting`, `slides`, `method-lesson`, `decision-record`, `cockpit-update`, `session-close`, `genai-onboarding`; agents `delivery-auditor`, `minutes-verifier`, `design-reviewer` |
| [`claude-kit/`](claude-kit/README.md) | The Claude artefacts for each product repository (and each sandbox): skills `decision-record`, `design-phase`, `session-close`, `upskilling`, `verify-claim`; agent `change-reviewer` |

## Rules that hold everywhere

1. **Every decision and every open question goes into a register** of its instance, never
   scattered in a document. Registers share one format (see [`templates/decision-record.md`](templates/decision-record.md)).
2. **Plain words first, technical words second**, in every document.
3. **Evaluate is not execute**: a request to assess changes nothing; an action needs an
   explicit go-ahead.
4. **Measure before asserting**: a claim about the state of a system is backed by a
   command anyone can rerun.

## What the method fixes, what each project chooses

- **Design phase (first week)**: the team collects its drivers (facts and constraints) and decides its technology in `DD` records with the kit skill `design-phase` — twelve decisions, in order: repository layout, hosting, environments and promotion path, stack and language, data store, identity, infrastructure as code, continuous integration, test tools, secrets, dependency updates, monitoring; the method's rules name no tool.
- **Sandbox first**: until the product repositories exist (repository layout is the first decision), each team member works in their sandbox with the kit installed: Day 0, `/upskilling` (the kit's self-assessment skill of your starting level, with a personal plan), experiments; the project lead's sandbox hosts the design phase. A team member never opens Claude Code in `<pm-repo>`.
- **Tool landscape**: [`method/40-tool-landscape-examples.md`](method/40-tool-landscape-examples.md) lists options seen in past projects, dated and non-normative — illustrations, never defaults.
- **Firm rule**: end-to-end tests go through the real user interface and simulate the use cases, run by Claude, for verification and validation; the tool is the project's choice (Playwright is one example).
- **Prerequisite of the tooling**: GitHub (`gh`, pull requests, issues, CI workflows); another forge needs an adapted agent.
- **Multi-repository products**: the repository layout is a design decision; the kit is installed in each product repository, and the instance `README.md` in `<pm-repo>` lists them for the overall view.

Status: v0.7 · 2026-10-08 · entry page by role (Who is who, the repositories, one section per role); rules as invariants, technology chosen per project, sandbox repositories before the product repositories

## Licence

© 2026 [right-on-skill](https://rightonskill.odoo.com/); author Nicolas Guelfi. Source-available for **non-commercial use**, with **attribution**:
documents under [CC BY-NC 4.0](LICENSES/CC-BY-NC-4.0.txt), code under the
[PolyForm Noncommercial License 1.0.0](LICENSES/LicenseRef-PolyForm-Noncommercial-1.0.0.md).
Cite *Nicolas Guelfi, gse-light, 2026, https://github.com/nicolasguelfi/gse-light*
([`CITATION.cff`](CITATION.cff)); commercial use needs a separate licence from right-on-skill.
Details: [`LICENSE.md`](LICENSE.md).