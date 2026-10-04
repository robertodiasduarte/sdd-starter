# Changelog — sdd-kb

## 2.0.0 — out/2026

**Perfil normativo**, para bases de legislação e normas que alimentam agentes e software.

- O passo 1 pergunta se o domínio tem regra que vale por período e qual é a data-base; a resposta vira `perfil: normativo | geral` no registro do domínio.
- Novos tipos no perfil normativo: `rules/` (regra atômica com vigência, fonte, status, implementação e teste), `fontes/CATALOGO.md` (degrau normativo, versão, data de captura, SHA-256), `tabelas/AAAA-MM-DD/` (valores por vigência) e `casos/` (entrada → resultado esperado).
- `RULE_MAP.md` gerado por `scripts/kb_normativo.py rule-map` — regra → fonte com localizador → status → conflito → implementação → teste → severidade → código.
- Hierarquia normativa em `references/sourcing.md`: regra sustentada só por doutrina ou prática própria não pode ser `confirmado`. "A data do arquivo e o nome não provam vigência."
- Conflito entre fontes é primitiva: `conflito_com` na regra e seção obrigatória no `index.md`.
- `validate_kb.py`: checagens do perfil normativo (vigência com data real do calendário, fonte catalogada, SHA-256 do arquivo local, tabela × pasta, sobreposição de tabelas, caso dentro da vigência, RULE_MAP sem deriva, "Vale para:" em conceitos e receitas); `--strict` reprova base normativa `PENDENTE DE REVISÃO`; aviso "parece normativo" para domínio geral com marcadores de norma.
- `references/kb-protocol.md` documenta os tipos de apoio que o acervo já usava: `reference`, `spec` e o registro.
- Aviso de responsabilidade reforçado: a base normativa diz, no `index.md`, que não é aconselhamento tributário.
- Perfil `geral` (o padrão) inalterado: os domínios existentes continuam passando ou reprovando exatamente como na 1.0.1.

## 1.0.1 — out/2026

- `validate_kb.py` deixa de acusar como placeholder o JSON e as expressões dentro de código (bloco cercado ou `inline`); dentro de código só `{{MAIUSCULA}}` conta. No acervo de referência: de 1.188 para 5 acusos.
- `gate.sh` exige também fixtures boas e passa a rodar no CI.

## 1.0.0 — out/2026

- Primeira versão pública.
