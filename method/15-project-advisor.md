# 15 — The Project Advisor: the method and where the Advisor steps in

Status: draft · v0.3 · 2026-10-07 · generic · author: Nicolas Guelfi, with Claude

> **Essentials** — How a project is run in a few weekly sprints with generative AI under
> this method, who does each action (a person, a person asking Claude, or Claude and the CI
> on their own), and every point where the Project Advisor (Nicolas Guelfi) takes part.
> The team runs the project; the Advisor gives conceptual feedback and advice, owns the AI
> working method and its kit, and now and then brings a technical proposal prepared with
> Claude or drawn from his experience. Each instance records its own version of these
> roles in its project register and its presentations in
> `instances/<instance>/meetings/README.md`.
> `instances/<instance>/` designates the project's folder in its private project-management
> repository, cloned next to `gse-light` ([pm-kit](https://github.com/nicolasguelfi/gse-light/blob/main/pm-kit/README.md)).

## 0. Who does an action — three marks

Every action on this page carries one mark, so that everyone in the room knows what is
theirs:

| Mark | Meaning | Example |
|---|---|---|
| **Person** | a named person does it; Claude cannot | give a go-ahead, accept an increment, read a diff |
| **Ask Claude** | a person asks, Claude does, the person checks | "implement ticket #12 with its tests", "close the session" |
| **Automatic** | Claude by the kit's rules without being asked, or the CI (the server that runs the checks on every change) | open a pending record when a choice appears; run the gates on a pull request |

## 1. Who is in the project

| Who | Does | Decides |
|---|---|---|
| **Product owner** (client side) | says what the product must achieve; gives real examples and data of the need; accepts each delivered piece | the vision; acceptance of increments; production; cloud and client budget |
| **Project lead** (lead engineer) | runs the weeks: plans each week, reviews code, keeps the sprint record | sprints, priorities, tickets, technical choices, promotion to staging |
| **Engineers** | build the product with Claude Code as working partner; collect the examples | implementation within their tickets |
| **Data protection contact** (client side) | guards personal data | any new flow of personal data |
| **Project Advisor** (NG) | conceptual feedback and advice; owns the AI method and the kit; may propose tickets and priorities — the project lead decides | the method and the kit; the Claude Code licences |
| **Claude sessions** | propose, measure, write, test; act only on a go-ahead | nothing on their own |

Full table, per instance: `instances/<instance>/governance/10-roles-and-go-aheads.md`.

**Go-ahead.** Before anyone — a person or Claude — does something that changes a shared
system (deploys a version, changes a shared database, creates a cloud resource, spends
money, opens a new flow of personal data), the person responsible for it writes "yes, do
it" for that one action. The next action of the same kind needs a new "yes". Staging:
project lead. Production, cloud, budget: product owner. Personal data: data protection
contact.

**Who provides what**: the Advisor provides the Claude Code licences; the client provides
the API keys (access codes to paid AI models) for complementary models — the product owner
confirms the budget line.

## 2. The need

Each instance states its need in five lines (`instances/<instance>/requirements/00-vision.md`),
owned by the client's product owner and illustrated with real examples and data before
any requirement is written (principle 1).

## 3. The method

Claude is fast, tireless, has no memory between sessions and tends to sound sure. The
method gives it **memory** (files), **rules** (instructions) and **checks** (tests,
gates and measurements). Today's detail: [reference design ch. 1, 2, 8, 9, 13](00-reference-design.md#1-guiding-principles);
for engineers, the [starting guide](../claude-kit/ONBOARDING.md). The seven principles below
are those of the reference design ch. 1 and of the engineers' kit.

| # | Principle | In practice | Who |
|---|---|---|---|
| 1 | **Examples first** | every need is illustrated with real instances and data before it is specified | Person (product owner gives, team collects); Ask Claude (analyse them into requirements) |
| 2 | **Tests at every step** | unit tests (one function), integration tests (pieces together, real database), end-to-end tests (a user path in a real browser, driven by Playwright); Claude writes them with the code | Ask Claude; Person reads them |
| 3 | **Green gates to move forward** | a change moves along the pipeline (branch → dev → staging → production) only when every gate is green, then on its go-ahead | Automatic (CI); Person (go-ahead) |
| 4 | **Know what is verified** | coverage measured on each change (which lines and branches the tests run) and a map of which features and qualities have passing tests and which do not, read every week | Automatic (CI, built with the walking skeleton); Person (reads the map) |
| 5 | **Measure before asserting** | no statement about a system without the command that measured it | Automatic (Claude shows the command); Person (asks for it) |
| 6 | **One source of truth** | each fact has one source; nothing that changes at run time is hard-coded; documentation changes with the code | Automatic (gates check it) |
| 7 | **Evaluate is not execute** | assessing changes nothing; acting on a shared system needs a go-ahead | Automatic (Claude stops and asks); Person (gives it) |

**Habits, with their actor**

| Habit | Who |
|---|---|
| A choice appears → a pending record in a register (a numbered list of decisions: `PD` project, `DEC` requirements, `DD` design) | Automatic (Claude opens it); Person (the one in charge decides) |
| Each working session ends with a journal entry: what was done, with its commands, and a hand-over | Ask Claude ("close the session"); never rewritten — also research data |
| Before a pull request: gates and the `change-reviewer` agent, then a human reading of the diff | Automatic (Claude and CI); Person (reads, approves) |
| The kit — same `CLAUDE.md`, skills (packaged procedures) and agents (read-only reviewers) in every repository | Automatic (loaded in every session); Advisor maintains it |

## 4. The weeks: where the Advisor steps in

Weeks are numbered from the kick-off: **W-1** is the framing week that ends with it; W1
to Wn follow, one sprint each; the project lead dates them.

| When | Project Advisor (Person) | Team (Person) | Claude |
|---|---|---|---|
| **W-1 · framing** | names, vision draft, licences, reference design; recommends where the repositories live | — | Ask Claude: prepares the kick-off supports |
| **W-1 · kick-off** | presents the method and the kit; leads the round table "where do we start" on the skills grid ([upskilling](20-upskilling.md)) | proposes how to adopt the reference design; asks the client for the examples | Ask Claude: kick-off slides (`slides`) |
| **Each week · day before the meeting** | reads a one-page brief | keeps sprint file, linked tickets, journal | Ask Claude (Advisor's session): measures and writes the brief |
| **Each week · meeting (2 h)** | conceptual feedback on conduct and deliverables; may propose tickets and priorities (the project lead decides) | shows what was delivered; the project lead presents the next sprint | — |
| **Each week · same evening** | validates and sends the minutes | takes its tasks into the next sprint | Ask Claude: transcript, draft minutes, checked against the recording |
| **W1 · examples and data** | advice on the analysis of the need; now and then a technical proposal prepared with Claude | collects examples and source-data exports, writes a dated report per source | Ask Claude: analyses examples and data into requirements |
| **Last week · hand-over** | final retrospective; lessons kept in the method | runbooks, hand-over document | Ask Claude: hand-over document, last journal entry |
| **At any time** | decides changes to the method and the kit | proposes a lesson when something did not fit | Automatic: records the lesson, dated, once agreed |

## 5. The weekly meeting

Two hours, the day fixed at each meeting for the next one. Indicative agenda, adapted by
the participants ([template](../templates/meeting-agenda.md)): facts of the week (10 min);
demo or deliverables (30 min); the Advisor's feedback (25 min); decisions awaiting someone
in the room (20 min); next sprint, presented by the project lead (25 min); tasks per
participant and next date (10 min).

**What the brief measures** (built by the read-only `delivery-auditor` agent; facts with
their commands, not verdicts on people): something demonstrable this week; merges spread
over the week; gates green; test coverage and the map of what is verified; each ticket
linked to its requirement or example; each promotion on its go-ahead; journal written;
decisions in the registers.

**What makes the team's work visible**: the sprint file `instances/<instance>/planning/sprints/W<n>.md` and its
GitHub milestone, tickets linked to a requirement or an example, one journal entry per
session, the coverage report.

## 6. What the Advisor does by default, and does not

By default the Advisor does not write the sprint, the code or the budget, and does not
promote versions along the pipeline. He may propose tickets and priorities — the
project lead decides them — and brings technical proposals when useful. A question
that is really a decision becomes a pending record for the person who holds it.

---

© 2026 Nicolas Guelfi · [`gse-light`](https://github.com/nicolasguelfi/gse-light) · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))
