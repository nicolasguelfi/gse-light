# 00 — Reference design: infrastructure, continuous integration and AI practice for a GenAI-directed project

Status: draft for approval · v0.5 · 2026-10-08 (rules are invariants; every technology is chosen by each project in its design phase) · author: Nicolas Guelfi, with Claude

> **Essentials** — How a product run with this method is built, tested, delivered and
> run, and how people and AI sessions work together on it. Each chapter has three layers:
> (1) **rules** that hold whatever the tools — they name no technology; (2) **how to
> choose**: the decision drivers (the facts and constraints of the project) to collect
> with the team and Claude; (3) the project's **choices**, recorded as design decisions
> (`DD-NN`) in its instance, taken in the **design phase** (first week, kit skill
> `design-phase`): the register `instances/<instance>/design/05-design-decisions.md`, the
> drivers in `instances/<instance>/design/10-design-drivers.md`, and the resulting
> choice per chapter in `instances/<instance>/design/00-design-choices.md`.
> `instances/<instance>/` designates the project's folder in its private project-management
> repository, cloned next to `gse-light` ([pm-kit](https://github.com/nicolasguelfi/gse-light/blob/main/pm-kit/README.md)).
> Examples come from two projects the author led: [Sumvadis](https://sumvadis.ai/) and
> [StreamTeX](https://streamtex.org/). They show that a rule can be applied; they are not
> a starting point: each project chooses its architecture and infrastructure in its design
> phase from its own constraints. Tool names appear only in the dated, non-normative
> [tool landscape — examples](40-tool-landscape-examples.md).

---

## 0. Purpose, scope, how to read

**For whom.** The engineers who build the product (the project lead decides the technical
design), the Project Advisor who recommends and advises, and the Claude sessions that work
with them (they load this document through the [Claude kit](../claude-kit/README.md)).

**What it covers.** Everything between "the code is written" and "the service runs well
for its users": repositories, environments, infrastructure, data evolution, continuous
integration, tests, delivery, security, operations, and the practices specific to
working with generative AI. It does **not** cover what the product does for its users; that is
in the instance's `instances/<instance>/requirements/`.

**How to read.** Chapters 0–2 are for everyone. Chapters 3–12 are the technical body;
read the chapter you are about to work on. Chapter 13 is the AI working method. Chapter
15 is a checklist. When a rule says *must*, a gate or a review enforces it; *should* is
a strong default you may break with a decision record. A **"How to choose"** block lists
the questions the team answers in the design phase, the criteria to weigh the answers,
and the decision record (`DD`) to open; it never names a tool. Claude never proposes the
stack of an example project as a default: it asks the drivers first.

**Status.** A project's **recommended practice** once the Project Advisor approves it, and
**binding** for its team once the project lead adopts it at the kick-off — the project
lead may then deviate only with a decision record in the instance's register. Changes to
this page go through a pull request on the `gse-light` repository; a change of rule cites the
decision that motivates it.

**Prerequisite of the method's tooling.** The method's own scripts, kit and agents assume
**GitHub**: the `gh` command line, pull requests, issues, milestones and CI workflows under
`.github/workflows/`. A project hosted on another forge (a code-hosting service) needs an
adapted agent and an adapted CI template; the rules of this page do not change. This is a
prerequisite of the tooling, not a choice made for the product.

---

## 1. Guiding principles

Seven principles. Principles 5 to 7 were learned the hard way on Sumvadis; principles 1
to 4 were added by the Project Advisor
([Project Advisor's page §3](15-project-advisor.md#3-the-method)), so that
tests, and knowing what they prove, sit at the heart of every step. Each principle names
who carries it: a **person**, a person **asking Claude**, or Claude and the CI
**automatically**.

1. **Examples first.** Every need is illustrated with real instances and data before it
   is specified. The team collects them; each requirement
   links to the example that motivates it. *Who: person (the client gives, the team
   collects); ask Claude to analyse them into requirements.*
2. **Tests at every step.** Code arrives with its tests: unit (one function),
   integration (pieces together, on a real database), end-to-end (a user path through the
   real user interface). **End-to-end tests drive the real user interface and simulate
   the use cases; Claude runs them, for verification and validation** — this rule is
   firm. The tool is the instance's test decision (`DD`); for a web interface, Playwright
   is one such tool. Claude writes the tests with the code; a person reads them.
   *Who: ask Claude; person reads.*
3. **Green gates to move forward.** A change moves along the pipeline (working branch →
   integration → rehearsal → production; names and branch model in the instance's `DD`,
   ch. 10) only when every gate is green — then, for rehearsal and production, on its
   go-ahead. *Who: automatic (CI); person for the go-ahead.*
4. **Know what is verified.** Coverage is measured on every change (static: which code
   the tests run), and a weekly map shows which requirements and qualities have passing
   tests and which do not (dynamic, ch. 14).
   *Who: automatic (CI); person reads the map.*
5. **Measure before asserting.** A statement about a running system ("production is on
   version X", "the table is empty") is worth nothing without the command that measured
   it and the date. Never announce a cause you have not verified by measuring again after
   the fix. *Illustration — Sumvadis: a parameter blamed for five faulty renderings
   explained only three of them once re-measured.* *Who: automatic (Claude shows the command).*
6. **One source of truth.** Each fact has one source, and everything else is generated
   or checked against it: the schema from migrations, the API client from the API
   contract, documentation tables from the registers. Anything that changes at run time
   (courses, sessions, users) is read from the system, never written in code or tests;
   tests create their own data. Documentation changes with the code, in the same pull
   request, and a rule held at run time is checked in every output too. *Illustration —
   Sumvadis: campaign codes written in tests broke the day the campaign closed.* *Who:
   automatic (gates).*
7. **Evaluate is not execute.** Asking someone, human or AI, to assess a situation
   authorises reading and writing a report, nothing else. Changing a shared system
   requires an explicit go-ahead for that action (the instance's roles and go-aheads,
   `instances/<instance>/governance/10-roles-and-go-aheads.md`).
   *Who: automatic (Claude stops and asks); person gives the go-ahead.*

---

## 2. Human-AI project governance

**In short.** People decide, AI sessions propose and execute on request, and everything
decided is written where the next person — or the next session, which remembers
nothing — will find it.

### Rules

- **Roles and go-aheads** are listed in each instance's `instances/<instance>/governance/10-roles-and-go-aheads.md`.
  A go-ahead covers one action; the next action of the same kind needs a new one.
- **Registers.** Three registers, one format: project (`PD-NN`), requirements
  (`DEC-NNN`), design (`DD-NN`). Each record: the problem in plain words, what to
  consult, the drivers it rests on, all options with advantages and drawbacks, a
  recommendation, a status badge (🟢 decided, 🔴 pending, 🟡 provisional). Each register
  opens with a dashboard of pending and decided records. Documents state outcomes and
  link to the record; **no document carries its own list of open questions**.
- **Design phase.** The first week opens the design decisions the product needs
  (architecture, hosting, repository layout, data, tests, delivery, identity, residency)
  from the drivers collected with the team; the project lead decides them, the Project
  Advisor advises (kit skill `design-phase`, ch. 15). Until they are decided, the gates
  script of each product repository is a stub that passes and says so.
- **Cockpit.** Each instance's `instances/<instance>/BRIEFING.md` is the Project Advisor's single entry point:
  §1 what awaits him (his decisions, the points where the team expects his advice), with
  links; §1b what awaits the team; §2 what changed since his last acknowledgement; §3
  state. It is refreshed at the end of every session. A stale §1 is a defect.
- **Sprints.** Weekly sprints; one file per sprint in `instances/<instance>/planning/sprints/` and one
  GitHub milestone, both kept by the project lead. The Project Advisor's weekly
  brief reads them; the Project Advisor writes no sprint.
- **Journal.** One file per working session in the instance's `instances/<instance>/journal/`, plus
  one row in `metrics.csv`. Entries are dated and never rewritten: they are both the
  project's memory and research data on AI-assisted engineering.
- **Tickets.** Work items are GitHub issues in the product repository (several
  repositories: in the one the ticket changes); each ticket names the requirement or
  decision it serves.

### Illustration — Sumvadis

About 160 design decisions over three months, all in one register; the cockpit was the
only document the director read daily. The one real failure — a §1 that went stale for
a week — is why refreshing it is now part of closing every session.

---

## 3. Reference architecture

**In short.** One shape among others, common to products that read data from existing
systems and show indicators or proposals: *sources → import and checks (each version
kept) → store (dated snapshots, migrations) → application (API + user interface) →
exports*. It is an example of a boundary drawing, not a required architecture: each
instance draws its own in its design phase and records it (`DD`, architecture).

### Rules

- **Thin, explicit boundaries.** Import, application and exports (or whatever the
  product's modules are) are separate modules with typed interfaces; the application
  never calls a source system directly.
- **One deployable unit, built once, configured from outside.** Each deployable unit is
  built into one artefact (a container image, a package or a bundle — the instance's
  choice) that is promoted unchanged from rehearsal to production and configured only
  by environment variables or an equivalent external configuration, so it can move
  between hosting models.
- **The store is the only state.** No file written on the application's disk survives a
  redeploy; files go to a store meant for them.
- **Computation is reproducible**: an indicator or a proposal records the snapshot date
  and the code version that produced it.
- **Repository layout is a decision.** One repository or several (for example one per
  deployable unit) is decided in the design phase (`DD`, repository layout); the kit is
  installed in each product repository and the instance's `README.md` in the
  project-management repository lists them (ch. 13).

### How to choose

| Question (driver) | Criteria | Record |
|---|---|---|
| Where does the data come from, how often does it change, who owns it? | number of sources, their interfaces, refresh frequency, right to copy | `DD` architecture |
| What must the product compute — reports, indicators, an optimisation, a workflow? | computation class (query, statistics, scheduling or allocation, simulation) and the skills to maintain it | `DD` architecture, `DD` language and frameworks |
| Who uses it, through what — a web page, an office tool, an API, a mobile device? | the real user interface the end-to-end tests will drive (ch. 9) | `DD` user interface |
| What skills does the team have today and what can it learn in the project's time? | skills grid ([upskilling](20-upskilling.md)), hiring, maintenance after the project | `DD` language and frameworks |
| How many deployable units, and who changes each of them? | team size, release rhythm per unit, shared code | `DD` repository layout |

### Illustration — Sumvadis · StreamTeX

Sumvadis is a web application on managed platforms with a Python analysis pipeline beside
it; StreamTeX is a documentation service on machines the author operates. The same rules
hold in both; the options they took are in the [tool landscape](40-tool-landscape-examples.md).

---

## 4. Two hosting models, compared

**In short.** Either a provider runs the machines and you rent services (**managed
platforms**), or you run machines and put your services on them in containers (**machines
you operate**). These two are compared below because they are the commonest; they are
examples, not the only options — an organisation's **shared platform** (one platform team
operating containers for several products), **serverless functions** or a **platform as
a service** are hosting models too, and are scored on the same criteria. Neither is
better in general; they trade money against effort and control. The choice is a design
decision of the instance (`DD`, hosting).

| Criterion | Managed platforms | Machines you operate, services in containers |
|---|---|---|
| Control | What the provider exposes | Everything, down to the operating system |
| Cost | Higher per unit, near zero when idle on some providers; grows with each environment | Low and flat; one machine can host several environments |
| Effort | Low: patching, backups, TLS handled | You patch, back up, renew, monitor |
| Isolation between environments | Natural: one project per environment | To build: separate machines or strict container limits |
| Compliance | Provider certifications; region choice | Your configuration is the evidence |
| Lock-in | Real (proprietary services) | Low if you stay on containers and a standard database |
| Scaling | Automatic | Manual, or a bigger machine |

### How to choose

| Question (driver) | What it weighs |
|---|---|
| Does the client organisation already operate a platform that must host the product? | an imposed model, with its portal, its monitoring and its rules — score the others only as fallbacks |
| Where must the data live (country, region), and who must be able to audit it? | residency and compliance (ch. 11) exclude some providers outright |
| Who will operate the product after the project, with what skills and hours? | effort and patching; a thin team without operations skills leans to managed platforms |
| Is the load steady or in peaks; is cost a constraint or secondary? | flat cost of machines versus elastic cost of managed services |
| How many environments are needed (ch. 5), how isolated? | cost per environment, isolation to build |
| How much lock-in is acceptable, for how long? | portability of the build artefact (ch. 3) and of the database |

Score each candidate model on the criteria above with the team; record the scores and
the choice in the `DD`. **Illustration** — Sumvadis took managed platforms because the
team was small and had no operations hours; StreamTeX took machines it operates because
its load is steady and cost mattered.

---

## 5. Environments and their independence

**In short.** Several copies of the product — at least a **development** copy per
engineer, **one rehearsal environment** (identical in shape to production) and
**production**. A mistake in one must not be able to reach another. How many
environments, their names and who promotes to each are decided in the design phase
(`DD`, environments).

### Rules

- **At least one rehearsal environment before production.** Nothing reaches production
  that was not deployed and smoke-checked in a rehearsal environment first.
- Each environment has **its own database, its own secrets, its own identity** with the
  hosting provider. No credential works in two environments.
- **Data never flows up**: production data is not copied into rehearsal or development.
  Rehearsal uses synthetic data, or pseudonymised extracts approved under the instance's
  data regime.
- **Parity of shape, not of size**: same build artefact, same schema, same configuration
  keys; rehearsal may be smaller.
- **Isolation is built, then measured**: on managed platforms, one project or resource
  group per environment; on machines you operate, separate machines or at least separate
  networks, databases and backups; the control plane (the console that deploys) is not
  reachable from the application's containers; backups leave the machine. The isolation
  claimed is checked by a command recorded in the journal.

### How to choose

| Question (driver) | What it weighs |
|---|---|
| How many people will test before production (product owner, pilot users, a client acceptance team)? | one rehearsal environment, or a separate acceptance environment |
| Does the hosting model price each environment (ch. 4)? | the number of environments the budget allows |
| Can real data be pseudonymised, or must rehearsal run on synthetic data only? | the data regime (ch. 11) and who approves extracts |

### Illustration — Sumvadis · StreamTeX

Sumvadis isolates layer by layer (one provider project per environment, for the
application and for the database). StreamTeX ran a single production server — acceptable
for documentation, not for a data platform; its target is one server per environment.

---

## 6. Infrastructure as code, domains, secrets

**In short.** Every environment is described in files kept in git, so it can be
rebuilt, reviewed and compared; nobody configures production by clicking.

### Rules

- Infrastructure is declared in the product repository (`infra/`, or the layout the
  instance decides) and applied by CI with a go-ahead, never from a laptop.
- **Secrets are never in git.** The repository names where a secret lives, never its
  value. Runtime secrets come from a vault (a service that holds secrets and hands them
  out to identities it recognises) through the application's identity.
- **Domains and TLS** are declared too; certificate renewal is automatic and monitored.
- **Hardening when you operate the machines**: firewall closed except the gateway, no
  host ports published by services, no container with privileges or with access to the
  container runtime's control socket, automatic security updates, automatic banning of
  repeated intrusion attempts, build artefacts pinned by digest (their fingerprint).
  The instance's `DD` names the tools that implement each line.

### How to choose

| Question (driver) | What it weighs | Record |
|---|---|---|
| What does the hosting model (ch. 4) provide — a declarative language, a portal, manifests? | the infrastructure-as-code tool is usually dictated by the provider | `DD` infrastructure as code |
| Where may secrets live according to the client organisation's policy? | an imposed vault, or the provider's own | `DD` secrets |
| Who owns the domain names and the DNS of the client organisation? | who declares domains, how fast a change is made | `DD` domains |
| Is there a gateway (reverse proxy) imposed by the platform? | TLS automation, routing | `DD` gateway |

---

## 7. Data and schema evolution

**In short.** The structure of the database changes through numbered, reviewed scripts
(migrations), applied in the same order everywhere, and never in a way that breaks the
version currently running.

### Rules

- **Migration ledger**: every schema change is a migration file in git; the database
  records which ones it has applied. No manual change, ever.
- **Expand, then contract**: add the new column or table, deploy code that uses both,
  migrate data, deploy code that uses only the new one, then remove the old. Each step
  is deployable and reversible on its own.
- **Rehearse on a throwaway copy** of the rehearsal database before applying to
  production; a migration that fails in rehearsal never reaches production.
- **Imported data is versioned**: each import is a dated snapshot, so an indicator can
  be recomputed exactly as it was.
- **Backups you can restore**: a backup that was never restored is a hope. Restore
  drills are dated in the journal. When a provider backs up, you still test the restore;
  when you run the database, you also own the backup itself and its off-machine copy.
- Only fields named by a requirement are imported (data minimisation; the instance's data regime).

### How to choose

| Question (driver) | What it weighs | Record |
|---|---|---|
| Which database engine, and is it managed by the provider or run by the team? | migration tool (usually the one of the application framework), backup ownership | `DD` database, `DD` migrations |
| How much data, how often imported, how long kept? | snapshot storage, retention, cost | `DD` data retention |
| What is the acceptable loss (minutes, a day) and the acceptable time to restore? | backup frequency, point-in-time recovery or daily dumps | `DD` backups |

---

## 8. Continuous integration

**In short.** Every change goes through the same automated checks (gates), and a change
that fails a gate cannot be merged or promoted.

### Rules

- **Blocking gates** on every pull request: formatting and lint, type checks, unit and
  integration tests, migration check, security scan of dependencies, documentation
  checks (links, registers), and the domain audits the product needs (for example: no
  personal field outside the allowed list).
- **Local gates identical to CI**: one command (`./gates.sh`, installed by the kit; a
  stub that passes during the design phase) runs exactly what CI runs. An engineer — or
  a Claude session — runs it before pushing.
- **Generated artefacts are checked**: if a file is generated (API client, schema
  documentation), CI regenerates it and fails when the committed copy differs.
- **Cross-validation oracle**: a computation that matters (an indicator, an optimisation
  result) is checked against an independent implementation or hand-computed fixtures.
- When the build artefact is a container image (`DD`, ch. 3): image build, image
  vulnerability scan, image signature, digest pinned in the deployment manifest.
- **Dependency updates arrive automatically** and pass the same gates; the tool that
  opens them is the instance's choice ([landscape](40-tool-landscape-examples.md)).

### Illustration — Sumvadis

26 local gates run by one command, the same set in CI; a gate rejects hard-coded campaign
codes; another checks that every served media file carries its provenance signature.

---

## 9. Testing strategy

**In short.** Many fast tests of small pieces, fewer tests of pieces together, a few
tests of the whole path as a user sees it — plus tests that simulate load and freeze the
expected results of important computations.

| Level | What it proves | How to choose the tool (driver) |
|---|---|---|
| Unit | a function does what it says | the test runner native to the language and framework decided in the design phase |
| Database integration | queries and migrations work on a real database of the production engine | a disposable database of the same engine, started by the test run |
| End-to-end | a user path works through the real user interface, in each supported language | a tool that drives the product's real interface (a browser, a desktop or mobile application, an API client) and that Claude can run and read |
| Layout | pages remain usable on small screens | the end-to-end tool with the viewports the requirements name |
| Load | the system holds the expected peak (for example planning periods, exports) | a load tool that simulates users on the real paths |
| Golden vectors | an indicator or optimisation gives the same result on frozen inputs | fixtures + expected outputs in git, no tool |

**Rules.** Tests create their own data (principle 6). A bug fixed gets a test that would
have caught it. Flaky tests are fixed or removed, never retried until green.
Claude writes the unit, integration and end-to-end tests together with the code it is
asked for. **End-to-end tests drive the real user interface and simulate the use cases;
Claude runs them, for verification (the product does what was specified) and validation
(it does what the users need)** — a firm rule of the method. The tool is the instance's
test decision (`DD`, tests); for a web interface, Playwright is one such tool. Each test
names the requirement or example it proves. Coverage is measured on every change and is
a gate; the weekly map of what is verified and what is not is built from the test names
(principle 4).

---

## 10. Delivery and promotion

**In short.** Code flows from a working branch to the integration line, then to the
rehearsal environment, then to production; each step up needs its own go-ahead, and
going back is always possible. The branch model (names, how many lines, what deploys
where) is decided in the design phase (`DD`, delivery).

```text
 working branch ──PR + gates──▶ integration ──go-ahead (project lead)──▶ rehearsal ──go-ahead (product owner)──▶ production
                                                 rehearsal: migrations, end-to-end, smoke tests   probe + rollback ready
```

### Rules

- **Promotion is a separate decision** from merging: green gates make a version eligible,
  not deployed.
- **The same build artefact is promoted unchanged**: CI builds it once; promotion moves
  that artefact (by its digest or version) from rehearsal to production, configured from
  outside (ch. 3). On managed platforms where a push to a branch deploys, the branch
  model makes the rehearsal and production branches receive the same commit.
- **Smoke check after every deployment**: health endpoint, version endpoint, one real
  read path. The deployed version is measured, not assumed (principle 5).
- **Rollback** is a documented command, tested once per increment.
- **Freeze** before a critical period of the client's business: no promotion except fixes.

### How to choose

| Question (driver) | What it weighs |
|---|---|
| Does the hosting model deploy on push to a branch, or from an artefact promoted by a command? | branch model: one branch per environment, or one line and tagged artefacts |
| Who gives the go-ahead for each environment (roles record)? | protection rules on the branches or on the promotion command |
| Does the client's business have periods where nothing may change? | freeze windows in the release plan |

### Illustration — Sumvadis

Three branches, one per environment, one go-ahead per step, a dated line per production
promotion in the cockpit's history.

---

## 11. Security, compliance and trust

**In short.** Protect personal data first, keep secrets out of reach, and be able to
prove what we claim.

### Rules

- **GDPR by design**: the instance's data regime (aggregate, pseudonymised, identified)
  decides what may be stored, logged and exported. No log line, error report or
  monitoring trace carries an identifier the regime forbids.
- **Data residency**: every store of personal data, backups included, lives where the
  instance's residency decision says (`DD`, residency); the hosting choice (ch. 4) is
  made under it, not the reverse.
- **Sign-in** through the identity provider the instance decides (`DD`, identity — usually
  the client organisation's); authorisation by role inside the product; least privilege
  for people and for services.
- **Secrets**: vault, rotation dates recorded, no secret in logs, CI or repositories.
- **Patching** when you operate the machines: operating system and base images updated on a
  schedule; artefacts rebuilt when a vulnerability is fixed upstream.
- **Provenance**: any AI-generated media or document published by the product is labelled;
  a signing standard for media provenance was applied on Sumvadis and can be reused.
- **Evidence**: a `security.txt` file, a short public page on data handling if the product has
  external users, and a record of processing for the data protection contact.

### How to choose

| Question (driver) | What it weighs | Record |
|---|---|---|
| Which law and which client policy apply to the data (country, sector)? | residency, allowed providers, retention | `DD` residency |
| Does the client organisation have an identity provider every user already has an account on? | sign-in through it, roles mapped from its groups; otherwise an identity service to run | `DD` identity |
| Which data regime does each requirement need (aggregate, pseudonymised, identified)? | what may be stored and logged; the data protection contact's go-ahead | `DEC` data regime |

---

## 12. Operations and observability

**In short.** Know that the product works before its users tell you otherwise, and know why when
it does not.

### Rules

- **Probes**: an external check of the health endpoint and of one real path, at a
  frequency that matches the stakes; an alert opens a ticket.
- **Logs** structured (one JSON object per line), without personal data beyond the
  regime; **metrics** for latency, errors, job durations and import freshness.
- **Runbooks** for the five most likely incidents (import failed, database full,
  certificate expiring, sign-in broken, bad release): symptom, check, fix, rollback.
- **Incidents** recorded with a timeline and a cause verified by measurement.
- **Dated measurements**: capacity and cost are measured, dated and kept in the journal.

**What you get vs what you run.** On managed platforms, the provider gives logs, metrics
and backups; you configure alerts. On machines you operate — or as a module of a shared
platform — the platform provides a monitoring workspace, or you run one; the product
exposes health and metrics in the format the instance decides (`DD`, observability).

---

## 13. GenAI-specific practice

**In short.** Claude is a fast, tireless colleague with no memory between sessions and a
tendency to sound sure. The method gives it memory (files), rules (instructions), and
checks (gates and measurements).

### Rules

- **Three repositories side by side.** A developer's working folder holds `gse-light`
  (the method, public, never edited), the project-management repository `<pm-repo>`
  (private: registers, sprints, journal) and the product repository (private: the code,
  with the kit committed in it), as siblings. The kit's `install.sh`, run from inside the
  product clone, finds the two others and gives Claude read access to them, with write
  access denied under `gse-light` and on the cockpit. Known limit: a Claude Code session
  opened on claude.ai (web or cloud) sees one repository only — the one it was started
  on — so the method's cross-repository steps run from a local session.
- **Multi-repository products.** When the design phase splits the product into several
  repositories (`DD`, repository layout), the kit is installed in **each** product
  repository; the instance's `README.md` in the project-management repository lists the
  project's repositories, and is the place for an overall view: open Claude Code there,
  with the product repositories added as additional directories, when a task spans them.
- **Instruction files.** Every repository has a `CLAUDE.md` built from the
  [kit template](../claude-kit/templates/CLAUDE.product-repo.md): purpose, phase,
  standing rules, commands to run the gates, what never to do. It is short and kept
  true; a rule learned from an incident is added with the date and the reason.
- **Skills and agents** from the [Claude kit](../claude-kit/README.md) give every session
  the same procedures (record a decision, close a session, review a change, run the
  design phase).
- **One writer per repository** at a time. With several parallel sessions, give each a
  name, one writing session and read-only watchers.
- **Verify AI claims**: a session's statement about the system is accepted only with the
  command and its output. Code is accepted only through the gates and a human review.
- **No default stack**: Claude proposes a technology only after the drivers are collected
  and inside a `DD` record with its options; the examples of this page and of the
  [landscape](40-tool-landscape-examples.md) are illustrations, never defaults.
- **Propagate fixes**: after correcting a fact, search the whole repository (and the
  instance's other repositories) for the old claim. A fix made by hand in an output is
  carried back into the generator that produced it.
- **Context hand-over**: a long session ends with a journal entry written for a reader
  with no memory — state, rules, what remains, traps.
- **Cost**: model usage per session is recorded in `instances/<instance>/journal/metrics.csv`; expensive
  actions (paid APIs, large generations) need a go-ahead.
- **Model access**: Claude Code licences come from the Project Advisor; API keys for
  complementary models come from the client organisation. Keys live in a git-ignored
  `.env` per repository, one variable per vendor; "direct" and "through a model
  provider" differ only by configuration, never by code.
- **Coding agent**: the kit targets Claude Code; independence from the agent is a goal of
  the method's follow-up.
- **The Project Advisor's own kit** (`pm-kit/`, installed in each project-management repository's `.claude/`) is separate from the
  engineers' kit: `advisor` (the entry point), `meeting` (brief, record, transcribe,
  minutes with the tasks per participant), `slides`, and the read-only agents
  `delivery-auditor` and `minutes-verifier`. It serves the weekly meeting; it manages
  nothing.

---

## 14. Documentation and traceability

**In short.** From any requirement you can find the design that serves it and the tests
that prove it, and back.

### Rules

- Identifiers: `FR-<AREA>-NNN` and `NFR-<AREA>-NNN` for requirements, `DD-NN` for design
  decisions, test names citing the requirement they cover.
- A traceability table (`instances/<instance>/requirements/70-traceability.md`) is generated from these
  identifiers by a script, not maintained by hand.
- Each requirement links to the example that motivates it (principle 1); the weekly map
  "requirement → tests → last result" lists unverified requirements and qualities first
  (principle 4).
- Registers carry dashboards; the cockpit links to them.
- The journal is the research record: dated, append-only, with metrics.

---

## 15. Starting a new project

Checklist for an instance's walking skeleton. Tick in the instance's journal, with
dates. Who does it: *Person*, *Ask Claude*, *Automatic*. Every technical item below is
done with the choices of the design phase; none of them names a tool here.

| When | Item | Who |
|---|---|---|
| **W1 · design phase** | **Drivers collected, `DD` records opened and decided with the team** (the twelve decisions of `design-phase` §2, in order) — skill `design-phase`; the Project Advisor advises, the project lead decides | Person (team, project lead); Ask Claude (`design-phase`) |
| Day 0 (W1, in parallel) | Kit installed in each product repository (`install.sh` from inside the clone); `CLAUDE.md` filled with the instance and the project-management repository | Person (project lead); Automatic (`install.sh`) |
| Day 0 | Registers and cockpit in place in `instances/<instance>/` | Ask Claude (pm-kit) |
| Day 0 | Day-0 CI green: `./gates.sh` is a stub that prints "no gates yet: design phase in progress" and passes, run on every pull request and on `main` | Automatic (CI) |
| After the design phase | Gates script filled from the `DD` records (lint, types, tests, migrations, dependency scan, documentation checks); runs locally and in CI, empty test suite green | Ask Claude; Automatic (CI) |
| Week 1–2 | Rehearsal environment declared as code, in the hosting model decided | Ask Claude; Person (go-ahead) |
| Week 1–2 | Sign-in with the identity provider decided, on rehearsal | Ask Claude; Person (client access) |
| Week 1–2 | Database with first migration, backups on (owner per the hosting `DD`) | Ask Claude |
| Week 1–2 | Secrets in the vault decided; CI reaches the hosting provider through a short-lived identity (OIDC), never a stored password | Ask Claude; Person (go-ahead) |
| Week 1–2 | One end-to-end path deployed to rehearsal, smoke-checked, one end-to-end test through the real interface run by Claude | Ask Claude; Person (reads) |
| Before first production | Production environment, separate from rehearsal | Ask Claude; Person (go-ahead) |
| Before first production | Probe, alerts, runbooks, restore drill done | Ask Claude; Person (reads the drill) |
| Before first production | Data protection contact sign-off on data flows | Person |
| Before first production | Rollback tested | Ask Claude; Person (reads) |

---

## Appendix A — Tool landscape

How to choose, per category: the questions the design phase answers, the criteria, and
the record to open. Tool names are **not** here: options seen in past projects, dated
and non-normative, are in [40 — Tool landscape: examples](40-tool-landscape-examples.md).
Each instance lists its own choices in `instances/<instance>/design/00-design-choices.md`.

| Category | Questions (drivers) | Criteria | Record |
|---|---|---|---|
| Source control & CI | — (GitHub is a prerequisite of the method's tooling, ch. 0) | — | — |
| Hosting | imposed platform? residency? who operates after the project? load shape? | control, cost, effort, isolation, compliance, lock-in, scaling (ch. 4) | `DD` hosting |
| Database | managed or self-run? volume, retention, acceptable loss? | engine the team knows, backup ownership, migrations (ch. 7) | `DD` database |
| Infrastructure as code | what the hosting provider offers? | declarative, reviewable in a pull request, applied by CI (ch. 6) | `DD` infrastructure as code |
| Secrets | client policy on vaults? provider vault available? | identity-based access, rotation, no value in git (ch. 6) | `DD` secrets |
| Sign-in | identity provider in the client organisation? external users? | single sign-on, roles from groups, least privilege (ch. 11) | `DD` identity |
| Language and back end | team skills, computation class, who maintains after the project? | learning cost, ecosystem for the computation, test tooling (ch. 3) | `DD` language and frameworks |
| Data processing | volumes, transformations, who writes them? | reproducibility, snapshot versioning (ch. 7) | `DD` data processing |
| Optimisation | is there a scheduling, allocation or planning problem, of what size? | an independent oracle for cross-validation (ch. 8) | `DD` optimisation |
| Tests | what is the real user interface? what are the peaks? | a tool Claude can run and read; drives the real interface (ch. 9) | `DD` tests |
| Observability | what the platform provides? stakes of an outage? | probes, structured logs, metrics, alerts that open tickets (ch. 12) | `DD` observability |
| Dependency updates | — | automatic proposals that pass the gates (ch. 8) | `DD` dependency updates |

## Appendix B — Templates

- Decision record (with its **Drivers** line): [`templates/decision-record.md`](../templates/decision-record.md)
- Design drivers of an instance (`instances/<instance>/design/10-design-drivers.md`): [`templates/design-drivers.md`](../templates/design-drivers.md)
- Session journal entry: [`templates/session-journal.md`](../templates/session-journal.md)
- Product repository instructions: [`claude-kit/templates/CLAUDE.product-repo.md`](../claude-kit/templates/CLAUDE.product-repo.md)
- CI pipeline and gates script: installed by the kit as a stub, filled after the design
  phase from [`claude-kit/templates/ci-gates.yml`](../claude-kit/templates/ci-gates.yml).
- Tool options seen in past projects: [`method/40-tool-landscape-examples.md`](40-tool-landscape-examples.md).

## Appendix C — Anti-patterns lived on Sumvadis

| Anti-pattern | What happened | Rule it produced |
|---|---|---|
| A constant for something that changes | Tests pinned a campaign code; they broke when the campaign closed | Principle 6; a blocking gate on literals |
| A measured deviation called a defect | An audit presented the director's own decision as a drift to fix | Read the register before naming a defect |
| A cause announced without re-measuring | A parameter blamed for five faults explained three | Principle 5, corollary |
| A fix applied to one twin only | The room report kept two defects for five weeks after the participant report was fixed | Fix the generator, then every output |
| A rule enforced only on screen | A guarantee held in the browser vanished in the downloaded report | Check every guarantee on the produced file |
| A stale cockpit | §1 listed done tasks for a week | Cockpit refreshed at every session close |

## Appendix D — Glossary

Each instance keeps its glossary in `instances/<instance>/requirements/01-glossary.md`. Technical terms used
here: *container* (a packaged application with everything it needs to run), *image*
(the file a container starts from), *digest* (the fingerprint that identifies one exact
image or artefact), *migration* (a numbered script that changes the database structure),
*OIDC* (a way for CI to obtain short-lived cloud rights without a stored password), *gate*
(an automated check that blocks a merge or a promotion), *driver* (a fact or constraint
of the project that a decision rests on), *rehearsal environment* (a copy of production
where a version is deployed and checked before production), *forge* (a code-hosting
service with pull requests and CI, such as GitHub).

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))
