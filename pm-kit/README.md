# pm-kit — the Project Advisor's kit for a project-management repository

Status: v0.1 · 2026-10-08 · entry page in the shape of board r5: a part for everyone, one section per role, then the reference

This page is for the **Project Advisor** of a project run with the method gse-light: what the
pm-kit is, how he creates the project's project-management repository and installs the kit
there, what his Claude Code sessions then do every week, and what he never does. A project
lead or a developer needs only one thing from it: this kit is not theirs ([their
section](#if-you-are-the-project-lead-or-a-developer)). The pm-kit is the tooling of the
method's author (Nicolas Guelfi) in his role of Project Advisor; another Project Advisor may
use it as is. The method itself needs only [`claude-kit`](../claude-kit/README.md), also
called the product kit: the kit of the product and sandbox repositories.

**Words used here** (every other term: [GLOSSARY.md](../GLOSSARY.md))

| Word | Meaning |
|---|---|
| **Project-management repository** `<pm-repo>` | the project's shared record — decisions, requirements, plans, minutes, journal — private, one per project. Everyone reads it; each person writes their own part in it through the kit's skills (the project lead: the sprints; the Project Advisor: the cockpit and the minutes); nobody manages the project from it |
| **Kit** | the files that make every Claude Code session in a repository follow the method — `CLAUDE.md`, skills, an agent, permissions, a CI workflow — installed with one command, committed with the code |
| **Session** | one conversation with Claude Code, from opening it in a folder to closing it |
| **Instance** | one project run with the method, and its folder `instances/<instance>/` in `<pm-repo>` |
| **Skill, agent** | a skill is a procedure Claude runs when asked (`/name`) or when the situation calls for it; an agent is a read-only helper Claude launches (an auditor, a reviewer) |
| **Cockpit** | `BRIEFING.md`, the Project Advisor's one-page dashboard in the instance — what awaits him, what awaits the team, what changed; written by his sessions only |
| **Register** | one document per kind of decision — project `PD`, requirements `DEC`, design `DD` — one numbered record per decision, each with a status badge: 🔴 pending, 🟢 decided, 🟡 provisional; the *decider* is the person the roles record names for that record, the only one who turns it 🟢 |
| **Sandbox** | a personal, private, throwaway repository `<project>-sandbox-<firstname>` with the kit, for Day 0 and experiments until the product repositories exist; the project lead's sandbox hosts the design phase |
| **Leak guard** | the check (`check_docs.py`) that no private name of the client or project reaches the public `gse-light` repository, in files or commit messages |
| **Start hook** | the small script run when a session opens in `<pm-repo>`; it prints where the project stands |

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

## The repositories

| Repository | What it is for | Who writes in it | Who reads it | Why it is separate |
|---|---|---|---|---|
| `gse-light` (public) | the method: the rules every session follows, the templates, the scripts, the two kits | the method's author only; every session reads it, none changes it | everyone | public and reusable by other projects, so nothing of a client may appear in it — the leak guard enforces it |
| `<pm-repo>` (private, one per project) | the project's shared record: decisions, requirements, plans, minutes, journal; `instances/<instance>/` holds the instance; this kit is installed in it | each person their own part, through the kit's skills: the Project Advisor's sessions the cockpit, the minutes and his journal entries; the project lead the sprints; every team member their journal entries and new 🔴 records | everyone | nobody manages the project from it; its sessions are the Project Advisor's, and it is the **overall view**: the instance `README.md` lists the product repositories, and every product repository's sessions write their decisions and journal into it |
| `<project>-sandbox-<firstname>` (private, one per team member) | Day 0, `/upskilling` and experiments with the product kit until the product repositories exist; the project lead's hosts the design phase | its owner | its owner, the project lead | throwaway, never audited, never a product repository |
| product repositories (private, one or several) | the code, data jobs, infrastructure code, each with the product kit | the developers by pull request, the project lead reviews | the team | code is separate from project management: a session in a product repository writes into `<pm-repo>` only through the kit's skills |

## If you are the Project Advisor

- **Read first**:
  - [the Project Advisor's page](../method/15-project-advisor.md) — who is in the project, the weeks and where the Advisor steps in, the weekly meeting, what he does by default and does not;
  - the [reference design](../method/00-reference-design.md), chapters 0 (purpose and how to read it), 1 (principles), 2 (how people and AI share the decisions), 13 (working with the AI day to day) and 15 (the start-of-project checklist);
  - the [glossary](../GLOSSARY.md) for every term.
- **Install**: the machine first, once — [`scripts/README.md`](../scripts/README.md) (ffmpeg, `uv`, the Python environment in `~/.venvs/<pm-repo>` linked as `.venv`, `.env`). Then the project-management repository and this kit:

  ```bash
  cd ~/dev/<project>                                          # parent folder: the clones side by side
  git clone https://github.com/nicolasguelfi/gse-light.git   # the gse-light repository (this method)
  mkdir -p <pm-repo>/instances/<instance> && cd <pm-repo> && git init   # <instance>: the folder name of the project under instances/
  ../gse-light/pm-kit/install.sh .                          # skills, agents, settings, CLAUDE.md, .env.example, CI, and the instance skeleton
  cp .env.example .env                                        # fill it (never committed)
  printf 'ClientName\nProjectName\n' > instances/<instance>/private-terms.txt   # terms the leak guard refuses in gse-light (regular expressions, one per line)
  ```

  `pm-kit/install.sh` copies [`templates/instance/`](templates/instance/) into an empty `instances/<instance>/`:
  - `README.md` — the instance's entry page: people, **the list of the project's repositories**, the calendar, where each role starts;
  - `BRIEFING.md` — the cockpit: §1, §1b, §2, §3 with the pending counts;
  - the three registers in the format of [`templates/decision-record.md`](../templates/decision-record.md) — `governance/05-project-decisions.md`, `requirements/05-decisions.md`, `design/05-design-decisions.md` — with their §0 dashboards;
  - the roles record `governance/10-roles-and-go-aheads.md`;
  - `journal/` and `meetings/`.

  Then, in order:
  1. fill the `<…>` fields of `CLAUDE.md` and of the skeleton (the people in `README.md` and in the roles record, the calendar);
  2. run `python3 ../gse-light/scripts/check_docs.py`;
  3. commit;
  4. create the repository on GitHub (private; branch protection on `main` is recommended, decided in the roles record) and push.

  Each team member's sandbox is created on GitHub by the project lead or by you, and receives the product kit by its one command ([`claude-kit/README.md`](../claude-kit/README.md)).
- **Write**, every week: open Claude Code in `<pm-repo>` — the start hook prints the situation (today, next meeting, next step) — and say "go". The `advisor` skill does the step and asks you only what only you know, one short multiple-choice question (QCM) at a time:
  - `meeting brief` the day before — facts measured by the `delivery-auditor` agent, decisions awaiting, a timed agenda;
  - `record` or `import` on the day;
  - `transcribe`;
  - `minutes` — checked by `minutes-verifier`, then validated by you: "validated by <your name> on YYYY-MM-DD" in the header;
  - `decision-record` for what was decided;
  - `session-close` — journal entry, metrics row, cockpit.

  Your sessions write the cockpit `BRIEFING.md`, the minutes, the instance `README.md`, your journal entries, and the 🟢 of the records you decide (the method, the kits, your own spending); a lesson learned goes through `method-lesson`.
- **Cross-repository work**: open Claude Code in `<pm-repo>` with the product repositories added — `claude --add-dir ../<repo-a> --add-dir ../<repo-b>`, or list them in `permissions.additionalDirectories` of `.claude/settings.json` — to read code, pull requests and gates of every repository of the project from the overall view. A Claude Code session on claude.ai (web or cloud) sees one repository only; the overall view is a local session.
- **Check**: after any change to the pm-kit or to the scripts, replay your block of the Day-0 rehearsal — [`claude-kit/TEST-DAY0.md`](../claude-kit/TEST-DAY0.md) §1 (the pm-kit scaffold in a throwaway folder, `check_docs`, the situation, one dry-run model call, the meeting chain on a ten-second recording).
- **Never**: write a sprint, a ticket or code; decide in the project (sprints, priorities, promotions, the client's budget: the roles record names who does); turn 🟢 a record whose decider is someone else; push without having run `check_docs`; write a client's or project's name in `gse-light` (the leak guard refuses it).

## If you are the project lead or a developer

- **Read first**: [QUICKSTART.md](../QUICKSTART.md) — what gse-light does for you, the one install command, what to use at each moment of the project.
- **Install**: not this kit — yours is the product kit, `claude-kit`, installed in your sandbox and in each product repository.
- **Write**: from your sandbox or a product repository, your kit's skills `session-close` and `decision-record` push your journal entries and your new 🔴 records into `<pm-repo>` (those paths only); the project lead also writes `planning/sprints/` there. A record turns 🟢 only in a session of its decider; `BRIEFING.md` is the Advisor's (the product kit's `settings.json` denies the Edit tool on it — a convenience, not a security boundary; branch protection on `main` is the real guard).
- **Never**: open Claude Code in `<pm-repo>` — a session opened there loads this kit and acts in the Project Advisor's name (it writes his cockpit, it closes decisions).

## Reference

### Contents of the kit

| Path | What it is | Installed as |
|---|---|---|
| [`install.sh`](install.sh) | Installs or refreshes the kit in a project-management repository; copies the instance skeleton into an empty `instances/<instance>/` | run from `<pm-repo>`: `../gse-light/pm-kit/install.sh .` |
| [`skills/`](skills/) | `advisor` (single entry point), `meeting`, `slides`, `method-lesson`, `decision-record`, `cockpit-update`, `session-close`, `genai-onboarding` | `.claude/skills/` (refreshed) |
| [`agents/`](agents/) | `delivery-auditor` (measures what the team delivered, before each meeting), `minutes-verifier` (every task of the minutes backed by the transcript), `design-reviewer` (consistency of a documentation change) | `.claude/agents/` (refreshed) |
| [`templates/settings.json`](templates/settings.json) | Permissions (read-only commands, `.env` denied, `../gse-light` reachable) and the start hook | `.claude/settings.json` (created once) |
| [`templates/CLAUDE.pm-repo.md`](templates/CLAUDE.pm-repo.md) | Rules of the Project Advisor's sessions | `CLAUDE.md` (created once, then owned by `<pm-repo>`) |
| [`templates/env.example`](templates/env.example) | Keys and settings of the scripts (paid models, recording, transcription): one variable per vendor, nothing project-specific | `.env.example` (created once; `.env` never committed) |
| [`templates/docs.yml`](templates/docs.yml) | CI: `check_docs` with `gse-light` checked out next to `<pm-repo>` | `.github/workflows/docs.yml` (created once) |
| [`templates/instance/`](templates/instance/) | Skeleton of a new instance: `README.md`, `BRIEFING.md` (§1, §1b, §2, §3 with the counts line), the three registers with their §0 dashboards, `governance/10-roles-and-go-aheads.md`, `journal/README.md`, `journal/metrics.csv`, `meetings/README.md` | `instances/<instance>/` (copied once, when the folder is empty) |

### Refresh after a change in gse-light

1. `git pull` in `gse-light`;
2. `../gse-light/pm-kit/install.sh .` in `<pm-repo>`;
3. commit.

`check_docs` fails while `.claude/` differs from the pm-kit (from a product or sandbox
repository: `python3 ../gse-light/scripts/check_docs.py ../<pm-repo>`, the repository to
check as the argument).

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))
