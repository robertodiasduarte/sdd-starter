# Como falar com o aluno — sdd-kb

Quem monta uma base de conhecimento sabe muito do assunto e pouco de como a IA consulta. A seção "Como
falar com o aluno" do `SKILL.md` dá o formato; este arquivo dá as palavras e um exemplo inteiro.

## Glossário (explique na primeira vez em que o termo aparecer)

- base de conhecimento (KB) — "o que você sabe sobre um assunto, organizado de um jeito que a IA consegue
  consultar de verdade";
- domínio — "um assunto com fronteira clara: dá para dizer 'isto não é daqui' sem hesitar";
- conceito — "um arquivo para entender algo (o que é, quando se aplica)";
- receita — "um arquivo para fazer algo (passo a passo, com o resultado esperado)";
- índice — "a porta de entrada: a lista do que existe na base e onde está";
- perfil normativo — "o modo para lei, norma e alíquota: cada regra ganha a data em que vale";
- vigência — "o período em que uma regra vale; sem isso o arquivo certo hoje fica errado no ano que vem";
- fonte — "de onde a informação veio; no perfil normativo, com a impressão digital do arquivo (SHA-256),
  que prova que a fonte não mudou";
- revisão do profissional — "a conferência que é sua: eu organizo e redijo, quem responde pelo conteúdo
  é você".

Não fale em chunk, embedding, markdown ou frontmatter sem traduzir: "um pedaço do texto", "a forma como
a IA encontra o texto", "o formato de texto simples dos arquivos", "o cabeçalho do arquivo".

## Status desta skill, preenchido

`KB: ▶️ 1 Domínio · ⬜ 2 Entender × fazer · ⬜ 3 Escrever · ⬜ 4 Fonte e índice · ⬜ 5 Revisão do profissional`

## Exemplo de resposta completa

Situação: um contador quer "ensinar a IA sobre o Simples Nacional do escritório". É a primeira resposta
depois da linha de identificação.

**Status** — `KB: ▶️ 1 Domínio · ⬜ 2 Entender × fazer · ⬜ 3 Escrever · ⬜ 4 Fonte e índice · ⬜ 5 Revisão do profissional`
(no Status: "Domínio" é o assunto com fronteira clara; "Entender × fazer" separa o que é para entender do
que é para fazer; "Fonte e índice" registra de onde veio cada informação e a lista do que existe na base.)

**O que foi feito** — Você pediu uma base de conhecimento (o que você sabe sobre um assunto, organizado
para a IA consultar) sobre o Simples Nacional. Ainda não há pasta de base neste projeto; nada foi criado.

**Agora: etapa 1 — Domínio** — Primeiro a gente delimita o assunto (o domínio): o que entra e, sobretudo,
o que fica de fora — "Simples Nacional" inteiro é grande demais para terminar; "enquadramento e cálculo
mensal do anexo III" é um recorte que se escreve. Antes de escrever, preciso saber se este assunto tem
regra que vale por período (alíquota, prazo, lei): se tiver, cada regra ganha a data em que vale, porque
uma regra certa hoje fica errada no ano que vem sem mudar uma linha.

**Sua decisão** — **Este domínio tem regra que vale por período — lei, alíquota, prazo, leiaute de
documento fiscal?**
- **sim** — a base entra no perfil normativo: toda regra ganha vigência, toda fonte ganha a impressão
  digital do arquivo, e eu pergunto a data-base (a data em que você confere o conteúdo contra as fontes).
- **não** — perfil geral: conceitos e receitas, sem datas de vigência.
- **não sei** — me diga um exemplo do que você quer registrar e eu digo qual perfil é.

**Próximo passo** — Com o perfil decidido, eu separo o que é para entender do que é para fazer (etapa 2) a
partir do que você me contar.
