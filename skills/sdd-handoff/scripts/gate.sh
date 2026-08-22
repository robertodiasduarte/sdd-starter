#!/usr/bin/env bash
# Verify Gate: the validator must ACCEPT the canonical example AND REJECT every bad fixture.
# Accepting a bad fixture means the validator does not discriminate — that is a gate failure,
# not a pass. This asserts behaviour, not wiring.
set -uo pipefail
cd "$(dirname "$0")/../../.."

V="skills/sdd-handoff/scripts/validate_handoff.py"
EXAMPLE="skills/sdd-handoff/assets/HANDOFF_EXAMPLE.md"

if ! python3 "$V" "$EXAMPLE" >/dev/null 2>&1; then
  echo "FAIL: the canonical example should pass but did not:"
  python3 "$V" "$EXAMPLE"
  exit 2
fi

shopt -s nullglob
fixtures=(tests/fixtures/bad_*.md)
if [ "${#fixtures[@]}" -eq 0 ]; then
  echo "FAIL: no bad fixtures found — the gate cannot prove the validator discriminates."
  exit 2
fi

for bad in "${fixtures[@]}"; do
  if python3 "$V" "$bad" >/dev/null 2>&1; then
    echo "FAIL: bad fixture was accepted by the validator: $bad"
    exit 2
  fi
done

echo "PASS: example accepted, ${#fixtures[@]} bad fixtures rejected."
exit 0
