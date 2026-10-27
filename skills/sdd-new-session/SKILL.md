---
name: sdd-new-session
license: MIT
description: "Abre uma frente de trabalho isolada neste repositório: cria uma git worktree fora da pasta do projeto, com uma branch nova nascida da branch de produção ATUALIZADA do remoto, prepara a pasta (dependências, arquivos locais) e abre no editor. Na primeira vez, investiga o repositório e grava o que descobriu em sdd/ambiente.md. Use quando o usuário disser 'abrir uma frente', 'nova sessão', 'nova tarefa isolada', 'criar worktree para X' ou quiser começar uma feature/correção sem misturar com outra em andamento."
metadata:
  author: Roberto Dias Duarte
  version: "1.3.0"
  updated: "2026-10"
---

# Nova frente de trabalho (new-session)

Na primeira resposta desta skill, comece com esta linha, uma vez só:
`sdd-new-session v1.3.0 · out/2026 · versão atual: https://github.com/robertodiasduarte/sdd-starter/releases/latest`

Um comando, uma tarefa, um diretório: `git worktree` + branch nova nascida do estado **remoto atual**
da branch de produção, pronta para abrir no editor.

## Como falar com o aluno

Quem usa esta skill, em geral, nunca usou git. Cada resposta é uma etapa explicada, não um relatório
técnico.

**As 4 etapas, sempre com estes nomes:**

| Etapa | Nome para o aluno | Passos desta skill |
|---|---|---|
| 1 | Pré-voo | Passo 0 (só lê) |
| 2 | Conhecer o repositório | Passo 1 — só na primeira vez; com `sdd/ambiente.md` já gravado, ➖ |
| 3 | Criar a frente | Passo 2, itens 1 a 5 |
| 4 | Abrir no editor | Passo 2, item 6, e Passo 3 |

**Toda resposta tem estas partes, nesta ordem** (pule a que não tiver conteúdo):

1. **Status** — uma linha: `✅ 1 Pré-voo · ➖ 2 Conhecer o repositório · ▶️ 3 Criar a frente · ⬜ 4 Abrir no editor`
   (✅ concluída — não só visitada; ▶️ a de agora; ⬜ por fazer; ⏸️ parada; ➖ pulada). Ao voltar a uma
   etapa, o motivo vai em **Agora**.
2. **O que foi feito** — em frases curtas, o resultado da etapa anterior, sem saída de comando. Com o
   pré-voo saudável, a linha ✅ do `checar.sh` não é colada: seu conteúdo vira estas frases. Registre a
   escolha do aluno: *"Você respondeu **sim**: …"*.
3. **Agora: etapa N — nome** — o que esta etapa faz e por quê, em 2 a 4 frases, como para alguém que nunca
   viu um terminal. Se for criar algo, diga **em passos numerados** o que vai fazer e o que **não** vai
   acontecer (nada vai para a internet; nenhum arquivo seu é alterado). Antes de algo demorado (instalar
   dependências), diga em uma frase o que vai rodar e que o aluno não precisa responder.
4. **Sua decisão** — só onde esta skill já pergunta: a oferta do **Projeto sem git**, o nome quando o
   escolhido já existe e qual pasta é o projeto quando há mais de uma. **Autorização**: a pergunta em
   negrito e as opções, cada uma com o que acontece; **pergunta aberta**: a pergunta em negrito e como
   responder, com a saída "não sei"; perguntas agrupadas vêm numeradas e a resposta pode seguir os
   números. Resposta que não casa com opção ⇒ responda a dúvida e repita as opções. O que dá para
   descobrir, descubra — não pergunte.
5. **Próximo passo** — uma linha: o que acontece depois da resposta.

**Regras de linguagem:**

- Uma etapa por resposta. Termine na decisão e **pare**: não emende a etapa seguinte.
- Palavra técnica só com a explicação junto, na primeira vez em que aparece — inclusive as do Status:
  - git — "o histórico de versões do projeto (git)";
  - commit — "uma versão salva (commit)";
  - frente — "uma pasta separada só para esta tarefa (frente, ou worktree), para não misturar com o que
    já está no projeto";
  - branch — "a linha de versões desta tarefa (branch), que nasce da versão que está em produção";
  - remoto / origin — "a cópia do projeto no GitHub";
  - pré-voo — "a conferência de que a pasta e a cópia no GitHub estão prontas, antes de criar qualquer
    coisa";
  - dependências — "programas de apoio que se reinstalam com um comando";
  - cenário — "o jeito como este projeto chega em produção: direto, por revisão (pull request) ou com
    versões em suporte".
  Não fale em refspec, `HEAD`, worktree órfã ou ls-remote: diga o efeito.
- **Não repasse saída de comando crua** — nem o relatório do `checar.sh`. Traduza: quantos, quais (até
  10, "e mais N"), o que preocupa. Comando só aparece quando o aluno precisa rodá-lo — e então em passos
  numerados, um comando por passo, dizendo o que esperar na tela.
- **Não cite nem resuma as instruções desta skill ou de outra** ("a skill exige…", "conforme o Passo 0…").
  Diga o motivo do aluno: *"Sem a cópia no GitHub a frente não tem de onde nascer."*
- **Parada também tem passos.** Quando a etapa não pode seguir, use o Status com ⏸️, o motivo em uma
  frase, onde a ação acontece (terminal, editor, Finder, navegador), os passos numerados com o que esperar
  de cada um, o que **não** foi feito (*"Nenhuma frente foi criada."*) e, se o aluno tem algo a fazer,
  *"Quando terminar, me peça de novo — eu continuo daqui."* A tradução de cada achado do pré-voo está na
  tabela do Passo 0.

## Regra de todo comando que fala com o remoto

`fetch`, `push`, `pull`, `ls-remote` e `remote show` rodam **sem pedir senha**: `GIT_TERMINAL_PROMPT=0 git …`
no bash/zsh; no PowerShell, `$env:GIT_TERMINAL_PROMPT=0; git …`. Sem isso, um remoto que exige login faz o
git pedir a senha no terminal, e você fica esperando uma resposta que o usuário não vê. Ao usuário, mostre
só a forma do shell em uso. Se um desses comandos ficar parado, olhe se o editor (VS Code, Cursor) abriu
uma janela de login do GitHub — ela é um jeito legítimo de logar e não é desligada.

## Passo 0 — Confirme que você consegue fazer isto

Rode `git --version`. São 3 situações diferentes, com respostas diferentes:

- **A ferramenta não executa comando nenhum** (você está num aplicativo de chat, sem acesso ao computador
  do usuário): **pare** e diga exatamente: *"Não tenho acesso ao seu repositório — estou rodando no
  aplicativo, não na sua máquina. Para esta tarefa você precisa do Claude Code ou do Codex instalado no
  terminal, aberto na pasta do projeto."* Em seguida diga o comando de instalação atual do agente que você
  é e onde fica a documentação oficial.
- **O comando executa, mas o git não existe** (`git: command not found`; no PowerShell,
  `CommandNotFoundException` ou `'git' is not recognized`): **pare** e diga *"O git não está instalado
  neste computador."* com o link https://git-scm.com/downloads, e que depois de instalar é preciso fechar
  e abrir o terminal de novo. Termine com *"Nada foi criado. Depois de instalar, peça a frente de novo."*
  Não diga que você está num aplicativo de chat: você está no terminal.
- **O git existe**: siga para o pré-voo. Ele vem antes de tudo porque também responde quando a pasta
  **não** é um repositório — e diz **qual** é o caso (pasta sincronizada pela nuvem, pasta pessoal,
  projeto numa subpasta, pasta vazia, projeto sem git). Nunca responda só "`git init`".

**Pré-voo.** Com o git no lugar, confira onde a pasta está e se a frente consegue nascer do remoto,
**antes** de criar qualquer coisa (inclusive o `sdd/ambiente.md`):

- Se existir a skill `sdd-checar-ambiente` na mesma pasta de skills desta (`.claude/skills/`,
  `.agents/skills/` ou a pasta global do agente) e houver bash, rode
  `bash <pasta das skills>/sdd-checar-ambiente/scripts/checar.sh --frente` e **leia a saída — ela não é
  repassada ao aluno**: cada achado tem a sua tradução na tabela **Como traduzir cada achado** abaixo.
  Código de saída 1 (bloco `🔴 Impede o trabalho`) ⇒ **pare aí**, respondendo pela tabela — se o achado for
  *"Este projeto ainda não usa git"*, veja também **Projeto sem git** abaixo. Código 0 ⇒ a única linha é
  `✅ Pronto para abrir a frente: …`; siga (o conteúdo dela vira o "O que foi feito" da etapa 1). Saiu 0
  **sem** essa linha (um relatório completo, com ⚠️ ou
  `✅ Repo …`)? A `sdd-checar-ambiente` instalada é anterior à 1.1.0 e não conhece o `--frente`: não conte
  isso como pré-voo — faça as checagens à mão abaixo e sugira atualizar a skill.
  Saída com *"provavelmente o terminal foi aberto na pasta errada"* ⇒ a `sdd-checar-ambiente` instalada
  é anterior à 1.2.0 e não diz qual é o caso: faça as checagens 0 e A–D abaixo à mão e sugira atualizá-la.
- Sem a skill ou sem bash (PowerShell puro), faça as mesmas checagens à mão, nesta ordem, parando na
  primeira que falhar:
  0. **Pasta sincronizada** (antes de tudo, com ou sem repositório): o caminho (`pwd -P` no bash/zsh,
     `(Get-Location).Path` no PowerShell) tem `Library/Mobile Documents`, `Library/CloudStorage`,
     `iCloudDrive`, `OneDrive`, `Dropbox`, `Google Drive`, `My Drive` ou `Meu Drive`; ou, no Mac, a pasta
     está em `~/Desktop` ou `~/Documents` e `ls -ld ~/Library/Mobile\ Documents/com~apple~CloudDocs/Documents`
     (ou `Desktop`) mostra um atalho (`->`) — é a Mesa e Documentos no iCloud, e o caminho não muda.
     ⇒ *"Esta pasta está dentro do <provedor>, que sincroniza tudo o que muda — o .git e as frentes se
     corrompem ou duplicam."*: mover o projeto para fora da nuvem (ex.: `~/Projetos`) pelo Finder ou
     Explorador de Arquivos e abrir o terminal lá.
  Com `git rev-parse --show-toplevel` falhando, diga **qual** é o caso, nesta ordem:
     - A. **Pasta pessoal** — a pasta é `~` (`$HOME`; no PowerShell, `$env:USERPROFILE`) ⇒ *"O terminal
       está na sua pasta pessoal, não na pasta de um projeto."* (não varra a pasta pessoal).
     - B. **Git numa subpasta** — bash/zsh:
       `find . -mindepth 1 -maxdepth 3 \( -name node_modules -o -name .Trash -o -name Library \) -prune -o -name .git -print`;
       PowerShell: `Get-ChildItem -Recurse -Depth 2 -Force -Filter .git -ErrorAction SilentlyContinue | Where-Object { $_.FullName -notmatch 'node_modules' } | ForEach-Object { Split-Path $_.FullName -Parent }`.
       Uma pasta ⇒ *"O projeto está em ./X — o terminal foi aberto uma pasta acima dele."*: abrir o chat
       de novo dentro dela. Duas ou três ⇒ liste e pergunte qual. Mais de três ⇒ diga quantas e pergunte
       qual é o projeto, sem listar todas.
     - C. **Pasta vazia** — nada além de `.DS_Store`, `desktop.ini`, `Thumbs.db` (`ls -A`; no PowerShell,
       `Get-ChildItem -Force`) ⇒ *"Ainda não há projeto nesta pasta."*: começar pela skill
       `sdd-brainstorm`; o git entra quando houver o que guardar.
     - D. **Arquivos sem git** ⇒ *"Este projeto ainda não usa git — e a frente nasce do git."*: veja
       **Projeto sem git** abaixo.
  Com repositório:
  1. `git remote` vazio ⇒ *"O repositório não tem remoto — a frente nasce dele."* com
     `git remote add origin <url do repositório>`. Há remoto, mas nenhum chamado `origin` (um fork com só
     `upstream`, por exemplo) ⇒ *"O repositório tem remoto, mas nenhum chamado origin — a frente nasce do
     origin."* com `git remote rename <nome> origin` (ou `git remote add origin <url>`). Não é login.
  2. Com janela de login do editor configurada (`GIT_ASKPASS` ou `SSH_ASKPASS` definidos, ou `git config core.askPass` não vazio — o terminal de VS Code ou Cursor), comece por um diagnóstico: a mesma consulta
     sem a janela e sem credencial guardada, que não pede nada a ninguém, com teto de 10 segundos —
     `GIT_TERMINAL_PROMPT=0 GIT_ASKPASS= GCM_INTERACTIVE=never GIT_SSH_COMMAND="ssh -o BatchMode=yes -o ConnectTimeout=8" git -c credential.helper= -c core.askPass= ls-remote --heads origin`
     (PowerShell: `$a=$env:GIT_ASKPASS; try { $env:GIT_TERMINAL_PROMPT=0; $env:GIT_ASKPASS=''; $env:GCM_INTERACTIVE='never'; git -c credential.helper= -c core.askPass= ls-remote --heads origin } finally { $env:GIT_ASKPASS=$a }`).
     Parado ou erro de rede ⇒ é rede, não janela: `GIT_ASKPASS` definido não prova login nenhum (com a rede
     parada o git nem chega a pedir senha). Qualquer outra resposta ⇒ o remoto respondeu; siga.
     Depois (ou direto, sem `GIT_ASKPASS`), a consulta de verdade, com a janela do editor ligada (quem está
     logado por ela passa): `GIT_TERMINAL_PROMPT=0 GCM_INTERACTIVE=never GIT_SSH_COMMAND="ssh -o BatchMode=yes -o ConnectTimeout=8" git ls-remote --heads origin`
     (o `GIT_SSH_COMMAND` só se não houver ssh próprio configurado — `GIT_SSH_COMMAND`, `GIT_SSH` ou
     `core.sshCommand`; com ele o ssh não fica parado pedindo frase-senha nem confirmação do host) (PowerShell:
     `$env:GIT_TERMINAL_PROMPT=0; $env:GCM_INTERACTIVE='never'; git ls-remote --heads origin` — o
     `GCM_INTERACTIVE` impede a janela do gerenciador de credenciais do Windows, sem desligar a credencial
     já guardada) — se passar de 10 segundos sem resposta,
     interrompa. Parada **depois de o diagnóstico ter pedido login** (`could not read Username`,
     `terminal prompts disabled`, `Permission denied (`) ⇒ *"A janela de login do editor está esperando
     resposta."*: responder a janela, ou `gh auth login` para não depender dela; parada em qualquer outro
     caso ⇒ rede. Erro de login (`could not read Username`, `Authentication failed`,
     `Permission denied (publickey)`, `Repository not found`) ⇒ *"O GitHub não deixou este computador ler
     o repositório: ou o endereço está errado, ou o repositório é privado e este computador não está logado
     no GitHub."* com `gh auth login` (alternativas, numa linha: chave SSH ou o gerenciador de credenciais
     do git); remoto fora do GitHub ⇒ *"O remoto `<host>` recusou o acesso deste computador (login ou
     permissão)."*, com o login daquele serviço — nunca `gh auth login`. `Host key verification failed` ⇒ `ssh -T git@<host>` e responder `yes` — não é login.
     `Could not resolve host`, `timed out`, ou parado sem prova de pedido de login ⇒ sem internet ou rede bloqueada (não fale
     em senha). Qualquer outra mensagem ⇒ a linha "Qualquer outro achado" da tabela abaixo: *"Não consegui
     ler a cópia do projeto no GitHub por um motivo que não reconheço."* e `git remote -v` — não chute a
     causa e não mostre a linha de erro ao aluno.
  3. Nenhuma branch listada ⇒ *"O repositório remoto ainda não tem nenhum commit — a frente nasce dele."*
     com o primeiro commit e `GIT_TERMINAL_PROMPT=0 git push -u origin <branch atual>`.
  Qualquer bloqueio é uma parada da etapa 1 (Status ⏸️), traduzida pela tabela abaixo: termina com
  *"Nenhuma frente foi criada."* e, quando o aluno tem algo a fazer, *"Quando terminar, me peça de novo —
  eu continuo daqui."*
- **Projeto sem git** (o achado D, ou o mesmo texto vindo do `checar.sh`). Esta skill não commita nem
  publica, e pôr um projeto no git sem conferir antes leva planilha de cliente, `.env` e certificado A1
  para o GitHub. Então:
  - se existir a skill `sdd-iniciar-repo` na mesma pasta de skills desta, a resposta segue a moldura de
    **Como falar com o aluno** (Status com ⏸️ na etapa 1, "O que foi feito", "Agora" em uma frase), sem
    o bloco 🔴, sem *"Depois de resolver, peça a frente de novo"* (você mesmo vai resolver) e sem citar
    ou explicar esta instrução; a decisão é esta, com as duas opções:
    > Este projeto ainda não usa git — e a frente nasce do git.
    >
    > **Quer que eu ponha este projeto no git e num GitHub privado agora? Eu confiro antes o que não pode
    > ir e peço seu OK em cada etapa.**
    > - **sim** — sigo a `sdd-iniciar-repo` do início (ela pede seu OK em cada etapa) e, quando ela
    >   terminar, volto aqui e abro a frente.
    > - **não** — paro aqui; nada é criado nem alterado.

    Com o sim, siga a `sdd-iniciar-repo` do início; quando ela terminar, volte ao pré-voo e abra a
    frente. Sem o sim, pare com *"Nenhuma frente foi criada."*;
  - se não existir, diga que a skill `sdd-iniciar-repo` faz isso e que ela vem com
    `npx skills add robertodiasduarte/sdd-starter -a <claude-code ou codex> -g -y`; depois, é pedir
    *"use a skill sdd-iniciar-repo para pôr este projeto no git"*. Pare com *"Nada foi criado."*
  Repositório sem remoto (item 1) num projeto que ainda não está no GitHub é o mesmo caso: a
  `sdd-iniciar-repo` retoma de onde ele parou.
- Pré-voo saudável não vira relatório: o conteúdo da linha ✅ entra no "O que foi feito", e siga para o
  Passo 1.

**Como traduzir cada achado** (do `checar.sh --frente` ou da checagem à mão). O aluno recebe a coluna
"Diga ao aluno", o lugar, os passos e o fechamento — nunca o relatório do script nem a linha de erro do git:

| Achado (como o script ou a checagem o identifica) | Diga ao aluno | Onde | Passos (um comando por passo, com o que esperar) | Fecha com |
|---|---|---|---|---|
| Pasta sincronizada ("Esta pasta está dentro do <provedor>…") | Esta pasta é sincronizada pela nuvem (<provedor>), e aqui o histórico do projeto se corrompe. | Finder / Explorador de Arquivos | 1. Mover a pasta do projeto para fora da nuvem, por exemplo `~/Projetos` (ela some da nuvem e aparece lá). 2. Abrir o terminal na pasta nova. | Nenhuma frente foi criada. Quando terminar, me peça de novo — eu continuo daqui. |
| A. Pasta pessoal ("O terminal está na sua pasta pessoal…") | O terminal está aberto na sua pasta pessoal, não na pasta de um projeto. | terminal / editor | 1. Abrir o chat de novo dentro da pasta do projeto. | Nenhuma frente foi criada. Quando terminar, me peça de novo — eu continuo daqui. |
| B. Uma subpasta com `.git` ("O projeto está em ./X…") | O projeto está na pasta X, um nível abaixo de onde o terminal foi aberto. | terminal / editor | 1. Abrir o chat de novo dentro de X. | Nenhuma frente foi criada. Quando terminar, me peça de novo — eu continuo daqui. |
| B. Duas ou três subpastas ("Há repositórios git nas subpastas…") | Há mais de um projeto aqui dentro; preciso saber qual é o seu. | — | — | **Sua decisão** (autorização): **"Qual destas pastas é o seu projeto?"** — uma opção por pasta: *"X — te digo como abrir o chat lá dentro."* |
| B. Mais de três ("Há N pastas com git aqui dentro…") | Há N pastas com projeto aqui dentro; preciso saber qual é a sua. | — | — | **Sua decisão** (pergunta aberta): **"Qual é a pasta do seu projeto? Responda com o nome dela."** |
| C. Pasta vazia ("Ainda não há projeto nesta pasta.") | Esta pasta está vazia: ainda não há projeto para abrir uma frente. | — | 1. Começar pela skill `sdd-brainstorm`; o git entra quando houver o que guardar. | Nenhuma frente foi criada. |
| D. Projeto sem git ("Este projeto ainda não usa git…") | Este projeto ainda não usa git — e a frente nasce do git. | com a `sdd-iniciar-repo`: — ; sem ela: terminal | Com a `sdd-iniciar-repo` instalada: a oferta do bloco **Projeto sem git** (sim / não). Sem ela: 1. `npx skills add robertodiasduarte/sdd-starter -a <claude-code ou codex> -g -y` (pede uma confirmação e lista as skills instaladas). 2. Fechar e abrir o agente de novo. 3. Pedir *"use a skill sdd-iniciar-repo para pôr este projeto no git"* (ela começa conferindo o que há na pasta). | Com a oferta: a decisão. Sem ela: Nenhuma frente foi criada. Quando terminar, me peça de novo — eu continuo daqui. |
| Git sem nome ou e-mail (o `--frente` não produz este achado hoje; é o do modo normal do `checar.sh`) | O git ainda não sabe quem você é; sem isso a primeira versão salva falha. | terminal | 1. `git config --global user.name "Seu Nome"` (não mostra nada). 2. `git config --global user.email "voce@exemplo.com"` (não mostra nada). | Nenhuma frente foi criada. Quando terminar, me peça de novo — eu continuo daqui. |
| Sem remoto ("O repositório não tem remoto…", item 1) | Este projeto ainda não tem uma cópia no GitHub — e a frente nasce dela. | terminal (ou —, com a oferta) | Projeto ainda sem GitHub, com a `sdd-iniciar-repo` instalada: a mesma oferta sim / não (ela retoma de onde o projeto parou). Projeto ainda sem GitHub e sem a `sdd-iniciar-repo`: os 3 passos de instalação da linha D. Já existe o repositório no GitHub: 1. `git remote add origin <endereço do repositório>` (não mostra nada). | Com a oferta: a decisão. Senão: Nenhuma frente foi criada. Quando terminar, me peça de novo — eu continuo daqui. |
| Remoto sem `origin` ("…nenhum chamado origin…", item 1) | O projeto tem uma cópia remota, mas com outro nome; a frente precisa que ela se chame origin. | terminal | 1. `git remote rename <nome> origin` (não mostra nada). | Nenhuma frente foi criada. Quando terminar, me peça de novo — eu continuo daqui. |
| Credencial recusada ("O GitHub não deixou este computador ler o repositório…") | O GitHub não deixou este computador ler o repositório: ou o endereço está errado, ou ele é privado e este computador não está logado. | terminal e navegador | 1. `gh auth login` (abre o navegador; entre com a conta do GitHub e volte ao terminal). 2. Pedir a frente de novo. Remoto fora do GitHub: o login daquele serviço. | Nenhuma frente foi criada. Quando terminar, me peça de novo — eu continuo daqui. |
| Servidor não confirmado (`Host key verification failed`) | Este computador nunca confirmou a identidade do servidor; não é problema de senha. | terminal e navegador | 1. `ssh -T git@<host>` (ele mostra a impressão digital do servidor e pergunta se confia). 2. No GitHub, antes de responder, confira a impressão digital em https://docs.github.com/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints; batendo, responda `yes`. | Nenhuma frente foi criada. Quando terminar, me peça de novo — eu continuo daqui. |
| Janela de login do editor ("A janela de login do editor está esperando resposta.") | O seu editor abriu uma janela de login que está esperando a sua resposta. | editor | 1. Responder a janela (ou `gh auth login`, para não depender dela). | Nenhuma frente foi criada. Quando terminar, me peça de novo — eu continuo daqui. |
| Sem rede ("Não consegui falar com <host> agora…") ou remoto vazio ("O repositório remoto ainda não tem nenhum commit…") | Sem internet ou rede bloqueada agora — não é senha. / A cópia no GitHub ainda está vazia; a frente nasce da primeira versão salva. | terminal | Rede: 1. Quando a conexão voltar, pedir a frente de novo. Vazio, já havendo uma versão salva neste computador: 1. `GIT_TERMINAL_PROMPT=0 git push -u origin <branch atual>` (mostra o envio). Vazio, sem nenhuma versão salva: 1. `git add <arquivos, pelo nome>` (não mostra nada). 2. `git commit -m "primeira versão"` (lista o que foi salvo). 3. o mesmo envio acima. | Nenhuma frente foi criada. Quando terminar, me peça de novo — eu continuo daqui. |
| Qualquer outro achado | Não consegui ler a cópia do projeto no GitHub por um motivo que não reconheço. | terminal | 1. `git remote -v` — confira se o endereço do origin é o do seu repositório. 2. Pedir a frente de novo. | Nenhuma frente foi criada. Quando terminar, me peça de novo — eu continuo daqui. (Nunca a linha de erro do git.) |

⛔ Não invente uma frente assumindo como o projeto é. Uma frente criada a partir de suposição falha na
primeira vez que for usada, e o usuário não vai saber por quê. Parar aqui é melhor que entregar algo
plausível e errado.

## Regra número um: não pergunte o que dá para descobrir

Investigue e decida. Só pergunte o que for genuinamente ambíguo — e aí com a sua recomendação e o
motivo, para o usuário só confirmar. Tudo o que você assumir sozinho vai para a seção `## Suposições`
de `sdd/ambiente.md`, onde ele corrige em uma linha.

## Passo 1 — Descubra o ambiente (uma vez por repositório)

O checkout principal é o primeiro caminho de `git worktree list --porcelain` (linha `worktree …`).
Se existir `<checkout principal>/sdd/ambiente.md`, **leia e use** — não redescubra o que já está
escrito. Se não existir, investigue sem perguntar — mas, se o nome da tarefa já veio no pedido, faça
**antes** a checagem de colisão do Passo 2 (item 2): nome repetido aborta sem gravar nada, nem o
`sdd/ambiente.md`.

```bash
GIT_TERMINAL_PROMPT=0 git remote show origin
git branch -r
git log --oneline -20
git tag --list
git worktree list
```

E leia, se existirem: `README.md`, `package.json`, `composer.json`, `requirements.txt`, `Makefile`,
`.gitignore`, `.env.example`, `.github/workflows/`, `CLAUDE.md`, `AGENTS.md`.

Extraia:

- **Branch principal** — a "HEAD branch" do `GIT_TERMINAL_PROMPT=0 git remote show origin`. Não é "a branch em que estou agora".
- **Preparação** — `package.json` versionado com `node_modules` no `.gitignore` ⇒ `npm install` na pasta
  nova (senão ela nasce quebrada). Mesma lógica para `requirements.txt`, `composer.json`.
- **Arquivos locais fora do git** — `.env` no `.gitignore` e `.env.example` versionado ⇒ a pasta nova
  precisa de uma cópia do `.env` do checkout principal.
- **Skills do agente fora do git** — cada pasta em `.claude/skills/` ou `.agents/skills/` sem nenhum
  arquivo versionado (`git ls-files <pasta>` vazio, pasta por pasta) ⇒ precisa ser copiada para a frente;
  sem isso, a `sdd-release` não existe dentro dela.
- **Editor** — o primeiro que existir de `code`, `cursor`, `subl` (`command -v <nome>` no bash/zsh,
  `Get-Command <nome>` no PowerShell).
- **Cenário de branching**, pela evidência do repositório (critério do material "Git na Prática"):

| Cenário | Como reconhecer | Estratégia | A frente termina em |
|---|---|---|---|
| **A — entrega contínua, sem revisor** | Sem `develop`/`staging` no remoto; histórico de commits diretos na principal | Trunk-Based simplificado | merge direto na principal |
| **B — entrega via Pull Request** | Histórico com "Merge pull request #…"; `.github/workflows/`; mais de um autor | GitHub Flow | push da branch + PR |
| **C — várias versões em suporte** | Tags de versão **e** branches `release/*` ou `hotfix/*` no remoto | GitFlow | PR para `develop` (a branch nasce de `develop`) |

Escolha sempre o mais simples que serve. Empate entre A e B ⇒ **A** (acrescentar PR depois é trivial;
tirar cerimônia que virou hábito, não). C exige as **duas** evidências; repositório de uma pessoa quase
nunca é C — se você concluiu C, reveja.

Grave em `<checkout principal>/sdd/ambiente.md` (crie a pasta `sdd/` se preciso), neste formato — uma
chave por linha, para o usuário corrigir à mão:

```markdown
# Ambiente deste repositório

> Gerado pelas skills sdd-new-session/sdd-release. Está errado? Corrija a linha — as skills leem daqui.

- branch_principal: main
- cenario: A (Trunk-Based) — evidência: <o que você viu, ex.: "20 últimos commits diretos na main, sem develop no remoto">
- pasta_das_frentes: ../<nome-do-repo>-frentes
- editor: code
- preparacao: npm install
- arquivos_locais: .env
- deploy: <preencha só se descobriu; senão "a descobrir pelo sdd-release">
- testes: <comando, se descobriu>
- sintaxe: <comando, se descobriu>
- versionamento: nenhum

## Suposições

- assumi <X> porque <Y>
```

Não commite esse arquivo: ele é do usuário, que decide se versiona.

## Passo 2 — Crie a frente

Receba o nome da tarefa em linguagem natural e, na ordem:

1. **Slug**: minúsculas, hífens, sem acento (ex.: "Relatório mensal" → `relatorio-mensal`).
2. **Aborte se a branch ou a pasta já existirem** (`git show-ref --verify refs/heads/<slug>`,
   `GIT_TERMINAL_PROMPT=0 git ls-remote --heads origin <slug>`, e a pasta `<pasta_das_frentes>/<slug>`). Não invente outro
   nome: peça outro ao usuário. Nada pode ter sido criado antes desta checagem.
3. `GIT_TERMINAL_PROMPT=0 git fetch origin "+refs/heads/<branch-base>:refs/remotes/origin/<branch-base>"`
   (refspec explícito: num clone de uma branch só, o fetch só com o nome da branch não atualiza
   `origin/<branch-base>`) e
   `git worktree add <pasta_das_frentes>/<slug> -b <slug> origin/<branch-base>` — a partir do estado
   **remoto**, não do local, que pode estar atrasado. `<branch-base>` é a principal (A, B) ou `develop` (C).
   Cenário C sem `origin/develop` (`GIT_TERMINAL_PROMPT=0 git ls-remote --heads origin develop` vazio)? Pare antes de criar
   qualquer coisa e diga: o critério aponta GitFlow, mas não há `develop` de onde a frente possa nascer.
4. Na pasta nova: rode a preparação, se houver.
5. **Copie para a frente o que o git não leva**: os arquivos locais (`.env`) e **cada pasta de skill não
   versionada**, sempre a partir do checkout principal (caminhos absolutos, entre aspas):
   `mkdir -p "<frente>/.claude/skills" && cp -R "<checkout principal>/.claude/skills/<skill>" "<frente>/.claude/skills/"`,
   idem `.agents/skills/`.
   Confira que `<frente>/.claude/skills/sdd-release` (ou `.agents/skills/sdd-release`) existe quando existe
   no checkout principal — sem ela, a frente não consegue ser fechada. O Claude Code pede aprovação para
   escrever em `.claude/`: se a cópia for negada, **não pare** — termine a frente e, na resposta, entregue
   o comando de cópia pronto e a alternativa de instalar as skills uma vez para todos os projetos
   (`npx skills add robertodiasduarte/sdd-starter -a <motor> -g -y`).
6. Abra no editor (`code <pasta>`). **Sem editor, não aborte**: a frente já está pronta; mostre o caminho
   para abrir à mão.

A pasta fica **fora** do repositório (`../<repo>-frentes/<slug>`): dentro dele, a worktree apareceria
como arquivo não rastreado e sujaria o `git status` de todas as outras frentes.

**O que esta skill NÃO faz:** não commita, não faz push, não apaga, não integra. Só cria. Tudo o que
destrói ou publica é entregue como comando — ou fica para a skill `sdd-release`.

## Passo 3 — Responda

Na moldura de **Como falar com o aluno**: o Status pelo resultado efetivo (✅ no que foi feito; ➖ na etapa
2 quando `sdd/ambiente.md` já existia; ➖ na etapa 4 sem editor, com o caminho para abrir à mão), e os
itens abaixo distribuídos entre "O que foi feito" (1, 2 e 4), "Próximo passo" (3 e 5) e a última linha.
Nesta ordem:

1. **Cenário** (A, B ou C) com a evidência — o que você viu, não "parece ser".
2. **Caminho** da pasta e **nome da branch**.
3. **Como encerrar** esta frente, pronto para copiar: no fim, use a skill `sdd-release` de dentro da
   pasta nova; ou, à mão, o comando de integração do cenário seguido de
   `git worktree remove <pasta>` e `git branch -d <slug>`.
4. **Suposições** que você fez (se houver) e onde corrigi-las (`sdd/ambiente.md`).
5. No cenário A, trabalhando sozinho com IA: lembre de pedir uma revisão do código à IA antes de
   integrar — não há segundo humano olhando.
6. **Última linha, destacada:**
   `⚠️ Continue na janela nova. Esta sessão do agente continua presa à pasta onde foi aberta — nenhum
   cd muda isso. Build, commit e push rodam lá dentro.`

## Por que cada regra existe (não apague sem ler)

- **A branch nasce de `origin/<branch-base>` atualizada** (a principal; `develop` no cenário C) — nascer da branch atual herda trabalho pela
  metade de outra tarefa, e a frente nova "já vem com código estranho".
- **A mesma branch não abre em duas worktrees** — o Git recusa. Por isso não se volta para a principal
  dentro da pasta da frente: integra-se pelo caminho do cenário e atualiza-se no checkout principal.
- **Se outra frente for integrada antes desta**, esta nasceu de um ponto que já não existe. Antes de
  integrar: `GIT_TERMINAL_PROMPT=0 git fetch origin` + `git merge origin/<branch-base>` + **rodar os testes de novo** — é aí que
  o conflito entre as duas aparece. (A `sdd-release` faz isso.)
- **Worktree e branch órfãs se acumulam** — depois de integrar, `git worktree remove` **e**
  `git branch -d`. O `-d` minúsculo é proteção: só apaga o que já foi integrado.
- **Pasta que não é repositório tem quatro casos opostos** — "abra na pasta certa" e "ponha o projeto no
  git" são respostas contrárias; juntar as duas numa frase deixou um aluno sem saber qual era a dele. E
  "`git init`" sozinho leva a pasta inteira, com planilha de cliente, para o primeiro commit.
- **Pasta sincronizada para antes de tudo** — iCloud, OneDrive, Dropbox e Google Drive sincronizam arquivo
  por arquivo; `.git` e worktrees se corrompem ou duplicam. No Mac com Mesa e Documentos no iCloud o
  caminho não denuncia: a evidência é o atalho dentro do iCloud Drive.
- **O pré-voo vem antes de qualquer criação** — sem remoto, com o remoto vazio ou sem login, o
  `git worktree add … origin/<principal>` falha no meio e deixa a pasta pela metade; o aluno não sabe o que
  apagar. Parar antes, dizendo a causa e que nada foi criado, é o que permite simplesmente pedir de novo.
- **Git ausente não é "você está no app de chat"** — o diagnóstico errado manda instalar o agente que já
  está instalado.
- **A sessão do agente não migra** — abrir a pasta nova abre outra janela, mas a sessão onde a skill
  rodou fica ancorada no diretório de origem. Sem o aviso final, a frente inteira acaba sendo feita no
  lugar errado e isso só aparece na hora do commit.

---

Parte do SDD Starter by RDD — https://github.com/robertodiasduarte/sdd-starter
