# -*- coding: utf-8 -*-
"""
cnes_leitos_neo.py
Lê os arquivos LT (leitos por competência) do CNES e guarda, por CNES e competência, os leitos
existentes e SUS dos códigos da unidade neonatal — UTIN (80 tipo I, 81 tipo II, 82 tipo III),
UCINCo (92) e UCINCa (93) — e dos leitos obstétricos (10, 43), além do tipo de gestão, esfera e
natureza jurídica do estabelecimento. Serve para reproduzir UNIDADE NEONATAL COMPLETA, GESTÃO e
NATUREZA JURÍDICA da planilha e testar a competência usada.
Uso: python cnes_leitos_neo.py <pasta_lt> <aamm_ini> <aamm_fim> <saida.json>
"""
import collections, json, os, sys, time

ESTEIRA = r"C:\Users\anapa\OneDrive\Documentos\Projeto Apresentações Internação\Extracao_SIH"
sys.path.insert(0, ESTEIRA)
import datasus_dbc                       # noqa: E402
from dbf_rapido import registros_bytes   # noqa: E402

pasta, aamm_ini, aamm_fim, out = sys.argv[1:5]
CODIGOS = {"80", "81", "82", "92", "93", "10", "43"}
CAMPOS = ("CNES", "CODLEITO", "TP_LEITO", "QT_EXIST", "QT_SUS", "COMPETEN", "TPGESTAO", "ESFERA_A", "NAT_JUR", "NATUREZA", "CODUFMUN")
arqs = sorted(a for a in os.listdir(pasta) if a.startswith("LT") and a.endswith(".dbc") and aamm_ini <= a[4:8] <= aamm_fim)
print(f"{len(arqs)} arquivos LT {aamm_ini}-{aamm_fim}", flush=True)

leitos = collections.defaultdict(dict)       # leitos[cnes][aamm] = {cod: [exist, sus]}
cadastro = {}                                # cadastro[cnes] = {aamm: (gestao, esfera, natjur, natureza, mun)}  última competência
t0 = time.time()
for i, a in enumerate(arqs, 1):
    aamm = a[4:8]
    dados = datasus_dbc.decompress_bytes(open(os.path.join(pasta, a), "rb").read())
    for r in registros_bytes(dados, CAMPOS):
        cnes = r["CNES"].zfill(7)
        cad = cadastro.setdefault(cnes, {})
        if aamm >= max(cad, default="0000"):
            cad[aamm] = (r["TPGESTAO"], r["ESFERA_A"], r["NAT_JUR"], r["NATUREZA"], r["CODUFMUN"])
            for k in [k for k in cad if k != aamm]:
                del cad[k]
        cod = r["CODLEITO"]
        if cod not in CODIGOS:
            continue
        ex = int(r["QT_EXIST"]) if r["QT_EXIST"].isdigit() else 0
        su = int(r["QT_SUS"]) if r["QT_SUS"].isdigit() else 0
        d = leitos[cnes].setdefault(aamm, {})
        v = d.setdefault(cod, [0, 0])
        v[0] += ex; v[1] += su
    if i % 27 == 0 or i == len(arqs):
        print(f"  {i}/{len(arqs)} ({time.time()-t0:.0f}s)", flush=True)

json.dump({"arquivos": arqs, "leitos": leitos,
           "cadastro": {c: {"aamm": k, "tpgestao": v[0], "esfera": v[1], "nat_jur": v[2], "natureza": v[3], "codufmun": v[4]}
                        for c, cad in cadastro.items() for k, v in cad.items()}},
          open(out, "w", encoding="utf-8"), ensure_ascii=False)
print(f"{len(leitos)} CNES com leitos de interesse; {len(cadastro)} CNES no cadastro -> {out} ({time.time()-t0:.0f}s)")
