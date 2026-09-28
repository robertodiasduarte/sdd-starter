---
name: sdd-checar-ambiente
license: MIT
description: "Diagnostica, sem alterar nada, se este computador e este repositório estão prontos para trabalhar com SDD: repositório git, agente de código, identidade do git, worktrees órfãs, dependências e editor. Responde em uma linha quando está tudo certo e, quando não está, lista o que impede primeiro, cada item com o comando exato que resolve. Use quando o usuário pedir para checar o ambiente, antes de abrir a primeira frente de trabalho num projeto, ou quando algo estranho acontecer (commit que falha, comando não encontrado, worktree que sumiu)."
metadata:
  author: Roberto Dias Duarte
---

# Checar ambiente

Responder uma pergunta: **este ambiente está pronto para trabalhar com SDD aqui?** Em segundos, sem
mudar nada, dizendo o que consertar.

## Regras

- **Somente leitura.** Não instale, não configure, não conserte, não crie arquivo. Entregue o comando;
  quem roda é o usuário, depois de ver o que está autorizando.
- **Não invente problema.** Sem `.env.example` versionado, não reclame de `.env` ausente. Sem
  `package.json`, não fale de `node_modules`. Um alarme falso ensina a ignorar todos os outros.
- **Ordene por consequência, não por categoria.** O que trava vem antes do que incomoda.
- **Descubra, não pergunte.** Tudo abaixo se descobre rodando comandos.
- **Funciona em qualquer shell.** Os comandos de `git` são iguais no bash, no zsh e no PowerShell. Para
  saber se um programa existe, use `command -v <nome>` no bash/zsh ou `Get-Command <nome>` no PowerShell.

## O que verificar, nesta ordem

**1. Onde estou**
- `git rev-parse --show-toplevel` — é um repositório git? Se **não** for, esse é o achado mais
  importante: diga na primeira linha (provavelmente o terminal foi aberto na pasta errada, ou o
  projeto ainda não tem git — `git init`).
- Pasta, branch atual (`git branch --show-current`) e se há mudanças não commitadas (`git status --short`).

**2. Agentes disponíveis**
- `claude --version` e `codex --version` — registre a versão de cada um que existir.
- Qual deles está executando esta skill agora.

**3. Git utilizável**
- `git --version`.
- `git config user.name` e `git config user.email`. Sem os dois, o primeiro commit falha com uma
  mensagem que não diz claramente o que fazer. O comando que resolve:
  `git config --global user.name "Seu Nome"` e `git config --global user.email "voce@exemplo.com"`.
- `git remote -v` — há remoto? Qual é a branch principal dele (`git remote show origin`, linha
  "HEAD branch")?

**4. Frentes de trabalho (worktrees)**
- `git worktree list` — quantas frentes abertas e onde.
- **Worktree órfã:** entrada da lista marcada `prunable`, ou cuja pasta não existe mais (alguém
  apagou a pasta à mão). Comando: `git worktree prune`.
- **Frente já integrada ainda aberta:** branch de uma worktree que já está contida na principal
  (`git branch --merged origin/<principal>`). Comando: `git worktree remove <pasta>` e depois
  `git branch -d <branch>`.
- Se existir `sdd/ambiente.md` no checkout principal (a primeira linha de
  `git worktree list --porcelain`), leia-o: ele diz a branch principal e onde as frentes ficam.
  Um `sdd/` não rastreado no checkout principal é esse arquivo — **não** é problema.

**5. Ferramentas do projeto**
- `package.json` presente e `node_modules` ausente ⇒ falta `npm install` (sem isso o primeiro
  comando do projeto falha com um erro que parece outra coisa). Mesma lógica para `requirements.txt`
  sem ambiente virtual e `composer.json` sem `vendor/`.
- `.env.example` versionado e nenhum `.env` ⇒ falta a configuração local (copiar o exemplo e
  preencher).
- Editor no PATH: `code`, `cursor` ou `subl` (nesta ordem). **Sem editor não é problema** — não entra
  em 🔴 nem em ⚠️; se houver um, cite-o no resumo ✅.

## Como reportar

Não entregue relatório longo: quem roda isto quer ser desbloqueado, não ler. Três blocos, nesta
ordem, **omitindo os vazios**:

1. **🔴 Impede o trabalho** — não é repositório git, git sem identidade, dependências faltando.
   Cada item com o **comando exato** que resolve, pronto para copiar.
2. **⚠️ Vale arrumar** — worktree órfã, frente integrada ainda aberta, `.env` ausente.
3. **✅ Resumo em uma linha** — ex.: `✅ Pronto: repo meu-app, branch main, 2 frentes abertas, Claude Code 2.1.`

Se estiver tudo certo, a resposta inteira é **só a linha ✅**. Ambiente saudável não merece parágrafo.

## Exemplos

Saudável:

```text
✅ Pronto: repo meu-app, branch main, 1 frente aberta, Claude Code 2.1.
```

Com dois problemas:

```text
🔴 Impede o trabalho
- O git não tem e-mail configurado — o primeiro commit vai falhar.
  git config --global user.email "voce@exemplo.com"

⚠️ Vale arrumar
- A frente ../meu-app-frentes/relatorio-mensal já foi integrada na main e continua aberta.
  git worktree remove ../meu-app-frentes/relatorio-mensal
  git branch -d relatorio-mensal

✅ Repo meu-app, branch main, Claude Code 2.1.
```

---

Parte do SDD Starter by RDD — https://github.com/robertodiasduarte/sdd-starter
