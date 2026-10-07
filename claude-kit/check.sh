#!/usr/bin/env bash
# SPDX-FileCopyrightText: Copyright (c) 2026 right-on-skill (https://rightonskill.odoo.com/) - gse-light by Nicolas Guelfi (https://github.com/nicolasguelfi/gse-light)
# SPDX-License-Identifier: LicenseRef-PolyForm-Noncommercial-1.0.0  (non-commercial; see LICENSE.md)
# Day-0 check for a developer (claude-kit/INSTALL.md). Read-only: changes nothing.
# Usage, from inside your product repository:  ../gse-light/claude-kit/check.sh
# Prints one line per check (OK / MISSING / WARN) and exits 1 if anything is MISSING.
set -uo pipefail

repo="$(git rev-parse --show-toplevel 2>/dev/null || true)"
kit="$(cd "$(dirname "$0")" && pwd)"
fail=0
ok()   { printf 'OK       %s\n' "$1"; }
miss() { printf 'MISSING  %s — %s\n' "$1" "$2"; fail=1; }
warn() { printf 'WARN     %s — %s\n' "$1" "$2"; }

[ -n "$repo" ] || { echo "MISSING  run this from inside your product repository"; exit 1; }
cd "$repo"

command -v git >/dev/null && ok "git $(git --version | awk '{print $3}')" || miss "git" "install Git"
if command -v claude >/dev/null; then ok "Claude Code $(claude --version 2>/dev/null | head -1)"
else miss "Claude Code" "install it and sign in with the invited account (INSTALL.md §1)"; fi

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

n=0
for s in decision-record session-close verify-claim upskilling; do
  [ -f ".claude/skills/$s/SKILL.md" ] || { miss "skill $s" "kit missing or outdated: ask the project lead"; n=1; }
done
[ $n = 0 ] && ok "kit skills present (decision-record, session-close, verify-claim, upskilling)"
[ -f .claude/agents/change-reviewer.md ] && ok "agent change-reviewer present" || miss "agent change-reviewer" "kit missing or outdated"

if [ -n "$(git ls-files .claude/skills | head -1)" ]; then ok "kit committed in the repository"
else miss "kit committed" "the kit files are not in git: the project lead commits them (INSTALL.md §2)"; fi

if [ -f .claude/KIT_VERSION ]; then
  v="$(cat .claude/KIT_VERSION)"; head="$(git -C "$kit" rev-parse --short HEAD 2>/dev/null || echo '?')"
  [ "$v" = "$head" ] && ok "kit version $v (current)" || warn "kit version $v" "gse-light is at $head: the project lead may refresh the kit"
else miss "KIT_VERSION" "kit not installed by install.sh"; fi

[ -f .claude/KIT_LICENSE.md ] && ok "kit licence notice present" || warn "KIT_LICENSE.md" "licence notice of the kit missing: the project lead re-runs install.sh"

n=0
for p in .env CLAUDE.local.md .claude/settings.local.json; do
  [ -z "$(git ls-files "$p")" ] || { miss "$p not in git" "personal file is tracked: git rm --cached $p"; n=1; }
done
[ $n = 0 ] && ok "no personal file tracked by git (.env, CLAUDE.local.md, settings.local.json)"
[ -f .env ] && ok ".env present" || warn ".env" "copy .env.example to .env and fill it (INSTALL.md §3)"

exit $fail
