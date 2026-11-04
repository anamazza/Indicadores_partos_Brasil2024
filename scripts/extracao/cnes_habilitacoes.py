# -*- coding: utf-8 -*-
"""
cnes_habilitacoes.py
Busca a ficha de cada estabelecimento na API de Dados Abertos do Ministério da Saúde (CNES) e as
habilitações (com competência de início e fim) no serviço do site do CNES — a mesma rota usada pelo
hub Indicadores_Brasil (atualizar_cnes.py). Serve para HGPAR (habilitação 1420), gestão, natureza
jurídica e situação do estabelecimento. Cache por CNES, retomável.
Uso: python cnes_habilitacoes.py <lista_cnes.txt> <saida.json>
"""
import json, os, sys, time, urllib.request

API = "https://apidadosabertos.saude.gov.br/cnes/estabelecimentos/{}"
API_HAB = "https://cnes.datasus.gov.br/services/estabelecimentos-habilitacoes/{}"
HEADERS = {"User-Agent": "Mozilla/5.0", "Referer": "https://cnes.datasus.gov.br/"}

lista, out = sys.argv[1:3]
cnes_lista = [l.strip().zfill(7) for l in open(lista, encoding="utf-8") if l.strip()]
saida = json.load(open(out, encoding="utf-8")) if os.path.exists(out) else {}


def busca(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


erros = 0
for i, cnes in enumerate(cnes_lista, 1):
    if cnes in saida and saida[cnes].get("habilitacoes") is not None:
        continue
    for tent in (1, 2, 3):
        try:
            info = busca(API.format(int(cnes)))
            uid = info.get("codigo_estabelecimento_saude")
            info["habilitacoes"] = busca(API_HAB.format(uid)) if uid else []
            saida[cnes] = info
            break
        except Exception as e:
            if tent == 3:
                erros += 1; saida[cnes] = {"erro": str(e)}
                print(f"[{i}/{len(cnes_lista)}] {cnes} ERRO: {e}", flush=True)
            else:
                time.sleep(5 * tent)
    if i % 25 == 0:
        json.dump(saida, open(out, "w", encoding="utf-8"), ensure_ascii=False)
        print(f"[{i}/{len(cnes_lista)}] gravado", flush=True)
    time.sleep(0.3)
saida["_atualizado_em"] = time.strftime("%Y-%m-%d")
json.dump(saida, open(out, "w", encoding="utf-8"), ensure_ascii=False)
print(f"{len([c for c in saida if not c.startswith('_')])} fichas em {out}; erros: {erros}")
