# Working with generative AI under this method — starting guide for the team

Status: v0.7 · 2026-10-08 · generic · for the project lead and the developers, with a short section for the product owner and the Project Advisor · maintained by the Project Advisor

> **Essentials** — A project run with this method (an *instance*) is built in sprints
> with Claude Code as a working partner, under a few firm rules: measure before asserting,
> decisions in registers, nothing state-changing without a go-ahead. This guide gets a
> team member from zero to a first productive session in about an hour and tells the rhythm
> of the weeks after.
>
> - **The hour**: 15 minutes to install, 15 for `/upskilling`, 30 for the first session.
> - **The order of reading**: the part for everyone first (§0–§1), then your own section (§2–§5), then the checklists (§6).
> - **Fields written `<like this>`** are filled by the project lead at the kick-off; `<instance>` is your project's folder name in `instances/` of its project-management repository `<pm-repo>` (`ls ../<pm-repo>/instances` shows it; the project lead gives it).
> - **Three repositories, side by side**: `gse-light` (this method, public), `<pm-repo>` (your project's management, private) and your product repository `<product-repo>` (the code, private; one or several) — or, until it exists, your sandbox.

**Words used here** (the people — client, product owner, project lead, developers, Project Advisor, Claude sessions — are in *Who is who* just below; every other term and acronym: the [glossary](../GLOSSARY.md))

| Word | Meaning |
|---|---|
| **Instance** | one project run with this method, and its folder `instances/<instance>/` in `<pm-repo>` |
| **Project-management repository** `<pm-repo>` | the project's shared record — decisions, requirements, plans, minutes, journal — private, one per project. Everyone reads it; each person writes their own part in it through the kit's skills (the project lead: the sprints; the Project Advisor: the cockpit and the minutes); nobody manages the project from it |
| **Sandbox** | your personal, private, throwaway repository `<project>-sandbox-<firstname>` with the kit, for Day 0 and your experiments until the product repositories exist; the project lead's sandbox hosts the design phase |
| **Kit** | the files that make every Claude Code session in a repository follow the method — `CLAUDE.md`, six skills, one agent, permissions, a `gates.sh` stub, a CI workflow — installed with one command, committed with the code |
| **Day 0** | each person's first hour on the project — clone, kit, `.env`, `check.sh`, first session |
| **W1 … W6**, **W-1** | the project's weeks, one sprint each; W-1 is the framing week before W1 |
| **Design phase** | the step of W1 where the project lead, with Claude, turns the project's facts and constraints into twelve technical decisions (`DD` records), in order: repository layout, hosting, environments and promotion path, stack and language, data store, identity, infrastructure as code, continuous integration, test tools, secrets, dependency updates, monitoring — recorded with the kit skill `design-phase` |
| **Register**, **decision record and badges** | one register per kind of decision (`PD` project, `DEC` requirements, `DD` design); every `PD-NN`, `DEC-NNN` or `DD-NN` in these pages is one numbered decision record, with a status badge — 🔴 pending, 🟢 decided, 🟡 provisional; its *decider* (the person the roles record names) is the only one who turns it 🟢 |
| **Gates** | the project's automated checks (tests, lint, end-to-end) run by `./gates.sh` and the CI before a merge; on Day 0 a stub that says "no gates yet" |
| **Go-ahead** | the written yes of the person who holds that right (roles record), before any state-changing action (push to a branch that deploys, deploy, spend) |

<!-- who-is-who:start -->
**Who is who** — who decides what in a given project: its **roles record**, `<pm-repo>/instances/<instance>/governance/10-roles-and-go-aheads.md`.

| Role | Side | What they do | What they decide or write |
|---|---|---|---|
| **Client** | the organisation the product is built for | names the product owner and the data protection contact | — |
| **Product owner** | client | owns the need; accepts each delivered increment | the production and budget go-aheads |
| **Data protection contact** | client | — | how personal data may enter the product |
| **Project lead** (lead developer) | the team | runs the project: sprints, tickets, technical choices, code review; the developers' first contact | the sprints; the design decisions |
| **Developers** | the team | build the product with Claude Code, each in their own repository ("team member" = the project lead or a developer) | the implementation of their tickets; their own journal entries and pending records |
| **Project Advisor** | outside the team; the method's author | two hours of meeting and two hours of preparation a week; feedback and advice | nothing in the project — the method and the kits only |
| **Claude sessions** | in every repository | propose, measure, write, test | nothing; they act on a go-ahead |
<!-- who-is-who:end -->

The one-page version, to keep at hand: [QUICKSTART.md](../QUICKSTART.md).

## 0. Who provides what

| You need | Who gives it | How |
|---|---|---|
| A **Claude Code licence** (the coding agent) | the Project Advisor (named in the roles record, `<pm-repo>/instances/<instance>/governance/10-roles-and-go-aheads.md`) | an invitation to the Advisor's Claude team, by e-mail; sign in with it, not with a personal account |
| **API keys** for complementary models (if a task needs one) | the client organisation, through the project lead | one variable per vendor in your `.env` (see §3a); never in a file under git |
| Access to the **repositories** (on GitHub) | `<product-repo>` and your sandbox: the project lead; `<pm-repo>`: the host of `<pm-repo>` (named in the roles record) | `<product-repo>` (the code), your sandbox `<project>-sandbox-<firstname>`, and `<pm-repo>` (your project's management: everyone reads it; you write your own journal entries and new 🔴 records in `instances/<instance>/`, pushed by `session-close` and `decision-record`; the project lead also writes the sprints; the cockpit `BRIEFING.md` — the Project Advisor's one-page dashboard — is his); the method `nicolasguelfi/gse-light` is public |
| The **rules** | `gse-light` and `<pm-repo>` | the reference design `gse-light/method/00-reference-design.md` — the method's page of rules for building, testing, delivering and running a product — chapters 0 (purpose and how to read it), 1 (principles), 2 (how people and AI share the decisions) and 13 (working with the AI day to day) first; the project lead adds 15 (the start-of-project checklist); your instance's `<pm-repo>/instances/<instance>/design/00-design-choices.md`, and your repository's `CLAUDE.md` |

The kit targets **Claude Code only**.
If you work with another coding agent, tell the project lead: the rules still apply, the
kit does not install itself there.

## 1. How we work with generative AI here — one page

Claude is fast, tireless, has no memory between sessions and tends to sound sure. The
method gives it memory (files), rules (instructions) and checks (gates, measurements).
Seven principles ([reference design ch. 1](../method/00-reference-design.md#1-guiding-principles)).
Each says who carries it: **you** (a person), **ask Claude**, or **automatic** (Claude by
the rules of your `CLAUDE.md`, or the CI):

1. **Examples first.** Before specifying a need, get a real example and its data from
   the client (one file per example in `<pm-repo>/instances/<instance>/requirements/40-examples/`;
   personal data stays out of git). Link each requirement to its example. *You collect;
   ask Claude to analyse.*
2. **Tests at every step.** Ask for code *with* its tests: unit, integration (real
   database) and, for every user path, **end-to-end tests through the real user interface,
   driven by Claude to play the use case** — this is how the product is verified and
   validated, and it is a firm rule; the tool is the instance's choice (the test-tools
   `DD`; Playwright is one example for a web interface). Each test names the requirement it
   proves. *Ask Claude; you read them.*
3. **Green gates to move forward.** Nothing merges with a red gate (`./gates.sh`, the same
   in CI); nothing goes to the rehearsal environment (a copy of production where a version
   is deployed and checked before production — the environments-and-promotion-path `DD`),
   nor to production, without its go-ahead. *Automatic (CI); a person for the go-ahead.*
4. **Know what is verified.** Coverage on every change, and a weekly map of which
   requirements and qualities have passing tests. *Automatic (CI); you read it.*
5. **Measure before asserting.** "Tests pass", "the rehearsal environment is on 1.4", "the
   import ran": only with the command and its output, dated. Ask Claude the same: *show me
   the command*. Skill `verify-claim`. *Automatic (Claude); ask if missing.*
6. **One source of truth.** No hard-coded identifier of a business object (for example a
   course, a session, a user) in code or tests (tests create their own data); schema from
   migrations, client from the API contract; documentation changes with the code, in the
   same pull request. *Automatic (gates).*
7. **Evaluate is not execute.** Asking Claude to assess changes nothing. Pushing to a
   branch that deploys, migrating a shared database, creating cloud resources, spending
   money: only with the written go-ahead of the person in
   roles and go-aheads (`<pm-repo>/instances/<instance>/governance/10-roles-and-go-aheads.md`) — the rehearsal
   environment: project lead; production, cloud, budget: product owner. The Project Advisor
   advises; he does not decide the project. *Automatic (Claude stops and asks); a person gives it.*

And three habits:

- **Decisions go to the registers**, never as "TODO decide" in a file. A choice between
  options with consequences → skill `decision-record` → a `PD`/`DEC`/`DD` record in
  `<pm-repo>/instances/<instance>/`, 🔴 until its decider decides. Your session can open a
  record and push it (the skill commits that path only); it closes none.
- **Every session ends with a journal entry** in `<pm-repo>/instances/<instance>/journal/` (skill
  `session-close`, which commits and pushes your entry and the metrics row, nothing else):
  what was done with the command that measured it, decisions touched, what is left, a
  hand-over for a reader with no memory. These entries are also research data on
  AI-assisted engineering — never rewritten.
- **Before a pull request, run the `change-reviewer` agent.** It checks gates, data
  regime, secrets, migrations, documentation, decisions, tests — and says "ready" or lists
  the fixes.

**Never**:

- a secret, token or key in a file under git (`.env` is yours alone);
- a push to `main`, or to any branch that deploys, without the go-ahead;
- a personal-data field outside the regime of your instance's data-regime record;
- a claim about a running system without its command;
- editing `<pm-repo>/instances/<instance>/BRIEFING.md` (the Project Advisor's cockpit) or anything under `gse-light` from a project session;
- opening Claude Code in `<pm-repo>`.

The kit's `settings.json` denies Claude the Edit tool on the cockpit and under `gse-light`,
and the literal command `git push origin main`; Claude asks before any `git push`. These
rules are conveniences for the session, not a security boundary: review by a person guards
the rest, with GitHub branch protection on `main` when the project has enabled it (recommended; roles record).

## 2. If you are the project lead

Your Day 0, first session and sprint rhythm are a developer's (§3), run in your own sandbox
then in the product repositories. In addition, you:

- **decide** sprints, priorities, tickets, technical choices inside an approved design
  decision, code review, promotion to the rehearsal environment; the product owner accepts
  increments and gives the production and budget go-aheads; the Project Advisor advises;
- **write in `<pm-repo>`** directly: `instances/<instance>/planning/sprints/`, your journal entries, new 🔴
  records in the registers — never `instances/<instance>/BRIEFING.md` (the cockpit) nor
  the instance `README.md`: the Project Advisor's pages;
- **validate and send the minutes** of each meeting with the Project Advisor, with Claude: your
  session reads `../<pm-repo>/instances/<instance>/meetings/<date>/minutes.md` (the Advisor's
  draft, with his feedback section), you correct what you must, it writes "validated by <your
  name> on YYYY-MM-DD" in the header, commits and pushes that one file (it asks first); you send
  the minutes to the participants (roles record §2);
- **create the sandboxes** on GitHub, one per team member (`<project>-sandbox-<firstname>`,
  private), or ask the Project Advisor to;
- **run the design phase in W1 (the first sprint), in your own sandbox** (skill
  `design-phase`, with Claude): the project's drivers → the twelve `DD` records, in order
  (repository layout, hosting, environments and promotion path, stack and language, data
  store, identity, infrastructure as code, continuous integration, test tools, secrets,
  dependency updates, monitoring) → fill `gates.sh`, the CI and the `<…>` fields of
  `CLAUDE.md` from its decisions; the first decision, repository layout, names the product
  repositories, which then receive the kit; ask the Project Advisor to list them in the
  instance `README.md` (his page);
- **install, commit and refresh the kit** in each product repository, with one command run
  from inside the product clone ([INSTALL.md §2](INSTALL.md#2-if-you-are-the-project-lead--install-the-kit-in-the-product-repository-once-per-product-repository));
  ask Claude to fill the `<…>` fields of `CLAUDE.md` (purpose, commands), and keep "Lessons
  learned here" alive: a rule learned from an incident is added the same day, dated;
- run the **start-of-project checklist** ([reference design ch. 15](../method/00-reference-design.md#15-starting-a-new-project)):
  kit installed in each product repository, gates green on an empty suite (the Day-0 stub,
  then the real gates), the rehearsal environment declared as code, sign-in, database with
  its first migration, secrets in the vault, one end-to-end path through the real user
  interface (the walking skeleton: the thinnest end-to-end slice of the product, deployed
  and tested, built first);
- **never** open Claude Code in `<pm-repo>`, decide in the product owner's place
  (production, budget) or turn 🟢 a record whose decider you are not.

## 3. If you are a developer

- **Read first**: this page, then your repository's `CLAUDE.md`.
- **Install**: the kit in your sandbox only (§3a); a product repository brings it with the clone.
- **Write**, through the kit's skills: your journal entries and your new 🔴 records.
- **Never**: run `install.sh` in a product repository, open Claude Code in `<pm-repo>`, turn a record 🟢 — and the **Never** of §1 holds.

### 3a. Day 0 — get set up (15 minutes to install, 15 for `/upskilling`)

The full procedure, with prerequisites for macOS and Windows and what is shared or
personal, is **[INSTALL.md](INSTALL.md)**. In short:

1. **Prerequisites**: Git with access to the repositories on GitHub, a bash terminal (Git
   Bash on Windows), `python3`, Claude Code signed in with the account the Project Advisor
   invited ([INSTALL.md §1](INSTALL.md#1-prerequisites-everyone)).
2. **Before W1 — in your sandbox.** Until the product repositories exist (the first
   decision of the design phase, repository layout, names them), you work in
   `<project>-sandbox-<firstname>`: a personal, private, throwaway repository on GitHub,
   created for you by the project lead or the Project Advisor. Clone it next to `gse-light`
   and `<pm-repo>`, run the one command in it **yourself**
   (`../gse-light/claude-kit/install.sh <instance>`) and commit the kit
   ([INSTALL.md §3](INSTALL.md#3-if-you-are-a-developer--get-the-kit-about-15-minutes)). Your sessions'
   journal entries and 🔴 records go to `<pm-repo>/instances/<instance>/` through the
   skills, as from any product repository. You never open Claude Code in `<pm-repo>`: the
   sessions opened there are the Project Advisor's.
3. **Once the product repository exists**, clone it side by side with the two others, in
   the same parent folder: the kit is already in it, installed by the project lead with one
   command from inside its clone and committed. **You never run `install.sh` there**; if you
   cloned before the kit was there, `git pull` once the project lead has pushed.
4. **Your `.env`**: `cp .env.example .env`, then fill it with what the project lead gave you.
5. **Check**: `../gse-light/claude-kit/check.sh` from inside your sandbox or product
   repository — every line OK, or it tells you what to do.
6. **Open a session**: `claude`, accept the workspace trust dialog, type `/` and check that
   `design-phase`, `decision-record`, `review`, `session-close`, `verify-claim` and `upskilling` appear.
   Whenever Claude needs your answer, it asks by a short multiple-choice question or, for a
   complex choice, by a review board (skill `review`): the problem restated, every option's
   advantages, drawbacks and consequences, a comment under every point; you send back one line.
   Work locally: a Claude Code session started on claude.ai (web or cloud) sees one
   repository only, not `../gse-light` nor `../<pm-repo>`.
7. **Start from where you are**: in the session, type `/upskilling` (the kit's
   self-assessment skill). Ten minutes of questions and two or three small checks, then a
   short personal plan matched to your responsibilities; your answers stay in your home
   folder, outside every repository ([method](../method/20-upskilling.md)). The method
   comes in two steps: the base in your first sprint, tests and coverage in the second.

**Check you are done**: `../gse-light/claude-kit/check.sh` prints no MISSING line.

### 3b. Your first session, step by step (30 minutes)

Open `claude` in the product repository and work through this, in your own words:

1. *"Read CLAUDE.md and the reference design chapters 0 (purpose), 1 (principles), 2 (how
   people and AI share the decisions) and 13 (working with the AI day to day), then tell me
   in five lines how you will work here."* — check the answer names the gates command, the
   registers and the go-aheads.
2. *"Run the gates and show me the output."* — `./gates.sh` (the Day-0 stub until the
   design phase fills it); green or not, you now know the state, measured.
3. Take a ticket (GitHub issue, in the sprint milestone; it names the requirement or
   decision it serves). *"Propose how to do #NN; change nothing yet."* — read the proposal;
   ask for the alternatives if there is a choice; if it is a real choice, *"record it with
   decision-record"*.
4. *"Do it on a feature branch, run the gates, show me the diff."* — review the diff
   yourself; Claude's code is accepted through the gates **and** your reading.
5. *"Run the change-reviewer agent."* — fix what it lists, then open the pull request to
   the integration branch named in `CLAUDE.md` (from the environments-and-promotion-path
   `DD`). The pull request updates the document that describes the behaviour, in the same
   diff.
6. *"Close the session."* (skill `session-close`) — journal entry in `<pm-repo>/instances/<instance>/journal/`,
   one row in `metrics.csv`. Read the entry: a colleague with no memory must be able to
   resume from it.

What good looks like after a sprint: every claim in your journal has a command next to it;
every pull request was reviewed by the agent and by you; no decision lives only in a chat.

### 3c. The rhythm of a sprint

- **Sprint**: a goal, 3–7 tickets with acceptance criteria, each linked to a
  requirement or a decision. The project lead keeps `<pm-repo>/instances/<instance>/planning/sprints/W<n>.md`
  and the GitHub milestone, and dates and sizes the sprints with the team.
- **Meeting with the Project Advisor**: the method's rhythm is weekly — two hours, the day
  fixed at each meeting for the next one; a part-time period (an October start, for
  example) may hold only two meetings, as the instance's planning says. The Project Advisor
  arrives with a brief measured from GitHub and the journal (merged pull requests, gates,
  increment demonstrable or not, tickets without a requirement, journal entries) — so link
  your tickets and write your journal: that is how your work becomes visible. The minutes
  list, per participant, the tasks for the next sprint, each with the timestamp where it
  was said.
- **Iterative and incremental**: every sprint ends with something demonstrable, merged to
  the integration branch and, when the gates are green and the project lead says so,
  promoted to the rehearsal environment (the environments-and-promotion-path `DD`).
  Branches that live a sprint without a merge are the first thing the brief shows.

## 4. If you are the product owner

- **Install**: nothing, no Claude Code needed.
- **Read**, on GitHub in `<pm-repo>`: the instance `README.md` (project, phase, people), the roles record (your go-aheads: production and budget; you accept each delivered increment), the 🔴 records that await you (each register's §0 dashboard names its decider) and the sprint page for what is demonstrable.
- **Write**: nothing — your decisions are given to the project lead or the Project Advisor and recorded by the Advisor's sessions, 🟢 by you as decider.
- **Never**: the commands of this page — you never need them.

## 5. If you are the Project Advisor

- **Read first**: the cockpit (your page), the journal entries and the weekly brief.
- **Install**: the [pm-kit](../pm-kit/README.md) in `<pm-repo>`, never this kit; your sessions open there.
- **Write**: the cockpit, the draft minutes and your feedback section (the project lead validates and sends them), the instance `README.md` and the governance pages; push only on your own go-ahead.
- **Never**: decide in the project (your advice is 🟡 at most); write a client or project name in `gse-light` (the leak guard refuses it); work in a team member's sandbox or product repository.

## 6. Checklists

Copy into your journal entries and tick with the command that proves each line.

### 6a. Day 0 — in your sandbox, before W1

- [ ] Git, `python3` and Claude Code installed, Claude signed in with the invited account — `git --version`, `python3 --version`, `claude --version`
- [ ] `gse-light`, `<pm-repo>` and your sandbox `<project>-sandbox-<firstname>` cloned side by side, in one parent folder — `ls ..`
- [ ] Kit installed in the sandbox by the one command and committed — `git log --oneline -1 -- .claude`
- [ ] Personal files out of git — `../gse-light/claude-kit/check.sh` (no MISSING line)
- [ ] `.env` created from `.env.example`, not tracked — `git status --short | grep -c .env` → 0
- [ ] Gates run once — `./gates.sh` output quoted (the Day-0 stub)
- [ ] Reference design chapters 0 (purpose), 1 (principles), 2 (how people and AI share the decisions) and 13 (working with the AI day to day) read — the project lead adds 15 (the start-of-project checklist); `CLAUDE.md` read
- [ ] `/upskilling` run once; plan noted in your private record
- [ ] First journal entry written and pushed to `<pm-repo>` (`session-close`), from the sandbox

### 6b. First sprint — in the product repository

- [ ] Design phase done by the project lead (`DD` records in `<pm-repo>`, product repositories named and listed in the instance's `README.md` by the Project Advisor) — or its date known
- [ ] `<product-repo>` cloned next to the others, kit present — `../gse-light/claude-kit/check.sh` (no MISSING line)
- [ ] `.env` created from `.env.example`, not tracked — `git status --short | grep -c .env` → 0
- [ ] Gates run once — `./gates.sh` output quoted (the real gates once the design phase has filled them)
- [ ] First ticket taken, first pull request opened to the integration branch, `change-reviewer` run
- [ ] Journal entry written and pushed (`session-close`)

## 7. Where to ask

- **Technical and sprint questions**: the project lead.
- **Method, Claude, the kit**: the Project Advisor, at the weekly meeting or through the project lead.
- **A question that is really a decision**: open the record (`decision-record`) and let its decider close it.
- **Something the kit should do and does not**: say it — the kit improves from what happens in the sessions.

## Appendix — mistakes already made for you

Illustration — Sumvadis (<https://sumvadis.ai/>), one of the author's own projects, an
illustration and not a reference: its stack is never a default for yours. From the
[reference design, appendix C](../method/00-reference-design.md), each of these produced one
of the rules above:

- a constant for something that changes (a campaign code in tests);
- a measured deviation called a defect when it was a decision;
- a cause announced without re-measuring after the fix;
- a fix applied to one output and not to its twin;
- a rule enforced on screen but not in the exported file;
- a cockpit left stale for a week.

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))
