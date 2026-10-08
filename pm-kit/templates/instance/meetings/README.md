# Meetings

One folder per meeting with the Project Advisor, `YYYY-MM-DD/`, produced by the `meeting`
skill:

| File | Written by | In git |
|---|---|---|
| `agenda.md` | `meeting brief`, the day before | yes |
| `audio.m4a` (or imported audio) | `meeting record` / `meeting import` | **no** (git-ignored; stays in the Advisor's private storage, outside git) |
| `meta.json`, `imports.jsonl` | the recording script | yes |
| `transcript.md` (+ `.srt`, `.json`) | `meeting transcribe` | yes |
| `minutes.md` | `meeting minutes`, verified by `minutes-verifier`, validated by the Project Advisor | yes |
| `cost.json` | `../gse-light/scripts/llm_call.py` when a paid model was used | yes |

Minutes carry the tasks each participant took for the next sprint, each with the
transcript timestamp where it was said. The project lead's sprint file
(`planning/sprints/`) takes them from here.

The meeting day is variable, fixed at each meeting for the next one. `../gse-light/scripts/situation.py`
finds the next date in `schedule.json` (`{"next": "YYYY-MM-DD"}`, written by the minutes
step), else in the "Next meeting" section of the latest minutes, else as the earliest
future folder; otherwise the session asks the Project Advisor. A meeting's chain is
complete when `minutes.md` carries "validated by NG on <date>" — this exact wording,
which `situation.py` reads (NG: the method's author, the Project Advisor).

## Presentations and review boards

Artifacts on claude.ai published for this instance (private links until the Project
Advisor shares them). Each has a folder with its sources and an **`open.html`**:
double-click it in the file explorer to open the artifact. In a meeting folder, `slides/`
is the deck in force and `slides-v<n>/` a replaced version. Decks are made and kept in
sync by the [`slides`](https://github.com/nicolasguelfi/gse-light/blob/main/pm-kit/skills/slides/SKILL.md) skill.

| Date | Artifact | Link | Folder |
|---|---|---|---|

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))
