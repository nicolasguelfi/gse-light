# The catalogue — every artefact of gse-light, by type

Status: v0.3 · 2026-10-09 · §6 renamed "Published on claude.ai — decks and review boards" (an artefact of the method is any piece of it; an Artifact is also what claude.ai calls a published page — NG, 2026-10-09) · one row per artefact: what it does, who uses it, where it lives or is installed · the `review` skill added to both kits; the location column shortened so that "what it does" has the room (NG, 2026-10-09) · `check_docs` verifies that every skill, agent, template and script in the folders has its row here

**What this page is.** The inventory of the method's artefacts, grouped by type, for anyone who
wants to know what exists and what each piece is for before opening it. The two kits are the
artefacts that travel into other repositories; everything else is read in place. A location
written `…/x` is relative to the prefix given above its table.

**Words used here** (every other term: [GLOSSARY.md](GLOSSARY.md))

| Word | Meaning |
|---|---|
| **Skill** | a procedure Claude runs when asked (`/name`) or when the situation calls for it; a folder `skills/<name>/SKILL.md` |
| **Agent** | a read-only helper Claude launches for one job (a review, an audit, a check); a file `agents/<name>.md` |
| **Hook** | a script Claude Code runs by itself at a moment of the session (here: at session start) |
| **Template** | a document to copy and fill; it carries no licence obligation once filled |
| **Kit** | the files that make every Claude Code session in a repository follow the method; `claude-kit` for sandboxes and product repositories, `pm-kit` for the project-management repository |
| **Review board** | an interactive page of proposals by subject — the problem restated, each option's advantages, drawbacks and consequences, a comment under every point — that the person ticks and sends back as one line; made by the `review` skill |
| **Register** | one file per kind of decision (project, requirements, design); every decision is a numbered section of that file, never a file of its own |
| **Installed in** | the repository where a copy of the artefact ends up (`<product-repo>`, a sandbox, or `<pm-repo>`); "read in place" means it is only read from the `gse-light` clone |

## 1. The method — read in place

Where: in the `gse-light` clone.

| Artefact | What it does | Who uses it | Where |
|---|---|---|---|
| [`method/00-reference-design.md`](method/00-reference-design.md) | the method's rules for building, testing, delivering and running a product — rules as invariants, "how to choose" drivers, no tool names; approved v0.8 | everyone (chapters 0–2, 13); the project lead adds 15 (the start-of-project checklist) | `method/` |
| [`method/15-project-advisor.md`](method/15-project-advisor.md) | the Project Advisor's page: his role, the weekly meeting, where he steps in week by week; the source of the kick-off presentation | the Project Advisor, the project lead | `method/` |
| [`method/20-upskilling.md`](method/20-upskilling.md) | starting from the team's real levels: the skills round table, the personal plan, the `/upskilling` skill's principles | the Project Advisor, every team member | `method/` |
| [`method/40-tool-landscape-examples.md`](method/40-tool-landscape-examples.md) | tools seen in past projects, dated, non-normative — illustrations for the design phase, never defaults | the project lead in the design phase | `method/` |
| [`GLOSSARY.md`](GLOSSARY.md) | every term and acronym of the method in plain words, by theme | newcomers; every page links it | root |
| [`README.md`](README.md), [`QUICKSTART.md`](QUICKSTART.md) | the entry pages: what the method is and which repositories each role clones; the developers' one-page start | everyone / the developers and the project lead | root |
| [`CLAUDE.md`](CLAUDE.md) | the rules every Claude session follows when it works **in** the `gse-light` repository (no client name, naming, readable layout, entry-document skeleton, asking the author) | the method's author's sessions | root |
| [`LICENSE.md`](LICENSE.md), [`CITATION.cff`](CITATION.cff), `REUSE.toml`, `LICENSES/` | the licence (CC BY-NC 4.0 for documents, PolyForm Noncommercial for code), how to cite, the SPDX inventory | anyone who reuses the method | root |

## 2. Templates — copied and filled in a project-management repository

Where: under `<pm-repo>/instances/<instance>/`.

| Artefact | What it does | Who uses it | Where |
|---|---|---|---|
| [`templates/decision-record.md`](templates/decision-record.md) | the format of **one** decision or open question: plain-language problem, what to consult, options with advantages and drawbacks, drivers, recommendation, status badge. Each record is a numbered section appended to its register file (`PD`, `DEC` or `DD`), never a file per decision; the register's §0 dashboard lists them | the `decision-record` skill, in the three registers | `governance/05-…`, `requirements/05-…`, `design/05-…` |
| [`templates/design-drivers.md`](templates/design-drivers.md) | the project's facts and constraints collected before the twelve design decisions | the `design-phase` skill, the project lead | `design/` |
| [`templates/example-record.md`](templates/example-record.md) | one real example of the need, `EX-<AREA>-NNN`, anonymised, cited by the requirements | the team, the product owner | `requirements/40-examples/` |
| [`templates/requirement-record.md`](templates/requirement-record.md) | one requirement, `FR-<AREA>-NNN` or `NFR-<AREA>-NNN`, linked to its examples and tests | the project lead, the developers | `requirements/` |
| [`templates/session-journal.md`](templates/session-journal.md) | one working session: what was done with its commands, decisions, what was not done, hand-over | the `session-close` skill, every role | `journal/` |
| [`templates/meeting-agenda.md`](templates/meeting-agenda.md) | the Project Advisor's brief: the topics in a proposed order with indicative durations (the project lead chairs and keeps time), measured facts, decisions awaiting, points to raise | the `meeting` skill (`brief`) | `meetings/<date>/` |
| [`templates/meeting-minutes.md`](templates/meeting-minutes.md) | the minutes: executive summary, decisions, tasks per participant with transcript timestamps, the Advisor's feedback, "validated by … on" | the `meeting` skill (`minutes`), `minutes-verifier` | `meetings/<date>/` |
| [`templates/skills-grid.md`](templates/skills-grid.md) | the skills round table: eight lines, levels 0–3, counts per level, no names | the Project Advisor at the kick-off | `governance/` |
| [`templates/artifact-open.html`](templates/artifact-open.html) | a shortcut that opens a claude.ai artifact (deck, review board) from the file explorer | the `slides` and `review` skills | `meetings/<date>/…/open.html` |
| [`templates/slides/`](templates/slides/) | the deck model: `deck.json` and six slide models (cover, marks, table, cards, statement, next), dark, numbered | the `slides` skill | `meetings/<date>/slides/` |

## 3. Scripts — run from a project-management repository, read in place

Where: in the `gse-light` clone, run as `python3 ../gse-light/scripts/<name>` from `<pm-repo>`.

| Artefact | What it does | Who uses it | Needs |
|---|---|---|---|
| [`scripts/check_docs.py`](scripts/check_docs.py) | the documentation gates: links and anchors, registers and cockpit counts, kit copies, the *Who is who* copies, the catalogue rows, the deck's freshness, the leak guard (no client term in `gse-light`, files and commit messages) | every session before a commit; both CI workflows | Python only |
| [`scripts/situation.py`](scripts/situation.py) | where the project stands this week: today, next meeting, next step of the meeting chain | the start hook, the `advisor` skill | Python only |
| [`scripts/session_start.py`](scripts/session_start.py) | the session-start hook of `<pm-repo>`: git user, situation, what is missing | Claude Code, at every session opened in `<pm-repo>` | Python only |
| [`scripts/llm_call.py`](scripts/llm_call.py) | one paid model call (Gemini, or a text model through OpenRouter), cost estimated and logged in the instance's journal; switches by itself to `<pm-repo>/.venv` | `transcribe.py`; the Project Advisor's sessions | the environment of [`scripts/README.md`](scripts/README.md) §1 |
| [`scripts/meeting/meeting.sh`](scripts/meeting/meeting.sh) | records the meeting with ffmpeg (macOS), or imports a file recorded elsewhere; `devices`, `start`, `status`, `stop`, `import` | the `meeting` skill (`record`, `import`) | `ffmpeg` |
| [`scripts/meeting/transcribe.py`](scripts/meeting/transcribe.py) | transcribes a recording, locally (mlx-whisper, whisper.cpp) or with Gemini; `transcript.md` with timestamps | the `meeting` skill (`transcribe`) | a local engine or a Gemini key |
| [`scripts/README.md`](scripts/README.md) | how to prepare a machine: environments in `~/.venvs/<name>` linked as `.venv`, ffmpeg, the transcription engine, `.env` | the Project Advisor; the rule holds for every team member's machine | — |

## 4. The product kit `claude-kit/` — installed in every sandbox and product repository

Installed by one command run inside the clone, `../gse-light/claude-kit/install.sh <instance>`; committed with the code. Where: in that repository.

| Artefact | What it does | Who uses it | Where |
|---|---|---|---|
| **Skills** | | | `.claude/skills/<name>/` |
| [`decision-record`](claude-kit/skills/decision-record/SKILL.md) | records a decision or an open question in the right register (`PD`, `DEC`, `DD`) in the standard format and updates the dashboard; pushes the new 🔴 record | every team member, when a choice appears | |
| [`design-phase`](claude-kit/skills/design-phase/SKILL.md) | runs the design phase in W1 with the project lead: the drivers, then the twelve decisions in order, each as a `DD` record; then fills `gates.sh`, the CI and `CLAUDE.md` | the project lead, from his sandbox | |
| [`review`](claude-kit/skills/review/SKILL.md) | how the session asks you anything — an answer, a choice, a validation, a go-ahead: a short multiple-choice question for a simple point, a review board for the rest; the problem restated, every option's advantages, drawbacks and consequences, a comment under every point and a global one; your answer in one line. Carries the generator `review_board.py` | every session, by rule, whenever the person must decide | |
| [`session-close`](claude-kit/skills/session-close/SKILL.md) | closes a session: journal entry and metrics row in `<pm-repo>`, pushed; a hand-over a session with no memory can resume from | every team member, at the end of every session | |
| [`upskilling`](claude-kit/skills/upskilling/SKILL.md) | the personal coach: assesses where you stand, proposes a short plan of exercises, re-checks it later; its record stays on your machine | every team member, on Day 0 and when stuck | |
| [`verify-claim`](claude-kit/skills/verify-claim/SKILL.md) | before stating anything about a system (version, counts, test results, cause), measures it and shows the command and its output | every session, by rule | |
| **Agent** | | | `.claude/agents/<name>.md` |
| [`change-reviewer`](claude-kit/agents/change-reviewer.md) | reviews a diff or pull request against the reference design and the registers before it is merged — gates, data regime, secrets, migrations, documentation with the code | the developers, before a pull request | |
| **Files written by the install** | | | |
| [`templates/CLAUDE.product-repo.md`](claude-kit/templates/CLAUDE.product-repo.md) | the rules every session follows in the repository: the project's zone in `<pm-repo>`, the standing rules (asking the person included), the lessons, the commands; `<…>` fields filled by the design phase | every session in the repository | `CLAUDE.md` |
| [`templates/settings.json`](claude-kit/templates/settings.json) | permissions: read access to `../gse-light` and `../<pm-repo>`; the Edit tool denied under `../gse-light/**` and on the cockpit; `git push origin main` denied; ask before any `git push` | Claude Code | `.claude/settings.json` |
| [`templates/gates.sh`](claude-kit/templates/gates.sh) | the project's automated checks, run by the CI (`bash ./gates.sh`); on Day 0 a stub that says "no gates yet" | the CI, every session | `gates.sh` |
| [`templates/ci-gates.yml`](claude-kit/templates/ci-gates.yml) | the CI workflow that runs `gates.sh` on every change; services and branches filled from the design decisions | GitHub Actions | `.github/workflows/gates.yml` |
| [`templates/env.example`](claude-kit/templates/env.example) | the personal secrets and settings to copy into `.env`, never committed | every team member | `.env.example` |
| [`templates/gitattributes`](claude-kit/templates/gitattributes) | line endings: text normalised, shell scripts always LF (Windows) | git | `.gitattributes` |
| [`templates/KIT_LICENSE.md`](claude-kit/templates/KIT_LICENSE.md) | the licence notice that travels with the kit | anyone who reads the repository | `.claude/KIT_LICENSE.md` |
| **Scripts and pages of the kit** | | | read in place |
| [`install.sh`](claude-kit/install.sh) | writes the files above, fills `<instance>`, `<pm-repo>` and the repository name, records `KIT_VERSION`; `--pm <folder>` when several siblings hold `instances/<instance>/` | the project lead once per product repository; every team member in their sandbox | |
| [`check.sh`](claude-kit/check.sh) | checks a machine and a clone line by line: prerequisites, the two sibling repositories, the kit files, the kit version, nothing personal in git | every team member on Day 0 and when something is odd | |
| [`README.md`](claude-kit/README.md), [`INSTALL.md`](claude-kit/INSTALL.md), [`ONBOARDING.md`](claude-kit/ONBOARDING.md) | the kit's pages by role: what it is, how to install it, the first session step by step and the Day-0 checklists | every team member | |
| [`TEST-DAY0.md`](claude-kit/TEST-DAY0.md), [`TEST-DAY0-fast.txt`](claude-kit/TEST-DAY0-fast.txt) | the Day-0 rehearsal by role in a throwaway folder (the Project Advisor's own Day 0, the sandbox, the product repository), and the same as five blocks to paste | the Project Advisor and the project lead, after any kit change | |

## 5. The Project Advisor's kit `pm-kit/` — installed in the project-management repository

Installed by `../gse-light/pm-kit/install.sh . [<instance>]`, which also copies the instance scaffold into an empty `instances/<instance>/`. Where: in `<pm-repo>`.

| Artefact | What it does | Who uses it | Where |
|---|---|---|---|
| **Skills** | | | `.claude/skills/<name>/` |
| [`advisor`](pm-kit/skills/advisor/SKILL.md) | the single entry point of the Advisor's sessions: reads the situation, does the next step by orchestrating the other skills and agents, asks only what only he knows — a QCM, or a review board for a complex choice | the Project Advisor, on his first message | |
| [`meeting`](pm-kit/skills/meeting/SKILL.md) | the weekly meeting chain: `brief` the day before (the topics in a proposed order; the project lead chairs and keeps time), `record` or `import` on the day, `transcribe`, `minutes` checked by `minutes-verifier`, validated and sent by the project lead | the Project Advisor | |
| [`cockpit-update`](pm-kit/skills/cockpit-update/SKILL.md) | refreshes the cockpit `BRIEFING.md`: §1 what awaits the Advisor, §1b the team, §2 the delta, §3 the state and the pending counts | `session-close`, the Advisor's sessions | |
| [`decision-record`](pm-kit/skills/decision-record/SKILL.md) | the same skill as in the product kit (identical copy) | the Advisor's sessions | |
| [`review`](pm-kit/skills/review/SKILL.md) | the same skill as in the product kit (identical copy): a QCM or a review board whenever the Advisor must answer, choose or validate | the Advisor's sessions | |
| [`session-close`](pm-kit/skills/session-close/SKILL.md) | the same skill as in the product kit (identical copy) | the Advisor's sessions | |
| [`genai-onboarding`](pm-kit/skills/genai-onboarding/SKILL.md) | prepares one person's arrival: a cover note built on `ONBOARDING.md`, the Advisor's own to-do (licence, access, sandbox), then verifies the Day-0 checklist from the first journal entry | the Project Advisor, before the kick-off and for late arrivals | |
| [`method-lesson`](pm-kit/skills/method-lesson/SKILL.md) | turns something learned in a session into one dated lesson at the right place (`CLAUDE.md`, a skill, a template, the reference design, the kit template), propagated | the Advisor's sessions, as soon as a gap is named | |
| [`slides`](pm-kit/skills/slides/SKILL.md) | makes, reopens, updates or exports a presentation as a claude.ai Slides artifact; sources in git, synced from the viewer before any change; the freshness check; the registry of links | the Project Advisor | |
| **Agents** | | | `.claude/agents/<name>.md` |
| [`delivery-auditor`](pm-kit/agents/delivery-auditor.md) | read-only weekly audit for the brief: what the team delivered since the last meeting, measured (sprint file, pull requests, gates, journal, registers) | the `meeting` skill (`brief`) | |
| [`minutes-verifier`](pm-kit/agents/minutes-verifier.md) | checks the minutes against the transcript: every task and decision backed by an excerpt at the cited timestamp | the `meeting` skill (`minutes`) | |
| [`design-reviewer`](pm-kit/agents/design-reviewer.md) | reviews a change to the project-management documents for consistency: contradictions, decisions outside a register, broken links, stale cockpit, unverified claims | the Advisor's sessions before a substantial documentation change | |
| **Files written by the install** | | | |
| [`templates/CLAUDE.pm-repo.md`](pm-kit/templates/CLAUDE.pm-repo.md) | the rules of the Advisor's sessions in `<pm-repo>`: registers, cockpit discipline, evaluate ≠ execute, asking the person, the one entry point, improve from every interaction | every session opened in `<pm-repo>` | `CLAUDE.md` |
| [`templates/settings.json`](pm-kit/templates/settings.json) | permissions (read access to `../gse-light`, `.env` denied) and the **session-start hook** that runs `scripts/session_start.py` | Claude Code | `.claude/settings.json` |
| [`templates/env.example`](pm-kit/templates/env.example) | the Advisor's keys and settings: Google AI Studio, OpenRouter, the instance, the microphone, the transcription engine | the Project Advisor | `.env.example` |
| [`templates/docs.yml`](pm-kit/templates/docs.yml) | the CI workflow that runs `check_docs.py` on every push, with `gse-light` checked out at the installed pm-kit version | GitHub Actions | `.github/workflows/docs.yml` |
| [`templates/instance/`](pm-kit/templates/instance/) | the instance scaffold: `README.md` (people, repositories, calendar, start here by role), `BRIEFING.md` (the cockpit), the three registers with their dashboards, the roles record, `journal/` (README, `metrics.csv`), `meetings/README.md` | the Project Advisor when a project starts | `instances/<instance>/` |
| **Scripts and pages of the kit** | | | read in place |
| [`install.sh`](pm-kit/install.sh) | copies skills, agents, settings, `CLAUDE.md`, `.env.example`, the CI, the scaffold; records `PM_KIT_VERSION` | the Project Advisor, at the start and after every pm-kit change | |
| [`README.md`](pm-kit/README.md) | the pm-kit's page by role: what a project-management repository is, how to start a project, the weekly chain | the Project Advisor | |

## 6. Published on claude.ai — decks and review boards, one folder per artefact in the instance

Where: under `<pm-repo>/instances/<instance>/meetings/<date>/`, with a row in the registry `meetings/README.md`.

| Artefact | What it does | Who uses it | Where |
|---|---|---|---|
| A **deck** (Slides artifact) | a presentation for a meeting: dark, numbered slides, actor marks, a "Source" footer per slide so that `check_docs` warns when a source changed; made and synced by the `slides` skill | the Project Advisor | `slides/` (sources, `open.html`) |
| A **review board** | a page of proposals by subject with the problem restated, each option's advantages, drawbacks and consequences, a recommendation, a comment under every point and a global one; the person ticks and sends back one line; made by the `review` skill | any session, for any choice the person must make; in a sandbox or product repository the sources go to `boards/<date>-<round>/` | `boards/<round>/` (spec, generator call, page, `open.html`) |

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))
