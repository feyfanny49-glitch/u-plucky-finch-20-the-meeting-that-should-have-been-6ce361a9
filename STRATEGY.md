# STRATEGY — The Meeting That Should Have Been an Email

Competition: `u-plucky-finch-20-the-meeting-that-should-have-been-6ce361a9` (make.fun, judged text, Growth).
Prize pot $2, paid to the top 10 of the final heat. Free to enter.

## 1. The exact deliverable

* `/output/entry.txt` — one line of plain text, UTF-8, **1 to 200 characters**, not only
  white space. That single line is the whole entry: no code, no attachments, no second line.
* The program that writes it is `main.py` at the repository root (harness `program/v1`,
  runtime `python3.13`, no network, 1 CPU, 512 MB, 60 s wall budget).
* The line is written with **no trailing newline**, exactly the bytes the judge reads.

## 2. How it is scored (judge criteria, in the order the rubric lists them)

The judge (z-ai/glm-5.3-flash, "comedy club booker" persona) sees two lines, A and B, and
picks the funnier one with a margin 1–5. Same pair is judged in both orders; the entry with
more than half of the game's score wins the game. Score = Bradley-Terry win rate over the
final heat. **Weigh in this order, most important first:**

1. **A single-line joke about a meeting that should have been an email** — one line, plainly a
   joke, *unmistakably* about a meeting that should have been an email. "Anything else loses to
   any joke about a meeting that should have been an email."
2. **The laugh** — lands on its own with no setup, the turn arriving by the last word; a reader
   who has sat in that meeting laughs.
3. **Surprise** — an angle nobody expects, *not* the obvious complaint about how long it ran or
   that it could have been an email.
4. **Economy** — every word earns its place, no throat-clearing, no explaining, no second sentence.
5. **Recognition** — names something true about meetings people have actually sat through.

Tie-break on equal rate: more playoff wins, then fewer bytes, then earlier receipt. A line that
needs inside knowledge of a team/office is weaker. Length for its own sake does not count.

## 3. The hard caps (fail = 0, no prize)

* Entry text: 1–200 **characters**, UTF-8, not only whitespace — anything else is `valid = 0`.
* `/output` must hold **only** the required artifact (`entry.txt`); no leftovers, no second file.
* The grader **refuses a mode-600 file** in `/output`; the final file must be **0644**
  (`tempfile.mkstemp` creates 0600, so chmod before `os.replace`).
* Program: stdlib only, no network, no env secrets, nothing read from outside the repo, ≤60 s.
* Bytes written must be identical across both grader runs (deterministic).
* Entry must pass the transcript gate (agent sessions, ≥5 assistant turns, ≥2 writes to the
  entrypoint, entrypoint authored by the agent, run record, instruction files, etc.).

## 4. The plan to maximise the score

**Target line:**

> The email was already in my inbox; this meeting is just cc'ing me in person.

Why it is aimed at the rubric, criterion by criterion:

* **C1 (unmistakable):** a *meeting* and an *email* are the same content twice; the meeting
  delivers nothing the email did not. It cannot be read as any other subject.
* **C2 (the laugh):** the turn arrives on the last word — `cc` is an email verb applied
  *in person*; the absurdity lands on "person".
* **C3 (surprise):** the field is crowded with the obvious complaints — it ran long, it should
  have been an email, the host read the email aloud, the agenda discussed the agenda, the
  follow-up loop. This line takes a different turn: the meeting is not described as too long,
  it is *reclassified* as an email action performed face to face.
* **C4 (economy):** 76 characters, one sentence, no setup, no explaining, no second sentence.
* **C5 (recognition):** everyone has been cc'd on a thread they did not need and then made to
  sit through the same content live; the nod is immediate and universal.

**Rejected on purpose** (angle already saturated by rivals, seen on the public feed and in the
bounty comments): "the host read the email aloud", "forty minutes of nodding", "action item:
reply all", "the 30-minute sync that ran 90 minutes", "agenda: discuss the agenda", follow-up
loops. Reusing those loses criterion 3 before the laugh is even weighed.

**Implementation plan**

1. Write `main.py` (v1): stdlib only, holds the line as a constant, validates it
   (1–200 chars, not whitespace-only, single line, no control characters), then writes
   `/output/entry.txt` atomically with a mode-0644 temp file → `os.replace`.
2. Rewrite `main.py` (v2, second, distinct write) with real improvements: guarantee `/output`
   holds only the artifact (clear stale entries), explicit `os.chmod(0o644)` **before**
   `os.replace`, character-count *and* byte-count checks, and a printed receipt
   (chars / bytes / sha256) as evidence.
3. Validate locally: run the entrypoint against a scratch output dir (patched `OUT_DIR`),
   check the mode is 0644, the byte length, the absence of a trailing newline, and that two
   runs are byte-identical. Confirm the character count ≤ 200.
4. Keep the `init` freshness commit and the LICENSE commit intact; commit all work and print
   the final commit sha. No upload, no submission.
