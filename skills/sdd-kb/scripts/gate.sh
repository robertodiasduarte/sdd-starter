#!/usr/bin/env bash
# Verify Gate: the validator must ACCEPT the canonical example KB AND REJECT every bad fixture.
# Accepting a bad fixture means the validator does not discriminate — that is a gate failure.
set -uo pipefail
cd "$(dirname "$0")/../../.."

V="skills/sdd-kb/scripts/validate_kb.py"
EXAMPLE="skills/sdd-kb/assets/example-kb"

if ! python3 "$V" "$EXAMPLE" >/dev/null 2>&1; then
  echo "FAIL: the canonical example KB should pass but did not:"
  python3 "$V" "$EXAMPLE"
  exit 2
fi

shopt -s nullglob
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

echo "PASS: example KB accepted, ${#fixtures[@]} bad fixtures rejected."
exit 0
