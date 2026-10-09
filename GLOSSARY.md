# Glossary — the words and acronyms of gse-light

Status: v0.2 · 2026-10-08 · for newcomers to generative software engineering · maintained with the method

> **Essentials** — Every term the method's pages use, in plain words, grouped by theme;
> the acronyms are in one table at the end. Each entry page (README, quick start, install,
> onboarding, an instance's README) defines its own few words in a *Words used here* box
> and sends here for the rest. If a word you meet is missing, open a 🔴 record (a pending
> entry in a decision register, §3) or tell the Project Advisor (the method's author, who
> advises the project without deciding in it, §2): a missing definition is a defect of the
> method.

## 1. Generative software engineering

| Term | Meaning |
|---|---|
| **Generative software engineering (GSE)** | Building software with a generative AI model as a working partner that writes code, tests and documents on request, under rules and checks that keep people in charge. The method gse-light is one way of doing it. |
| **Large language model (LLM), model** | The AI program that reads and writes text (and code). Claude is Anthropic's family of models; a project names which model its sessions use. |
| **Coding agent** | A program that lets a model act on your computer: read and edit files, run commands, use tools, in a loop until the task is done. **Claude Code** is the coding agent this method uses, in a terminal or an editor. |
| **Session** | One conversation with the coding agent, from the moment you open it in a folder to the moment you close it. The model remembers nothing from one session to the next: what must last is written in files; `session-close` writes the session's journal entry. |
| **Prompt** | What you type to the model: a request, a question, an instruction. The method gives the useful prompts in the skills, so that you do not have to invent them. |
| **Context, context window** | Everything the model can see during a session: your messages, the files it read, the rules loaded at start. It is limited; long sessions are summarised, which is one reason to close a session with a journal entry. |
| **Token** | The unit models count text in (roughly three quarters of a word). Paid models are billed per token; the method logs the cost of every paid call. |
| **Hallucination** | A confident statement by the model that is false. The method's answer is the rule *measure before asserting*: a claim about a system comes with the command that measured it. |
| **CLAUDE.md** | The instructions file a coding agent reads at the start of every session in a repository: the project's purpose, commands, rules. The kit creates it; the project lead fills it. |
| **Skill** | A packaged procedure the agent follows when you call it (`/decision-record`, `/session-close`…) or when it recognises the situation. Skills live in `.claude/skills/` and are shared by everyone who clones the repository. |
| **Agent, subagent** | A separate, read-only helper the coding agent launches for one job (`change-reviewer`, `delivery-auditor`…), with its own instructions. It reports; it does not change files. |
| **Hook, start hook** | A small program the coding agent runs at a given moment. The **start hook** runs when a session opens in a project-management repository: it prints the git user and where the project stands (today, next meeting, next step). |
| **Permissions, allow / ask / deny rules** | The settings that say what the agent may do without asking, what it must ask for, and what it may never do (`.claude/settings.json`). Conveniences for the session, not a security boundary. |
| **Kit, Claude kit** | The files that make every Claude Code session in a repository follow the method — `CLAUDE.md`, skills, an agent, permissions, a `gates.sh` stub, a CI workflow — installed with one command, committed with the code. Two kits: `claude-kit` (also called the product kit: product and sandbox repositories) and `pm-kit` (the Project Advisor's sessions in the project-management repository). |
| **Licence, API key** | A **licence** is a paid seat for the coding agent (Claude Code), given by invitation. An **API key** is a secret code that lets a program call a paid model directly; it lives in `.env`, never in a file under git. |
| **`.env`** | A file of personal settings and secrets at the root of a repository, ignored by git and never read by the agent. `.env.example` shows which variables exist, without values. |

## 2. The method and its people

| Term | Meaning |
|---|---|
| **gse-light** | This method: a light way to run a software project with generative AI, with a Project Advisor who gives feedback and advice in two hours of meeting and two hours of preparation a week. |
| **Instance** | One project run with the method, and its folder `instances/<instance>/` in the project-management repository (cockpit, registers, requirements, planning, meetings, journal). |
| **Client** | The organisation the product is built for. It names the product owner and the data protection contact; its name never appears in the public `gse-light` repository (leak guard, §3). |
| **Product owner** | The client's person who owns the need: confirms the vision, accepts each delivered increment, gives the production, cloud and budget go-aheads. |
| **Data protection contact** | The client's person who decides how personal data may enter the product. |
| **Project lead (lead developer)** | The person who runs the project inside the team: sprints, tickets, technical choices, code review, promotion to the rehearsal environment; the developers' first contact. His sandbox hosts the design phase. |
| **Developer** (also: team member, with the project lead) | Anyone who builds the product with the coding agent, in their own repository, under the kit's rules. "Team member" means the project lead or a developer, and is used only when both are meant. |
| **Project Advisor** | The person outside the team who advises it: the method's author, who owns the method and the kits, gives feedback and advice on how the project is run and on what it delivers, and takes part in requirements choices — two hours of meeting and two hours of preparation a week. He decides nothing in the project itself. Named in full at its first use on a page, then "the Advisor". |
| **NG** | The author's initials (Nicolas Guelfi); the Project Advisor of his own instances. |
| **Claude sessions** | The sessions of the coding agent opened by anyone in the project's repositories: they propose, measure, write and test; they decide nothing and act on a go-ahead. |
| **Decider** | For one decision record, the person the roles record names as the one who decides it; the only one who turns the record 🟢. |
| **Host of `<pm-repo>`** | The person who grants access to the project-management repository, named in the roles record. |
| **Actor marks: Person · Ask Claude · Automatic** | On every plan and slide, who does an action: a named person does it; a person asks the agent and checks; the agent does it by the kit's rules without being asked, or the CI does. |
| **Go-ahead** | The written "yes, do it" of the person who holds a right, given before one state-changing action (deploy, change a shared database, create a cloud resource, spend money, open a flow of personal data). The next action of the same kind needs a new yes. |
| **Roles record** | The page of an instance that says who decides what and who gives which go-ahead: `<pm-repo>/instances/<instance>/governance/10-roles-and-go-aheads.md`. |
| **Evaluate ≠ execute** | The rule that a request to assess, review or propose changes nothing; acting needs a go-ahead. |
| **Measure before asserting** | The rule that no one, person or agent, states the state of a system (a version, a count, a test result, a cause) without the command that measured it. |
| **Examples first** | The principle that every need is illustrated with real instances and real data before it is specified. |
| **Light by design** | The principle that the Project Advisor's four hours a week are the budget: one artefact that fits in them beats several that do not. |
| **Lesson** | A dated rule learned from a session, written in one place (`CLAUDE.md` "Lessons learned here", a skill, a template) and propagated. |

## 3. The project's documents

| Term | Meaning |
|---|---|
| **Placeholders `<instance>`, `<pm-repo>`, `<product-repo>`, `<project>`, `<firstname>`** | Words in angle brackets that stand for the project's real names: `<instance>` is the folder name under `instances/` (`ls ../<pm-repo>/instances` shows it; the project lead gives it), `<pm-repo>` the project-management repository, `<product-repo>` a product repository, `<project>` the project's short name (also the parent folder `~/dev/<project>`), `<firstname>` the person's first name in a sandbox name. A page defines `<instance>` before the first command that uses it. |
| **Project-management repository (`<pm-repo>`)** | The project's shared record — decisions, requirements, plans, minutes, journal — private, one per project. Everyone reads it; each person writes their own part in it through the kit's skills (the project lead: the sprints; the Project Advisor: the cockpit and the minutes). Nobody manages the project from it. Sessions opened there are the Project Advisor's. |
| **Product repository (`<product-repo>`)** | A private git repository holding the product's code, with the Claude kit committed in it. One or several: the repository layout is the first design decision. |
| **Sandbox repository** | A personal, private, throwaway repository `<project>-sandbox-<firstname>` with the kit installed, where a team member does Day 0, `/upskilling` and experiments until the product repositories exist; the project lead's sandbox hosts the design phase. |
| **Project-management zone (`<pm-zone>`)** | From a product repository, the path of the instance folder the kit's skills write to: `../<pm-repo>/instances/<instance>/`. |
| **Register** | One document per kind of decision, in one format, with a dashboard at the top: `PD` (project), `DEC` (requirements), `DD` (design). |
| **Record** | One entry of a register (`PD-NN`, `DEC-NNN`, `DD-NN`): the problem in plain words, what to consult, options with advantages and drawbacks, a recommendation, a status badge, who decides (the decider, §2). |
| **Status badge** | 🔴 pending (awaits its decider) · 🟢 decided (who and when are written) · 🟡 provisional (a choice made before the decider was named). |
| **Dashboard (§0)** | The table at the top of a register: one row per record with its badge and who decides. The checks compare it with the records. |
| **Cockpit, `BRIEFING.md`** | The Project Advisor's one-page dashboard in an instance: §1 what awaits him, §1b what awaits the team, §2 what changed since he last acknowledged, §3 the state. Written only by his sessions. |
| **Journal** | One dated entry per session in `journal/` (what was done, with the commands that measured it; decisions touched; a hand-over for a reader with no memory), plus one row in `metrics.csv`. Entries are never rewritten: they are research data. |
| **Hand-over** | The last section of a journal entry: what a session with no memory needs to resume (state, rules learned, traps). |
| **Vision** | The need in five lines, owned by the product owner: who uses the product, which decision it serves, from which evidence, what "better" means measurably, what it will never do. |
| **Example record (`EX-<AREA>-NNN`)** | One real instance of the need (a document, a case, a dataset) kept in `requirements/40-examples/`, one file `EX-<AREA>-NNN-<short-name>.md` each: `EX` example, `AREA` the short code of the part of the product it belongs to, `NNN` its number; `EX-<AREA>-NNN` is the identifier the requirements cite. |
| **Requirement (`FR-<AREA>-NNN`, `NFR-<AREA>-NNN`)** | What the product must do (functional, `FR`) or how well (non-functional, `NFR`), with the same `AREA` codes as the examples; each with acceptance criteria, the example it rests on and the test that proves it. |
| **Data regime** | The level of personal data a product may hold — aggregate, pseudonymised or identified — decided in a requirements record with the data protection contact. |
| **Design drivers** | The facts and constraints of the project that design decisions rest on (users, data, the client's existing systems, skills, budget, hosting capacity, compliance), collected in `design/10-design-drivers.md`. |
| **Design phase** | The step of W1 where the project lead, with Claude, turns the project's facts and constraints (the drivers) into twelve technical decisions, one `DD` record each, in order: repository layout, hosting, environments and promotion path, stack and language, data store, identity, infrastructure as code, continuous integration, test tools, secrets, dependency updates, monitoring — recorded with the kit skill `design-phase`, from his sandbox. The method names no technology; the project chooses. |
| **Reference design** | The method's page of rules for building, testing, delivering and running a product (`method/00-reference-design.md`): rules that hold whatever the tools, "How to choose" questions, and pointers to the instance's decisions. Its chapters most often cited: 0 (purpose and how to read it), 1 (principles), 2 (how people and AI share the decisions), 13 (working with the AI day to day), 15 (the start-of-project checklist). |
| **Template** | A blank document to fill (`templates/`): decision record, journal entry, agenda, minutes, example, requirement, design drivers, skills grid, slides. |
| **Leak guard** | The check (`scripts/check_docs.py`) that no private term of a project (listed in `instances/<instance>/private-terms.txt`: the client's name, the project's name) reaches the public `gse-light` repository, in files or commit messages. |

## 4. The weeks

| Term | Meaning |
|---|---|
| **W-1, W0** | The framing weeks before the project's first sprint: names, vision draft, licences, kick-off, examples requested, sandboxes. |
| **W1 … Wn** | The project's weeks, one sprint each. W1 holds the design phase; the last week holds the hand-over. |
| **Sprint** | One week with a goal, a few tickets with acceptance criteria, and something demonstrable at the end; one file per sprint in `planning/sprints/`. |
| **Ticket, issue** | One unit of work on the forge (GitHub issue), linked to a requirement or an example, grouped in a **milestone** per sprint. |
| **Kick-off** | The first meeting: the method and its rules presented and adopted, the need and the examples, who decides what, the calendar. |
| **Weekly meeting** | The Project Advisor's two hours with the team: facts measured the day before (the **brief**), feedback, decisions, tasks per participant in the **minutes**, each cited from the recording's transcript. |
| **Day 0** | Each person's first hour on the project: clone the repositories, the kit, `.env`, `check.sh`, a first session, `/upskilling`, a first journal entry. |
| **Upskilling** | The kit skill that measures where a person starts (eight dimensions, scale 0–3), compares with what their responsibilities need, and proposes a short personal plan; answers stay in the person's home folder. |
| **Skills grid** | The eight dimensions of the round table at the kick-off (AI assistants, coding agents, reviewing AI code, git and pull requests, tests and CI, and three the instance replaces with its own stack). |
| **Hand-over** (project) | The last week's deliverables: runbooks, the hand-over document, a final retrospective. |

## 5. Building, testing, delivering

| Term | Meaning |
|---|---|
| **Repository, clone, branch, commit, push, pull** | Git words: the project's history (**repository**), your local copy (**clone**), a line of work (**branch**), one saved change (**commit**), sending it to the forge (**push**), fetching others' changes (**pull**). |
| **Forge** | The service that hosts repositories, pull requests and CI; the method's own tooling assumes GitHub. |
| **Pull request (PR)** | A proposed change on the forge, reviewed by a person and checked by the CI before it is merged. |
| **Branch protection** | A forge setting that forbids direct pushes to a branch (`main`) and requires a pull request: the real guard behind the kit's convenience rules, decided per project. |
| **Gates, `gates.sh`** | The automated checks run on every change — unit, integration and end-to-end tests, coverage, lint, documentation checks. `bash ./gates.sh` runs them locally; the CI runs the same. A red gate blocks the merge. On Day 0 the script is a stub that says "no gates yet". |
| **Continuous integration (CI)** | The forge's server that runs the gates on every pull request and push (`.github/workflows/gates.yml`). |
| **Lint** | An automatic reading of the code for style and common mistakes, without running it. |
| **Unit, integration, end-to-end tests** | Tests of one piece in isolation; of pieces working together with a real data store; of a whole user path **through the real user interface**, driven by the agent to replay the use cases. The end-to-end rule is firm; the tool is the project's choice. |
| **Coverage** | The share of the code the tests actually run, measured on every change, kept as a gate. |
| **Verified map** | The weekly table of which requirements and qualities have passing tests and which do not. |
| **Smoke check** | A one-minute check that a deployed version is alive and answers (a health page, one real request). |
| **Walking skeleton** | The thinnest end-to-end slice of the product — one path from the user interface to the data store — deployed and tested first, in week 2. |
| **Increment** | The set of changes promoted to production on one go-ahead; a sprint ends with something demonstrable, an increment when accepted. |
| **Environments, rehearsal environment, production** | The places a version runs: the developer's machine, an integration environment, at least one **rehearsal environment** (a copy of production where a version is checked before production), and **production** (what users use). Names and number are the project's decision. |
| **Promotion** | Moving a version from one environment to the next, on green gates and the go-ahead for that step. |
| **Rollback** | Putting the previous version back when a promotion goes wrong; always ready before a promotion. |
| **Infrastructure as code (IaC)** | Declaring environments in files kept in git, so they can be recreated identically. |
| **Container, image** | A packaged application with everything it needs to run (**container**), started from a file that defines it (**image**). One option among others for the build artefact. |
| **Migration** | A numbered script that changes the structure of the database, rehearsed before production. |
| **Secrets** | Passwords, keys and tokens: never in files under git; where they live is a design decision. |
| **Monitoring, runbook** | Watching a running system (health, errors, cost) and, for each foreseeable incident, a written procedure (**runbook**): symptom, check, fix, rollback. |

## 6. Acronyms

| Acronym | Stands for | See |
|---|---|---|
| **AI** | Artificial intelligence | §1 |
| **API** | Application programming interface: the way one program calls another; an **API key** opens a paid one | §1 |
| **CI** | Continuous integration | §5 |
| **DD-NN** | Design decision record number NN, in the design register | §3 |
| **DEC-NNN** | Requirements decision record, in the requirements register | §3 |
| **E2E** | End-to-end (test) | §5 |
| **EX-<AREA>-NNN** | Example record: `EX` example, `AREA` the short code of the part of the product, `NNN` its number — the identifier the requirements cite | §3 |
| **FR-<AREA>-NNN, NFR-<AREA>-NNN** | Functional, non-functional requirement, with the same `AREA` codes | §3 |
| **GSE** | Generative software engineering | §1 |
| **IaC** | Infrastructure as code | §5 |
| **LLM** | Large language model | §1 |
| **NG** | The author's initials; the Project Advisor of his own instances | §2 |
| **PD-NN** | Project decision record, in the project register | §3 |
| **PR** | Pull request | §5 |
| **QCM** | *Questionnaire à choix multiples*: a short multiple-choice question, the way a Claude session asks a person one simple thing at a time (skill `review`) | §2 |
| **Review board** | an interactive page of proposals by subject — the problem restated, each option's advantages, drawbacks and consequences, a recommendation, a comment under every point — that the person ticks and sends back as one line; how a session asks for a complex choice, a validation or a decision (skill `review`) | §2 |
| **W-1, Wn** | The framing week before the first sprint; week n of the project | §4 |
| **🔴 🟢 🟡** | Pending, decided, provisional (status badges) | §3 |

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))
