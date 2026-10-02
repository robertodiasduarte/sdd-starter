# Contributing

Thanks for your interest in SDD Starter!

## How this project is maintained

- **Releases are curated.** Changes land in curated releases, not continuous merges.
- **Each skill carries its own version.** `metadata.version` (X.Y.Z) and `metadata.updated` (YYYY-MM) in the `SKILL.md` frontmatter, plus the identification line right below the title. A PR that changes a skill bumps both and the line (and `manifest.json` / `evals/cases.json` when present); CI and the release workflow fail otherwise. People who install from a `.zip` never `git pull` — the version inside the file is how they learn their copy is old.
- **Discuss before coding.** Please open an issue describing the problem or proposal before sending a pull request. PRs without prior discussion may be closed with a pointer to this policy.
- **Language.** Documentation is bilingual (English canonical, Brazilian Portuguese translation). Skill content is currently written in Brazilian Portuguese.

## What makes a good issue

- A concrete problem you hit while running one of the four skills (say which agent: claude.ai, Claude Code, ChatGPT, Codex, other).
- The phase artifact involved (`BRAINSTORM_*.md`, `DEFINE_*.md`, `DESIGN_*.md`, `BUILD_REPORT_*.md`) and what you expected vs. what happened.
- Suggestions to make instructions clearer for beginners.

## What we will not merge

- Changes that couple the skills to a single vendor or agent.
- Project-specific rules, secrets, personal data, or references to private infrastructure.
- Rewrites that grow the skills beyond beginner scope — that is what [SpecGate](https://github.com/robertodiasduarte/specgate) is for.

## Local checks

Before proposing changes, run:

```bash
bash scripts/publish-check.sh   # content safety gate (must print PASS)
python3 scripts/check-versions.py --base origin/main   # version gate (must print PASS)
for t in skills/*/tests; do python3 -B -m unittest discover -s "$t" -p 'test_*.py'; done
bash scripts/package.sh         # builds the per-skill zips into dist/
```
