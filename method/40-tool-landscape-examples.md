# 40 — Tool landscape: examples seen in past projects

Status: **examples seen in past projects, dated 2026-10 — not recommendations** · v0.3 · 2026-10-08 · author: Nicolas Guelfi, with Claude

> **Essentials** — The [reference design](00-reference-design.md) names no technology:
> its rules are invariants, and each project chooses its tools in its design phase from
> its own drivers (the facts and constraints of the project), recorded as `DD` records.
> This page is the only place in the method where tool names appear, apart from GitHub
> (prerequisite of the tooling) and Playwright, named as the one example of the firm
> end-to-end rule. It is a memory of options seen in past projects, so that a team
> collecting its drivers knows what exists; it is **non-normative**: a row here is never
> a default, never a recommendation, and Claude never proposes one without the drivers
> and a `DD` record with its options. The illustration projects are the author's own:
> [Sumvadis](https://sumvadis.ai/) (a web application on managed platforms) and
> [StreamTeX](https://streamtex.org/) (a service on machines the author operates). In
> the **Illustration** column, a project name means the option was lived there; "—"
> means it was evaluated for a project, not lived. **Seen** is the month (YYYY-MM) the
> row was last checked as current: the landscape moves every few months; a row older
> than a year is only history.

## How to use this page

1. *Person (team, project lead)* — collect the drivers first
   (`project/design/10-design-drivers.md`, skill `design-phase`).
2. *Ask Claude* — for each category, open the `DD` record with at least two options; the
   rows below are candidates to score against the drivers, beside any option the team or
   the client organisation brings.
3. *Person (project lead)* — decide; the choice goes to
   `project/design/00-design-choices.md`, not here.

## Options by category

Reference design chapter in the first column; the driver column says what led a project
to that option — the same driver in another project may lead elsewhere. The category
maps to one of the twelve design decisions of the design phase (in order: repository
layout, hosting, environments and promotion path, stack and language, data store,
identity, infrastructure as code, continuous integration, test tools, secrets, dependency
updates, monitoring) as in the reference design's Appendix A.

| Chapter · category | Option | The driver that led a project there | Illustration | Seen |
|---|---|---|---|---|
| 0 · Source control & CI | GitHub + GitHub Actions | prerequisite of the method's own tooling (`gh`, workflows, issues, milestones) | Sumvadis, StreamTeX | 2026-10 |
| 0 · Source control & CI | GitLab CI | an organisation already on GitLab (needs adapted agents) | — | 2026-10 |
| 3 · Language, back end | TypeScript, a light web framework with typed procedure calls (Hono + ORPC) | one language for front and back; a small team fluent in TypeScript | Sumvadis | 2026-10 |
| 3 · Language, back end | Python web frameworks (FastAPI, Django) | a data-heavy product where the analysis code is in Python; a team strong in Python | — | 2026-10 |
| 3 · Language, back end | TypeScript server frameworks (NestJS) | a larger team wanting a structured, opinionated framework | — | 2026-10 |
| 3 · Data processing | a Python analysis pipeline beside the web application | the analysis code already existed in Python; statisticians on the team | Sumvadis | 2026-10 |
| 3 · Data processing | pandas, Polars, dbt | in-memory tables; volumes beyond memory; transformations expressed as SQL models | — | 2026-10 |
| 3 · Optimisation | OR-Tools, PuLP, Pyomo | a scheduling or allocation problem stated as constraints; need for an independent oracle | — | 2026-10 |
| 4 · Hosting, managed platforms | Vercel (front and API) | a small team without operations hours; preview deployment per branch | Sumvadis | 2026-10 |
| 4 · Hosting, managed platforms | a cloud provider's managed container or application service (Azure Container Apps, AWS App Runner, Google Cloud Run) | an organisation whose IT already runs on that cloud, with existing agreements and identity | — | 2026-10 |
| 4 · Hosting, machines you operate | Hetzner Cloud + Coolify (a self-hosted deployment console) | steady load, cost as a constraint, control of the operating system | StreamTeX | 2026-10 |
| 4 · Hosting, shared platform | a shared container platform with a gateway, operated by the organisation's platform team | a platform team already operating containers for several products | — | 2026-10 |
| 5–6 · Container gateway, TLS | Caddy, Traefik | automatic certificates, routing by host name on machines you operate | — | 2026-10 |
| 6 · Infrastructure as code | the cloud provider's own declarative language (for example Bicep on Azure) | that provider as the hosting provider | — | 2026-10 |
| 6 · Infrastructure as code | OpenTofu / Terraform | several providers, or a wish to stay provider-neutral | — | 2026-10 |
| 6 · Infrastructure as code | the provider's own configuration files | managed platforms whose configuration is small | Sumvadis | 2026-10 |
| 6 · Container registry | GitHub Container Registry, the cloud provider's registry | where the CI already authenticates; where the hosting pulls from | — | 2026-10 |
| 6 · DNS and filtering | Cloudflare in front | DNS owned outside the hosting provider; filtering of abusive traffic | — | 2026-10 |
| 6 · Hardening, intrusion banning | fail2ban | machines you operate, exposed SSH or gateway | — | 2026-10 |
| 6 · Secrets | the cloud provider's vault and managed identities (for example Azure Key Vault) | that provider as the hosting provider; identity-based access without stored passwords | — | 2026-10 |
| 6 · Secrets | provider environment variables + 1Password | managed platforms; a team already on a password manager | Sumvadis | 2026-10 |
| 6 · Secrets | Doppler | several environments and providers to feed from one place | — | 2026-10 |
| 7 · Database | PostgreSQL, managed in the EU (Supabase) | a managed database with EU residency; no operations hours | Sumvadis | 2026-10 |
| 7 · Database | PostgreSQL, self-run in a container | machines you operate; backup owned by the team | — | 2026-10 |
| 7 · Migrations | Drizzle, Prisma | TypeScript applications; migrations generated from a typed schema | — | 2026-10 |
| 7 · Migrations | Alembic (SQLAlchemy), Django migrations | Python applications | — | 2026-10 |
| 7 · Backups | `pg_dump` on a schedule, point-in-time recovery | acceptable loss of a day versus minutes (ch. 7) | — | 2026-10 |
| 8 · Dependency updates | Dependabot | GitHub-hosted repositories, no extra service | Sumvadis | 2026-10 |
| 8 · Dependency updates | Renovate | grouped updates, finer rules, a repository with several components | — | 2026-10 |
| 9 · Unit tests | Vitest | TypeScript | Sumvadis | 2026-10 |
| 9 · Unit tests | pytest | Python | — | 2026-10 |
| 9 · Database integration | Testcontainers (a disposable database started by the test run) | integration tests on the real engine, in CI | — | 2026-10 |
| 9 · End-to-end | Playwright | a web interface; a tool Claude runs and reads to simulate the use cases (firm rule: the end-to-end tests go through the real user interface) | Sumvadis | 2026-10 |
| 9 · End-to-end | a bot harness (scripted users against the real API and pages) | long user journeys with many actors | Sumvadis | 2026-10 |
| 9 · Load | Locust, k6 | peaks named by a requirement (planning periods, exports) | — | 2026-10 |
| 11 · Sign-in | the client organisation's identity provider (for example Microsoft Entra ID) | the organisation's directory; single sign-on | — | 2026-10 |
| 11 · Sign-in | Better Auth | external users without an organisation directory, in a TypeScript stack | Sumvadis | 2026-10 |
| 11 · Sign-in | Auth0 | an identity service bought rather than run | — | 2026-10 |
| 11 · Provenance | C2PA signing of published media | AI-generated media published to the public; a gate checks every served file | Sumvadis | 2026-10 |
| 12 · Observability | the hosting provider's logs and metrics + external probes | managed platforms; small team | Sumvadis | 2026-10 |
| 12 · Observability | the cloud provider's monitoring workspace (for example Azure Monitor / Application Insights) | that provider as the hosting provider | — | 2026-10 |
| 12 · Observability | Grafana stack, Sentry | machines you operate; error tracking across services | — | 2026-10 |
| 13 · Model access | direct vendor API keys, or through a model provider such as OpenRouter | one key per vendor in `.env`; switching providers by configuration only | — | 2026-10 |

## Adding a row

A row is added when a project of the method lived or evaluated an option, with the
driver that led there; the Illustration column says which (the project's name if it may
be named, "—" if only evaluated), and the Seen column gives the month the row was last
checked as current. A row is never promoted to a rule: a rule is tool-neutral by
construction ([reference design](00-reference-design.md), Essentials).

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))
