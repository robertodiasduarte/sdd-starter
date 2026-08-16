# Quickstart

> 🇧🇷 [Versão em Português](quickstart.pt-BR.md)

Get the four SDD skills into your agent and run your first flow.

## 1. Install the skills

### Claude Code (or any filesystem-based agent: Codex CLI, Cursor, etc.)

```bash
git clone https://github.com/robertodiasduarte/sdd-starter.git
cp -R sdd-starter/skills/* ~/.claude/skills/        # user-level, available everywhere
# or, for a single project:
cp -R sdd-starter/skills/* your-project/.claude/skills/
```

For other agents, copy the four folders (`sdd-brainstorm`, `sdd-define`, `sdd-design`, `sdd-build`) into whatever directory your agent reads skills/instructions from, keeping each folder intact.

### claude.ai (web)

1. Download the per-skill `.zip` files from the [latest Release](../../../releases/latest).
2. In claude.ai, open **Settings → Capabilities → Skills** and upload each zip.

### ChatGPT / OpenAI-based agents

Each skill ships an `agents/openai.yaml` with a display name and a ready-made default prompt. Two common setups:

- **Custom GPT / Project**: attach the skill's files (`SKILL.md`, `references/`, `assets/`) as knowledge and paste the `default_prompt` from `agents/openai.yaml` as the starting instruction.
- **Agent platforms that accept skill uploads**: upload the per-skill zip from the [latest Release](../../../releases/latest).

Menus change between product versions — if the paths above don't match your UI, the rule of thumb is: give the agent the skill folder's files and tell it to follow `SKILL.md`.

## 2. Run your first flow

Start a conversation and say, for example:

> Use the **sdd-brainstorm** skill. I want to build a personal expense tracker for macOS.

The agent will interview you (one question at a time), compare 2–3 approaches, and produce `BRAINSTORM_EXPENSE_TRACKER.md`. Then chain the phases, always handing the previous artifact to the next skill:

1. **Brainstorm** → produces `BRAINSTORM_*.md`
2. **Define** (give it the Brainstorm) → produces `DEFINE_*.md`
3. **Design** (give it Brainstorm + Define) → produces `DESIGN_*.md`
4. **Build** (give it all three, in an agent with write access to your project) → real code + `BUILD_REPORT_*.md`

Each artifact ends with a **Next Step** line telling you exactly which skill to run next.

> **Note:** phases 1–3 work in any chat agent — no filesystem needed. Phase 4 (**Build**) requires an agent that can write code to your project (Claude Code, Codex, Cursor, Lovable, Base44, etc.).

## 3. Optional: validate artifacts locally

Skills that produce gated artifacts ship a structural validator:

```bash
python skills/sdd-define/scripts/validate_define.py DEFINE_MY_FEATURE.md
python skills/sdd-design/scripts/validate_design.py DESIGN_MY_FEATURE.md
python skills/sdd-build/scripts/validate_build_report.py BUILD_REPORT_MY_FEATURE.md
```

They check structure (required sections, EARS tests, Next Step handoff) and exit non-zero with a reason when something is missing.

## Where to go next

- [Workflow](workflow.md) — what each phase does and why the order matters.
- Want executable gates and CI enforcement? Graduate to [SpecGate](https://github.com/robertodiasduarte/specgate).
