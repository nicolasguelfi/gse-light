# pm-kit — the Project Advisor's kit for a project-management repository

A project-management repository is the **private** repository of one client or project: it
holds `instances/<name>/` (cockpit `BRIEFING.md`, registers, requirements, planning, meetings,
journal) and nothing of the method. The Project Advisor opens Claude Code there; this kit gives
those sessions their skills, agents, start hook and rules, and the scripts of `gse-light` do
the work from there.

## Contents

| Path | What it is | Installed as |
|---|---|---|
| [`install.sh`](install.sh) | Installs or refreshes the kit in a project-management repository | run from the project-management repository: `../gse-light/pm-kit/install.sh .` |
| [`skills/`](skills/) | `advisor` (single entry point), `meeting`, `slides`, `method-lesson`, `decision-record`, `cockpit-update`, `session-close`, `genai-onboarding` | `.claude/skills/` (refreshed) |
| [`agents/`](agents/) | `delivery-auditor`, `minutes-verifier`, `design-reviewer` | `.claude/agents/` (refreshed) |
| [`templates/settings.json`](templates/settings.json) | Permissions (read-only commands, `.env` denied, `../gse-light` reachable) and the session-start hook | `.claude/settings.json` (created once) |
| [`templates/CLAUDE.pm-repo.md`](templates/CLAUDE.pm-repo.md) | Rules of the Project Advisor's sessions | `CLAUDE.md` (created once, then owned by the repository) |
| [`templates/env.example`](templates/env.example) | Keys and settings of the scripts (paid models, recording, transcription) | `.env.example` (created once; `.env` never committed) |
| [`templates/docs.yml`](templates/docs.yml) | CI: `check_docs` with `gse-light` checked out next to the repository | `.github/workflows/docs.yml` (created once) |

## Start a project

```bash
cd ~/dev/<client>                                          # parent folder
git clone https://github.com/nicolasguelfi/gse-light.git   # the gse-light repository (this method)
mkdir -p <pm-repo>/instances/<name> && cd <pm-repo> && git init
../gse-light/pm-kit/install.sh .                          # skills, agents, settings, CLAUDE.md, .env.example, CI
cp .env.example .env                                        # fill it (never committed)
printf 'ClientName\nProjectName\n' > instances/<name>/private-terms.txt   # terms the leak guard refuses in gse-light (regular expressions, one per line)
```

Then create the instance's files — there is no scaffold yet: `BRIEFING.md` (§1, §1b, §2, §3 with the
pending counts), the three registers in the format of `../gse-light/templates/decision-record.md`
(`governance/05-project-decisions.md`, `requirements/05-decisions.md`, `design/05-design-decisions.md`),
`governance/10-roles-and-go-aheads.md`, `meetings/`, `journal/` —
fill the `<…>` fields of `CLAUDE.md`, run `python3 ../gse-light/scripts/check_docs.py`, commit,
and open Claude Code in `<pm-repo>`: the hook prints the situation; say « go ».

## Refresh after a change in gse-light

`git pull` in `gse-light`, then `../gse-light/pm-kit/install.sh .` in the project-management
repository, commit. `check_docs` fails while `.claude/` differs from the pm-kit.

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))
