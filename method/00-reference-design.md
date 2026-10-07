# 00 — Reference design: infrastructure, continuous integration and AI practice for a GenAI-directed project

Status: draft for approval · v0.4 · 2026-10-07 (generic: each project's choices live in its instance) · author: Nicolas Guelfi, with Claude

> **Essentials** — How a product run with this method is built, tested, delivered and
> run, and how people and AI sessions work together on it. Each chapter has two layers
> here: **rules** that hold whatever the tools, and the **best tools today**. The third
> layer, each project's **choice**, lives in its instance:
> `instances/<instance>/design/00-design-choices.md`.
> `instances/<instance>/` designates the project's folder in its private project-management
> repository, cloned next to `gse-light` ([pm-kit](https://github.com/nicolasguelfi/gse-light/blob/main/pm-kit/README.md)).
> Two lived projects illustrate the rules: **Sumvadis** (managed platforms: Vercel +
> Supabase) and **StreamTeX** (machines we operate: Hetzner + Coolify); an organisation's
> shared container platform (one cloud VM + containers) is a third reference.

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
a strong default you may break with a decision record.

**Status.** A project's **recommended practice** once the Project Advisor approves it, and
**binding** for its team once the project lead adopts it at the kick-off — the project
lead may then deviate only with a decision record in the instance's register. Changes to
this page go through a pull request on this repository; a change of rule cites the
decision that motivates it.

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
   integration (pieces together, on a real database), end-to-end (a user path in a real
   browser, driven by Playwright). Claude writes them with the code; a person reads them.
   *Who: ask Claude; person reads.*
3. **Green gates to move forward.** A change moves along the pipeline (branch → `dev` →
   staging → production, ch. 10) only when every gate is green — then, for staging and
   production, on its go-ahead. *Who: automatic (CI); person for the go-ahead.*
4. **Know what is verified.** Coverage is measured on every change (static: which code
   the tests run), and a weekly map shows which requirements and qualities have passing
   tests and which do not (dynamic, ch. 14).
   *Who: automatic (CI); person reads the map.*
5. **Measure before asserting.** A statement about a running system ("production is on
   version X", "the table is empty") is worth nothing without the command that measured
   it and the date. Never announce a cause you have not verified by measuring again after
   the fix. *Sumvadis: a parameter blamed for five faulty renderings explained only three
   of them once re-measured.* *Who: automatic (Claude shows the command).*
6. **One source of truth.** Each fact has one source, and everything else is generated
   or checked against it: the schema from migrations, the API client from the API
   contract, documentation tables from the registers. Anything that changes at run time
   (courses, sessions, users) is read from the system, never written in code or tests;
   tests create their own data. Documentation changes with the code, in the same pull
   request, and a rule held at run time is checked in every output too. *Sumvadis:
   campaign codes written in tests broke the day the campaign closed.* *Who: automatic
   (gates).*
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
  consult, all options with advantages and drawbacks, a recommendation, a status badge
  (🟢 decided, 🔴 pending, 🟡 provisional). Each register opens with a dashboard of
  pending and decided records. Documents state outcomes and link to the record; **no
  document carries its own list of open questions**.
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
- **Tickets.** Work items are GitHub issues in the product repository; each ticket names
  the requirement or decision it serves.

### Lived on Sumvadis

About 160 design decisions over three months, all in one register; the cockpit was the
only document the director read daily. The one real failure — a §1 that went stale for
a week — is why refreshing it is now part of closing every session.

---

## 3. Reference architecture

**In short.** The product reads data from the client's existing systems, keeps only what
it needs, computes indicators and proposals, and shows them through a web application
behind the client's sign-in: *sources → import and checks (each version kept) → database
(dated snapshots, migrations) → application (API + pages) → exports*. Each instance draws
its own.

### Rules

- **Thin, explicit boundaries.** Import jobs, application and exports are separate
  modules with typed interfaces; the application never calls the source system directly.
- **One container image per deployable unit**, configured only by environment variables,
  so the same image runs in staging and production and can move between hosting models.
- **The database is the only state.** No file written on the application's disk
  survives a redeploy; files go to object storage.
- **Computation is reproducible**: an indicator or a proposal records the snapshot date
  and the code version that produced it.

### Best tools today

PostgreSQL for the database; a Python web framework (FastAPI or Django) for API and
pages; Polars or pandas for transformations; OR-Tools or PuLP if the "optimisation" is
a scheduling or allocation problem (see [appendix A](#appendix-a--tool-landscape)).

---

## 4. Two hosting models, compared

**In short.** Either a provider runs the machines and you rent services (Model A), or you
run machines and put your services on them in containers (Model B). Neither is better in
general; they trade money against effort and control.

| Criterion | Model A — managed platforms | Model B — machines you operate, services in containers |
|---|---|---|
| Example | Sumvadis: Vercel (front and API) + Supabase (PostgreSQL, EU) | StreamTeX: Hetzner Cloud + Coolify; a shared platform: one cloud VM with Caddy |
| Control | What the provider exposes | Everything, down to the operating system |
| Cost | Higher per unit, near zero when idle on some providers; grows with each environment | Low and flat; one machine can host several environments |
| Effort | Low: patching, backups, TLS handled | You patch, back up, renew, monitor |
| Isolation between environments | Natural: one project per environment | To build: separate machines or strict container limits |
| Compliance | Provider certifications; region choice | Your configuration is the evidence |
| Lock-in | Real (proprietary services) | Low if you stay on containers and PostgreSQL |
| Scaling | Automatic | Manual, or a bigger machine |

**When to choose which.** Model A when the team is small, operations skills are thin and
cost is secondary. Model B when cost matters, the load is steady, or an existing
platform already does the operating (for example an organisation's shared container platform).

---

## 5. Environments and their independence

**In short.** Three copies of the product: **dev** (each engineer's machine), **staging** (the
rehearsal, identical in shape to production) and **production**. A mistake in one must
not be able to reach another.

### Rules

- Each environment has **its own database, its own secrets, its own identity** in the
  cloud. No credential works in two environments.
- **Data never flows up**: production data is not copied into staging or dev. Staging
  uses synthetic data, or pseudonymised extracts approved under the instance's data regime.
- **Parity of shape, not of size**: same image, same schema, same configuration keys;
  staging may be smaller.
- Under **Model A**: one project or resource group per environment.
  Under **Model B**: staging and production on separate machines, or at least separate
  networks, databases and backups; the control plane (Coolify, or the platform portal)
  is not reachable from the application containers; backups leave the machine.

### Lived

Sumvadis isolates layer by layer (separate Vercel projects and Supabase projects per
environment). StreamTeX today runs a single production server — acceptable for
documentation, not for a data platform; its target is one server per environment.

---

## 6. Infrastructure as code, domains, secrets

**In short.** Every environment is described in files kept in git, so it can be
rebuilt, reviewed and compared; nobody configures production by clicking.

### Rules

- Infrastructure is declared in the product repository (`infra/`) and applied by CI
  with a go-ahead, never from a laptop.
- **Secrets are never in git.** The repository names where a secret lives, never its
  value. Runtime secrets come from a vault through the application's identity.
- **Domains and TLS** are declared too; certificate renewal is automatic and monitored.
- Model B hardening: firewall closed except the gateway, no host ports published by
  services, no container with privileges or access to the Docker socket, automatic
  security updates, intrusion banning (fail2ban), images pinned by digest.

### Best tools today

Model A on Azure: Bicep or OpenTofu, Azure Key Vault, Azure Front Door, managed
identities. Model B: Docker images in a registry (GitHub Container Registry or Azure
Container Registry), Caddy or Traefik as gateway with automatic TLS, Coolify or a shared
platform's module manifests, Cloudflare in front for DNS and filtering.

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
- **Rehearse on a throwaway copy** of the staging database before applying to
  production; a migration that fails in rehearsal never reaches production.
- **Imported data is versioned**: each import is a dated snapshot, so an indicator can
  be recomputed exactly as it was.
- **Backups you can restore**: a backup that was never restored is a hope. Restore
  drills are dated in the journal. Under Model A the provider backs up and you test the
  restore; under Model B you also own the backup itself and its off-machine copy.
- Only fields named by a requirement are imported (data minimisation; the instance's data regime).

### Best tools today

Alembic (SQLAlchemy) or Django migrations in Python; Drizzle or Prisma in TypeScript;
`pg_dump` / point-in-time recovery for backups.

---

## 8. Continuous integration

**In short.** Every change goes through the same automated checks (gates), and a change
that fails a gate cannot be merged or promoted.

### Rules

- **Blocking gates** on every pull request: formatting and lint, type checks, unit and
  integration tests, migration check, security scan of dependencies, documentation
  checks (links, registers), and the domain audits the product needs (for example: no
  personal field outside the allowed list).
- **Local gates identical to CI**: one command (`make gates` or equivalent) runs exactly
  what CI runs. An engineer — or a Claude session — runs it before pushing.
- **Generated artefacts are checked**: if a file is generated (API client, schema
  documentation), CI regenerates it and fails when the committed copy differs.
- **Cross-validation oracle**: a computation that matters (an indicator, an optimisation
  result) is checked against an independent implementation or hand-computed fixtures.
- Model B adds: image build, image vulnerability scan, image signature, digest pinned in
  the deployment manifest.
- Dependency updates arrive automatically (Dependabot or Renovate) and pass the same
  gates.

### Lived on Sumvadis

26 local gates run by one command, the same set in CI; a gate rejects hard-coded campaign
codes; another checks that every served media file carries its provenance signature.

---

## 9. Testing strategy

**In short.** Many fast tests of small pieces, fewer tests of pieces together, a few
tests of the whole path as a user sees it — plus tests that simulate load and freeze the
expected results of important computations.

| Level | What it proves | Tooling |
|---|---|---|
| Unit | a function does what it says | pytest (or Vitest) |
| Database integration | queries and migrations work on a real PostgreSQL | pytest + a disposable PostgreSQL (Testcontainers) |
| End-to-end | a user path works in a real browser, in each supported language | Playwright |
| Layout | pages remain usable on small screens | Playwright with mobile viewports |
| Load | the system holds the expected peak (for example planning periods, exports) | Locust or k6, simulated users |
| Golden vectors | an indicator or optimisation gives the same result on frozen inputs | fixtures + expected outputs in git |

**Rules.** Tests create their own data (principle 6). A bug fixed gets a test that would
have caught it. Flaky tests are fixed or removed, never retried until green.
Claude writes the unit, integration and end-to-end tests together with the code it is
asked for; end-to-end tests drive a real browser (Playwright). Each test names the
requirement or example it proves. Coverage is measured on every change and is a gate;
the weekly map of what is verified and what is not is built from the test names
(principle 4).

---

## 10. Delivery and promotion

**In short.** Code flows from a working branch to staging, then to production; each step
up needs its own go-ahead, and going back is always possible.

```text
 feature branch ──PR + gates──▶ dev ──go-ahead (project lead)──▶ staging ──go-ahead (product owner)──▶ main = production
                                         rehearsal: migrations, e2e, smoke tests     probe + rollback ready
```

### Rules

- Promotion is a **separate decision** from merging: green gates make a version eligible,
  not deployed.
- Under **Model A**, a push to the environment's branch deploys. Under **Model B**, CI
  builds an image once, and promotion moves the same image digest from staging to
  production (rolling or blue-green replacement).
- **Smoke check after every deployment**: health endpoint, version endpoint, one real
  read path. The deployed version is measured, not assumed (principle 5).
- **Rollback** is a documented command, tested once per increment.
- **Freeze** before a critical period of the client's business: no promotion except fixes.

### Lived on Sumvadis

Branches `dev → staging → main`, one go-ahead per step, a dated line per production
promotion in the cockpit's history.

---

## 11. Security, compliance and trust

**In short.** Protect personal data first, keep secrets out of reach, and be able to
prove what we claim.

### Rules

- **GDPR by design**: the instance's data regime (aggregate, pseudonymised, identified)
  decides what may be stored, logged and exported. No log line, error report or
  monitoring trace carries an identifier the regime forbids.
- **EU residency** for every store of personal data, backups included.
- **Sign-in** through the client's identity provider; authorisation by role inside the product; least
  privilege for people and for services.
- **Secrets**: vault, rotation dates recorded, no secret in logs, CI or repositories.
- **Patching** (Model B): operating system and base images updated on a schedule; images
  rebuilt when a vulnerability is fixed upstream.
- **Provenance**: any AI-generated media or document published by the product is labelled; C2PA
  signing is available from the Sumvadis work if needed.
- **Evidence**: a `security.txt` file, a short public page on data handling if the product has
  external users, and a record of processing for the data protection contact.

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

**What you get vs what you run.** Under Model A, the provider gives logs, metrics and
backups; you configure alerts. Under Model B — or as a module of a shared
platform — the platform provides a monitoring workspace; the product exposes health
and metrics in its format.

---

## 13. GenAI-specific practice

**In short.** Claude is a fast, tireless colleague with no memory between sessions and a
tendency to sound sure. The method gives it memory (files), rules (instructions), and
checks (gates and measurements).

### Rules

- **Instruction files.** Every repository has a `CLAUDE.md` built from the
  [kit template](../claude-kit/templates/CLAUDE.product-repo.md): purpose, phase,
  standing rules, commands to run the gates, what never to do. It is short and kept
  true; a rule learned from an incident is added with the date and the reason.
- **Skills and agents** from the [Claude kit](../claude-kit/README.md) give every session
  the same procedures (record a decision, close a session, review a change).
- **One writer per repository** at a time. With several parallel sessions, give each a
  name, one writing session and read-only watchers.
- **Verify AI claims**: a session's statement about the system is accepted only with the
  command and its output. Code is accepted only through the gates and a human review.
- **Propagate fixes**: after correcting a fact, search the whole repository (and the
  instance's other repositories) for the old claim. A fix made by hand in an output is
  carried back into the generator that produced it.
- **Context hand-over**: a long session ends with a journal entry written for a reader
  with no memory — state, rules, what remains, traps.
- **Cost**: model usage per session is recorded in `instances/<instance>/journal/metrics.csv`; expensive
  actions (paid APIs, large generations) need a go-ahead.
- **Model access**: Claude Code licences come from the Project Advisor; API keys for
  complementary models come from the client organisation. Keys live in a git-ignored
  `.env` per repository, one variable per vendor; "direct" and "through a provider such
  as OpenRouter" differ only by configuration, never by code.
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

Checklist for an instance's walking skeleton.
Tick in the instance's journal, with dates.

| When | Item | Model A (managed) | Model B (platform module or Coolify) |
|---|---|---|---|
| Day 0 | Repositories created from the kit; `CLAUDE.md` filled | ✓ | ✓ |
| Day 0 | Registers and cockpit in place | ✓ (`instances/<instance>/`) | ✓ |
| Day 0 | Gates script runs locally and in CI, empty test suite green | ✓ | ✓ |
| Week 1 | Staging environment declared as code | resource group + Bicep | module manifest / Coolify project |
| Week 1 | Sign-in with the client's identity provider on staging | app registration | platform portal grant |
| Week 1 | Database with first migration, backups on | managed PostgreSQL | platform database or own container + off-site backup |
| Week 1 | Secrets in the vault, CI reaches cloud through OIDC | ✓ | ✓ |
| Week 1 | One end-to-end path deployed to staging, smoke-checked | ✓ | ✓ |
| Before first production | Production environment, separate from staging | ✓ | ✓ |
| Before first production | Probe, alerts, runbooks, restore drill done | ✓ | ✓ |
| Before first production | Data protection contact sign-off on data flows | ✓ | ✓ |
| Before first production | Rollback tested | ✓ | ✓ |

---

## Appendix A — Tool landscape

Each instance lists its own proposals.

| Category | Best options today | Sumvadis choice |
|---|---|---|
| Source control & CI | GitHub + Actions; GitLab CI | GitHub + Actions |
| Hosting | Azure (Container Apps, App Service), Vercel, Hetzner + Coolify | Vercel |
| Database | PostgreSQL (managed or self-run) | Supabase PostgreSQL, EU |
| Infrastructure as code | Bicep, OpenTofu/Terraform | provider configuration files |
| Secrets | Azure Key Vault, 1Password, Doppler | provider environment variables + 1Password |
| Sign-in | Microsoft Entra ID, Better Auth, Auth0 | Better Auth |
| Back end | FastAPI, Django; Hono, NestJS | Hono + ORPC (TypeScript) |
| Data processing | Polars, pandas, dbt | Python analysis pipeline |
| Optimisation | OR-Tools, PuLP, Pyomo | — |
| Tests | pytest, Vitest, Playwright, Locust, k6 | Vitest, Playwright, bot harness |
| Observability | Azure Monitor / Application Insights, Grafana stack, Sentry | Vercel + probes |
| Dependency updates | Dependabot, Renovate | Dependabot |

## Appendix B — Templates

- Decision record: [`templates/decision-record.md`](../templates/decision-record.md)
- Session journal entry: [`templates/session-journal.md`](../templates/session-journal.md)
- Product repository instructions: [`claude-kit/templates/CLAUDE.product-repo.md`](../claude-kit/templates/CLAUDE.product-repo.md)
- CI pipeline and gates script: written with the walking skeleton, from
  [`claude-kit/templates/ci-gates.yml`](../claude-kit/templates/ci-gates.yml).

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
image), *migration* (a numbered script that changes the database structure), *OIDC*
(a way for CI to obtain short-lived cloud rights without a stored password), *gate* (an
automated check that blocks a merge or a promotion).

---

© 2026 Nicolas Guelfi · [`gse-light`](https://github.com/nicolasguelfi/gse-light) · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))
