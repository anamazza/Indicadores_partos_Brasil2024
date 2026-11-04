# -*- coding: utf-8 -*-
"""
sih_partos.py
Varre os arquivos RD (AIH reduzida) do SIH/SUS e conta, por CNES, os procedimentos de parto,
AMIU/curetagem e laqueadura pós-parto, em três atribuições de ano — competência (ANO_CMPT),
data de internação (DT_INTER) e data de saída (DT_SAIDA) — para calibrar contra a planilha.
Para os CNES de referência (planilha de 2024) guarda também a distribuição completa de
PROC_REA por ano de competência, para localizar os códigos de DIU, implante e violência sexual.
Lê os .dbc já baixados pela esteira Extracao_SIH (datasus_dbc + dbf_rapido) e grava um
checkpoint por UF, retomável.
Uso: python sih_partos.py <pasta_rd> <aamm_ini> <aamm_fim> <cnes_referencia.txt> <pasta_saida> [UF ...]
"""
import collections, json, os, sys, time

ESTEIRA = r"C:\Users\anapa\OneDrive\Documentos\Projeto Apresentações Internação\Extracao_SIH"
sys.path.insert(0, ESTEIRA)
import datasus_dbc                       # noqa: E402
from dbf_rapido import registros_bytes   # noqa: E402

pasta_rd, aamm_ini, aamm_fim, arq_cnes, out = sys.argv[1:6]
UFS = [u.upper() for u in sys.argv[6:]]
os.makedirs(out, exist_ok=True)
REF = {l.strip().zfill(7) for l in open(arq_cnes, encoding="utf-8") if l.strip()}

PARTO_VAGINAL = {"0310010039", "0310010047", "0310010055"}
CESARIANA = {"0411010026", "0411010034", "0411010042"}
LAQ_PV = "0409060313"                       # laqueadura na internação do parto normal (vigente desde 04/2024)
AMIU, CURET, CURET_SEMIO = "0409060070", "0411020013", "0409060046"
INTERESSE = PARTO_VAGINAL | CESARIANA | {LAQ_PV, AMIU, CURET, CURET_SEMIO}
CAMPOS = ("CNES", "PROC_REA", "ANO_CMPT", "DT_INTER", "DT_SAIDA", "IDENT", "SEXO", "IDADE", "COD_IDADE")

arqs = sorted(a for a in os.listdir(pasta_rd)
              if a.startswith("RD") and a.endswith(".dbc") and aamm_ini <= a[4:8] <= aamm_fim)
ufs = sorted({a[2:4] for a in arqs})
if UFS:
    ufs = [u for u in ufs if u in UFS]
print(f"{len(arqs)} arquivos RD {aamm_ini}-{aamm_fim}, {len(ufs)} UFs, {len(REF)} CNES de referência", flush=True)

for uf in ufs:
    destino = os.path.join(out, f"{uf}.json")
    if os.path.exists(destino):
        print(f"{uf}: checkpoint existente, pulando", flush=True); continue
    cont = collections.defaultdict(collections.Counter)      # cont[cnes][(proc, atribuição)]
    todos = collections.defaultdict(collections.Counter)     # todos[cnes][(proc, ano_cmpt)] só p/ referência
    t0 = time.time(); n = 0
    lista = [a for a in arqs if a[2:4] == uf]
    for i, a in enumerate(lista, 1):
        dados = datasus_dbc.decompress_bytes(open(os.path.join(pasta_rd, a), "rb").read())
        for r in registros_bytes(dados, CAMPOS):
            n += 1
            cnes = r["CNES"].zfill(7)
            p = r["PROC_REA"]
            ac = r["ANO_CMPT"]
            if cnes in REF:
                todos[cnes][(p, ac)] += 1
            if p not in INTERESSE:
                continue
            c = cont[cnes]
            ai, asd = r["DT_INTER"][:4], r["DT_SAIDA"][:4]
            c[(p, "c" + ac)] += 1
            c[(p, "i" + ai)] += 1
            c[(p, "s" + asd)] += 1
            if r["IDENT"] == "5":
                c[(p, "ident5_c" + ac)] += 1
            if r["SEXO"] not in ("3", "2", "F"):
                c[(p, "naofem_c" + ac)] += 1
        if i % 8 == 0 or i == len(lista):
            print(f"  {uf} {i}/{len(lista)} arquivos, {n:,} AIH ({time.time()-t0:.0f}s)", flush=True)
    json.dump({"uf": uf, "arquivos": lista, "aih_lidas": n,
               "procedimentos": {cnes: {f"{p}|{k}": v for (p, k), v in c.items()} for cnes, c in cont.items()},
               "referencia_todos_proc": {cnes: {f"{p}|{k}": v for (p, k), v in c.items()} for cnes, c in todos.items()}},
              open(destino, "w", encoding="utf-8"), ensure_ascii=False)
    print(f"=== {uf}: {len(cont)} CNES com procedimentos de interesse -> {destino} ({time.time()-t0:.0f}s)", flush=True)
print("FIM_SIH_PARTOS")
