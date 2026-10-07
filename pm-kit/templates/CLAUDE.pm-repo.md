# <pm-repo> — instructions for Claude

This **private** repository holds the project management of the project(s) run with the
method **gse-light**: one folder per project in `instances/<name>/` (cockpit, registers,
requirements, planning, meetings, journal). **No product code here.** The method itself —
reference design, templates, scripts, the kits — lives in the **public** repository
`gse-light`, cloned next to this one (`../gse-light`); its Claude artefacts are copied into
`.claude/` here by `../gse-light/pm-kit/install.sh .`.

**Active instance**: `INSTANCE` in `.env` (empty = the only folder in `instances/`). In skills,
agents and documents, `instances/<instance>/` means the active instance's folder. At the start
of a session, read the active instance's `README.md` for its project, phase and people.
**Method changes go to `../gse-light`, project facts stay here**: never write a client's name,
data or project detail in `gse-light` — `instances/<instance>/private-terms.txt` lists the
terms the leak guard refuses there.

Nicolas Guelfi (NG), author of gse-light, is the **Project Advisor** of each instance, not
its project manager: he gives feedback and advice on project conduct and deliverables, owns the generative-AI method
and the Claude kits, and takes part in requirements choices — two hours of meeting and two
hours of preparation per week. Each instance's project lead writes in its instance folder
(`planning/sprints/`, the team's journal entries, new 🔴 records — never `BRIEFING.md`);
roles per instance in `instances/<instance>/governance/10-roles-and-go-aheads.md`.

## Standing rules

- **Decisions and open questions → a register, never scattered.**
  Project → `instances/<instance>/governance/05-project-decisions.md` (`PD-NN`);
  requirements → `instances/<instance>/requirements/05-decisions.md` (`DEC-NNN`);
  design → `instances/<instance>/design/05-design-decisions.md` (`DD-NN`).
  One format for all: plain-language problem · what to consult · options with
  advantages and drawbacks · recommendation · status badge (🟢 decided, 🔴 pending,
  🟡 provisional) · a §0 dashboard at the top. Use `../gse-light/templates/decision-record.md`
  or the `decision-record` skill.
- **Writing style**: plain words first, technical words second, in every document.
  Define each technical term at first use. Readers are strong scientifically, medium on
  concrete technologies.
- **Evaluate ≠ execute**: when asked to evaluate, assess or propose, change nothing
  outside the document being written. State-changing actions (push, deploy, delete,
  create cloud resources, send messages) need an explicit go-ahead from the person
  named in `instances/<instance>/governance/10-roles-and-go-aheads.md` — in this repository, from the owner
  of the folder being changed: NG for everything except `instances/<instance>/planning/sprints/`,
  the team's journal entries and new 🔴 records, which the project lead owns.
- **Measure before asserting**: never state the state of a system (a branch, a
  deployment, a count) without the command that measured it. Never announce an
  unverified cause.
- **Read the register before calling something a defect**: a measured deviation may be
  a decision already taken.
- **Propagation**: after any change to a fact, grep the whole repository for the old
  claim, not only the edited file.
- **Cockpit discipline**: at the end of every session, refresh `instances/<instance>/BRIEFING.md` §1 (what
  awaits NG: his decisions and the points where the team expects his advice), §1b (what
  awaits the team), reset §2 to the delta since the last acknowledgement, re-stamp the
  date. Use the `cockpit-update` skill. Never push project-management tasks into §1.
- **Light by design**: NG has four hours a week per instance. Prefer one
  artefact that fits in them to several that do not; project management belongs to the
  project lead.
- **One entry point: the session orchestrates** (NG, 2026-10-07). NG never needs a
  command. At start, the hook prints the situation — today, next meeting, next step —
  computed by `../gse-light/scripts/situation.py` from `instances/<instance>/meetings/`. NG's **first message, whatever
  it says** (« go », « bonjour », a remark), means: do that step through the `advisor`
  skill, running the agents and skills yourself (`meeting`, `delivery-auditor`,
  `minutes-verifier`, `decision-record`, `method-lesson`, `session-close`); ask him only
  what only he knows (meeting day, participants, points to raise, validation), one
  short QCM at a time. If his message is a different request, serve it, then return to
  the step. `/advisor` re-assesses on demand.
- **Improve the project from every interaction** (NG, 2026-10-07). This repository, the
  method in `../gse-light`, their documents and Claude artefacts are improved iteratively and incrementally from
  what happens in the sessions. Whenever NG asks for something no artefact covers, an
  artefact does not fit the way he works, or a document is wrong or missing:
  1. name the gap in one line (what was asked, what exists);
  2. do the task by hand if it is small — never block on the gap;
  3. propose the smallest change that would cover it next time (a rule here, a field in
     a template, a step in a skill, a new skill only when nothing else fits), by QCM,
     with its cost in minutes;
  4. on his yes, make it in the same session, measure it, and record the lesson with a
     date through the `method-lesson` skill (one place, propagated — most often the
     section "Lessons learned here" below);
  5. mention it in the journal entry.
  A gap never passes silently; a fix never grows beyond the gap.
- **Journal**: one `instances/<instance>/journal/YYYY-MM-DD-sNN.md` per session plus one row in
  `instances/<instance>/journal/metrics.csv`. Dated entries are never rewritten (they are research data on
  AI-assisted engineering). Use the `session-close` skill.
- **Secrets**: never write a secret, token or key in any repository. Point to where it
  lives (vault name, never its value).
- **Language**: documents are in English (engineers' working language). NG may write
  to you in French; answer him in French.

## Lessons learned here

Dated rules learned from the sessions in this repository (newest first): rule — date —
why. Keep each to two lines; move a rule up into "Standing rules" when it holds everywhere.

- Never write "the repository" (or « le dépôt ») alone: always name it — `gse-light`, this
  project-management repository, the product repository… — in documents, commands' comments
  and messages to NG — 2026-10-07 — NG: « nous avons trop de dépôts ».
- Every artifact published from this repository (deck, review board, page) gets a folder
  in its instance with its sources and an `open.html` from `../gse-light/templates/artifact-open.html`,
  plus a row in `meetings/README.md` — 2026-10-07 — NG: open any artifact from the file
  explorer; board sources were left in a temporary folder.
- Before republishing an artifact (or pushing), re-read what someone else changed and
  merge; never resend your copy — 2026-10-07 — a slide NG edited was overwritten once.
- Never run a shell command that waits on standard input (a bare `cat > file`) —
  2026-10-07 — it blocked a session until stopped by hand.
- Name who does each action — person, ask Claude, automatic — in every plan or support;
  presentations: dark, slides numbered n/N, proposal tone (`meeting` §1b) — 2026-10-07 — NG.
- Lessons that hold for engineers are also copied into the kit template's "Lessons
  learned here" — 2026-10-07 — NG asked to carry the project's lessons into the kit.

- Interact by QCM for simple questions and by review board (an artifact) for complex
  ones; always restate the problem and each option's advantages, drawbacks and
  consequences — 2026-10-07 — NG's directive, applied on the two boards of s02.
- Do not raise GDPR or "keep it out of Dropbox" for meeting recordings: NG handles
  consent himself and the files stay in his Dropbox folder — 2026-10-07 — his line on
  the round-1 board.
- Keep permission deny rules narrow: `Read(./.env.*)` also blocked `.env.example` —
  2026-10-07 — found while building the kit.
- The scaffold's `settings.json` denied `git push origin main` to Claude sessions; NG
  relaxed it for this repository on 2026-10-07 (documentation only, `main` deploys
  nothing) — the go-ahead rule in "Git" below still applies, and the kit template keeps
  the deny for product repositories — found at the first push.

## Checks

Run `python3 ../gse-light/scripts/check_docs.py` before committing, here and after any change
in `../gse-light`: it checks internal links (including links to the method), the registers
and the cockpit counts, that `.claude/` matches the pm-kit, and the **leak guard** — no term
of `instances/<name>/private-terms.txt` in `gse-light`. CI runs the same script
(`.github/workflows/docs.yml`).

## Git

Branch `main`, in this repository and in `../gse-light`. Commit coherent units of work, each
in its own repository; a method change is committed in `gse-light` first, then
`../gse-light/pm-kit/install.sh .` refreshes `.claude/` here (commit that too). A session working for NG pushes only on
his go-ahead (or when he asked for the push in the same request); a session working for
the project lead pushes only his own commits (sprints, journal, new 🔴 records)
and only on his go-ahead.

---

© 2026 Nicolas Guelfi · [`gse-light`](https://github.com/nicolasguelfi/gse-light) · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))
