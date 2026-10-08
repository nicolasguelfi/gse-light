---
name: session-close
description: Close a working session (method or active instance) - write the dated journal entry and the metrics row, refresh the cockpit, and leave a hand-over a session with no memory can resume from. Use when the user says the session ends, before a context handover, or after a significant unit of work.
---

# Close a session

The journal lives in the project-management repository, `instances/<instance>/journal/`.
From a product repository, or from a personal sandbox repository while the product
repositories do not exist yet, that is the sibling folder named in the repository's
`CLAUDE.md` (`../<pm-repo>`): a sandbox holds no journal and no register of its own. Paths
below are relative to the project-management repository; the method is `../gse-light`.

## Steps

1. **Number the session**: one counter per person. The Project Advisor's entries are
   `YYYY-MM-DD-sNN.md`; every other author's are `YYYY-MM-DD-<initials>-sNN.md` (two or
   three lowercase letters), `sNN` being the next number after that author's highest
   existing entry — so two people closing on the same day never collide.
2. **Write the entry** at that path from `../gse-light/templates/session-journal.md`:
   - each action with the command that **measured** its result (not "deployed", but
     "deployed — `curl …/version` → 1.4.2");
   - decisions created, decided or amended, by identifier;
   - what was not done, and why;
   - a hand-over for a reader with no memory: state, rules learned, traps.
3. **Append one row to `instances/<instance>/journal/metrics.csv`** (columns in `instances/<instance>/journal/README.md`).
4. **Who closes?** Only the Project Advisor's sessions, opened in the project-management
   repository, edit `instances/<instance>/BRIEFING.md` (roles record). A session of the
   project lead or of a developer — from a product repository or a sandbox — **never
   touches it** (the kit's settings deny it there): it reports what §1 or §1b should say
   in its journal entry, under "For the next session", and stops here for the cockpit.
   The Project Advisor's session **refreshes `instances/<instance>/BRIEFING.md`** with the
   `cockpit-update` skill if it is available, otherwise by hand: §1 what awaits the
   Project Advisor, §1b what awaits the team, §2 the delta since the last acknowledgement
   as dated bullets (the session writes its own date on each bullet it adds), §3 the
   counted state. "Last acknowledgement" is re-stamped **only when the Project Advisor has
   read and acknowledged** the cockpit; otherwise its date stays and §2 keeps accumulating.
5. **Never edit an earlier journal entry.** A correction is a new entry citing it.
6. **Go-ahead first.** A push is a state-changing action: the Project Advisor's sessions
   commit, then ask, and push only on his explicit go-ahead; a developer or the project
   lead pushes their own entry on their own word (they have write access for their journal
   entries and new 🔴 records), and the kit's settings make Claude ask before any `git push`
   in a product repository — answer for your own paths only. Then, from the
   project-management repository: `python3 ../gse-light/scripts/check_docs.py`; from a
   product or sandbox repository: `python3 ../gse-light/scripts/check_docs.py ../<pm-repo>`
   (the argument names the repository to check). **Commit and push only those paths**:
   `git -C ../<pm-repo> add instances/<instance>/journal/YYYY-MM-DD-sNN.md instances/<instance>/journal/metrics.csv`
   (plus a new 🔴 record opened in the session), `git -C ../<pm-repo> commit -m "journal sNN"`,
   `git -C ../<pm-repo> push` (inside the project-management repository, drop `-C ../<pm-repo>`).
   If the push is refused because the branch moved, pull, re-read what changed, merge,
   push again — never force.

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))
