#!/usr/bin/env bash
# =============================================================================
#  Publica as alteracoes locais no repositorio oficial do painel:
#    https://github.com/anamazza/Indicadores_partos_Brasil2024
#
#  COMO USAR (Windows):
#   1. (uma unica vez) Baixe o repositorio:
#        git clone https://github.com/anamazza/Indicadores_partos_Brasil2024.git
#   2. Abra o "Git Bash" DENTRO da pasta do repositorio
#      (clique direito na pasta -> "Git Bash Here").
#   3. Rode:  bash publicar_no_github.sh
#   4. Quando o GitHub pedir login, autorize na janela que abrir.
#
#  O script NAO apaga historico: ele traz o que ja esta no GitHub (pull),
#  cria um commit com suas alteracoes e envia (push).
# =============================================================================
set -e

if [ ! -d .git ]; then
  echo "ERRO: esta pasta nao e um clone do repositorio (nao ha .git)."
  echo "Baixe o repositorio uma unica vez com:"
  echo "  git clone https://github.com/anamazza/Indicadores_partos_Brasil2024.git"
  exit 1
fi

git config user.name  >/dev/null 2>&1 || git config user.name  "anamazza"
git config user.email >/dev/null 2>&1 || git config user.email "anamaza.smsrio@gmail.com"

echo ">> Trazendo o que ja esta no GitHub (pull)..."
git pull origin main

echo ">> Adicionando alteracoes e criando commit..."
git add -A
git commit -m "Atualizacao do painel ($(date +%d/%m/%Y))" || echo "   (nada novo para commitar)"

echo ">> Enviando (push)..."
git push origin main

echo ""
echo ">> Pronto! Painel publicado em:"
echo "   https://anamazza.github.io/Indicadores_partos_Brasil2024/"
