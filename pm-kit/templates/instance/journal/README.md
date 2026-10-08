# Journal

One file per working **session** (one conversation with Claude Code, from opening it in a
folder to closing it), named `YYYY-MM-DD-sNN.md` for the Project Advisor's sessions and
`YYYY-MM-DD-<initials>-sNN.md` for every other author (one `sNN` counter per person, so two
sessions closed the same day never collide), written from
[`templates/session-journal.md`](https://github.com/nicolasguelfi/gse-light/blob/main/templates/session-journal.md),
and one row per session in [`metrics.csv`](metrics.csv).

**Entries are never rewritten.** A correction is a new entry that cites the old one.
The journal is the project's memory and research data on AI-assisted engineering.

Every session writes here, whoever runs it: the Project Advisor's sessions directly; the
team's sessions, from their **sandbox** (a personal, private, throwaway repository with the
kit, until the product repositories exist) or product repositories, through the **kit**'s
`session-close` **skill** — the kit: the files that make every Claude Code session in a
repository follow the method; a skill: a procedure Claude runs when asked
(`/session-close`) or when the situation calls for it. That skill commits and pushes the
entry and the metrics row only.

`metrics.csv` columns: `date, session, person, model, repository, duration_min,
commits, decisions_created, decisions_closed, notes`. `llm-costs.csv` is created by
`../gse-light/scripts/llm_call.py` at the first paid model call.

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))
