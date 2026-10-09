#!/usr/bin/env python3
"""review_board.py — a review board: proposals → the person's choice → one line to paste back.

Builds a self-contained HTML page (media inlined as data URIs, no network, no server) that
presents N proposals grouped by subject, lets the person tick what they keep, writes a
comment under every proposal, every subject and the whole board, and composes at the
bottom of the screen **the answer line** they copy with one click and paste into the
conversation. The page is the form; the conversation stays the channel of record.

Input: a JSON specification (see --example). Output: one or more .html files.

    python3 .claude/skills/review/review_board.py spec.json -o board.html --fragment
    python3 .claude/skills/review/review_board.py spec.json -o board.html --per-page 4   # default: 8 per page
    python3 .claude/skills/review/review_board.py spec.json -o board.html --lang fr      # French labels
    python3 .claude/skills/review/review_board.py --example > spec.json

Specification
-------------
{
  "title":   "Where the tests run",            # title + <title>
  "eyebrow": "project · design phase",         # small line above the title (page number added)
  "intro":   "…",                              # the instructions frame; the only field that accepts HTML
  "prefix":  "r1",                             # head of the copied line
  "mode":    "single",                         # single = radio (one per subject) | multi = checkboxes
  "groups": [{
     "key": "runner",                          # what appears in the copied line (unique per page)
     "heading": "1. Where the tests run", "meta": "design",
     "notes":   [{"label":"Problem","text":"…","tone":"accent"},
                 {"label":"Measured","text":"…"}],
     "recommend": "p1: …",                     # the recommended answer, one sentence, always
     "details": [{"summary":"Specification","text":"…","open":true}],
     "items":   [{"label":"p1","title":"Proposal 1","meta":"~20 min",
                  "facts":"who does it · cost",
                  "pros":["…"], "cons":["…"], "recommended":true,
                  "media":"/path/a.png", "caption":"…"}]
  }]
}

Comments: a free field per SUBJECT (group) AND a field per PROPOSAL (item), plus a GLOBAL
field at the end — all three carried into the copied line. A proposal commented but not
ticked appears as `!label«…»`. `"comment": false` (group or item) removes the field, only
on the person's explicit request.

`media` accepts .mp3/.wav/.m4a (audio player), .png/.jpg/.webp/.gif (thumbnail + zoom),
.mp4/.webm (video player), or nothing at all (a purely textual proposal).

`notes`, `facts`, `details` and `meta` are HTML-escaped: write them in plain text.
"""
from __future__ import annotations

import argparse
import base64
import html
import json
import mimetypes
import os

AUDIO = {".mp3", ".wav", ".m4a", ".ogg", ".flac", ".aac"}
IMAGE = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".avif"}
VIDEO = {".mp4", ".webm", ".mov"}

# User-interface labels, by language. The person's language, not the author's.
LABELS = {
    "en": {
        "keep": "Keep", "recommended": "recommended", "recommendation": "Recommendation",
        "item_note": "comment on this proposal (optional)",
        "group_note": "comment on this subject (optional — carried into the copied line)",
        "global_title": "Global comment",
        "global_note": "global comment on the whole board (optional — carried into the copied line)",
        "select_all": "select all",
        "select_all_title": "tick every proposal of the subject — click again to untick them",
        "speed": "speed",
        "tick_reco": "Tick the recommendations",
        "tick_reco_title": "tick every recommended proposal of the page — click again to untick them",
        "untick": "Untick all", "copy": "Copy my answer",
        "copied": "Copied — paste it into the conversation",
        "hint": "Tick what you keep, write your comments, then copy the line.",
        "page": "page {page} of {pages}",
    },
    "fr": {
        "keep": "Retenir", "recommended": "recommandé", "recommendation": "Recommandation",
        "item_note": "commentaire sur cette proposition (facultatif)",
        "group_note": "commentaire sur ce sujet (facultatif — repris dans la ligne copiée)",
        "global_title": "Commentaire global",
        "global_note": "commentaire global sur toute la planche (facultatif — repris dans la ligne copiée)",
        "select_all": "tout sélectionner",
        "select_all_title": "cocher toutes les propositions du sujet — re-cliquer pour tout décocher",
        "speed": "vitesse",
        "tick_reco": "Cocher les recommandations",
        "tick_reco_title": "cocher toutes les propositions recommandées de la page — re-cliquer pour les décocher",
        "untick": "Tout décocher", "copy": "Copier ma sélection",
        "copied": "Copié — colle-le dans la discussion",
        "hint": "Coche ce que tu retiens, écris tes commentaires, puis copie la ligne.",
        "page": "page {page} sur {pages}",
    },
}

CSS = """
:root{
  --ground:#f6f5f1;--panel:#fffefb;--line:#ddd9cf;--line-soft:#eae6dc;--sunk:#efece4;
  --ink:#1d211f;--ink-2:#4b524e;--ink-3:#7c837e;
  --accent:#2f6b5c;--accent-soft:#e3ede9;--accent-ink:#fff;
  --warn:#8a5a2b;--warn-soft:#f3e8d9;
  --serif:"Iowan Old Style","Palatino Linotype",Palatino,"Book Antiqua",Georgia,serif;
  --sans:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
  --mono:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,monospace;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --ground:#14181a;--panel:#1b2022;--line:#2c3336;--line-soft:#232a2c;--sunk:#111517;
  --ink:#e8e6e0;--ink-2:#aeb4b1;--ink-3:#7b827f;
  --accent:#6fb9a4;--accent-soft:#1f2f2b;--accent-ink:#0d1412;
  --warn:#d3a06a;--warn-soft:#2e2519;color-scheme:dark}}
:root[data-theme="dark"]{--ground:#14181a;--panel:#1b2022;--line:#2c3336;--line-soft:#232a2c;
  --sunk:#111517;--ink:#e8e6e0;--ink-2:#aeb4b1;--ink-3:#7b827f;
  --accent:#6fb9a4;--accent-soft:#1f2f2b;--accent-ink:#0d1412;--warn:#d3a06a;--warn-soft:#2e2519;color-scheme:dark}

*{box-sizing:border-box}
body{margin:0;background:var(--ground);color:var(--ink);font-family:var(--sans);
     font-size:16px;line-height:1.55;-webkit-font-smoothing:antialiased}
.wrap{max-width:70rem;margin:0 auto;padding:2.5rem 1.25rem 7rem;
      display:flex;flex-direction:column;gap:1.4rem}
header{display:flex;flex-direction:column;gap:.45rem;border-bottom:1px solid var(--line);
       padding-bottom:1.15rem}
.eyebrow{font-size:.72rem;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-3);
         font-weight:600}
h1{font-family:var(--serif);font-weight:600;font-size:clamp(1.9rem,4vw,2.6rem);line-height:1.1;
   margin:0;text-wrap:balance}
.sub{color:var(--ink-2);font-size:.95rem}
.sub b{color:var(--ink);font-weight:600}
h2{font-family:var(--serif);font-size:1.35rem;font-weight:600;margin:.9rem 0 -.3rem;
   display:flex;align-items:baseline;gap:.6rem;flex-wrap:wrap}
h2 .m{font-family:var(--mono);font-size:.75rem;color:var(--ink-3);font-weight:400}
h2 .selall{font-family:var(--sans);font-size:.72rem;font-weight:600;
   padding:.2rem .6rem;margin-left:auto;align-self:center}

.note{border-radius:4px;padding:.85rem 1.05rem;font-size:.9rem;
      background:var(--warn-soft);border:1px solid var(--warn)}
.note b{color:var(--warn)}
.note.accent{background:var(--accent-soft);border-color:var(--accent)}
.note.accent b{color:var(--accent)}
details{border:1px solid var(--line-soft);border-radius:4px;background:var(--panel)}
summary{cursor:pointer;padding:.5rem .85rem;font-size:.85rem;font-weight:600;color:var(--ink-2)}
details p{margin:0;padding:0 .95rem .85rem;font-size:.9rem;color:var(--ink-2);
          font-family:var(--serif);white-space:pre-wrap}

.grid{display:grid;gap:1rem;grid-template-columns:repeat(4,minmax(0,1fr))}
@media(max-width:64rem){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:40rem){.grid{grid-template-columns:1fr}}
.rates{display:flex;align-items:center;gap:.35rem;font-size:.8rem;color:var(--ink-3)}
.rates button.on{border-color:var(--accent);color:var(--accent)}
.card,.clip{background:var(--panel);border:1px solid var(--line);border-radius:4px;
            display:flex;flex-direction:column;overflow:hidden}
.card.on,.clip.on{border-color:var(--accent);box-shadow:0 0 0 1px var(--accent)}
.clip{padding:.75rem .9rem;gap:.5rem}
.clip-head{display:flex;align-items:baseline;gap:.6rem;flex-wrap:wrap}
.tag{font-family:var(--mono);font-size:.72rem;color:var(--ink-3)}
.ttl{font-weight:600;font-size:.92rem}
.dur{margin-left:auto;font-family:var(--mono);font-size:.75rem;color:var(--ink-3)}
audio,video{width:100%;display:block}
video{border-radius:3px;background:#000}
.shot{display:block;width:100%;aspect-ratio:4/3;background:var(--sunk);cursor:zoom-in;
      border:0;padding:0}
.shot img{width:100%;height:100%;object-fit:cover;display:block}
.facts{font-size:.78rem;color:var(--ink-3);font-family:var(--mono);line-height:1.45}
.pc{display:flex;flex-direction:column;gap:.2rem;font-size:.82rem;line-height:1.4;margin:.35rem 0}
.pc .pro::before{content:'+ ';color:var(--accent);font-weight:700}.pc .con::before{content:'− ';color:var(--warn);font-weight:700}
.reco{display:inline-block;margin-left:.5rem;padding:.05rem .45rem;border-radius:999px;background:var(--accent);color:var(--accent-ink);font-size:.7rem;font-weight:700;letter-spacing:.04em;text-transform:uppercase}
.note.reco-note{border-width:2px}
.body{padding:.7rem .85rem;display:flex;flex-direction:column;gap:.45rem;flex:1}
.pick{display:flex;align-items:center;gap:.45rem;font-size:.85rem;font-weight:600;
      color:var(--ink-2);cursor:pointer;user-select:none}
.pick input{accent-color:var(--accent);width:1.05rem;height:1.05rem;cursor:pointer}
.card.on .pick,.clip.on .pick{color:var(--accent)}

.bar{position:fixed;left:0;right:0;bottom:0;background:var(--panel);
     border-top:1px solid var(--line);padding:.75rem 1.25rem;z-index:20;
     padding-bottom:calc(.75rem + env(safe-area-inset-bottom, 0px))}
.bar-in{max-width:70rem;margin:0 auto;width:100%;display:flex;align-items:center;gap:.9rem;
        flex-wrap:wrap}
.pick-txt{font-family:var(--mono);font-size:.85rem;flex:1 1 16rem;min-width:0;
          overflow-x:auto;white-space:nowrap}
.pick-txt em{color:var(--ink-3);font-style:normal}
button{font-family:var(--sans);font-size:.85rem;font-weight:600;border-radius:3px;
       padding:.45rem .85rem;cursor:pointer;border:1px solid var(--line);
       background:transparent;color:var(--ink-2)}
button:hover{border-color:var(--ink-3);color:var(--ink)}
button.primary{background:var(--accent);border-color:var(--accent);color:var(--accent-ink)}
button.primary:hover{opacity:.9;color:var(--accent-ink)}
button:disabled{opacity:.45;cursor:default}
button:focus-visible{outline:2px solid var(--accent);outline-offset:2px}

.gnote{width:100%;margin:.4rem 0 0;padding:.45rem .7rem;border:1px solid var(--line-soft);border-radius:4px;background:var(--panel);color:var(--ink);font-size:.9rem}
.inote{width:100%;margin:.15rem 0 0;padding:.3rem .55rem;border:1px solid var(--line-soft);border-radius:4px;background:var(--sunk);color:var(--ink);font-size:.8rem}
dialog{border:none;padding:0;background:transparent;max-width:96vw;max-height:96vh}
dialog::backdrop{background:rgba(10,12,12,.86)}
dialog img{max-width:96vw;max-height:88vh;display:block;margin:0 auto;cursor:zoom-out}
dialog .cap{color:#d8d5cd;font-size:.85rem;text-align:center;padding:.6rem;font-family:var(--mono)}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
"""

JS = """
const KEYS=%(keys)s, PREFIX=%(prefix)s;
let RATE=%(rate)s;
function applyRate(){document.querySelectorAll('audio,video').forEach(m=>m.playbackRate=RATE);
  document.querySelectorAll('.rates button').forEach(b=>b.classList.toggle('on',parseFloat(b.dataset.rate)===RATE));}
document.addEventListener('play',e=>{if(e.target.playbackRate!==RATE)e.target.playbackRate=RATE;},true);
document.querySelectorAll('.rates button').forEach(b=>b.addEventListener('click',()=>{RATE=parseFloat(b.dataset.rate);applyRate();}));
applyRate();
const out=document.getElementById('pick'), btn=document.getElementById('copy');
function refresh(){
  document.querySelectorAll('[data-holder]').forEach(el=>{
    const i=el.querySelector('input'); el.classList.toggle('on', !!(i&&i.checked));});
  const parts=[];
  KEYS.forEach(k=>{
    const seg=[];
    document.querySelectorAll('input[data-k="'+k+'"]').forEach(i=>{
      const nEl=document.querySelector('input[data-inote="'+k+'::'+i.dataset.label+'"]');
      const note=nEl&&nEl.value.trim()?'«'+nEl.value.trim()+'»':'';
      if(i.checked) seg.push(i.dataset.label+note);
      else if(note) seg.push('!'+i.dataset.label+note);
    });
    const nEl=document.querySelector('input[data-note="'+k+'"]');
    const note=nEl&&nEl.value.trim()?' «'+nEl.value.trim()+'»':'';
    if(seg.length||note) parts.push(k+'='+(seg.join('+')||'?')+note);
  });
  const gEl=document.getElementById('gnote'); const gv=gEl&&gEl.value.trim();
  if(gv) parts.push('global«'+gv+'»');
  window.__sel=(PREFIX?PREFIX+'  ':'')+parts.join('  ');
  out.innerHTML=parts.length
    ? (PREFIX?'<b>'+PREFIX+'</b>  ':'')+parts.join('   ')
    : '<em>%(hint)s</em>';
  btn.disabled=!parts.length;
}
document.addEventListener('change',e=>{if(e.target.matches('input[data-k]'))refresh();});
document.addEventListener('input',e=>{if(e.target.matches('input[data-note],input[data-inote],#gnote'))refresh();});
document.getElementById('clear').addEventListener('click',()=>{
  document.querySelectorAll('input[data-k]').forEach(i=>i.checked=false); refresh();});
const recoBtn=document.getElementById('reco-all');
if(recoBtn){const recos=()=>[...document.querySelectorAll('input[data-k][data-reco="1"]')];
  if(!recos().length) recoBtn.hidden=true;
  recoBtn.addEventListener('click',()=>{const ins=recos(); const all=ins.every(i=>i.checked);
    ins.forEach(i=>i.checked=!all); refresh();});}
document.querySelectorAll('[data-all]').forEach(b=>b.addEventListener('click',()=>{
  const ins=[...document.querySelectorAll('input[data-k="'+b.dataset.all+'"]')];
  const all=ins.length&&ins.every(i=>i.checked);
  ins.forEach(i=>i.checked=!all); refresh();}));
btn.addEventListener('click',async()=>{
  try{await navigator.clipboard.writeText(window.__sel);}
  catch(e){const t=document.createElement('textarea');t.value=window.__sel;
    document.body.appendChild(t);t.select();document.execCommand('copy');t.remove();}
  const o=btn.textContent;btn.textContent=%(copied)s;
  setTimeout(()=>btn.textContent=o,2600);});
const dlg=document.getElementById('zoom');
if(dlg) document.querySelectorAll('.shot').forEach(s=>s.addEventListener('click',()=>{
  dlg.querySelector('img').src=s.querySelector('img').src;
  dlg.querySelector('.cap').textContent=s.dataset.cap||''; dlg.showModal();}));
if(dlg) dlg.addEventListener('click',()=>dlg.close());
refresh();
"""

EXAMPLE = {
    "title": "Where the end-to-end tests run",
    "eyebrow": "project · design phase · board r1",
    "intro": "<b>What you must do</b>: tick one proposal per subject, write a comment under any "
             "point and a global comment, then <b>Copy my answer</b> and paste the line into the "
             "conversation. <b>What your choice triggers</b>: nothing before your line comes back; "
             "then the design record is written and the pipeline configured. <b>What is not "
             "chosen</b> stays in the record as a rejected option, with its reasons.",
    "prefix": "r1",
    "mode": "single",
    "groups": [{
        "key": "runner",
        "heading": "1. Where the end-to-end tests run", "meta": "design",
        "notes": [{"label": "Problem", "tone": "accent",
                   "text": "End-to-end tests drive the real interface; they need a browser and the "
                           "running system. Where they run decides their cost and their credibility."},
                  {"label": "Measured",
                   "text": "The CI runs gates.sh in 4 minutes today; no browser installed."}],
        "recommend": "p1: in the CI on every pull request; the gate stays green or the change waits.",
        "items": [
            {"label": "p1", "title": "In the CI, on every pull request", "meta": "~1 h to set up",
             "facts": "Ask Claude · a browser in the CI image",
             "pros": ["every change proven on the real interface", "no one has to remember to run them"],
             "cons": ["adds minutes to each run", "a flaky test blocks everyone until fixed"],
             "recommended": True},
            {"label": "p2", "title": "On each developer's machine before a pull request", "meta": "0 min",
             "facts": "Person · by discipline",
             "pros": ["nothing to set up"],
             "cons": ["skipped under pressure; no record that they ran"]},
        ],
    }],
}


def esc(s):
    return html.escape(str(s or ""), quote=True)


def data_uri(path, max_px=0):
    """Encode a media file as a data URI. For an image, `max_px` makes a reduced PREVIEW;
    the file on disk keeps its full resolution."""
    if max_px and os.path.splitext(path)[1].lower() in IMAGE:
        try:
            from io import BytesIO

            from PIL import Image
        except ImportError:
            max_px = 0
        else:
            im = Image.open(path)
            im.thumbnail((max_px, max_px), Image.LANCZOS)
            buf = BytesIO()
            im.convert("RGB").save(buf, "JPEG", quality=85, optimize=True)
            blob = buf.getvalue()
            return "data:image/jpeg;base64," + base64.b64encode(blob).decode(), len(blob)
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    with open(path, "rb") as f:
        blob = f.read()
    return f"data:{mime};base64," + base64.b64encode(blob).decode(), len(blob)


def render_item(it, key, mode, L, max_px=0):
    """One proposal: inline media + facts + advantages and drawbacks + the tick that keeps it
    + its own comment field."""
    media, kind = it.get("media"), None
    uri = ""
    if media:
        ext = os.path.splitext(media)[1].lower()
        kind = "audio" if ext in AUDIO else "image" if ext in IMAGE else \
               "video" if ext in VIDEO else None
        if kind is None:
            raise SystemExit(f"unsupported media extension: {media}")
        if not os.path.exists(media):
            raise SystemExit(f"media not found: {media}")
        uri, _ = data_uri(media, max_px)

    facts = list(filter(None, [it.get("facts", "")]))
    inp = (f'<input type="{"radio" if mode == "single" else "checkbox"}" '
           f'name="g-{esc(key)}" data-k="{esc(key)}" data-label="{esc(it["label"])}"'
           + (' data-reco="1"' if it.get("recommended") else "") + '>')
    head = (f'<div class="clip-head"><span class="tag">{esc(key)}</span>'
            f'<span class="ttl">{esc(it.get("title", it["label"]))}</span>'
            + (f'<span class="reco">{esc(L["recommended"])}</span>' if it.get("recommended") else "")
            + (f'<span class="dur">{esc(it["meta"])}</span>' if it.get("meta") else "")
            + '</div>')
    pick = f'<label class="pick">{inp} {esc(it.get("pick_label", L["keep"]))}</label>'
    facts_html = f'<div class="facts">{esc(" · ".join(facts))}</div>' if facts else ""
    pros = it.get("pros") or []; cons = it.get("cons") or []
    if isinstance(pros, str): pros = [pros]
    if isinstance(cons, str): cons = [cons]
    if pros or cons:
        facts_html += ('<div class="pc">' + "".join(f'<span class="pro">{esc(x)}</span>' for x in pros)
                       + "".join(f'<span class="con">{esc(x)}</span>' for x in cons) + '</div>')
    inote = (f'<input type="text" class="inote" '
             f'data-inote="{esc(key)}::{esc(it["label"])}" '
             f'placeholder="{esc(L["item_note"])}">'
             if it.get("comment", True) else "")

    if kind == "image":
        return (f'<div class="card" data-holder>'
                f'<button class="shot" data-cap="{esc(it.get("caption", ""))}">'
                f'<img src="{uri}" alt="{esc(it.get("caption", it["label"]))}" loading="lazy">'
                f'</button><div class="body">{head}{facts_html}{pick}{inote}</div></div>')
    player = ""
    if kind == "audio":
        player = f'<audio controls preload="metadata" src="{uri}"></audio>'
    elif kind == "video":
        player = f'<video controls preload="metadata" src="{uri}"></video>'
    return f'<section class="clip" data-holder>{head}{player}{facts_html}{pick}{inote}</section>'


def render_group(g, mode, L, max_px=0):
    o = [f'<h2>{esc(g["heading"])}'
         + (f'<span class="m">{esc(g["meta"])}</span>' if g.get("meta") else "")
         + (f'<button type="button" class="selall" data-all="{esc(g["key"])}" '
            f'title="{esc(L["select_all_title"])}">{esc(L["select_all"])}</button>'
            if mode == "multi" else "")
         + '</h2>']
    for n in g.get("notes", []):
        tone = " accent" if n.get("tone") == "accent" else ""
        o.append(f'<div class="note{tone}"><b>{esc(n.get("label", ""))}</b> {esc(n["text"])}</div>')
    if g.get("recommend"):
        o.append(f'<div class="note accent reco-note"><b>{esc(L["recommendation"])}</b> {esc(g["recommend"])}</div>')
    for d in g.get("details", []):
        op = " open" if d.get("open") else ""
        o.append(f'<details{op}><summary>{esc(d["summary"])}</summary>'
                 f'<p>{esc(d["text"])}</p></details>')
    items = "".join(render_item(it, g["key"], mode, L, max_px) for it in g["items"])
    kinds = {os.path.splitext(it.get("media", ""))[1].lower() for it in g["items"]}
    o.append(f'<div class="grid">{items}</div>' if kinds & (IMAGE | AUDIO | VIDEO) else items)
    if g.get("comment", True):
        o.append(f'<input type="text" class="gnote" data-note="{esc(g["key"])}" '
                 f'placeholder="{esc(L["group_note"])}">')
    return "\n".join(o)


def render_page(spec, groups, L, lang, page=None, pages=None, max_px=0, fragment=False):
    """Render one page. `fragment` produces the content ALONE, publishable as an artifact
    (the artifact wraps the file in its own doctype, head and body; the <title> stays)."""
    mode = spec.get("mode", "single")
    eyebrow = spec.get("eyebrow", "")
    if pages and pages > 1:
        eyebrow = f"{eyebrow} · {L['page'].format(page=page, pages=pages)}".lstrip(" ·")
    title = spec.get("title", "Review")
    heads = " · ".join(g["heading"] for g in groups)
    has_media = any(it.get("media") for g in groups for it in g["items"])
    js = JS % {"keys": json.dumps([g["key"] for g in groups], ensure_ascii=False),
               "prefix": json.dumps(spec.get("prefix", ""), ensure_ascii=False),
               "rate": json.dumps(spec.get("rate", 1.0)),
               "hint": esc(spec.get("hint", L["hint"])),
               "copied": json.dumps(L["copied"], ensure_ascii=False)}
    head = (f'<title>{esc(title)}{f" {page}/{pages}" if pages and pages > 1 else ""}</title>\n'
            f'<style>{CSS}</style>')
    rates = (f'<span class="rates">{esc(L["speed"])} <button type="button" data-rate="1">1×</button>'
             f'<button type="button" data-rate="1.5">1.5×</button><button type="button" data-rate="2">2×</button></span>'
             if has_media else "")
    body = f"""<div class="wrap">
 <header><div class="eyebrow">{esc(eyebrow)}</div>
 <h1>{esc(heads) if len(groups) <= 6 else esc(title)}</h1>
 <div class="sub">{spec.get("intro", "")}</div></header>
{chr(10).join(render_group(g, mode, L, max_px) for g in groups)}
 <section class="group"><h2>{esc(L["global_title"])}</h2>
 <input type="text" id="gnote" class="gnote" placeholder="{esc(L["global_note"])}"></section>
</div>
<div class="bar"><div class="bar-in">
  <div class="pick-txt" id="pick"></div>
  {rates}
  <button id="reco-all" type="button" title="{esc(L["tick_reco_title"])}">{esc(L["tick_reco"])}</button>
  <button id="clear">{esc(L["untick"])}</button>
  <button id="copy" class="primary" disabled>{esc(L["copy"])}</button>
</div></div>
<dialog id="zoom"><img alt=""><div class="cap"></div></dialog>
<script>{js}</script>"""
    if fragment:
        return head + "\n" + body + "\n"
    return (f'<!doctype html>\n<html lang="{lang}"><head><meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">\n'
            f'{head}</head><body>\n{body}\n</body></html>\n')


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec", nargs="?", help="the JSON specification")
    ap.add_argument("-o", "--out", help="the .html file to write")
    ap.add_argument("--per-page", type=int, default=8,
                    help="subjects per page (0 = everything on one page); suffix -1, -2 … "
                         "past 8 a page with media gets heavy and slow to open")
    ap.add_argument("--fragment", action="store_true",
                    help="content ALONE, without doctype/html/head/body — to publish as an "
                         "artifact (the panel next to the conversation)")
    ap.add_argument("--lang", default="en", choices=sorted(LABELS),
                    help="language of the page's buttons and fields (default: en)")
    ap.add_argument("--max-px", type=int, default=1400,
                    help="longest side of the inlined image PREVIEWS (0 = full size); "
                         "the file on disk is never touched")
    ap.add_argument("--max-mb", type=float, default=18.0,
                    help="warn when a page is larger than this (default 18 MB)")
    ap.add_argument("--example", action="store_true", help="print an example specification")
    a = ap.parse_args()

    if a.example:
        print(json.dumps(EXAMPLE, ensure_ascii=False, indent=2))
        return
    if not a.spec or not a.out:
        ap.error("spec and --out are required (or --example)")

    with open(a.spec, encoding="utf-8") as f:
        spec = json.load(f)
    groups = spec["groups"]
    keys = [g["key"] for g in groups]
    dupes = sorted({k for k in keys if keys.count(k) > 1})
    if dupes:
        raise SystemExit(f"duplicate subject keys (the copied line would be ambiguous): {dupes}")
    L = LABELS[a.lang]

    n = a.per_page or len(groups)
    chunks = [groups[i:i + n] for i in range(0, len(groups), n)]
    base, ext = os.path.splitext(a.out)
    for i, ch in enumerate(chunks, 1):
        out = a.out if len(chunks) == 1 else f"{base}-{i}{ext}"
        page = render_page(spec, ch, L, a.lang, i, len(chunks), a.max_px, a.fragment)
        with open(out, "w", encoding="utf-8") as f:
            f.write(page)
        mb = os.path.getsize(out) / 1e6
        flag = "  ⚠ heavy, lower --per-page" if mb > a.max_mb else ""
        print(f"{out}  {mb:.1f} MB  {len(ch)} subject(s), "
              f"{sum(len(g['items']) for g in ch)} proposal(s){flag}")
    if len(chunks) > 1:
        print(f"\n{len(chunks)} pages: publish each one as its own artifact.")


if __name__ == "__main__":
    main()
