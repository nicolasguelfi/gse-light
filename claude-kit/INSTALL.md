# Installing the kit — project lead once, developers by cloning

Status: v0.3 · 2026-10-08 · maintained by the Project Advisor (NG)

> **Essentials** — Three repositories, cloned **side by side** in one parent folder:
> the **`gse-light` repository** (this method and its kits; public), the project's
> **project-management repository `<pm-repo>`** (its instance folder `instances/<instance>/`:
> registers, cockpit, journal, sprints; private) and the **product repository
> `<product-repo>`** (the code; private). The kit lives **in `<product-repo>`**, committed like
> the code: the project lead installs it with **one command run from inside the product
> clone**, once per product repository, and commits it; a developer gets it simply **by
> cloning `<product-repo>`**, then does three personal steps. Everything personal stays out
> of all three repositories. This follows the Claude Code documentation: `.claude/` and
> `CLAUDE.md` are the team's shared rules; each person's data lives in their own `~/.claude/`.
> The one-page version: [QUICKSTART.md](../QUICKSTART.md).

## 0. Shared and personal

| What | Where | In git? |
|---|---|---|
| Rules for the whole team: `CLAUDE.md`, `.claude/settings.json`, `.claude/skills/`, `.claude/agents/`, `.claude/KIT_LICENSE.md`, `.claude/KIT_VERSION` | `<product-repo>` | **yes** — committed by the project lead |
| The gates: `gates.sh` (a Day-0 stub until the design phase fills it) and the CI workflow `.github/workflows/gates.yml` that runs it | `<product-repo>` | **yes** — committed by the project lead, filled in week 1 |
| `.gitattributes` (`*.sh text eol=lf`: keeps `gates.sh` runnable from a Windows clone) and `.env.example` | `<product-repo>` | **yes** |
| Your keys and settings: `.env` | `<product-repo>` (your clone) | **no** (git-ignored by the kit) |
| Your personal instructions: `CLAUDE.local.md`; your personal permissions: `.claude/settings.local.json` | `<product-repo>` (your clone) | **no** (the kit ignores the first; Claude Code excludes the second itself) |
| Your sessions, Claude's memory of you, your personal skills | `~/.claude/` on your machine | **no** — never in any repository |
| Your upskilling record (answers, plan) | `~/.claude/upskilling/<instance>/record.md` | **no** — in your home folder, one sub-folder per project |
| What you produce for the project: journal entries, new 🔴 decision records | the `<pm-repo>` repository, `instances/<instance>/` | **yes**, on purpose, under your name — committed and pushed by `session-close` and `decision-record` (those paths only) |

## 1. Prerequisites (everyone)

| Need | macOS | Windows |
|---|---|---|
| Git, and access on **GitHub** to `<pm-repo>` (write: your journal entries and 🔴 records) and `<product-repo>` (SSH key or GitHub CLI login); `gse-light` is public. GitHub is a prerequisite of the method's own tooling (pull requests, CI, the Project Advisor's brief) | Xcode command-line tools or Homebrew `git` | Git for Windows (it brings **Git Bash**) |
| A bash terminal for `install.sh`, `check.sh` and `gates.sh` | Terminal | Git Bash or WSL |
| **`python3`** (3.10 or later) for the method's scripts (`check_docs.py`, the situation hook) | Xcode command-line tools or Homebrew `python` | python.org installer or `winget install Python.Python.3.12` |
| **Claude Code**, signed in with the account the Project Advisor invited | desktop app, or the CLI (`npm install -g @anthropic-ai/claude-code`, which needs Node.js) | same |

Check: `git --version`, `python3 --version` and `claude --version` each print a version.

## 2. Project lead — install the kit in the product repository `<product-repo>` (once per product repository)

**Step 0 — the repository exists on GitHub.** You or the client's IT create
`<product-repo>`, empty or with a README only. If its `main` branch is protected, the kit
arrives by pull request (see below); nothing else changes.

```bash
mkdir -p ~/dev/<project> && cd ~/dev/<project>            # the parent folder of the three repositories
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
| `.claude/settings.json` | additional directories `../gse-light` and `../<pm-repo>`; deny rules: no edit under `../gse-light/**`, none of `../<pm-repo>/instances/<instance>/BRIEFING.md`, no push to `main` |
| `.claude/skills/` (`design-phase`, `decision-record`, `session-close`, `verify-claim`, `upskilling`), `.claude/agents/change-reviewer.md` | the kit's own files, refreshed on every run |
| `gates.sh` | Day-0 stub: prints *no gates yet: design phase in progress* and exits 0; the design phase fills it |
| `.github/workflows/gates.yml` | runs `./gates.sh` on every pull request and on every push to `main` — green from Day 0 |
| `.gitattributes`, `.env.example`, `.gitignore` entries (`.env`, `CLAUDE.local.md`) | line endings, personal files out of git |
| `.claude/KIT_LICENSE.md`, `.claude/KIT_VERSION` | the licence notice and the last `gse-light` commit that touched `claude-kit/` |

Then commit and push:

```bash
git add CLAUDE.md .claude .env.example .gitattributes .gitignore .github gates.sh
git commit -m "Install the Claude kit (<instance>, kit $(cat .claude/KIT_VERSION))"
git push                                                   # first push on an empty repository: git push -u origin HEAD
```

Protected `main`: `git switch -c kit && git push -u origin kit`, then open the pull request
(`gh pr create`); the Day-0 CI runs the stub and is green. Tell the team once the kit is in.

**Week 1 — the design phase** (*ask Claude*, with you): the skill `design-phase` turns the
project's drivers into `DD` records (architecture, repository layout, environments, branch
model, test tools) and fills `gates.sh`, the CI and the `<…>` fields of `CLAUDE.md` from them.
Until then the gates are the stub.

**Refresh** after the kit changes in the `gse-light` repository: `git pull` in `gse-light`,
then rerun the same command from inside `<product-repo>`. It overwrites only the kit's own
skills, agents, licence notice and `KIT_VERSION`; `CLAUDE.md`, `settings.json`, `gates.sh` and
the CI stay yours. When the templates of `CLAUDE.md` or `settings.json` changed since your
`KIT_VERSION`, it prints a warning: compare and carry the change over by hand
(`git -C ../gse-light diff $(cat .claude/KIT_VERSION)..HEAD -- claude-kit/templates/`), then
commit and push in `<product-repo>`. `check.sh` tells each developer when the kit in their
clone of `<product-repo>` is older than `claude-kit/` in their clone of `gse-light`.

A product made of **several repositories**: run the same command in each. The list of the
project's repositories lives in `<pm-repo>/instances/<instance>/README.md` (repository-layout
`DD`); for an overall view, open Claude Code in `<pm-repo>` with the product repositories
added (`claude --add-dir ../<repo-a> --add-dir ../<repo-b>`).

## 3. Developer — get the kit (about 15 minutes)

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
short personal plan). You never run `install.sh` yourself. If you cloned `<product-repo>`
before the kit was there: `git pull` once the project lead has pushed.

Keep the one-page [quick start](../QUICKSTART.md) at hand for the rest of the project; then
continue with the [starting guide](ONBOARDING.md) (§2 the method in one page, §3
your first session).

**Known limit**: a Claude Code session started on claude.ai (web or cloud) clones **one**
GitHub repository into its own sandbox and sees neither `../gse-light` nor `../<pm-repo>`.
Work locally, where the three clones are side by side.

## 4. If something is missing

To rehearse §2 and §3 on your own machine first: [TEST-DAY0.md](TEST-DAY0.md).

| `check.sh` says | Do |
|---|---|
| `MISSING CLAUDE.md` or a skill | the kit is not installed in `<product-repo>`, or not committed: ask the project lead (§2) |
| `MISSING kit committed` | the project lead installed the kit in `<product-repo>` without committing: ask them to commit and push |
| `MISSING gates.sh` | the kit is older than Day-0 CI, or the file was deleted: the project lead reruns the one command (§2) |
| `MISSING python3` | install it (§1): the method's scripts need it |
| `WARN kit version … the kit in gse-light is at …` | the kit was updated in the `gse-light` repository (last commit touching `claude-kit/`, not `HEAD`): the project lead refreshes it in `<product-repo>` (§2) |
| `WARN .gitattributes` | `*.sh text eol=lf` is missing: `gates.sh` may break on a Windows clone; the project lead reruns the one command (§2) |
| `WARN KIT_LICENSE.md` | the licence notice of the kit is missing: the project lead reruns the one command (§2) |
| `MISSING .env not in git` | in your clone of `<product-repo>`: `git rm --cached .env`, then commit |
| `MISSING gse-light next to this repository` | clone the `gse-light` repository in the same parent folder as your clone of `<product-repo>` |
| `MISSING <pm-repo> next to this repository` | clone the project-management repository `<pm-repo>` there too (ask the project lead for access) |

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))
