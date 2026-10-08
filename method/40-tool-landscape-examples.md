# 40 — Tool landscape: examples seen in past projects

Status: **examples seen in past projects, dated 2026-10 — not recommendations** · v0.1 · 2026-10-08 · author: Nicolas Guelfi, with Claude

> **Essentials** — The [reference design](00-reference-design.md) names no technology:
> its rules are invariants, and each project chooses its tools in its design phase from
> its own drivers (the facts and constraints of the project), recorded as `DD` records.
> This page is the only place in the method where tool names appear. It is a memory of
> options seen in past projects, so that a team collecting its drivers knows what exists;
> it is **non-normative**: a row here is never a default, never a recommendation, and
> Claude never proposes one without the drivers and a `DD` record with its options.
> The illustration projects are the author's own: [Sumvadis](https://sumvadis.ai/) (a
> web application on managed platforms) and [StreamTeX](https://streamtex.org/) (a
> service on machines the author operates). "—" in the last column: an option evaluated
> for a project, not lived. Dated: the landscape moves every few months; a row older than
> a year is only history.

## How to use this page

1. *Person (team, project lead)* — collect the drivers first
   (`instances/<instance>/design/10-design-drivers.md`, skill `design-phase`).
2. *Ask Claude* — for each category, open the `DD` record with at least two options; the
   rows below are candidates to score against the drivers, beside any option the team or
   the client organisation brings.
3. *Person (project lead)* — decide; the choice goes to
   `instances/<instance>/design/00-design-choices.md`, not here.

## Options by category

Reference design chapter in the first column; the driver column says what led a project
to that option — the same driver in another project may lead elsewhere.

| Chapter · category | Option | The driver that led a project there | Illustration |
|---|---|---|---|
| 0 · Source control & CI | GitHub + GitHub Actions | prerequisite of the method's own tooling (`gh`, workflows, issues, milestones) | Sumvadis, StreamTeX |
| 0 · Source control & CI | GitLab CI | an organisation already on GitLab (needs adapted agents) | — |
| 3 · Language, back end | TypeScript, a light web framework with typed procedure calls (Hono + ORPC) | one language for front and back; a small team fluent in TypeScript | Sumvadis |
| 3 · Language, back end | Python web frameworks (FastAPI, Django) | a data-heavy product where the analysis code is in Python; a team strong in Python | — |
| 3 · Language, back end | TypeScript server frameworks (NestJS) | a larger team wanting a structured, opinionated framework | — |
| 3 · Data processing | a Python analysis pipeline beside the web application | the analysis code already existed in Python; statisticians on the team | Sumvadis |
| 3 · Data processing | pandas, Polars, dbt | in-memory tables; volumes beyond memory; transformations expressed as SQL models | — |
| 3 · Optimisation | OR-Tools, PuLP, Pyomo | a scheduling or allocation problem stated as constraints; need for an independent oracle | — |
| 4 · Hosting, managed platforms | Vercel (front and API) | a small team without operations hours; preview deployment per branch | Sumvadis |
| 4 · Hosting, managed platforms | Azure Container Apps, Azure App Service | a client organisation whose IT runs on Azure with existing agreements and identity | — |
| 4 · Hosting, machines you operate | Hetzner Cloud + Coolify (a self-hosted deployment console) | steady load, cost as a constraint, control of the operating system | StreamTeX |
| 4 · Hosting, shared platform | an organisation's container platform: one cloud VM, containers, Caddy as gateway | a platform team already operating containers for several products | — |
| 5–6 · Container gateway, TLS | Caddy, Traefik | automatic certificates, routing by host name on machines you operate | — (Caddy on a shared platform) |
| 6 · Infrastructure as code | Bicep | Azure as the hosting provider | — |
| 6 · Infrastructure as code | OpenTofu / Terraform | several providers, or a wish to stay provider-neutral | — |
| 6 · Infrastructure as code | the provider's own configuration files | managed platforms whose configuration is small | Sumvadis |
| 6 · Container registry | GitHub Container Registry, Azure Container Registry | where the CI already authenticates; where the hosting pulls from | — |
| 6 · DNS and filtering | Cloudflare in front | DNS owned outside the hosting provider; filtering of abusive traffic | — |
| 6 · Hardening, intrusion banning | fail2ban | machines you operate, exposed SSH or gateway | — |
| 6 · Secrets | Azure Key Vault, managed identities | Azure hosting; identity-based access without stored passwords | — |
| 6 · Secrets | provider environment variables + 1Password | managed platforms; a team already on a password manager | Sumvadis |
| 6 · Secrets | Doppler | several environments and providers to feed from one place | — |
| 7 · Database | PostgreSQL, managed in the EU (Supabase) | a managed database with EU residency; no operations hours | Sumvadis |
| 7 · Database | PostgreSQL, self-run in a container | machines you operate; backup owned by the team | — |
| 7 · Migrations | Drizzle, Prisma | TypeScript applications; migrations generated from a typed schema | — |
| 7 · Migrations | Alembic (SQLAlchemy), Django migrations | Python applications | — |
| 7 · Backups | `pg_dump` on a schedule, point-in-time recovery | acceptable loss of a day versus minutes (ch. 7) | — |
| 8 · Dependency updates | Dependabot | GitHub-hosted repositories, no extra service | Sumvadis |
| 8 · Dependency updates | Renovate | grouped updates, finer rules, monorepositories | — |
| 9 · Unit tests | Vitest | TypeScript | Sumvadis |
| 9 · Unit tests | pytest | Python | — |
| 9 · Database integration | Testcontainers (a disposable database started by the test run) | integration tests on the real engine, in CI | — |
| 9 · End-to-end | Playwright | a web interface; a tool Claude runs and reads to simulate the use cases (firm rule: the end-to-end tests drive the real interface) | Sumvadis |
| 9 · End-to-end | a bot harness (scripted users against the real API and pages) | long user journeys with many actors | Sumvadis |
| 9 · Load | Locust, k6 | peaks named by a requirement (planning periods, exports) | — |
| 11 · Sign-in | Microsoft Entra ID | the client organisation's identity provider; single sign-on | — |
| 11 · Sign-in | Better Auth | external users without an organisation directory, in a TypeScript stack | Sumvadis |
| 11 · Sign-in | Auth0 | an identity service bought rather than run | — |
| 11 · Provenance | C2PA signing of published media | AI-generated media published to the public; a gate checks every served file | Sumvadis |
| 12 · Observability | the hosting provider's logs and metrics + external probes | managed platforms; small team | Sumvadis |
| 12 · Observability | Azure Monitor / Application Insights | Azure hosting | — |
| 12 · Observability | Grafana stack, Sentry | machines you operate; error tracking across services | — |
| 13 · Model access | direct vendor API keys, or through a model provider such as OpenRouter | one key per vendor in `.env`; switching providers by configuration only | — |

## Adding a row

A row is added when a project of the method lived an option, with the driver that led
there and the illustration project if it may be named; dated in the status line. A row
is never promoted to a rule: a rule is tool-neutral by construction
([reference design](00-reference-design.md), Essentials).

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))
