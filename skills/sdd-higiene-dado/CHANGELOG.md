# Changelog

## 1.0.0 - 2026-10

- Criada a skill `sdd-higiene-dado`: alarme de commit (pre-commit) instalado com OK explícito.
- Recusa CPF/CNPJ com dígito verificador válido (com e sem máscara, inclusive em CSV Latin-1),
  `.env`/`.env.*` (exceto `.env.example` e `.env.sample`), `.pfx`, `.p12`, `.pem` com chave privada e
  planilha nova de qualquer tamanho; número mascarado na mensagem.
- Mensagem ensina a corrigir, cita `git commit --no-verify` e diz como desinstalar.
- Não instala por cima de outro alarme (husky, `core.hooksPath`, pre-commit próprio); desinstalar
  remove só o alarme desta skill.
