# <repository name> — instructions for Claude

Part of the project **<instance>**. Three repositories side by side, in one parent folder:
this one (the code); the method **`gse-light`** in `../gse-light`, read by every session and
changed by none; and the project's private project-management repository **`<pm-repo>`** in
`../<pm-repo>`, whose instance folder holds the registers, cockpit, journal and sprints.
**Project-management zone** (`<pm-zone>` in the kit's skills):
**`../<pm-repo>/instances/<instance>/`**. Both are additional directories of this
repository's `.claude/settings.json`; the same file denies any edit under `../gse-light/`
and of `<pm-zone>/BRIEFING.md` (the Project Advisor's cockpit) — never try to work around
it. This repository is one of the project's repositories listed in `<pm-zone>/README.md`;
the kit is installed in each of them, and an overall view is Claude Code opened in
`../<pm-repo>` with the product repositories added as additional directories.
**Read `../gse-light/method/00-reference-design.md` chapters 1 and 13, and
`<pm-zone>/design/00-design-choices.md` and `05-design-decisions.md`, once per session.**
A person new to the project reads `../gse-light/QUICKSTART.md` (one page), then
`../gse-light/claude-kit/ONBOARDING.md`, then runs the skill `upskilling`.

## Purpose and phase

<What this repository delivers, in two lines. Current phase and increment.>

## Commands

| Purpose | Command |
|---|---|
| Install | `<command>` |
| Run locally | `<command>` |
| **All gates (same as CI)** | `./gates.sh` (filled after the design phase; until then a stub that passes) |
| Tests only | `<command>` |
| End-to-end tests through the real interface | `<command, from the test DD>` |
| New migration | `<command>` |

Run the gates before every commit you propose. Report their output; never say "tests
pass" without it.

## Standing rules (from the reference design)

- **Design phase first**: before any architecture or infrastructure choice, run the skill
  `design-phase` with the project lead; every `DD` record cites the project's drivers it
  answers. Architecture, repository layout, environments, branch model and test tools are
  the instance's `DD` records, not defaults.
- **Never propose an example project's stack as a default** (Sumvadis, StreamTeX or any
  project the method cites): they are illustrations. Cite one only when a driver of this
  project makes it relevant, and say which.
- **Examples first**: a requirement links to the real example (instance and data) that
  motivates it; if none exists, ask for it before specifying.
- **Tests with the code**: every change comes with its unit and integration tests, and
  every user path with its **end-to-end test through the real user interface, driven by you
  to play the use case** — this is how the product is verified and validated, and it is a
  firm rule. The tool is the instance's choice, in its test `DD` (Playwright is the example
  for a web interface). Each test names the requirement it proves. Coverage is measured on
  every change; do not lower it.
- **Green gates to move forward**: `./gates.sh` green locally and in CI; never propose a
  merge with a red gate.
- **Measure before asserting** (skill `verify-claim`).
- **State is never a constant**: no hard-coded course, session or user identifier;
  tests create their own data.
- **Decisions go to the registers** in `<pm-zone>` (skill `decision-record`, which commits
  and pushes that record only), never as "open questions" in a file here.
- **Evaluate ≠ execute**: when asked to evaluate or propose, change nothing.
  Push, deploy, migrate a shared database, create cloud resources: only with an explicit
  go-ahead (`<pm-zone>/governance/10-roles-and-go-aheads.md`).
- **Environments and branch model** come from the instance's `DD` records (environments
  `DD`, branch-model `DD`), named in "Git" below; a branch that deploys is never pushed
  without the go-ahead for that promotion.
- **Data regime** (<the instance's data-regime record>): <the regime in force>. Never log or store a field outside it.
- **Secrets**: never in files. `.env` is git-ignored; never edit it — ask.
- **Model access**: your Claude Code licence comes from the Project Advisor; API keys for
  complementary models come from the client organisation and live in `.env`, one variable per vendor
  (`<VENDOR>_API_KEY`, optional `<VENDOR>_BASE_URL` when a provider such as OpenRouter
  is in front). Code reads them through the project's single model helper, never
  directly. These rules hold whatever coding agent you use.
- **Roles** (the instance's `governance/10-roles-and-go-aheads.md`): the project lead decides sprints, tickets and technical choices;
  the Project Advisor (NG) gives feedback and advice and owns this kit. Do not wait for NG on a
  project decision — ask the project lead.
- **Documentation with the code**: behaviour changed ⇒ document changed in the same commit.
- **Propagation**: after correcting a fact, grep this repository and `<pm-zone>` for
  the old claim.
- Before a pull request, run the `change-reviewer` agent.
- At the end of a session, use the skill `session-close`: it writes the journal entry and
  the metrics row in `<pm-zone>` and commits and pushes those paths only.

## Lessons learned here

Carried over from the method's sessions (rule — date — why):

- When a push or a publish is refused because someone changed the target since you read
  it, re-read it and merge your change onto it; never resend your copy, never force —
  2026-10-07 — a slide the Project Advisor had edited was overwritten once.
- Never run a shell command that waits on standard input (a bare `cat > file` with no
  input) — 2026-10-07 — it blocked a session until it was stopped by hand.
- Keep permission deny rules narrow: `Read(./.env.*)` also blocks `.env.example` —
  2026-10-07 — found while building the kit.
- When you describe a task or a plan, name who does each action: a person, a person
  asking Claude, or Claude and the CI automatically — 2026-10-07 — the Project Advisor's
  rule at the kick-off: everyone must know what is theirs.

<Dated rules learned from incidents in this repository: rule — date — why.>

## Git

Branch model: <from the instance's branch-model DD — e.g. feature branches → an integration
branch → the branch that deploys to the rehearsal environment → `main` (production)>. Work
on feature branches; open pull requests to <the integration branch>. Never push to `main`,
nor to any branch that deploys, without the go-ahead for that promotion (`main` is denied to
Claude by `settings.json`).

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))
