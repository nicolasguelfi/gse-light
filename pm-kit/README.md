# pm-kit — the Project Advisor's kit for a project-management repository

A project-management repository is the **private** repository of one client or project: it
holds `instances/<name>/` (cockpit `BRIEFING.md`, registers, requirements, planning, meetings,
journal) and nothing of the method. It is the project's **overall view**: the instance's
`README.md` lists the project's repositories (repository layout, the first of the twelve
decisions of `design-phase` §2), and every product repository's sessions write their
decisions and journal here. The Project Advisor opens Claude Code there; this kit gives those
sessions their skills, agents, start hook and rules, and the scripts of `gse-light` do the
work from there. The pm-kit is the author's own tooling as Project Advisor (the Project
Advisor of an instance is named in its roles record); the method itself needs only the
[product kit](../claude-kit/README.md).

## Contents

| Path | What it is | Installed as |
|---|---|---|
| [`install.sh`](install.sh) | Installs or refreshes the kit in a project-management repository; copies the instance skeleton into an empty `instances/<name>/` | run from the project-management repository: `../gse-light/pm-kit/install.sh .` |
| [`skills/`](skills/) | `advisor` (single entry point), `meeting`, `slides`, `method-lesson`, `decision-record`, `cockpit-update`, `session-close`, `genai-onboarding` | `.claude/skills/` (refreshed) |
| [`agents/`](agents/) | `delivery-auditor`, `minutes-verifier`, `design-reviewer` | `.claude/agents/` (refreshed) |
| [`templates/settings.json`](templates/settings.json) | Permissions (read-only commands, `.env` denied, `../gse-light` reachable) and the session-start hook | `.claude/settings.json` (created once) |
| [`templates/CLAUDE.pm-repo.md`](templates/CLAUDE.pm-repo.md) | Rules of the Project Advisor's sessions | `CLAUDE.md` (created once, then owned by the repository) |
| [`templates/env.example`](templates/env.example) | Keys and settings of the scripts (paid models, recording, transcription): one variable per vendor, nothing project-specific | `.env.example` (created once; `.env` never committed) |
| [`templates/docs.yml`](templates/docs.yml) | CI: `check_docs` with `gse-light` checked out next to the repository | `.github/workflows/docs.yml` (created once) |
| [`templates/instance/`](templates/instance/) | Skeleton of a new instance: `README.md`, `BRIEFING.md` (§1, §1b, §2, §3 with the counts line), the three registers with their §0 dashboards, `governance/10-roles-and-go-aheads.md`, `journal/README.md`, `journal/metrics.csv`, `meetings/README.md` | `instances/<name>/` (copied once, when the folder is empty) |

## Start a project

The machine first, once: [`scripts/README.md`](../scripts/README.md) (ffmpeg, `uv`, the
Python environment in `~/.venvs/<pm-repo>` linked as `.venv`, `.env`). Then:

```bash
cd ~/dev/<client>                                          # parent folder
git clone https://github.com/nicolasguelfi/gse-light.git   # the gse-light repository (this method)
mkdir -p <pm-repo>/instances/<name> && cd <pm-repo> && git init
../gse-light/pm-kit/install.sh .                          # skills, agents, settings, CLAUDE.md, .env.example, CI, and the instance skeleton
cp .env.example .env                                        # fill it (never committed)
printf 'ClientName\nProjectName\n' > instances/<name>/private-terms.txt   # terms the leak guard refuses in gse-light (regular expressions, one per line)
```

`pm-kit/install.sh` copies `pm-kit/templates/instance/` into an empty `instances/<name>/`:
`README.md` (project, phase, people, **the list of the project's repositories**), `BRIEFING.md`
(§1, §1b, §2, §3 with the pending counts), the three registers in the format of
`../gse-light/templates/decision-record.md` (`governance/05-project-decisions.md`,
`requirements/05-decisions.md`, `design/05-design-decisions.md`) with their §0 dashboards,
`governance/10-roles-and-go-aheads.md`, `journal/` and `meetings/`. Then fill the `<…>` fields
of `CLAUDE.md` and of the skeleton, run `python3 ../gse-light/scripts/check_docs.py`, commit,
and open Claude Code in `<pm-repo>`: the hook prints the situation; say "go".

Who writes here: **sessions opened here are the Project Advisor's**; team members never open
Claude Code in this repository. They work from their sandbox or product repository, whose
kit writes their journal entries and new 🔴 records here (`session-close` and
`decision-record` commit and push those paths only); the **project lead** also writes
`planning/sprints/`; a record turns 🟢 in a session of its decider (named in the roles
record); `BRIEFING.md` is the Advisor's (the product kit's `settings.json` denies the Edit
tool on it — a convenience, not a security boundary; GitHub branch protection on `main` is
recommended and decided per project in its roles record). Until the product repositories exist, each team member works in a personal,
private, throwaway **sandbox repository** (`<project>-sandbox-<firstname>`, created on GitHub
by the project lead or the Project Advisor, cloned next to `gse-light` and this repository,
the product kit installed by its one command). In **W1** the project lead runs the design
phase from that sandbox (`design-phase`): drivers → `DD` records here; its first decision,
repository layout, names the product repositories, which then receive the kit; gates, CI and
`CLAUDE.md` filled there.

**Cross-repository work**: open Claude Code here with the product repositories added —
`claude --add-dir ../<repo-a> --add-dir ../<repo-b>`, or list them in
`permissions.additionalDirectories` of `.claude/settings.json` — to read code, pull requests
and gates of every repository of the project from the overall view. A Claude Code session
on claude.ai (web or cloud) sees one repository only; the overall view is a local session.

## Refresh after a change in gse-light

`git pull` in `gse-light`, then `../gse-light/pm-kit/install.sh .` in the project-management
repository, commit. `check_docs` fails while `.claude/` differs from the pm-kit (from a
product or sandbox repository: `python3 ../gse-light/scripts/check_docs.py ../<pm-repo>`).

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))
