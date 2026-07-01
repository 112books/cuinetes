#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════
#  Cuinetes — Script de deploy i gestió
#  Ús: ./sync-cuinetes.sh
# ═══════════════════════════════════════════════════════════════════════

set -euo pipefail

# ── Variables ────────────────────────────────────────────────────────────
REMOTE="origin"
BUILD_DIR="public"
BRANCH_PROD="main"
REPO_PROD="https://cuinetes.linuxbcn.com/"

# ── Colors i helpers ─────────────────────────────────────────────────────
RED='\033[0;31m'
GRN='\033[0;32m'
YLW='\033[1;33m'
BLU='\033[0;34m'
DIM='\033[2m'
RST='\033[0m'

print() { echo -e "${BLU}▶${RST} $1"; }
ok()    { echo -e "${GRN}✓${RST} $1"; }
err()   { echo -e "${RED}✗ Error:${RST} $1" >&2; }
warn()  { echo -e "${YLW}⚠${RST}  $1"; }
dim()   { echo -e "${DIM}  $1${RST}"; }

# ── Funcions ──────────────────────────────────────────────────────────────

status() {
  echo ""
  CURRENT=$(git branch --show-current)
  print "Branca actual: ${YLW}${CURRENT}${RST}"
  echo ""
  git status --short
  echo ""
  dim "Últims commits:"
  git log --oneline -5
  echo ""
}

sync() {
  CURRENT=$(git branch --show-current)
  print "Sincronitzant amb ${REMOTE}/${CURRENT}..."

  git add -A

  if ! git diff --cached --quiet; then
    read -r -p "  Missatge de commit: " msg
    [[ -z "$msg" ]] && msg="Auto-sync $(date '+%Y-%m-%d %H:%M')"
    git commit -m "$msg"
  else
    print "Sense canvis locals per cometre."
  fi

  git pull --rebase "$REMOTE" "$CURRENT" || {
    err "Pull/rebase fallat. Resol els conflictes manualment i torna a executar."
    exit 1
  }

  git push "$REMOTE" "$CURRENT" || exit 1
  ok "Sync complet → ${REMOTE}/${CURRENT}"
  dim "GitHub Action desplegarà a ${REPO_PROD}"
  dim "Segueix el progrés: https://github.com/112books/cuinetes/actions"
}

server_local() {
  print "Arrancant servidor local..."
  dim "http://localhost:1313  —  Ctrl+C per aturar"
  echo ""
  hugo server -D
}

build_local() {
  print "Build local (amb drafts)..."
  hugo --minify --buildDrafts || exit 1
  ok "Build correcte → ./${BUILD_DIR}/"
}

nova_recepta() {
  read -r -p "  Slug de la recepta (ex: coca-de-recapte): " slug
  if [[ -z "$slug" ]]; then err "El slug no pot estar buit."; exit 1; fi
  hugo new receptes/"${slug}".md
  ok "Creat: content/receptes/${slug}.md"
  dim "Recorda afegir la imatge a: static/images/receptes/${slug}.jpg"
}

# ── Menú ──────────────────────────────────────────────────────────────────

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " Cuinetes — Deploy & Gestió"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
CURRENT=$(git branch --show-current 2>/dev/null || echo "?")
echo -e " Branca: ${YLW}${CURRENT}${RST}"
echo ""
echo " 1) Status del repo"
echo " 2) Sync  (commit + pull --rebase + push)"
echo " 3) Servidor local  →  localhost:1313"
echo " 4) Build local (amb drafts)"
echo "───────────────────────────────────────"
echo " 5) Deploy producció → GitHub Pages (main)"
echo "───────────────────────────────────────"
echo " r) Nova recepta"
echo "───────────────────────────────────────"
echo " 0) Sortir"
echo ""

read -r -p "Opció: " opt
echo ""

case $opt in
  1) status ;;
  2) sync ;;
  3) server_local ;;
  4) build_local ;;
  5)
    CURRENT=$(git branch --show-current)
    if [[ "$CURRENT" != "$BRANCH_PROD" ]]; then
      warn "No estàs a '${BRANCH_PROD}' (estàs a '${CURRENT}')."
      exit 1
    fi
    print "Pujant a GitHub (branca ${BRANCH_PROD})..."
    git pull --rebase "$REMOTE" "$BRANCH_PROD" || exit 1
    git push "$REMOTE" "$BRANCH_PROD" || exit 1
    ok "Deploy producció iniciat → GitHub Pages"
    dim "Segueix el progrés: https://github.com/112books/cuinetes/actions"
    ;;
  r) nova_recepta ;;
  0) exit 0 ;;
  *) err "Opció no vàlida: '${opt}'"; exit 1 ;;
esac

echo ""
