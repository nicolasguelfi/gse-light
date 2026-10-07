---
name: advisor
description: The single entry point of NG's sessions on this repository (method and active instance) - work out where we are in the Project Advisor's week (../gse-light/scripts/situation.py), do the next step yourself by orchestrating the `meeting` skill, the agents `delivery-auditor` and `minutes-verifier`, `decision-record`, `method-lesson` and `session-close`, and ask NG only what only he knows. Use on NG's first message of a session whatever it says ("go", "bonjour", a question), and whenever he asks "where are we" or "what now"; /advisor re-assesses on demand.
---

# advisor — NG launches Claude, the session does the rest

NG is the Project Advisor: two hours of meeting, two hours of preparation a week, no command to
remember. The hook has already printed the **situation** (today, next meeting, next
step). This skill turns it into action.

## 0. Read the situation

`python3 ../gse-light/scripts/situation.py --json` → `steps[0]` is the next step, the rest follow.
If NG's message is a different request, serve it first, then come back here.

## 1. Do the step — who does what

| `kind` | You do | You ask NG (only this) |
|---|---|---|
| `schedule` | — | the date of the next meeting — the day is variable, fixed at each meeting for the next one (one short question); write `instances/<instance>/meetings/schedule.json` `{"next": "YYYY-MM-DD", "time": "..."}` |
| `brief` | `meeting` step 1: create the folder, run `delivery-auditor`, read the previous minutes, write `agenda.md` from the template, summarise in five lines; a kick-off or hand-over meeting follows `meeting` §1b instead | participants if unknown; which of the auditor's points he wants to raise (one QCM, at most four options) |
| `read` | show the agenda's "Points the Project Advisor intends to raise" and "Material to look at"; refresh the facts only if something changed (`gh`, journal) | nothing, unless he wants to add a point |
| `record` | ask the one question, then: in person → `../gse-light/scripts/meeting/meeting.sh start <date>`; Teams → wait for the file, then `meeting.sh import` | in person / Teams / no recording today |
| `recording` | `../gse-light/scripts/meeting/meeting.sh status`; at his word, `stop` | "the meeting is over?" only if he says nothing |
| `stop` | `../gse-light/scripts/meeting/meeting.sh stop`, then continue with `transcribe` | — |
| `transcribe` | `python3 ../gse-light/scripts/meeting/transcribe.py instances/<instance>/meetings/<date>` with the engine from `.env`; if no local engine, give him the install line and offer Gemini with its estimated cost | engine, only when the default is unavailable or he asked for speaker labels |
| `minutes` | `meeting` step 4: draft `minutes.md` from the template, record decisions with `decision-record`, run `minutes-verifier`, fix what it flags; write the next meeting's date (fixed in the meeting) in "Next meeting" and in `instances/<instance>/meetings/schedule.json` | participants' names if the transcript has no labels and the agenda does not say; the next meeting's date if the transcript does not give it |
| `validate` | present the minutes: summary, tasks per participant, Project Advisor's feedback | one QCM: send as is · change (he says what) · hold. On "send as is", write "validated by NG on <date>" in the header; he distributes, or asks you to |
| `done` / `free` | show `instances/<instance>/BRIEFING.md` §1 (his tasks) and anything the session could improve (standing rule) | one QCM: which task, an improvement, or close |

Rules while doing a step: measure before asserting (every fact with its command or
timestamp); no paid call without saying the estimate first; never start a recording
NG did not ask for; never distribute minutes yourself; one QCM at a time, short.

## 2. After the step

Re-run `../gse-light/scripts/situation.py`. If another step is due today, say so in one line and do
it on his word. Otherwise one QCM: *continue with <next step>* · *something else* ·
*close the session*. On "close": `session-close` (journal entry, metrics row, cockpit;
commit; push only if he says "pousse").

## 3. Improve as you go

Every gap met during a step (a missing field in a template, an auditor criterion that
does not fit, a question NG had to answer twice) follows the standing rule: name it, do
the task, propose the smallest fix, and on his yes apply it with `method-lesson` in the
same session.
