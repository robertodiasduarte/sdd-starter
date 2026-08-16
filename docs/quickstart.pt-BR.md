# Quickstart

> 🇺🇸 [English version](quickstart.md) (canônica)

Coloque as quatro skills SDD no seu agente e rode seu primeiro fluxo.

## 1. Instale as skills

### Claude Code (ou qualquer agente com filesystem: Codex CLI, Cursor, etc.)

```bash
git clone https://github.com/robertodiasduarte/sdd-starter.git
cp -R sdd-starter/skills/* ~/.claude/skills/        # nível de usuário, vale em todo lugar
# ou, para um único projeto:
cp -R sdd-starter/skills/* seu-projeto/.claude/skills/
```

Para outros agentes, copie as quatro pastas (`sdd-brainstorm`, `sdd-define`, `sdd-design`, `sdd-build`) para o diretório de onde seu agente lê skills/instruções, mantendo cada pasta intacta.

### claude.ai (web)

1. Baixe os `.zip` (um por skill) da [última Release](../../../releases/latest).
2. No claude.ai, abra **Configurações → Capacidades → Skills** e faça o upload de cada zip.

### ChatGPT / agentes baseados em OpenAI

Cada skill traz um `agents/openai.yaml` com display name e um prompt inicial pronto. Dois caminhos comuns:

- **GPT personalizado / Projeto**: anexe os arquivos da skill (`SKILL.md`, `references/`, `assets/`) como conhecimento e cole o `default_prompt` do `agents/openai.yaml` como instrução inicial.
- **Plataformas de agente que aceitam upload de skill**: suba o zip da skill baixado da [última Release](../../../releases/latest).

Menus mudam entre versões dos produtos — se os caminhos acima não baterem com a sua tela, a regra geral é: entregue ao agente os arquivos da pasta da skill e mande-o seguir o `SKILL.md`.

## 2. Rode seu primeiro fluxo

Comece uma conversa e diga, por exemplo:

> Use a skill **sdd-brainstorm**. Quero construir um controle de despesas pessoais para macOS.

O agente vai te entrevistar (uma pergunta por vez), comparar 2–3 abordagens e produzir `BRAINSTORM_CONTROLE_DESPESAS.md`. Depois encadeie as fases, sempre entregando o artefato anterior à skill seguinte:

1. **Brainstorm** → produz `BRAINSTORM_*.md`
2. **Define** (entregue o Brainstorm) → produz `DEFINE_*.md`
3. **Design** (entregue Brainstorm + Define) → produz `DESIGN_*.md`
4. **Build** (entregue os três, num agente com acesso de escrita ao projeto) → código real + `BUILD_REPORT_*.md`

Cada artefato termina com uma linha de **Next Step** dizendo exatamente qual skill rodar em seguida.

> **Nota:** as fases 1–3 funcionam em qualquer agente de chat — sem filesystem. A fase 4 (**Build**) exige um agente que escreva código no seu projeto (Claude Code, Codex, Cursor, Lovable, Base44, etc.).

## 3. Opcional: valide os artefatos localmente

As skills que produzem artefatos com gate trazem um validador estrutural:

```bash
python skills/sdd-define/scripts/validate_define.py DEFINE_MINHA_FEATURE.md
python skills/sdd-design/scripts/validate_design.py DESIGN_MINHA_FEATURE.md
python skills/sdd-build/scripts/validate_build_report.py BUILD_REPORT_MINHA_FEATURE.md
```

Eles checam a estrutura (seções obrigatórias, testes EARS, handoff de Next Step) e saem com código diferente de zero, com o motivo, quando algo falta.

## Próximos passos

- [Workflow](workflow.pt-BR.md) — o que cada fase faz e por que a ordem importa.
- Quer gates executáveis e enforcement em CI? Gradue-se no [SpecGate](https://github.com/robertodiasduarte/specgate).
