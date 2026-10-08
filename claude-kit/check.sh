#!/usr/bin/env bash
# SPDX-FileCopyrightText: Copyright (c) 2026 right-on-skill (https://rightonskill.odoo.com/) - gse-light by Nicolas Guelfi (https://github.com/nicolasguelfi/gse-light)
# SPDX-License-Identifier: LicenseRef-PolyForm-Noncommercial-1.0.0  (non-commercial; see LICENSE.md)
# Day-0 check for a developer (claude-kit/INSTALL.md). Read-only: changes nothing.
# Usage, from inside your product repository:  ../gse-light/claude-kit/check.sh
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

[ -n "$repo" ] || { echo "MISSING  run this from inside your product repository"; exit 1; }
cd "$repo"

# prerequisites: git, python3 (the method's scripts), Claude Code
command -v git >/dev/null && ok "git $(git --version | awk '{print $3}')" || miss "git" "install Git"
command -v python3 >/dev/null && ok "python3 $(python3 --version 2>&1 | awk '{print $2}')" \
  || miss "python3" "install Python 3 (the method's scripts need it: check_docs.py, situation.py)"
if command -v claude >/dev/null; then ok "Claude Code $(claude --version 2>/dev/null | head -1)"
else miss "Claude Code" "install it and sign in with the invited account (INSTALL.md §1)"; fi

# the three repositories side by side
[ -d "$repo/../gse-light/method" ] && ok "gse-light (the method) cloned next to this repository" \
  || miss "gse-light next to this repository" "git clone https://github.com/nicolasguelfi/gse-light.git into $(dirname "$repo")"

if [ -f CLAUDE.md ]; then
  zone="$(grep -oE '\.\./[A-Za-z0-9._-]+/instances/[A-Za-z0-9_-]+/' CLAUDE.md | head -1)"
  pmname="$(echo "$zone" | cut -d/ -f2)"; inst="$(echo "$zone" | cut -d/ -f4)"
  if [ -n "$inst" ]; then
    ok "CLAUDE.md (instance: $inst, project management in $pmname)"
    [ -d "$repo/../$pmname/instances/$inst" ] && ok "$pmname cloned next to this repository" \
      || miss "$pmname next to this repository" "clone the project-management repository $pmname into $(dirname "$repo") (ask the project lead for access)"
  else warn "CLAUDE.md" "no project-management zone (../<pm-repo>/instances/<instance>/) named in it"; fi
else miss "CLAUDE.md" "the kit is not installed here: ask the project lead (INSTALL.md §2)"; fi

# the kit's files
n=0
for s in decision-record session-close verify-claim upskilling design-phase; do
  [ -f ".claude/skills/$s/SKILL.md" ] || { miss "skill $s" "kit missing or outdated: ask the project lead"; n=1; }
done
[ $n = 0 ] && ok "kit skills present (decision-record, session-close, verify-claim, upskilling, design-phase)"
[ -f .claude/agents/change-reviewer.md ] && ok "agent change-reviewer present" || miss "agent change-reviewer" "kit missing or outdated"

if [ -f .claude/settings.json ]; then
  grep -q '"additionalDirectories"' .claude/settings.json \
    && ok "settings.json gives Claude read access to ../gse-light and the project-management repository" \
    || warn "settings.json" "no additionalDirectories: Claude will not see ../gse-light nor the registers — compare with ../gse-light/claude-kit/templates/settings.json"
else miss ".claude/settings.json" "kit not installed by install.sh: ask the project lead"; fi

if [ -f gates.sh ]; then
  [ -x gates.sh ] && ok "gates.sh present and executable (./gates.sh)" || warn "gates.sh" "not executable: chmod +x gates.sh (then commit the mode)"
else miss "gates.sh" "the gates command is missing: the project lead re-runs install.sh"; fi
[ -f .github/workflows/gates.yml ] && ok "CI workflow gates.yml present" || warn "gates.yml" "no CI workflow: the project lead re-runs install.sh"
if [ -f .gitattributes ] && grep -qF '*.sh text eol=lf' .gitattributes; then ok ".gitattributes keeps scripts LF"
else warn ".gitattributes" "'*.sh text eol=lf' missing: scripts may break on Windows — the project lead re-runs install.sh"; fi

if [ -n "$(git ls-files .claude/skills | head -1)" ]; then ok "kit committed in the repository"
else miss "kit committed" "the kit files are not in git: the project lead commits them (INSTALL.md §2)"; fi

# kit version = last commit of gse-light that touched claude-kit/ (not HEAD)
if [ -f .claude/KIT_VERSION ]; then
  v="$(tr -d '[:space:]' < .claude/KIT_VERSION)"
  last="$(git -C "$gse" log -1 --format=%h -- claude-kit 2>/dev/null || echo '?')"
  [ "$v" = "$last" ] && ok "kit version $v (current)" || warn "kit version $v" "the kit in gse-light is at $last: the project lead may refresh it (install.sh)"
else miss "KIT_VERSION" "kit not installed by install.sh"; fi

[ -f .claude/KIT_LICENSE.md ] && ok "kit licence notice present" || warn "KIT_LICENSE.md" "licence notice of the kit missing: the project lead re-runs install.sh"

# personal files
n=0
for p in .env CLAUDE.local.md .claude/settings.local.json; do
  [ -z "$(git ls-files "$p")" ] || { miss "$p not in git" "personal file is tracked: git rm --cached $p"; n=1; }
done
[ $n = 0 ] && ok "no personal file tracked by git (.env, CLAUDE.local.md, settings.local.json)"
[ -f .env ] && ok ".env present" || warn ".env" "copy .env.example to .env and fill it (INSTALL.md §3)"

exit $fail
