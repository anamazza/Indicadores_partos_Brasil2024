# -*- coding: utf-8 -*-
"""
sih_sp_atos.py
Varre os arquivos SP (serviços profissionais da AIH) do SIH/SUS e conta, para os CNES de referência,
os atos profissionais (SP_ATOPROF) por código, em duas atribuições de ano — competência (SP_AA) e
ano da data de saída (SP_DTSAIDA) — contando linhas, quantidade (SP_QTD_ATO) e AIH distintas.
Serve para localizar os códigos de DIU, implante e violência sexual usados na planilha.
Uso: python sih_sp_atos.py <pasta_sp> <aamm_ini> <aamm_fim> <cnes_referencia.txt> <pasta_saida> [UF ...]
"""
import collections, json, os, sys, time

ESTEIRA = r"C:\Users\anapa\OneDrive\Documentos\Projeto Apresentações Internação\Extracao_SIH"
sys.path.insert(0, ESTEIRA)
import datasus_dbc                       # noqa: E402
from dbf_rapido import registros_bytes   # noqa: E402

pasta, aamm_ini, aamm_fim, arq_cnes, out = sys.argv[1:6]
UFS = [u.upper() for u in sys.argv[6:]]
os.makedirs(out, exist_ok=True)
REF = {l.strip().zfill(7) for l in open(arq_cnes, encoding="utf-8") if l.strip()}
CAMPOS = ("SP_CNES", "SP_NAIH", "SP_ATOPROF", "SP_QTD_ATO", "SP_AA", "SP_DTSAIDA")

arqs = sorted(a for a in os.listdir(pasta) if a.startswith("SP") and a.endswith(".dbc") and aamm_ini <= a[4:8] <= aamm_fim)
ufs = sorted({a[2:4] for a in arqs})
if UFS:
    ufs = [u for u in ufs if u in UFS]
print(f"{len(arqs)} arquivos SP {aamm_ini}-{aamm_fim}, {len(ufs)} UFs, {len(REF)} CNES", flush=True)
for uf in ufs:
    destino = os.path.join(out, f"{uf}.json")
    if os.path.exists(destino):
        print(f"{uf}: checkpoint existente, pulando", flush=True); continue
    lin = collections.defaultdict(collections.Counter); qtd = collections.defaultdict(collections.Counter)
    aih = collections.defaultdict(lambda: collections.defaultdict(set))
    lista = [a for a in arqs if a[2:4] == uf]; t0 = time.time(); n = 0
    for i, a in enumerate(lista, 1):
        dados = datasus_dbc.decompress_bytes(open(os.path.join(pasta, a), "rb").read())
        for r in registros_bytes(dados, CAMPOS):
            n += 1
            cnes = r["SP_CNES"].zfill(7)
            if cnes not in REF:
                continue
            p = r["SP_ATOPROF"].zfill(10)
            q = int(r["SP_QTD_ATO"]) if r["SP_QTD_ATO"].isdigit() else 1
            for k in (f"{p}|c{r['SP_AA']}", f"{p}|s{r['SP_DTSAIDA'][:4]}"):
                lin[cnes][k] += 1; qtd[cnes][k] += q; aih[cnes][k].add(r["SP_NAIH"])
        if i % 6 == 0 or i == len(lista):
            print(f"  {uf} {i}/{len(lista)} arquivos, {n:,} linhas ({time.time()-t0:.0f}s)", flush=True)
    json.dump({"uf": uf, "arquivos": lista, "linhas_lidas": n,
               "linhas": {c: dict(v) for c, v in lin.items()}, "qtd": {c: dict(v) for c, v in qtd.items()},
               "aih": {c: {k: len(s) for k, s in v.items()} for c, v in aih.items()}},
              open(destino, "w", encoding="utf-8"), ensure_ascii=False)
    print(f"=== {uf}: {len(lin)} CNES -> {destino} ({time.time()-t0:.0f}s)", flush=True)
print("FIM_SIH_SP_ATOS")
