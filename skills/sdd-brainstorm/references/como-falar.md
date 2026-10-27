# Como falar com o aluno — sdd-brainstorm

Quem pede um brainstorm, em geral, tem uma ideia e nenhum vocabulário de software. A seção "Como falar
com o aluno" do `SKILL.md` dá o formato; este arquivo dá as palavras e um exemplo inteiro.

## Glossário (explique na primeira vez em que o termo aparecer)

- brainstorm — "a conversa em que a gente entende o problema antes de decidir como resolver";
- abordagem — "um jeito de resolver o problema; eu mostro dois ou três e recomendo um";
- amostra — "um exemplo real do que entra e do que deve sair: uma planilha, um e-mail, um relatório";
- ground truth / dado verificado — "um exemplo em que já se sabe a resposta certa, para conferir depois";
- YAGNI — "a regra de deixar de fora o que não é necessário agora; a gente anota para depois";
- checkpoint — "uma parada para você confirmar que entendi certo antes de eu seguir";
- requisito — "uma frase que diz o que o sistema precisa fazer; é o que a próxima fase (Define) escreve";
- fase — "cada etapa do método: brainstorm, define, design, build, handoff".

Não fale em MVP, stakeholder, trade-off ou escopo sem traduzir: "o mínimo que resolve", "quem é
afetado", "o que se ganha e o que se perde", "o que entra e o que fica de fora".

## Status desta skill, preenchido

`Brainstorm: ✅ 1 Entender · ✅ 2 Perguntas · ✅ 3 Amostras · ▶️ 4 Abordagens · ⬜ 5 Validar · ⬜ 6 Gravar`

## Exemplo de resposta completa

Situação: um contador quer "automatizar a conferência das notas fiscais"; já respondeu três perguntas e
disse que tem um mês de notas em PDF como amostra. É a hora de escolher a abordagem.

**Status** — `Brainstorm: ✅ 1 Entender · ✅ 2 Perguntas · ✅ 3 Amostras · ▶️ 4 Abordagens · ⬜ 5 Validar · ⬜ 6 Gravar`
(no Status: "Amostras" são exemplos reais do que entra e do que deve sair; "Abordagens" são jeitos de
resolver o problema; "Validar" são as paradas para você confirmar que entendi certo.)

**O que foi feito** — Você respondeu que a conferência é feita hoje à mão, por uma pessoa, duas vezes por
mês, e que o erro mais comum é nota lançada em duplicidade. Você disse que tem um mês de notas em PDF
como amostra (um exemplo real do que entra); eu li dez delas e todas têm o número da nota e o CNPJ no
mesmo lugar.

**Agora: etapa 4 — Abordagens** — Com o problema entendido, eu mostro jeitos diferentes de resolver
(abordagens) e recomendo um. Nenhum deles é construído agora: esta etapa só escolhe o caminho. O que
fica de fora por enquanto, eu anoto para depois (é a regra de não construir o que não é necessário
agora).

**Sua decisão** — **Qual abordagem seguimos?**
- **1 — planilha de conferência gerada a partir dos PDFs** (recomendada): um programa lê os PDFs e monta
  a planilha com as duplicidades marcadas; você confere na planilha, como já faz. Menos mudança na sua
  rotina; funciona com a amostra que você tem.
- **2 — sistema com tela própria**: além de ler os PDFs, mostra as notas numa tela e pede a sua
  aprovação uma a uma. Mais completo, mas leva mais tempo e exige decidir mais coisas antes.
- **3 — só o alerta de duplicidade por e-mail**: o programa avisa quando encontra duas notas iguais e
  nada mais. Mais rápido de fazer, mas não resolve o resto da conferência.
- **não sei** — eu explico a diferença com um exemplo das suas notas.

**Próximo passo** — Com a sua escolha, eu apresento o primeiro checkpoint (a parada para você confirmar
que entendi certo) antes de gravar o documento.
