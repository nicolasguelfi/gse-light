#!/usr/bin/env bash
# SPDX-FileCopyrightText: Copyright (c) 2026 right-on-skill (https://rightonskill.odoo.com/) - gse-light by Nicolas Guelfi (https://github.com/nicolasguelfi/gse-light)
# SPDX-License-Identifier: LicenseRef-PolyForm-Noncommercial-1.0.0  (non-commercial; see LICENSE.md)
# Day-0 check for a team member (kit/INSTALL.md). Read-only: changes nothing.
# Usage, from the root of the project's repository:  ../gse-light/kit/check.sh
# Prints one line per check (OK / MISSING / WARN) and exits 1 if anything is MISSING.
# Works with bash 3.2 (macOS) and Git Bash.
set -uo pipefail

repo="$(git rev-parse --show-toplevel 2>/dev/null || true)"
kit="$(cd "$(dirname "$0")" && pwd)"
gse="$(cd "$kit/.." && pwd)"
fail=0
ok()   { printf 'OK       %s\n' "$1"; }
miss() { printf 'MISSING  %s — %s\n' "$1" "$2"; fail=1; }
warn() { printf 'WARN     %s — %s\n' "$1" "$2"; }

[ -n "$repo" ] || { echo "MISSING  run this from inside the project's repository"; exit 1; }
cd "$repo"

# prerequisites: git, python3 (the method's scripts), Claude Code
command -v git >/dev/null && ok "git $(git --version | awk '{print $3}')" || miss "git" "install Git"
command -v python3 >/dev/null && ok "python3 $(python3 --version 2>&1 | awk '{print $2}')" \
  || miss "python3" "install Python 3 (the method's scripts need it: check_docs.py, situation.py)"
if command -v claude >/dev/null; then ok "Claude Code $(claude --version 2>/dev/null | head -1)"
elif [ -n "${CLAUDECODE:-}" ]; then ok "Claude Code (running inside a Claude Code session; \`claude\` not on this shell's PATH)"
else miss "Claude Code" "install it and sign in with the invited account (INSTALL.md §1)"; fi

# the two repositories side by side
[ -d "$repo/../gse-light/method" ] && ok "gse-light (the method) cloned next to this repository" \
  || miss "gse-light next to this repository" "git clone https://github.com/nicolasguelfi/gse-light.git into $(dirname "$repo")"

[ -f CLAUDE.md ] && ok "CLAUDE.md (the rules every session loads)" \
  || miss "CLAUDE.md" "the kit is not installed here: the person who installs the kit runs ../gse-light/kit/install.sh (INSTALL.md §2)"
if [ -f project/README.md ] && [ -f project/BRIEFING.md ]; then ok "project/ (the shared record: registers, requirements, planning, meetings, journal)"
else miss "project/" "the project folder is missing or incomplete: install.sh creates it from the kit's skeleton (INSTALL.md §2)"; fi

# the kit's files
n=0
for s in decision-record session-close verify-claim upskilling design-phase review; do
  [ -f ".claude/skills/$s/SKILL.md" ] || { miss "skill $s" "kit missing or outdated: ask the person who installs the kit"; n=1; }
done
[ $n = 0 ] && ok "team skills present (decision-record, session-close, verify-claim, upskilling, design-phase, review)"
n=0
for s in advisor meeting slides cockpit-update method-lesson genai-onboarding; do
  [ -f ".claude/skills/$s/SKILL.md" ] || { warn "skill $s" "the Project Advisor's skill is missing: kit outdated"; n=1; }
done
[ $n = 0 ] && ok "Project Advisor's skills present (advisor, meeting, slides, cockpit-update, method-lesson, genai-onboarding)"
n=0
for a in change-reviewer delivery-auditor minutes-verifier design-reviewer; do
  [ -f ".claude/agents/$a.md" ] || { miss "agent $a" "kit missing or outdated"; n=1; }
done
[ $n = 0 ] && ok "agents present (change-reviewer, delivery-auditor, minutes-verifier, design-reviewer)"

if [ -f .claude/settings.json ]; then
  grep -q '"additionalDirectories"' .claude/settings.json \
    && ok "settings.json gives Claude read access to ../gse-light" \
    || warn "settings.json" "no additionalDirectories: Claude will not see ../gse-light — compare with ../gse-light/kit/templates/settings.json"
  grep -q 'session_start.py' .claude/settings.json \
    && ok "settings.json runs the start hook (the situation at every session start)" \
    || warn "settings.json" "no start hook: compare with ../gse-light/kit/templates/settings.json"
else miss ".claude/settings.json" "kit not installed by install.sh"; fi

if [ -f gates.sh ]; then
  # executable on this disk (what ./gates.sh needs here) and in git (what a fresh clone and CI get)
  [ -x gates.sh ] && ok "gates.sh present and executable (./gates.sh)" || warn "gates.sh" "not executable here: chmod +x gates.sh"
  mode="$(git ls-files -s gates.sh 2>/dev/null | awk '{print $1}')"
  if [ -n "$mode" ] && [ "$mode" != 100755 ]; then
    warn "gates.sh mode in git ($mode)" "not executable in git: git update-index --chmod=+x gates.sh, then commit"
  fi
else miss "gates.sh" "the gates command is missing: rerun install.sh"; fi
[ -f .github/workflows/gates.yml ] && ok "CI workflow gates.yml present" || warn "gates.yml" "no CI workflow for the gates: rerun install.sh"
[ -f .github/workflows/docs.yml ] && ok "CI workflow docs.yml present (documentation checks of project/)" || warn "docs.yml" "no CI workflow for the documentation checks: rerun install.sh"
if [ -f .gitattributes ] && grep -qF '*.sh text eol=lf' .gitattributes; then ok ".gitattributes keeps scripts LF"
else warn ".gitattributes" "'*.sh text eol=lf' missing: scripts may break on Windows — rerun install.sh"; fi

if [ -n "$(git ls-files .claude/skills | head -1)" ]; then ok "kit committed in this repository"
else miss "kit committed" "the kit files are not in git: the person who installed it commits them (INSTALL.md §2)"; fi

# kit version = last commit of gse-light that touched kit/ (not HEAD). Two clones can lag:
# this repository's kit behind ../gse-light (refresh with install.sh), or ../gse-light itself
# behind GitHub (git pull) — the recorded commit is then unknown in your clone.
if [ -f .claude/KIT_VERSION ]; then
  v="$(tr -d '[:space:]' < .claude/KIT_VERSION)"
  last="$(git -C "$gse" log -1 --format=%h -- kit 2>/dev/null || echo '?')"
  if [ "$v" = "$last" ]; then ok "kit version $v (current)"
  elif ! git -C "$gse" merge-base --is-ancestor "$v" HEAD 2>/dev/null; then
    warn "kit version $v" "your clone of gse-light is behind (it does not know $v): git pull in ../gse-light (and git pull here too)"
  else
    warn "kit version $v" "the kit in gse-light is newer ($last): the person who installs the kit refreshes it (install.sh), then you git pull here"
  fi
else miss "KIT_VERSION" "kit not installed by install.sh"; fi

[ -f .claude/KIT_LICENSE.md ] && ok "kit licence notice present" || warn "KIT_LICENSE.md" "licence notice of the kit missing: rerun install.sh"

# personal files
n=0
for p in .env CLAUDE.local.md .claude/settings.local.json; do
  [ -z "$(git ls-files "$p")" ] || { miss "$p not in git" "personal file is tracked: git rm --cached $p"; n=1; }
done
[ $n = 0 ] && ok "no personal file tracked by git (.env, CLAUDE.local.md, settings.local.json)"
# your own Claude Code rules: .claude/settings.local.json holds every rule of your role's file
if [ -f .claude/settings.local.json ]; then
  role="$(python3 - <<'PY' 2>/dev/null
import json, pathlib
mine = json.loads(pathlib.Path(".claude/settings.local.json").read_text()).get("permissions", {})
for f in sorted(pathlib.Path(".claude/roles").glob("*.json")):
    ref = json.loads(f.read_text()).get("permissions", {})
    if all(set(ref.get(k, [])) <= set(mine.get(k, [])) for k in ("allow", "ask", "deny")):
        print(f.stem); break
PY
)"
  [ -n "$role" ] && ok "your Claude Code rules hold the role '$role' (.claude/settings.local.json)" \
    || warn "settings.local.json" "it holds no role's full rules: compare with .claude/roles/*.json"
else
  warn "settings.local.json" "your own Claude Code rules are missing: cp .claude/roles/team.json .claude/settings.local.json (the Project Advisor: advisor.json)"
fi
[ -f .env ] && ok ".env present" || warn ".env" "copy .env.example to .env and fill it (INSTALL.md §3)"

exit $fail
