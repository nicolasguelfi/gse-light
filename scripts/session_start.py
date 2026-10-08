#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2026 right-on-skill (https://rightonskill.odoo.com/) - gse-light by Nicolas Guelfi (https://github.com/nicolasguelfi/gse-light)
# SPDX-License-Identifier: LicenseRef-PolyForm-Noncommercial-1.0.0  (non-commercial; see LICENSE.md)
"""Session-start hook: print what the Project Advisor's session needs first, in ~30 lines.

  1. who is working (`git config user.name`) — sessions opened in a project-management
     repository are the Project Advisor's; team members work from their sandbox or product repository;
  2. instances/<INSTANCE>/BRIEFING.md §1 — what awaits the Project Advisor (task id and title);
  3. the latest journal entry's hand-over ("For the next session");
  4. the number of uncommitted files, measured by `git status --short`.

Wired in .claude/settings.json under hooks.SessionStart. Read-only; prints nothing that
is not already in the repository. Exit code 0 always (a hook must never block a session).
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
try:
    from llm_call import PM, instance_dir  # noqa: E402
    INST = instance_dir()
except SystemExit as e:  # a hook never blocks a session
    print(f"session start: {e}")
    sys.exit(0)


def section(text: str, heading_prefix: str) -> str:
    """Return the body of the first heading starting with `heading_prefix` (any level)."""
    lines = text.splitlines()
    out, inside = [], False
    for line in lines:
        if line.startswith("#"):
            if inside:
                break
            inside = line.lstrip("#").strip().startswith(heading_prefix)
            continue
        if inside:
            out.append(line)
    return "\n".join(out).strip()


def briefing_tasks() -> list[str]:
    text = (INST / "BRIEFING.md").read_text(encoding="utf-8")
    body = section(text, "§1")
    rows = []
    for line in body.splitlines():
        m = re.match(r"^\|\s*(T\d+)\s*\|\s*(.*?)\s*\|", line)
        if m:
            rows.append(f"  {m.group(1)}  {m.group(2)[:110]}")
    return rows


def last_handover() -> tuple[str, str]:
    entries = sorted(p for p in (INST / "journal").glob("20*-s*.md"))
    if not entries:
        return "", ""
    last = entries[-1]
    return last.name, section(last.read_text(encoding="utf-8"), "For the next session")


def git_user() -> str:
    try:
        r = subprocess.run(["git", "config", "user.name"], cwd=PM, capture_output=True, text=True, timeout=10)
        return r.stdout.strip() or "(git user.name not set)"
    except Exception as e:  # noqa: BLE001 — a hook never fails the session
        return f"(git user unavailable: {e})"


def uncommitted() -> str:
    try:
        r = subprocess.run(["git", "status", "--short"], cwd=PM, capture_output=True, text=True, timeout=10)
        n = len([l for l in r.stdout.splitlines() if l.strip()])
        return f"{n} uncommitted file(s)" if n else "working tree clean"
    except Exception as e:  # noqa: BLE001 — a hook never fails the session
        return f"git status unavailable ({e})"


def main() -> int:
    try:
        print(f"{PM.name} — session start (hook, read-only, method gse-light) · active instance: {INST.name} ({INST.relative_to(PM)}/README.md). Keep it light.")
        print(f"Git user: {git_user()} — sessions here are the Project Advisor's; team members work from their sandbox or product repository.")
        print("Improve the project from this session: when a request has no artefact or an artefact "
              "does not fit, name the gap, do the task, propose the smallest fix (CLAUDE.md rule).")
        print(f"Repository: {uncommitted()} (`git status --short`).")
        try:
            sys.path.insert(0, str(ROOT / "scripts"))
            from situation import situation, text  # noqa: E402
            import datetime as _dt
            print(text(situation(_dt.date.today())))
        except Exception as e:  # noqa: BLE001
            print(f"  (situation unavailable: {e})")
        tasks = briefing_tasks()
        print("BRIEFING §1 — awaiting the Project Advisor:" if tasks else "BRIEFING §1 — nothing awaits the Project Advisor.")
        for row in tasks[:8]:
            print(row)
        name, hand = last_handover()
        if name:
            print(f"Last journal entry: {INST.relative_to(PM)}/journal/{name} — hand-over:")
            for line in hand.splitlines()[:12]:
                print("  " + line)
    except Exception as e:  # noqa: BLE001
        print(f"session_start hook: could not read the cockpit ({e})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
