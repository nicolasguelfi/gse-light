#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2026 right-on-skill (https://rightonskill.odoo.com/) - gse-light by Nicolas Guelfi (https://github.com/nicolasguelfi/gse-light)
# SPDX-License-Identifier: LicenseRef-PolyForm-Noncommercial-1.0.0  (non-commercial; see LICENSE.md)
"""Transcribe a meeting recording: locally by default, with Gemini on request.

  python3 ../gse-light/scripts/meeting/transcribe.py project/meetings/<date>            # engine from .env (TRANSCRIBE_ENGINE; else openrouter when its key is set; else local)
  python3 ../gse-light/scripts/meeting/transcribe.py project/meetings/<date> --engine gemini
  python3 ../gse-light/scripts/meeting/transcribe.py path/to/audio.m4a --language fr
  python3 ../gse-light/scripts/meeting/transcribe.py project/meetings/<date> --engine openrouter \
      --speakers "Ana (project lead), Ben (developer), the Project Advisor"

Given a folder, the audio file is audio.m4a (what meeting.sh records) when present, else the
first audio file in name order; the choice and the other candidates are printed.

Engines
  local   mlx-whisper (Apple Silicon, fast) if installed, else whisper.cpp's `whisper-cli`.
          Nothing leaves the machine. No speaker labels. Install once, in the project
          repository's environment (<project-repo>/.venv, a link to ~/.venvs/<name>; set-up in
          scripts/README.md — the script switches to that environment by itself):
              uv pip install --python .venv/bin/python mlx-whisper   # model (~1.6 GB) downloads on first run
          or  brew install whisper-cpp           # and set WHISPER_CPP_MODEL to a ggml model file
  gemini  Google AI Studio (GOOGLE_API_KEY in .env) through scripts/llm_call.py: the audio
          is uploaded; the model returns a transcript with timestamps and speaker labels.
          The cost line goes to project/journal/llm-costs.csv and <meeting>/cost.json.
          Rule of thumb for the cost: Gemini counts about 32 input tokens per second of audio,
          so one hour of meeting is about 115 000 input tokens (plus the transcript as output).
  openrouter  The same kind of transcript through OpenRouter (OPENROUTER_API_KEY in .env, model
          OPENROUTER_MODEL, default google/gemini-2.5-pro), through llm_call.py too. The audio
          is cut by ffmpeg into parts of --chunk-minutes (default 20) that overlap by 10 s, sent
          one after the other (mp3 mono, inline); each part gets the end of the previous one so
          that the speaker labels stay the same; the times are shifted back onto the whole
          meeting and the overlap is dropped. One cost line per part.
          Speaker labels are the model's guesses: --speakers names the people present (names
          and roles) so that the model can use a name when the conversation makes it certain.

Output, next to the audio: transcript.md (one paragraph per segment, [hh:mm:ss] prefix),
plus transcript.srt and transcript.json for the local engine.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from llm_call import REPO, load_env, prefer_pm_venv  # noqa: E402

AUDIO_EXT = (".m4a", ".mp3", ".wav", ".aac", ".ogg", ".flac", ".mp4", ".mov", ".webm")

GEMINI_PROMPT = """Transcribe this meeting recording completely and faithfully, in the language(s)
actually spoken (French and English may alternate; keep each sentence in its language).
Format: Markdown, one line per utterance:
[hh:mm:ss] Speaker N: text
Use stable labels Speaker 1, Speaker 2… for distinct voices (do not guess names).
Do not summarise, do not omit, do not translate. Mark inaudible passages [inaudible]."""


def hms(seconds: float) -> str:
    s = int(seconds)
    return f"{s // 3600:02d}:{(s % 3600) // 60:02d}:{s % 60:02d}"


def find_audio(target: Path) -> tuple[Path, Path]:
    """Return (meeting_dir, audio_file) from a folder or a file path. In a folder, audio.m4a (the
    recorder's own file) comes first, else the first audio file in name order; the choice is printed."""
    if target.is_dir():
        cands = sorted(p for p in target.iterdir() if p.is_file() and p.suffix.lower() in AUDIO_EXT)
        if not cands:
            sys.exit(f"no audio file in {target} (expected one of {', '.join(AUDIO_EXT)})")
        chosen = next((p for p in cands if p.name == "audio.m4a"), cands[0])
        others = [p.name for p in cands if p != chosen]
        print(f"[transcribe] audio: {chosen.name}" + (f" (also here, not used: {', '.join(others)} — pass the file path to pick one)" if others else ""),
              file=sys.stderr)
        return target, chosen
    if target.suffix.lower() in AUDIO_EXT and target.exists():
        return target.parent, target
    sys.exit(f"not a meeting folder nor an audio file: {target}")


# ------------------------------------------------------------------------------- local

def local_engine() -> tuple[str, str] | None:
    in_venv = REPO / ".venv" / "bin" / "mlx_whisper"  # the project repository's environment
    if in_venv.exists():
        return "mlx_whisper", str(in_venv)
    if shutil.which("mlx_whisper"):
        return "mlx_whisper", shutil.which("mlx_whisper")
    if shutil.which("whisper-cli"):
        return "whisper-cli", shutil.which("whisper-cli")
    return None


def transcribe_local(mdir: Path, audio: Path, language: str, env: dict) -> Path:
    eng = local_engine()
    if not eng:
        sys.exit("no local engine. Install once, in the project repository's environment\n"
                 "(<project-repo>/.venv, a link to ~/.venvs/<name> — set-up in gse-light/scripts/README.md):\n"
                 "  uv pip install --python .venv/bin/python mlx-whisper   (Apple Silicon; model downloads on first run)\n"
                 "  or: brew install whisper-cpp     (then WHISPER_CPP_MODEL=/path/to/ggml-large-v3-turbo.bin in .env)\n"
                 "Or run with --engine gemini.")
    name, exe = eng
    out_md = mdir / "transcript.md"
    if name == "mlx_whisper":
        model = env.get("WHISPER_MODEL", "mlx-community/whisper-large-v3-turbo")
        # Without these two, whisper can loop on one phrase for an hour (measured 2026-10-09:
        # 157 of 229 lines); with them, 1 of 1 249.
        cmd = [exe, str(audio), "--model", model, "--output-dir", str(mdir), "--output-format", "all",
               "--condition-on-previous-text", "False", "--word-timestamps", "True",
               "--hallucination-silence-threshold", "2"]
        if language:
            cmd += ["--language", language]
        print("[transcribe] " + " ".join(cmd), file=sys.stderr)
        subprocess.run(cmd, check=True)
        # mlx_whisper names its outputs after the audio file; keep one stable name.
        for ext in ("json", "srt", "txt", "vtt", "tsv"):
            produced = mdir / f"{audio.stem}.{ext}"
            if produced.exists():
                produced.replace(mdir / f"transcript.{ext}")
        seg_json = mdir / "transcript.json"
        segments = json.loads(seg_json.read_text(encoding="utf-8")).get("segments", []) if seg_json.exists() else []
        lines = [f"[{hms(s['start'])}] {s['text'].strip()}" for s in segments]
    else:  # whisper.cpp
        model = env.get("WHISPER_CPP_MODEL")
        if not model:
            sys.exit("WHISPER_CPP_MODEL missing in .env (path to a ggml model file)")
        wav = mdir / "audio-16k.wav"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(audio), "-ac", "1", "-ar", "16000", str(wav)], check=True)
        cmd = [exe, "-m", model, "-f", str(wav), "-oj", "-osrt", "-of", str(mdir / "transcript")]
        if language:
            cmd += ["-l", language]
        print("[transcribe] " + " ".join(cmd), file=sys.stderr)
        subprocess.run(cmd, check=True)
        wav.unlink(missing_ok=True)
        data = json.loads((mdir / "transcript.json").read_text(encoding="utf-8"))
        lines = [f"[{hms(t['offsets']['from'] / 1000)}] {t['text'].strip()}" for t in data.get("transcription", [])]
    header = f"# Transcript — {mdir.name}\n\nEngine: {name} ({env.get('WHISPER_MODEL') or env.get('WHISPER_CPP_MODEL')}), local, no speaker labels.\n\n"
    out_md.write_text(header + "\n".join(lines) + "\n", encoding="utf-8")
    return out_md


# -------------------------------------------------------------------------- openrouter

OVERLAP_S = 10
# Any [a:b] or [a:b:c] / [a:b.c] stamp, wherever the model puts it (it may glue utterances on one line).
STAMP = re.compile(r"\[(\d{1,2}):(\d{2})(?:[:.](\d{1,3}))?\]")
PART_FORMAT = """
Times: [MM:SS] counted from the start of this audio part (minutes and seconds only, e.g. [07:42]).
Start a NEW LINE for every utterance; every line starts with its [MM:SS] stamp."""


def stamp_seconds(a: str, b: str, c: str | None, part_len: float) -> float:
    """[MM:SS], [MM:SS:mmm] / [MM:SS.mmm] (milliseconds) or [HH:MM:SS]; a reading that falls
    beyond the part is taken as minutes:seconds:fraction instead."""
    a_, b_ = int(a), int(b)
    if c is None:
        return a_ * 60 + b_
    if len(c) == 3:
        return a_ * 60 + b_ + int(c) / 1000
    hms_reading = a_ * 3600 + b_ * 60 + int(c)
    return hms_reading if hms_reading <= part_len + 5 else a_ * 60 + b_ + int(c) / 100


def utterances(raw: str, part_len: float) -> list[tuple[float, str]]:
    """Split the model's answer into (seconds from the part's start, text) at every stamp."""
    stamps = list(STAMP.finditer(raw))
    out = []
    for i, m in enumerate(stamps):
        end = stamps[i + 1].start() if i + 1 < len(stamps) else len(raw)
        text = " ".join(raw[m.end():end].split())
        if text:
            out.append((stamp_seconds(*m.groups(), part_len), text))
    return out


def duration_s(audio: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                          str(audio)], check=True, capture_output=True, text=True).stdout.strip()
    return float(out)


def transcribe_openrouter(mdir: Path, audio: Path, language: str, env: dict,
                          speakers: str = "", chunk_minutes: int = 20) -> Path:
    model = env.get("OPENROUTER_MODEL") or "google/gemini-2.5-pro"
    out_md = mdir / "transcript.md"
    total = duration_s(audio)
    step = chunk_minutes * 60
    starts = [i * step for i in range(int(total // step) + (1 if total % step else 0))]
    lines: list[str] = []
    parts_dir = mdir / "transcript-parts"  # the model's raw answer per part, kept for checking
    parts_dir.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="transcribe-") as tmp:
        for n, start in enumerate(starts, 1):
            lead = OVERLAP_S if start else 0
            part_len = min(step + lead, total - start + lead)
            part = Path(tmp) / f"part{n:02d}.mp3"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(start - lead), "-t", str(step + lead),
                            "-i", str(audio), "-ac", "1", "-ar", "16000", "-c:a", "libmp3lame", "-b:a", "32k",
                            str(part)], check=True)
            prompt = (GEMINI_PROMPT.replace("[hh:mm:ss]", "[MM:SS]") + PART_FORMAT
                      + (f"\nThe main language is {language}." if language else "")
                      + (f"\nPeople present (use a name only when the conversation makes it certain, "
                         f"otherwise Speaker N): {speakers}" if speakers else ""))
            if lines:
                prompt += ("\nThis part follows an earlier one; keep the same speaker labels. "
                           "The earlier part ended with:\n" + "\n".join(lines[-12:]))
            raw = parts_dir / f"part{n:02d}.md"
            cmd = [sys.executable, str(ROOT / "scripts" / "llm_call.py"), "--provider", "openrouter",
                   "--model", model, "--prompt", prompt, "--file", str(part), "--out", str(raw),
                   "--meeting", str(mdir), "--purpose", f"transcribe {mdir.name} part {n}/{len(starts)}"]
            print(f"[transcribe] openrouter {model} part {n}/{len(starts)} from {hms(start)}", file=sys.stderr)
            subprocess.run(cmd, check=True)
            for rel, text in utterances(raw.read_text(encoding="utf-8"), part_len):
                if rel < lead:  # already in the previous part
                    continue
                lines.append(f"[{hms(start - lead + rel)}] {text}")
    header = (f"# Transcript — {mdir.name}\n\nEngine: OpenRouter ({model}), {len(starts)} parts of "
              f"{chunk_minutes} min; speaker labels are the model's guesses — check them before the minutes.\n\n")
    out_md.write_text(header + "\n".join(lines) + "\n", encoding="utf-8")
    return out_md


# ------------------------------------------------------------------------------ gemini

def transcribe_gemini(mdir: Path, audio: Path, language: str, env: dict) -> Path:
    out_md = mdir / "transcript.md"
    prompt = GEMINI_PROMPT + (f"\nThe main language is {language}." if language else "")
    cmd = [sys.executable, str(ROOT / "scripts" / "llm_call.py"), "--provider", "gemini",
           "--prompt", prompt, "--file", str(audio), "--out", str(out_md),
           "--meeting", str(mdir), "--purpose", f"transcribe {mdir.name}"]
    print("[transcribe] gemini via llm_call.py (cost logged)", file=sys.stderr)
    subprocess.run(cmd, check=True)
    text = out_md.read_text(encoding="utf-8")
    out_md.write_text(f"# Transcript — {mdir.name}\n\nEngine: Gemini ({env.get('GEMINI_MODEL', '?')}), speaker labels are the model's guesses.\n\n" + text, encoding="utf-8")
    return out_md


def main() -> int:
    prefer_pm_venv()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target", type=Path, help="meeting folder or audio file")
    ap.add_argument("--engine", choices=["local", "gemini", "openrouter"], help="default: TRANSCRIBE_ENGINE in .env, else openrouter when OPENROUTER_API_KEY is set, else local")
    ap.add_argument("--language", help="e.g. fr, en; default: TRANSCRIBE_LANGUAGE in .env, else auto")
    ap.add_argument("--speakers", default="", help="openrouter: the people present, names and roles, for the speaker labels")
    ap.add_argument("--chunk-minutes", type=int, default=20, help="openrouter: length of each audio part (default 20)")
    a = ap.parse_args()
    env = load_env()
    engine = a.engine or env.get("TRANSCRIBE_ENGINE") or ("openrouter" if env.get("OPENROUTER_API_KEY") else "local")
    language = a.language if a.language is not None else env.get("TRANSCRIBE_LANGUAGE", "")
    mdir, audio = find_audio(a.target)
    if engine == "openrouter":
        out = transcribe_openrouter(mdir, audio, language, env, a.speakers, a.chunk_minutes)
    else:
        out = (transcribe_local if engine == "local" else transcribe_gemini)(mdir, audio, language, env)
    n = sum(1 for l in out.read_text(encoding="utf-8").splitlines() if l.startswith("["))
    print(f"transcript → {out} ({n} timed lines, engine {engine})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
