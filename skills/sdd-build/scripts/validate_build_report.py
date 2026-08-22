#!/usr/bin/env python3
import re
import sys
from pathlib import Path

REQUIRED_COMPLETE = [
    "## Metadata",
    "## Mode Selection",
    "## Summary",
    "## Task Execution",
    "## Files Changed",
    "## Drift Detected",
    "## Verification Results",
    "### Verify Gate",
    "## Acceptance Test Verification",
    "## Issues Encountered",
    "## Deviations from Design",
    "## Blockers",
    "## Final Status",
]

PLACEHOLDER = re.compile(r"\{[^{}\n]{1,160}\}")
LEGACY = re.compile(r"/release\s+|Ready for:", re.I)

def fail(errors, msg):
    errors.append(msg)

def slice_section(text, start, end=None):
    i = text.find(start)
    if i < 0:
        return ""
    if end:
        j = text.find(end, i + len(start))
        if j >= 0:
            return text[i:j]
    return text[i:]

def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/validate_build_report.py <BUILD_REPORT.md>")
        return 64

    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"FAIL: file not found: {path}")
        return 64

    text = path.read_text(encoding="utf-8")
    errors = []

    for sec in REQUIRED_COMPLETE:
        if sec not in text:
            fail(errors, f"missing section: {sec}")

    if PLACEHOLDER.search(text):
        fail(errors, "unresolved template placeholder remains")

    metadata = slice_section(text, "## Metadata", "## Mode Selection")
    status_m = re.search(r"\|\s*\*\*Status\*\*\s*\|\s*([^|]+)\|", metadata, re.I)
    status = status_m.group(1).strip().lower() if status_m else ""
    if not status:
        fail(errors, "Metadata Status not found")

    final = slice_section(text, "## Final Status")
    overall_m = re.search(r"### Overall:\s*(COMPLETE|IN PROGRESS|BLOCKED)", final, re.I)
    overall = overall_m.group(1).upper() if overall_m else None
    if not overall:
        fail(errors, "Final Status Overall not found")

    mode = slice_section(text, "## Mode Selection", "## Summary")
    if "Recommendation:" not in mode or "User decision:" not in mode:
        fail(errors, "Mode Selection must record recommendation and user decision")

    gate = slice_section(text, "### Verify Gate", "### Manual UX Receipt")
    for label in ("Kind", "Command / Method", "Exit / Result", "Status", "Evidence"):
        if label not in gate:
            fail(errors, f"Verify Gate missing {label}")

    gate_status_m = re.search(r"\|\s*\*\*Status\*\*\s*\|\s*([^|]+)\|", gate, re.I)
    gate_status = gate_status_m.group(1).strip().lower() if gate_status_m else ""

    if overall == "COMPLETE":
        if status != "complete":
            fail(errors, "Overall COMPLETE requires Metadata Status=Complete")
        if not any(token in gate_status for token in ("green", "manual receipt")):
            fail(errors, "Complete build requires Verify Gate Green or Manual receipt")
        blockers = slice_section(text, "## Blockers", "## Final Status")
        if re.search(r"\|\s*[^|\n]+\|\s*[^|\n]+\|\s*[^|\n]+\|", blockers):
            # Ignore markdown header/separator; detect likely data rows.
            data = []
            for line in blockers.splitlines():
                s = line.strip()
                if not s.startswith("|"):
                    continue
                cells = [c.strip() for c in s.strip("|").split("|")]
                if cells and cells[0].lower() not in {"blocker", "---"} and not all(re.fullmatch(r"-+", c) for c in cells):
                    data.append(cells)
            if data:
                fail(errors, "Complete build cannot contain blocker rows")

        expected_tail = "## Next Step\n\nExecute o **SDD Handoff by RDD**."
        pos = text.find("## Next Step")
        if pos < 0:
            fail(errors, "Complete build requires Next Step")
        elif text[pos:].strip() != expected_tail:
            fail(errors, "Complete build Next Step must contain only the standard SDD completion handoff")
    else:
        if "## Next Step" in text:
            fail(errors, "Blocked/In Progress build must not include completion Next Step")

    if LEGACY.search(slice_section(text, "## Next Step")):
        fail(errors, "legacy slash-command handoff detected")

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 2

    print("PASS: BUILD_REPORT structural lint passed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
