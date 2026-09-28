#!/usr/bin/env bash
# checar.sh — diagnóstico read-only do ambiente para trabalhar com SDD neste repositório.
# Faz as verificações e imprime o relatório JÁ NO FORMATO FINAL (a skill só repassa):
#   🔴 Impede o trabalho   (cada item com o comando que resolve)
#   ⚠️ Vale arrumar
#   ✅ resumo em uma linha
# Blocos vazios não aparecem. Ambiente saudável = só a linha ✅.
#
# Não instala, não configura, não grava nada. Roda em bash (macOS, Linux, Git Bash no Windows).
# Uso: bash checar.sh            (de dentro da pasta do projeto)

set -u

IMPEDE=""
ARRUMAR=""
add_impede()  { IMPEDE="${IMPEDE}- $1"$'\n'"  $2"$'\n'; }
add_arrumar() { ARRUMAR="${ARRUMAR}- $1"$'\n'"  $2"$'\n'; }
tem() { command -v "$1" >/dev/null 2>&1; }

relatorio() {   # $1 = linha de resumo (sem o ✅)
  [ -n "${IMPEDE}" ] && printf '🔴 Impede o trabalho\n%s\n' "${IMPEDE}"
  [ -n "${ARRUMAR}" ] && printf '⚠️ Vale arrumar\n%s\n' "${ARRUMAR}"
  if [ -z "${IMPEDE}" ] && [ -z "${ARRUMAR}" ]; then
    printf '✅ Pronto: %s\n' "$1"
  else   # "✅ Repo …" (maiúscula; bash 3.2 não tem ${1^})
    printf '✅ %s%s\n' "$(printf '%s' "$1" | cut -c1 | tr '[:lower:]' '[:upper:]')" "$(printf '%s' "$1" | cut -c2-)"
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

# ── resumo ───────────────────────────────────────────────────────────────────
case "${FRENTES}" in
  0) TXT_FRENTES="nenhuma frente aberta" ;;
  1) TXT_FRENTES="1 frente aberta" ;;
  *) TXT_FRENTES="${FRENTES} frentes abertas" ;;
esac
EDITOR_ACHADO=""
for e in code cursor subl; do tem "${e}" && { EDITOR_ACHADO="${e}"; break; }; done
RESUMO="repo ${REPO}, branch ${BRANCH}, ${TXT_FRENTES}, ${AGENTES}${EDITOR_ACHADO:+, editor ${EDITOR_ACHADO}}"
relatorio "${RESUMO}"
exit 0
