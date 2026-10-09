<!-- Template of the gse-light method (https://github.com/nicolasguelfi/gse-light), CC BY-NC 4.0. Documents made from this template carry no licence obligation: fill it in and keep the result as your own. -->
<!-- One record per requirement. FR-<AREA>-NNN: a functional requirement (what the product does), in
     project/requirements/20-functional/ (one file per capability, several records in it).
     NFR-<AREA>-NNN: a quality (speed, availability, security, usability…), in requirements/30-non-functional.md.
     <AREA>: the short code of the product area (two to four capital letters, the same codes as the examples).
     NNN: three digits, in order of creation; an id is never reused. Keep the heading format: the traceability
     table and the test names cite the id. Every <…> is a placeholder to replace; delete this comment block. -->
## FR-<AREA>-NNN — <the requirement in one sentence: who can do what, with what result>

🔴 **Draft** <!-- 🟡 Agreed (product owner, YYYY-MM-DD) · 🟢 Verified (test passing, YYYY-MM-DD) · ⚪ Dropped (DEC-NNN) -->

**Statement.** <One or two sentences in plain words: in <situation>, the product <does what> so that <who> <gets what>. For an NFR: the measurable target (for example "the page shows within 2 s for 50 users at once").>

**Rests on.** `EX-<AREA>-NNN` <linked to its file, `../40-examples/EX-<AREA>-NNN-<short-name>.md` — the real example that motivates it; principle 1: no requirement without one; a second example if it adds a case>

**Acceptance criteria.** <Each criterion is checkable by a test, or by the product owner looking at the product. Write them as: given <situation>, when <action>, then <observable result>.>

1. <Given …, when …, then ….>
2. <…>

**Data regime.** <aggregate · pseudonymised · identified — the level this requirement needs (reference design ch. 11); a new flow of personal data needs the data protection contact's go-ahead>

**Decisions.** <the `DEC-NNN` records that shaped it, or "none">

**Proved by.** <the test or tests whose name cites this id (for example `test_FR_<AREA>_NNN_<what>`), with the level: unit · integration · end-to-end through the real user interface, run by Claude. "none yet" until it exists: the weekly map of what is verified lists the requirement as unverified until then.>
