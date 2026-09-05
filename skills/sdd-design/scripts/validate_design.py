#!/usr/bin/env python3
import re
import sys
from pathlib import Path
from collections import defaultdict

REQUIRED_SECTIONS = [
    "## Metadata",
    "## Architecture Overview",
    "## Components",
    "## Key Decisions",
    "## File Manifest",
    "## Code Patterns",
    "## Data Flow",
    "## Integration Points",
    "## Testing Strategy",
    "## Error Handling",
    "## Configuration",
    "## Security Considerations",
    "## Observability",
    "## Requirements Traceability",
    "## Risks and Mitigations",
    "## Advisor Ledger",
    "## Revision History",
    "## Next Step",
]

BLOCKING_PATTERNS = [
    r"\[NEEDS CLARIFICATION",
    r"\bTBD\b",
    r"\{[^{}\n]{1,120}\}",
]

def section(text, start, end=None):
    i = text.find(start)
    if i < 0:
        return ""
    j = text.find(end, i + len(start)) if end else -1
    return text[i:j if j >= 0 else None]

def table_rows(block):
    rows = []
    for line in block.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if not cells or all(re.fullmatch(r":?-{2,}:?", c or "-") for c in cells):
            continue
        rows.append(cells)
    return rows

def parse_manifest(text):
    block = section(text, "## File Manifest", "## Code Patterns")
    rows = table_rows(block)
    data = []
    for cells in rows:
        if not cells or cells[0] in {"#", "---"}:
            continue
        if re.fullmatch(r"\d+", cells[0]) and len(cells) >= 6:
            idx = int(cells[0])
            deps = []
            if cells[5].lower() not in {"none", "n/a", "—", "-"}:
                deps = [int(x) for x in re.findall(r"\d+", cells[5])]
            data.append((idx, cells[1], cells[2], cells[3], cells[4], deps))
    return data

def has_cycle(items):
    graph = {idx: deps[:] for idx, *_rest, deps in items}
    visiting, visited = set(), set()

    def dfs(n):
        if n in visiting:
            return True
        if n in visited:
            return False
        visiting.add(n)
        for d in graph.get(n, []):
            if d in graph and dfs(d):
                return True
        visiting.remove(n)
        visited.add(n)
        return False

    return any(dfs(n) for n in graph)

def fail(errors, msg):
    errors.append(msg)

def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/validate_design.py <DESIGN.md>")
        return 64

    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"FAIL: file not found: {path}")
        return 64

    text = path.read_text(encoding="utf-8")
    errors = []

    for sec in REQUIRED_SECTIONS:
        if sec not in text:
            fail(errors, f"missing section: {sec}")

    for pat in BLOCKING_PATTERNS:
        if re.search(pat, text, re.I):
            fail(errors, f"blocking placeholder/ambiguity detected: {pat}")

    # O handoff legado e a linha "Ready for: `/build ...`" no lugar do Next Step canonico.
    # NAO se caracteriza pelo caminho: `.claude/sdd/` e `sdd/` sao os dois caminhos validos
    # (a skill grava em `sdd/`, ou em `.claude/sdd/` quando o projeto ja usa essa pasta).
    # Citar qualquer um deles no CORPO do documento e legitimo.
    if "Ready for: `/build" in text:
        fail(errors, "legacy /build handoff detected")

    metadata = section(text, "## Metadata", "## Architecture Overview")
    for label in ("BRAINSTORM", "DEFINE", "LLM Prompts", "Status"):
        if label not in metadata:
            fail(errors, f"metadata missing {label}")

    llm_match = re.search(r"\|\s*\*\*LLM Prompts\*\*\s*\|\s*(true|false)\s*\|", metadata, re.I)
    if not llm_match:
        fail(errors, "LLM Prompts must be literal true or false in Metadata")
        llm_value = None
    else:
        llm_value = llm_match.group(1).lower()

    status_match = re.search(r"\|\s*\*\*Status\*\*\s*\|\s*([^|]+)\|", metadata, re.I)
    if not status_match or "Ready for Build" not in status_match.group(1):
        fail(errors, "final DESIGN status must be Ready for Build")

    arch = section(text, "## Architecture Overview", "## Components")
    if "```text" not in arch or len(re.sub(r"\s+", "", arch)) < 80:
        fail(errors, "Architecture Overview must contain a substantive text diagram")

    components = table_rows(section(text, "## Components", "## Key Decisions"))
    component_data = [r for r in components if r and r[0] != "Component"]
    if not component_data:
        fail(errors, "Components table has no component rows")

    decisions = section(text, "## Key Decisions", "## File Manifest")
    if not re.search(r"### Decision", decisions):
        fail(errors, "at least one inline architecture decision is required")
    for token in ("Context:", "Choice:", "Rationale:", "Alternatives Rejected:", "Consequences:"):
        if token not in decisions:
            fail(errors, f"Key Decisions missing {token}")

    manifest = parse_manifest(text)
    if not manifest:
        fail(errors, "File Manifest has no concrete numbered rows")
    else:
        ids = {x[0] for x in manifest}
        for idx, _file, _action, _purpose, _owner, deps in manifest:
            bad = [d for d in deps if d not in ids]
            if bad:
                fail(errors, f"manifest row {idx} references missing dependencies: {bad}")
        if has_cycle(manifest):
            fail(errors, "File Manifest dependency graph has a cycle")

        total_m = re.search(r"\*\*Total Files:\*\*\s*(\d+)", section(text, "## File Manifest", "## Code Patterns"))
        if not total_m:
            fail(errors, "Total Files must be numeric")
        elif int(total_m.group(1)) != len(manifest):
            fail(errors, f"Total Files={total_m.group(1)} but manifest has {len(manifest)} rows")

    code_patterns = section(text, "## Code Patterns", "## Data Flow")
    if "```" not in code_patterns:
        fail(errors, "Code Patterns must include at least one fenced snippet")

    if llm_value == "true":
        if "## LLM Prompts" not in text:
            fail(errors, "LLM Prompts=true requires ## LLM Prompts")
        else:
            lp = section(text, "## LLM Prompts", "## Data Flow")
            for required in ("Inventory", "one-shot", "loop", "Consumer", "Output"):
                if required.lower() not in lp.lower():
                    fail(errors, f"LLM Prompts section missing {required}")
            prompt_paths = [f for _i, f, *_rest in manifest if "/prompts/" in f or f.startswith("prompts/")]
            for pp in prompt_paths:
                clean = pp.strip("` ")
                if clean not in lp:
                    fail(errors, f"prompt manifest path missing from LLM inventory: {clean}")
    elif llm_value == "false" and "## LLM Prompts" in text:
        fail(errors, "LLM Prompts=false must not include ## LLM Prompts")

    testing = section(text, "## Testing Strategy", "## Error Handling")
    if not any(k in testing.lower() for k in ("unit", "integration", "e2e", "verify")):
        fail(errors, "Testing Strategy lacks recognizable test coverage")

    trace = section(text, "## Requirements Traceability", "## Risks and Mitigations")
    if not re.search(r"\|\s*(?:AT-\d+|MUST|SHOULD|COULD)", trace, re.I):
        fail(errors, "Requirements Traceability has no requirement/AT row")

    expected_tail = "## Next Step\n\nExecute o **SDD Build by RDD**."
    next_pos = text.find("## Next Step")
    if next_pos < 0:
        fail(errors, "Next Step missing")
    elif text[next_pos:].strip() != expected_tail:
        fail(errors, "Next Step must contain only the standard SDD Build by RDD handoff")

    if errors:
        for e in errors:
            print(f"FAIL: {e}")
        return 2

    print("PASS: DESIGN structural lint passed")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
