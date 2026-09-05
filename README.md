# SDD Starter

**Skills de Spec-Driven Development para iniciantes, agnósticas de agente — by RDD.**

> 🇺🇸 **English version below** — click "English version" at the end of this page.

O SDD Starter é um conjunto de **skills** portáteis que guiam qualquer agente de IA — Claude (claude.ai ou Claude Code), ChatGPT, Codex ou qualquer agente de código — por um fluxo simples de desenvolvimento guiado por especificação:

```
💡 Brainstorm  →  📋 Define  →  📐 Design  →  🔨 Build  →  📄 Handoff
```

Cada fase produz um artefato Markdown que alimenta a próxima. Você termina com requisitos de verdade, arquitetura de verdade e código funcionando — em vez de um prompt único e uma reza. As aplicações que você especificar podem mirar qualquer alvo que seu agente consiga construir: Windows, macOS, web, Lovable, Base44 e outros.

Se você quer a versão avançada deste fluxo — com Verify Gate executável, contrato de exit codes e integração com CI — veja o projeto irmão **[SpecGate](https://github.com/robertodiasduarte/specgate)**. O SDD Starter é a rampa de entrada; o SpecGate é a rodovia.

## As skills

| Skill | Fase | Entrada | Saída |
|---|---|---|---|
| [`sdd-brainstorm`](skills/sdd-brainstorm/) | Explorar a ideia | Uma ideia, problema ou notas soltas | `BRAINSTORM_{FEATURE}.md` |
| [`sdd-define`](skills/sdd-define/) | Formalizar requisitos | O arquivo de Brainstorm | `DEFINE_{FEATURE}.md` (testes de aceitação EARS, Clarity Score, Verify Gate) |
| [`sdd-design`](skills/sdd-design/) | Arquitetar a solução | Brainstorm + Define | `DESIGN_{FEATURE}.md` (arquitetura, ADRs, File Manifest) |
| [`sdd-build`](skills/sdd-build/) | Implementar | Os três artefatos + projeto gravável | Código funcionando + `BUILD_REPORT_{FEATURE}.md` |
| [`sdd-handoff`](skills/sdd-handoff/) | Fechar o ciclo | O trabalho da sessão | `HANDOFF_{FEATURE}.md` + prompt de retomada |

E uma skill **complementar**, que não entra na sequência — ela alimenta qualquer fase:

| Skill | Para quê | Entrada | Saída |
|---|---|---|---|
| [`sdd-kb`](skills/sdd-kb/) | Ensinar seu contexto à IA | O que você sabe sobre um domínio | Base de conhecimento consultável |

Cada pasta de skill é autocontida: um `SKILL.md` com o procedimento completo, `references/` com os protocolos, `assets/` com os templates canônicos de saída e (quando aplicável) `scripts/` com um validador estrutural e `agents/openai.yaml` para agentes baseados em OpenAI.

## Instalação

Dois caminhos, dependendo do seu agente — instruções completas no [Quickstart](docs/quickstart.pt-BR.md):

- **Claude Code** — um comando: `npx skills add robertodiasduarte/sdd-starter -a claude-code -y` (instala em `.claude/skills/` do projeto; com `-g`, em `~/.claude/skills/`, valendo em todo projeto).
- **Codex** — o mesmo comando trocando o motor: `npx skills add robertodiasduarte/sdd-starter -a codex -y` (instala em `.agents/skills/` do projeto; com `-g`, em `~/.agents/skills/` — o Codex lê essa pasta e também `~/.codex/skills/`).
- **Cursor, Kimi, Gemini CLI e outros** — mesmo comando com o nome do seu agente em `-a`. Sem Node.js, clone este repositório e copie as pastas de `skills/` para o diretório de skills do seu agente.
- **claude.ai ou ChatGPT (web)** — baixe os `.zip` prontos, um por skill, anexados na [última Release](../../releases/latest) e faça o upload no seu agente.

## Documentação

- [Quickstart](docs/quickstart.pt-BR.md) ([EN](docs/quickstart.md)) — instale e rode seu primeiro fluxo em minutos.
- [Workflow](docs/workflow.pt-BR.md) ([EN](docs/workflow.md)) — como as quatro fases se encadeiam e o que cada artefato contém.

## Contribuindo

As releases são curadas. Abra uma issue para discutir antes de enviar um PR — veja [CONTRIBUTING.md](CONTRIBUTING.md).

## Licença e atribuição

MIT — veja [LICENSE](LICENSE). Este projeto se apoia em conceitos do **AgentSpec** de Luan Moreno Maciel — veja [NOTICE](NOTICE).

---

<details>
<summary>🇺🇸 <strong>English version</strong> (click to expand)</summary>

# SDD Starter

**Beginner-friendly, agent-agnostic Spec-Driven Development skills — by RDD.**

> Skill content is currently written in **Brazilian Portuguese**; English skill versions are planned.

SDD Starter is a set of portable **skills** that guide any AI agent — Claude (claude.ai or Claude Code), ChatGPT, Codex, or any coding agent — through a simple Spec-Driven Development flow:

```
💡 Brainstorm  →  📋 Define  →  📐 Design  →  🔨 Build  →  📄 Handoff
```

Each phase produces a Markdown artifact that feeds the next one. You end up with real requirements, a real architecture, and working code — instead of a one-shot prompt and a prayer. The apps you specify can target anything your agent can build: Windows, macOS, web, Lovable, Base44, and more.

If you want the advanced version of this workflow — with an executable Verify Gate, exit-code contracts, and CI integration — see the sibling project **[SpecGate](https://github.com/robertodiasduarte/specgate)**. SDD Starter is the on-ramp; SpecGate is the highway.

## The skills

| Skill | Phase | Input | Output |
|---|---|---|---|
| [`sdd-brainstorm`](skills/sdd-brainstorm/) | Explore the idea | An idea, problem, or rough notes | `BRAINSTORM_{FEATURE}.md` |
| [`sdd-define`](skills/sdd-define/) | Formalize requirements | The Brainstorm file | `DEFINE_{FEATURE}.md` (EARS acceptance tests, Clarity Score, Verify Gate) |
| [`sdd-design`](skills/sdd-design/) | Architect the solution | Brainstorm + Define | `DESIGN_{FEATURE}.md` (architecture, ADRs, File Manifest) |
| [`sdd-build`](skills/sdd-build/) | Implement | All three artifacts + writable project | Working code + `BUILD_REPORT_{FEATURE}.md` |
| [`sdd-handoff`](skills/sdd-handoff/) | Close the cycle | The session's work | `HANDOFF_{FEATURE}.md` + resume prompt |

Plus a **complementary** skill that is not part of the sequence — it feeds any phase:

| Skill | Purpose | Input | Output |
|---|---|---|---|
| [`sdd-kb`](skills/sdd-kb/) | Teach the AI your context | What you know about a domain | A consultable knowledge base |

Each skill folder is self-contained: a `SKILL.md` with the full procedure, `references/` with protocols, `assets/` with the canonical output templates, and (where applicable) `scripts/` with a structural validator and `agents/openai.yaml` for OpenAI-based agents.

## Installation

Two paths, depending on your agent — full instructions in the [Quickstart](docs/quickstart.md):

- **Claude Code** — one command: `npx skills add robertodiasduarte/sdd-starter -a claude-code -y` (installs into the project's `.claude/skills/`; add `-g` for `~/.claude/skills/`).
- **Codex** — same command, different engine: `npx skills add robertodiasduarte/sdd-starter -a codex -y` (installs into the project's `.agents/skills/`; with `-g`, into `~/.agents/skills/` — Codex reads that folder and `~/.codex/skills/` too).
- **Cursor, Kimi, Gemini CLI and others** — same command with your agent's name in `-a`. Without Node.js, clone this repo and copy the folders under `skills/` into your agent's skills directory.
- **claude.ai or ChatGPT (web)** — download the ready-made per-skill `.zip` files attached to the [latest Release](../../releases/latest) and upload them to your agent.

## Documentation

- [Quickstart](docs/quickstart.md) ([PT-BR](docs/quickstart.pt-BR.md)) — install and run your first flow in minutes.
- [Workflow](docs/workflow.md) ([PT-BR](docs/workflow.pt-BR.md)) — how the four phases chain together, and what each artifact contains.

## Contributing

Releases are curated. Please open an issue to discuss before sending a PR — see [CONTRIBUTING.md](CONTRIBUTING.md).

## License & attribution

MIT — see [LICENSE](LICENSE). This project builds on concepts from **AgentSpec** by Luan Moreno Maciel — see [NOTICE](NOTICE).

</details>
