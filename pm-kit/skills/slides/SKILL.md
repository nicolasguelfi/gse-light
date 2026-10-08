---
name: slides
description: Make, reopen, update or export a presentation of the active instance as a claude.ai Slides artifact - kick-off, weekly meeting, hand-over or any talk the Project Advisor gives. Dark template, numbered slides, actor marks; sources kept in instances/<instance>/meetings/<date>/slides/project/; the published version is synced back into the repository before any change, so the Project Advisor's edits in the viewer are never lost; a registry of links in instances/<instance>/meetings/README.md. Use whenever the Project Advisor wants slides for a session, or to reopen or change those of any week.
---

# slides — one deck per session, its source in git, never out of sync

Nicolas Guelfi (NG), the Project Advisor, prepares his sessions with Slides artifacts on
claude.ai (NG, 2026-10-07). A deck
lives in two places: **published** on claude.ai (what NG sees, presents, edits in the
viewer, shares and exports) and **in git** (`instances/<instance>/meetings/<date>/slides/project/`, so any
later session can reopen it). The published version wins: NG may have edited it in the
viewer.

## 0. Find the deck

`instances/<instance>/meetings/README.md` → "Presentations": one row per deck — date, title, link, folder.
No row: it is a new deck (§1). A row: reopen it (§2).

## 1. New deck

1. Source of content: the meeting's `agenda.md` (weekly brief), the previous
   `minutes.md`, or [`../gse-light/method/15-project-advisor.md`](https://github.com/nicolasguelfi/gse-light/blob/main/method/15-project-advisor.md)
   for a milestone meeting (`meeting` §1b). Ask NG at most one short multiple-choice
   question (QCM: audience, length).
2. `cp -R ../gse-light/templates/slides instances/<instance>/meetings/<date>/slides`; edit `project/deck.json` (title,
   `order`, sections) and one `project/slides/<id>.html` per slide, starting from the
   six models (cover, marks, table, cards, statement, next). Slide format: the Slides
   type's rules (one `<section>` per file, inline styles, 1920×1080, notes in `<aside>`).
3. Create the artifact: `Artifact` `action: "quickstart"`, `intent: "slides"` gives the
   Slides `type_url`; publish with that `type_url`, a `title` and
   `auto_open: "after_first_write"`. Then publish the files with
   `url: <new link>`, `root: instances/<instance>/meetings/<date>/slides`,
   `file_path: <root>/project/deck.json`, `files: {"project/slides/<id>.html": "project/slides/<id>.html", …}`.
4. Write `open.html` in `instances/<instance>/meetings/<date>/slides/` from
   `../gse-light/templates/artifact-open.html` (title and link; double-click opens the deck — NG,
   2026-10-07). Add the row to `instances/<instance>/meetings/README.md` "Presentations"; link the deck from the
   meeting's `agenda.md`.

## 2. Reopen or change a deck — sync first, always

1. **Sync**: `Artifact` `action: "read"`, the deck's `url`, `paths`: `project/deck.json`
   and every `project/slides/<id>.html` of its `order`, `out_dir` in the scratchpad.
   `diff -rq <out_dir>/project instances/<instance>/meetings/<date>/slides/project`. Any difference: copy the
   published files into the repository (NG's edits win) and commit "slides <date>: sync
   from the viewer".
2. Edit the repository files; publish **only the changed files** with the same `url` and
   `root` (send `deck.json` only when the order, title or sections change). **After adding,
   removing or reordering slides, renumber every footer** `n / N` (bottom right of each
   `project/slides/<id>.html`) to match the new `order`, and publish every slide whose
   number changed — a deck with two slides "7 / 21" is a defect.
3. A publish refused because the deck changed meanwhile: read the files it names, merge
   onto them, publish again. Never resend a copy you have not merged, never `force`
   (2026-10-07: one of NG's slides was overwritten once).
4. After the publish, the repository and the published deck are identical; say so with
   the `diff` that shows it.

## 3. After the meeting

Sync once more (§2.1) so the presented version is in git. NG exports the PDF (Share ›
Export › PDF) if it is to be distributed; commit it in `instances/<instance>/meetings/<date>/slides/`.

## Design rules (NG, 2026-10-07)

- Dark palette of the template: backgrounds `#08111F` (cover), `#0F1A2E`, `#16233B`;
  cards `#1D2C47`, border `#2E3F5E`; text `#EEF1F5`, body `#C3CCD9`, footer `#95A3B8`;
  accent `#F0A35E`; statement slide `#A8521A`. Fonts: Source Serif 4 (titles), IBM Plex
  Sans (text).
- Every slide numbered **n / N** bottom right (the viewer does not follow NG's screen);
  the source of its facts bottom left.
- A mark on every action: **Person** (`#EEF1F5`), **Ask Claude** (`#F0A35E`),
  **Automatic** (`#6FD3CC`; Claude by the kit's rules, or the CI).
- A meeting NG does not run alone is written as a proposal (times "around", open lists,
  "with the Project Advisor's recommendations"); examples and data before
  specifications; one idea per slide; speaker notes on every slide; nothing invented —
  unknowns in `[brackets]`.
- Review with NG by review board (one comment per slide or group, one global comment);
  a second version for comparison is a new artifact and a new registry row.

- `slides/` always holds the deck **in force**. A version replaced by a new artifact moves
  to `slides-v<n>/` (n = its version number) with its own `open.html`, and its registry row
  says "superseded" (NG, 2026-10-07).

## Never

Publish a deck that was not synced first; delete a deck or a slide NG did not ask to
remove; share a deck (only NG shares, from the Share menu — the link is private until
then).

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))
