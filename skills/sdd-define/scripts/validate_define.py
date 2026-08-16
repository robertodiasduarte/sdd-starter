#!/usr/bin/env python3
import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = [
    "## Metadata",
    "## Problem Statement",
    "## Target Users",
    "## Goals",
    "## Success Criteria",
    "## Acceptance Tests",
    "## Clarifications",
    "## Verify Gate",
    "## Out of Scope",
    "## Constraints",
    "## Technical Context",
    "## Assumptions",
    "## Clarity Score Breakdown",
    "## Open Questions",
    "## Revision History",
    "## Next Step",
]

EARS = re.compile(r"\b(When|While|Where|shall|If)\b")
ACTIVE_MARKER = re.compile(r"\[NEEDS CLARIFICATION:", re.I)

def fail(msg):
    print(f"FAIL: {msg}")
    return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/validate_define.py <DEFINE.md>")
        return 64

    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"FAIL: file not found: {path}")
        return 64

    text = path.read_text(encoding="utf-8")
    ok = True

    for section in REQUIRED_SECTIONS:
        if section not in text:
            ok = fail(f"missing section: {section}") and ok

    if ACTIVE_MARKER.search(text):
        ok = fail("active NEEDS CLARIFICATION marker remains") and ok

    score_matches = re.findall(r"(?:Clarity Score.*?\|\s*\*\*?(\d{1,2})/15|Total\*\*?\s*\|\s*\*\*(\d{1,2})/15)", text, flags=re.S)
    scores = []
    for pair in score_matches:
        for val in pair:
            if val:
                scores.append(int(val))
    if scores:
        score = scores[-1]
        if score < 12:
            ok = fail(f"Clarity Score {score}/15 is below 12/15") and ok
    else:
        ok = fail("could not find numeric Clarity Score") and ok

    # Acceptance test rows: require EARS anchors in AT lines.
    at_lines = [ln for ln in text.splitlines() if re.search(r"\|\s*AT-\d+", ln)]
    if not at_lines:
        ok = fail("no Acceptance Test rows found") and ok
    else:
        for ln in at_lines:
            if not EARS.search(ln):
                ok = fail(f"Acceptance Test lacks EARS keyword: {ln.strip()}") and ok

    # Verify Gate structural fields.
    m = re.search(r"```yaml\s*(verify_gate:.*?)```", text, flags=re.S | re.I)
    if not m:
        ok = fail("missing yaml verify_gate block") and ok
    else:
        block = m.group(1)
        for field in ("kind:", "cmd:", "pass_when:", "threshold:", "manual_fallback:"):
            if field not in block:
                ok = fail(f"verify_gate missing field: {field[:-1]}") and ok
        kind_match = re.search(r"kind:\s*[\"']?([a-z-]+)", block)
        if kind_match and kind_match.group(1) not in {"test", "smoke", "eval", "typecheck", "manual-ux"}:
            ok = fail(f"invalid verify_gate kind: {kind_match.group(1)}") and ok

    # LLM Prompts must be literal true or false in Technical Context.
    llm_line = next((ln for ln in text.splitlines() if "LLM Prompts" in ln and "|" in ln), None)
    if not llm_line or not re.search(r"\|\s*(true|false)\s*\|", llm_line, re.I):
        ok = fail("LLM Prompts must be literal true or false") and ok

    expected_next = "Execute o **SDD Design by RDD**."
    next_idx = text.find("## Next Step")
    if next_idx == -1:
        ok = fail("Next Step section missing") and ok
    else:
        tail = text[next_idx:].strip()
        expected_tail = f"## Next Step\n\n{expected_next}"
        if tail != expected_tail:
            ok = fail("Next Step must contain only the standard SDD Design by RDD handoff") and ok

    if ok:
        print("PASS: DEFINE structural lint passed")
        return 0
    return 2

if __name__ == "__main__":
    raise SystemExit(main())
