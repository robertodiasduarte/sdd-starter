# Protocolo do Handoff

Referência de apoio da skill `sdd-handoff`. Contém as regras de decisão que o procedimento aplica.

---

## 1. Inferir o modo (não perguntar em menu)

A skill é acionada quase sempre num momento ruim: o contexto da conversa está acabando, ou o dia está terminando. Abrir com um menu de escolha adiciona fricção justamente aí. Então: **infira pelo contexto e confirme em uma linha.**

| Sinais na fala do usuário | Modo | Confirmação |
|---|---|---|
| "vou parar", "acabou meu contexto", "continuo amanhã", "documenta pra outra sessão", "passa o bastão" | **continuar** | "Vou registrar o estado e preparar o prompt de retomada." |
| "terminei", "está pronto", "vou entregar", "fechei essa parte", "acabei" | **entregar** | "Vou registrar o estado, conferir o fechamento e preparar o prompt." |
| Nenhum sinal claro | **continuar** (default) | "Assumindo que você vai continuar depois — se já terminou de vez, me diga que eu incluo o fechamento." |

O usuário corrige com uma palavra. Um menu custaria mais do que isso.

**A única diferença entre os modos** é que *entregar* acrescenta o checklist de fechamento. Todo o resto — ficha, seções, pendências, prompt — é idêntico.

---

## 2. Resolver a família da feature

O erro mais comum e mais caro: a mesma feature ganhar dois arquivos com nomes diferentes. Acontece porque na segunda sessão o nome usado não é idêntico ao da primeira — e aí o histórico se parte em dois, cada metade contando parte da história.

**Antes de criar qualquer arquivo:**

1. Procure por handoffs existentes que tratem do mesmo assunto. Busque por **domínio**, não por prefixo: "honorários", "cobrança", "financeiro" podem ser a mesma feature.
2. Achou um? **Atualize esse arquivo** — acrescente a etapa nova no topo.
3. Está em dúvida se é a mesma feature? **Pergunte**, mostrando qual arquivo você encontrou.
4. Só crie arquivo novo quando for genuinamente uma feature nova.

O nome escolhido na primeira vez é o nome para sempre. Vale a pena escolher com calma.

---

## 3. As seis seções da etapa

Toda etapa registra as mesmas seis coisas. Elas existem porque cada uma responde a uma pergunta que a próxima sessão vai fazer:

| Seção | Pergunta que responde |
|---|---|
| **O que foi feito** | "O que já está pronto?" |
| **Casos e testes em aberto** | "O que estava sendo testado quando parou?" |
| **Pendências** | "O que está quebrado e o que é melhoria?" |
| **Próximos passos** | "Por onde eu começo agora?" |
| **Alertas** | "O que eu posso quebrar sem perceber?" |
| **Onde está o trabalho** | "Onde ficaram os arquivos?" |

Nenhuma pode ficar vazia por preguiça. Se genuinamente não há nada, escreva que não há — isso também é informação.

---

## 4. Classificar pendências

Duas categorias, sempre:

- **🐛 Bug fix** — está quebrado, parcial, ou com comportamento errado conhecido. Alguém precisa consertar.
- **✨ Feature improvement** — é incremento planejado, melhoria ou próxima etapa. Ninguém precisa consertar; alguém pode construir.

Sem essa separação, "pendências" vira uma lista indistinta onde o urgente e o desejável se confundem. Quando não houver itens numa categoria, escreva "nenhuma" — a categoria vazia é informação, não é seção a ser omitida.

---

## 5. Registrar mudança de escopo em Eventos

Quando o escopo muda — algo saiu, algo entrou, o trabalho pausou — isso vira **linha nova** na seção `## Eventos`, com a data e o motivo.

O que **não** pode acontecer: reescrever o campo "Falta" da ficha como se o item nunca tivesse existido. Semanas depois ninguém lembra por que aquilo saiu, e a discussão recomeça do zero.

---

## 6. Definir "pronto quando"

O campo **Pronto quando** da ficha é o critério de conclusão da feature inteira. Ele precisa ser verificável: alguém deve conseguir olhar e dizer "sim" ou "não", sem opinião.

| ❌ Vago | ✅ Verificável |
|---|---|
| "Quando estiver funcionando bem" | "Quando eu conseguir emitir o relatório do mês sem abrir a planilha" |
| "Quando estiver rápido" | "Quando a tela abrir em menos de 3 segundos" |
| "Quando estiver completo" | "Quando as três telas estiverem no ar e eu tiver usado por uma semana sem erro" |

A feature só é marcada como ✅ completa quando esse critério estiver objetivamente satisfeito.

---

## 7. O checklist de fechamento (modo *entregar*)

Quatro perguntas, apresentadas como **inventário do que foi conferido** — nunca como aprovação ou reprovação:

1. O código roda?
2. Os critérios de aceite combinados passam?
3. As mudanças estão salvas onde deveriam?
4. O que quebrou está anotado?

**Este checklist não bloqueia nada.** Item não confirmado vira pendência registrada, e o handoff é entregue do mesmo jeito. Um checklist que reprova o trabalho de quem está encerrando o dia não ajuda ninguém — e um "verde" que não prova nada é pior ainda.

Por isso, na apresentação: sem ✅/❌ pareados, sem contagem tipo "3 de 4" lida como nota, sem vermelho, sem a palavra "reprovado".

---

## 8. Anti-padrões

| ❌ Não faça | Por quê |
|---|---|
| Criar `HANDOFF_FEATURE_ETAPA2.md` | Etapa nunca vira arquivo novo — o estado se parte |
| "Continue de onde paramos" | A próxima sessão não sabe onde foi |
| "O cliente que estava com problema" | Sem o nome, ninguém encontra |
| "Como discutimos antes" | A conversa não existe mais |
| Deixar o comando para a próxima sessão descobrir | Ela vai gastar tempo redescobrindo |
| Documentar só o que deu certo | O que quebrou é a informação mais útil |
| Reescrever "Falta" sem registrar em Eventos | A decisão desaparece |
| Marcar ✅ completa sem o critério satisfeito | O registro passa a mentir |

---

## 9. Checklist de qualidade

Antes de entregar:

- [ ] Família resolvida — atualizou arquivo existente, ou é feature genuinamente nova
- [ ] Ficha preenchida: Objetivo · Status · Feito · Falta · Pronto quando
- [ ] As seis seções da etapa preenchidas
- [ ] Pendências separadas em 🐛 e ✨ (ou "nenhuma" declarado)
- [ ] Mudança de escopo registrada em `## Eventos`
- [ ] Todo caso citado tem o dado concreto junto
- [ ] Próximos passos ordenados, com critério de pronto
- [ ] Prompt de retomada se sustenta sozinho
- [ ] Nenhum `{placeholder}` sobrou
- [ ] Sem filesystem: foi dito que não gravou, o nome sugerido e o que fazer com o documento
