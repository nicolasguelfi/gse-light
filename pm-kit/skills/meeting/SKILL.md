---
name: meeting
description: The Project Advisor's weekly meeting chain for the active instance - `brief` the day before (facts from delivery-auditor, decisions awaiting, timed agenda), `record` / `import` on the day, `transcribe` (local by default, Gemini on request), `minutes` (executive summary, decisions to the registers, tasks per participant cited from the transcript, Project Advisor's feedback) checked by minutes-verifier. One folder per meeting under instances/<instance>/meetings/<date>/. Use for anything about preparing, recording, transcribing or writing up the weekly meeting.
---

# meeting — one skill, five steps, one folder

Nicolas Guelfi (NG) is the **Project Advisor**: he gives feedback and advice; the project
lead runs the project. This skill serves his two-hour meeting with the team (the rhythm
and the day are fixed with the team: the project lead dates the weeks) and must fit in his
two hours of preparation. Everything lands in `instances/<instance>/meetings/<YYYY-MM-DD>/`
(layout in `instances/<instance>/meetings/README.md`). Recordings stay in the Advisor's
private storage, outside git (audio is git-ignored); consent is his own process — do not
raise it.

| Step | When | Produces |
|---|---|---|
| `meeting brief [date]` | the day before | `agenda.md` (milestone meeting: §1b) |
| `meeting record start\|stop\|status` · `meeting import <file>` | on the day | `audio.m4a`, `meta.json` |
| `meeting transcribe [--engine local\|gemini]` | after the meeting | `transcript.md` (+ `.srt`, `.json` locally) |
| `meeting minutes` | the same evening | `minutes.md`, checked by `minutes-verifier` |

Scripts: `../gse-light/scripts/meeting/meeting.sh`, `../gse-light/scripts/meeting/transcribe.py`,
`../gse-light/scripts/llm_call.py` (paid calls, cost logged). Settings in `.env` (see `.env.example`;
never read `.env` yourself — the scripts do).

## 1. `brief` — the day before

1. **Date.** Next meeting date from NG (ask in one short multiple-choice question, QCM,
   if unknown); create `instances/<instance>/meetings/<date>/`.
2. **Facts.** Run the `delivery-auditor` agent (read-only). It measures what the team
   delivered since the last meeting — sprint file in `instances/<instance>/planning/sprints/`, GitHub
   milestone, pull requests, gates, journal entries, registers — and returns facts with
   their commands. Before the product repositories exist it works from the registers,
   the roadmap and the previous minutes, and says so.
3. **Threads.** Read the previous `minutes.md`: tasks per participant (which are done,
   measured when possible), open questions, decisions promised.
4. **Decisions awaiting.** The 🔴 and 🟡 rows of the three registers whose decider is in
   the room, and `instances/<instance>/BRIEFING.md` §1b.
5. **Write `agenda.md`** from `../gse-light/templates/meeting-agenda.md`: a two-hour timed agenda
   (facts first, then the team's demo or deliverables, then the Project Advisor's feedback, then
   decisions, then next sprint — which the project lead presents, not NG), the
   auditor's facts, the follow-up table, the points NG wants to raise (ask him once,
   QCM, if the auditor found something he must choose to raise or not).
6. Tell NG in five lines what the brief says and what he should look at before the
   meeting. Do not refresh the cockpit for this (session-close does).

## 1b. `brief` for a milestone meeting — kick-off, Wn hand-over

Not every meeting is a sprint meeting (2026-10-07, a kick-off once done by hand).
For a milestone meeting — the kick-off, the hand-over of the last week Wn — there is
nothing to audit: skip `delivery-auditor`.

1. One QCM with three questions: audience (the client, the team, both), support (document +
   slides, slides only, document only), scope (the whole project, or this meeting only) —
   each with its advantages, drawbacks and consequences.
2. Write `agenda.md` (participants, timed agenda, decisions awaiting someone in the
   room, points the Project Advisor intends to raise, material) from
   [`../gse-light/method/15-project-advisor.md`](https://github.com/nicolasguelfi/gse-light/blob/main/method/15-project-advisor.md), which is the
   source of the support; update that document rather than writing a second one.
3. Slides, when asked: the [`slides`](../slides/SKILL.md) skill (template, sync,
   registry); link the deck from the document.
4. Offer NG a review board (one line per point, a comment per point, a global comment).
5. Design rules and the sync before any republish: [`slides`](../slides/SKILL.md)
   (NG, 2026-10-07).

## 2. `record` / `import` — on the day

- In person: `../gse-light/scripts/meeting/meeting.sh start [date] [device]`; check with `status`;
  end with `stop`. First time on a machine: `meeting.sh devices` to pick the microphone
  index and put it in `.env` (`MEETING_AUDIO_DEVICE`). The recording runs detached: a
  closed Claude session does not stop it; `stop` from any session on the same machine.
- Teams / another recorder: NG exports the file; `../gse-light/scripts/meeting/meeting.sh import
  <file> [date]` copies it into the folder (audio, or a `.vtt`/`.docx` transcript, which
  then replaces step 3).
- Never delete or move an audio file. Never start a recording without NG asking.

## 3. `transcribe`

- `python3 ../gse-light/scripts/meeting/transcribe.py instances/<instance>/meetings/<date>` — engine from `.env`
  (`TRANSCRIBE_ENGINE`, default `local`). Local = mlx-whisper or whisper.cpp, nothing
  leaves the machine, no speaker labels; if no engine is installed the script prints the
  one-line install command — pass it to NG, do not install it yourself.
- `--engine gemini` when speaker labels matter: the audio is uploaded to Google AI
  Studio with NG's key; the cost line is written to `instances/<instance>/journal/llm-costs.csv` and
  `instances/<instance>/meetings/<date>/cost.json`. Say the estimated cost before running it.
- Output `transcript.md`: `[hh:mm:ss]` per line. Keep it; `minutes-verifier` needs it.

## 4. `minutes` — the same evening

1. **Inputs.** `transcript.md` (or the imported transcript), `agenda.md`, the list of
   participants (in `agenda.md`; ask NG once if missing), the sprint file.
2. **Write `minutes.md`** from `../gse-light/templates/meeting-minutes.md`:
   - *Executive summary*: ten lines at most, what was shown, what was decided, what is at
     risk;
   - *Decisions*: each one recorded with the `decision-record` skill (new 🔴 or 🟢 by the
     person who holds the right — the Project Advisor's advice is not a decision); the minutes
     link to the record;
   - *Tasks for the next sprint, per participant*: who · what · by when · ticket or link
     · `[hh:mm:ss]` of the transcript where it was said. A task without a timestamp
     does not go in. Tasks NG took himself are listed too;
   - *Project Advisor's feedback*: project conduct (does the week show an iterative, incremental
     cycle? were the gates and go-aheads respected?) and deliverables (what is good, what
     to change, one priority) — written in NG's name, from what he said in the meeting
     and the auditor's facts; nothing he did not say or ask for;
   - *Open questions*, *next meeting*: the date fixed in the meeting (the day is
     variable, decided each time for the next one) — written here **and** in
     `instances/<instance>/meetings/schedule.json` as `{"next": "YYYY-MM-DD"}`, which is what
     `../gse-light/scripts/situation.py` reads to announce the next brief.
3. **Verify.** Run the `minutes-verifier` agent: every task and decision must be backed
   by a transcript excerpt. Fix or remove what it flags; never argue with it in the
   minutes.
4. **The Advisor's feedback section** — one QCM to the Project Advisor: as is · change (he says
   what). Then commit and push the draft `minutes.md` (without a validation line) and tell him
   the project lead is up.
5. **Validation and sending — the project lead, with Claude** (NG, 2026-10-09; roles record §2).
   From his own repository, his session reads `../<pm-repo>/instances/<instance>/meetings/<date>/minutes.md`,
   he corrects what he must, and his session writes "validated by <the project lead's name> on
   YYYY-MM-DD" in the header, commits and pushes that one file; he sends the minutes to the
   participants himself. The Advisor's session never distributes them.
   <!-- keep this exact shape: situation.py reads "validated by … on YYYY-MM-DD", with any name -->
6. The tasks feed the project lead's next sprint file.

## Rules

- Light: a brief in under 60 minutes of NG's time, minutes in under 45. If a step takes
  longer, say so and propose what to drop.
- Measure before asserting: every fact in `agenda.md` and `minutes.md` carries its
  command or its transcript timestamp.
- Costs: any Gemini or OpenRouter call goes through `../gse-light/scripts/llm_call.py`; say the
  estimate first (rule of thumb for audio sent to Gemini: about 32 tokens per second of
  recording — a two-hour meeting is roughly 230,000 input tokens, priced at the model's
  input rate).
- At the end of the session: `session-close` (journal entry, cockpit).

---

© 2026 [right-on-skill](https://rightonskill.odoo.com/) · [`gse-light`](https://github.com/nicolasguelfi/gse-light) by Nicolas Guelfi · [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — non-commercial use, cite the author and the repository ([licence](https://github.com/nicolasguelfi/gse-light/blob/main/LICENSE.md))
