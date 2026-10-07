#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2026 right-on-skill (https://rightonskill.odoo.com/) - gse-light by Nicolas Guelfi (https://github.com/nicolasguelfi/gse-light)
# SPDX-License-Identifier: LicenseRef-PolyForm-Noncommercial-1.0.0  (non-commercial; see LICENSE.md)
"""One door to the paid models, with a cost line for every call.

Reads the keys from `.env` at the root of the project-management repository (never from the environment of a
Claude session, which is denied that file), calls one provider, prints the answer, and
appends one row to a cost log. Two providers today:

  gemini      Google AI Studio through the `google-genai` package; accepts files
              (audio, PDF, images) uploaded with the Files API.
  openrouter  OpenAI-compatible HTTP API (one key for many vendors); text only.

Usage
-----
  python3 ../gse-light/scripts/llm_call.py --provider gemini --prompt "Summarise this" --file notes.md
  python3 ../gse-light/scripts/llm_call.py --provider openrouter --model openai/gpt-4o-mini --prompt-file p.txt
  python3 ../gse-light/scripts/llm_call.py --provider gemini --prompt "..." --meeting instances/<name>/meetings/2026-10-14 --out minutes-draft.md
  python3 ../gse-light/scripts/llm_call.py --provider gemini --prompt "..." --dry-run      # no network, no cost

Every real call appends: timestamp, provider, model, input tokens, output tokens,
estimated cost (EUR), purpose, output path to `instances/<INSTANCE>/journal/llm-costs.csv`, and, when
`--meeting DIR` is given, one entry to `DIR/cost.json`. Costs are **estimates** from a
small price table (`LLM_PRICES_JSON` in `.env` overrides it); the invoice is the truth.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # the method (gse-light)


def pm_root() -> Path:
    """The project-management repository: GSE_PM_ROOT, else the nearest folder above the
    current directory that holds `instances/` (run the scripts from that repository)."""
    env = os.environ.get("GSE_PM_ROOT")
    if env:
        return Path(env).resolve()
    for d in (Path.cwd().resolve(), *Path.cwd().resolve().parents):
        if (d / "instances").is_dir():
            return d
    sys.exit("no project-management repository found: run this from a folder holding instances/ "
             "(for example ../<project>-pm), or set GSE_PM_ROOT")


PM = pm_root()
COST_LOG: Path  # set after load_env(): the active instance's journal (see instance_dir)
COST_COLUMNS = ["timestamp", "provider", "model", "input_tokens", "output_tokens",
                "est_cost_eur", "purpose", "output"]

# EUR per million tokens (input, output). Rough, dated 2026-10; override in .env.
DEFAULT_PRICES = {
    "gemini-2.5-flash": (0.30, 2.50),
    "gemini-2.5-pro": (1.25, 10.00),
    "openai/gpt-4o-mini": (0.15, 0.60),
}


def load_env(path: Path = PM / ".env") -> dict[str, str]:
    """Parse KEY=VALUE lines; ignore comments and blanks; strip quotes and inline comments."""
    env: dict[str, str] = {}
    if not path.exists():
        return env
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        value = value.split(" #", 1)[0].strip().strip('"').strip("'")
        env[key.strip()] = value
    return env


def instance_dir() -> Path:
    """The active instance's folder: instances/<INSTANCE> of the project-management repository;
    INSTANCE from the environment or .env, else the only folder in instances/."""
    name = os.environ.get("INSTANCE") or load_env().get("INSTANCE")
    if not name:
        found = sorted(p.name for p in (PM / "instances").iterdir() if p.is_dir())
        if len(found) != 1:
            sys.exit(f"set INSTANCE in {PM / '.env'}: instances/ holds {found or 'nothing'}")
        name = found[0]
    path = PM / "instances" / name
    if not path.is_dir():
        sys.exit(f"unknown instance {name!r}: no folder {path.relative_to(PM)} (set INSTANCE in .env)")
    return path


COST_LOG = instance_dir() / "journal" / "llm-costs.csv"


def prices(env: dict[str, str]) -> dict[str, tuple[float, float]]:
    table = dict(DEFAULT_PRICES)
    if env.get("LLM_PRICES_JSON"):
        try:
            table.update({k: tuple(v) for k, v in json.loads(env["LLM_PRICES_JSON"]).items()})
        except (json.JSONDecodeError, TypeError, ValueError) as e:
            print(f"warning: LLM_PRICES_JSON ignored ({e})", file=sys.stderr)
    return table


def estimate(model: str, tin: int, tout: int, table: dict) -> float | None:
    if model not in table:
        return None
    pin, pout = table[model]
    return round((tin * pin + tout * pout) / 1_000_000, 4)


def log_cost(row: dict, meeting: Path | None) -> None:
    COST_LOG.parent.mkdir(parents=True, exist_ok=True)
    new = not COST_LOG.exists()
    with COST_LOG.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COST_COLUMNS)
        if new:
            w.writeheader()
        w.writerow(row)
    if meeting:
        meeting.mkdir(parents=True, exist_ok=True)
        cj = meeting / "cost.json"
        calls = json.loads(cj.read_text(encoding="utf-8")) if cj.exists() else []
        calls.append(row)
        cj.write_text(json.dumps(calls, indent=2, ensure_ascii=False), encoding="utf-8")


# ----------------------------------------------------------------------------- providers

def call_gemini(env: dict, model: str, prompt: str, system: str | None,
                files: list[Path]) -> tuple[str, int, int]:
    try:
        from google import genai  # type: ignore
        from google.genai import types  # type: ignore
    except ImportError:
        sys.exit("google-genai is not installed: `uv pip install google-genai` (or pip) in the Python you run this with")
    key = env.get("GOOGLE_API_KEY")
    if not key:
        sys.exit("GOOGLE_API_KEY missing in .env")
    client = genai.Client(api_key=key)
    contents: list = []
    for path in files:
        up = client.files.upload(file=str(path))
        # Large files (audio) are processed asynchronously; wait until ACTIVE.
        while getattr(up, "state", None) and str(up.state).endswith("PROCESSING"):
            time.sleep(3)
            up = client.files.get(name=up.name)
        if getattr(up, "state", None) and str(up.state).endswith("FAILED"):
            sys.exit(f"upload failed for {path}")
        contents.append(up)
    contents.append(prompt)
    config = types.GenerateContentConfig(system_instruction=system) if system else None
    resp = client.models.generate_content(model=model, contents=contents, config=config)
    usage = getattr(resp, "usage_metadata", None)
    tin = int(getattr(usage, "prompt_token_count", 0) or 0)
    tout = int(getattr(usage, "candidates_token_count", 0) or 0)
    return resp.text or "", tin, tout


def call_openrouter(env: dict, model: str, prompt: str, system: str | None,
                    files: list[Path]) -> tuple[str, int, int]:
    if files:
        sys.exit("openrouter: files are not supported by this helper (text only); use --provider gemini")
    key = env.get("OPENROUTER_API_KEY")
    if not key:
        sys.exit("OPENROUTER_API_KEY missing in .env")
    base = env.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1").rstrip("/")
    messages = ([{"role": "system", "content": system}] if system else []) + [
        {"role": "user", "content": prompt}]
    body = json.dumps({"model": model, "messages": messages}).encode()
    req = urllib.request.Request(f"{base}/chat/completions", data=body, headers={
        "Authorization": f"Bearer {key}", "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/nicolasguelfi/gse-light", "X-Title": "gse-light Project Advisor kit"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            data = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        sys.exit(f"openrouter HTTP {e.code}: {e.read().decode()[:500]}")
    text = data["choices"][0]["message"]["content"]
    usage = data.get("usage", {})
    return text, int(usage.get("prompt_tokens", 0)), int(usage.get("completion_tokens", 0))


PROVIDERS = {"gemini": call_gemini, "openrouter": call_openrouter}
DEFAULT_MODEL_VAR = {"gemini": "GEMINI_MODEL", "openrouter": "OPENROUTER_MODEL"}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--provider", required=True, choices=sorted(PROVIDERS))
    ap.add_argument("--model", help="defaults to GEMINI_MODEL / OPENROUTER_MODEL from .env")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--prompt")
    g.add_argument("--prompt-file", type=Path)
    ap.add_argument("--system", help="system instruction (text)")
    ap.add_argument("--file", type=Path, action="append", default=[], help="file to attach (gemini only); repeatable")
    ap.add_argument("--out", type=Path, help="write the answer here instead of stdout")
    ap.add_argument("--meeting", type=Path, help="meeting folder: also append the cost to its cost.json")
    ap.add_argument("--purpose", default="", help="free text for the cost log")
    ap.add_argument("--dry-run", action="store_true", help="show what would be sent; no network, no cost")
    a = ap.parse_args()

    env = load_env()
    model = a.model or env.get(DEFAULT_MODEL_VAR[a.provider]) or ""
    if not model and not a.dry_run:
        sys.exit(f"no model: pass --model or set {DEFAULT_MODEL_VAR[a.provider]} in .env")
    model = model or "(unset)"
    prompt = a.prompt if a.prompt is not None else a.prompt_file.read_text(encoding="utf-8")
    for f in a.file:
        if not f.exists():
            sys.exit(f"file not found: {f}")

    if a.dry_run:
        print(json.dumps({"provider": a.provider, "model": model, "prompt_chars": len(prompt),
                          "files": [str(f) for f in a.file], "system": bool(a.system),
                          "key_present": bool(env.get("GOOGLE_API_KEY" if a.provider == "gemini" else "OPENROUTER_API_KEY")),
                          "cost_log": str(COST_LOG.relative_to(PM))}, indent=2))
        return 0

    text, tin, tout = PROVIDERS[a.provider](env, model, prompt, a.system, a.file)
    if a.out:
        a.out.parent.mkdir(parents=True, exist_ok=True)
        a.out.write_text(text, encoding="utf-8")
    else:
        print(text)
    cost = estimate(model, tin, tout, prices(env))
    row = {"timestamp": dt.datetime.now().isoformat(timespec="seconds"), "provider": a.provider,
           "model": model, "input_tokens": tin, "output_tokens": tout,
           "est_cost_eur": "" if cost is None else cost, "purpose": a.purpose,
           "output": str(a.out) if a.out else "stdout"}
    log_cost(row, a.meeting)
    print(f"[llm_call] {a.provider} {model} in={tin} out={tout} "
          f"est_cost_eur={'n/a (model not in price table)' if cost is None else cost} "
          f"→ {COST_LOG.relative_to(PM)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
