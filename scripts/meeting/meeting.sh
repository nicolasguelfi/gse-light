#!/usr/bin/env bash
# SPDX-FileCopyrightText: Copyright (c) 2026 right-on-skill (https://rightonskill.odoo.com/) - gse-light by Nicolas Guelfi (https://github.com/nicolasguelfi/gse-light)
# SPDX-License-Identifier: LicenseRef-PolyForm-Noncommercial-1.0.0  (non-commercial; see LICENSE.md)
# meeting.sh — record the weekly meeting with ffmpeg, or import a file recorded elsewhere.
# Part of the Project Advisor's `meeting` skill. macOS only (avfoundation).
#
#   ../gse-light/scripts/meeting/meeting.sh devices                 # list audio inputs with their index
#   ../gse-light/scripts/meeting/meeting.sh start [DATE] [DEVICE]   # start recording, detached; DATE=YYYY-MM-DD (default today)
#   ../gse-light/scripts/meeting/meeting.sh status                  # is a recording running? for how long?
#   ../gse-light/scripts/meeting/meeting.sh stop                    # stop cleanly (ffmpeg finalises the file)
#   ../gse-light/scripts/meeting/meeting.sh import FILE [DATE]      # copy an audio/transcript file into the day folder
#                                                                   # (.docx is converted to text with textutil on macOS)
#
# Run from the project's repository (the folder holding project/), e.g.
#   ../gse-light/scripts/meeting/meeting.sh status
# Settings come from `.env` at its root (MEETING_AUDIO_DEVICE, MEETINGS_DIR); a value
# may end with an inline comment, and a blank value counts as unset.
# Output: <MEETINGS_DIR>/<DATE>/audio.m4a (AAC mono 48 kHz 96 kb/s ≈ 43 MB per hour),
# meta.json (start, stop, device, duration), record.log. Audio files are git-ignored.
set -euo pipefail

# the project's repository: GSE_PROJECT_ROOT, else the nearest folder above holding project/
root="${GSE_PROJECT_ROOT:-}"
if [ -z "$root" ]; then
  d="$PWD"
  while [ "$d" != "/" ] && [ ! -d "$d/project" ]; do d="$(dirname "$d")"; done
  [ -d "$d/project" ] || { echo "run this from the project's repository (the folder holding project/)" >&2; exit 1; }
  root="$d"
fi
cd "$root"

# --- .env: only KEY=VALUE lines, no code is sourced. The inline comment is stripped, then the
# blanks around the value (MEETINGS_DIR=   # comment  once gave a folder named by spaces), then
# the quotes; an empty value is left unset so the defaults below apply.
trim() { local x="$1"; x="${x#"${x%%[![:space:]]*}"}"; x="${x%"${x##*[![:space:]]}"}"; printf '%s' "$x"; }
if [ -f .env ]; then
  while IFS='=' read -r k v; do
    case "$k" in ''|\#*) continue ;; esac
    v="${v%%[[:space:]]#*}"; case "$v" in \#*) v="" ;; esac   # inline comment: blank then #, or # first
    v="$(trim "$v")"; v="${v%\"}"; v="${v#\"}"; v="${v%\'}"; v="${v#\'}"
    [ -n "$v" ] && export "$k=$v"
  done < <(grep -E '^[A-Za-z_][A-Za-z0-9_]*=' .env || true)
fi
dir_base="${MEETINGS_DIR:-project/meetings}"
case "$dir_base" in /*) base="$dir_base" ;; *) base="$root/$dir_base" ;; esac
device="${MEETING_AUDIO_DEVICE:-0}"

need() { command -v "$1" >/dev/null 2>&1 || { echo "missing: $1 (brew install $1)" >&2; exit 1; }; }

day_dir() { echo "$base/${1:-$(date +%F)}"; }

cmd="${1:-help}"; shift || true
case "$cmd" in
  devices)
    need ffmpeg
    echo "Audio inputs seen by ffmpeg (use the index as DEVICE / MEETING_AUDIO_DEVICE):"
    ffmpeg -hide_banner -f avfoundation -list_devices true -i "" 2>&1 \
      | sed -n '/audio devices/,$p' | grep -E '^\[AVFoundation[^]]*\] \[[0-9]+\]' \
      | sed -E 's/^\[[^]]*\] //' || true
    ;;

  start)
    need ffmpeg
    date_arg="${1:-$(date +%F)}"; dev="${2:-$device}"
    d="$(day_dir "$date_arg")"; mkdir -p "$d"
    pidfile="$d/.record.pid"
    if [ -f "$pidfile" ] && kill -0 "$(cat "$pidfile")" 2>/dev/null; then
      echo "already recording (pid $(cat "$pidfile")) in $d"; exit 1
    fi
    out="$d/audio.m4a"
    if [ -e "$out" ]; then out="$d/audio-$(date +%H%M%S).m4a"; fi
    nohup ffmpeg -hide_banner -nostdin -loglevel warning \
      -f avfoundation -i ":$dev" -ac 1 -ar 48000 -c:a aac -b:a 96k "$out" \
      > "$d/record.log" 2>&1 &
    pid=$!
    sleep 2
    if ! kill -0 "$pid" 2>/dev/null; then
      echo "ffmpeg stopped at once — see $d/record.log (wrong device index? run: $0 devices)"; cat "$d/record.log"; exit 1
    fi
    echo "$pid" > "$pidfile"
    printf '{"start": "%s", "device": "%s", "file": "%s"}\n' "$(date -Iseconds)" "$dev" "$(basename "$out")" > "$d/meta.json"
    echo "recording → $out (pid $pid, device $dev). Stop with: $0 stop"
    ;;

  status)
    found=0
    for pidfile in "$base"/*/.record.pid; do
      [ -f "$pidfile" ] || continue
      pid="$(cat "$pidfile")"; d="$(dirname "$pidfile")"
      if kill -0 "$pid" 2>/dev/null; then
        start="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["start"])' "$d/meta.json" 2>/dev/null || echo "?")"
        echo "recording in $d (pid $pid) since $start"; found=1
      else
        echo "stale pid file in $d (ffmpeg not running) — removing"; rm -f "$pidfile"
      fi
    done
    [ "$found" = 1 ] || echo "no recording running"
    ;;

  stop)
    stopped=0
    for pidfile in "$base"/*/.record.pid; do
      [ -f "$pidfile" ] || continue
      pid="$(cat "$pidfile")"; d="$(dirname "$pidfile")"
      if kill -0 "$pid" 2>/dev/null; then
        kill -INT "$pid"                      # ffmpeg writes the m4a index on SIGINT
        for _ in $(seq 1 30); do kill -0 "$pid" 2>/dev/null || break; sleep 1; done
        kill -0 "$pid" 2>/dev/null && kill -TERM "$pid" || true
      fi
      rm -f "$pidfile"
      file="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["file"])' "$d/meta.json" 2>/dev/null || echo audio.m4a)"
      dur=""
      command -v ffprobe >/dev/null && dur="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$d/$file" 2>/dev/null || true)"
      python3 - "$d/meta.json" "$dur" <<'PY'
import json, sys, datetime
p, dur = sys.argv[1], sys.argv[2]
m = json.load(open(p)); m["stop"] = datetime.datetime.now().isoformat(timespec="seconds")
if dur: m["duration_s"] = round(float(dur))
json.dump(m, open(p, "w"), indent=2)
PY
      echo "stopped → $d/$file${dur:+ ($(printf '%.0f' "$dur") s)}"; stopped=1
    done
    [ "$stopped" = 1 ] || echo "nothing to stop"
    ;;

  import)
    src="${1:?usage: $0 import FILE [DATE]}"; date_arg="${2:-$(date +%F)}"
    [ -f "$src" ] || { echo "not a file: $src" >&2; exit 1; }
    d="$(day_dir "$date_arg")"; mkdir -p "$d"
    ext="${src##*.}"; lower="$(echo "$ext" | tr '[:upper:]' '[:lower:]')"
    convert=""
    case "$lower" in
      m4a|mp3|wav|aac|ogg|flac|mp4|mov|webm) dest="$d/audio.$lower" ;;
      vtt|srt|txt|md)                        dest="$d/transcript-imported.$lower" ;;
      docx)  # a word-processor transcript: plain text when textutil (macOS) is there, else the file as-is
        if command -v textutil >/dev/null 2>&1; then convert=textutil; dest="$d/transcript-imported.txt"
        else echo "no textutil here: .docx imported as-is (convert it to .txt by hand, or import the .txt)"; dest="$d/transcript-imported.docx"; fi ;;
      *) echo "unknown extension .$ext — importing as-is"; dest="$d/$(basename "$src")" ;;
    esac
    [ -e "$dest" ] && dest="${dest%.*}-$(date +%H%M%S).${dest##*.}"
    if [ "$convert" = textutil ]; then textutil -convert txt -output "$dest" "$src"; else cp "$src" "$dest"; fi
    printf '{"imported_from": "%s", "file": "%s", "imported_at": "%s"}\n' "$src" "$(basename "$dest")" "$(date -Iseconds)" >> "$d/imports.jsonl"
    echo "imported → $dest"
    ;;

  *)  # help: the comment block at the top of this file, without the licence header lines
    awk 'NR > 3 && /^set -/ { exit } NR > 3 && /^#/ { sub(/^# ?/, ""); print }' "$0"
    ;;
esac
