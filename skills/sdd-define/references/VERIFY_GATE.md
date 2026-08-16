# Verify Gate

## Purpose

Transformar aceitação em um stop condition objetivo. O gate é um único mecanismo pass/fail que poderá ser usado depois por Build/Release ou por validação humana explícita.

## Canonical block

```yaml
verify_gate:
  kind: test
  cmd: "comando real do projeto"
  pass_when: "exit 0"
  threshold: "—"
  manual_fallback: "—"
```

## Fields

| Field | Required | Meaning |
|---|---|---|
| kind | sempre | `test`, `smoke`, `eval`, `typecheck` ou `manual-ux` |
| cmd | exceto manual-ux | comando executável real |
| pass_when | sempre | `exit 0`, `exit N`, `contains: TEXT` ou critério humano no manual-ux |
| threshold | eval | alvo numérico documentado e embutido no comando |
| manual_fallback | manual-ux | checklist humano objetivo |

Não usar comentário inline nos valores do bloco.

## Taxonomy

| kind | Quando usar |
|---|---|
| test | lógica/estado/comportamento testável |
| smoke | endpoint ou integração real |
| eval | qualidade medida contra threshold |
| typecheck | compilação/tipos é o done signal |
| manual-ux | percepção/UX genuinamente humana |

## From EARS to gate

- `When` → disparar evento e verificar resposta.
- `If/Then` → provocar falha/trigger pelo caminho real e verificar handling.
- `While` → montar o estado e verificar comportamento.
- `Where` → testar matriz on/off.
- `shall continue to` → caso explícito de regressão.

## Rules

- Nunca inventar comando de projeto.
- `manual-ux` não é fallback para desconhecimento de comando.
- Um Verify Gate incompleto bloqueia conclusão do DEFINE.
- Para eval, o threshold precisa ser numérico.
- Para manual-ux, `cmd` deve ser `N/A (manual-ux)` e o checklist deve ser verificável.
