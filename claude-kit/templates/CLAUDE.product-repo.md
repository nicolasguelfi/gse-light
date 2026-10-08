# <repository name> — instructions for Claude

Part of the project **<instance>**. Three repositories side by side, in one parent folder:
this one (the code); the method **`gse-light`** in `../gse-light`, read by every session and
changed by none; and the project's private project-management repository **`<pm-repo>`** in
`../<pm-repo>`, whose instance folder holds the registers, cockpit, journal and sprints.
**Project-management zone** (`<pm-zone>` in the kit's skills):
**`../<pm-repo>/instances/<instance>/`**. Both are additional directories of this
repository's `.claude/settings.json`. The same file denies the Edit tool under `../gse-light/`
and on `<pm-zone>/BRIEFING.md` (the Project Advisor's cockpit) and the literal command
`git push origin main`, and asks before any `git push`. These rules are conveniences, not a
security boundary: the project decides in its roles record whether `main` is protected on
GitHub (branch protection, recommended). Never try to work around them. The skills push your
own journal entries and 🔴 records with `git -C <pm-zone>/..` forms: those are not asked for. This repository is one of the project's repositories listed
in `<pm-zone>/README.md` — or a personal sandbox repository (`<project>-sandbox-<firstname>`,
used until the product repositories exist): same rules. The kit is installed in each of
them. Your sessions write your journal entries and new 🔴 records into `<pm-zone>` through
the skills; never open Claude Code in `<pm-repo>` itself (its sessions are the Project
Advisor's, who opens it with the product repositories added as additional directories for
the overall view).
**Read `../gse-light/method/00-reference-design.md` chapters 1 (principles) and 13 (working
with the AI day to day), and
`<pm-zone>/design/00-design-choices.md` and `05-design-decisions.md`, once per session.**
A person new to the project reads `../gse-light/QUICKSTART.md` (one page), then
`../gse-light/claude-kit/ONBOARDING.md`, then runs the skill `upskilling`.

## Words

The method's terms and acronyms (`PD`, `DEC`, `DD`, gate, go-ahead, rehearsal environment…)
are defined in `../gse-light/GLOSSARY.md`; the project's own terms in
`<pm-zone>/requirements/01-glossary.md`.

## Purpose and phase

<What this repository delivers, in two lines. Current phase and increment.>

## Commands

| Purpose | Command |
|---|---|
| Install | `<command>` |
| Run locally | `<command>` |
| **All gates (same as CI)** | `bash ./gates.sh` (filled after the design phase; until then a stub that passes) |
| Tests only | `<command>` |
| End-to-end tests through the real user interface | `<command, from the test tools decision>` |
| New migration | `<command>` |
| Documentation checks of `<pm-zone>` | `python3 ../gse-light/scripts/check_docs.py ../<pm-repo>` (the repository to check is the argument) |

Run the gates before every commit you propose. Report their output; never say "tests
pass" without it.

## Standing rules (from the reference design)

- **Design phase first**: before any architecture or infrastructure choice, run the skill
  `design-phase` with the project lead; every design decision (`DD` record) cites the
  project's drivers it answers. Every such choice — the twelve decisions of the design
  phase, in order: repository layout, hosting, environments and promotion path, stack and
  language, data store, identity, infrastructure as code, continuous integration, test
  tools, secrets, dependency updates, monitoring — is an instance `DD` record, never a
  default.
- **Never propose an example project's stack as a default** (Sumvadis, StreamTeX or any
  project the method cites): they are illustrations. Cite one only when a driver of this
  project makes it relevant, and say which.
- **Examples first**: a requirement links to the real example (instance and data) that
  motivates it; if none exists, ask for it before specifying.
- **Tests with the code**: every change comes with its unit and integration tests, and
  every user path with its **end-to-end test through the real user interface, driven by you
  to play the use case** — this is how the product is verified and validated, and it is a
  firm rule. The tool is the instance's choice, in its test tools decision (the ninth of
  the twelve; for a web interface, Playwright is one example). Each test names the requirement
  it proves. Coverage is measured on every change; do not lower it.
- **Green gates to move forward**: `bash ./gates.sh` green locally and in CI; never propose
  a merge with a red gate.
- **Measure before asserting** (skill `verify-claim`).
- **State is never a constant**: no hard-coded identifier of a business object (for example
  a course, a session, a user); tests create their own data.
- **Decisions go to the registers** in `<pm-zone>` (skill `decision-record`, which commits
  and pushes that record only), never as "open questions" in a file here.
- **Evaluate ≠ execute**: when asked to evaluate or propose, change nothing.
  Push, deploy, migrate a shared database, create cloud resources: only with an explicit
  go-ahead (`<pm-zone>/governance/10-roles-and-go-aheads.md`).
- **Environments and branch model** come from the instance's environments and promotion
  path decision (the third of the twelve), named in "Git" below; a branch that deploys is
  never pushed without the go-ahead for that promotion.
- **Data regime** (<the instance's data-regime record>): <the regime in force>. Never log or store a field outside it.
- **Secrets**: never in files. `.env` is git-ignored; never edit it — ask.
- **Model access**: your Claude Code licence comes from the Project Advisor; API keys for
  complementary models come from the client organisation and live in `.env`, one variable per vendor
  (`<VENDOR>_API_KEY`, optional `<VENDOR>_BASE_URL` when a provider such as OpenRouter
  is in front). Code reads them through the project's single model helper, never
  directly. These rules hold whatever coding agent you use.
- **Roles** (the instance's `governance/10-roles-and-go-aheads.md`): the project lead decides sprints, tickets and technical choices;
  the Project Advisor (named in that record) gives feedback and advice and owns this kit. Do
  not wait for the Project Advisor on a project decision — ask the project lead.
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

Branch model: <from the instance's environments and promotion path decision — e.g. feature
branches → an integration branch → the branch that deploys to the rehearsal environment →
`main` (production)>. Work on feature branches; open pull requests to <the integration
branch>. Never push to `main`, nor to any branch that deploys, without the go-ahead for that
promotion (`settings.json` denies the literal `git push origin main` and asks before any
push; GitHub branch protection on `main` when the project has enabled it).

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))
