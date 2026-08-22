#!/usr/bin/env python3
"""Structural and size lint for a knowledge-base domain folder.

Usage: python scripts/validate_kb.py <kb-domain-dir> [index-file]

Checks the minimum viable KB (index + quick-reference + >=1 concept + >=1 pattern),
the per-type line limits, leftover template placeholders, and registration in the index.

Exit codes: 0 pass, 2 fail, 64 usage error.
"""
import re
import sys
from pathlib import Path

LIMITS = {"quick_reference": 100, "concept": 150, "pattern": 200}

PLACEHOLDER = re.compile(r"\{\{[^}]*\}\}|\{[A-Z][A-Z0-9_]{2,}\}|\{[^{}\n]*\s[^{}\n]*\}")


def fail(msg):
    print(f"FAIL: {msg}")
    return False


def count_lines(path):
    return len(path.read_text(encoding="utf-8").splitlines())


def check_placeholders(path, ok):
    for num, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        # The templates carry intentional guidance after a horizontal rule; still, a
        # published KB must not ship any placeholder at all.
        for match in PLACEHOLDER.finditer(line):
            ok = fail(
                f"{path.name}:{num}: unsubstituted placeholder {match.group(0)!r}"
            ) and ok
    return ok


def main():
    if len(sys.argv) not in (2, 3):
        print("Usage: python scripts/validate_kb.py <kb-domain-dir> [index-file]")
        return 64

    root = Path(sys.argv[1])
    if not root.is_dir():
        print(f"FAIL: not a directory: {root}")
        return 64

    ok = True

    index = root / "index.md"
    quick = root / "quick-reference.md"

    if not index.is_file():
        ok = fail("missing index.md (the entry point)") and ok
    if not quick.is_file():
        ok = fail("missing quick-reference.md") and ok

    concepts = sorted((root / "concepts").glob("*.md")) if (root / "concepts").is_dir() else []
    patterns = sorted((root / "patterns").glob("*.md")) if (root / "patterns").is_dir() else []

    if not concepts:
        ok = fail("no concept found — a KB needs at least one concepts/*.md") and ok
    if not patterns:
        ok = fail("no pattern found — a KB needs at least one patterns/*.md") and ok

    if quick.is_file():
        n = count_lines(quick)
        if n > LIMITS["quick_reference"]:
            ok = fail(
                f"quick-reference.md has {n} lines, limit is {LIMITS['quick_reference']}"
            ) and ok
        ok = check_placeholders(quick, ok)

    if index.is_file():
        ok = check_placeholders(index, ok)

    for path in concepts:
        n = count_lines(path)
        if n > LIMITS["concept"]:
            ok = fail(
                f"concepts/{path.name} has {n} lines, limit is {LIMITS['concept']}"
            ) and ok
        ok = check_placeholders(path, ok)

    for path in patterns:
        n = count_lines(path)
        if n > LIMITS["pattern"]:
            ok = fail(
                f"patterns/{path.name} has {n} lines, limit is {LIMITS['pattern']}"
            ) and ok
        ok = check_placeholders(path, ok)

    # Registration: a KB that exists on disk but not in the index is invisible.
    index_file = Path(sys.argv[2]) if len(sys.argv) == 3 else root.parent / "_index.yaml"
    if not index_file.is_file():
        ok = fail(
            f"index file not found: {index_file} — register the domain "
            "(create it from KB_INDEX_TEMPLATE.yaml on the first run)"
        ) and ok
    else:
        registry = index_file.read_text(encoding="utf-8")
        if not re.search(rf"^\s+{re.escape(root.name)}\s*:", registry, re.M):
            ok = fail(
                f"domain {root.name!r} is not registered in {index_file.name} "
                "— an unregistered KB is invisible to whoever consults the index"
            ) and ok

    if ok:
        print(
            f"PASS: KB lint passed ({len(concepts)} concept(s), {len(patterns)} pattern(s))"
        )
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
