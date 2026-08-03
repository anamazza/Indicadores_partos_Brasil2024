#!/usr/bin/env bash
# =============================================================================
#  Publica o painel no repositorio:
#  https://github.com/anamazza/novo-painel-partos-2024
#
#  COMO USAR (Windows):
#   1. Crie o repositorio VAZIO em github.com/new com o nome
#      "novo-painel-partos-2024" (sem README, sem .gitignore, sem licenca).
#   2. Abra o "Git Bash" DENTRO desta pasta
#      (clique direito na pasta -> "Git Bash Here").
#   3. Rode:  bash publicar_no_github.sh
#   4. Quando o GitHub pedir login, autorize na janela que abrir.
# =============================================================================
set -e

echo ">> Removendo .git parcial (se existir)..."
rm -rf .git

echo ">> Inicializando repositorio..."
git init
git branch -M main

echo ">> Configurando autor..."
git config user.name  "anamazza"
git config user.email "anamaza.smsrio@gmail.com"

echo ">> Adicionando arquivos e criando commit..."
git add -A
git commit -m "Painel de indicadores obstetricos 2024 + aba de mapa de unidades (com selo x sem selo)"

echo ">> Conectando ao repositorio remoto e enviando..."
git remote add origin https://github.com/anamazza/novo-painel-partos-2024.git
git push -u origin main

echo ""
echo ">> Pronto! Confira em: https://github.com/anamazza/novo-painel-partos-2024"
