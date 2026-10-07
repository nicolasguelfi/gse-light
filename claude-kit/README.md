# Claude kit for product repositories

The Claude artefacts every product repository of an instance uses, kept here
so a fix is made once and propagated everywhere.

## Contents

| Path | What it is | Installed as |
|---|---|---|
| [`INSTALL.md`](INSTALL.md) | **How to install**: the project lead once per product repository (and commit), developers by cloning; shared vs personal files; prerequisites macOS / Windows | read, not installed |
| [`TEST-DAY0.md`](TEST-DAY0.md) | Rehearse a developer's Day 0 on your own machine, in a throwaway folder (15 minutes) | read, not installed |
| [`TEST-DAY0-fast.txt`](TEST-DAY0-fast.txt) | The same rehearsal as three blocks to copy and paste (reset, project lead, developer) | read, not installed |
| [`check.sh`](check.sh) | Day-0 check a developer runs from the product repository (read-only) | run from `gse-light` |
| [`ONBOARDING.md`](ONBOARDING.md) | **Starting guide for engineers and the project lead**: who provides what, Day-0 install, the method in one page, first session step by step, the week's rhythm, checklist | read, not installed |
| [`templates/env.example`](templates/env.example) | Local secrets and settings; keys for complementary models come from the client organisation | `.env.example` (created once; `.env` is never committed) |
| [`templates/CLAUDE.product-repo.md`](templates/CLAUDE.product-repo.md) | Instructions file for a product repository | `CLAUDE.md` (created once, then owned by the repository) |
| [`templates/settings.json`](templates/settings.json) | Shared Claude Code permissions: read-only commands allowed, `.env` and pushes to `main`/`staging` denied | `.claude/settings.json` (created once) |
| [`templates/ci-gates.yml`](templates/ci-gates.yml) | CI workflow that runs the local gates command | `.github/workflows/gates.yml` (created once) |
| [`skills/decision-record/`](skills/decision-record/SKILL.md) | Record a decision in the right register | `.claude/skills/decision-record/` (refreshed) |
| [`skills/session-close/`](skills/session-close/SKILL.md) | Journal entry, metrics, cockpit, hand-over | `.claude/skills/session-close/` (refreshed) |
| [`skills/verify-claim/`](skills/verify-claim/SKILL.md) | Measure before asserting | `.claude/skills/verify-claim/` (refreshed) |
| [`skills/upskilling/`](skills/upskilling/SKILL.md) | Personal coach: where you start, what your responsibilities need, a short plan, the method in two steps ([method](../method/20-upskilling.md)) | `.claude/skills/upskilling/` (refreshed) |
| [`agents/change-reviewer.md`](agents/change-reviewer.md) | Reviews a change against the reference design | `.claude/agents/change-reviewer.md` (refreshed) |

The kit targets **Claude Code only**;
licences come from the Project Advisor, API keys from the client.
The project lead installs and refreshes it; the Project Advisor owns its content.

## Install or refresh

Full procedure: [INSTALL.md](INSTALL.md). The project lead, once per product repository:

Clone `gse-light` (this method) and the project-management repository `<pm-repo>` next to the
product repository (same parent folder), then, from that parent folder:

```bash
gse-light/claude-kit/install.sh <product-repo> <pm-repo> <instance>
```

Skills and agents are overwritten on every run (the kit owns them); `CLAUDE.md`,
`settings.json`, `.env.example` and the CI workflow are created only if absent (the repository owns
them after creation); `<instance>` and `<pm-repo>` in the new `CLAUDE.md` are replaced by the names given. The kit's commit is written to `.claude/KIT_VERSION`.

## Changing the kit

Change it here, by pull request, then run `install.sh` in each product repository.
Two skills (`decision-record`, `session-close`) are also in the [pm-kit](../pm-kit/README.md),
for project-management repositories: `scripts/check_docs.py` fails if the two copies differ.

---

© 2026 Nicolas Guelfi · [`gse-light`](https://github.com/nicolasguelfi/gse-light) · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))
