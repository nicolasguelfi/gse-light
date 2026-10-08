---
name: decision-record
description: Record a decision or open question of the active instance in the right register (PD, DEC or DD) in the standard format, and update the register's dashboard with who decides. Use whenever a choice appears, a question awaits a decision, or a pending decision is settled.
---

# Record a decision

Each instance keeps every decision and open question in one of three registers, all in the
project-management repository — the private repository that holds `instances/<instance>/`
(this repository if it has an `instances/` folder; from a product repository, the sibling
folder named in its `CLAUDE.md`, `../<pm-repo>`; if absent, draft the record in your answer
and ask the engineer to open a pull request there). The same holds from a personal
**sandbox repository**, used while the product repositories do not exist yet: a sandbox
holds no register — its records go to `../<pm-repo>` like any other. Paths below are
relative to the project-management repository; the method is `../gse-light`:

| Kind | Register | Prefix |
|---|---|---|
| Organisation, people, budget, collaboration tools | `instances/<instance>/governance/05-project-decisions.md` | `PD-NN` |
| What the product must do | `instances/<instance>/requirements/05-decisions.md` | `DEC-NNN` |
| How the product is built and run | `instances/<instance>/design/05-design-decisions.md` | `DD-NN` |

## Steps

1. **Search first.** Grep the three registers for the topic. If a record exists, amend
   it (add an "Amended YYYY-MM-DD" line) rather than creating a duplicate. If the
   question is already decided, say so and cite the record — do not reopen it unless
   asked.
2. **Pick the next number** in the chosen register.
3. **Drivers** (design records, and any record where a technology or a vendor is an
   option): cite the lines of `instances/<instance>/design/10-design-drivers.md` the
   decision rests on (section and fact), and name the driver next to each option. No
   driver page yet, or no line for this choice: say so and run the `design-phase` skill
   (or add the missing driver row) before writing the options. **Never propose an
   illustration project's stack (Sumvadis, StreamTeX) as a default**: the method cites
   them to show how a choice played out, not to set this project's answer.
4. **Write the record** from `../gse-light/templates/decision-record.md`: problem in plain words,
   what to consult, every reasonable option with advantages and drawbacks, one
   recommendation with its reason, status badge.
5. **Update the §0 dashboard** of the register: a row under 🔴 Pending (with the
   "Who decides" column, from `instances/<instance>/governance/10-roles-and-go-aheads.md`) or 🟢 Decided,
   with an anchor link to the record.
6. **Mark a decision 🟢 only on an explicit decision** by the person who holds that
   right (`instances/<instance>/governance/10-roles-and-go-aheads.md`). Write who and when in the outcome.
   The Project Advisor's advice is not a decision; a provisional decision he takes before the
   holder is named is 🟡.
7. If the decision awaits the Project Advisor (his method, his kit, his approval, advice the team
   asked for), add or update a task in `instances/<instance>/BRIEFING.md` §1; if it awaits the project lead,
   the product owner or the data protection contact, §1b — **only from a session in the
   project-management repository**: from a product repository, `BRIEFING.md` is denied to
   Claude; report what §1 or §1b should say in the journal entry instead.
8. Run the documentation gates: inside the project-management repository,
   `python3 ../gse-light/scripts/check_docs.py`; from a product or sandbox repository,
   `python3 ../gse-light/scripts/check_docs.py ../<pm-repo>` (the argument names the
   repository to check). Then, when the author is a developer or the project lead and the
   record is **new and 🔴**: `git -C ../<pm-repo> add instances/<instance>/<register>`,
   `git -C ../<pm-repo> commit -m "<XX-NN> opened"`, `git -C ../<pm-repo> push` (inside the
   project-management repository, drop `-C ../<pm-repo>`) — developers have write access
   there for their own journal entries and new 🔴 records, and the kit's settings make
   Claude ask before any `git push` in a product repository. A decided (🟢) record, an
   amendment of someone else's record and `BRIEFING.md` are never committed from a product
   or sandbox repository: they change through a session in the project-management
   repository, protected by the kit's deny rules and by review. The Project Advisor's
   sessions push only on his go-ahead.

Never write "open questions" inside another document: link to the record instead.

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))
