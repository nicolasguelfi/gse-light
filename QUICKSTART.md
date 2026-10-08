# Quick start — what gse-light does for you and what to use, all project long

Status: v0.4 · 2026-10-08 · one page, a section per role; details in [INSTALL.md](claude-kit/INSTALL.md) and [ONBOARDING.md](claude-kit/ONBOARDING.md)

## What gse-light does for you

This page is the one-page start of a project run with `gse-light`, written first for the
team members — the project lead or a developer: what the method does for your Claude Code
sessions, which repositories you clone, your Day 0 in the section of your role, then what to
use all project long; the product owner and the Project Advisor have their short section.
`gse-light` is the method your project runs with: you clone it once, next to the
project-management repository `<pm-repo>` and the product repositories, and never change it.
It gives your sessions a few firm habits — measure before asserting, decisions in registers,
nothing state-changing without a go-ahead (the written yes of the person who holds that
right, named in the roles record), a journal entry per session, end-to-end tests through the
real user interface — through a **kit** committed in each product repository and in your sandbox.

> **Words used here** — *Day 0*: each person's first hour on the project — clone, kit, `.env`, `check.sh`, first session.
> *Project-management repository* `<pm-repo>`: the project's shared record — decisions, requirements, plans, minutes, journal — private, one per project; everyone reads it, each person writes their own part in it through the kit's skills; nobody manages the project from it.
> *Instance*: one project run with the method, and its folder `instances/<instance>/` in `<pm-repo>`.
> *Product repository* `<product-repo>`: the code, private, one or several (repository layout, the first design decision); the kit is committed in it.
> *Register*: one document per kind of decision — project `PD`, requirements `DEC`, design `DD` — one numbered record per decision, a dashboard at the top.
> *Decision record and badges*: every `PD-NN`, `DEC-NNN` or `DD-NN` in these pages is one numbered decision record, with a status badge: 🔴 pending, 🟢 decided, 🟡 provisional; its *decider* is the person the roles record names for it, the only one who turns it 🟢.
> *Kit*: the files that make every Claude Code session in a repository follow the method — `CLAUDE.md`, five skills (`design-phase`, `decision-record`, `session-close`, `verify-claim`, `upskilling`: procedures Claude runs when asked, `/name`), one agent (`change-reviewer`, a read-only helper Claude launches), permissions, a `gates.sh` stub, a CI workflow that runs it (`bash ./gates.sh`) — installed with one command, committed with the code.
> *Gates*: the project's automated checks (tests, lint, end-to-end) run by `gates.sh` and the CI before a merge; on Day 0 a stub that says "no gates yet".
> *Sandbox*: a personal, private, throwaway repository `<project>-sandbox-<firstname>` with the kit, for Day 0 and experiments until the product repositories exist; the project lead's sandbox hosts the design phase.
> *Placeholders* `<instance>`, `<pm-repo>`, `<product-repo>`, `<project>`, `<firstname>`: stand for the project's real names; `<instance>` is the folder name under `instances/` (`ls ../<pm-repo>/instances` shows it; the project lead gives it). Every other term: [GLOSSARY.md](GLOSSARY.md).

```text
~/dev/<project>/                      one parent folder, the clones side by side
├── gse-light/        the method (public) — read by every session, changed by none
├── <pm-repo>/        project management (private): instances/<instance>/ — registers,
│                     journal, sprints, the Project Advisor's cockpit BRIEFING.md
├── <product-repo>/   the code (private) — you work here; the kit is committed in it
└── <project>-sandbox-<firstname>/   your sandbox (private, throwaway): Day 0 and your
                      experiments, and the stand-in for <product-repo> until it exists
```

**Prerequisites**: Git, a bash terminal (Git Bash on Windows; the scripts keep Unix line
endings there), `python3`, Claude Code signed in with the invited account, access on GitHub
to `<pm-repo>` (from the host of `<pm-repo>`, named in the roles record) and to
`<product-repo>` or your sandbox (from the project lead). The method needs no Python
environment on your machine; the product's own environments follow one rule on a machine
with a synced folder (Dropbox, OneDrive…): the environment lives in `~/.venvs/<name>`, the
product repository holds a link — commands in [`scripts/README.md`](scripts/README.md) §0.

<!-- who-is-who:start -->
**Who is who.** The **client** is the organisation the product is built for; it names the **product owner** (owns the need, accepts each delivered increment, gives the production and budget go-aheads) and the **data protection contact** (decides how personal data may enter the product). The **project lead** (lead developer) runs the project inside the team: sprints, tickets, technical choices, code review; the developers' first contact. The **developers** build the product with Claude Code, each in their own repository; "team member" means the project lead or a developer. The **Project Advisor** is outside the team: the method's author, two hours of meeting and two hours of preparation a week; gives feedback and advice, decides nothing in the project. **Claude sessions** propose, measure, write and test; they decide nothing and act on a go-ahead. Who decides what in a given project: its **roles record**, `<pm-repo>/instances/<instance>/governance/10-roles-and-go-aheads.md`.
<!-- who-is-who:end -->

## Which repositories you clone, by role

| Role | Clones | Why |
|---|---|---|
| Developer | your sandbox or the product repository · `gse-light` · `<pm-repo>` | your Claude sessions read the method's rules in `../gse-light` and write your own journal entries and pending records in `../<pm-repo>`; you do not manage the project from there |
| Project lead | the same three (his sandbox hosts the design phase) | plus the sprints in `<pm-repo>` |
| Project Advisor | `<pm-repo>` · `gse-light` (+ the product repositories as additional directories for the overall view) | his sessions run in `<pm-repo>` |
| Product owner | none | reads on GitHub |

Your sessions **read** the method in `../gse-light` and **write** your journal entries and records
in `../<pm-repo>/instances/<instance>/`: both are additional directories in the kit's `settings.json`,
which also denies Claude the Edit tool under `../gse-light/**` and on `BRIEFING.md` (the Advisor's
cockpit: his one-page dashboard in the instance) and the literal `git push origin main`; Claude asks
before any `git push`. Conveniences for the session, not a security boundary: what guards the method,
the cockpit and `main` is review by a person and, when the project has enabled it in its roles record, GitHub branch protection on `main`.

- **Known limit**: a Claude Code session started on claude.ai (the web or cloud version) works in
  an isolated container with **one** GitHub repository cloned into it; it sees neither `../gse-light`
  nor `../<pm-repo>`, so the rules, the registers and the journal are out of its reach. Work locally, where the clones are side by side.
- **A product made of several repositories**: the kit is installed **in each** product repository
  (same one command); the instance `README.md` in `<pm-repo>` lists them (decided in the design phase,
  repository-layout `DD`). For an overall view, the Advisor opens Claude Code in `<pm-repo>` with the
  product repositories as additional directories (`claude --add-dir ../<repo-a> --add-dir ../<repo-b>`).

## If you are the project lead: once per product repository

**Read first**: [the Project Advisor's page](method/15-project-advisor.md) — who is in the project,
the weeks, the weekly meeting; [INSTALL.md](claude-kit/INSTALL.md), its project-lead section;
the reference design chapters in "Read next", plus chapter 15. **Your sandbox first** (*you*):
the same commands as a developer's sandbox (next section). Yours also hosts the design phase,
in W1 (the project's first week): *"Run design-phase"* turns the project's facts and constraints
into twelve `DD` records (listed in the table below, row W1); the first, repository layout,
names the real product repositories, which then receive the kit as follows.

**Then, once per product repository** (*you*, then *ask Claude*). **Step 0 — the product repository
exists on GitHub**, named by the repository-layout `DD`; you or the client's IT create it, empty or
with a README only. If its `main` branch is protected on GitHub (recommended; each project decides it
in its roles record), the kit arrives by pull request instead of a direct push; everything else is the same.

```bash
cd ~/dev/<project>                                         # gse-light and <pm-repo> are already there (your sandbox step)
git clone <product-repo URL>                               # the product repository (empty or README only)
cd <product-repo>
../gse-light/claude-kit/install.sh <instance>              # ONE command; add --pm <pm-repo> if it asks
claude                                                     # then say: "fill CLAUDE.md with this project's purpose and commands"
git add CLAUDE.md .claude .env.example .gitattributes .gitignore .github gates.sh
git commit -m "Install the Claude kit (<instance>)"
git push                                                   # first push on an empty repository: git push -u origin HEAD
```

Then tell the team the kit is in. The command finds `../gse-light` and the sibling folder
that holds `instances/<instance>/` by itself; it asks for `--pm <folder>` only when there are
none or several. **Write**: the sprint file `<pm-repo>/instances/<instance>/planning/sprints/W<n>.md`,
the `DD` records, the review of every pull request. **Never**: open Claude Code in `<pm-repo>`
(a session opened there acts in the Advisor's name); turn a record 🟢 unless the roles record
names you its decider; run `install.sh` for someone else — each developer runs it in their
own sandbox, and nobody but you in a product repository.

## If you are a developer: your sandbox

**Read first**: this page; then [INSTALL.md](claude-kit/INSTALL.md) — prerequisites, Windows,
troubleshooting — and [ONBOARDING.md](claude-kit/ONBOARDING.md) — the words used, your first
session step by step, the Day-0 and first-sprint checklists. **Install** (*you*, once the
project lead or the Advisor has created your sandbox on GitHub): until the product
repositories exist, every team member works in their sandbox `<project>-sandbox-<firstname>`,
with the kit installed by the one command — here **you** run it, it is your repository:

```bash
mkdir -p ~/dev/<project> && cd ~/dev/<project>
git clone https://github.com/nicolasguelfi/gse-light.git   # the gse-light repository (the method)
git clone <pm-repo URL>                                    # the project-management repository
git clone <sandbox URL>                                    # your sandbox <project>-sandbox-<firstname>
cd <project>-sandbox-<firstname>
../gse-light/claude-kit/install.sh <instance>              # ONE command; add --pm <pm-repo> if it asks
git add CLAUDE.md .claude .env.example .gitattributes .gitignore .github gates.sh
git commit -m "Install the Claude kit (<instance>)" && git push -u origin HEAD
cp .env.example .env                                       # your keys, never committed
../gse-light/claude-kit/check.sh                           # every line OK, or it says what to do
claude                                                     # type /, run /upskilling, then experiment
```

`/upskilling` is the kit's self-assessment of your starting level, with a personal plan; its record
stays in your sandbox. **Write**: your journal entry at the end of each session and your new 🔴
records — the skills `session-close` and `decision-record` push them to `<pm-repo>/instances/<instance>/`
for you, from the sandbox as from any product repository. **Never**: open Claude Code in `<pm-repo>` —
the sessions opened there are the Advisor's. Your sandbox stays yours for experiments afterwards (next section).

## If you are a developer: a product repository that already has the kit

(*you*, once the project lead has pushed the kit):

```bash
cd ~/dev/<project>                                         # gse-light and <pm-repo> are already there (your sandbox step)
git clone <product-repo URL>                               # the product repository, kit included
cd <product-repo> && cp .env.example .env                  # your keys, never committed
../gse-light/claude-kit/check.sh                           # every line OK, or it says what to do
```

Then `claude` in the product repository, type `/` (the five skills appear), run `/upskilling`
if you have not done it in your sandbox. **Write**: the code, by pull request on a feature
branch with its tests; your journal entries and 🔴 records as from your sandbox. **Never**:
run `install.sh` in a product repository (if you cloned before the kit was there: `git pull`
once the project lead has pushed); edit `gse-light` from a project session; push to `main`
without the go-ahead; commit a secret.

## If you are the product owner

Nothing to install, nothing to clone: you read on GitHub — `<pm-repo>/instances/<instance>/README.md`
(the project, its phase, its people) and the dashboard at the top of each register, where the 🔴 records
that await you are listed. You write nothing by hand: your decisions and go-aheads are recorded by the
team (`decision-record`) and in the meeting minutes. Never decide in a chat or a mail only: a decision that is not in a register does not exist for the project.

## If you are the Project Advisor

**Read first**: [`pm-kit/README.md`](pm-kit/README.md) — create `<pm-repo>` and install the pm-kit,
one command — then [the Project Advisor's page](method/15-project-advisor.md) — your week: the brief,
the meeting, the minutes; your machine: [`scripts/README.md`](scripts/README.md). **Install**: the pm-kit
in `<pm-repo>`; your sessions run there, the only ones that do. **Write**: the cockpit `BRIEFING.md`, the
meeting briefs and minutes, your journal, the method in `gse-light`. **Never**: decide in the project;
write a client or project name in `gse-light` (the leak guard — `check_docs.py` — refuses it); write in a team member's name.

## All project long — when, what

Who does it: *you*, *ask Claude* (say it in the session), *automatic*.

| When | What | Who |
|---|---|---|
| Start of a session | `claude` in the product repository (or your sandbox); it reads `CLAUDE.md`: rules, commands and the **project's zone** — `../<pm-repo>/instances/<instance>/`, the folder where your decisions and journal go | automatic |
| W1 — design phase | in the project lead's sandbox, *"Run design-phase"*: the project's drivers → `DD` records — twelve decisions, in order: repository layout, hosting, environments and promotion path, stack and language, data store, identity, infrastructure as code, continuous integration, test tools, secrets, dependency updates, monitoring; the first names the product repositories — → in each product repository, `gates.sh`, the CI and the `<…>` fields of `CLAUDE.md` filled from them | ask Claude + project lead |
| Taking a ticket | *"Read ticket #N, its requirement and its example; restate what is asked"* | ask Claude |
| A choice with consequences | *"Record it with decision-record"* — a 🔴 record in `<pm-repo>`, pushed by the skill; the person who holds the right decides | ask Claude |
| Before stating a fact (version, count, test result, cause) | `verify-claim`: the command and its output, never a guess | ask Claude |
| Writing code | on a feature branch, with its tests; a user path gets its **end-to-end test through the real user interface**, driven by Claude to play the use case (the tool from the test-tools `DD`; Playwright is one example for a web interface); run `./gates.sh`; read the diff yourself | ask Claude + you |
| Before a pull request | *"Run the change-reviewer agent"*; fix what it lists; the PR updates the document of the behaviour | ask Claude |
| Merging | gates green in CI (`bash ./gates.sh`), review by a person; the rehearsal environment and production only with the go-ahead in the roles record | automatic + a person |
| End of a session | *"Close the session"* (`session-close`): journal entry and metrics row in `<pm-repo>`, pushed by the skill — a colleague with no memory must be able to resume | ask Claude |
| Stuck with Claude or a technology | `/upskilling` again: it re-checks and adjusts your plan | you |
| Every sprint | sprint file `<pm-repo>/instances/<instance>/planning/sprints/W<n>.md`; meeting with the Advisor (weekly; a part-time period may hold fewer), who reads the merged PRs, gates and journal — link your tickets and write your journal | project lead + you |
| When `check.sh` says *kit version … the kit in gse-light is at …* | *you*: `git pull` in `gse-light` and in `<product-repo>`; if the line stays, the project lead reruns the one command in `<product-repo>` and pushes | you, then the project lead |
| Last week | hand-over document and last journal entry; retrospective, lessons kept in the method | ask Claude + the team |

## Never

A secret in a file under git (`.env` is yours alone) · a push to `main`, or to any branch that
deploys, without the go-ahead · a claim about a running system without its command · a decision
that lives only in a chat · editing `BRIEFING.md` (the Advisor's cockpit) · editing
`gse-light` from a project session · opening Claude Code in `<pm-repo>` (your journal and
records get there through the skills).

## Read next

[ONBOARDING.md](claude-kit/ONBOARDING.md) — the words used, the method in one page, your first
session step by step, the Day-0 and first-sprint checklists · [reference design](method/00-reference-design.md)
— the method's page of rules for building, testing, delivering and running a product — chapters 0 (purpose
and how to read it), 1 (principles), 2 (how people and AI share the decisions) and 13 (working with the AI
day to day); the project lead adds 15 (the start-of-project checklist) · [GLOSSARY.md](GLOSSARY.md) — every word and acronym above (`DD`, gate, go-ahead, sandbox…) in plain words.

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))
