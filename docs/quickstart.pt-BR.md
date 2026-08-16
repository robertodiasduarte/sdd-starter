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

O ChatGPT instala skills nativamente (planos Business, Enterprise e Edu):

1. Abra **Configurações → Habilidades** (ou `chatgpt.com/admin/skills`).
2. Clique no **+** e arraste cada `.zip` da [última Release](../../../releases/latest) — sem descompactar.
3. Defina o acesso e repita para as 4 skills. Depois acione pelo nome (`sdd-brainstorm`, `sdd-define`…).

**Sem acesso à administração?** Crie um Projeto, envie os arquivos da skill (principalmente `SKILL.md` e `references/`) e, nas instruções do projeto, escreva: *"Siga o SKILL.md que está nos arquivos deste projeto."*

Cada skill também traz um `agents/openai.yaml` com display name e, em algumas fases, um `default_prompt` — usado por plataformas de agente que leem esse formato.

Menus mudam entre versões dos produtos — se os caminhos acima não baterem com a sua tela, a regra que não muda é: **entregue ao agente os arquivos da skill e mande-o seguir o `SKILL.md`**, que é onde o método está.

## 2. Rode seu primeiro fluxo

O caminho é o mesmo em qualquer ferramenta. Em cada fase você **aciona a skill, recebe um documento e o valida antes de seguir**.

> **A regra do método:** nunca siga para a próxima fase com um documento que você não leu.
> Corrigir uma frase agora custa minutos; corrigir depois que a IA já escreveu o aplicativo custa horas.

### Fase 1 — Brainstorm: lapide a ideia

```text
Use a skill sdd-brainstorm. Quero construir [sua ideia — ex.: um controle de despesas pessoais].
```

O agente te entrevista (uma pergunta por vez), compara 2–3 abordagens e produz `BRAINSTORM_*.md`.

**Valide antes de seguir:** a ideia está descrita como você pensou? Falta alguma coisa? Peça a correção agora.

### Fase 2 — Define: o que o app precisa fazer

```text
Use a skill sdd-define. Elabore a definição do projeto a partir do documento de brainstorm.
```

Novas perguntas (responda com calma) e sai o `DEFINE_*.md`, com os testes de aceitação.

**Valide antes de seguir:** está tudo que você espera? Tem algo sobrando? Corrija antes do Design.

### Fase 3 — Design: o plano técnico

Aqui você declara **onde a solução vai rodar** — é o que decide a ferramenta da fase seguinte:

| Você quer… | Escreva no prompt | No Build, use |
|---|---|---|
| Um site ou sistema web | aplicativo web (SaaS) | Claude Code ou Codex |
| Um app sem programar | aplicativo Lovable | Lovable conectado ao Claude ou ChatGPT |
| Um programa de Windows | executável (.exe) para Windows | Claude Code ou Codex |
| Um programa de Mac | aplicativo para macOS | Claude Code ou Codex |

```text
Use a skill sdd-design. Elabore o design do projeto com base nos documentos de brainstorm e define.
A aplicação utilizará a arquitetura [escolha na tabela acima].
```

**Valide antes de seguir:** é a última parada barata. Depois daqui, mudança significa reescrever código.

### Fase 4 — Build: a IA escreve o aplicativo

```text
Use a skill sdd-build. Construa a aplicação com base nos documentos de brainstorm, define e design.
```

Rode na ferramenta que a tabela indicou, entregando os três documentos.

**Valide o resultado:** teste o app e volte à IA com o que estiver diferente do combinado no Design.

Cada artefato termina com uma linha de **Next Step** dizendo exatamente qual skill rodar em seguida. Guarde os documentos — cada um é a entrada da fase seguinte e o registro do que você decidiu.

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
