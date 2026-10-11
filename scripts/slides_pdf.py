#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2026 right-on-skill (https://rightonskill.odoo.com/) - gse-light by Nicolas Guelfi (https://github.com/nicolasguelfi/gse-light)
# SPDX-License-Identifier: LicenseRef-PolyForm-Noncommercial-1.0.0  (non-commercial; see LICENSE.md)
"""Render a deck's sources to one PDF, one 1920x1080 page per slide (the `slides` skill, §3).

  python3 ../gse-light/scripts/slides_pdf.py project/meetings/<date>/slides "<title> v<N>.pdf"

Reads <slides>/project/deck.json (order, fonts) and <slides>/project/slides/<id>.html, the sources
the skill keeps in git — sync them from the published artifact first (skill §2.1), so the PDF is the
deck in force. Writes the PDF into <slides>/ under the given name. Speaker notes (<aside>) are left
out. Needs Playwright with its Chromium (`pip install playwright && playwright install chromium`); the
fonts come from Google Fonts, so the machine must be online. The viewer's own base styles are not
public: tables, lists and the `x-shape` arrows are drawn here with styles close to the template's,
so check a few pages before distributing.
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

CSS = """
@page { size: 1920px 1080px; margin: 0 }
html, body { margin: 0; padding: 0; background: #08111F }
section { position: relative; width: 1920px; height: 1080px; box-sizing: border-box; overflow: hidden;
          break-after: page; color: #EEF1F5 }
section aside { display: none }
section p, section h1, section h2, section h3, section ul, section ol { margin: 0 }
section ul, section ol { padding-left: 1.2em }
section table { width: 100%; border-collapse: collapse }
section th { text-align: left; font-weight: 600; color: #F0A35E; padding: 10px 16px; border-bottom: 2px solid #2E3F5E }
section td { padding: 10px 16px; border-bottom: 1px solid #22324F; vertical-align: top }
x-shape { display: block; flex: none }
x-shape[kind="arrow-right"] { clip-path: polygon(0 30%, 60% 30%, 60% 0, 100% 50%, 60% 100%, 60% 70%, 0 70%) }
x-shape[kind="arrow-left"] { clip-path: polygon(100% 30%, 40% 30%, 40% 0, 0 50%, 40% 100%, 40% 70%, 100% 70%) }
"""


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__.strip().split("\n\n")[1], file=sys.stderr)
        return 2
    folder, name = Path(sys.argv[1]), sys.argv[2]
    src = folder / "project"
    deck = json.loads((src / "deck.json").read_text(encoding="utf-8"))
    missing = [i for i in deck["order"] if not (src / "slides" / f"{i}.html").exists()]
    if missing:
        print(f"slides_pdf: missing slide files: {', '.join(missing)}", file=sys.stderr)
        return 1
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("slides_pdf: Playwright is not installed: pip install playwright && playwright install chromium", file=sys.stderr)
        return 1
    fonts = "".join(f'<link rel="stylesheet" href="{f["href"]}">' for f in deck.get("faces", {}).values())
    body = "\n".join((src / "slides" / f"{i}.html").read_text(encoding="utf-8") for i in deck["order"])
    html = f'<!doctype html><html><head><meta charset="utf-8">{fonts}<style>{CSS}</style></head><body>{body}</body></html>'
    out = folder / name
    with tempfile.TemporaryDirectory() as tmp:
        page_file = Path(tmp) / "deck.html"
        page_file.write_text(html, encoding="utf-8")
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1920, "height": 1080})
            page.goto(page_file.as_uri())
            page.wait_for_load_state("networkidle")
            page.evaluate("document.fonts.ready")
            page.pdf(path=str(out), width="1920px", height="1080px", print_background=True,
                     margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
            browser.close()
    print(f"slides_pdf: {out} — {len(deck['order'])} pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
