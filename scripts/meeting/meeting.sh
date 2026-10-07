#!/usr/bin/env bash
# SPDX-FileCopyrightText: Copyright (c) 2026 Nicolas Guelfi - gse-light (https://github.com/nicolasguelfi/gse-light)
# SPDX-License-Identifier: LicenseRef-PolyForm-Noncommercial-1.0.0  (non-commercial; see LICENSE.md)
# meeting.sh — record the weekly meeting with ffmpeg, or import a file recorded elsewhere.
# Part of the Project Advisor's `meeting` skill. macOS only (avfoundation).
#
#   ../gse-light/scripts/meeting/meeting.sh devices                 # list audio inputs with their index
#   ../gse-light/scripts/meeting/meeting.sh start [DATE] [DEVICE]   # start recording, detached; DATE=YYYY-MM-DD (default today)
#   ../gse-light/scripts/meeting/meeting.sh status                  # is a recording running? for how long?
#   ../gse-light/scripts/meeting/meeting.sh stop                    # stop cleanly (ffmpeg finalises the file)
#   ../gse-light/scripts/meeting/meeting.sh import FILE [DATE]      # copy an audio/transcript file into the day folder
#
# Run from the project-management repository (the folder holding instances/), e.g.
#   ../gse-light/scripts/meeting/meeting.sh status
# Settings come from `.env` at its root (MEETING_AUDIO_DEVICE, INSTANCE, MEETINGS_DIR).
# Output: <MEETINGS_DIR>/<DATE>/audio.m4a (AAC mono 48 kHz 96 kb/s ≈ 43 MB per hour),
# meta.json (start, stop, device, duration), record.log. Audio files are git-ignored.
set -euo pipefail

# the project-management repository: GSE_PM_ROOT, else the nearest folder above holding instances/
root="${GSE_PM_ROOT:-}"
if [ -z "$root" ]; then
  d="$PWD"
  while [ "$d" != "/" ] && [ ! -d "$d/instances" ]; do d="$(dirname "$d")"; done
  [ -d "$d/instances" ] || { echo "run this from the project-management repository (the folder holding instances/)" >&2; exit 1; }
  root="$d"
fi
cd "$root"

# --- .env: only KEY=VALUE lines, no code is sourced
if [ -f .env ]; then
  while IFS='=' read -r k v; do
    case "$k" in ''|\#*) continue ;; esac
    v="${v%% #*}"; v="${v%\"}"; v="${v#\"}"
    export "$k=$v"
  done < <(grep -E '^[A-Za-z_][A-Za-z0-9_]*=' .env || true)
fi
if [ -z "${INSTANCE:-}" ]; then
  n="$(find instances -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')"
  [ "$n" = 1 ] || { echo "set INSTANCE in $root/.env (instances/ holds $n folders)" >&2; exit 1; }
  INSTANCE="$(basename "$(find instances -mindepth 1 -maxdepth 1 -type d)")"
fi
dir_base="${MEETINGS_DIR:-instances/$INSTANCE/meetings}"
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
    case "$lower" in
      m4a|mp3|wav|aac|ogg|flac|mp4|mov|webm) dest="$d/audio.$lower" ;;
      vtt|srt)                               dest="$d/transcript-imported.$lower" ;;
      txt|md|docx)                           dest="$d/transcript-imported.$lower" ;;
      *) echo "unknown extension .$ext — importing as-is"; dest="$d/$(basename "$src")" ;;
    esac
    [ -e "$dest" ] && dest="${dest%.*}-$(date +%H%M%S).${dest##*.}"
    cp "$src" "$dest"
    printf '{"imported_from": "%s", "file": "%s", "imported_at": "%s"}\n' "$src" "$(basename "$dest")" "$(date -Iseconds)" >> "$d/imports.jsonl"
    echo "imported → $dest"
    ;;

  *)
    sed -n '2,15p' "$0" | sed 's/^# \{0,1\}//'
    ;;
esac
