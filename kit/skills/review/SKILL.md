---
name: review
description: How a session asks the person for anything — an answer, a choice, a validation, a go-ahead. A short multiple-choice question (QCM) when the point is simple; a review board (an interactive page published as an artifact, or opened in a browser) when the interaction is more complex or when data must be shown. Every question restates the problem simply; every proposal states its advantages, its drawbacks and all the consequences; a comment field under every point and a global comment; the answer comes back as one line. Standing rule of every session (CLAUDE.md "Asking the person"); the generator is review_board.py in this folder.
---

# review — asking the person: a QCM, or a review board

**The rule, loaded by every session** (the person who owns the method, 2026-10-09):

> When you must interact with me, prefer the built-in multiple-choice question (QCM). When
> the interaction is more complex, or when you must present data to me, use the review
> board below, making sure I can give a comment on each of the points you ask me about,
> and a global comment too. Always and systematically, for each question, restate the
> problem simply so that I understand it; and for each proposal, explain just as simply
> its advantages and its drawbacks, with all the consequences of that solution.

A choice written in prose ("so, which do you prefer?") is a choice the person cannot tick:
if a question has options, it is a QCM or a board, never a paragraph.

## 1. QCM or board?

| The person must… | Use | Example |
|---|---|---|
| answer one simple point with two to four options | the built-in **multiple-choice question** (one at a time) | the date of the next meeting; "continue, something else, or close?" |
| choose on several subjects at once | a **board**, one subject per group | the twelve design decisions of the design phase |
| judge something that needs data in front of them | a **board**, with the measured facts in the notes | which tests to keep, where the pipeline fails, a catalogue to triage |
| validate a document or give a go-ahead with comments | a **board**, one group per point to validate | the minutes before they are sent; the hand-over plan |

In a QCM too: each option's description states its advantage and its drawback; the
recommended option comes first and is labelled "(Recommended)".

## 2. Build a board

```bash
python3 .claude/skills/review/review_board.py --example > spec.json      # the shape
python3 .claude/skills/review/review_board.py spec.json -o board.html --fragment --per-page 0
python3 .claude/skills/review/review_board.py spec.json -o board.html --fragment --lang fr   # French labels
```

The specification (one JSON) carries, **per subject** (`groups[]`): a `key` (what comes back
in the line), a `heading`, the `notes` — **"Problem"** restated in plain words, then
**"Measured"**: the facts with their commands — a `recommend` sentence, and the `items`.
**Per proposal** (`items[]`): `label` (`p1`, `p2`…), `title`, `facts` (who does it, in which
mark — Person, Ask Claude, Automatic — and its cost), `pros`, `cons` (each a list: say every
consequence, not only the obvious one), `recommended` on one of them.

The `intro` is the only field that accepts HTML. It is the **instructions frame** and it
says, every time: what the person must do (one tick per subject? several?); what their
choice triggers (which file, which tool, and that nothing is written before the line comes
back); what happens to what is not chosen; the cost if they follow the recommendations.

`notes`, `facts`, `details` and `meta` are HTML-escaped: plain text only.

The generator renders, by itself: a comment field under every proposal and every subject,
a global comment field at the end, the "Tick the recommendations" toggle (the page loads
unticked: the toggle is the person's act), "Untick all", and the copy button that composes
one line with the ticks and every comment. Never disable a comment field.

## 3. Publish it

- **With the Artifact tool** (claude.ai, Claude Code connected to it): build with
  `--fragment` and publish the file; one artifact per page; the same file path republished
  keeps the URL (a correction before any answer), a new round is a new file and a new
  artifact, with a distinct `prefix`.
- **Without it**: tell the person the path of the `.html` file (without `--fragment`, so it
  is a complete page) and ask them to open it in a browser; the copy button works there too.
- **Keep the sources**: the board's `spec.json`, the generator call, the page and an
  `open.html` shortcut go to `project/meetings/<date>/boards/<round>/` of the project's
  repository, with a row in the meetings registry (`project/meetings/README.md`).

## 4. The line comes back

`r1  runner=p1«…»  data=p2  global«…»` — the prefix, then `key=label` per subject, each
comment between `«…»`, a commented but unticked proposal as `!label«…»`. Apply nothing
before the line; then do what the frame announced, quote the line in the session's journal
entry, and record any decision through `decision-record`.

## Guardrails

- **Never pre-tick, never decide for the person.** Recommend, always; choose, never.
- **Show every option that exists**, including the ones you would not recommend, with why.
- **Nothing changes before the line** — no file, no push, no paid call.
- **One question, one place**: never ask the same thing in the board and in the chat.
