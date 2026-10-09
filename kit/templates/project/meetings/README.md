# Meetings

One folder per meeting with the Project Advisor, `YYYY-MM-DD/`, produced by the `meeting`
skill — a procedure Claude runs when asked (`/meeting`) or when the situation calls for it —
in the Project Advisor's sessions. **Who writes here**: his sessions only. **Who reads**:
everyone — the team takes its tasks for the next sprint from the minutes, the product owner
reads the minutes on GitHub.

| File | Written by | In git |
|---|---|---|
| `agenda.md` | `meeting brief`, the day before | yes |
| `audio.m4a` (or imported audio) | `meeting record` / `meeting import` | **no** (git-ignored; stays in the Advisor's private storage, outside git) |
| `meta.json`, `imports.jsonl` | the recording script | yes |
| `transcript.md` (+ `.srt`, `.json`) | `meeting transcribe` | yes |
| `minutes.md` | `meeting minutes` (the Advisor's session: draft and his feedback section), verified by `minutes-verifier`, **validated and sent by the project lead** with his own session (roles record §2) | yes |
| `cost.json` | `../gse-light/scripts/llm_call.py` when a paid model was used | yes |

Minutes carry the tasks each participant took for the next sprint, each with the
transcript timestamp where it was said. The project lead's sprint file
(`planning/sprints/`) takes them from here.

A meeting's **chain** is this sequence of files — agenda → recording → transcript → minutes
→ validation — one link after the other. `../gse-light/scripts/situation.py` (the script the
start hook runs to say where the week stands) reads which links exist and announces the next
step. It finds the next meeting date in `schedule.json` (`{"next": "YYYY-MM-DD"}`, written by
the minutes step), else in the "Next meeting" section of the latest minutes, else as the
earliest future folder; otherwise the session asks the Project Advisor. The meeting day is
variable, fixed at each meeting for the next one. A chain is complete when `minutes.md`
carries "validated by <the project lead's name> on YYYY-MM-DD" — this shape, with any
name and the date, is what `situation.py` reads.

## Presentations and review boards

Artifacts on claude.ai published for this project (private links until the Project
Advisor shares them). Each has a folder with its sources and an **`open.html`**:
double-click it in the file explorer to open the artifact. In a meeting folder, `slides/`
is the deck in force and `slides-v<n>/` a replaced version. Decks are made and kept in
sync by the [`slides`](https://github.com/nicolasguelfi/gse-light/blob/main/kit/skills/slides/SKILL.md) skill.

| Date | Artifact | Link | Folder |
|---|---|---|---|

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))
