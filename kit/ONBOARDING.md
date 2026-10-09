# Working with generative AI under this method — starting guide for the team

Status: v0.9 · 2026-10-09 · generic · one repository per project (board r11) · for the project lead and the developers, with a short section for the product owner and the Project Advisor · maintained by the Project Advisor

> **Essentials** — A project run with this method is built in sprints with Claude Code as a
> working partner, under a few firm rules: measure before asserting, decisions in registers,
> nothing state-changing without a go-ahead. This guide gets a team member from zero to a
> first productive session in about an hour and tells the rhythm of the weeks after.
>
> - **The hour**: 10 minutes to clone and check, 15 for `/upskilling`, 30 for the first session.
> - **The order of reading**: the part for everyone first (§0–§1), then your own section (§2–§5), then the checklists (§6).
> - **Fields written `<like this>`** are filled by the project lead at the kick-off; `<project-repo>` is your project's repository, `project/` the folder in it that holds the shared record.
> - **Two repositories, side by side**: `gse-light` (this method, public) and `<project-repo>` (the code and the project's shared record, private). Everyone opens Claude Code in `<project-repo>`.

**Words used here** (the people — client, product owner, project lead, developers, Project Advisor, Claude sessions — are in *Who is who* just below; every other term and acronym: the [glossary](../GLOSSARY.md))

| Word | Meaning |
|---|---|
| **Project's repository** `<project-repo>` | the one repository of the project: the code, and in `project/` the shared record — cockpit, registers, requirements, planning, meetings, journal, roles. Everyone reads it; each person writes their own part |
| **Kit** | the files that make every Claude Code session in `<project-repo>` follow the method — `CLAUDE.md`, twelve skills, four agents, permissions and the start hook, a `gates.sh` stub, two CI workflows — installed once by the Project Advisor, committed with the code; you get it by cloning |
| **Day 0** | each person's first hour on the project — clone, `.env`, `check.sh`, first session |
| **W1 … W6**, **W-1** | the project's weeks, one sprint each; W-1 is the framing week before W1 |
| **Design phase** | the step of W1 where the project lead, with Claude, turns the project's facts and constraints into twelve technical decisions (`DD` records), in order: repository layout, hosting, environments and promotion path, stack and language, data store, identity, infrastructure as code, continuous integration, test tools, secrets, dependency updates, monitoring — recorded with the kit skill `design-phase` |
| **Register**, **decision record and badges** | one register per kind of decision (`PD` project, `DEC` requirements, `DD` design) in `project/`; every `PD-NN`, `DEC-NNN` or `DD-NN` in these pages is one numbered decision record, with a status badge — 🔴 pending, 🟢 decided, 🟡 provisional; its *decider* (the person the roles record names) is the only one who turns it 🟢 |
| **Gates** | the project's automated checks (tests, lint, end-to-end) run by `./gates.sh` and the CI before a merge; on Day 0 a stub that says "no gates yet" |
| **Go-ahead** | the written yes of the person who holds that right (roles record), before any state-changing action (push to a branch that deploys, deploy, spend) |
| **Sandbox** | a personal, private, throwaway repository you may create for experiments outside the project; optional, never audited |

<!-- who-is-who:start -->
**Who is who** — who decides what in a given project: its **roles record**, `project/governance/10-roles-and-go-aheads.md`.

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
| A **Claude Code licence** (the coding agent) | the Project Advisor (named in the roles record, `project/governance/10-roles-and-go-aheads.md`) | an invitation to the Advisor's Claude team, by e-mail or through an identity on his organisation's domain; sign in with it, not with a personal account |
| **API keys** for complementary models (if a task needs one) | the client organisation, through the project lead | one variable per vendor in your `.env` (see §3a); never in a file under git |
| Access to the **project's repository** (on GitHub) | its host, named in the roles record (the project lead, or the client's organisation) | `<project-repo>` holds the code and `project/`: everyone reads it; you write your code by pull request and your own journal entries and new 🔴 records through the kit's skills; the project lead also writes the sprints; the cockpit `project/BRIEFING.md` — the Project Advisor's one-page dashboard — is his. The method `nicolasguelfi/gse-light` is public |
| The **kit** | the Project Advisor installs it once in `<project-repo>` and refreshes it | you get it by cloning; `../gse-light/kit/check.sh` says whether your clone has it |
| The **rules** | `gse-light` and `<project-repo>` | the reference design `gse-light/method/00-reference-design.md` — the method's page of rules for building, testing, delivering and running a product — chapters 0 (purpose and how to read it), 1 (principles), 2 (how people and AI share the decisions) and 13 (working with the AI day to day) first; the project lead adds 15 (the start-of-project checklist); your project's `project/design/00-design-choices.md`, and `CLAUDE.md` at the root of `<project-repo>` |

The kit targets **Claude Code only**.
If you work with another coding agent, tell the project lead: the rules still apply, the
kit does not install itself there.

## 1. How we work with generative AI here — one page

Claude is fast, tireless, has no memory between sessions and tends to sound sure. The
method gives it memory (files), rules (instructions) and checks (gates, measurements).
Seven principles ([reference design ch. 1](../method/00-reference-design.md#1-guiding-principles)).
Each says who carries it: **you** (a person), **ask Claude**, or **automatic** (Claude by
the rules of `CLAUDE.md`, or the CI):

1. **Examples first.** Before specifying a need, get a real example and its data from
   the client (one file per example in `project/requirements/40-examples/`;
   personal data stays out of git). Link each requirement to its example. *You collect;
   ask Claude to analyse.*
2. **Tests at every step.** Ask for code *with* its tests: unit, integration (real
   database) and, for every user path, **end-to-end tests through the real user interface,
   driven by Claude to play the use case** — this is how the product is verified and
   validated, and it is a firm rule; the tool is the project's choice (the test-tools
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
   roles and go-aheads (`project/governance/10-roles-and-go-aheads.md`) — the rehearsal
   environment: project lead; production, cloud, budget: product owner. The Project Advisor
   advises; he does not decide the project. *Automatic (Claude stops and asks); a person gives it.*

And three habits:

- **Decisions go to the registers**, never as "TODO decide" in a file. A choice between
  options with consequences → skill `decision-record` → a `PD`/`DEC`/`DD` record in
  `project/`, 🔴 until its decider decides. Your session can open a record and commit it
  (the skill commits that path only); it closes none.
- **Every session ends with a journal entry** in `project/journal/` (skill
  `session-close`, which commits your entry and the metrics row, nothing else): what was
  done with the command that measured it, decisions touched, what is left, a hand-over for
  a reader with no memory. These entries are also research data on AI-assisted
  engineering — never rewritten.
- **Before a pull request, run the `change-reviewer` agent.** It checks gates, data
  regime, secrets, migrations, documentation, decisions, tests — and says "ready" or lists
  the fixes.

**Never**:

- a secret, token or key in a file under git (`.env` is yours alone);
- a push to `main`, or to any branch that deploys, without the go-ahead;
- a personal-data field outside the regime of your project's data-regime record;
- a claim about a running system without its command;
- editing `project/BRIEFING.md` (the Project Advisor's cockpit) or anything under `gse-light` from a project session;
- running the Project Advisor's skills (`advisor`, `meeting`, `slides`, `cockpit-update`, `method-lesson`, `genai-onboarding`): they check the git user and stop.

The kit's `settings.json` is the floor every session shares: it denies Claude reading `.env`,
a forced push and the literal command `git push origin main`. Your own rules go in
`.claude/settings.local.json` (never committed), copied once from your role's file in
`.claude/roles/`: with `team.json`, Claude asks before any `git push` and may not edit the
cockpit nor `gse-light`. Claude Code adds up the rules of every file and checks deny, then
ask, then allow, so a personal file can add a rule but never lift a shared one. These rules
are conveniences for the session, not a security boundary: GitHub rights guard the rest —
only the Project Advisor writes to `gse-light`; in the project everyone goes through pull
requests, reviewed by a person, with branch protection on `main` when the project has
enabled it (roles record).

**Skipping permission prompts.** The mode that skips Claude Code's confirmations cannot be
set in the project's files (Claude Code ignores it there): it is each person's own choice,
best made per session at launch — for instance with an alias in your shell profile
(`~/.zshrc` or `~/.bashrc`):

```bash
alias claude-libre='claude --dangerously-skip-permissions'
```

— or for all your projects with `"defaultMode": "bypassPermissions"` in `~/.claude/settings.json`.
Even in that mode, deny rules and explicit ask rules still apply (Claude Code documentation:
settings, permissions, permission modes — read 2026-10-09).

## 2. If you are the project lead

Your Day 0, first session and sprint rhythm are a developer's (§3), run in your own clone of
the project's repository. In addition, you:

- **decide** sprints, priorities, tickets, technical choices inside an approved design
  decision, code review, promotion to the rehearsal environment; the product owner accepts
  increments and gives the production and budget go-aheads; the Project Advisor advises;
- **chair the meetings and keep time**; the Project Advisor proposes the topics in his brief;
- **write in `project/`** directly: `planning/sprints/`, your journal entries, new 🔴
  records in the registers — never `BRIEFING.md` (the cockpit) nor `README.md`: the
  Project Advisor's pages;
- **validate and send the minutes** of each meeting with the Project Advisor, with Claude: your
  session reads `project/meetings/<date>/minutes.md` (the Advisor's draft, with his feedback
  section), you correct what you must, it writes "validated by <your name> on YYYY-MM-DD" in
  the header and commits that one file; you send the minutes to the participants (roles record §2);
- **run the design phase in W1 (the first sprint), in your clone** (skill
  `design-phase`, with Claude): the project's drivers → the twelve `DD` records, in order
  (repository layout, hosting, environments and promotion path, stack and language, data
  store, identity, infrastructure as code, continuous integration, test tools, secrets,
  dependency updates, monitoring) → fill `gates.sh`, the CI and the `<…>` fields of
  `CLAUDE.md` from its decisions; the first decision, repository layout, settles how the
  code is laid out in this repository (folders per component, one CI per component if needed);
- keep "Lessons learned here" of `CLAUDE.md` alive: a rule learned from an incident is added
  the same day, dated;
- run the **start-of-project checklist** ([reference design ch. 15](../method/00-reference-design.md#15-starting-a-new-project)):
  gates green on an empty suite (the Day-0 stub, then the real gates), the rehearsal
  environment declared as code, sign-in, database with its first migration, secrets in the
  vault, one end-to-end path through the real user interface (the walking skeleton: the
  thinnest end-to-end slice of the product, deployed and tested, built first);
- **never** install or refresh the kit (the Project Advisor does), decide in the product
  owner's place (production, budget) or turn 🟢 a record whose decider you are not.

## 3. If you are a developer

- **Read first**: this page, then `CLAUDE.md` at the root of the project's repository.
- **Install**: nothing — the kit comes with the clone; three personal steps (§3a).
- **Write**, through the kit's skills: your journal entries and your new 🔴 records.
- **Never**: run `install.sh`, edit the cockpit, turn a record 🟢 — and the **Never** of §1 holds.

### 3a. Day 0 — get set up (10 minutes to clone and check, 15 for `/upskilling`)

The path from zero — no account yet — to your first session is **one numbered table**,
with who does each step: [QUICKSTART.md, "from zero to your first session"](../QUICKSTART.md#if-you-are-a-developer-from-zero-to-your-first-session).
Prerequisites by platform, what is shared or personal and what `check.sh` says:
[INSTALL.md](INSTALL.md). What to know while you follow it:

- **Two clones side by side**, in one parent folder: `gse-light` and `<project-repo>`. The kit
  is already in `<project-repo>`, installed by the Project Advisor and committed. **You never
  run `install.sh`**; if you cloned before the kit was there, `git pull` once he has pushed.
- **Day 0 on your own branch**: `git switch -c day0-<firstname>` in `<project-repo>`; your
  first session, `/upskilling` and your first journal entry happen there; the branch is merged
  or deleted afterwards. A sandbox (your own throwaway repository) is for experiments outside
  the project, if you want one; nothing of value stays there.
- **Your `.env`**: `cp .env.example .env`, then fill it with what the project lead gave you.
- **Your rules for Claude**: `cp .claude/roles/team.json .claude/settings.local.json` (never
  committed); adapt it if you wish — it can add rules, never lift the shared ones (§1).
- **Check**: `../gse-light/kit/check.sh` from inside `<project-repo>` — every line OK, or it
  tells you what to do.
- **Open a session**: `claude`, accept the workspace trust dialog, type `/` and check that
  `design-phase`, `decision-record`, `review`, `session-close`, `verify-claim` and `upskilling`
  appear. Whenever Claude needs your answer, it asks by a short multiple-choice question or,
  for a complex choice, by a review board (skill `review`): the problem restated, every
  option's advantages, drawbacks and consequences, a comment under every point; you send back
  one line. Work locally: a Claude Code session started on claude.ai (web or cloud) sees one
  repository only, not `../gse-light`.
- **`/upskilling`** is the kit's self-assessment skill: ten minutes of questions and two or
  three small checks, then a short personal plan matched to your responsibilities; your
  answers stay in your home folder, outside every repository ([method](../method/20-upskilling.md)).
  The method comes in two steps: the base in your first sprint, tests and coverage in the second.

**Check you are done**: `../gse-light/kit/check.sh` prints no MISSING line.

### 3b. Your first session, step by step (30 minutes)

Open `claude` in the project's repository and work through this, in your own words:

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
6. *"Close the session."* (skill `session-close`) — journal entry in `project/journal/`,
   one row in `metrics.csv`. Read the entry: a colleague with no memory must be able to
   resume from it.

What good looks like after a sprint: every claim in your journal has a command next to it;
every pull request was reviewed by the agent and by you; no decision lives only in a chat.

### 3c. The rhythm of a sprint

- **Sprint**: a goal, 3–7 tickets with acceptance criteria, each linked to a
  requirement or a decision. The project lead keeps `project/planning/sprints/W<n>.md`
  and the GitHub milestone, and dates and sizes the sprints with the team.
- **Meeting with the Project Advisor**: the method's rhythm is weekly — two hours, the day
  fixed at each meeting for the next one; a part-time period may hold fewer meetings, as the
  project's planning says. The project lead chairs and keeps time. The Project Advisor
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
- **Read**, on GitHub in the project's repository: `project/README.md` (project, phase, people), the roles record (your go-aheads: production and budget; you accept each delivered increment), the 🔴 records that await you (each register's §0 dashboard names its decider) and the sprint page for what is demonstrable.
- **Write**: nothing — your decisions are given to the project lead or the Project Advisor and recorded in the registers, 🟢 by you as decider.
- **Never**: the commands of this page — you never need them.

## 5. If you are the Project Advisor

- **Read first**: the cockpit (your page), the journal entries and the weekly brief.
- **Install**: the kit, once, in the project's repository ([INSTALL.md §2](INSTALL.md#2-if-you-are-the-project-advisor--install-the-kit-once-and-refresh-it)); your sessions open there, like everyone's — the start hook tells them apart. Your own rules: `cp .claude/roles/advisor.json .claude/settings.local.json`, once.
- **Write**: the cockpit, the draft minutes and your feedback section (the project lead validates and sends them), `project/README.md` and the governance pages; push only on your own go-ahead.
- **Never**: decide in the project (your advice is 🟡 at most); write a client or project name in `gse-light` (the leak guard refuses it).

## 6. Checklists

Copy into your journal entries and tick with the command that proves each line.

### 6a. Day 0 — in the project's repository, before W1

- [ ] Git, `python3` and Claude Code installed, Claude signed in with the invited account — `git --version`, `python3 --version`, `claude --version`
- [ ] `gse-light` and `<project-repo>` cloned side by side, in one parent folder — `ls ..`
- [ ] The kit present in your clone — `../gse-light/kit/check.sh` (no MISSING line)
- [ ] `.env` created from `.env.example`, not tracked — `git status --short | grep -c .env` → 0
- [ ] Your role's rules copied to `.claude/settings.local.json` — `../gse-light/kit/check.sh` says OK
- [ ] Your Day-0 branch — `git branch --show-current` → `day0-<firstname>`
- [ ] Gates run once — `./gates.sh` output quoted (the Day-0 stub)
- [ ] Reference design chapters 0 (purpose), 1 (principles), 2 (how people and AI share the decisions) and 13 (working with the AI day to day) read — the project lead adds 15 (the start-of-project checklist); `CLAUDE.md` read
- [ ] `/upskilling` run once; plan noted in your private record
- [ ] First journal entry written and committed in `project/journal/` (`session-close`)

### 6b. First sprint

- [ ] Design phase done by the project lead (`DD` records in `project/design/`) — or its date known
- [ ] Gates run once — `./gates.sh` output quoted (the real gates once the design phase has filled them)
- [ ] First ticket taken, first pull request opened to the integration branch, `change-reviewer` run
- [ ] Journal entry written and committed (`session-close`)

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
