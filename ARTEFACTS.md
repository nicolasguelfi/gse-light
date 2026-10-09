# The catalogue — every artefact of gse-light, by type

Status: v0.4 · 2026-10-09 · one kit for every role, installed in the project's repository (board r11): the former §4 and §5 merged into one section, the pm-kit retired · 56 rows (method 8, templates 10, scripts 7, kit 29, claude.ai 2) · one row per artefact: what it does, who uses it, where it lives or is installed · `check_docs` verifies that every skill, agent, template and script in the folders has its row here

**What this page is.** The inventory of the method's artefacts, grouped by type, for anyone who
wants to know what exists and what each piece is for before opening it. The kit is the
artefact that travels into the project's repository; everything else is read in place. A
location written `…/x` is relative to the prefix given above its table.

**Words used here** (every other term: [GLOSSARY.md](GLOSSARY.md))

| Word | Meaning |
|---|---|
| **Skill** | a procedure Claude runs when asked (`/name`) or when the situation calls for it; a folder `skills/<name>/SKILL.md` |
| **Agent** | a read-only helper Claude launches for one job (a review, an audit, a check); a file `agents/<name>.md` |
| **Hook** | a script Claude Code runs by itself at a moment of the session (here: at session start) |
| **Template** | a document to copy and fill; it carries no licence obligation once filled |
| **Kit** | the files that make every Claude Code session in the project's repository follow the method; one kit for every role, installed by one command |
| **Project's repository, project folder** | the one private repository of a project — its code, and its shared record in `project/` (cockpit, registers, requirements, planning, meetings, journal) |
| **Review board** | an interactive page of proposals by subject — the problem restated, each option's advantages, drawbacks and consequences, a comment under every point — that the person ticks and sends back as one line; made by the `review` skill |
| **Register** | one file per kind of decision (project, requirements, design); every decision is a numbered section of that file, never a file of its own |
| **Installed in** | the place where a copy of the artefact ends up in the project's repository; "read in place" means it is only read from the `gse-light` clone |

## 1. The method — read in place

Where: in the `gse-light` clone.

| Artefact | What it does | Who uses it | Where |
|---|---|---|---|
| [`method/00-reference-design.md`](method/00-reference-design.md) | the method's rules for building, testing, delivering and running a product — rules as invariants, "how to choose" drivers, no tool names; approved v0.8 | everyone (chapters 0–2, 13); the project lead adds 15 (the start-of-project checklist) | `method/` |
| [`method/15-project-advisor.md`](method/15-project-advisor.md) | the Project Advisor's page: his role, the weekly meeting, where he steps in week by week; the source of the kick-off presentation | the Project Advisor, the project lead | `method/` |
| [`method/20-upskilling.md`](method/20-upskilling.md) | starting from the team's real levels: the skills round table, the personal plan, the `/upskilling` skill's principles | the Project Advisor, every team member | `method/` |
| [`method/40-tool-landscape-examples.md`](method/40-tool-landscape-examples.md) | tools seen in past projects, dated, non-normative — illustrations for the design phase, never defaults | the project lead in the design phase | `method/` |
| [`GLOSSARY.md`](GLOSSARY.md) | every term and acronym of the method in plain words, by theme | newcomers; every page links it | root |
| [`README.md`](README.md), [`QUICKSTART.md`](QUICKSTART.md) | the entry pages: what the method is, the two repositories each person clones, one section per role; the team members' one-page start with the numbered path from zero | everyone / the developers and the project lead | root |
| [`CLAUDE.md`](CLAUDE.md) | the rules every Claude session follows when it works **in** the `gse-light` repository (no client name, naming, readable layout, entry-document skeleton, asking the author) | the method's author's sessions | root |
| [`LICENSE.md`](LICENSE.md), [`CITATION.cff`](CITATION.cff), `REUSE.toml`, `LICENSES/` | the licence (CC BY-NC 4.0 for documents, PolyForm Noncommercial for code), how to cite, the SPDX inventory | anyone who reuses the method | root |

## 2. Templates — copied and filled in the project folder

Where: under `project/` of the project's repository.

| Artefact | What it does | Who uses it | Where |
|---|---|---|---|
| [`templates/decision-record.md`](templates/decision-record.md) | the format of **one** decision or open question: plain-language problem, what to consult, options with advantages and drawbacks, drivers, recommendation, status badge. Each record is a numbered section appended to its register file (`PD`, `DEC` or `DD`), never a file per decision; the register's §0 dashboard lists them | the `decision-record` skill, in the three registers | `governance/05-…`, `requirements/05-…`, `design/05-…` |
| [`templates/design-drivers.md`](templates/design-drivers.md) | the project's facts and constraints collected before the twelve design decisions | the `design-phase` skill, the project lead | `design/` |
| [`templates/example-record.md`](templates/example-record.md) | one real example of the need, `EX-<AREA>-NNN`, anonymised, cited by the requirements | the team, the product owner | `requirements/40-examples/` |
| [`templates/requirement-record.md`](templates/requirement-record.md) | one requirement, `FR-<AREA>-NNN` or `NFR-<AREA>-NNN`, linked to its examples and tests | the project lead, the developers | `requirements/` |
| [`templates/session-journal.md`](templates/session-journal.md) | one working session: what was done with its commands, decisions, what was not done, hand-over | the `session-close` skill, every role | `journal/` |
| [`templates/meeting-agenda.md`](templates/meeting-agenda.md) | the Project Advisor's brief for any meeting that is not a sprint meeting (kick-off, hand-over, ad hoc): kind and purpose, the topics in a proposed order with indicative durations (the project lead chairs and keeps time), decisions awaiting, points to raise | the `meeting` skill (`brief`, §1b) | `meetings/<date>/` |
| [`templates/sprint-agenda.md`](templates/sprint-agenda.md) | the Project Advisor's brief for the weekly sprint meeting: the same, plus the week's measured facts (`delivery-auditor`), the demo and the next sprint | the `meeting` skill (`brief`, §1) | `meetings/<date>/` |
| [`templates/meeting-minutes.md`](templates/meeting-minutes.md) | the minutes of any meeting that is not a sprint meeting: kind and purpose, source, speakers table, executive summary, decisions, actions until the next meeting with transcript timestamps (or `[notes <name>]`), the Advisor's feedback (optional, readable by the client), "validated by … on"; lines shared with `sprint-minutes.md` compared by `check_docs` | the `meeting` skill (`minutes`), `minutes-verifier` | `meetings/<date>/` |
| [`templates/sprint-minutes.md`](templates/sprint-minutes.md) | the minutes of the weekly sprint meeting: the same skeleton, plus the sprint review, the demo, the tasks for the next sprint per participant and the Advisor's feedback on the week's cycle | the `meeting` skill (`minutes`), `minutes-verifier` | `meetings/<date>/` |
| [`templates/skills-grid.md`](templates/skills-grid.md) | the skills round table: eight lines, levels 0–3, counts per level, no names | the Project Advisor at the kick-off | `governance/` |
| [`templates/artifact-open.html`](templates/artifact-open.html) | a shortcut that opens a claude.ai artifact (deck, review board) from the file explorer | the `slides` and `review` skills | `meetings/<date>/…/open.html` |
| [`templates/slides/`](templates/slides/) | the deck model: `deck.json` and six slide models (cover, marks, table, cards, statement, next), dark, numbered | the `slides` skill | `meetings/<date>/slides/` |

## 3. Scripts — run from the project's repository, read in place

Where: in the `gse-light` clone, run as `python3 ../gse-light/scripts/<name>` from the root of the project's repository.

| Artefact | What it does | Who uses it | Needs |
|---|---|---|---|
| [`scripts/check_docs.py`](scripts/check_docs.py) | the documentation gates: links and anchors, registers and cockpit counts, the kit copy in `.claude/`, the *Who is who* copies, the catalogue rows, the deck's freshness, the leak guard (no client term in `gse-light`, files and commit messages) | every session before a commit under `project/`; the CI workflow `docs.yml` | Python only |
| [`scripts/situation.py`](scripts/situation.py) | where the project stands this week: today, next meeting, next step of the meeting chain, from `project/meetings/` | the start hook, the `advisor` skill | Python only |
| [`scripts/session_start.py`](scripts/session_start.py) | the session-start hook: the repository, the git user and their role (matched against the roles record), the uncommitted files, the next meeting; for the Advisor also his tasks and the last hand-over | Claude Code, at every session opened in the project's repository | Python only |
| [`scripts/llm_call.py`](scripts/llm_call.py) | one paid model call (Gemini, or a text model through OpenRouter), cost estimated and logged in `project/journal/llm-costs.csv`; switches by itself to the repository's `.venv` | `transcribe.py`; the Project Advisor's sessions | the environment of [`scripts/README.md`](scripts/README.md) §1 |
| [`scripts/meeting/meeting.sh`](scripts/meeting/meeting.sh) | records the meeting with ffmpeg (macOS), or imports a file recorded elsewhere; `devices`, `start`, `status`, `stop`, `import`; folders under `project/meetings/<date>/` | the `meeting` skill (`record`, `import`) | `ffmpeg` |
| [`scripts/meeting/transcribe.py`](scripts/meeting/transcribe.py) | transcribes a recording, locally (mlx-whisper, whisper.cpp) or with Gemini; `transcript.md` with timestamps | the `meeting` skill (`transcribe`) | a local engine or a Gemini key |
| [`scripts/README.md`](scripts/README.md) | how to prepare a machine: environments in `~/.venvs/<name>` linked as `.venv`, ffmpeg, the transcription engine, `.env` | the Project Advisor; the rule holds for every team member's machine | — |

## 4. The kit `kit/` — installed in the project's repository, for every role

Installed by one command run at the root of the project's repository, `../gse-light/kit/install.sh`, by the Project Advisor; committed with the code; everyone else gets it by cloning. Where: in that repository.

| Artefact | What it does | Who uses it | Where |
|---|---|---|---|
| **Skills — every role** | | | `.claude/skills/<name>/` |
| [`decision-record`](kit/skills/decision-record/SKILL.md) | records a decision or an open question in the right register (`PD`, `DEC`, `DD`) in the standard format and updates the dashboard; commits the new 🔴 record | everyone, when a choice appears | |
| [`design-phase`](kit/skills/design-phase/SKILL.md) | runs the design phase in W1 with the project lead: the drivers, then the twelve decisions in order, each as a `DD` record; then fills `gates.sh`, the CI and `CLAUDE.md` | the project lead | |
| [`review`](kit/skills/review/SKILL.md) | how the session asks you anything — an answer, a choice, a validation, a go-ahead: a short multiple-choice question for a simple point, a review board for the rest; the problem restated, every option's advantages, drawbacks and consequences, a comment under every point and a global one; your answer in one line. Carries the generator `review_board.py` | every session, by rule, whenever the person must decide | |
| [`session-close`](kit/skills/session-close/SKILL.md) | closes a session: journal entry and metrics row in `project/journal/`, committed; a hand-over a session with no memory can resume from | everyone, at the end of every session | |
| [`upskilling`](kit/skills/upskilling/SKILL.md) | the personal coach: assesses where you stand, proposes a short plan of exercises, re-checks it later; its record stays on your machine | every team member, on Day 0 and when stuck | |
| [`verify-claim`](kit/skills/verify-claim/SKILL.md) | before stating anything about a system (version, counts, test results, cause), measures it and shows the command and its output | every session, by rule | |
| **Skills — the Project Advisor's** (they check the git user against the roles record and stop for anyone else) | | | `.claude/skills/<name>/` |
| [`advisor`](kit/skills/advisor/SKILL.md) | the single entry point of the Advisor's sessions: reads the situation, does the next step by orchestrating the other skills and agents, asks only what only he knows — a QCM, or a review board for a complex choice | the Project Advisor, on his first message | |
| [`meeting`](kit/skills/meeting/SKILL.md) | the weekly meeting chain: `brief` the day before (the topics in a proposed order; the project lead chairs and keeps time), `record` or `import` on the day, `transcribe`, `minutes` checked by `minutes-verifier`, validated and sent by the project lead | the Project Advisor | |
| [`cockpit-update`](kit/skills/cockpit-update/SKILL.md) | refreshes the cockpit `project/BRIEFING.md`: §1 what awaits the Advisor, §1b the team, §2 the delta, §3 the state and the pending counts | `session-close`, the Advisor's sessions | |
| [`genai-onboarding`](kit/skills/genai-onboarding/SKILL.md) | prepares one person's arrival: a cover note built on `ONBOARDING.md`, the Advisor's own to-do (licence, access), then verifies the Day-0 checklist from the first journal entry | the Project Advisor, before the kick-off and for late arrivals | |
| [`method-lesson`](kit/skills/method-lesson/SKILL.md) | turns something learned in a session into one dated lesson at the right place (`CLAUDE.md`, a skill, a template, the reference design, the kit template), propagated | the Advisor's sessions, as soon as a gap is named | |
| [`slides`](kit/skills/slides/SKILL.md) | makes, reopens, updates or exports a presentation as a claude.ai Slides artifact; sources in git, synced from the viewer before any change; the freshness check; the registry of links | the Project Advisor | |
| **Agents** | | | `.claude/agents/<name>.md` |
| [`change-reviewer`](kit/agents/change-reviewer.md) | reviews a diff or pull request against the reference design and the registers before it is merged — gates, data regime, secrets, migrations, documentation with the code | the developers, before a pull request | |
| [`delivery-auditor`](kit/agents/delivery-auditor.md) | read-only weekly audit for the brief: what the team delivered since the last meeting, measured (sprint file, pull requests, gates, journal, registers) | the `meeting` skill (`brief`) | |
| [`minutes-verifier`](kit/agents/minutes-verifier.md) | checks the minutes against the transcript: every task and decision backed by an excerpt at the cited timestamp | the `meeting` skill (`minutes`) | |
| [`design-reviewer`](kit/agents/design-reviewer.md) | reviews a change to the project folder's documents for consistency: contradictions, decisions outside a register, broken links, stale cockpit, unverified claims | the Advisor's sessions before a substantial documentation change | |
| **Files written by the install** (created once, then owned by the project's repository; the skills and agents are refreshed at every run) | | | |
| [`templates/CLAUDE.md`](kit/templates/CLAUDE.md) | the rules every session follows in the repository: the project folder `project/`, the standing rules (asking the person included), what each role's session does, the lessons, the commands; `<…>` fields filled by the design phase | every session in the repository | `CLAUDE.md` |
| [`templates/settings.json`](kit/templates/settings.json) | permissions: read access to `../gse-light`; the Edit tool denied under `../gse-light/**` and on `project/BRIEFING.md`; `git push origin main` denied; ask before any `git push`; the **session-start hook** that runs `scripts/session_start.py` | Claude Code | `.claude/settings.json` |
| [`templates/env.example`](kit/templates/env.example) | the personal secrets and settings to copy into `.env`, never committed: the product's keys; on the Advisor's machine also Google AI Studio, OpenRouter, the microphone, the transcription engine | everyone | `.env.example` |
| [`templates/gates.sh`](kit/templates/gates.sh) | the project's automated checks, run by the CI (`bash ./gates.sh`); on Day 0 a stub that says "no gates yet" | the CI, every session | `gates.sh` |
| [`templates/ci-gates.yml`](kit/templates/ci-gates.yml) | the CI workflow that runs `gates.sh` on every change; services and branches filled from the design decisions | GitHub Actions | `.github/workflows/gates.yml` |
| [`templates/ci-docs.yml`](kit/templates/ci-docs.yml) | the CI workflow that runs `check_docs.py` on every change, with `gse-light` checked out at the installed kit version | GitHub Actions | `.github/workflows/docs.yml` |
| [`templates/gitattributes`](kit/templates/gitattributes) | line endings: text normalised, shell scripts always LF (Windows) | git | `.gitattributes` |
| [`templates/KIT_LICENSE.md`](kit/templates/KIT_LICENSE.md) | the licence notice that travels with the kit | anyone who reads the repository | `.claude/KIT_LICENSE.md` |
| [`templates/project/`](kit/templates/project/) | the project folder's skeleton: `README.md` (people, the repository, calendar, start here by role), `BRIEFING.md` (the cockpit), the three registers with their dashboards, the roles record, `journal/` (README, `metrics.csv`), `meetings/README.md`; copied once, when `project/` is missing or empty | the Project Advisor when a project starts | `project/` |
| **Scripts and pages of the kit** | | | read in place |
| [`install.sh`](kit/install.sh) | writes the files above, fills the repository's name, records `KIT_VERSION` (the last `gse-light` commit that touched `kit/`); warns when a template changed since the recorded version | the Project Advisor, once per project and after every kit change | |
| [`check.sh`](kit/check.sh) | checks a machine and a clone line by line: prerequisites, the two sibling repositories, `project/`, the kit files, the start hook, the kit version, nothing personal in git | every team member on Day 0 and when something is odd | |
| [`README.md`](kit/README.md), [`INSTALL.md`](kit/INSTALL.md), [`ONBOARDING.md`](kit/ONBOARDING.md) | the kit's pages by role: what it is, how it is installed and refreshed, what is shared or personal, the first session step by step and the Day-0 checklists | everyone | |
| [`TEST-DAY0.md`](kit/TEST-DAY0.md), [`TEST-DAY0-fast.txt`](kit/TEST-DAY0-fast.txt) | the Day-0 rehearsal by role in a throwaway folder, and the same as blocks to paste | the Project Advisor, after any kit change | |

## 5. Published on claude.ai — decks and review boards, one folder per artefact in the project folder

Where: under `project/meetings/<date>/`, with a row in the registry `project/meetings/README.md`.

| Artefact | What it does | Who uses it | Where |
|---|---|---|---|
| A **deck** (Slides artifact) | a presentation for a meeting: dark, numbered slides, actor marks, a "Source" footer per slide so that `check_docs` warns when a source changed; made and synced by the `slides` skill | the Project Advisor | `slides/` (sources, `open.html`) |
| A **review board** | a page of proposals by subject with the problem restated, each option's advantages, drawbacks and consequences, a recommendation, a comment under every point and a global one; the person ticks and sends back one line; made by the `review` skill | any session, for any choice the person must make | `boards/<round>/` (spec, generator call, page, `open.html`) |

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))
