# Installing the kit — project lead once, developers by cloning

Status: v0.5 · 2026-10-08 · one section per role (project lead, developer, product owner, Project Advisor) · maintained by the Project Advisor

> **Essentials** — How the kit gets into the repositories, and what is shared or personal:
> for the project lead (one command, once per product repository, then a commit — §2), the
> developers (a clone and three personal steps — §3), the product owner (nothing to install
> — §4) and the Project Advisor (the rehearsal and the refresh — §5). Three repositories,
> cloned **side by side** in one parent folder: the **`gse-light` repository** (this method
> and its two kits; public), the **project-management repository `<pm-repo>`** (the
> project's shared record — decisions, requirements, plans, minutes, journal — private, one
> per project: everyone reads it, each person writes their own part in it through the kit's
> skills; nobody manages the project from it) and the **product repository
> `<product-repo>`** (the code; private; one or several, named by the first design
> decision). The kit lives **in `<product-repo>`**, committed like the code. **No product
> repository yet?** Your **sandbox** `<project>-sandbox-<firstname>` plays `<product-repo>`
> for Day 0 — there you run the one command yourself (§3). Nobody but the Project Advisor
> opens Claude Code in `<pm-repo>`. Everything personal stays out of all the repositories,
> as the Claude Code documentation has it: `.claude/` and `CLAUDE.md` are the team's
> shared rules; each person's data lives in their own `~/.claude/`. The one-page version:
> [QUICKSTART.md](../QUICKSTART.md).

> **Words used here** — *Kit*: the files that make every Claude Code session in a
> repository follow the method — `CLAUDE.md`, five skills, one agent, permissions, a
> `gates.sh` stub, a CI workflow — installed with one command, committed with the code; two
> kits: this `claude-kit` for product and sandbox repositories, the `pm-kit` for the Project
> Advisor in `<pm-repo>`. *Instance*: one project run with the method, and its folder
> `instances/<instance>/` in `<pm-repo>`. *Placeholders* `<instance>`, `<pm-repo>`,
> `<product-repo>`, `<project>`, `<firstname>`: the project's real names; `<instance>` is
> the folder name under `instances/` (`ls ../<pm-repo>/instances` shows it; the project
> lead gives it). *Sandbox*: a personal, private, throwaway repository
> `<project>-sandbox-<firstname>` with the kit, created on GitHub by the project lead or the
> Project Advisor, for Day 0 and experiments until the product repositories exist; the
> project lead's sandbox hosts the design phase. *Day 0*: each person's first hour on the
> project — clone, kit, `.env`, `check.sh`, first session. *Gates*: the project's automated
> checks (tests, lint, end-to-end) run by `gates.sh` and the CI before a merge; on Day 0 a
> stub that says "no gates yet". *Design phase*: the step of W1 (the first project week)
> where the project lead, with Claude, turns the project's facts and constraints into
> twelve technical decisions (`DD` records), in order: repository layout, hosting,
> environments and promotion path, stack and language, data store, identity,
> infrastructure as code, continuous integration, test tools, secrets, dependency updates,
> monitoring — recorded with the skill `design-phase`. *Decision record and badges*: every
> `PD-NN`, `DEC-NNN` or `DD-NN` in these pages is one numbered decision record, with a
> status badge — 🔴 pending, 🟢 decided, 🟡 provisional; its *decider* (the person the roles
> record names) is the only one who turns it 🟢. *Cockpit*: `BRIEFING.md`, the Project
> Advisor's one-page dashboard in the instance, written by his sessions only. *Go-ahead*:
> the written yes of the person who holds that right (roles record), before any
> state-changing action (push to a branch that deploys, deploy, spend). Every other term:
> [GLOSSARY.md](../GLOSSARY.md).

<!-- who-is-who:start -->
**Who is who.** The **client** is the organisation the product is built for; it names the **product owner** (owns the need, accepts each delivered increment, gives the production and budget go-aheads) and the **data protection contact** (decides how personal data may enter the product). The **project lead** (lead developer) runs the project inside the team: sprints, tickets, technical choices, code review; the developers' first contact. The **developers** build the product with Claude Code, each in their own repository; "team member" means the project lead or a developer. The **Project Advisor** is outside the team: the method's author, two hours of meeting and two hours of preparation a week; gives feedback and advice, decides nothing in the project. **Claude sessions** propose, measure, write and test; they decide nothing and act on a go-ahead. Who decides what in a given project: its **roles record**, `<pm-repo>/instances/<instance>/governance/10-roles-and-go-aheads.md`.
<!-- who-is-who:end -->

## 0. Shared and personal (everyone)

| What | Where | In git? |
|---|---|---|
| Rules for the whole team: `CLAUDE.md`, `.claude/settings.json`, `.claude/skills/`, `.claude/agents/`, `.claude/KIT_LICENSE.md`, `.claude/KIT_VERSION` | `<product-repo>` | **yes** — committed by the project lead |
| The gates: `gates.sh` (a Day-0 stub until the design phase fills it) and the CI workflow `.github/workflows/gates.yml` that runs it (`bash ./gates.sh`) | `<product-repo>` | **yes** — committed by the project lead, filled in W1 (the design phase) |
| `.gitattributes` (`*.sh text eol=lf`: keeps `gates.sh` runnable from a Windows clone) and `.env.example` | `<product-repo>` | **yes** |
| Your sandbox `<project>-sandbox-<firstname>`: the same kit, installed and committed by **you**; Day 0, `/upskilling` (the kit's self-assessment skill, with a personal plan), experiments | its own private repository on GitHub, cloned next to the others | **yes**, in the sandbox only — throwaway |
| Your keys and settings: `.env` | `<product-repo>` (your clone) | **no** (git-ignored by the kit) |
| Your personal instructions: `CLAUDE.local.md`; your personal permissions: `.claude/settings.local.json` | `<product-repo>` (your clone) | **no** (the kit ignores the first; Claude Code excludes the second itself) |
| Your sessions, Claude's memory of you, your personal skills | `~/.claude/` on your machine | **no** — never in any repository |
| Your upskilling record (answers, plan) | `~/.claude/upskilling/<instance>/record.md` | **no** — in your home folder, one sub-folder per project |
| What you produce for the project: journal entries, new 🔴 decision records | the `<pm-repo>` repository, `instances/<instance>/` | **yes**, on purpose, under your name — committed and pushed by `session-close` and `decision-record` (those paths only), from a product repository or your sandbox alike |

## 1. Prerequisites (everyone)

| Need | macOS | Windows |
|---|---|---|
| Git, and access on **GitHub** (HTTPS with a personal access token, or an SSH key) to `<pm-repo>` (write: your journal entries and 🔴 records — from the host of `<pm-repo>`, named in the roles record) and to `<product-repo>` or your sandbox (from the project lead); `gse-light` is public. GitHub is a prerequisite of the method's own tooling (pull requests, CI, the Project Advisor's brief) | Xcode command-line tools or Homebrew `git` | Git for Windows (it brings **Git Bash**) |
| A bash terminal for `install.sh`, `check.sh` and `gates.sh` | Terminal | Git Bash or WSL |
| **`python3`** (3.10 or later) for the method's scripts (`check_docs.py` — from a product repository: `python3 ../gse-light/scripts/check_docs.py ../<pm-repo>` — and the start hook, the small script that prints where the project stands when a session opens in `<pm-repo>`) | Xcode command-line tools or Homebrew `python` | python.org installer or `winget install Python.Python.3.12` |
| **Claude Code**, signed in with the account the Project Advisor invited | desktop app, or the CLI (`npm install -g @anthropic-ai/claude-code`, which needs Node.js) | same |

Check: `git --version`, `python3 --version` and `claude --version` each print a version.

**Windows is covered**: the `gse-light` repository tracks a `.gitattributes` (`*.sh` and
`*.py` with `eol=lf`), and the kit writes one in `<product-repo>`, so the scripts keep Unix
line endings on a Windows clone whatever your `core.autocrlf`; run them from Git Bash.

## 2. If you are the project lead — install the kit in the product repository, once per product repository

**Step 0 — the product repository exists on GitHub.** The design phase, run in your own
sandbox (§3), names the product repositories in its first decision (repository layout).
You or the client's IT create each one, empty or with a README only. If its `main` branch
is protected on GitHub (branch protection — recommended; the project decides it in its
roles record), the kit arrives by pull request (see below); nothing else changes.

```bash
mkdir -p ~/dev/<project> && cd ~/dev/<project>            # the parent folder of the repositories
git clone https://github.com/nicolasguelfi/gse-light.git  # the gse-light repository (method, kits), if not there yet
git clone <pm-repo URL>                                    # the project-management repository <pm-repo>, if not there yet
git clone <product-repo URL>                               # the product repository <product-repo>
cd <product-repo>
../gse-light/claude-kit/install.sh <instance>              # the one command; add --pm <pm-repo> if it asks
```

The command looks for `../gse-light` and for the sibling folder that holds
`instances/<instance>/`; it requires `--pm <folder>` when it finds none or several. It writes:

| Created | What it is |
|---|---|
| `CLAUDE.md` | the rules, with `<instance>` and `<pm-repo>` filled; the `<…>` fields (purpose, commands) are yours — **ask Claude**: `claude`, then *"fill CLAUDE.md with this project's purpose and commands"* |
| `.claude/settings.json` | additional directories `../gse-light` and `../<pm-repo>`; the Edit tool denied under `../gse-light/**` and on `../<pm-repo>/instances/<instance>/BRIEFING.md` (the cockpit); the literal command `git push origin main` denied; Claude asks before any `git push`. Conveniences for the session, not a security boundary: `main` is protected on GitHub (branch protection) in every repository |
| `.claude/skills/` (`design-phase`, `decision-record`, `session-close`, `verify-claim`, `upskilling`), `.claude/agents/change-reviewer.md` | the kit's own files, refreshed on every run |
| `gates.sh` | Day-0 stub: prints *no gates yet: design phase in progress* and exits 0; the design phase fills it |
| `.github/workflows/gates.yml` | runs `bash ./gates.sh` on every pull request and on every push to `main` — green from Day 0 |
| `.gitattributes`, `.env.example`, `.gitignore` entries (`.env`, `CLAUDE.local.md`) | line endings, personal files out of git |
| `.claude/KIT_LICENSE.md`, `.claude/KIT_VERSION` | the licence notice and the last `gse-light` commit that touched `claude-kit/` |

Then commit and push:

```bash
git add CLAUDE.md .claude .env.example .gitattributes .gitignore .github gates.sh
git commit -m "Install the Claude kit (<instance>, kit $(cat .claude/KIT_VERSION))"
git push                                                   # first push on an empty repository: git push -u origin HEAD
```

Protected `main`: `git switch -c kit && git push -u origin kit`, then open the pull request
on GitHub; the Day-0 CI runs the stub and is green. Tell the team once the kit is in.

**W1 — the design phase** (*ask Claude*, with you, in your sandbox): the skill
`design-phase` turns the project's drivers into the twelve `DD` records (design decisions,
from repository layout to monitoring, in the order given under *Words used here*) and fills
`gates.sh`, the CI and the `<…>` fields of `CLAUDE.md` from them, in each product
repository. Until then the gates are the stub.

**Refresh** after the kit changes in the `gse-light` repository: `git pull` in `gse-light`,
then rerun the same command from inside `<product-repo>`. It overwrites only the kit's own
skills, agents, licence notice and `KIT_VERSION`; `CLAUDE.md`, `settings.json`, `gates.sh` and
the CI stay yours. When the templates of `CLAUDE.md` or `settings.json` changed since your
`KIT_VERSION`, it prints a warning naming the template and the exact command to compare,
with the hash of your **previous** `KIT_VERSION` —
`git -C ../gse-light diff <old hash>..HEAD -- claude-kit/templates/<template>` — because
`.claude/KIT_VERSION` already holds the new hash once the command has run. Run it as
printed, carry the change over by hand, then commit and push in `<product-repo>`. `check.sh`
tells each developer when the kit in their clone of `<product-repo>` is older than
`claude-kit/` in their clone of `gse-light`.

A product made of **several repositories**: run the same command in each. The list of the
project's repositories lives in `<pm-repo>/instances/<instance>/README.md` (the Project
Advisor's page: ask him to list them there, from the repository-layout `DD`); for an overall
view, the Project Advisor opens Claude Code in `<pm-repo>` with the product repositories
added (`claude --add-dir ../<repo-a> --add-dir ../<repo-b>`).

**You write** in `<pm-repo>`, besides the records above: the sprints
(`instances/<instance>/planning/sprints/`), your journal entries and your new 🔴 records —
never the cockpit nor the instance `README.md`. **You never** open Claude Code in
`<pm-repo>`: its sessions are the Project Advisor's; your sessions run in your sandbox,
then in the product repositories.

## 3. If you are a developer — get the kit (about 15 minutes)

```bash
mkdir -p ~/dev/<project> && cd ~/dev/<project>
git clone https://github.com/nicolasguelfi/gse-light.git  # the gse-light repository (method, kits)
git clone <pm-repo URL>                                    # the project-management repository <pm-repo>
git clone <product-repo URL>                               # the product repository: the kit comes with it
cd <product-repo>
cp .env.example .env                                       # in your clone of <product-repo>; fill it with what the project lead gives you
../gse-light/claude-kit/check.sh                           # every line OK, or it says what to do
claude                                                     # accept the workspace trust dialog
```

In the session: type `/` and check that `design-phase`, `decision-record`, `session-close`,
`verify-claim` and `upskilling` appear; then run **`/upskilling`** (where you start, and a
short personal plan). You never run `install.sh` in a product repository. If you cloned
`<product-repo>` before the kit was there: `git pull` once the project lead has pushed.

**No product repository yet? your sandbox.** Until the product repositories exist (the first
decision of the design phase names them), every team member works in their sandbox
`<project>-sandbox-<firstname>`, cloned next to `gse-light` and `<pm-repo>`. It plays
`<product-repo>` in the commands above, with one difference: it is yours, so **you** run the
one command in it and commit the kit — `../gse-light/claude-kit/install.sh <instance>`, then
the `git add` and `git commit` lines of §2 — before `cp .env.example .env` and `check.sh`.
Day 0, `/upskilling` and your experiments happen there. **You write**, through the kit's
skills only: your journal entries and 🔴 records, which go to
`<pm-repo>/instances/<instance>/` from the sandbox as from any product repository. The
project lead's sandbox is also where the design phase runs. **You never** open Claude Code
in `<pm-repo>`: the sessions opened there are the Project Advisor's.

Time: about 15 minutes to install, 15 for `/upskilling`, 30 for your first session
([starting guide §3b](ONBOARDING.md)); words you do not know are in the [glossary](../GLOSSARY.md).
Keep the one-page [quick start](../QUICKSTART.md) at
hand for the rest of the project.

**Known limit**: a Claude Code session started on claude.ai (web or cloud) clones **one**
GitHub repository into an isolated container and sees neither `../gse-light` nor
`../<pm-repo>`. Work locally, where the clones are side by side.

## 4. If you are the product owner

Nothing to install, nothing to clone, no Claude Code licence needed. You read `<pm-repo>` on
GitHub: the instance `README.md` (project, phase, people), the roles record (your go-aheads:
production, budget; you accept each delivered increment) and the 🔴 records that await you
in the registers. Your decisions are recorded by the Project Advisor's sessions (🟢 by its
decider, you); the cockpit is his page.

## 5. If you are the Project Advisor

You install nothing in a product repository: you maintain this kit in the `gse-light`
repository and replay the Day-0 rehearsal ([TEST-DAY0.md](TEST-DAY0.md)) after every kit
change. Your own kit is the [pm-kit](../pm-kit/README.md), installed in `<pm-repo>`
(`../gse-light/pm-kit/install.sh .`), where your sessions open — with the product
repositories as additional directories for the overall view (§2). You create the sandboxes
when the project lead asks you to, invite each team member to your Claude team (the
licence) and write the cockpit. You never write a client or project name in `gse-light`
(the leak guard, `check_docs.py`, refuses it), nor open Claude Code in a team member's
sandbox.

## 6. If something is missing

To rehearse §2 and §3 on your own machine first: [TEST-DAY0.md](TEST-DAY0.md).

| `check.sh` says | Do |
|---|---|
| `MISSING CLAUDE.md` or a skill | the kit is not installed in `<product-repo>`, or not committed: ask the project lead (§2) — in your sandbox, run the one command yourself (§3) |
| `MISSING kit committed` | the kit was installed without being committed: the project lead commits and pushes (§2) — in your sandbox, you do |
| `MISSING gates.sh` | the kit is older than Day-0 CI, or the file was deleted: the project lead reruns the one command (§2) |
| `MISSING python3` | install it (§1): the method's scripts need it |
| `MISSING Claude Code` | install it and sign in with the invited account (§1) |
| `WARN kit version … the kit in gse-light is at …` | the kit was updated in the `gse-light` repository (last commit touching `claude-kit/`, not `HEAD`): first `git pull` in `gse-light` and in `<product-repo>` (the project lead may already have refreshed and pushed); if the line stays, the project lead refreshes it in `<product-repo>` (§2) |
| `WARN .gitattributes` | `*.sh text eol=lf` is missing: `gates.sh` may break on a Windows clone; the project lead reruns the one command (§2) |
| `WARN KIT_LICENSE.md` | the licence notice of the kit is missing: the project lead reruns the one command (§2) |
| `WARN .env` | `cp .env.example .env` in your clone, then fill it (§3) |
| `MISSING .env not in git` | in your clone of `<product-repo>`: `git rm --cached .env`, then commit |
| `MISSING gse-light next to this repository` | clone the `gse-light` repository in the same parent folder as your clone of `<product-repo>` |
| `MISSING <pm-repo> next to this repository` | clone the project-management repository `<pm-repo>` there too (ask the host of `<pm-repo>`, named in the roles record, for access) |

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))
