# Brainstorm Protocol

Este arquivo detalha a política conversacional da Fase 0.

## Estados

Tratar a sessão como uma sequência de estados:

1. `CONTEXT`
2. `DISCOVERY`
3. `SAMPLES`
4. `APPROACHES`
5. `SELECTION`
6. `YAGNI`
7. `VALIDATION_1`
8. `VALIDATION_2`
9. `HANDOFF_TO_DEFINE`

Não avançar para `APPROACHES` com menos de 3 respostas de descoberta. Não avançar para `HANDOFF_TO_DEFINE` sem seleção confirmada e 2 validações.

## Regra de uma pergunta por vez

Cada mensagem de coleta deve conter uma pergunta principal. Pode incluir opções de resposta, mas não deve empilhar perguntas independentes.

Preferência:
1. múltipla escolha quando houver opções conhecidas;
2. aberta quando o espaço ainda for desconhecido;
3. clarificação quando a resposta anterior não resolver a dúvida.

Evitar:
- perguntar propósito, usuários, prazo e sucesso na mesma mensagem;
- responder à própria pergunta com uma suposição;
- avançar depois de uma correção do usuário sem revisar o impacto.

## Sequência recomendada de descoberta

Adaptar à entrada, mas buscar estas dimensões:

### Propósito
Descobrir qual problema ou oportunidade precisa ser resolvido e por que isso importa agora.

### Usuário
Identificar quem sente a dor, usa a solução ou recebe o resultado.

### Restrições
Investigar integrações obrigatórias, tecnologias existentes, regras, prazo, orçamento, segurança ou limites operacionais relevantes.

### Sucesso
Buscar sinais observáveis de que a solução funcionou. Não inventar números.

Perguntas de exemplo são apenas padrões:
- "Qual é o principal resultado que você quer obter com isso?"
- "Quem é o usuário principal: (a) equipe interna, (b) cliente, (c) ambos, (d) outro?"
- "Existe alguma restrição que a solução obrigatoriamente precisa respeitar?"
- "Como você saberá que essa ideia deu certo?"

## Coleta de amostras

Fazer uma pergunta específica sobre grounding depois da descoberta inicial:

"Você tem algum material que possa ancorar a solução: (a) arquivos de entrada, (b) exemplos de saída esperada, (c) ground truth/dados verificados, (d) código/padrões relacionados, (e) nada disponível?"

Registrar:
- tipo;
- localização ou identificação;
- quantidade, quando conhecida;
- observações;
- como a amostra será usada.

## Construção de abordagens

Cada abordagem precisa representar uma escolha real. Exemplos de eixos de diferenciação:
- solução simples/manual assistida vs automação completa;
- síncrona vs assíncrona;
- regra determinística vs LLM;
- integração direta vs fila/eventos;
- extensão do sistema atual vs serviço separado.

A abordagem recomendada vem primeiro e deve incluir o raciocínio da recomendação. Não apresentar alternativas neutras sem orientar o usuário.

## Seleção

Pedir confirmação explícita. Registrar:
- abordagem escolhida;
- confirmação do usuário;
- razão principal da escolha.

Se a escolha for híbrida, transformar a combinação em uma abordagem coerente e validar novamente.

## YAGNI

Revisar cada item adicional contra duas perguntas:
1. É necessário para o MVP?
2. Resolve o problema central agora?

Classificar cada item como:
- manter;
- adiar;
- remover.

Documentar adiamentos e remoções. Um resultado com zero remoções é válido se a revisão tiver sido feita e justificada.

## Validações incrementais

Fazer no mínimo dois checkpoints depois da direção escolhida.

Sugestão para software:
- `Validation 1`: conceito, componentes, escopo e responsabilidades;
- `Validation 2`: fluxo de dados, tratamento de erro, dependências, observabilidade/operabilidade quando relevante.

Para fluxos não técnicos:
- `Validation 1`: experiência/processo e boundaries;
- `Validation 2`: dados, exceções e critérios de sucesso.

Registrar feedback e se houve ajuste.

## Honestidade epistemológica

Usar três categorias:
- `Provided`: dito pelo usuário;
- `Observed`: verificado em material acessível;
- `Inferred`: hipótese de trabalho.

Nunca escrever `Inferred` como se fosse `Observed`. Quando a inferência for decisiva para a abordagem, transformá-la em pergunta.

## Critério de conclusão

Somente concluir o Brainstorm e apresentar o handoff quando todos forem verdadeiros:
- `discovery_answers >= 3`
- `sample_question_asked = true`
- `approaches >= 2`
- `selected_approach_confirmed = true`
- `yagni_review_done = true`
- `validation_checkpoints >= 2`
- `draft_requirements_present = true`


## Handoff obrigatório para o SDD Define by RDD

Depois de gerar o BRAINSTORM, não usar comando de terminal ou sintaxe `/define` como próximo passo.

O `Next Step` deve conter **somente**:

Execute o **SDD Define by RDD**.

Não especificar se o SDD Define by RDD é GPT ou Skill. Não acrescentar upload, prompt, coleta paralela de amostras ou qualquer outra ação ao `Next Step`. A coleta de samples, ground truth, exemplos e código relacionado pertence ao estado `SAMPLES` desta Skill. Se algo continuar indisponível, registrar a lacuna no BRAINSTORM como `TBD`, limitação ou dependência conhecida.
