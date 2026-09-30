---
name: "ux-review"
description: "Revisa a UX/CX de uma feature depois do Define e antes do Design, usando o UX_STANDARD.md canônico do projeto e o UX_REVIEW_TEMPLATE.md. Use quando houver uma feature especificada que precise de jornada, conformidade com regras canônicas, estados, acessibilidade, responsividade, copy, riscos, priorização e handoff para o Design. Os achados citam IDs canônicos quando aplicável; qualquer MUST bloqueia o Design até correção ou aceite explícito. Não altera o UX_STANDARD.md automaticamente e não substitui a auditoria do sistema."
license: "MIT"
metadata:
  author: "Roberto Dias Duarte"
  methodology: "Metodologia de Roberto Dias Duarte"
---

# UX Review

## Quick start

**Pasta do SDD.** Os documentos do SDD ficam em `sdd/` na raiz do projeto — pasta visível, igual em qualquer agente. Se o projeto já tiver `.claude/sdd/`, continue nela. Os documentos ficam lado a lado, sem subpastas.

Ler obrigatoriamente, nessa pasta:
- `DEFINE_{FEATURE}.md`;
- `UX_STANDARD.md`;
- `UX_REVIEW_TEMPLATE.md`.

Ler quando disponíveis: o BRAINSTORM da feature, capturas de tela, mockups, design system, tokens, componentes existentes e URLs relacionadas.

Gravar `UX_REVIEW_{FEATURE}.md` na mesma pasta, seguindo o modelo. A fase Design lê esse arquivo dali.

## Quando usar / Quando não usar

Usar depois do Define e antes do Design, para revisar a experiência da feature contra a fonte canônica do projeto.

Não usar para alterar o `UX_STANDARD.md`, definir a arquitetura técnica, auditar segurança ou implementação como objetivo principal, nem aprovar silenciosamente uma feature com `MUST` pendente.

## Dados necessários

Obrigatórios: o DEFINE da feature, o UX_STANDARD vigente e o UX_REVIEW_TEMPLATE vigente.

Complementares: BRAINSTORM, telas, componentes, design system, referências, URLs e evidências do comportamento atual.

Se uma fonte obrigatória estiver ausente, bloquear a conclusão e pedir o artefato. Não reconstruir o padrão de memória. Se o DEFINE estiver em outra pasta, usar essa pasta, sem criar subpastas.

## Procedimento passo a passo

### 1. Carregar o contexto

Extrair do DEFINE: usuário, objetivo, dor, critérios de sucesso, restrições e o que está fora do escopo. Ler a versão e as regras aplicáveis do UX_STANDARD.

### 2. Mapear a jornada

Usar: Before -> Entry -> Core Action -> Feedback -> Recovery -> Completion -> Follow-up.

Em cada etapa, registrar intenção, emoção/risco, fricção, feedback necessário e recuperação.

### 3. Avaliar a conformidade canônica

Para cada regra relevante do UX_STANDARD, marcar `CONFORME`, `MUST`, `SHOULD`, `COULD`, `WONT` ou `NAO AVALIAVEL`. Citar o ID da regra e a evidência concreta.

Não marcar `CONFORME` sem evidência suficiente.

### 4. Aplicar o gate universal

Uma violação comprovada de `UX-CORE-*` recebe a severidade-base do UX_STANDARD: `MUST` em todos os princípios universais, exceto `UX-CORE-008` (Consistência), que nasce em `SHOULD` — a menos que o projeto a tenha endurecido. Conflito relevante entre DEFINE e UX_STANDARD é `MUST`.

### 5. Revisar as dimensões da experiência

Cobrir clareza, eficiência, confiança, navegação, hierarquia, densidade, acessibilidade, responsividade, estados, copy, feedback, recuperação, consistência e os padrões específicos do projeto.

### 6. Revisar os estados

Tratar loading, empty, error, success, partial data, permission denied e disabled quando aplicáveis. A ausência de um estado essencial capaz de quebrar a tarefa é `MUST`.

### 7. Avaliar gamificação apenas quando aplicável

Usar somente se o UX_STANDARD ou o objetivo da feature justificar progresso, marcos, feedback positivo ou outra mecânica. Não recomendar engajamento manipulativo.

### 8. Produzir o handoff para o Design

Escrever requisitos de comportamento, componentes necessários, estados, copy, direção visual, acessibilidade, responsividade e critérios de aceite.

Não desenhar a arquitetura técnica nem substituir o Design.

### 9. Determinar o resultado do gate

- Sem `MUST`: `READY FOR DESIGN`, mantendo SHOULD/COULD no handoff.
- Com `MUST` não resolvido: `BLOCKED FOR DESIGN`.
- Com `MUST` aceito explicitamente: registrar a exceção e o responsável; não marcar como conforme.

### 10. Tratar a evolução do padrão

Se a revisão mostrar que o UX_STANDARD precisa mudar, registrar uma `Proposta de evolução canônica`. Não editar a fonte canônica: encaminhar a mudança para o fluxo de governança (a meta-skill `ux-review-builder`, no modo Evolução).

## Validações e checklist de qualidade

- jornada mapeada;
- regras canônicas aplicáveis identificadas;
- achados com IDs e evidências;
- nenhum `CONFORME` sem evidência;
- dez princípios universais considerados;
- estados essenciais avaliados;
- acessibilidade e responsividade tratadas;
- copy e feedback tratados;
- conflito DEFINE x UX_STANDARD bloqueado;
- `MUST` bloqueia o Design, salvo aceite explícito;
- nenhuma mudança automática no UX_STANDARD;
- handoff concreto para o Design;
- relatório gravado na pasta do SDD, sem subpastas;
- modelo preenchido sem valores fixos de outro projeto.

## Tratamento de exceções

**UX_STANDARD ausente:** bloquear a conclusão e pedir a fonte canônica.

**DEFINE ausente:** bloquear a conclusão e pedir o documento do Define da feature.

**Regra ambígua:** marcar `NAO AVALIAVEL` e abrir pergunta. Não inventar interpretação canônica.

**Evidência visual insuficiente:** revisar o que o DEFINE e o padrão permitem e marcar o restante como `NAO AVALIAVEL`.

**Pedido para mudar o padrão:** registrar a sugestão e encaminhar à governança; não editar.

**MUST aceito:** registrar aceite, motivo e responsável. O achado continua sendo violação aceita.

## Examples

**Conforme.** `UX-STATE-004` exige confirmação inequívoca de sucesso e o DEFINE especifica mensagem persistente e próximo passo. Registrar `CONFORME` com a evidência.

**MUST.** O fluxo permite enviar duas vezes sem indicar processamento, violando `UX-CORE-002` e `UX-CORE-007`. Registrar `MUST`, a recomendação e `BLOCKED FOR DESIGN`.

**Não avaliável.** O UX_STANDARD exige foco visível, mas não há mockup nem comportamento implementado. Marcar `NAO AVALIAVEL`; não afirmar conformidade.

## Texto canônico de recusa

"Não vou alterar o UX_STANDARD.md durante esta revisão. Posso registrar a mudança proposta para o fluxo de governança."

"Existe um MUST pendente; o gate permanece bloqueado para o Design até correção ou aceite explícito do responsável."

## Base documental

Fonte canônica: `UX_STANDARD.md`. Formato de saída: `UX_REVIEW_TEMPLATE.md`. Requisitos funcionais: o DEFINE da feature. Os três ficam na pasta do SDD, lado a lado.

## Inventário do bundle

Esta skill é gerada pela `ux-review-builder` e instalada como skill do projeto no agente que executa o SDD. Ela depende dos três documentos acima na pasta do SDD.

## Metodologia e autoria

Esta skill foi construída com a metodologia de Roberto Dias Duarte.
