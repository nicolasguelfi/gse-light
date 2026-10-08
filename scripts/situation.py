#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2026 right-on-skill (https://rightonskill.odoo.com/) - gse-light by Nicolas Guelfi (https://github.com/nicolasguelfi/gse-light)
# SPDX-License-Identifier: LicenseRef-PolyForm-Noncommercial-1.0.0  (non-commercial; see LICENSE.md)
"""Where are we in the Project Advisor's week, and what is the next step? (single entry point)

Read-only. Printed by the session-start hook and read as JSON by the `advisor` skill:

  python3 ../gse-light/scripts/situation.py            # short text block
  python3 ../gse-light/scripts/situation.py --json     # machine-readable
  python3 ../gse-light/scripts/situation.py --today 2026-10-14   # simulate a date (tests)

The week is a chain per meeting folder meetings/<date>/:
  agenda.md  →  audio* / transcript-imported.*  →  transcript.md  →  minutes.md  →  "validated by <who> on <date>"
(the last link is the validation line of templates/meeting-minutes.md: "validated by … on YYYY-MM-DD").
The meeting day is variable, fixed at each meeting for the next one (Project Advisor's rule,
2026-10-07). The next date is read, in this order: instances/<instance>/meetings/schedule.json
{"next": "YYYY-MM-DD"} (written by the minutes step or by the Project Advisor), the "Next meeting"
section of the latest minutes.md, the earliest future meeting folder, or a fixed
{"weekday": "..."} in schedule.json if ever set. A past date in schedule.json is reported, not used.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from llm_call import PM, instance_dir, load_env  # noqa: E402  (same .env convention as the other scripts)

_mdir = os.environ.get("MEETINGS_DIR") or load_env().get("MEETINGS_DIR")
MEET = (Path(_mdir) if Path(_mdir).is_absolute() else PM / _mdir) if _mdir else instance_dir() / "meetings"
SCHEDULE = MEET / "schedule.json"
WEEKDAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def folders() -> list[Path]:
    if not MEET.exists():
        return []
    return sorted(p for p in MEET.iterdir() if p.is_dir() and DATE.match(p.name))


def chain(d: Path) -> dict:
    """What exists in one meeting folder."""
    def has(pattern: str) -> bool:
        return any(d.glob(pattern))
    minutes = d / "minutes.md"
    validated = minutes.exists() and bool(
        re.search(r"validated by [^\n]{1,60}? on \d{4}-\d{2}-\d{2}", minutes.read_text(encoding="utf-8")))
    imported = has("transcript-imported.*")
    return {
        "agenda": (d / "agenda.md").exists(),
        "recording": (d / ".record.pid").exists(),
        "audio": has("audio*.*"),
        "transcript": (d / "transcript.md").exists() or imported,
        "minutes": minutes.exists(),
        "validated": validated,
    }


def schedule() -> dict:
    """schedule.json as a dict; an absent, malformed or non-object file ([], a string) counts as empty."""
    if SCHEDULE.exists():
        try:
            data = json.loads(SCHEDULE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return {}
        return data if isinstance(data, dict) else {}
    return {}


def date_in(text: str) -> dt.date | None:
    m = re.search(r"(\d{4}-\d{2}-\d{2})", text or "")
    return dt.date.fromisoformat(m.group(1)) if m else None


def next_from_minutes(today: dt.date) -> dt.date | None:
    """The 'Next meeting' section of the latest minutes, if it names a future date."""
    for d in reversed(folders()):
        m = d / "minutes.md"
        if not m.exists():
            continue
        text = m.read_text(encoding="utf-8")
        part = text.split("## Next meeting", 1)
        when = date_in(part[1][:200]) if len(part) == 2 else None
        return when if when and when >= today else None
    return None


def next_meeting(today: dt.date) -> tuple[dt.date | None, str]:
    """(next meeting date or None, where it came from: schedule.json | minutes | folder | weekday | none)."""
    sched = schedule()
    nxt = date_in(str(sched.get("next", "")))
    if nxt and nxt >= today:
        return nxt, "schedule.json"
    nxt = next_from_minutes(today)
    if nxt:
        return nxt, "minutes"
    future = [dt.date.fromisoformat(p.name) for p in folders() if dt.date.fromisoformat(p.name) >= today]
    if future:
        return min(future), "folder"
    wd = str(sched.get("weekday", "")).lower()
    if wd in WEEKDAYS:
        delta = (WEEKDAYS.index(wd) - today.weekday()) % 7
        return today + dt.timedelta(days=delta), "weekday"  # today counts when it is the day
    return None, "none"


def unfinished_step(d: Path, c: dict, past: bool = False) -> tuple[str, str] | None:
    """The first missing link of a meeting that already happened (`past`: the day is over)."""
    if c["recording"]:
        return "stop", f"A recording is still running in {d.name}: stop it (`scripts/meeting/meeting.sh stop`)."
    if c["audio"] and not c["transcript"]:
        return "transcribe", f"{d.name}: audio recorded, no transcript yet → meeting transcribe."
    if c["transcript"] and not c["minutes"]:
        return "minutes", f"{d.name}: transcript ready, no minutes yet → meeting minutes."
    if c["minutes"] and not c["validated"]:
        return "validate", (f"{d.name}: minutes drafted, not validated by the Project Advisor → present them "
                            "(a short multiple-choice question, QCM).")
    if past and c["agenda"] and not c["audio"] and not c["transcript"] and not c["minutes"]:
        return "import", (f"{d.name}: agenda only, no recording or transcript → `scripts/meeting/meeting.sh import <file> {d.name}` "
                          "(the recording or transcript made elsewhere), or write minutes.md from the notes.")
    return None


def situation(today: dt.date) -> dict:
    steps: list[dict] = []
    notes: list[str] = []

    if not (PM / ".env").exists():
        notes.append("No .env yet: copy .env.example to .env and fill the keys. Local steps still work.")

    # 1. finish what a past meeting left open
    for d in folders():
        day = dt.date.fromisoformat(d.name)
        if day < today:
            s = unfinished_step(d, chain(d), past=True)
            if s:
                steps.append({"kind": s[0], "meeting": d.name, "text": s[1]})

    # 2. the next meeting
    nxt, source = next_meeting(today)
    if nxt is None:
        steps.append({"kind": "schedule", "meeting": None,
                      "text": "No next meeting date known: ask the Project Advisor the date (it is fixed at each meeting for the next one) and write instances/<instance>/meetings/schedule.json {\"next\": \"YYYY-MM-DD\"}."})
    else:
        d = MEET / nxt.isoformat()
        c = chain(d) if d.exists() else {k: False for k in ("agenda", "recording", "audio", "transcript", "minutes", "validated")}
        days = (nxt - today).days
        if days > 0:
            if not c["agenda"]:
                steps.append({"kind": "brief", "meeting": nxt.isoformat(),
                              "text": f"Meeting {nxt} ({WEEKDAYS[nxt.weekday()]}, in {days} day{'s' if days > 1 else ''}): no agenda yet → meeting brief {nxt}."})
            else:
                steps.append({"kind": "read", "meeting": nxt.isoformat(),
                              "text": f"Meeting {nxt} in {days} day{'s' if days > 1 else ''}: agenda ready — the Project Advisor reads it; refresh only if new facts appeared."})
        else:  # today
            s = unfinished_step(d, c) if d.exists() else None
            if c["recording"]:
                steps.append({"kind": "recording", "meeting": nxt.isoformat(), "text": "Meeting day: recording in progress — stop it when the meeting ends."})
            elif not c["audio"] and not c["transcript"]:
                steps.append({"kind": "record", "meeting": nxt.isoformat(),
                              "text": "Meeting day: start the recording before the meeting (in person) or import the recording made elsewhere after (meeting.sh import)."
                                      + ("" if c["agenda"] else " No agenda: brief first if there is time.")})
            elif s:
                steps.append({"kind": s[0], "meeting": nxt.isoformat(), "text": s[1]})
            else:
                steps.append({"kind": "done", "meeting": nxt.isoformat(), "text": f"Meeting {nxt}: chain complete (minutes validated)."})

    if not steps or all(st["kind"] in ("done", "read") for st in steps):
        steps.append({"kind": "free", "meeting": None,
                      "text": "Nothing pending in the meeting chain: BRIEFING §1 tasks, improvements from this session, or close."})

    return {"today": today.isoformat(), "next_meeting": nxt.isoformat() if nxt else None,
            "next_meeting_source": source, "schedule": schedule(), "steps": steps, "notes": notes,
            "folders": [p.name for p in folders()]}


ORIGIN = {"schedule.json": "from schedule.json", "minutes": "from the latest minutes",
          "folder": "from the earliest future meeting folder", "weekday": "from the weekday in schedule.json"}


def text(s: dict) -> str:
    source = s.get("next_meeting_source", "none")
    origin = f" ({ORIGIN[source]})" if source in ORIGIN else ""
    sched_next = str(s["schedule"].get("next", "")) if isinstance(s.get("schedule"), dict) else ""
    if source != "schedule.json" and sched_next:  # a date is written there but already past: say so, do not use it
        origin += f" (schedule.json: {sched_next} is past)"
    out = [f"Situation ({s['today']}): next meeting {s['next_meeting'] or 'unknown'}{origin}."]
    for n in s["notes"]:
        out.append(f"  note: {n}")
    out.append(f"  Next step: {s['steps'][0]['text']}")
    for st in s["steps"][1:]:
        out.append(f"  Then: {st['text']}")
    out.append('  Say "go" (or anything) and the session does it; /advisor re-assesses on demand.')
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--today", type=dt.date.fromisoformat, default=dt.date.today())
    a = ap.parse_args()
    s = situation(a.today)
    print(json.dumps(s, indent=2, ensure_ascii=False) if a.json else text(s))
    return 0


if __name__ == "__main__":
    sys.exit(main())
