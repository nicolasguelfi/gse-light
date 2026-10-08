# Claude kit for product repositories

The Claude artefacts every product repository of an instance uses — five skills, one agent
and the files a repository starts from — kept here so a fix is made once and propagated
everywhere. Until the product repositories exist (repository layout, the first of the twelve
decisions of `design-phase` §2), each team member works in a personal, private, throwaway
**sandbox repository** (`<project>-sandbox-<firstname>`, created on GitHub by the project
lead or the Project Advisor, cloned next to `gse-light` and the project-management
repository): the same kit, installed by the same command, the same rules.

## Contents

| Path | What it is | Installed as |
|---|---|---|
| [`INSTALL.md`](INSTALL.md) | **How to install**: the project lead with one command from inside the product clone (and commit), developers by cloning; shared vs personal files; prerequisites macOS / Windows; what `check.sh` says | read, not installed |
| [`TEST-DAY0.md`](TEST-DAY0.md) | Rehearse a developer's Day 0 on your own machine, in a throwaway folder: 15 minutes for the install and checks; the first session adds 15 minutes of `/upskilling` and 30 minutes of work | read, not installed |
| [`TEST-DAY0-fast.txt`](TEST-DAY0-fast.txt) | The same rehearsal as three blocks to copy and paste (reset, project lead, developer) | read, not installed |
| [`install.sh`](install.sh) | Installs or refreshes the kit; run from inside the product (or sandbox) repository: `../gse-light/claude-kit/install.sh <instance> [--pm <folder>]` | run from the product repository |
| [`check.sh`](check.sh) | Day-0 check a developer runs from inside the product repository (read-only); compares `KIT_VERSION` with the last `gse-light` commit that touched `claude-kit/` and says whether the kit in `gse-light` is newer or your clone of `gse-light` is behind | run from the product repository |
| [`ONBOARDING.md`](ONBOARDING.md) | **Starting guide for engineers and the project lead**: who provides what, Day-0 install, the method in one page, first session step by step, the week's rhythm, checklist | read, not installed |
| [`templates/env.example`](templates/env.example) | Local secrets and settings; keys for complementary models come from the client organisation | `.env.example` (created once; `.env` is never committed) |
| [`templates/CLAUDE.product-repo.md`](templates/CLAUDE.product-repo.md) | Instructions file for a product repository; `<instance>` and `<pm-repo>` are substituted at install | `CLAUDE.md` (created once, then owned by the repository) |
| [`templates/settings.json`](templates/settings.json) | Shared Claude Code permissions: `../gse-light` and `../<pm-repo>` as additional directories; read-only commands, the gates and the checks allowed; the Edit tool denied under `../gse-light/` and on the cockpit `BRIEFING.md`; the literal `git push origin main` denied and any other `git push` asked — conveniences, not a security boundary (`main` is protected on GitHub in every repository) | `.claude/settings.json` (created once) |
| [`templates/gates.sh`](templates/gates.sh) | Day-0 stub of the gates: prints *no gates yet: design phase in progress* and exits 0; filled from the test tools and continuous integration decisions (`design-phase` §2, #8 and #9) | `gates.sh` (created once, executable) |
| [`templates/ci-gates.yml`](templates/ci-gates.yml) | CI workflow that runs `bash ./gates.sh` on every pull request and on every push to `main` | `.github/workflows/gates.yml` (created once) |
| [`templates/gitattributes`](templates/gitattributes) | `*.sh text eol=lf`: shell scripts keep Unix line endings on a Windows clone | `.gitattributes` (created once) |
| [`templates/KIT_LICENSE.md`](templates/KIT_LICENSE.md) | Licence notice that travels with the kit | `.claude/KIT_LICENSE.md` (refreshed) |
| [`skills/design-phase/`](skills/design-phase/SKILL.md) | W1: the project's drivers → `DD` records (the twelve decisions of `design-phase` §2, in order) → `gates.sh`, CI and `CLAUDE.md` placeholders filled | `.claude/skills/design-phase/` (refreshed) |
| [`skills/decision-record/`](skills/decision-record/SKILL.md) | Record a decision in the right register; commits and pushes that record only | `.claude/skills/decision-record/` (refreshed) |
| [`skills/session-close/`](skills/session-close/SKILL.md) | Journal entry, metrics, hand-over; commits and pushes those paths only | `.claude/skills/session-close/` (refreshed) |
| [`skills/verify-claim/`](skills/verify-claim/SKILL.md) | Measure before asserting | `.claude/skills/verify-claim/` (refreshed) |
| [`skills/upskilling/`](skills/upskilling/SKILL.md) | Personal coach: where you start, what your responsibilities need, a short plan, the method in two steps ([method](../method/20-upskilling.md)) | `.claude/skills/upskilling/` (refreshed) |
| [`agents/change-reviewer.md`](agents/change-reviewer.md) | Reviews a change against the reference design and the instance's `DD` records | `.claude/agents/change-reviewer.md` (refreshed) |

The kit targets **Claude Code only**;
licences come from the Project Advisor, API keys from the client.
The project lead installs and refreshes it; the Project Advisor owns its content.

## Install or refresh

Full procedure: [INSTALL.md](INSTALL.md); one page: [QUICKSTART.md](../QUICKSTART.md). The
project lead, once per product repository (and once per sandbox repository), with `gse-light`
and the project-management repository `<pm-repo>` cloned next to it (same parent folder):

```bash
cd <product-repo>                                   # inside the product (or sandbox) clone
../gse-light/claude-kit/install.sh <instance>       # add --pm <pm-repo> when it asks (none or several candidates)
```

Skills, agents, the licence notice and `.claude/KIT_VERSION` are overwritten on every run
(the kit owns them); `CLAUDE.md`, `settings.json`, `gates.sh`, `.gitattributes`,
`.env.example` and the CI workflow are created only if absent (the repository owns them after
creation). `<instance>` and `<pm-repo>` in the new `CLAUDE.md` are replaced by the names
found. `KIT_VERSION` is the last `gse-light` commit that touched `claude-kit/`. On a refresh,
the command warns when the `CLAUDE.md` or `settings.json` templates changed since the recorded
`KIT_VERSION` and prints the exact `git diff` command (from that old hash) so the project lead
can carry the change over by hand. A product made of several repositories: the same command
in each. The documentation checks of the project-management repository run from a product
repository as `python3 ../gse-light/scripts/check_docs.py ../<pm-repo>` (the repository to
check is the argument).

## Changing the kit

Change it here, by pull request, then rerun the command in each product repository.
Two skills (`decision-record`, `session-close`) are also in the [pm-kit](../pm-kit/README.md),
for project-management repositories: `scripts/check_docs.py` fails if the two copies differ.
The developer documents stay in step: [QUICKSTART.md](../QUICKSTART.md), [INSTALL.md](INSTALL.md),
[ONBOARDING.md](ONBOARDING.md), this file, the `CLAUDE.md` template and the Day-0 rehearsals
change together.

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))
