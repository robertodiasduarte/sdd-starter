#!/usr/bin/env python3
"""Structural and content lint for a HANDOFF document.

Exit codes: 0 pass, 2 fail, 64 usage error.
"""
import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = [
    "## Ficha da feature",
    "## Eventos",
    "### O que foi feito",
    "### Casos e testes em aberto",
    "### Pendências",
    "### Próximos passos",
    "### Alertas",
    "### Onde está o trabalho",
]

REQUIRED_FICHA_FIELDS = ["Objetivo", "Status", "Feito", "Falta", "Pronto quando"]

# The real failure mode of a handoff: referring to context the next session cannot see.
VAGUE = re.compile(
    r"como (discutimos|discutido|combinamos|combinado|vimos antes|falamos|conversamos)"
    r"|conforme (conversamos|discutimos|combinado|falado)"
    r"|(daquele|naquele|aquele) jeito que"
    r"|continu(ar|e) de onde paramos",
    re.I,
)

# Unsubstituted template placeholders: «...», {UPPER_SNAKE}, or any {prose with spaces}.
# The prose form must contain a space so real inline code ({"a": 1}) is not flagged.
PLACEHOLDER = re.compile(r"«[^»]*»|\{[A-Z][A-Z0-9_]{2,}\}|\{[^{}\n]*\s[^{}\n]*\}")

PENDING_LABELS = ["🐛", "✨"]


def fail(msg):
    print(f"FAIL: {msg}")
    return False


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/validate_handoff.py <HANDOFF.md>")
        return 64

    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"FAIL: file not found: {path}")
        return 64

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    ok = True

    for section in REQUIRED_SECTIONS:
        if section not in text:
            ok = fail(f"missing section: {section}") and ok

    for field in REQUIRED_FICHA_FIELDS:
        if not re.search(rf"\*\*{re.escape(field)}\*\*", text):
            ok = fail(f"Ficha da feature missing field: {field}") and ok

    for label in PENDING_LABELS:
        if label not in text:
            ok = fail(
                f"Pendências must classify items with {label} "
                "(use 'nenhuma' when there is nothing pending)"
            ) and ok

    for num, line in enumerate(lines, 1):
        for match in VAGUE.finditer(line):
            ok = fail(
                f"line {num}: vague back-reference {match.group(0)!r} — "
                "paste the actual value instead"
            ) and ok
        for match in PLACEHOLDER.finditer(line):
            ok = fail(
                f"line {num}: unsubstituted placeholder {match.group(0)!r}"
            ) and ok

    if not re.search(r"^#\s+HANDOFF:\s+\S", text, re.M):
        ok = fail("first heading must be '# HANDOFF: <feature name>'") and ok

    if ok:
        print("PASS: HANDOFF lint passed")
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
