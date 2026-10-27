# Como falar com o aluno — sdd-handoff

Quem pede um handoff costuma estar sem tempo ou sem contexto. A seção "Como falar com o aluno" do
`SKILL.md` dá o formato; este arquivo dá as palavras e um exemplo inteiro.

## Glossário (explique na primeira vez em que o termo aparecer)

- handoff — "o registro do que ficou pronto e do que falta, para a próxima conversa continuar sem
  depender desta";
- modo continuar / entregar — "continuar: o trabalho segue depois; entregar: a etapa terminou e fecha
  com um checklist";
- família da feature — "o assunto a que este trabalho pertence; um handoff por assunto, com cada etapa
  nova no topo";
- ficha — "a tabela no topo do handoff: objetivo, status, feito, falta, pronto quando";
- pendência — "o que ficou por fazer; separo o que está quebrado do que é melhoria";
- prompt de retomada — "o texto pronto para colar na próxima conversa, que funciona sozinho";
- HANDOFF — "o documento desta skill, um por assunto".

Não fale em contexto, branch ou worktree sem traduzir: "o que esta conversa sabe", "a linha de versões
desta tarefa", "a pasta separada desta tarefa".

## Status desta skill, preenchido

`Handoff: ✅ 1 Modo · ▶️ 2 Estado · ⬜ 3 Ficha e pendências · ⬜ 4 Documento · ⬜ 5 Prompt de retomada`

## Exemplo de resposta completa

Situação: o aluno disse "preciso parar, documenta para eu continuar amanhã"; há um handoff antigo de um
assunto parecido e não está claro se é o mesmo.

**Status** — `Handoff: ✅ 1 Modo · ▶️ 2 Estado · ⬜ 3 Ficha e pendências · ⬜ 4 Documento · ⬜ 5 Prompt de retomada`
(no Status: "Ficha" é a tabela no topo do registro — objetivo, status, feito, falta, pronto quando;
"pendências" é o que ficou por fazer; "Prompt de retomada" é o texto pronto para colar na próxima conversa.)

**O que foi feito** — Modo **continuar**: você vai seguir amanhã, então o registro fecha com o texto
pronto para colar na próxima conversa (o prompt de retomada). Procurei registros anteriores deste assunto
e encontrei um: `sdd/HANDOFF_CONFERENCIA_NOTAS.md`, de duas semanas atrás, sobre a planilha de
conferência de notas.

**Agora: etapa 2 — Estado** — Antes de escrever, preciso saber se o que você fez hoje é continuação
daquele assunto ou um assunto novo: o handoff é um por assunto, com cada etapa nova no topo, e a escolha
errada deixa a próxima conversa lendo o registro errado. Nada é gravado ainda.

**Sua decisão** — **O trabalho de hoje é do mesmo assunto daquele registro?**
- **é esse** — acrescento a etapa de hoje no topo de `HANDOFF_CONFERENCIA_NOTAS.md`.
- **é outro** — crio um registro novo com o nome do assunto de hoje; diga qual é.
- **não sei** — eu mostro as três primeiras linhas do registro antigo para você comparar.

**Próximo passo** — Com a sua resposta, eu reúno o estado (o que mudou, o que foi conferido) e preencho a
ficha e as pendências.
