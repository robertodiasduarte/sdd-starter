# Verify Gate no Build

## Regra

O bloco `verify_gate` do DEFINE é o acceptance gate bloqueante.

Não substituir por lint/test genérico.

Campos esperados:
- `kind`;
- `cmd`;
- `pass_when`;
- `threshold`;
- `manual_fallback`.

Kinds:
- `test`;
- `smoke`;
- `eval`;
- `typecheck`;
- `manual-ux`.

## Runner

Se o projeto possuir `scripts/verify-gate.sh` compatível, preferi-lo.

Caso contrário:
- ler o `cmd`;
- verificar se é real, pertinente e não destrutivo;
- executar no contexto correto;
- avaliar `pass_when`.

Nunca instalar pacote ou executar mudança destrutiva apenas para “fazer o gate rodar” sem consentimento.

## Exit contract

| Exit | Significado | Ação |
|---:|---|---|
| 0 | green | prosseguir |
| 2 | red | abortar sucesso; corrigir e rerodar |
| 3 | inconclusivo | resolver tool/infra; não marcar green |
| 4 | manual-ux | mostrar checklist e exigir receipt |
| 5 | clarification pending | voltar ao humano/spec |
| 64 | gate malformado/ausente | DEFINE inválido |

## manual-ux

Nunca autoaprovar.

Receipt mínimo:
- pessoa que validou;
- data;
- resultado;
- observações, se houver.

Somente receipt positivo libera o Build como Complete.

## smoke 403 / infra noise

Não assumir regression automaticamente.

Se a evidência indicar bloqueio do runner/WAF:
- classificar como inconclusivo;
- executar a partir de ambiente apropriado quando possível;
- registrar no relatório.

## Build Report

Registrar:
- kind;
- comando/método;
- resultado;
- exit;
- output/evidência;
- receipt humano se aplicável.

Sem essa evidência, Final Status não pode ser COMPLETE.
