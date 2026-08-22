# Molde do prompt de retomada

> Este é o texto que o usuário cola numa **sessão nova** para continuar o trabalho. A nova sessão não viu a conversa anterior: ela só tem este prompt e, se existir, o arquivo de handoff.
>
> **Regra de ouro:** todo dado vai **colado**, nunca referenciado. Se uma linha não tem valor concreto, ou você busca o valor agora, ou apaga a linha. Um prompt que só faz sentido para quem participou da conversa anterior falhou.

---

```markdown
# Continuar: {NOME DA FEATURE} — {etapa}

{Se houver arquivo de handoff:}
Comece lendo o arquivo `HANDOFF_{FEATURE}.md` — a Ficha no topo e a etapa mais recente.

## Onde paramos

{2-3 linhas: o que já funciona, o que ficou pela metade e qual é o próximo movimento.
Inclua os dados concretos que a próxima sessão vai precisar logo de cara.}

## Contexto que você precisa ter

- {Onde o trabalho vive: pasta, projeto, branch}
- {Decisões já tomadas que não devem ser reabertas}
- {Ferramentas, arquivos ou bases envolvidas}

## Tarefas, em ordem

1. {Ação} — {arquivo, comando ou dado exato}. Pronto quando: {critério verificável}.
2. {Ação} — {dados colados: número, nome, data, identificador}. Pronto quando: {critério}.
3. {…}

## O que não quebrar

- {Invariante ou regra de negócio que precisa sobreviver}
- **Fora de escopo:** {o que não é para mexer nesta sessão}

## Como fechar

Ao terminar, rode a skill **SDD Handoff by RDD** de novo para registrar o que foi feito
e preparar a próxima retomada.
```

---

## Antes de entregar o prompt, confira

- [ ] Nenhuma frase do tipo "como discutimos", "conforme conversamos" ou "continue de onde paramos"
- [ ] Todo caso citado tem o dado concreto junto (nome, número, data, arquivo) — não só o apelido
- [ ] Cada tarefa tem critério de pronto verificável
- [ ] Nenhum `{placeholder}` sobrou
- [ ] O prompt se sustenta sozinho, mesmo que o arquivo de handoff se perca
