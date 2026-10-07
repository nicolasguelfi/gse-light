#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2026 Nicolas Guelfi - gse-light (https://github.com/nicolasguelfi/gse-light)
# SPDX-License-Identifier: LicenseRef-PolyForm-Noncommercial-1.0.0  (non-commercial; see LICENSE.md)
"""Transcribe a meeting recording: locally by default, with Gemini on request.

  python3 ../gse-light/scripts/meeting/transcribe.py instances/<name>/meetings/2026-10-14            # engine from .env (default local)
  python3 ../gse-light/scripts/meeting/transcribe.py instances/<name>/meetings/2026-10-14 --engine gemini
  python3 ../gse-light/scripts/meeting/transcribe.py path/to/audio.m4a --language fr

Engines
  local   mlx-whisper (Apple Silicon, fast) if installed, else whisper.cpp's `whisper-cli`.
          Nothing leaves the machine. No speaker labels. Install once, outside Dropbox:
              uv tool install mlx-whisper        # then the model downloads on first run (~1.6 GB)
          or  brew install whisper-cpp           # and set WHISPER_CPP_MODEL to a ggml model file
  gemini  Google AI Studio (GOOGLE_API_KEY in .env) through scripts/llm_call.py: the audio
          is uploaded; the model returns a transcript with timestamps and speaker labels.
          The cost line goes to instances/<INSTANCE>/journal/llm-costs.csv and <meeting>/cost.json.

Output, next to the audio: transcript.md (one paragraph per segment, [hh:mm:ss] prefix),
plus transcript.srt and transcript.json for the local engine.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from llm_call import load_env  # noqa: E402

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
    """Return (meeting_dir, audio_file) from a folder or a file path."""
    if target.is_dir():
        cands = sorted(p for p in target.iterdir() if p.suffix.lower() in AUDIO_EXT)
        if not cands:
            sys.exit(f"no audio file in {target} (expected one of {', '.join(AUDIO_EXT)})")
        return target, cands[0]
    if target.suffix.lower() in AUDIO_EXT and target.exists():
        return target.parent, target
    sys.exit(f"not a meeting folder nor an audio file: {target}")


# ------------------------------------------------------------------------------- local

def local_engine() -> tuple[str, str] | None:
    if shutil.which("mlx_whisper"):
        return "mlx_whisper", shutil.which("mlx_whisper")
    if shutil.which("whisper-cli"):
        return "whisper-cli", shutil.which("whisper-cli")
    return None


def transcribe_local(mdir: Path, audio: Path, language: str, env: dict) -> Path:
    eng = local_engine()
    if not eng:
        sys.exit("no local engine. Install once (outside Dropbox):\n"
                 "  uv tool install mlx-whisper      (Apple Silicon; model downloads on first run)\n"
                 "  or: brew install whisper-cpp     (then WHISPER_CPP_MODEL=/path/to/ggml-large-v3-turbo.bin in .env)\n"
                 "Or run with --engine gemini.")
    name, exe = eng
    out_md = mdir / "transcript.md"
    if name == "mlx_whisper":
        model = env.get("WHISPER_MODEL", "mlx-community/whisper-large-v3-turbo")
        cmd = [exe, str(audio), "--model", model, "--output-dir", str(mdir), "--output-format", "all"]
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
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("target", type=Path, help="meeting folder or audio file")
    ap.add_argument("--engine", choices=["local", "gemini"], help="default: TRANSCRIBE_ENGINE in .env, else local")
    ap.add_argument("--language", help="e.g. fr, en; default: TRANSCRIBE_LANGUAGE in .env, else auto")
    a = ap.parse_args()
    env = load_env()
    engine = a.engine or env.get("TRANSCRIBE_ENGINE") or "local"
    language = a.language if a.language is not None else env.get("TRANSCRIBE_LANGUAGE", "")
    mdir, audio = find_audio(a.target)
    out = (transcribe_local if engine == "local" else transcribe_gemini)(mdir, audio, language, env)
    n = sum(1 for l in out.read_text(encoding="utf-8").splitlines() if l.startswith("["))
    print(f"transcript → {out} ({n} timed lines, engine {engine})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
