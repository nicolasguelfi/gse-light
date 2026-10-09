# <repository name> — instructions for Claude

This is the **project's repository**, run with the method **gse-light**: the code, and in
**`project/`** the project's shared record — cockpit, registers, requirements, planning,
meetings, journal. Two repositories side by side, in one parent folder: this one, and the
method **`gse-light`** in `../gse-light`, read by every session and changed by none
(an additional directory of `.claude/settings.json`). Every role opens Claude Code **here**:
the developers, the project lead and the Project Advisor; the rules below say what each
one's session does. The same `settings.json` denies the Edit tool under `../gse-light/` and
on `project/BRIEFING.md` (the Project Advisor's cockpit) and the literal command
`git push origin main`, and asks before any `git push`. These rules are conveniences, not a
security boundary: the project decides in its roles record how `main` is protected on
GitHub. Never try to work around them.
**Read `../gse-light/method/00-reference-design.md` chapters 1 (principles) and 13 (working
with the AI day to day), `project/README.md` (the project, its phase, its people), and
`project/design/00-design-choices.md` and `05-design-decisions.md`, once per session.**
A person new to the project reads `../gse-light/QUICKSTART.md` (one page), then
`../gse-light/kit/ONBOARDING.md`, then runs the skill `upskilling`.

## Words

The method's terms and acronyms (`PD`, `DEC`, `DD`, gate, go-ahead, rehearsal environment…)
are defined in `../gse-light/GLOSSARY.md`; the project's own terms in
`project/requirements/01-glossary.md`. **Who is who** — the client, its product owner and
data protection contact, the project lead (lead developer), the developers ("team member"
means the project lead or a developer), the Project Advisor, the Claude sessions — is
written once, with the names, in `project/README.md` and in the roles record
`project/governance/10-roles-and-go-aheads.md` (who decides what, who gives which
go-ahead); use those names, never "engineer", "tutor" or "mentor".

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
| Documentation checks of `project/` (same as CI) | `python3 ../gse-light/scripts/check_docs.py` |
| Where the week stands (next meeting, next step) | `python3 ../gse-light/scripts/situation.py` (printed by the start hook) |

Run the gates before every commit you propose. Report their output; never say "tests
pass" without it.

## Standing rules (from the reference design)

- **Design phase first**: before any architecture or infrastructure choice, run the skill
  `design-phase` with the project lead; every design decision (`DD` record) cites the
  project's drivers it answers. Every such choice — the twelve decisions of the design
  phase, in order: repository layout, hosting, environments and promotion path, stack and
  language, data store, identity, infrastructure as code, continuous integration, test
  tools, secrets, dependency updates, monitoring — is a `DD` record of `project/design/`,
  never a default.
- **Never propose an example project's stack as a default** (Sumvadis, StreamTeX or any
  project the method cites): they are illustrations. Cite one only when a driver of this
  project makes it relevant, and say which.
- **Examples first**: a requirement links to the real example (file and data) that
  motivates it, in `project/requirements/40-examples/`; if none exists, ask for it before
  specifying.
- **Tests with the code**: every change comes with its unit and integration tests, and
  every user path with its **end-to-end test through the real user interface, driven by you
  to play the use case** — this is how the product is verified and validated, and it is a
  firm rule. The tool is the project's choice, in its test tools decision (the ninth of
  the twelve; for a web interface, Playwright is one example). Each test names the requirement
  it proves. Coverage is measured on every change; do not lower it.
- **Green gates to move forward**: `bash ./gates.sh` green locally and in CI; never propose
  a merge with a red gate.
- **Measure before asserting** (skill `verify-claim`): never state the state of a system (a
  branch, a deployment, a count) without the command that measured it; never announce an
  unverified cause. **Read the register before calling something a defect**: a measured
  deviation may be a decision already taken.
- **State is never a constant**: no hard-coded identifier of a business object (for example
  a course, a session, a user); tests create their own data.
- **Decisions and open questions go to the registers**, never scattered: project →
  `project/governance/05-project-decisions.md` (`PD-NN`); requirements →
  `project/requirements/05-decisions.md` (`DEC-NNN`); design →
  `project/design/05-design-decisions.md` (`DD-NN`). One format for all (plain-language
  problem · what to consult · options with advantages and drawbacks · recommendation · status
  badge 🟢 decided, 🔴 pending, 🟡 provisional · a §0 dashboard at the top):
  `../gse-light/templates/decision-record.md`, or the skill `decision-record`, which
  commits that record only. A record turns 🟢 only by its decider (roles record).
- **Evaluate ≠ execute**: when asked to evaluate, assess or propose, change nothing outside
  the document being written. State-changing actions — push, deploy, migrate a shared
  database, create cloud resources, spend, send messages — need an explicit go-ahead from
  the person the roles record names (`project/governance/10-roles-and-go-aheads.md`).
- **Asking the person** (the method's owner, 2026-10-09; skill `review`): when you must
  interact with the person — an answer, a choice, a validation, a go-ahead — prefer the
  built-in multiple-choice question (QCM), one at a time. When the interaction is more complex,
  or when you must present data, use the `review` skill: a review board, with a comment field
  for every point you ask about and a global comment field. In both forms, always and for every
  question, restate the problem simply so that the person understands it; for every proposal,
  explain just as simply its advantages and its drawbacks, with all the consequences of that
  solution. A choice written in prose is a choice the person cannot tick.
- **Environments and branch model** come from the project's environments and promotion
  path decision (the third of the twelve), named in "Git" below; a branch that deploys is
  never pushed without the go-ahead for that promotion.
- **Data regime** (<the project's data-regime record>): <the regime in force>. Never log or store a field outside it.
- **Secrets**: never in files. `.env` is git-ignored; never edit it — ask. Never write a
  secret, token or key in any repository; point to where it lives (vault name, never its value).
- **Model access**: your Claude Code licence comes from the Project Advisor; API keys for
  complementary models come from the client organisation and live in `.env`, one variable per vendor
  (`<VENDOR>_API_KEY`, optional `<VENDOR>_BASE_URL` when a provider such as OpenRouter
  is in front). Code reads them through the project's single model helper, never
  directly. These rules hold whatever coding agent you use.
- **Roles** (`project/governance/10-roles-and-go-aheads.md`): the project lead decides sprints,
  tickets and technical choices, chairs the meetings and keeps time, and validates and sends
  the meeting minutes (his session writes the validation line in
  `project/meetings/<date>/minutes.md`); the Project Advisor gives feedback and advice, owns
  the method and this kit, and installs and refreshes the kit here. Do not wait for the
  Project Advisor on a project decision — ask the project lead.
- **Writing style**: plain words first, technical words second, in every document; define
  each technical term at first use. Documents are in English (the team's working language);
  a person may write in another language — answer them in theirs.
- **Documentation with the code**: behaviour changed ⇒ document changed in the same commit.
- **Propagation**: after correcting a fact, grep the whole repository (code and `project/`)
  for the old claim. The deck in force is part of it: `check_docs` warns when a file named
  in a slide's "Source:" footer was committed after the slide.
- **Never "the repository" alone**: name it — this repository `<repository name>`, the
  method `gse-light`.
- Before a pull request, run the `change-reviewer` agent.
- **Every session ends with `session-close`**: a journal entry in `project/journal/`
  (one `YYYY-MM-DD-<initials>-sNN.md` per session, never rewritten — research data on
  AI-assisted engineering) and one row in `project/journal/metrics.csv`; the skill commits
  those paths only and pushes on the person's go-ahead.

## If you are a developer's or the project lead's session

- **Your skills**: `design-phase` (the project lead, W1), `decision-record`, `review`,
  `session-close`, `verify-claim`, `upskilling`; your agent: `change-reviewer`. The six other
  skills (`advisor`, `meeting`, `slides`, `cockpit-update`, `method-lesson`,
  `genai-onboarding`) and the agents `delivery-auditor`, `minutes-verifier` and
  `design-reviewer` are the Project Advisor's: they check the git user and stop for anyone else.
- **You write**: the code, by pull request on a feature branch with its tests; the person's
  own journal entries and new 🔴 records; the project lead's session also
  `project/planning/sprints/`, the drivers page and the `DD` records of the design phase, and
  the validation line of the minutes.
- **Never**: edit `project/BRIEFING.md` (the cockpit) or anything under `../gse-light`; turn a
  record 🟢 whose decider is not the person you work for; push to `main`, or to any branch
  that deploys, without the go-ahead; run the Project Advisor's skills.

## If you are the Project Advisor's session

- **One entry point: the session orchestrates.** The Advisor never needs a command. At start,
  the hook prints the situation — today, next meeting, next step — computed by
  `../gse-light/scripts/situation.py` from `project/meetings/`. His **first message, whatever
  it says** ("go", "bonjour", a remark), means: do that step through the `advisor` skill,
  running the agents and skills yourself (`meeting`, `delivery-auditor`, `minutes-verifier`,
  `decision-record`, `method-lesson`, `session-close`); ask him only what only he knows
  (meeting day, participants, points to raise, his feedback section of the minutes), one
  short QCM at a time. If his message is a different request, serve it, then return to the
  step. `/advisor` re-assesses on demand.
- **You write**: the cockpit `project/BRIEFING.md` (the Edit tool is denied on it for every
  session, his included: his `.claude/settings.local.json`, never committed, allows it —
  `"allow": ["Edit(./project/BRIEFING.md)"]`), the meeting briefs and the draft minutes with
  his feedback section (the project lead validates and sends them), `project/README.md` and
  the governance pages, his journal entries, the 🟢 of the records he decides; the method, in
  `../gse-light` — never with a client or project term in it (`project/private-terms.txt`
  lists what the leak guard refuses there).
- **Cockpit discipline**: at the end of every session, refresh `project/BRIEFING.md` §1 (what
  awaits the Advisor), §1b (what awaits the team), add the session's dated bullets to §2; re-stamp
  "Last acknowledgement" only when he has explicitly acknowledged (`cockpit-update`). Never
  push project-management tasks into §1.
- **Light by design**: the Advisor has four hours a week for the project. Prefer one artefact
  that fits in them to several that do not; project management belongs to the project lead.
- **Improve the project from every interaction**. Whenever the Advisor asks for something no
  artefact covers, an artefact does not fit the way he works, or a document is wrong or
  missing: name the gap in one line; do the task by hand if it is small; propose the smallest
  change that would cover it next time, by QCM, with its cost in minutes; on his yes, make it
  in the same session, measure it, and record the lesson with a date through `method-lesson`
  (one place, propagated — most often "Lessons learned here" below); mention it in the
  journal entry. A gap never passes silently; a fix never grows beyond the gap.
- **Never**: decide in the project (the deciders are in the roles record); write a sprint, a
  ticket or code; push a team member's work for them.

## Lessons learned here

Carried over from the method's sessions (rule — date — why), newest first; the lessons of
this repository's own sessions join them. Keep each to two lines; move a rule up into
"Standing rules" when it holds everywhere.

- Every artifact published from this repository (deck, review board, page) gets a folder
  under `project/meetings/<date>/` with its sources and an `open.html` from
  `../gse-light/templates/artifact-open.html`, plus a row in `project/meetings/README.md` —
  2026-10-07 — the method's owner: open any artifact from the file explorer.
- When a push or a publish is refused because someone changed the target since you read
  it, re-read it and merge your change onto it; never resend your copy, never force —
  2026-10-07 — a slide the Project Advisor had edited was overwritten once.
- Never run a shell command that waits on standard input (a bare `cat > file` with no
  input) — 2026-10-07 — it blocked a session until it was stopped by hand.
- `bash -n a.sh b.sh` checks only `a.sh` (the others are its arguments): syntax-check each
  script on its own — 2026-10-07 — a missing quote passed such a check.
- Keep permission deny rules narrow: `Read(./.env.*)` also blocks `.env.example` —
  2026-10-07 — found while building the kit.
- When you describe a task or a plan, name who does each action: a person, a person
  asking Claude, or Claude and the CI automatically; presentations: dark, slides numbered
  n/N, proposal tone — 2026-10-07 — the Project Advisor's rule at the kick-off: everyone
  must know what is theirs.
- Do not raise consent or storage-location concerns for meeting recordings: the Project
  Advisor handles them himself — 2026-10-07 — his directive.

<Dated rules learned from incidents in this repository: rule — date — why.>

## Checks

`python3 ../gse-light/scripts/check_docs.py` before committing anything under `project/`,
and after any change in `../gse-light`: links (including links to the method), the registers
and the cockpit counts, that `.claude/` matches the kit, the deck's freshness, and the
**leak guard** — no term of `project/private-terms.txt` in `gse-light`. CI runs the same
script (`.github/workflows/docs.yml`) next to the gates (`.github/workflows/gates.yml`).

## Git

Branch model: <from the project's environments and promotion path decision — e.g. feature
branches → an integration branch → the branch that deploys to the rehearsal environment →
`main` (production)>. Work on feature branches; open pull requests to <the integration
branch>. Never push to `main`, nor to any branch that deploys, without the go-ahead for that
promotion (`settings.json` denies the literal `git push origin main` and asks before any
push; GitHub branch protection on `main` when the project has enabled it). A session pushes
only on the go-ahead of the person it works for (or when they asked for the push in the same
request), and only that person's own commits. A method change is committed in `gse-light`
first, then `../gse-light/kit/install.sh` refreshes `.claude/` here (commit that too).

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))
