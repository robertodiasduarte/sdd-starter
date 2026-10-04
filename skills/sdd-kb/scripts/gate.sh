#!/usr/bin/env bash
# Verify Gate: the validator must ACCEPT the canonical example KB and every good fixture,
# AND REJECT every bad fixture.
# Accepting a bad fixture means the validator does not discriminate — that is a gate failure.
set -uo pipefail
cd "$(dirname "$0")/../../.."

V="skills/sdd-kb/scripts/validate_kb.py"
RM="skills/sdd-kb/scripts/kb_normativo.py"
EXAMPLE="skills/sdd-kb/assets/example-kb"
EXAMPLE_NORM="skills/sdd-kb/assets/example-kb-normativo"

if ! python3 "$V" "$EXAMPLE" >/dev/null 2>&1; then
  echo "FAIL: the canonical example KB should pass but did not:"
  python3 "$V" "$EXAMPLE"
  exit 2
fi

# Normative profile: the example passes, its RULE_MAP has not drifted, and every mutation
# (missing vigência, uncatalogued source, SHA mismatch, …) is rejected FOR THE RIGHT REASON.
out="$(python3 "$V" "$EXAMPLE_NORM" 2>&1)"
case "$out" in
  *"normativo: "*"rule(s)"*) : ;;
  *) echo "FAIL: the normative example KB should pass as perfil normativo:"; echo "$out"; exit 2 ;;
esac
if ! python3 "$RM" rule-map "$EXAMPLE_NORM" --check >/dev/null 2>&1; then
  echo "FAIL: example-kb-normativo/RULE_MAP.md drifted from rules/ — regenerate it"
  exit 2
fi
if ! python3 -B -m unittest discover -s tests -p 'test_sdd_kb_*.py' >/dev/null 2>&1; then
  echo "FAIL: normative mutation tests:"
  python3 -B -m unittest discover -s tests -p 'test_sdd_kb_*.py'
  exit 2
fi

shopt -s nullglob
# Good fixtures: real KB content the validator must NOT flag (JSON and template expressions in code).
# A validator that rejects good content trains people to ignore it — as harmful as accepting bad.
good=(tests/fixtures/kb_good_*/)
if [ "${#good[@]}" -eq 0 ]; then
  echo "FAIL: no good fixtures found — the gate cannot prove the validator avoids false positives."
  exit 2
fi
for dir in "${good[@]}"; do
  name="$(basename "$dir")"
  if ! python3 "$V" "${dir}${name}" "${dir}/_index.yaml" >/dev/null 2>&1; then
    echo "FAIL: good fixture was rejected by the validator: $name"
    python3 "$V" "${dir}${name}" "${dir}/_index.yaml"
    exit 2
  fi
done

fixtures=(tests/fixtures/kb_bad_*/)
if [ "${#fixtures[@]}" -eq 0 ]; then
  echo "FAIL: no bad fixtures found — the gate cannot prove the validator discriminates."
  exit 2
fi

for dir in "${fixtures[@]}"; do
  name="$(basename "$dir")"
  if python3 "$V" "${dir}${name}" "${dir}/_index.yaml" >/dev/null 2>&1; then
    echo "FAIL: bad fixture was accepted by the validator: $name"
    exit 2
  fi
done

echo "PASS: example KBs accepted (geral + normativo), ${#good[@]} good fixture(s) accepted, ${#fixtures[@]} bad fixtures rejected, normative mutation tests green."
exit 0
