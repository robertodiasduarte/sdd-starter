# Changelog

## 1.1.0 - 2026-09-30

- A `ux-review` gerada segue a pasta do SDD do método: `sdd/` na raiz do projeto (ou a pasta do SDD que o projeto já usa), com os documentos lado a lado, sem subpastas — a mesma pasta em que o Define grava e o Design lê.
- Entrega em dois caminhos: no chat, os três artefatos para download; no agente, os documentos na pasta do SDD e a `ux-review/` pronta para instalar.
- Texto revisado e acentuado; a entrevista descreve o que pergunta, sem rotular quem responde.
- Catálogo de referências renomeado para `references/CATALOGO_DE_REFERENCIAS.md`.
- Removidos os registros internos de construção da 1.0.0.
- Validador: aceita texto acentuado; recusa `ux-review` que aponte para subpasta (`SUBPASTA_SDD_NA_FILHA`) ou sem a regra de pasta completa (`REGRA_DE_PASTA_AUSENTE`); arquivo vazio é checado, não pulado; ID citado em exceção ou histórico não conta como duplicado; acha a `ux-review/` na raiz do projeto quando os documentos estão na pasta do SDD, ou recebe `--skill`.
- `UX-CORE-008` (Consistência) mantém a severidade-base `SHOULD` também no gate da `ux-review`.

## 1.0.0 - 2026-09-21

- Criada a meta-skill `ux-review-builder`.
- Entrevista progressiva, catálogo inicial de referências (Apple/iPhone, ChatGPT, Nubank, Notion, Linear, Stripe e combinações) e análise opcional de URL com separação observado/desejado/recomendado.
- Modos Criação e Evolução do `UX_STANDARD.md`; dez princípios universais; IDs canônicos estáveis; gate `MUST` antes do Design.
- Modelos para `UX_STANDARD.md`, skill `ux-review` e `UX_REVIEW_TEMPLATE.md`; validador estrutural e testes locais.
