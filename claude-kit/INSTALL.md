# Installing the kit — project lead once, developers by cloning

Status: v0.2 · 2026-10-07 · maintained by the Project Advisor (NG)

> **Essentials** — Three repositories, cloned **side by side** in one parent folder:
> the **`gse-light` repository** (this method and its kits; public), the project's
> **project-management repository `<pm-repo>`** (its instance folder `instances/<instance>/`:
> registers, cockpit, journal, sprints; private) and the **product repository
> `<product-repo>`** (the code; private). The kit lives **in `<product-repo>`**, committed like
> the code: the project lead installs it **once per product repository** and commits it; a
> developer gets it simply **by cloning `<product-repo>`**, then does three personal steps.
> Everything personal stays out of all three repositories. This follows the Claude Code
> documentation: `.claude/` and `CLAUDE.md` are the team's shared rules; each person's data
> lives in their own `~/.claude/`.

## 0. Shared and personal

| What | Where | In git? |
|---|---|---|
| Rules for the whole team: `CLAUDE.md`, `.claude/settings.json`, `.claude/skills/`, `.claude/agents/`, `.claude/KIT_LICENSE.md`, the CI workflow | `<product-repo>` | **yes** — committed by the project lead |
| Your keys and settings: `.env` | `<product-repo>` (your clone) | **no** (git-ignored by the kit) |
| Your personal instructions: `CLAUDE.local.md`; your personal permissions: `.claude/settings.local.json` | `<product-repo>` (your clone) | **no** (the kit ignores the first; Claude Code excludes the second itself) |
| Your sessions, Claude's memory of you, your personal skills | `~/.claude/` on your machine | **no** — never in any repository |
| Your upskilling record (answers, plan) | `~/.claude/upskilling/<instance>/record.md` | **no** — in your home folder, one sub-folder per project |
| What you produce for the project: journal entries, decision records | the `<pm-repo>` repository, `instances/<instance>/` | **yes**, on purpose, under your name |

## 1. Prerequisites (everyone)

| Need | macOS | Windows |
|---|---|---|
| Git, and access on GitHub to `<pm-repo>` and `<product-repo>` (SSH key or GitHub CLI login); `gse-light` is public | Xcode command-line tools or Homebrew `git` | Git for Windows (it brings **Git Bash**) |
| A bash terminal for `install.sh` and `check.sh` | Terminal | Git Bash or WSL |
| **Claude Code**, signed in with the account the Project Advisor invited | desktop app, or the CLI (`npm install -g @anthropic-ai/claude-code`, which needs Node.js) | same |

Check: `git --version` and `claude --version` each print a version.

## 2. Project lead — install the kit in the product repository `<product-repo>` (once per product repository)

```bash
cd ~/dev/<project>                                        # the parent folder of the three repositories
git clone https://github.com/nicolasguelfi/gse-light.git  # the gse-light repository (method, kits), if not there yet
git clone <pm-repo URL>                                    # the project-management repository <pm-repo>, if not there yet
git clone <product-repo URL>                               # the product repository <product-repo>
gse-light/claude-kit/install.sh <product-repo> <pm-repo> <instance>   # installs the kit into <product-repo>
cd <product-repo>
# fill the <…> fields of CLAUDE.md (purpose, commands, gates) and of the CI workflow
git add CLAUDE.md .claude .env.example .gitignore .github
git commit -m "Install the Claude kit (<instance>, kit $(cat .claude/KIT_VERSION))"
git push                                                   # the kit is now in <product-repo> on GitHub
```

**Refresh** after the kit changes in the `gse-light` repository: `git pull` in `gse-light`,
run the same `install.sh` line (it overwrites only the kit's own skills, agents and licence
notice; `CLAUDE.md` and settings stay yours), then commit and push in `<product-repo>`.
`check.sh` tells each developer when the kit in their clone of `<product-repo>` is older than
their clone of `gse-light`.

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

In the session: type `/` and check that `decision-record`, `session-close`,
`verify-claim` and `upskilling` appear; then run **`/upskilling`** (where you start, and a
short personal plan). You never run `install.sh` yourself.

Then continue with the [starting guide](ONBOARDING.md) (§2 the method in one page, §3
your first session).

## 4. If something is missing

To rehearse §2 and §3 on your own machine first: [TEST-DAY0.md](TEST-DAY0.md).

| `check.sh` says | Do |
|---|---|
| `MISSING CLAUDE.md` or a skill | the kit is not installed in `<product-repo>`, or not committed: ask the project lead (§2) |
| `MISSING kit committed` | the project lead installed the kit in `<product-repo>` without committing: ask them to commit and push |
| `WARN kit version … gse-light is at …` | the kit was updated in the `gse-light` repository: the project lead refreshes it in `<product-repo>` (§2) |
| `WARN KIT_LICENSE.md` | the licence notice of the kit is missing: the project lead re-runs `install.sh` (§2) |
| `MISSING .env not in git` | in your clone of `<product-repo>`: `git rm --cached .env`, then commit |
| `MISSING gse-light next to this repository` | clone the `gse-light` repository in the same parent folder as your clone of `<product-repo>` |
| `MISSING <pm-repo> next to this repository` | clone the project-management repository `<pm-repo>` there too (ask the project lead for access) |

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))
