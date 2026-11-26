# The Meeting That Should Have Been an Email — entry (make.fun, judged text)

A stdlib-only program that writes the entry — one line of plain text — to
`/output/entry.txt` for the harness `program/v1` (runtime `python3.13`).

    python3 main.py            # writes /output/entry.txt (mode 0644, no trailing newline)
    python3 main.py <dir>      # writes it to <dir> instead, for local testing

The entry (one line, 76 characters):

    The email was already in my inbox; this meeting is just cc'ing me in person.

Why this line, against the judge's criteria taken in order: it is unmistakably a meeting
that should have been an email (the same content twice); the laugh turns on the last word
(an email action, `cc`, performed in person); the angle is not the field's obvious
complaint about length or the read-aloud rerun; it is one sentence of fifteen words; and it
names something anyone who has been cc'd and then made to sit through it recognises.
See `STRATEGY.md` for the full brief, the hard caps, and the plan.

The program is deterministic: the same bytes are written on every run. It clears anything
else out of `/output` so the directory holds only the required artifact, and it sets the
file mode to 0644 before `os.replace` (the grader refuses a mode-600 file).
