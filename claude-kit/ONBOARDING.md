# Working with generative AI under this method — starting guide for engineers

Status: v0.4 · 2026-10-07 · generic · for the project lead and the engineers · maintained by the Project Advisor (NG)

> **Essentials** — A project run with this method (an *instance*) is built
> in weekly sprints with Claude Code as a working
> partner, under a few firm rules: measure before asserting, decisions in registers,
> nothing state-changing without a go-ahead. This guide gets you from zero to your first
> productive session in about an hour, and tells you the rhythm of the weeks after.
> Fields written `<like this>` are filled by the project lead at the kick-off; `<instance>`
> is your project's folder name in `instances/` of its project-management repository
> `<pm-repo>`. Three repositories, side by side: `gse-light` (this method, public),
> `<pm-repo>` (your project's management, private) and your product repository.

## 0. Who provides what

| You need | Who gives it | How |
|---|---|---|
| A **Claude Code licence** (the coding agent) | Nicolas Guelfi, the Project Advisor | an invitation to his Claude team, by e-mail; sign in with it, not with a personal account |
| **API keys** for complementary models (if a task needs one) | the client organisation, through the project lead | one variable per vendor in your `.env` (see §1.4); never in a file under git |
| Access to the **repositories** | the project lead | `<product repository URL>` and `<pm-repo>` (your project's management: read for all, write for the project lead in `instances/<instance>/`); the method `nicolasguelfi/gse-light` is public |
| The **rules** | `gse-light` and `<pm-repo>` | `gse-light/method/00-reference-design.md` (chapters 1 and 13 first), your instance's `<pm-repo>/instances/<instance>/design/00-design-choices.md`, and your repository's `CLAUDE.md` |

The kit targets **Claude Code only**.
If you work with another coding agent, tell the project lead: the rules still apply, the
kit does not install itself there.

## 1. Day 0 — get set up (30 minutes)

The full procedure, with prerequisites for macOS and Windows and what is shared or
personal, is **[INSTALL.md](INSTALL.md)**. In short:

1. **Prerequisites**: Git with access to the repositories, a bash terminal (Git Bash on
   Windows), Claude Code signed in with the account the Project Advisor invited
   ([INSTALL.md §1](INSTALL.md#1-prerequisites-everyone)).
2. **Clone side by side** `gse-light`, `<pm-repo>` and your product repository: the kit is already in
   the product repository, committed by the project lead. **You never run `install.sh`**
   ([INSTALL.md §3](INSTALL.md#3-developer--get-the-kit-about-15-minutes)).
3. **Your `.env`**: `cp .env.example .env`, then fill it with what the project lead gave you.
4. **Check**: `../gse-light/claude-kit/check.sh` from inside the product repository —
   every line OK, or it tells you what to do.
5. **Open a session**: `claude`, accept the workspace trust dialog, type `/` and check that
   `decision-record`, `session-close`, `verify-claim` and `upskilling` appear.

6. **Start from where you are**: in the session, type `/upskilling`. Ten minutes of
   questions and two or three small checks, then a short personal plan matched to your
   responsibilities; your answers stay in your home folder, outside the repository
   ([method](../method/20-upskilling.md)). The method comes in two steps: the base in your
   first week, tests and coverage in the second.

**Check you are done**: `../gse-light/claude-kit/check.sh` prints no MISSING line.

## 2. How we work with generative AI here — one page

Claude is fast, tireless, has no memory between sessions and tends to sound sure. The
method gives it memory (files), rules (instructions) and checks (gates, measurements).
Seven principles ([reference design ch. 1](../method/00-reference-design.md#1-guiding-principles)).
Each says who carries it: **you** (a person), **ask Claude**, or **automatic** (Claude by
the rules of your `CLAUDE.md`, or the CI):

1. **Examples first.** Before specifying a need, get a real instance and its data from
   the client. Link each requirement
   to its example. *You collect; ask Claude to analyse.*
2. **Tests at every step.** Ask for code *with* its tests: unit, integration (real
   database), end-to-end in a real browser (Playwright). Each test names the requirement
   it proves. *Ask Claude; you read them.*
3. **Green gates to move forward.** Nothing merges with a red gate; nothing goes to
   staging or production without its go-ahead. *Automatic (CI); a person for the go-ahead.*
4. **Know what is verified.** Coverage on every change, and a weekly map of which
   requirements and qualities have passing tests. *Automatic (CI); you read it.*
5. **Measure before asserting.** "Tests pass", "staging is on 1.4", "the import ran": only
   with the command and its output, dated. Ask Claude the same: *show me the command*.
   Skill `verify-claim`. *Automatic (Claude); ask if missing.*
6. **One source of truth.** No hard-coded course, session or user identifier in code or
   tests (tests create their own data); schema from migrations, client from the API
   contract; documentation changes with the code, in the same pull request.
   *Automatic (gates).*
7. **Evaluate is not execute.** Asking Claude to assess changes nothing. Pushing to a
   branch that deploys, migrating a shared database, creating cloud resources, spending
   money: only with the written go-ahead of the person in
   roles and go-aheads (`<pm-repo>/instances/<instance>/governance/10-roles-and-go-aheads.md`) — staging: project lead;
   production, cloud, budget: product owner. The Project Advisor advises; he does not
   decide the project. *Automatic (Claude stops and asks); a person gives it.*

And three habits:

- **Decisions go to the registers**, never as "TODO decide" in a file. A choice between
  options with consequences → skill `decision-record` → a `PD`/`DEC`/`DD` record in
  `<pm-repo>/instances/<instance>/`, 🔴 until the person who holds the right decides. Your session can open a
  record; it closes none.
- **Every session ends with a journal entry** in `<pm-repo>/instances/<instance>/journal/` (skill
  `session-close`): what was done with the command that measured it, decisions touched,
  what is left, a hand-over for a reader with no memory. These entries are also research
  data on AI-assisted engineering — never rewritten.
- **Before a pull request, run the `change-reviewer` agent.** It checks gates, data
  regime, secrets, migrations, documentation, decisions, tests — and says "ready" or lists
  the fixes.

**Never**: a secret, token or key in a file under git (`.env` is yours alone); a push to
`staging` or `main` without the go-ahead; a personal-data field outside the regime of
your instance's data-regime record; a claim
about a running system without its command; editing `<pm-repo>/instances/<instance>/BRIEFING.md` (the Project Advisor's cockpit).

## 3. Your first session, step by step (30 minutes)

Open `claude` in the product repository and work through this, in your own words:

1. *"Read CLAUDE.md and the reference design chapters 1 and 13, then tell me in five lines
   how you will work here."* — check the answer names the gates command, the registers and
   the go-aheads.
2. *"Run the gates and show me the output."* — the command is in `CLAUDE.md` (`<make
   gates>`); green or not, you now know the state, measured.
3. Take a ticket (GitHub issue, in the sprint milestone; it names the requirement or
   decision it serves). *"Propose how to do #NN; change nothing yet."* — read the proposal;
   ask for the alternatives if there is a choice; if it is a real choice, *"record it with
   decision-record"*.
4. *"Do it on a feature branch, run the gates, show me the diff."* — review the diff
   yourself; Claude's code is accepted through the gates **and** your reading.
5. *"Run the change-reviewer agent."* — fix what it lists, then open the pull request to
   `dev`. The pull request updates the document that describes the behaviour, in the same
   diff.
6. *"Close the session."* (skill `session-close`) — journal entry in `<pm-repo>/instances/<instance>/journal/`,
   one row in `metrics.csv`. Read the entry: a colleague with no memory must be able to
   resume from it.

What good looks like after a week: every claim in your journal has a command next to it;
every pull request was reviewed by the agent and by you; no decision lives only in a chat.

## 4. The rhythm of a week

- **Sprint**: one week, a goal, 3–7 tickets with acceptance criteria, each linked to a
  requirement or a decision. The project lead keeps `<pm-repo>/instances/<instance>/planning/sprints/W<n>.md`
  and the GitHub milestone.
- **Meeting with the Project Advisor**: two hours a week, day fixed at each meeting for the next
  one. The Project Advisor arrives with a brief measured from GitHub and the journal (merged pull
  requests, gates, increment demonstrable or not, tickets without a requirement, journal
  entries) — so link your tickets and write your journal: that is how your work becomes
  visible. The minutes list, per participant, the tasks for the next sprint, each with the
  timestamp where it was said.
- **Iterative and incremental**: every sprint ends with something demonstrable, merged to
  `dev` and, when the gates are green and the project lead says so, promoted to staging.
  Branches that live a week without a merge are the first thing the brief shows.

## 5. If you are the project lead

In addition to the above, you:

- **decide** sprints, priorities, tickets, technical choices inside an approved design
  decision, code review, promotion to staging; the product owner accepts increments and
  gives the production and budget go-aheads; the Project Advisor advises;
- **write in `<pm-repo>`** directly: `instances/<instance>/planning/sprints/`, your journal entries, new 🔴
  records in the registers — never `instances/<instance>/BRIEFING.md`;
- **install, commit and refresh the kit** in each product repository ([INSTALL.md §2](INSTALL.md#2-project-lead--install-the-kit-in-the-product-repository--once-per-product-repository)),
  fill the `<…>` fields of `CLAUDE.md` (purpose, commands, gates), and keep "Lessons
  learned here" alive: a rule learned from an incident is added the same day, dated;
- run the **kick-off checklist** ([reference design ch. 15](../method/00-reference-design.md#15-starting-a-new-project)):
  repositories from the kit, gates green on an empty suite, staging declared as code,
  sign-in, database with its first migration, secrets in the vault, one end-to-end path.

## 6. Day-0 checklist

Copy into your first journal entry and tick with the command that proves each line.

- [ ] Claude Code installed and signed in with the invited account — `claude --version`
- [ ] `gse-light`, `<pm-repo>` and `<product repository>` cloned side by side — `ls ..`
- [ ] Kit present and personal files out of git — `../gse-light/claude-kit/check.sh`
- [ ] `.env` created from `.env.example`, not tracked — `git status --short | grep -c .env` → 0
- [ ] Gates command known and run once — `<make gates>` output quoted
- [ ] Reference design chapters 1 and 13 read; `CLAUDE.md` read
- [ ] First ticket taken, first pull request opened to `dev`, `change-reviewer` run
- [ ] `/upskilling` run once; plan noted in your private record
- [ ] First journal entry written (`session-close`)

## 7. Where to ask

Technical and sprint questions: the project lead. Method, Claude, the kit: the Project Advisor, at
the weekly meeting or through the project lead. A question that is really a decision:
open the record (`decision-record`) and let the right person close it. Something the kit
should do and does not: say it — the kit improves from what happens in the sessions.

## Appendix — mistakes we already made for you

From [reference design, appendix C](../method/00-reference-design.md#appendix-c--anti-patterns-lived-on-sumvadis):
a constant for something that changes (a campaign code in tests); a measured deviation
called a defect when it was a decision; a cause announced without re-measuring after the
fix; a fix applied to one output and not to its twin; a rule enforced on screen but not in
the exported file; a cockpit left stale for a week. Each produced one of the rules above.

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))
