#!/usr/bin/env python3
"""Entry for "The Meeting That Should Have Been an Email" (make.fun, judged text).

Deliverable: one line of plain text at /output/entry.txt — a single joke about a meeting
that should have been an email, 1..200 characters, UTF-8, no trailing newline, mode 0644.
/output must hold that artifact and nothing else.

Harness: program/v1, python3.13, no network. Stdlib only. Deterministic.

The joke turns on the last word: the meeting is nothing but an email action ("cc")
performed in person — the email already arrived, so the meeting delivers nothing new.
(The crowded rival angles — "read the email aloud", "ran 90 minutes", "action item: reply
all", "agenda: discuss the agenda" — are deliberately avoided: surprise is criterion 3.)
"""

from __future__ import annotations

import hashlib
import os
import sys
import tempfile

OUT_DIR = "/output"
ARTIFACT = "entry.txt"

ENTRY = "The email was already in my inbox; this meeting is just cc'ing me in person."

MAX_CHARS = 200
MIN_CHARS = 1
MODE = 0o644


def validate(text: str) -> None:
    """Fail loudly if the line would not pass the gate (1..200 chars, UTF-8, one line)."""
    if not text.strip():
        raise ValueError("entry is only white space")
    chars = len(text)
    if not MIN_CHARS <= chars <= MAX_CHARS:
        raise ValueError(f"entry is {chars} characters, the cap is {MIN_CHARS}..{MAX_CHARS}")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(c) < 32 for c in text):
        raise ValueError("entry holds a control character")
    text.encode("utf-8")  # must be valid UTF-8


def clear_output(out_dir: str) -> None:
    """/output must hold only the required artifact: drop any other regular file."""
    for name in os.listdir(out_dir):
        if name == ARTIFACT:
            continue
        p = os.path.join(out_dir, name)
        if os.path.isfile(p) and not os.path.islink(p):
            os.remove(p)


def write_artifact(data: bytes, out_dir: str) -> str:
    """Write the entry bytes atomically as <out_dir>/entry.txt with mode 0644."""
    os.makedirs(out_dir, exist_ok=True)
    clear_output(out_dir)
    path = os.path.join(out_dir, ARTIFACT)
    fd, tmp = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
        os.chmod(tmp, MODE)  # MUST be 0644 before os.replace: the grader refuses mode 600
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise
    return path


def main(argv: list[str]) -> int:
    validate(ENTRY)
    out_dir = argv[1] if len(argv) > 1 else OUT_DIR
    data = ENTRY.encode("utf-8")
    path = write_artifact(data, out_dir)

    # Read back and prove the artifact on disk: exact bytes, exact mode, single line.
    with open(path, "rb") as fh:
        on_disk = fh.read()
    if on_disk != data:
        raise SystemExit("artifact on disk differs from the entry bytes")
    mode = os.stat(path).st_mode & 0o777
    if mode != MODE:
        raise SystemExit(f"artifact mode is {mode:o}, expected {MODE:o}")
    if len(on_disk) > MAX_CHARS * 4:
        raise SystemExit("artifact is over the size cap")

    print(
        "entry.txt: {chars} chars, {bytes} bytes, mode {mode:o}, sha256 {sha}".format(
            chars=len(ENTRY),
            bytes=len(on_disk),
            mode=mode,
            sha=hashlib.sha256(on_disk).hexdigest(),
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
