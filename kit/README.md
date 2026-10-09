# The kit — one set of Claude files for the project's repository

Status: v0.2 · 2026-10-09 · one kit for every role, installed in the project's repository (board r11) · maintained by the Project Advisor

This folder is the **kit**: the files that make every Claude Code session in the project's
repository follow the method, kept here so a fix is made once and propagated everywhere.
One kit serves every role — the developers, the project lead and the Project Advisor open
Claude Code in the same repository, and the kit says what each one's session does. This page
is its map: for the Project Advisor who installs and refreshes it, the project lead and the
developers who receive it by cloning, the product owner who only needs to know what it
guarantees. Read your section (§1–§4), then the contents table (§5).

**Words used here** (every other term: [GLOSSARY.md](../GLOSSARY.md))

| Word | Meaning |
|---|---|
| **Project's repository** `<project-repo>` | the one repository of a project run with the method: the code, and in `project/` the project's shared record; private; everyone on the project clones it |
| **Project folder** `project/` | the shared record inside the project's repository — cockpit, registers, requirements, planning, meetings, journal, roles; created by the kit from a skeleton; everyone reads it, each person writes their own part |
| **Kit** | the files that make every Claude Code session in the project's repository follow the method — `CLAUDE.md`, twelve skills, four agents, permissions and the start hook, a `gates.sh` stub, two CI workflows, the `project/` skeleton — installed with one command, committed with the code |
| **Skill, agent** | a skill is a procedure Claude runs when asked (`/name`) or when the situation calls for it; an agent is a read-only helper Claude launches (a reviewer, an auditor) |
| **Design phase** | the step of W1 (the first project week) where the project lead, with Claude, turns the project's facts and constraints into twelve technical decisions (`DD` records), in order: repository layout, hosting, environments and promotion path, stack and language, data store, identity, infrastructure as code, continuous integration, test tools, secrets, dependency updates, monitoring — recorded with the skill `design-phase` |
| **Decision record and badges** | every `PD-NN`, `DEC-NNN` or `DD-NN` in these pages is one numbered decision record, with a status badge — 🔴 pending, 🟢 decided, 🟡 provisional; its *decider* (the person the roles record names) is the only one who turns it 🟢 |
| **Gates** | the project's automated checks (tests, lint, end-to-end) run by `gates.sh` and the CI before a merge; on Day 0 a stub that says "no gates yet" |
| **Cockpit** | `project/BRIEFING.md`, the Project Advisor's one-page dashboard — what awaits him, what awaits the team, what changed; written by his sessions only |
| **Start hook** | the small script run when a session opens in the project's repository; it prints who is working, the next meeting and, for the Project Advisor, his next step |
| **Sandbox** | a personal, private, throwaway repository a team member may create for experiments outside the project; optional, never audited |

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

## The repositories

| Repository | What it is for | Who writes in it | Who reads it | Why it is separate |
|---|---|---|---|---|
| `gse-light` (public) | the method: the rules every session follows, the templates, the scripts, this kit | the method's author only; every session reads it, none changes it | everyone | public and reusable by other projects, so nothing of a client may appear in it — the leak guard enforces it |
| `<project-repo>` (private, one per project) | the code, and in `project/` the shared record: cockpit, registers, requirements, planning, meetings, journal, roles; the kit is installed in it | each person their own part: the developers the code by pull request, their journal entries and new 🔴 records; the project lead the sprints, the design phase, the validation line of the minutes; the Project Advisor the cockpit, the briefs and draft minutes, `project/README.md`, the governance pages | everyone; the product owner on GitHub | one private repository per project: nothing to tell apart, every session finds the rules, the code and the record in one place |

## 1. If you are the Project Advisor

- **Read first**: [INSTALL.md §2](INSTALL.md#2-if-you-are-the-project-advisor--install-the-kit-once-and-refresh-it) — what the one command writes, the commit, the refresh; [the Project Advisor's page](../method/15-project-advisor.md) — your week.
- **Install**: the kit, **once**, in the project's repository, cloned next to `gse-light` (same parent folder); you install and refresh it because you own it:

  ```bash
  cd <project-repo>                                   # inside the project's clone
  ../gse-light/kit/install.sh                         # ONE command, no argument
  ```

  then fill `project/README.md`, the roles record and `project/private-terms.txt`, run `python3 ../gse-light/scripts/check_docs.py`, commit and push what it created. What the command does:
  - **overwritten on every run** (the kit owns them): skills, agents, the licence notice and `.claude/KIT_VERSION`;
  - **created only if absent** (the project's repository owns them after creation): `project/` (from the skeleton `templates/project/`, never touched once it has files), `CLAUDE.md`, `.claude/settings.json`, `gates.sh`, `.gitattributes`, `.env.example`, the two CI workflows (`gates.yml`, `docs.yml`) and the `.gitignore` entries;
  - **`KIT_VERSION`**: the last `gse-light` commit that touched `kit/`;
  - **refresh** after the kit changes: `git pull` in `gse-light`, then the same command; it warns when a template changed since the recorded `KIT_VERSION` and prints the exact `git diff` command so you can carry the change over by hand.
- **Your sessions**: open Claude Code in the project's repository — the start hook prints the situation (today, next meeting, next step) — and say "go". The `advisor` skill does the step and asks you only what only you know, one short multiple-choice question (QCM) at a time, or a review board (skill `review`) when the choice is complex: `meeting brief` the day before, `record` or `import` on the day, `transcribe`, `minutes` (your feedback section; the project lead validates and sends them), `decision-record`, `session-close`.
- **Write**: the cockpit `project/BRIEFING.md` — the team's rules deny the Edit tool on it, yours allow it: once on your machine, `cp .claude/roles/advisor.json .claude/settings.local.json` (never committed) —, the briefs and draft minutes, `project/README.md`, the governance pages, your journal entries, the 🟢 of the records you decide; the method and this kit, **here**, in `gse-light` — never with a client or project term in it (the leak guard refuses it).
- **Check**: after any kit change, replay [TEST-DAY0.md](TEST-DAY0.md).
- **Never**: write a sprint, a ticket or code; decide in the project (the roles record names who does); turn 🟢 a record whose decider is someone else; edit the kit's own files in the project's repository (they are changed here and overwritten at the next refresh).

## 2. If you are the project lead

- **Read first**: [QUICKSTART.md](../QUICKSTART.md) — the numbered path from zero to your first session, who does each step; then [INSTALL.md §3](INSTALL.md#3-if-you-are-the-project-lead-or-a-developer--clone-env-check-first-session) and [ONBOARDING.md §2](ONBOARDING.md#2-if-you-are-the-project-lead).
- **Install**: nothing — the kit comes with the clone; three personal steps (`.env`, `check.sh`, `claude`).
- **Write**: the sprints `project/planning/sprints/`; in W1 the drivers page and the twelve `DD` records (skill `design-phase`); then `gates.sh`, the CI and the `<…>` fields of `CLAUDE.md` from those decisions; your journal entries and new 🔴 records; the validation line of each meeting's minutes; the review of every pull request.
- **Never**: edit `project/BRIEFING.md` or anything under `../gse-light`; run `install.sh` (the Project Advisor does); turn a record 🟢 unless the roles record names you its decider; run the Advisor's skills.

## 3. If you are a developer

- **Read first**: [QUICKSTART.md](../QUICKSTART.md) — the numbered path; then [INSTALL.md §3](INSTALL.md#3-if-you-are-the-project-lead-or-a-developer--clone-env-check-first-session) and [ONBOARDING.md](ONBOARDING.md) — the method in one page, your first session, the Day-0 checklist; to rehearse Day 0 on your own machine first: [TEST-DAY0.md](TEST-DAY0.md).
- **Install**: nothing — the kit comes with the clone, then `.env`, `check.sh`, `claude`.
- **Write**: the code, by pull request on a feature branch with its tests; your journal entries and your new 🔴 records (skills `session-close` and `decision-record`).
- **Never**: run `install.sh`; edit `project/BRIEFING.md` or `../gse-light`; put a secret in a file under git; push to `main` without the go-ahead.

## 4. If you are the product owner

- **Install**: nothing — nothing to run, no Claude Code licence needed.
- **What the kit guarantees you**: every change comes with its tests; nothing reaches production and nothing is spent without the go-ahead the roles record gives you; every decision that awaits you is a 🔴 record in `project/`.
- **Read**: the project's repository on GitHub, `project/README.md` first, then the dashboard at the top of each register. The rest of this page is for the team.

## 5. Contents

| Path | What it is | Installed as |
|---|---|---|
| [`INSTALL.md`](INSTALL.md) | **How the kit gets in**: the Project Advisor with one command (and commit), everyone else by cloning; shared vs personal files; prerequisites macOS / Windows; what `check.sh` says | read, not installed |
| [`ONBOARDING.md`](ONBOARDING.md) | **Starting guide for the team**: who provides what, the method in one page, a section per role, the first session step by step, the week's rhythm, checklists | read, not installed |
| [`TEST-DAY0.md`](TEST-DAY0.md) | Rehearse Day 0 on your own machine, by role, in a throwaway folder: the Project Advisor's install and meeting chain, a team member's clone and check; about 15 minutes for the commands, plus the interactive sessions | read, not installed |
| [`TEST-DAY0-fast.txt`](TEST-DAY0-fast.txt) | The same rehearsal as four blocks to copy and paste (reset, Project Advisor, team member, project lead) | read, not installed |
| [`install.sh`](install.sh) | Installs or refreshes the kit; run by the Project Advisor from inside the project's repository: `../gse-light/kit/install.sh` | run from the project's repository |
| [`check.sh`](check.sh) | Day-0 check anyone runs from inside the project's repository (read-only); compares `KIT_VERSION` with the last `gse-light` commit that touched `kit/` and says whether the kit here is behind or your clone of `gse-light` is | run from the project's repository |
| [`templates/CLAUDE.md`](templates/CLAUDE.md) | Instructions file of the project's repository: the rules every session follows, then a section per kind of session (a team member's, the Project Advisor's); `<repository name>` substituted at install, the `<…>` fields (purpose, commands) filled after the design phase | `CLAUDE.md` (created once, then owned by the project's repository) |
| [`templates/settings.json`](templates/settings.json) | Shared Claude Code permissions and the start hook: `../gse-light` as additional directory; read-only commands, the gates, the checks and the situation allowed; the Edit tool denied under `../gse-light/` and on `project/BRIEFING.md`; the literal `git push origin main` denied, any other `git push` asked — conveniences, not a security boundary | `.claude/settings.json` (created once) |
| [`templates/env.example`](templates/env.example) | Local secrets and settings: the product's keys (one variable per vendor) and, on the Project Advisor's machine only, the keys and settings of the method's scripts (paid models, recording, transcription) | `.env.example` (created once; `.env` is never committed) |
| [`templates/gates.sh`](templates/gates.sh) | Day-0 stub of the gates: prints *no gates yet: design phase in progress* and exits 0; filled from the continuous integration and test tools decisions (the eighth and ninth of the twelve) | `gates.sh` (created once, executable) |
| [`templates/ci-gates.yml`](templates/ci-gates.yml) | CI workflow that runs `bash ./gates.sh` on every pull request and on every push to `main` | `.github/workflows/gates.yml` (created once) |
| [`templates/ci-docs.yml`](templates/ci-docs.yml) | CI workflow that runs the documentation checks of `project/` (`check_docs`) with `gse-light` checked out at the installed `KIT_VERSION` | `.github/workflows/docs.yml` (created once) |
| [`templates/gitattributes`](templates/gitattributes) | `*.sh text eol=lf`: shell scripts keep Unix line endings on a Windows clone | `.gitattributes` (created once) |
| [`templates/KIT_LICENSE.md`](templates/KIT_LICENSE.md) | Licence notice that travels with the kit | `.claude/KIT_LICENSE.md` (refreshed) |
| [`templates/project/`](templates/project/) | Skeleton of the project folder: `README.md` (the project, its phase, its people), `BRIEFING.md` (§1, §1b, §2, §3 with the counts line), the three registers with their §0 dashboards, the roles record `governance/10-roles-and-go-aheads.md`, `journal/README.md`, `journal/metrics.csv`, `meetings/README.md` | `project/` (copied once, when the folder is empty) |
| [`skills/design-phase/`](skills/design-phase/SKILL.md) | W1: the project's drivers → `DD` records (the twelve decisions of *Words used here*, in order) → `gates.sh`, CI and `CLAUDE.md` placeholders filled | `.claude/skills/design-phase/` (refreshed) |
| [`skills/decision-record/`](skills/decision-record/SKILL.md) | Record a decision in the right register of `project/`; commits that record only | `.claude/skills/decision-record/` (refreshed) |
| [`skills/review/`](skills/review/SKILL.md) | How Claude asks you to answer, choose, validate or decide: a short multiple-choice question for a simple point, a review board for the rest — the problem restated, every option's advantages, drawbacks and consequences, a comment under every point and a global one; your answer in one line | `.claude/skills/review/` (refreshed) |
| [`skills/session-close/`](skills/session-close/SKILL.md) | Journal entry, metrics, hand-over in `project/journal/`; commits those paths only | `.claude/skills/session-close/` (refreshed) |
| [`skills/verify-claim/`](skills/verify-claim/SKILL.md) | Measure before asserting | `.claude/skills/verify-claim/` (refreshed) |
| [`skills/upskilling/`](skills/upskilling/SKILL.md) | Personal coach: where you start, what your responsibilities need, a short plan, the method in two steps ([method](../method/20-upskilling.md)) | `.claude/skills/upskilling/` (refreshed) |
| [`skills/advisor/`](skills/advisor/SKILL.md) | The Project Advisor's single entry point: where the week stands (`scripts/situation.py`), the next step done by orchestrating the other skills and agents | `.claude/skills/advisor/` (refreshed; the Advisor's) |
| [`skills/meeting/`](skills/meeting/SKILL.md) | The weekly meeting chain: brief, record or import, transcribe, minutes — one folder per meeting under `project/meetings/<date>/` | `.claude/skills/meeting/` (refreshed; the Advisor's) |
| [`skills/slides/`](skills/slides/SKILL.md) | A presentation as a claude.ai artifact, sources kept under `project/meetings/<date>/slides/` | `.claude/skills/slides/` (refreshed; the Advisor's) |
| [`skills/cockpit-update/`](skills/cockpit-update/SKILL.md) | Refresh the cockpit `project/BRIEFING.md` | `.claude/skills/cockpit-update/` (refreshed; the Advisor's) |
| [`skills/method-lesson/`](skills/method-lesson/SKILL.md) | One lesson, one place, dated — in `CLAUDE.md`, a skill, a template or the method | `.claude/skills/method-lesson/` (refreshed; the Advisor's) |
| [`skills/genai-onboarding/`](skills/genai-onboarding/SKILL.md) | Prepare one person's arrival: a cover note, the Advisor's to-do, the Day-0 verification from their first journal entry | `.claude/skills/genai-onboarding/` (refreshed; the Advisor's) |
| [`agents/change-reviewer.md`](agents/change-reviewer.md) | Reviews a change against the reference design and the project's `DD` records; run before a pull request | `.claude/agents/change-reviewer.md` (refreshed) |
| [`agents/delivery-auditor.md`](agents/delivery-auditor.md) | Measures what the team delivered since the last meeting, for the Advisor's brief | `.claude/agents/delivery-auditor.md` (refreshed; the Advisor's) |
| [`agents/minutes-verifier.md`](agents/minutes-verifier.md) | Every task of the minutes backed by the transcript | `.claude/agents/minutes-verifier.md` (refreshed; the Advisor's) |
| [`agents/design-reviewer.md`](agents/design-reviewer.md) | Consistency of a documentation change in `project/` or in the method | `.claude/agents/design-reviewer.md` (refreshed; the Advisor's) |

The Advisor's skills and agents check `git config user.name` against the "Project Advisor"
row of the roles record and stop for anyone else. The kit targets **Claude Code only**; with
another coding agent the rules still apply, the kit does not install itself there.

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))
