# Quick start — what gse-light does for you and what to use, all project long

Status: v0.7 · 2026-10-09 · step 0 — the machine from zero (GitHub account, Git, Python, the environment rule) · one page, a section per role; one repository per project (board r11): two clones, the kit installed once by the Project Advisor; the developer's numbered path from zero; details in [INSTALL.md](kit/INSTALL.md) and [ONBOARDING.md](kit/ONBOARDING.md)

## What gse-light does for you

This page is the one-page start of a project run with `gse-light`, written first for the
team members — the project lead or a developer: what the method does for your Claude Code
sessions, which repositories you clone, your Day 0 in the section of your role, then what to
use all project long; the product owner and the Project Advisor have their short section.
`gse-light` is the method your project runs with: you clone it once, next to the project's
repository, and never change it. It gives your sessions a few firm habits — measure before
asserting, decisions in registers, nothing state-changing without a go-ahead (the written
yes of the person who holds that right, named in the roles record), a journal entry per
session, end-to-end tests through the real user interface — through a **kit** committed in
the project's repository.

**Words used here** (every other term: [GLOSSARY.md](GLOSSARY.md))

| Word | Meaning |
|---|---|
| **Day 0** | each person's first hour on the project — clone, `.env`, `check.sh`, first session, `/upskilling`, first journal entry — in the project's repository, on a personal branch |
| **Project's repository** `<project-repo>` | the one private git repository of the project: its code, and its shared record in `project/`; the kit is committed in it |
| **Project folder** `project/` | the shared record — cockpit, registers, requirements, planning, meetings, journal, roles record. Everyone reads it; each person writes their own part through the kit's skills |
| **Register** | one document per kind of decision — project `PD`, requirements `DEC`, design `DD` — one numbered record per decision, a dashboard at the top |
| **Decision record and badges** | every `PD-NN`, `DEC-NNN` or `DD-NN` in these pages is one numbered decision record, with a status badge: 🔴 pending, 🟢 decided, 🟡 provisional; its *decider* is the person the roles record names for it, the only one who turns it 🟢 |
| **Kit** | the files that make every Claude Code session in the project's repository follow the method — `CLAUDE.md`, twelve skills, four agents, permissions, a start hook, a `gates.sh` stub, two CI workflows (`bash ./gates.sh`, the documentation checks), the `project/` skeleton — installed with one command by the Project Advisor, committed with the code |
| **Skill, agent** | your six skills — `design-phase`, `decision-record`, `review`, `session-close`, `verify-claim`, `upskilling` — are procedures Claude runs when asked (`/name`) or by rule (`review`: how Claude asks you to choose — a short multiple-choice question, or a review board with the problem restated and every option's advantages, drawbacks and consequences); your agent, `change-reviewer`, is a read-only helper Claude launches. The six other skills and three other agents are the Project Advisor's: they stop for anyone else |
| **Gates** | the project's automated checks (tests, lint, end-to-end) run by `gates.sh` and the CI before a merge; on Day 0 a stub that says "no gates yet" |
| **Sandbox** | optional: a personal, private, throwaway repository `<project>-sandbox-<firstname>` for experiments outside the project, created by its owner; nothing of value stays there |
| **Placeholders** `<project-repo>`, `<project>`, `<firstname>` | stand for the project's real names: the repository, the project's short name (also the parent folder `~/dev/<project>`), a person's first name |

```text
~/dev/<project>/                      one parent folder, the two clones side by side
├── gse-light/        the method (public) — read by every session, changed by none
└── <project-repo>/   the project (private) — you work here: the code, the kit, and
                      project/ — registers, journal, sprints, meetings, the Advisor's cockpit
```

**Prerequisites** (details: [INSTALL.md §1](kit/INSTALL.md#1-prerequisites-everyone)):

- **Git**, with access on GitHub to `<project-repo>` (from its host, named in the roles record);
- **a bash terminal** (Git Bash on Windows; the scripts keep Unix line endings there);
- **`python3`**;
- **Claude Code**, signed in with the invited account;
- **no Python environment** for the method on your machine; the product's own environments follow one rule on a machine with a synced folder (Dropbox, OneDrive…): the environment lives in `~/.venvs/<name>`, the project's repository holds a link — commands in [`scripts/README.md`](scripts/README.md) §0.

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

## Which repositories you clone, by role

| Role | Clones | Why |
|---|---|---|
| Developer | `<project-repo>` · `gse-light` | your Claude sessions open in the project's repository, read the method's rules in `../gse-light` and write your journal entries and pending records in `project/` |
| Project lead | the same two | plus the sprints and the design decisions in `project/` |
| Project Advisor | the same two | his sessions open in the project's repository too; he installs and refreshes the kit there |
| Product owner | none | reads `project/` on GitHub, with read access to the project's repository |

Every session **reads** the method in `../gse-light` and **writes** in the project's repository.
The kit's `settings.json`:

- lists `../gse-light` as an additional directory;
- denies Claude the Edit tool under `../gse-light/**` and on `project/BRIEFING.md` (the Advisor's cockpit: his one-page dashboard; his own `.claude/settings.local.json`, never committed, allows it to him);
- denies the literal `git push origin main`; Claude asks before any `git push`;
- runs the start hook: the situation of the week for everyone, the Advisor's tasks for him (the git user matched against the roles record).

Conveniences for the session, not a security boundary: what guards the method, the cockpit
and `main` is review by a person and, when the project has enabled it in its roles record,
GitHub branch protection on `main` (not available on a private repository owned by a
personal account: the roles record says where the repository lives).

- **Known limit**: a Claude Code session started on claude.ai (the web or cloud version) works in
  an isolated container with **one** GitHub repository cloned into it; it sees `project/` but not
  `../gse-light`, so the method's pages and scripts are out of its reach. Work locally, where the
  two clones are side by side.
- **A product made of several repositories**: the repository layout `DD` (the first decision of
  the design phase) says which repository holds `project/`; the kit is installed in that one,
  and the others are listed in `project/README.md`.

## If you are the project lead: what you add to a developer's path

- **Read first**:
  - [the Project Advisor's page](method/15-project-advisor.md) — who is in the project, the weeks, the weekly meeting;
  - the reference design chapters in "Read next", plus chapter 15 (the start-of-project checklist).
- **Install**: nothing — the Project Advisor installs the kit in the project's repository and refreshes it after every change of the kit; you get it by cloning, like every developer: follow the numbered path below.
- **W1, the design phase** (*you*, then *ask Claude*): in the project's repository, on a branch, *"Run design-phase"* turns the project's facts and constraints into twelve `DD` records (listed in the table "All project long", row W1); the first, repository layout, says how the code is organised inside this repository; then `gates.sh`, the CI and the `<…>` fields of `CLAUDE.md` are filled from them, in a pull request.
- **Write**: the sprint file `project/planning/sprints/W<n>.md`, the `DD` records, the review of every pull request, the validation line of the minutes (your session writes it in `project/meetings/<date>/minutes.md`, then you send them).
- **Never**: turn a record 🟢 unless the roles record names you its decider; let a decision live only in a chat or a ticket; edit `project/BRIEFING.md` (the Advisor's cockpit).

## If you are a developer: from zero to your first session

One numbered path, from no account to your first session in the project's repository; keep
it open on Day 0. **Who** says who does the step — *you*, *the Project Advisor*, *the host of
the repository* (named in the roles record), *ask Claude*. The other pages point here instead
of repeating it: [INSTALL.md](kit/INSTALL.md) adds the prerequisites by platform, what is
shared or personal and what `check.sh` says; [ONBOARDING.md](kit/ONBOARDING.md) the method
in one page, your first session step by step and the checklists.

| # | Step | Who | Do | Check |
|---|---|---|---|---|
| 0a | **A GitHub account, and a way to sign in from the terminal** | you | an account on github.com with your professional e-mail; then `gh auth login` (the GitHub command-line tool, from https://cli.github.com — it sets up HTTPS or SSH for you) or, by hand, an SSH key (`ssh-keygen -t ed25519`, the public key pasted under Settings › SSH and GPG keys) | `gh auth status` says logged in, or `ssh -T git@github.com` greets you by name |
| 0b | **Git and a terminal** | you | macOS: `xcode-select --install` (Git and the command-line tools), or Homebrew's `brew install git`; Windows: Git for Windows from https://git-scm.com (it brings **Git Bash**: use it for every command of this page); Linux: your package manager. Then `git config --global user.name "Firstname Lastname"` and `git config --global user.email "you@…"` | `git --version` prints a version; `git config --global user.name` prints your name |
| 0c | **Python 3** (3.10 or later; the method's scripts need it) | you | macOS: comes with the command-line tools, or `brew install python`; Windows: the installer from https://python.org or `winget install Python.Python.3.12` (tick "Add to PATH"); Linux: your package manager | `python3 --version` prints 3.10 or later |
| 0d | **One rule before any environment** | you | nothing to install for the method itself. If your clones will live in a synced folder (Dropbox, OneDrive, iCloud Drive…), every Python environment of the product goes to `~/.venvs/<name>` and the repository holds a link — [`scripts/README.md` §0](scripts/README.md#0-the-rule-for-every-environment-on-every-machine); Node.js only if you choose the `npm` installer of Claude Code at step 4 (the native installer needs nothing) | — |
| 1 | **Your machine, checked** | you | the details by platform and the troubleshooting: [INSTALL.md §1](kit/INSTALL.md#1-prerequisites-everyone) | `git --version`, `python3 --version` and `gh auth status` all answer |
| 2 | **Your Claude seat** | the Project Advisor | invites you to his Claude team: an invitation to your e-mail address, or an identity on his organisation's domain (he gives you the address and a one-time password; you sign in once and set your password) | the mail "You've been invited to join … on Claude" is in that mailbox |
| 3 | **Accept the seat** | you | the mail's **Accept invitation** — or https://claude.ai/login › **Continue with Google** when the identity is a Google one | claude.ai opens in the Advisor's organisation (bottom-left menu); never a personal account |
| 4 | **Claude Code** | you | install it from https://claude.com/claude-code (the installer, or `npm install -g @anthropic-ai/claude-code`); open a new terminal; `claude` › **Claude account with subscription** (never *Anthropic Console account*) › **Authorize** in the browser | `claude --version` prints a version; no `/logout` afterwards |
| 5 | **GitHub access** | the host of the repository | access on `<project-repo>` (write for a team member; the roles record says who hosts it); you accept the invitation GitHub mails you | the repository opens on github.com under your account |
| 6 | **Two clones side by side** | you | `mkdir -p ~/dev/<project> && cd ~/dev/<project>` · `git clone https://github.com/nicolasguelfi/gse-light.git` · `git clone <project-repo URL>` | `ls` shows `gse-light` and `<project-repo>` |
| 7 | **Your `.env`** | you | `cd <project-repo>` · `cp .env.example .env`, then fill it with what the project lead gives you | `git status --short` never lists `.env` |
| 8 | **Check** | you | `../gse-light/kit/check.sh` | every line OK, no MISSING line — or it says what to do |
| 9 | **The gates, once** | you | `./gates.sh` | prints *no gates yet: design phase in progress* (the Day-0 stub) until the design phase fills it |
| 10 | **Your Day-0 branch** | you | `git switch -c day0-<firstname>` — your first session's commits go there; merged or deleted after | `git branch --show-current` prints it |
| 11 | **First session and `/upskilling`** | you | `claude`; accept the workspace trust dialog; the start hook prints the week's situation; type `/` — your six skills appear; `/upskilling` (ten minutes of questions, a short personal plan) | your plan is in `~/.claude/upskilling/<project>/record.md`, outside the repository |
| 12 | **Read** | you | the reference design chapters 0, 1, 2 and 13; the `CLAUDE.md` of the project's repository; `project/README.md`; then your first session step by step — [ONBOARDING.md §3b](kit/ONBOARDING.md#3b-your-first-session-step-by-step-30-minutes) | you can say in five lines how a session works here: gates, registers, go-aheads |
| 13 | **Close the session** | ask Claude | *"Close the session"* (skill `session-close`) | your first journal entry is in `project/journal/`, committed by the skill; push on your word |
| 14 | **Work** | you, ask Claude | a ticket, a feature branch with its tests, `./gates.sh`, the `change-reviewer` agent, the pull request, *"Close the session"* — the table "All project long" below | — |

Steps 2 and 5 are done for you, at the kick-off or the day you start; everything from step 6
is your own hour, and nothing in it needs the Advisor. You never run `install.sh`: the kit is
in the clone (cloned before it was there? `git pull`).

- **Write**: the code, by pull request on a feature branch with its tests; your journal entry at the end of each session and your new 🔴 records — the skills `session-close` and `decision-record` write them into `project/` for you.
- **Never**: edit `gse-light` from a project session; edit `project/BRIEFING.md`; push to `main` without the go-ahead; commit a secret. A sandbox of your own is optional, for experiments outside the project.

## If you are the product owner

- **Read**, on GitHub: `project/README.md` (the project, its phase, its people) and the dashboard at the top of each register, where the 🔴 records that await you are listed.
- **Install**: nothing, nothing to clone — the host of the project's repository gives you read access (roles record).
- **Write**: nothing by hand — your decisions and go-aheads are recorded by the team (`decision-record`) and in the meeting minutes; your tasks are in the minutes, per participant.
- **Never**: decide in a chat or a mail only — a decision that is not in a register does not exist for the project.

## If you are the Project Advisor

- **Read first**:
  - [`kit/README.md`](kit/README.md) — the kit: what it installs, the one command, the refresh;
  - then [the Project Advisor's page](method/15-project-advisor.md) — your week: the brief, the meeting, the minutes;
  - your machine: [`scripts/README.md`](scripts/README.md).
- **Install**: the kit in the project's repository, once, at its root — `../gse-light/kit/install.sh` — then commit and push; the same command refreshes it after every change in `gse-light`. Your sessions open there, like everyone's; `.claude/settings.local.json` (yours, never committed) allows you `project/BRIEFING.md`.
- **Write**: the cockpit `project/BRIEFING.md`, the meeting briefs and the draft minutes with your feedback section (the project lead validates and sends them), `project/README.md` and the governance pages, your journal, the method in `gse-light`.
- **Never**: decide in the project; write a client or project name in `gse-light` (the leak guard — `check_docs.py` — refuses it); write in a team member's name.

## All project long — when, what

Who does it: *you*, *ask Claude* (say it in the session), *automatic*.

| When | What | Who |
|---|---|---|
| Start of a session | `claude` in the project's repository; it reads `CLAUDE.md` (rules, commands, the project folder `project/` where your decisions and journal go) and the start hook prints the week's situation | automatic |
| W1 — design phase | in the project's repository, *"Run design-phase"*: the project's drivers → `DD` records — twelve decisions, in order: repository layout, hosting, environments and promotion path, stack and language, data store, identity, infrastructure as code, continuous integration, test tools, secrets, dependency updates, monitoring — → `gates.sh`, the CI and the `<…>` fields of `CLAUDE.md` filled from them | ask Claude + project lead |
| Taking a ticket | *"Read ticket #N, its requirement and its example; restate what is asked"* | ask Claude |
| A choice with consequences | *"Record it with decision-record"* — a 🔴 record in `project/`, committed by the skill; the person who holds the right decides | ask Claude |
| Before stating a fact (version, count, test result, cause) | `verify-claim`: the command and its output, never a guess | ask Claude |
| Writing code | on a feature branch, with its tests; a user path gets its **end-to-end test through the real user interface**, driven by Claude to play the use case (the tool from the test-tools `DD`; Playwright is one example for a web interface); run `./gates.sh`; read the diff yourself | ask Claude + you |
| Before a pull request | *"Run the change-reviewer agent"*; fix what it lists; the PR updates the document of the behaviour | ask Claude |
| Merging | gates green in CI (`bash ./gates.sh`), the documentation checks green (`docs.yml`), review by a person; the rehearsal environment and production only with the go-ahead in the roles record | automatic + a person |
| End of a session | *"Close the session"* (`session-close`): journal entry and metrics row in `project/journal/`, committed by the skill — a colleague with no memory must be able to resume | ask Claude |
| Stuck with Claude or a technology | `/upskilling` again: it re-checks and adjusts your plan | you |
| Every sprint | sprint file `project/planning/sprints/W<n>.md`; meeting with the Advisor (weekly; a part-time period may hold fewer), who reads the merged PRs, gates and journal — link your tickets and write your journal | project lead + you |
| When `check.sh` says *kit version … the kit in gse-light is at …* | *you*: `git pull` in `gse-light` and in `<project-repo>`; if the line stays, the Advisor reruns the one command and pushes | you, then the Project Advisor |
| Last week | hand-over document and last journal entry; retrospective, lessons kept in the method | ask Claude + the team |

## Never

- a secret in a file under git (`.env` is yours alone);
- a push to `main`, or to any branch that deploys, without the go-ahead;
- a claim about a running system without its command;
- a decision that lives only in a chat;
- editing `project/BRIEFING.md` (the Advisor's cockpit);
- editing `gse-light` from a project session;
- running `install.sh` yourself (the Advisor installs and refreshes the kit; you clone and pull).

## Read next

- [ONBOARDING.md](kit/ONBOARDING.md) — the words used, the method in one page, your first session step by step, the Day-0 and first-sprint checklists;
- [reference design](method/00-reference-design.md) — the method's page of rules for building, testing, delivering and running a product — chapters 0 (purpose and how to read it), 1 (principles), 2 (how people and AI share the decisions) and 13 (working with the AI day to day); the project lead adds 15 (the start-of-project checklist);
- [GLOSSARY.md](GLOSSARY.md) — every word and acronym above (`DD`, gate, go-ahead, sandbox…) in plain words.

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))
