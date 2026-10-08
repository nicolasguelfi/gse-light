---
name: cockpit-update
description: Refresh instances/<instance>/BRIEFING.md, the Project Advisor's cockpit for the active instance - §1 what awaits him (his decisions, the team's requests for advice), §1b what awaits the team, §2 delta since his last acknowledgement, §3 state - from the registers and the latest journal entries. Use at the end of every session and whenever a decision changes status.
---

# Refresh the cockpit

`instances/<instance>/BRIEFING.md` is the Project Advisor's single entry point (Nicolas
Guelfi, NG, is the Project Advisor, not the project manager). A stale §1 is a defect; so
is a §1 that carries project-management tasks that belong to the project lead. Only his
sessions, opened in this repository, edit it (roles record).

1. **Collect** the 🔴 rows of the three dashboards (`instances/<instance>/governance/05-project-decisions.md`,
   `instances/<instance>/requirements/05-decisions.md`, `instances/<instance>/design/05-design-decisions.md`) with their "Who
   decides" column, and the "Not done" and "For the next session" parts of journal
   entries since the last acknowledgement date written at the top of `instances/<instance>/BRIEFING.md`.
2. **§1 — Awaiting you**: one row per action only the Project Advisor can take (his decisions:
   method, kit, his spending; approvals he owes; advice the team explicitly asked for),
   each with why and a link. Remove tasks that are done (check the register or the
   journal — do not assume). Keep task numbers stable (`T1`, `T2`…); a new task gets
   the next number. **§1b — Awaiting the team**: the 🔴 records whose decider is the
   project lead, the product owner or the data protection contact, with the Project Advisor's
   part ("advice", "chosen with you").
3. **§2 — What changed**: dated bullets of what happened since the last
   acknowledgement, newest first — the session stamps **its own date** (and session
   number) on each bullet it adds. Facts only, each traceable to a journal entry or a
   commit.
4. **§3 — State**: update the table; counts of 🔴 per register are **counted**, not
   copied from the previous version, on one line in this exact form, which
   `check_docs.py` reads: `🔴 PD n · 🟡 PD n · 🔴 DEC n · 🔴 DD n`.
5. **Re-stamp** "Last acknowledgement" **only when the Project Advisor has read and
   acknowledged** the cockpit (he says so in the session); otherwise leave the date and
   keep accumulating §2. Closing a session is not an acknowledgement.
6. Run `python3 ../gse-light/scripts/check_docs.py`.

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))
