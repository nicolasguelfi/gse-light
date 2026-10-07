#!/usr/bin/env bash
# SPDX-FileCopyrightText: Copyright (c) 2026 Nicolas Guelfi - gse-light (https://github.com/nicolasguelfi/gse-light)
# SPDX-License-Identifier: LicenseRef-PolyForm-Noncommercial-1.0.0  (non-commercial; see LICENSE.md)
# Install or refresh the Project Advisor's kit in a project-management repository (the private
# repository holding instances/<name>/), cloned next to gse-light.
# Usage: ../gse-light/pm-kit/install.sh <path-to-pm-repository>      (e.g. .  from inside it)
# Overwrites only the kit's own skills and agents; creates CLAUDE.md, settings, .env.example and
# the CI workflow if absent (yours afterwards).
set -euo pipefail

[ $# -eq 1 ] || { echo "usage: $0 <path-to-pm-repository>" >&2; exit 1; }
kit="$(cd "$(dirname "$0")" && pwd)"
target="$(cd "$1" && pwd)"
[ -d "$target/instances" ] || { echo "$target has no instances/ folder: create instances/<name>/ first" >&2; exit 1; }
[ "$(cd "$target/.." && pwd)/gse-light" = "$(cd "$kit/.." && pwd)" ] \
  || echo "warning: gse-light is not next to $target; the scripts expect ../gse-light"

mkdir -p "$target/.claude/skills" "$target/.claude/agents"
for s in "$kit"/skills/*/; do
  name="$(basename "$s")"; rm -rf "$target/.claude/skills/$name"; cp -R "$s" "$target/.claude/skills/$name"; echo "skill   $name"
done
for a in "$kit"/agents/*.md; do cp "$a" "$target/.claude/agents/"; echo "agent   $(basename "$a" .md)"; done

if [ ! -f "$target/.claude/settings.json" ]; then cp "$kit/templates/settings.json" "$target/.claude/settings.json"; echo "created .claude/settings.json"; fi
if [ ! -f "$target/CLAUDE.md" ]; then cp "$kit/templates/CLAUDE.pm-repo.md" "$target/CLAUDE.md"; echo "created CLAUDE.md — fill the <…> fields"; fi
if [ ! -f "$target/.env.example" ]; then cp "$kit/templates/env.example" "$target/.env.example"; echo "created .env.example"; fi
if [ ! -f "$target/.github/workflows/docs.yml" ]; then
  mkdir -p "$target/.github/workflows"; cp "$kit/templates/docs.yml" "$target/.github/workflows/docs.yml"; echo "created .github/workflows/docs.yml"
fi
touch "$target/.gitignore"
for p in .env CLAUDE.local.md .claude/settings.local.json '**/meetings/**/audio*' '**/meetings/**/*.wav' '**/meetings/**/.record.pid' '**/meetings/**/record.log'; do
  grep -qxF "$p" "$target/.gitignore" || { echo "$p" >> "$target/.gitignore"; echo "added $p to .gitignore"; }
done

cp "$kit/../claude-kit/templates/KIT_LICENSE.md" "$target/.claude/KIT_LICENSE.md"
[ -z "$(git -C "$kit" status --porcelain -- . 2>/dev/null)" ] || echo "warning: pm-kit has uncommitted changes; PM_KIT_VERSION records the last commit only"
git -C "$kit" rev-parse --short HEAD > "$target/.claude/PM_KIT_VERSION" 2>/dev/null || true
echo "pm-kit version recorded in .claude/PM_KIT_VERSION; check: python3 ../gse-light/scripts/check_docs.py"
