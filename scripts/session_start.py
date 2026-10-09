#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2026 right-on-skill (https://rightonskill.odoo.com/) - gse-light by Nicolas Guelfi (https://github.com/nicolasguelfi/gse-light)
# SPDX-License-Identifier: LicenseRef-PolyForm-Noncommercial-1.0.0  (non-commercial; see LICENSE.md)
"""Session-start hook of the project's repository: print what the session needs first, in ~30 lines.

Every session, whoever opens it:
  1. the repository, who is working (`git config user.name`) and their role — the Project Advisor
     when the name matches the "Project Advisor" row of project/governance/10-roles-and-go-aheads.md,
     a team member otherwise — and the number of uncommitted files (`git status --short`);
  2. the next meeting (project/meetings/, scripts/situation.py).
The Project Advisor's session also gets:
  3. project/BRIEFING.md §1 — what awaits him (task id and title);
  4. the latest journal entry's hand-over ("For the next session") and the next step of his week.

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
    from llm_call import REPO, project_dir  # noqa: E402
    PROJECT = project_dir()
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
    path = PROJECT / "BRIEFING.md"
    if not path.exists():
        return []
    body = section(path.read_text(encoding="utf-8"), "§1")
    rows = []
    for line in body.splitlines():
        m = re.match(r"^\|\s*(T\d+)\s*\|\s*(.*?)\s*\|", line)
        if m:
            rows.append(f"  {m.group(1)}  {m.group(2)[:110]}")
    return rows


def last_handover() -> tuple[str, str]:
    entries = sorted(p for p in (PROJECT / "journal").glob("20*-s*.md")) if (PROJECT / "journal").is_dir() else []
    if not entries:
        return "", ""
    last = entries[-1]
    return last.name, section(last.read_text(encoding="utf-8"), "For the next session")


def git_user() -> str:
    try:
        r = subprocess.run(["git", "config", "user.name"], cwd=REPO, capture_output=True, text=True, timeout=10)
        return r.stdout.strip() or "(git user.name not set)"
    except Exception as e:  # noqa: BLE001 — a hook never fails the session
        return f"(git user unavailable: {e})"


def advisor_name() -> str:
    """The holder of the "Project Advisor" row of the roles record (§1 table), or ""."""
    path = PROJECT / "governance" / "10-roles-and-go-aheads.md"
    if not path.exists():
        return ""
    m = re.search(r"^\|\s*\**Project Advisor\**\s*\|\s*([^|]+?)\s*\|", path.read_text(encoding="utf-8"), re.M)
    return m.group(1).strip() if m else ""


def is_advisor(user: str, holder: str) -> bool:
    """True when the git user is named in the holder cell ("Nicolas Guelfi (NG)" holds "Nicolas Guelfi");
    also true when the roles record names nobody yet (a fresh project: the Advisor fills it)."""
    if not holder or holder.startswith("<") or "to fill" in holder.lower():
        return True
    return bool(user) and user.lower() in holder.lower()


def uncommitted() -> str:
    try:
        r = subprocess.run(["git", "status", "--short"], cwd=REPO, capture_output=True, text=True, timeout=10)
        n = len([l for l in r.stdout.splitlines() if l.strip()])
        return f"{n} uncommitted file(s)" if n else "working tree clean"
    except Exception as e:  # noqa: BLE001 — a hook never fails the session
        return f"git status unavailable ({e})"


def main() -> int:
    try:
        user, holder = git_user(), advisor_name()
        advisor = is_advisor(user, holder)
        role = "the Project Advisor's session" if advisor else "a team member's session (the Advisor's skills — advisor, meeting, slides, cockpit-update, method-lesson, genai-onboarding — and project/BRIEFING.md are his)"
        print(f"{REPO.name} — session start (hook, read-only, method gse-light) · project folder {PROJECT.relative_to(REPO)}/ (README.md: the project, its phase, its people). Keep it light.")
        print(f"Git user: {user} — {role}; roles: {PROJECT.relative_to(REPO)}/governance/10-roles-and-go-aheads.md.")
        print(f"Repository: {uncommitted()} (`git status --short`).")
        try:
            from situation import situation, text  # noqa: E402
            import datetime as _dt
            s = situation(_dt.date.today())
            if advisor:
                print(text(s))
            else:
                print(f"Next meeting with the Project Advisor: {s['next_meeting'] or 'date not fixed yet'} (project/meetings/).")
        except Exception as e:  # noqa: BLE001
            print(f"  (situation unavailable: {e})")
        if not advisor:
            print("New here? ../gse-light/QUICKSTART.md (the numbered path), then CLAUDE.md of this repository; type / to see the skills; /upskilling first.")
            return 0
        print("Improve the project from this session: when a request has no artefact or an artefact "
              "does not fit, name the gap, do the task, propose the smallest fix (CLAUDE.md rule).")
        tasks = briefing_tasks()
        print("BRIEFING §1 — awaiting the Project Advisor:" if tasks else "BRIEFING §1 — nothing awaits the Project Advisor.")
        for row in tasks[:8]:
            print(row)
        name, hand = last_handover()
        if name:
            print(f"Last journal entry: {PROJECT.relative_to(REPO)}/journal/{name} — hand-over:")
            for line in hand.splitlines()[:12]:
                print("  " + line)
    except Exception as e:  # noqa: BLE001
        print(f"session_start hook: could not read the project folder ({e})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
