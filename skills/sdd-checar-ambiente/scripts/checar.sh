#!/usr/bin/env bash
# checar.sh — diagnóstico read-only do ambiente para trabalhar com SDD neste repositório.
# Faz as verificações e imprime o relatório JÁ NO FORMATO FINAL (a skill só repassa):
#   🔴 Dado exposto        (senha ou certificado já salvo no git)
#   🔴 Impede o trabalho   (cada item com o comando que resolve)
#   ⚠️ Vale arrumar
#   ✅ resumo em uma linha
# Blocos vazios não aparecem. Ambiente saudável = só a linha ✅.
#
# Não instala, não configura, não grava nada. Roda em bash (macOS, Linux, Git Bash no Windows).
# Única saída de rede: uma consulta anônima ao GitHub (3s no máximo) para saber se o repositório
# é público. Se falhar, nada é dito sobre isso.
# Uso: bash checar.sh            (de dentro da pasta do projeto)

set -u

EXPOSTO=""
IMPEDE=""
ARRUMAR_DADO=""   # ⚠️ de dado vem antes dos outros ⚠️ (ordem por consequência)
ARRUMAR=""
add_exposto() { EXPOSTO="${EXPOSTO}- $1"$'\n'"  $2"$'\n'; }
add_impede()  { IMPEDE="${IMPEDE}- $1"$'\n'"  $2"$'\n'; }
add_arrumar_dado() { ARRUMAR_DADO="${ARRUMAR_DADO}- $1"$'\n'"  $2"$'\n'; }
add_arrumar() { ARRUMAR="${ARRUMAR}- $1"$'\n'"  $2"$'\n'; }
tem() { command -v "$1" >/dev/null 2>&1; }

# Identificação desta skill, lida do SKILL.md ao lado (fonte única da versão).
SKILL_MD="$(cd "$(dirname "$0")/.." 2>/dev/null && pwd)/SKILL.md"
meta() { grep -m1 "^  $1:" "${SKILL_MD}" 2>/dev/null | sed 's/^[^:]*: *//; s/"//g'; }
VERSAO="$(meta version)"; ATUAL="$(meta updated)"
case "${ATUAL#*-}" in
  01) MES=jan ;; 02) MES=fev ;; 03) MES=mar ;; 04) MES=abr ;; 05) MES=mai ;; 06) MES=jun ;;
  07) MES=jul ;; 08) MES=ago ;; 09) MES=set ;; 10) MES=out ;; 11) MES=nov ;; 12) MES=dez ;; *) MES="" ;;
esac
IDENT=""
[ -n "${VERSAO}" ] && [ -n "${MES}" ] && IDENT=" · sdd-checar-ambiente v${VERSAO} · ${MES}/${ATUAL%%-*} · versão atual: https://github.com/robertodiasduarte/sdd-starter/releases/latest"

relatorio() {   # $1 = linha de resumo (sem o ✅)
  ARRUMAR="${ARRUMAR_DADO}${ARRUMAR}"
  [ -n "${EXPOSTO}" ] && printf '🔴 Dado exposto\n%s\n' "${EXPOSTO}"
  [ -n "${IMPEDE}" ] && printf '🔴 Impede o trabalho\n%s\n' "${IMPEDE}"
  [ -n "${ARRUMAR}" ] && printf '⚠️ Vale arrumar\n%s\n' "${ARRUMAR}"
  if [ -z "${EXPOSTO}" ] && [ -z "${IMPEDE}" ] && [ -z "${ARRUMAR}" ]; then
    printf '✅ Pronto: %s%s\n' "$1" "${IDENT}"
  else   # "✅ Repo …" (maiúscula; bash 3.2 não tem ${1^})
    printf '✅ %s%s%s\n' "$(printf '%s' "$1" | cut -c1 | tr '[:lower:]' '[:upper:]')" "$(printf '%s' "$1" | cut -c2-)" "${IDENT}"
  fi
}

# ── 2. agentes (antes do git: vale mesmo fora de repositório) ─────────────────
AGENTES=""
if tem claude; then AGENTES="Claude Code $(claude --version 2>/dev/null | head -1 | awk '{print $1}')"; fi
if tem codex; then
  v="$(codex --version 2>/dev/null | head -1 | awk '{print $NF}')"
  AGENTES="${AGENTES:+${AGENTES}, }Codex ${v}"
fi
[ -n "${AGENTES}" ] || AGENTES="nenhum agente de código no terminal"

# ── 1. onde estou ────────────────────────────────────────────────────────────
if ! tem git; then
  add_impede "O git não está instalado — sem ele não há frentes nem publicação." \
             "Instale em https://git-scm.com/downloads e abra o terminal de novo."
  relatorio "${AGENTES}"; exit 0
fi
RAIZ="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [ -z "${RAIZ}" ]; then
  add_impede "Esta pasta não é um repositório git — provavelmente o terminal foi aberto na pasta errada." \
             "cd <pasta do projeto>   (ou, se o projeto ainda não tem git: git init)"
  relatorio "pasta $(basename "$(pwd)"), ${AGENTES}"; exit 0
fi
# sed, não awk '{print $2}': caminho com espaço ("Ana Silva/Projetos/…") quebraria no 1º espaço.
REPO="$(basename "$(git worktree list --porcelain | sed -n 's/^worktree //p' | head -1)")"
BRANCH="$(git branch --show-current 2>/dev/null)"; BRANCH="${BRANCH:-HEAD destacado}"

# ── 3. git utilizável ────────────────────────────────────────────────────────
[ -n "$(git config user.name 2>/dev/null)" ] || add_impede \
  "O git não tem nome configurado — o primeiro commit vai falhar." \
  "git config --global user.name \"Seu Nome\""
[ -n "$(git config user.email 2>/dev/null)" ] || add_impede \
  "O git não tem e-mail configurado — o primeiro commit vai falhar." \
  "git config --global user.email \"voce@exemplo.com\""

PRINCIPAL=""
if [ -z "$(git remote 2>/dev/null)" ]; then
  add_arrumar "O repositório não tem remoto — nada que você fizer sai desta máquina." \
              "git remote add origin <url do repositório>"
else
  PRINCIPAL="$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's#^origin/##')"
  if [ -z "${PRINCIPAL}" ]; then
    for b in main master; do git show-ref --verify --quiet "refs/remotes/origin/${b}" && { PRINCIPAL="${b}"; break; }; done
  fi
fi

# Repositório público? Só GitHub; consulta anônima (repo privado responde 404 sem login).
# Público sozinho não é problema: só aparece no resumo, e agrava o 🔴 Dado exposto.
PUBLICO=0
SLUG="$(git remote get-url origin 2>/dev/null \
  | sed -n -E 's#^(https?://([^@/]+@)?|ssh://([^@/]+@)?|git@)github\.com[:/]([^/]+/[^/]+)$#\4#p' | sed 's#\.git$##; s#/$##')"
if [ -n "${SLUG}" ]; then
  if tem curl; then
    [ "$(curl -s -o /dev/null -w '%{http_code}' --max-time 3 "${SDD_CHECAR_GITHUB_API:-https://api.github.com}/repos/${SLUG}" 2>/dev/null)" = "200" ] && PUBLICO=1
  elif tem gh; then
    [ "$(gh repo view "${SLUG}" --json visibility -q .visibility 2>/dev/null)" = "PUBLIC" ] && PUBLICO=1
  fi
fi

# ── 4. frentes (worktrees) ───────────────────────────────────────────────────
# A 1ª entrada de `git worktree list` é o checkout principal — NÃO é frente.
FRENTES=0
PRIMEIRA=1
wt=""; br=""; prunable=0
fecha_entrada() {
  if [ -n "${wt}" ]; then
    if [ "${PRIMEIRA}" -eq 1 ]; then
      PRIMEIRA=0
    else
      FRENTES=$((FRENTES + 1))
      if [ "${prunable}" -eq 1 ] || [ ! -d "${wt}" ]; then
        add_arrumar "A frente ${wt} não existe mais no disco (a pasta foi apagada à mão)." "git worktree prune"
      elif [ -n "${br}" ] && [ -n "${PRINCIPAL}" ] && [ "${br}" != "${PRINCIPAL}" ] \
           && git merge-base --is-ancestor "${br}" "origin/${PRINCIPAL}" 2>/dev/null \
           && git reflog show --format='%gs' "refs/heads/${br}" 2>/dev/null | grep -q '^commit'; then
        add_arrumar "A frente ${wt} (branch ${br}) já foi integrada na ${PRINCIPAL} e continua aberta." \
                    "git worktree remove \"${wt}\" && git branch -d ${br}"
      fi
    fi
  fi
  wt=""; br=""; prunable=0
}
while IFS= read -r l; do
  case "${l}" in
    "worktree "*) fecha_entrada; wt="${l#worktree }" ;;
    "branch refs/heads/"*) br="${l#branch refs/heads/}" ;;
    prunable*) prunable=1 ;;
  esac
done < <(git worktree list --porcelain)
fecha_entrada

# ── 5. ferramentas do projeto (na raiz desta pasta de trabalho) ──────────────
if [ -f "${RAIZ}/package.json" ] && [ ! -d "${RAIZ}/node_modules" ]; then
  add_impede "As dependências do projeto não estão instaladas (package.json sem node_modules)." "npm install"
fi
if [ -f "${RAIZ}/composer.json" ] && [ ! -d "${RAIZ}/vendor" ]; then
  add_impede "As dependências PHP não estão instaladas (composer.json sem vendor/)." "composer install"
fi
if [ -f "${RAIZ}/requirements.txt" ] && [ ! -d "${RAIZ}/.venv" ] && [ ! -d "${RAIZ}/venv" ]; then
  add_arrumar "requirements.txt sem ambiente virtual nesta pasta (as dependências podem estar instaladas fora dele)." \
              "python3 -m venv .venv && .venv/bin/pip install -r requirements.txt   (Windows: .venv\\Scripts\\pip)"
fi
if [ -f "${RAIZ}/.env.example" ] && [ ! -f "${RAIZ}/.env" ] \
   && [ -n "$(git -C "${RAIZ}" ls-files .env.example 2>/dev/null)" ]; then
  add_arrumar "O projeto espera um .env (há .env.example) e ele não existe nesta pasta." "cp .env.example .env   (e preencha)"
fi

# ── 6. dado de cliente e segredos ────────────────────────────────────────────
# Só olha o que o git já guarda (ls-files / grep --cached) e a pasta; não abre nada para escrita.
if [ "${PUBLICO}" -eq 1 ]; then
  ONDE="Este repositório é público: o arquivo já está na internet."
else
  ONDE="Tirar do git não apaga do histórico: se já houve push, quem tem acesso ao repositório tem o arquivo."
fi
exposto() {   # $1 = caminho, $2 = o que é, $3 = medida que protege
  add_exposto "${2} ${1} está salvo no git. ${ONDE}" \
    "git rm --cached \"${1}\" && echo \"${1}\" >> .gitignore"$'\n'"  ${3}"
}
while IFS= read -r -d '' f; do
  b="$(basename "${f}" | tr '[:upper:]' '[:lower:]')"
  case "${b}" in
    .env.example|.env.sample) ;;
    .env|.env.*) exposto "${f}" "O arquivo de senhas" "Depois, troque as senhas e chaves que estão nele." ;;
    *.pfx|*.p12) exposto "${f}" "O certificado digital" "Depois, revogue o certificado com a autoridade certificadora e emita outro." ;;
  esac
done < <(git -C "${RAIZ}" ls-files -z 2>/dev/null)
# .pem só é segredo quando traz a chave privada; certificado público é comum e não alarma.
while IFS= read -r -d '' f; do
  exposto "${f}" "A chave privada" "Depois, gere uma chave nova e descarte esta."
done < <(git -C "${RAIZ}" grep --cached -l -z -I -e "PRIVATE KEY" -- '*.pem' '*.PEM' 2>/dev/null)

if [ -f "${RAIZ}/.env" ] && [ -z "$(git -C "${RAIZ}" ls-files .env 2>/dev/null)" ] \
   && ! git -C "${RAIZ}" check-ignore -q .env 2>/dev/null; then
  add_arrumar_dado "O .env desta pasta não está no .gitignore — o próximo \"git add .\" leva suas senhas para o git." \
                   "echo \".env\" >> .gitignore"
fi
if [ -f "${RAIZ}/package.json" ] && tem npm \
   && [ "$(cd "${RAIZ}" && npm config get ignore-scripts 2>/dev/null)" != "true" ]; then
  add_arrumar_dado "O npm roda os scripts de instalação de qualquer pacote baixado — é por onde entram pacotes maliciosos." \
                   "npm config set ignore-scripts true   (se um pacote parar de funcionar: npm rebuild <pacote> --ignore-scripts=false)"
fi

# ── resumo ───────────────────────────────────────────────────────────────────
case "${FRENTES}" in
  0) TXT_FRENTES="nenhuma frente aberta" ;;
  1) TXT_FRENTES="1 frente aberta" ;;
  *) TXT_FRENTES="${FRENTES} frentes abertas" ;;
esac
EDITOR_ACHADO=""
for e in code cursor subl; do tem "${e}" && { EDITOR_ACHADO="${e}"; break; }; done
[ "${PUBLICO}" -eq 1 ] && REPO="${REPO} (público no GitHub)"
RESUMO="repo ${REPO}, branch ${BRANCH}, ${TXT_FRENTES}, ${AGENTES}${EDITOR_ACHADO:+, editor ${EDITOR_ACHADO}}"
relatorio "${RESUMO}"
exit 0
