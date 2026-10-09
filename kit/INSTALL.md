# Installing the kit — the Project Advisor once, everyone else by cloning

Status: v0.7 · 2026-10-09 · one repository per project, one kit for every role (board r11) · maintained by the Project Advisor

> **Essentials** — How the kit gets into the project's repository, and what is shared or personal.
>
> - **Project Advisor**: one command, once, in the project's repository, then a commit; the refresh — §2.
> - **Project lead, developers**: a clone and three personal steps — §3; the numbered path from zero is in [QUICKSTART.md](../QUICKSTART.md).
> - **Product owner**: nothing to install — §4.
> - **What `check.sh` says** — §5.
>
> Two repositories, cloned **side by side** in one parent folder:
>
> - the **`gse-light` repository** — this method and its kit; public; read by every session, changed by none;
> - the **project's repository `<project-repo>`** — the code and, in `project/`, the project's shared record (cockpit, registers, requirements, planning, meetings, journal, roles); private; the kit lives **in it**, committed like the code.
>
> Everyone opens Claude Code in the project's repository. Everything personal stays out of git, as the Claude Code documentation has it: `.claude/` and `CLAUDE.md` are the team's shared rules; each person's data lives in their own `~/.claude/`.

**Words used here** (every other term: [GLOSSARY.md](../GLOSSARY.md))

| Word | Meaning |
|---|---|
| **Kit** | the files that make every Claude Code session in the project's repository follow the method — `CLAUDE.md`, twelve skills, four agents, permissions and the start hook, a `gates.sh` stub, two CI workflows, the `project/` skeleton — installed with one command, committed with the code |
| **Project folder** `project/` | the shared record inside the project's repository; created by the kit from a skeleton, never touched again by the kit |
| **Day 0** | each person's first hour on the project — clone, `.env`, `check.sh`, first session |
| **Gates** | the project's automated checks (tests, lint, end-to-end) run by `gates.sh` and the CI before a merge; on Day 0 a stub that says "no gates yet" |
| **Design phase** | the step of W1 (the first project week) where the project lead, with Claude, turns the project's facts and constraints into twelve technical decisions (`DD` records), in order: repository layout, hosting, environments and promotion path, stack and language, data store, identity, infrastructure as code, continuous integration, test tools, secrets, dependency updates, monitoring — recorded with the skill `design-phase` |
| **Decision record and badges** | every `PD-NN`, `DEC-NNN` or `DD-NN` in these pages is one numbered decision record, with a status badge — 🔴 pending, 🟢 decided, 🟡 provisional; its *decider* (the person the roles record names) is the only one who turns it 🟢 |
| **Cockpit** | `project/BRIEFING.md`, the Project Advisor's one-page dashboard, written by his sessions only |
| **Go-ahead** | the written yes of the person who holds that right (roles record), before any state-changing action (push to a branch that deploys, deploy, spend) |
| **Sandbox** | a personal, private, throwaway repository a team member may create for experiments outside the project; optional |

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

## 0. Shared and personal (everyone)

| What | Where | In git? |
|---|---|---|
| Rules for the whole team: `CLAUDE.md`, `.claude/settings.json`, `.claude/skills/`, `.claude/agents/`, `.claude/KIT_LICENSE.md`, `.claude/KIT_VERSION` | `<project-repo>` | **yes** — committed by the Project Advisor |
| The shared record: `project/` (cockpit, registers, requirements, planning, meetings, journal, roles) | `<project-repo>` | **yes** — each person their own part, through the kit's skills |
| The gates: `gates.sh` (a Day-0 stub until the design phase fills it) and the CI workflow `.github/workflows/gates.yml` that runs it (`bash ./gates.sh`) | `<project-repo>` | **yes** — created by the kit, filled in W1 (the design phase) by the project lead |
| The documentation checks: `.github/workflows/docs.yml` (`check_docs` on `project/`, with `gse-light` at the installed `KIT_VERSION`) | `<project-repo>` | **yes** |
| `.gitattributes` (`*.sh text eol=lf`: keeps `gates.sh` runnable from a Windows clone) and `.env.example` | `<project-repo>` | **yes** |
| Your keys and settings: `.env` | `<project-repo>` (your clone) | **no** (git-ignored by the kit) |
| Your personal instructions: `CLAUDE.local.md`; your personal permissions: `.claude/settings.local.json` — the Project Advisor's allows the Edit tool on the cockpit: `{"permissions": {"allow": ["Edit(./project/BRIEFING.md)"]}}` | `<project-repo>` (your clone) | **no** (the kit ignores the first; Claude Code excludes the second itself) |
| Meeting recordings (`project/meetings/<date>/audio*`) | the Project Advisor's clone | **no** (git-ignored by the kit) |
| Your sessions, Claude's memory of you, your personal skills | `~/.claude/` on your machine | **no** — never in any repository |
| Your upskilling record (answers, plan) | `~/.claude/upskilling/<project>/record.md` | **no** — in your home folder, one sub-folder per project |
| A sandbox for experiments (optional) | your own private repository on GitHub | **yes**, there only — throwaway, never a project repository |

## 1. Prerequisites (everyone)

| Need | macOS | Windows |
|---|---|---|
| Git, and access on **GitHub** (HTTPS with a personal access token, or an SSH key) to `<project-repo>` (from its host, named in the roles record); `gse-light` is public. GitHub is a prerequisite of the method's own tooling (pull requests, CI, the Project Advisor's brief) | Xcode command-line tools or Homebrew `git` | Git for Windows (it brings **Git Bash**) |
| A bash terminal for `install.sh`, `check.sh` and `gates.sh` | Terminal | Git Bash or WSL |
| **`python3`** (3.10 or later) for the method's scripts (`check_docs.py`, `situation.py` and the start hook, the small script that prints where the project stands when a session opens) | Xcode command-line tools or Homebrew `python` | python.org installer or `winget install Python.Python.3.12` |
| **Claude Code**, signed in with the account the Project Advisor invited | desktop app, or the CLI (`npm install -g @anthropic-ai/claude-code`, which needs Node.js) | same |

Check: `git --version`, `python3 --version` and `claude --version` each print a version.

**Windows is covered**: the `gse-light` repository tracks a `.gitattributes` (`*.sh` and
`*.py` with `eol=lf`), and the kit writes one in `<project-repo>`, so the scripts keep Unix
line endings on a Windows clone whatever your `core.autocrlf`; run them from Git Bash.

## 2. If you are the Project Advisor — install the kit, once, and refresh it

**Step 0 — the project's repository exists on GitHub.** The project lead or the client's IT
creates it, empty or with a README only, private, and gives you write access. Where it lives
and who owns it is a project decision (its `PD` record); whether `main` is protected on
GitHub is decided in the roles record.

**Step 1 — clone side by side and run the one command** (*you*):

```bash
mkdir -p ~/dev/<project> && cd ~/dev/<project>            # the parent folder of the two repositories
git clone https://github.com/nicolasguelfi/gse-light.git  # the gse-light repository (method and kit), if not there yet
git clone <project-repo URL>                               # the project's repository (empty or README only)
cd <project-repo>
../gse-light/kit/install.sh                                # the one command, no argument
```

It writes:

| Created | What it is |
|---|---|
| `project/` | the shared record's skeleton, from `kit/templates/project/`: `README.md` (the project, its phase, its people, the repositories), `BRIEFING.md` (the cockpit: §1, §1b, §2, §3 with the pending counts), the three registers with their §0 dashboards (`governance/05-project-decisions.md`, `requirements/05-decisions.md`, `design/05-design-decisions.md`), the roles record `governance/10-roles-and-go-aheads.md`, `journal/` (README, `metrics.csv`), `meetings/README.md`; `<project>` filled with the repository's name; **never touched again** once the folder has files |
| `CLAUDE.md` | the rules every session loads, with the repository's name filled; the `<…>` fields (purpose, commands) are the project lead's after the design phase — **ask Claude**: *"fill CLAUDE.md with this project's purpose and commands"* |
| `.claude/settings.json` | `../gse-light` as additional directory; the Edit tool denied under `../gse-light/**` and on `./project/BRIEFING.md`; the literal command `git push origin main` denied; Claude asks before any `git push`; the start hook (`scripts/session_start.py`). Conveniences for the session, not a security boundary |
| `.claude/skills/` (twelve: `design-phase`, `decision-record`, `review`, `session-close`, `verify-claim`, `upskilling`, and yours — `advisor`, `meeting`, `slides`, `cockpit-update`, `method-lesson`, `genai-onboarding`), `.claude/agents/` (`change-reviewer`, `delivery-auditor`, `minutes-verifier`, `design-reviewer`) | the kit's own files, refreshed on every run |
| `gates.sh` | Day-0 stub: prints *no gates yet: design phase in progress* and exits 0; the design phase fills it |
| `.github/workflows/gates.yml` | runs `bash ./gates.sh` on every pull request and on every push to `main` — green from Day 0 |
| `.github/workflows/docs.yml` | runs `python3 ../gse-light/scripts/check_docs.py` on `project/`, with `gse-light` checked out at the installed `KIT_VERSION` |
| `.gitattributes`, `.env.example`, `.gitignore` entries (`.env`, `CLAUDE.local.md`, the meeting recordings) | line endings, personal files and recordings out of git |
| `.claude/KIT_LICENSE.md`, `.claude/KIT_VERSION` | the licence notice and the last `gse-light` commit that touched `kit/` |

**Step 2 — fill, check, commit and push** (*you*):

```bash
# fill the <…> fields of project/README.md and project/governance/10-roles-and-go-aheads.md (the people, the calendar)
printf 'ClientName\nProjectName\n' > project/private-terms.txt   # the terms the leak guard refuses in gse-light (regular expressions, one per line)
cp .env.example .env                                       # your keys and settings (recording, transcription), never committed
python3 ../gse-light/scripts/check_docs.py                 # expected: ok
git add project CLAUDE.md .claude .env.example .gitattributes .gitignore .github gates.sh
git commit -m "Install the gse-light kit (kit $(cat .claude/KIT_VERSION))"
git push                                                   # first push on an empty repository: git push -u origin HEAD
```

Protected `main`: `git switch -c kit && git push -u origin kit`, then open the pull request
on GitHub; the Day-0 CI runs the stub and the documentation checks, both green. Tell the team
the kit is in: they clone.

On your machine, once: `.claude/settings.local.json` with
`{"permissions": {"allow": ["Edit(./project/BRIEFING.md)"]}}` (the cockpit is yours; the shared
settings deny it to every session), and the machine's preparation for the recording and
transcription scripts ([`scripts/README.md`](../scripts/README.md) §1).

**Refresh** after the kit changes in the `gse-light` repository:

1. `git pull` in `gse-light`;
2. rerun the same command from inside `<project-repo>` — it overwrites only the kit's own skills, agents, licence notice and `KIT_VERSION`; `project/`, `CLAUDE.md`, `settings.json`, `gates.sh` and the two workflows stay the project's;
3. when a template changed since your `KIT_VERSION`, it prints a warning naming the template and the exact command to compare, with the hash of your **previous** `KIT_VERSION` — `git -C ../gse-light diff <old hash>..HEAD -- kit/templates/` — because `.claude/KIT_VERSION` already holds the new hash once the command has run: run it as printed and carry the change over by hand;
4. commit and push in `<project-repo>`.

`check.sh` tells each team member when the kit in their clone is older than `kit/` in their
clone of `gse-light`.

- **Write**: the cockpit, the briefs and draft minutes, `project/README.md`, the governance pages, your journal entries; the method and the kit in `gse-light`.
- **Never**: write a client's or project's name in `gse-light` (the leak guard, `check_docs.py`, refuses it); run the one command for a different project in the same clone.

## 3. If you are the project lead or a developer — clone, env, check, first session

- **The path, step by step** (*you*): one numbered table, from no account to your first session, with who does each step — [QUICKSTART.md, "from zero to your first session"](../QUICKSTART.md#if-you-are-a-developer-from-zero-to-your-first-session): your seat and Claude Code, GitHub access, the two clones side by side, `.env`, `check.sh`, the gates, `/upskilling`, your first journal entry. This page adds what is shared or personal (§0), the prerequisites by platform (§1) and what `check.sh` says (§5).
- **In short** (*you*), once the Project Advisor has pushed the kit:

  ```bash
  mkdir -p ~/dev/<project> && cd ~/dev/<project>
  git clone https://github.com/nicolasguelfi/gse-light.git  # the gse-light repository (method and kit)
  git clone <project-repo URL>                               # the project's repository: the kit comes with it
  cd <project-repo>
  cp .env.example .env                                       # fill it with what the project lead gives you
  ../gse-light/kit/check.sh                                  # every line OK, or it says what to do
  claude                                                     # accept the workspace trust dialog
  ```

  In the session: type `/` and check that `design-phase`, `decision-record`, `review`, `session-close`, `verify-claim` and `upskilling` appear (the six other skills are the Project Advisor's: they stop for anyone else); then run **`/upskilling`** (where you start, and a short personal plan). Day 0 happens on a personal branch `day0-<firstname>` of the project's repository; you never run `install.sh`. If you cloned before the kit was there: `git pull` once the Project Advisor has pushed.
- **Project lead, in addition**: in W1, *"Run design-phase"* in your clone — the drivers page, then the twelve `DD` records; the first, repository layout, settles how the code is laid out in this repository; then `gates.sh`, the CI and the `<…>` fields of `CLAUDE.md` filled from those decisions, committed by you ([ONBOARDING.md §2](ONBOARDING.md#2-if-you-are-the-project-lead)).
- **Write**, through the kit's skills: your journal entries and 🔴 records in `project/`; the project lead also the sprints and the validation line of the minutes.
- **Never**: edit `project/BRIEFING.md` (the Project Advisor's cockpit) or anything under `../gse-light`; push to `main` without the go-ahead.

Time: about 10 minutes to clone and check, 15 for `/upskilling`, 30 for your first session
([starting guide §3b](ONBOARDING.md#3b-your-first-session-step-by-step-30-minutes)); words you do not know are in the [glossary](../GLOSSARY.md).
Keep the one-page [quick start](../QUICKSTART.md) at hand for the rest of the project.

**Known limit**: a Claude Code session started on claude.ai (web or cloud) clones **one**
GitHub repository into an isolated container and sees `../gse-light` only if it is cloned next
to it. Work locally, where the two clones are side by side.

## 4. If you are the product owner

- **Install**: nothing, nothing to clone, no Claude Code licence needed.
- **Read**, in the project's repository on GitHub: `project/README.md` (project, phase, people), the roles record (your go-aheads: production, budget; you accept each delivered increment) and the 🔴 records that await you in the registers.
- **Write**: nothing — your decisions are recorded by the team (🟢 by its decider, you); the cockpit is the Project Advisor's.

## 5. What check.sh says

To rehearse your role's Day 0 on your own machine first: [TEST-DAY0.md](TEST-DAY0.md).

| `check.sh` says | Do |
|---|---|
| `MISSING git`, `MISSING python3`, `MISSING Claude Code` | install it (§1); sign Claude Code in with the invited account |
| `MISSING gse-light next to this repository` | clone the `gse-light` repository in the same parent folder as your clone of `<project-repo>` |
| `MISSING CLAUDE.md` or `MISSING project/` | the kit is not installed here, or not pushed yet: the Project Advisor runs the one command and pushes (§2); `git pull` once he has |
| `MISSING skill …`, `MISSING agent …`, `WARN skill …` | the kit is incomplete or outdated: the Project Advisor refreshes it (§2) |
| `MISSING .claude/settings.json`, `WARN settings.json` | the shared permissions or the start hook are missing: compare with `kit/templates/settings.json`; the Project Advisor refreshes |
| `MISSING gates.sh`, `WARN gates.yml`, `WARN docs.yml` | a file the kit created was deleted: the Project Advisor reruns the one command (§2) |
| `WARN gates.sh … not executable` | `chmod +x gates.sh`; in git: `git update-index --chmod=+x gates.sh`, then commit |
| `WARN .gitattributes` | `*.sh text eol=lf` is missing: `gates.sh` may break on a Windows clone; the Project Advisor reruns the one command |
| `MISSING kit committed` | the kit was installed without being committed: the Project Advisor commits and pushes (§2) |
| `WARN kit version … the kit in gse-light is newer` | the kit was updated in the `gse-light` repository: `git pull` here (the Project Advisor may already have refreshed and pushed); if the line stays, he refreshes it (§2) |
| `WARN kit version … your clone of gse-light is behind` | `git pull` in `gse-light` |
| `WARN KIT_LICENSE.md` | the licence notice of the kit is missing: the Project Advisor reruns the one command |
| `MISSING … not in git` | a personal file is tracked: `git rm --cached <file>`, then commit |
| `WARN .env` | `cp .env.example .env` in your clone, then fill it (§3) |

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))
