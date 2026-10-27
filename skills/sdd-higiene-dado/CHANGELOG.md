# Changelog

## 1.1.0 - 2026-10

- Seção "Como falar com o aluno": 3 etapas com nome fixo (Verificar · Explicar o alarme · Instalar) e os
  atendimentos Commit recusado e Desinstalar; toda resposta com status, o que foi feito, agora, decisão
  com opções e próximo passo; glossário na primeira vez; sem saída crua de comando; sem citar as
  próprias instruções.
- A pergunta de instalação vem com três opções (sim / não / ver o que ele recusa); o commit recusado
  pergunta "O que fazemos com este arquivo?" com corrigir / dado fictício / gravar mesmo assim.
  `--no-verify` continua só com a escolha explícita da pessoa, para aquele commit.
- Comandos, conferências e ordem dos passos não mudam.

## 1.0.0 - 2026-10

- Criada a skill `sdd-higiene-dado`: alarme de commit (pre-commit) instalado com OK explícito.
- Recusa CPF/CNPJ com dígito verificador válido (com e sem máscara, inclusive em CSV Latin-1),
  `.env`/`.env.*` (exceto `.env.example` e `.env.sample`), `.pfx`, `.p12`, `.pem` com chave privada e
  planilha nova de qualquer tamanho; número mascarado na mensagem.
- Mensagem ensina a corrigir, cita `git commit --no-verify` e diz como desinstalar.
- Não instala por cima de outro alarme (husky, `core.hooksPath`, pre-commit próprio); desinstalar
  remove só o alarme desta skill.
