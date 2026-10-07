#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2026 right-on-skill (https://rightonskill.odoo.com/) - gse-light by Nicolas Guelfi (https://github.com/nicolasguelfi/gse-light)
# SPDX-License-Identifier: LicenseRef-PolyForm-Noncommercial-1.0.0  (non-commercial; see LICENSE.md)
"""Where are we in the Project Advisor's week, and what is the next step? (single entry point)

Read-only. Printed by the session-start hook and read as JSON by the `advisor` skill:

  python3 ../gse-light/scripts/situation.py            # short text block
  python3 ../gse-light/scripts/situation.py --json     # machine-readable
  python3 ../gse-light/scripts/situation.py --today 2026-10-14   # simulate a date (tests)

The week is a chain per meeting folder meetings/<date>/:
  agenda.md  →  audio* / transcript-imported.*  →  transcript.md  →  minutes.md  →  "validated by NG on <date>"
The meeting day is variable, fixed at each meeting for the next one (NG, 2026-10-07). The
next date is read, in this order: instances/<instance>/meetings/schedule.json {"next": "YYYY-MM-DD"} (written by
the minutes step or by NG), the "Next meeting" section of the latest minutes.md, the
earliest future meeting folder, or a fixed {"weekday": "..."} in schedule.json if ever set.
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
        re.search(r"validated by NG on \d{4}-\d{2}-\d{2}", minutes.read_text(encoding="utf-8")))
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
    if SCHEDULE.exists():
        try:
            return json.loads(SCHEDULE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
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


def next_meeting(today: dt.date) -> dt.date | None:
    sched = schedule()
    nxt = date_in(str(sched.get("next", "")))
    if nxt and nxt >= today:
        return nxt
    nxt = next_from_minutes(today)
    if nxt:
        return nxt
    future = [dt.date.fromisoformat(p.name) for p in folders() if dt.date.fromisoformat(p.name) >= today]
    if future:
        return min(future)
    wd = str(sched.get("weekday", "")).lower()
    if wd in WEEKDAYS:
        delta = (WEEKDAYS.index(wd) - today.weekday()) % 7
        return today + dt.timedelta(days=delta)  # today counts when it is the day
    return None


def unfinished_step(d: Path, c: dict) -> tuple[str, str] | None:
    """The first missing link of a meeting that already happened."""
    if c["recording"]:
        return "stop", f"A recording is still running in {d.name}: stop it (`scripts/meeting/meeting.sh stop`)."
    if c["audio"] and not c["transcript"]:
        return "transcribe", f"{d.name}: audio recorded, no transcript yet → meeting transcribe."
    if c["transcript"] and not c["minutes"]:
        return "minutes", f"{d.name}: transcript ready, no minutes yet → meeting minutes."
    if c["minutes"] and not c["validated"]:
        return "validate", f"{d.name}: minutes drafted, not validated by NG → present them (QCM)."
    return None


def situation(today: dt.date) -> dict:
    steps: list[dict] = []
    notes: list[str] = []

    if not (PM / ".env").exists():
        notes.append("No .env yet: copy .env.example to .env and fill the keys (T8). Local steps still work.")

    # 1. finish what a past meeting left open
    for d in folders():
        day = dt.date.fromisoformat(d.name)
        if day < today:
            s = unfinished_step(d, chain(d))
            if s:
                steps.append({"kind": s[0], "meeting": d.name, "text": s[1]})

    # 2. the next meeting
    nxt = next_meeting(today)
    if nxt is None:
        steps.append({"kind": "schedule", "meeting": None,
                      "text": "No next meeting date known: ask NG the date (it is fixed at each meeting for the next one) and write instances/<instance>/meetings/schedule.json {\"next\": \"YYYY-MM-DD\"}."})
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
                              "text": f"Meeting {nxt} in {days} day{'s' if days > 1 else ''}: agenda ready — NG reads it; refresh only if new facts appeared."})
        else:  # today
            s = unfinished_step(d, c) if d.exists() else None
            if c["recording"]:
                steps.append({"kind": "recording", "meeting": nxt.isoformat(), "text": "Meeting day: recording in progress — stop it when the meeting ends."})
            elif not c["audio"] and not c["transcript"]:
                steps.append({"kind": "record", "meeting": nxt.isoformat(),
                              "text": "Meeting day: start the recording before the meeting (in person) or import the Teams file after."
                                      + ("" if c["agenda"] else " No agenda: brief first if there is time.")})
            elif s:
                steps.append({"kind": s[0], "meeting": nxt.isoformat(), "text": s[1]})
            else:
                steps.append({"kind": "done", "meeting": nxt.isoformat(), "text": f"Meeting {nxt}: chain complete (minutes validated)."})

    if not steps or all(st["kind"] in ("done", "read") for st in steps):
        steps.append({"kind": "free", "meeting": None,
                      "text": "Nothing pending in the meeting chain: BRIEFING §1 tasks, improvements from this session, or close."})

    return {"today": today.isoformat(), "next_meeting": nxt.isoformat() if nxt else None,
            "schedule": schedule(), "steps": steps, "notes": notes, "folders": [p.name for p in folders()]}


def text(s: dict) -> str:
    out = [f"Situation ({s['today']}): next meeting {s['next_meeting'] or 'unknown'}"
           + (f" (from schedule.json)" if s["schedule"].get("next") else "")
           + "."]
    for n in s["notes"]:
        out.append(f"  note: {n}")
    out.append(f"  Next step: {s['steps'][0]['text']}")
    for st in s["steps"][1:]:
        out.append(f"  Then: {st['text']}")
    out.append("  Say « go » (or anything) and the session does it; /advisor re-assesses on demand.")
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
