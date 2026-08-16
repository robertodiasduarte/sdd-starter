# SDD Starter

**Skills de Spec-Driven Development para iniciantes, agnósticas de agente — by RDD.**

> 🇺🇸 **English version below** — click "English version" at the end of this page.

O SDD Starter é um conjunto de quatro **skills** portáteis que guiam qualquer agente de IA — Claude (claude.ai ou Claude Code), ChatGPT, Codex ou qualquer agente de código — por um fluxo simples de desenvolvimento guiado por especificação:

```
💡 Brainstorm  →  📋 Define  →  📐 Design  →  🔨 Build
```

Cada fase produz um artefato Markdown que alimenta a próxima. Você termina com requisitos de verdade, arquitetura de verdade e código funcionando — em vez de um prompt único e uma reza. As aplicações que você especificar podem mirar qualquer alvo que seu agente consiga construir: Windows, macOS, web, Lovable, Base44 e outros.

Se você quer a versão avançada deste fluxo — com Verify Gate executável, contrato de exit codes e integração com CI — veja o projeto irmão **[SpecGate](https://github.com/robertodiasduarte/specgate)**. O SDD Starter é a rampa de entrada; o SpecGate é a rodovia.

## As quatro skills

| Skill | Fase | Entrada | Saída |
|---|---|---|---|
| [`sdd-brainstorm`](skills/sdd-brainstorm/) | Explorar a ideia | Uma ideia, problema ou notas soltas | `BRAINSTORM_{FEATURE}.md` |
| [`sdd-define`](skills/sdd-define/) | Formalizar requisitos | O arquivo de Brainstorm | `DEFINE_{FEATURE}.md` (testes de aceitação EARS, Clarity Score, Verify Gate) |
| [`sdd-design`](skills/sdd-design/) | Arquitetar a solução | Brainstorm + Define | `DESIGN_{FEATURE}.md` (arquitetura, ADRs, File Manifest) |
| [`sdd-build`](skills/sdd-build/) | Implementar | Os três artefatos + projeto gravável | Código funcionando + `BUILD_REPORT_{FEATURE}.md` |

Cada pasta de skill é autocontida: um `SKILL.md` com o procedimento completo, `references/` com os protocolos, `assets/` com os templates canônicos de saída e (quando aplicável) `scripts/` com um validador estrutural e `agents/openai.yaml` para agentes baseados em OpenAI.

## Instalação

Dois caminhos, dependendo do seu agente — instruções completas no [Quickstart](docs/quickstart.pt-BR.md):

- **Claude Code, Codex ou qualquer agente com filesystem** — clone este repositório e copie as pastas de `skills/` para o diretório de skills do seu agente (ex.: `.claude/skills/`).
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

SDD Starter is a set of four portable **skills** that guide any AI agent — Claude (claude.ai or Claude Code), ChatGPT, Codex, or any coding agent — through a simple Spec-Driven Development flow:

```
💡 Brainstorm  →  📋 Define  →  📐 Design  →  🔨 Build
```

Each phase produces a Markdown artifact that feeds the next one. You end up with real requirements, a real architecture, and working code — instead of a one-shot prompt and a prayer. The apps you specify can target anything your agent can build: Windows, macOS, web, Lovable, Base44, and more.

If you want the advanced version of this workflow — with an executable Verify Gate, exit-code contracts, and CI integration — see the sibling project **[SpecGate](https://github.com/robertodiasduarte/specgate)**. SDD Starter is the on-ramp; SpecGate is the highway.

## The four skills

| Skill | Phase | Input | Output |
|---|---|---|---|
| [`sdd-brainstorm`](skills/sdd-brainstorm/) | Explore the idea | An idea, problem, or rough notes | `BRAINSTORM_{FEATURE}.md` |
| [`sdd-define`](skills/sdd-define/) | Formalize requirements | The Brainstorm file | `DEFINE_{FEATURE}.md` (EARS acceptance tests, Clarity Score, Verify Gate) |
| [`sdd-design`](skills/sdd-design/) | Architect the solution | Brainstorm + Define | `DESIGN_{FEATURE}.md` (architecture, ADRs, File Manifest) |
| [`sdd-build`](skills/sdd-build/) | Implement | All three artifacts + writable project | Working code + `BUILD_REPORT_{FEATURE}.md` |

Each skill folder is self-contained: a `SKILL.md` with the full procedure, `references/` with protocols, `assets/` with the canonical output templates, and (where applicable) `scripts/` with a structural validator and `agents/openai.yaml` for OpenAI-based agents.

## Installation

Two paths, depending on your agent — full instructions in the [Quickstart](docs/quickstart.md):

- **Claude Code, Codex, or any filesystem agent** — clone this repo and copy the folders under `skills/` into your agent's skills directory (e.g. `.claude/skills/`).
- **claude.ai or ChatGPT (web)** — download the ready-made per-skill `.zip` files attached to the [latest Release](../../releases/latest) and upload them to your agent.

## Documentation

- [Quickstart](docs/quickstart.md) ([PT-BR](docs/quickstart.pt-BR.md)) — install and run your first flow in minutes.
- [Workflow](docs/workflow.md) ([PT-BR](docs/workflow.pt-BR.md)) — how the four phases chain together, and what each artifact contains.

## Contributing

Releases are curated. Please open an issue to discuss before sending a PR — see [CONTRIBUTING.md](CONTRIBUTING.md).

## License & attribution

MIT — see [LICENSE](LICENSE). This project builds on concepts from **AgentSpec** by Luan Moreno Maciel — see [NOTICE](NOTICE).

</details>
